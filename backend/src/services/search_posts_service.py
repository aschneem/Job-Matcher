"""Service to execute search definitions to save new job posts"""
# pylint: disable=W0718
from datetime import datetime
import asyncio
import random
from helpers import search_script_generator
from matchers.matcher_engine import MatcherEngine
from repositories.job_post_mongo_repository import JobPostRepository
from repositories.resume_mongo_repository import ResumeRepository
from repositories.script_mongo_repository import ScriptRepository
from repositories.search_mongo_repository import SearchRepository
from services.analyzer_service import AnalyzerService
from services.browser_service import BrowserService

class SearchPostsService():
    """Service to execute search definitions to save new job posts"""

    def __init__(self, search_repo: SearchRepository, post_repo: JobPostRepository,
                 resume_repo: ResumeRepository,
                 matcher: MatcherEngine, analyzer: AnalyzerService, 
                 browser_service: BrowserService,
                 script_repo: ScriptRepository):
        self.analyzer = analyzer
        self.search_repo = search_repo
        self.post_repo = post_repo
        self.resume_repo = resume_repo
        self.script_repo = script_repo
        self.matcher = matcher
        self.browser_service = browser_service

    def search_all_posts(self, search_keywords):
        """Perform all searches"""
        search_config = self.search_repo.get_search_configs()
        random.shuffle(search_config)
        self.analyze_resumes()
        for config in search_config:
            print(config)
            try:
                self.search_for_posts(config, search_keywords)
            except Exception as e:
                print('Encountered error for ' + config['name'] + ' ' + str(e))
                continue
        self.matcher.run()

    def search_for_posts(self, config, search_keywords):
        """Starts an async run of a particular search"""
        if config.get('skip', False):
            return
        asyncio.run(self.search_for_posts_async(config, search_keywords))

    def get_script_for_search(self, config, search_keywords):
        """Gets a search script for the search configuration"""
        if 'searchScript' in config:
            return self.script_repo.get_script(config['searchScript'])
        return search_script_generator.convert_search_to_script(config, search_keywords)

    async def search_for_posts_async(self, config, search_keywords):
        """Starts an async playwright instance and performs the search with it"""
        script = self.get_script_for_search(config, search_keywords)
        self.search_repo.save_search_run_data(config['name'],
                                                  {"search_status": "start",
                                                   'search_start_time': str(datetime.now())})
        error_encountered = False
        try:
            script_results = await self.browser_service.run_script_async(script)
            await self.process_results(config, script_results)
        except Exception as e:
            print('Encountered error running search ' + config['name'] + ": " + str(e))
            self.search_repo.save_search_run_data(config['name'],
                                        {"search_status": "error",
                                            'search_end_time': str(datetime.now())})
            error_encountered = True
        if not error_encountered:
            self.search_repo.save_search_run_data(config['name'],
                                                {"search_status": "complete",
                                                'search_end_time': str(datetime.now())})
        self.matcher.run(status='created')

    def analyze_resumes(self):
        """Analyze resumes"""
        resumes = self.resume_repo.get_all_resumes()
        for resume in resumes:
            data = self.analyzer.analyze(resume['text'], resume)
            self.resume_repo.update_resume(resume['name'], data)

    async def process_results(self, config, results):
        """process search results"""
        search_data = { 'timestamp': str(datetime.now()),
                        'searchName':config.get('name', '') }
        for post in results['results']:
            post_data = search_data.copy()
            post_data['postLink'] = post.get('postLink', '')
            post_data['url'] = post.get('url', '')
            print(post_data['url'])
            text = '\n'.join(post.get('text', []))
            html = '<html><body>' + '\n'.join(post.get('html', [])) + "</body></html>"
            content_id = self.post_repo.sha1_value(self.post_repo.normalize(text))
            print(content_id)
            print(self.post_repo.post_exists(content_id))
            if not self.post_repo.post_exists(content_id):
                meta = self.analyzer.analyze(self.post_repo.normalize(text), post_data)
                self.post_repo.save_post(text, html, meta)
