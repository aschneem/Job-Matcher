"""Engine to run all matchers with all posts and resumes"""

class MatcherEngine():
    """Engine to run all matchers with all posts and resumes"""

    def __init__(self, matchers, post_repository, resume_repository):
        self.matchers = matchers
        self.post_repository = post_repository
        self.resume_repository = resume_repository

    def get_default_score(self):
        """Gets the default score to display"""
        for matcher in self.matchers:
            if matcher.is_default_matcher():
                return matcher.get_matcher_name()
        return self.matchers[0].get_matcher_name()

    def run(self):
        """Runs all matchers against all posts and resume combinations"""
        for matcher in self.matchers:
            matcher.initialize()
        resume_data = self.resume_repository.get_all_resumes()
        post_data = self.post_repository.get_all_posts_for_matcher()
        for post in post_data:
            scores = {}
            for matcher in self.matchers:
                scores[matcher.get_matcher_name()] = {}
                for resume in resume_data:
                    scores[matcher.get_matcher_name()][resume['name']] = matcher.match(post, resume)
            post['match_data'] = scores
            self.post_repository.update_post(post['contentID'], post)
            scores['contentID'] = post['contentID']
