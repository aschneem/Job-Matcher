"""Service to interact with the browser through playwright"""
from datetime import datetime
import hashlib
import re
from time import sleep
from playwright.async_api import async_playwright

class BrowserService():
    """Service to interact with the browser through playwright"""
    def __init__(self):
        self.pages = {}
        self.results = {}
        self.sha1 = hashlib.sha1()

    def run_script(self, script):
        """Runs a script"""
        self.run_script_async(script)

    def get_script_run_id(self, name):
        """Gets an id for a script run"""
        time = str(datetime.now().timestamp)
        self.sha1.update((name+time).encode('utf-8'))
        return  self.sha1.hexdigest()

    async def run_script_async(self, script):
        """Runs a script asynchronously"""
        run_id = self.get_script_run_id(script.get('name', 'untitled'))
        self.results[run_id] = {}
        async with async_playwright() as playwright:
            browser = await self.get_browser(playwright, script)
            context = await browser.new_context()
            page = await context.new_page()
            self.pages[run_id] = page
            for action in script['actions']:
                await self.execute_action(action, run_id, {})
            del self.pages[run_id]
            await browser.close()
        return self.results[run_id]

    async def get_browser(self, playwright, script):
        """Launches a browser instance"""
        chomium = playwright.chromium
        browser = await chomium.launch(headless=script.get('headless', False))
        return browser

    async def execute_action(self, action, run_id, context):
        """Executes the current action"""
        print(action)
        if action['action'] == 'Nav':
            await self.navigate(action, run_id)
        elif action['action'] == 'Click':
            await self.click(action, run_id, context)
        elif action['action'] == 'Fill':
            await self.fill(action, run_id, context)
        elif action['action'] == 'Sleep':
            sleep(action['actionValue'])
        elif action['action'] == 'SetResult':
            await self.set_result(action, run_id, context)
        elif action['action'] == 'Loop':
            print('in loop')
            elements = await self.get_target_element(action, run_id, context)
            print(elements)
            for element in elements:
                for loop_action in action['loopActions']:
                    await self.execute_action(loop_action, run_id, element)
        elif action['action'] == 'Evaluate':
            await self.evaluate(action, run_id, context)
        elif action['action'] == 'Back':
            await self.go_back(run_id)
        else:
            raise NotImplementedError()

    async def navigate(self, action, run_id):
        """Navigate the page to a URL"""
        url = action.get('targetKey', '')
        if 'actionValue' in action.keys():
            url = url.format(action['actionValue'])
        await self.pages[run_id].goto(url)

    async def click(self, action, run_id, context):
        """Click on a particular element"""
        target = await self.get_target_element(action, run_id, context)
        await target.click()

    async def fill(self, action, run_id, context):
        """Fill the target input with the action value"""
        target = await self.get_target_element(action, run_id, context)
        await target.fill(action['actionValue'])

    async def evaluate(self, action, run_id, context):
        """Evaluates JS code on the context of the target element"""
        target = await self.get_target_element(action, run_id, context)
        await target.evaluate(action['actionValue'])

    async def go_back(self, run_id):
        """navigates the browser back to the previous page"""
        await self.pages[run_id].go_back()

    async def get_target_element(self, action, run_id, context):
        """Get the target element for an action"""
        get_by = action['targetGetBy']
        page = self.pages[run_id]
        if get_by == 'role':
            return await page.get_by_role(action['targetRole'],
                                          name=self.get_target_key(action),
                                          exact=action.get('targetKeyExact', False))
        elif get_by == 'placeholder':
            return page.get_by_placeholder(self.get_target_key(action),
                                                 exact=action.get('targetKeyExact', False))
        elif get_by == 'css':
            return await page.locator('css='+action['targetKey']).all()
        elif get_by == 'label':
            return await page.get_by_label(self.get_target_key(action),
                                           exact=action.get('targetKeyExact', False))
        elif get_by == 'text':
            return await page.get_by_text(self.get_target_key(action),
                                          exact=action.get('targetKeyExact', False))
        elif get_by == 'result':
            return self.results[run_id]
        elif get_by == 'context':
            return context
        raise NotImplementedError()

    def get_target_key(self, action):
        """Gets the appropriate value to use as the target key"""
        if action.get('targetKeyType', 'string') == 'RegEx':
            return re.compile(action['targetKey'])
        return action['targetKey']

    async def set_result(self, action, run_id, context):
        """Sets the specified field in the result object"""
        action_values = action['actionValue'].split('|')
        field = action_values[0]
        key = action_values[1]
        value_name = action_values[2]
        value = await self.get_value(action, value_name, run_id, context)
        if len(key) == 0:
            self.results[run_id][field] = value
        elif key == 'append':
            self.results[run_id][field].append(value)
        else:
            self.results[run_id][field][key] = value

    async def get_value(self, action, value_name, run_id, context):
        """Gets the specified value"""
        if value_name == '{}':
            return {}
        if value_name == '[]':
            return []
        target = await self.get_target_element(action, run_id, context)
        if action['targetGetBy'] == 'result':
            return target[value_name]
        else:
            if value_name == 'text_content':
                return await target.text_content()
            elif value_name == 'inner_html':
                return await target.inner_html()
            raise NotImplementedError()
