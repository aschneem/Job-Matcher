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
        time = datetime.now().timestamp
        self.sha1.update((name+time).encode('utf-8'))
        return  self.sha1.hexdigest()

    async def run_script_async(self, script):
        """Runs a script asynchronously"""
        run_id = self.get_script_run_id(script.get('name', 'untitled'))
        async with async_playwright() as playwright:
            browser = self.get_browser(playwright, script)
            context = await browser.new_context()
            page = await context.new_page()
            self.pages[run_id] = page
            for action in script['actions']:
                self.execute_action(action, run_id)
            del self.pages[run_id]
            await browser.close()

    async def get_browser(self, playwright, script):
        """Launches a browser instance"""
        chomium = playwright.chromium
        browser = await chomium.launch(headless=script.get('headless', False))
        return browser

    async def execute_action(self, action, run_id):
        """Executes the current action"""
        if action == 'Nav':
            await self.navigate(action, run_id)
        elif action == 'Click':
            await self.click(action, run_id)
        elif action == 'Fill':
            await self.fill(action, run_id)
        elif action == 'Sleep':
            sleep(action['actionValue'])
        elif action == 'SetResult':
            pass
        elif action == 'Loop':
            pass

    async def navigate(self, action, run_id):
        """Navigate the page to a URL"""
        url = action['targetKey']
        if 'actionValue' in action.keys():
            url = url.format(action['actionValue'])
        await self.pages[run_id].goto(url)

    async def click(self, action, run_id):
        """Click on a particular element"""
        target = await self.get_target_element(action, run_id)
        await target.click()

    async def fill(self, action, run_id):
        """Fill the target input with the action value"""
        target = await self.get_target_element(action, run_id)
        await target.fill(action['actionValue'])

    async def get_target_element(self, action, run_id):
        """Get the target element for an action"""
        get_by = action['targetGetBy']
        page = self.pages[run_id]
        if get_by == 'role':
            return await page.get_by_role(action['targetRole'],
                                          name=self.get_target_key(action),
                                          exact=action.get('targetKeyExact', False))
        elif get_by == 'placeholder':
            return await page.get_by_placeholder(self.get_target_key(action),
                                                 exact=action.get('targetKeyExact', False))
        elif get_by == 'css':
            return await page.locator('css='+action['targetKey'])
        elif get_by == 'label':
            return await page.get_by_label(self.get_target_key(action),
                                           exact=action.get('targetKeyExact', False))
        elif get_by == 'text':
            return await page.get_by_text(self.get_target_key(action),
                                          exact=action.get('targetKeyExact', False))

    def get_target_key(self, action):
        """Gets the appropriate value to use as the target key"""
        if action.get('targetKeyType', 'string') == 'RegEx':
            return re.compile(action['targetKey'])
        return action['targetKey']
