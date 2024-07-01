"""Helper function to convert a search definition to a browser service script"""
import random

def add_search_to_script_actions(search, actions, keyword):
    """Adds the actions for a keyword search to the script"""
    if search['searchBoxGetBy'] == 'url':
        actions.append({'action': 'Nav',
                        'actionValue':keyword.replace(' ', search.get('searchSpaceChar', '%20')),
                        'targetKey': search['searchUrl']})
        actions.append({'action': 'Sleep', 'actionValue': 1})
    else:
        actions.append({'action': 'Click', 'targetGetBy': search['searchBoxGetBy'],
                        'targetKey': search['searchBoxKey'],
                        'targetRole': search.get('searchBoxRole', ''),
                        'targetKeyExact': search.get('searchBoxKeyExact', False)})
        actions.append({'action': 'Fill', 'actionValue':keyword,
                        'targetGetBy': search['searchBoxGetBy'],
                        'targetKey': search['searchBoxKey'],
                        'targetRole': search.get('searchBoxRole', ''),
                        'targetKeyExact': search.get('searchBoxKeyExact', False)})
        actions.append({'action': 'Click', 'targetGetBy': search['searchButtonGetBy'],
                        'targetKey': search['searchButtonKey'],
                        'targetRole': search.get('searchButtonRole', ''),
                        'targetKeyExact': search.get('searchButtonKeyExact', False)})
        actions.append({'action': 'Sleep', 'actionValue': 1})
    print('Filters')
    print(search.get('filters', []))
    for content_filter in search.get('filters', []):
        print(content_filter)
        actions.append({'action': 'Click', 'targetGetBy': content_filter['getBy'],
                        'targetKey': content_filter['key'],
                        'targetKeyType': content_filter.get('type', 'string'),
                        'targetKeyExact': content_filter.get('keyExact', False),
                        'targetRole': content_filter.get('role', '')})
        if 'fill' in content_filter.keys():
            actions.append({'action': 'Fill', 'actionValue': content_filter['fill'],
                            'targetGetBy': content_filter['getBy'],
                            'targetKey': content_filter['key'],
                            'targetKeyType': content_filter.get('type', 'string'),
                            'targetKeyExact': content_filter.get('keyExact', False),
                            'targetRole': content_filter.get('role', '')})
            actions.append({'action': 'Press', 'actionValue': 'Tab',
                            'targetGetBy': content_filter['getBy'],
                            'targetKey': content_filter['key'],
                            'targetKeyType': content_filter.get('type', 'string'),
                            'targetKeyExact': content_filter.get('keyExact', False),
                            'targetRole': content_filter.get('role', '')})
        actions.append({'action': 'Sleep', 'actionValue': 1})
    actions.append({'action': 'Sleep', 'actionValue': 5})
    add_crawl_results_to_actions(search, actions)

def add_crawl_results_to_actions(search, actions):
    """Add the actions to crawl a results page for posts to the script actions"""
    actions.append({'action': 'SetResult', 'actionValue': 'results||[]'})
    loop_actions = []
    loop_actions.append({'action': 'Evaluate',
                         'actionValue': 'element => element.target = ""', 'targetGetBy': 'context'})
    loop_actions.append({'action': 'SetResult', 'actionValue': 'temp||{}'})
    loop_actions.append({'action': 'SetResult',
                         'actionValue': 'temp|postLink|text_content', 'targetGetBy': 'context'})
    loop_actions.append({'action': 'Click', 'targetGetBy': 'context'})
    loop_actions.append({'action': 'Sleep', 'actionValue': 1})
    if 'extraDelay' in search.keys():
        loop_actions.append({'action': 'Sleep',
                             'actionValue': search['extraDelay'] + 5*random.random()})
    loop_actions.append({'action': 'SetResult',
                         'actionValue': 'tempTexts||[]', 'targetGetBy': 'context'})
    loop_actions.append({'action': 'SetResult',
                         'actionValue': 'tempHtmls||[]', 'targetGetBy': 'context'})
    loop_actions.append({'action': 'Loop', 'actionValue': search.get('pageMax', ''),
                         'targetGetBy': 'css', 'targetKey': search['jobPostsContentCSSSelector'],
                       'loopActions': [
                           {'action': 'SetResult',
                            'actionValue': 'tempTexts|append|text_content',
                            'targetGetBy': 'context'},
                           {'action': 'SetResult',
                            'actionValue': 'tempHtmls|append|inner_html',
                            'targetGetBy': 'context'}]})
    loop_actions.append({'action': 'SetResult',
                         'actionValue': 'temp|text|tempTexts', 'targetGetBy': 'result'})
    loop_actions.append({'action': 'SetResult',
                         'actionValue': 'temp|html|tempHtmls', 'targetGetBy': 'result'})
    loop_actions.append({'action': 'SetResult',
                         'actionValue': 'temp|url|url', 'targetGetBy': 'context'})
    loop_actions.append({'action': 'SetResult',
                         'actionValue': 'results|append|temp', 'targetGetBy': 'result'})
    if 'backToSearchGetBy' in search.keys():
        if search['backToSearchGetBy'] == 'back':
            loop_actions.append({'action': 'Back'})
        else:
            loop_actions.append({'action': 'Click', 'targetGetBy': search['backToSearchGetBy'],
                                 'targetKey': search['backToSearchKey'],
                                 'targetRole': search.get('backToSearchRole', '')})
    actions.append({'action': 'Loop', 'targetGetBy': 'css',
                    'targetKey': search['jobPostsCSSSelector'],
                     'loopActions':loop_actions})

def convert_search_to_script(search, keywords):
    """Converts the given search configuration to a browser service script"""
    print("BUILDING SCRIPT")
    script = { 'name': search['name'] }
    actions = []
    actions.append({'action': 'Nav', 'actionValue': '', 'targetKey': search['url']})
    actions.append({'action': 'Sleep', 'actionValue': 1})
    if 'acceptCookiesGetBy' in search.keys():
        actions.append({'action': 'Click', 'targetGetBy': search['acceptCookiesGetBy'],
                        'targetKey': search['acceptCookiesKey'],
                        'targetRole': search['acceptCookiesRole']})
    if 'searchBoxGetBy' in search.keys():
        for keyword in keywords:
            add_search_to_script_actions(search, actions, keyword)
    else:
        add_crawl_results_to_actions(search, actions)
    script['actions'] = actions
    script['headless'] = search['headless']
    print(search)
    print(script)
    print('SCRIPT COMPLETE')
    return script
