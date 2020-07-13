import asyncio
from pyppeteer import launch
import time
import random
from collections import Counter

"""
可执行
获取国家统计局标准地区信息
可改进点：使用redis存储队列和虑重
"""
async def get_region():
    browser = await launch({'headless': True, 'args': ['--no-sandbox']})
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(30000000)
    await page.setUserAgent(get_random_user_agent())
    fp = open('areas.txt', 'w+')
    handled = {}
    urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html']
    while urls:
        url = urls.pop()
        if handled.get(url) is None:
            await page.goto(url)
            items = await page.xpath('//tr[@class="provincetr"]/td/a')
            if len(items) == 0:
                items = await page.xpath('//tr/td[2]/a')
            for item in items:
                text = await (await item.getProperty('textContent')).jsonValue()
                href = await (await item.getProperty('href')).jsonValue()
                fp.write(href + "\t" + text + "\n")
                if Counter(href)['/'] <= 8:
                    urls.append(href)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), text, href, len(items))
            time.sleep(random.randint(2, 5))
        else:
            handled[url] = 1
    fp.close()


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.16",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Cortana 1.11.6.17763; 10.0.0.0.17763.1098) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763 RestrictedAPI",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; ru; rv:1.9.2.28) Gecko/20120306 Firefox/3.6.28",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/75.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; MASPJS; rv:11.0) like Gecko",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Safari/537.36 OPR/55.2.2719.50740,gzip(gfe)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.94",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 OPR/67.0.3575.97",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_14_6) AppleWebKit/905.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15"
    ]
    return random.choice(user_agents)

if __name__ == '__main__':
    print("Start")
    asyncio.get_event_loop().run_until_complete(get_region())
    print("Finish")
