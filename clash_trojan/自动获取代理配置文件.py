import asyncio
import aiohttp
import re
​
url = 'https://fofa.info/result?qbase64=Ym9keT0i6Ieq5Yqo5oqT5Y+WdGfpopHpgZPjgIHorqLpmIXlnLDlnYDjgIHlhazlvIDkupLogZTnvZHkuIrnmoRzc+OAgVNTcuOAgXZtZXNz44CBdHJvamFu6IqC54K55L+h5oGvIg=='
​
async def fetch(session, url):
    async with session.get(url, verify_ssl=False, timeout=2) as response:
        return await response.text()
​
async def main():
    async with aiohttp.ClientSession() as session:
        res = await session.get(url)
        res_text = await res.text()
        ip = re.findall('class="hsxa-host"><a href="(.*?)"', res_text)
​
        tasks = []
        for i in ip:
            new_ip = i + '/clash/proxies'
            tasks.append(asyncio.create_task(fetch(session, new_ip)))
​
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result, i in zip(results, ip):
            if isinstance(result, Exception):
                print(f"{i}----请求超时!")
                continue
            file_name = re.sub(r'[\\/:\*\?"<>\|]', '-', i)
            with open(file_name + '.yml', 'w',encoding='utf-8') as f:
                f.write(result)
print(''' ____ ____ ____
/ ___/ ___/ ___)
\___ \___ \___ \\
(____(____(____/ ''')
asyncio.run(main())