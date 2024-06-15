"""Service to execute search definitions to save new job posts"""
# pylint: disable=W0718
import urllib
from time import sleep
import re
from datetime import datetime
import random
import asyncio
from playwright.async_api import async_playwright
from matchers.matcher_engine import MatcherEngine
from repositories.job_post_mongo_repository import JobPostRepository
from repositories.resume_mongo_repository import ResumeRepository
from repositories.search_mongo_repository import SearchRepository
from services.analyzer_service import AnalyzerService
from playwright._impl._errors import TimeoutError as Timeout

class SearchPostsService():
    """Service to execute search definitions to save new job posts"""

    def __init__(self, search_repo: SearchRepository, post_repo: JobPostRepository,
                 resume_repo: ResumeRepository,
                 matcher: MatcherEngine, analyzer: AnalyzerService):
        self.analyzer = analyzer
        self.search_repo = search_repo
        self.post_repo = post_repo
        self.resume_repo = resume_repo
        self.matcher = matcher
        self.playwright = None
        self.playwright_context = None
        self.page = None

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

    async def search_for_posts_async(self, config, search_keywords):
        """Starts an async playwright instance and performs the search with it"""
        async with async_playwright() as playwright:
            self.playwright = playwright
            chromium = self.playwright.chromium
            browser = await chromium.launch(headless=config.get('headless', False))
            self.playwright_context = await browser.new_context()
            self.page = await self.playwright_context.new_page()
            self.search_repo.save_search_run_data(config['name'],
                                                  {"search_status": "start",
                                                   'search_start_time': str(datetime.now())})
            error_encountered = False
            try:
                await self.page.goto(config['url'])
                await self.accept_cookies_async(config)
                if 'searchBoxGetBy' in  config:
                    await self.perform_keyword_searches(config, search_keywords)
                elif 'jobPostsCSSSelector' in config:
                    await self.crawl_results_page(config)
            except Timeout as e:
                print('Encountered error running search ' + config['name'] + ": " + str(e))
                self.search_repo.save_search_run_data(config['name'],
                                              {"search_status": "error",
                                               'search_end_time': str(datetime.now())})
                error_encountered = True
            finally:
                await browser.close()
                self.playwright = None
                self.playwright_context = None
                self.page = None
        if not error_encountered:
            self.search_repo.save_search_run_data(config['name'],
                                                {"search_status": "complete",
                                                'search_end_time': str(datetime.now())})
        self.matcher.run()

    def analyze_resumes(self):
        """Analyze resumes"""
        resumes = self.resume_repo.get_all_resumes()
        for resume in resumes:
            data = self.analyzer.analyze(resume['text'], resume)
            self.resume_repo.update_resume(resume['name'], data)

    async def accept_cookies_async(self, config):
        """If defined accept cookies on the page to remove popup"""
        if "acceptCookiesGetBy" in config:
            if config["acceptCookiesGetBy"] == 'role':
                await self.page.get_by_role(config['acceptCookiesRole'],
                                            name=config['acceptCookiesKey']).click()

    async def crawl_results_page(self, config, keywords=""):
        """Crawl a search result page"""
        sleep(10)
        search_data = { 'search' : keywords, 'timestamp': str(datetime.now()),
                        'searchName':config.get('name', '') }
        posts = self.page.locator("css="+config["jobPostsCSSSelector"]).all()
        posts = await posts
        if 'pageMax' in config:
            posts = posts[0:config['pageMax']]
        for post in posts:
            post_data = search_data.copy()
            await post.evaluate("element => element.target = ''")
            try:
                post_data['postLink'] = await post.text_content()
            except Exception:
                await self.go_back_to_results(config)
                continue
            await post.click()
            sleep(1)
            if 'extraDelay' in config.keys():
                sleep(config["extraDelay"] + 5*random.random())
            post_data['url'] = self.page.url
            print(post_data['url'])
            post_content = self.page.locator("css="+config['jobPostsContentCSSSelector'])
            try:
                locator_count = await post_content.count()
            except Exception:
                await self.go_back_to_results(config)
                print('Error finding text')
                continue
            if not locator_count == 1:
                await self.go_back_to_results(config)
                print('Text found at ' + str(locator_count) + 'locations')
                continue
            text = await post_content.text_content()
            html = "<html><body>" + await post_content.inner_html() + "</body></html>"
            content_id = self.post_repo.sha1_value(self.post_repo.normalize(text))
            print(content_id)
            print(self.post_repo.post_exists(content_id))
            if not self.post_repo.post_exists(content_id):
                meta = self.analyzer.analyze(self.post_repo.normalize(text), post_data)
                self.post_repo.save_post(text, html, meta)
            await self.go_back_to_results(config)

    async def go_back_to_results(self, config):
        """Return to search results from a post"""
        if 'backToSearchGetBy' in config:
            if config['backToSearchGetBy'] == 'role':
                try:
                    await self.page.get_by_role(config['backToSearchRole'],
                                                name=config['backToSearchKey']).click()
                except Exception:
                    await self.page.go_back()
            elif config['backToSearchGetBy'] == 'label':
                try:
                    await self.page.get_by_label(config['backToSearchKey']).click()
                except Exception:
                    await self.page.go_back()
            elif config['backToSearchGetBy'] == 'back':
                    await self.page.go_back()


    async def perform_keyword_searches(self, config, search_keywords):
        """Perform a keyword searches"""
        for search in search_keywords:
            await self.perform_keyword_search(config, search)
            if 'jobPostsCSSSelector' in config:
                await self.crawl_results_page(config, search)
            await self.page.goto(config['url'])

    async def perform_keyword_search(self, config, search):
        """Perfom a keyword search"""
        if "preSearchLink" in config:
            await self.page.get_by_role("link", name=config['preSearchLink']).click()
        if config['searchBoxGetBy'] == 'placeholder':
            await self.page.get_by_placeholder(config['searchBoxKey'],
                                               exact=config.get('searchBoxKeyExact', False)
                                               ).click()
            await self.page.get_by_placeholder(config['searchBoxKey'],
                                               exact=config.get('searchBoxKeyExact', False)
                                               ).fill(search)
        elif config['searchBoxGetBy'] == 'label':
            await self.page.get_by_label(config['searchBoxKey']).click()
            await self.page.get_by_label(config['searchBoxKey']).fill(search)
        elif config['searchBoxGetBy'] == 'url':
            if 'searchSpaceChar' in config.keys():
                search = search.replace(' ', config['searchSpaceChar'])
            url_search = config['searchUrl'].replace('{search}', urllib.parse.quote(search))
            await self.page.goto(url_search)
        elif config['searchBoxGetBy'] == "role":
            await self.page.get_by_role(config["searchBoxGetByRole"],
                                        name=config['searchBoxKey']).click()
            await self.page.get_by_role(config["searchBoxGetByRole"],
                                        name=config['searchBoxKey']).fill(search)
        if 'searchButtonGetBy' in config:
            if config['searchButtonGetBy'] == 'role':
                await self.page.get_by_role(config['searchButtonRole'],
                                            name=config['searchButtonKey'],
                                            exact=config.get('searchButtonKeyExact', False)).click()
            elif config['searchButtonGetBy'] == 'label':
                await self.page.get_by_label(config['searchButtonKey']).click()
            elif config['searchButtonGetBy'] == 'css':
                await self.page.locator("css="+config["searchButtonKey"]).click()
        if 'filters' in config:
            await self.apply_filters(config)
            sleep(5)

    async def apply_filters(self, config):
        """Apply filters to the search"""
        for content_filter in config['filters']:
            try:
                key = content_filter['key']
                if content_filter.get('type', '') == 're':
                    key = re.compile(key)
                if content_filter["getBy"] == 'label':
                    await self.page.get_by_label(key).click()
                elif content_filter["getBy"] == 'placeholder':
                    await self.page.get_by_placeholder(key).click()
                    if "fill" in content_filter:
                        await self.page.get_by_placeholder(key).fill(content_filter["fill"])
                        await self.page.get_by_placeholder(key).press("Tab")
                elif content_filter["getBy"] == 'role':
                    await self.page.get_by_role(content_filter['role'], name=key,
                                                exact=content_filter.get("keyExact", False)).click()
                elif content_filter["getBy"] == 'text':
                    await self.page.get_by_text(key)
                sleep(1)
            except Exception:
                continue
