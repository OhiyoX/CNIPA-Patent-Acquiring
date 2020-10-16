import asyncio
from pyppeteer import launch
import tkinter
import os
import json


class Patent():
    def __init__(self):
        self.page = None

    async def launch(self):
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()

        browser = await launch(headless=False,
                               args=[f'--window-size={width},{height}'],
                               ignoreDefaultArgs="enable-automation")
        self.page = await browser.newPage()
        await self.page.setViewport(viewport={'width': width, 'height': height})
        await self.page.goto('http://cpquery.cnipa.gov.cn/')
        await self.page.evaluate(
            '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        # await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await self.page.waitForSelector("#publiclogin")
        await self.page.waitForNavigation()

    async def login(self):
        with open('danger/config.json', encoding="UTF-8") as f:
            auth = json.load(f)

        username = await self.page.waitForSelector("#username1")
        await username.type(auth["account_text"])
        password = await self.page.waitForSelector("#password1")
        await password.type(auth["password_text"])

        wait = input("authentication-done:")
        login = await self.page.waitForSelector("#publiclogin")
        await login.click()
        await asyncio.sleep(2)
        agree = await self.page.waitForSelector("#agreeid")
        await agree.click()
        await asyncio.sleep(0.5)
        go_btn = await self.page.waitForSelector("#goBtn")
        await go_btn.click()

    async def search(self, company=""):
        if company == "":
            company = "苏宁控股集团有限公司"
        applicant = await self.page.waitForSelector('#select-key\:shenqingrxm')
        await applicant.type(company)

    async def screenshot_dom_elem(self):
        auth = self.page.querySelector('#authImg')
        x,y,width,height = await auth.boundingBox()
        if width*height !=0:
            if not os.path.exists('temp/'):
                os.mkdir('temp/')
            await self.page.screenshot(path='temp/authImg.jpg',type='jpeg',clip={x,y,width,height})

    async def run(self):
        await self.launch()
        await self.login()
        # wait = input('...')


def main():
    pt = Patent()
    asyncio.get_event_loop().run_until_complete(pt.run())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
