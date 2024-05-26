import aiohttp
import asyncio
import sys
import json
# import platform
from datetime import datetime, timedelta


url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

async def json_parse(js: dict) -> dict:
    parsed_json, currency_dict = {}, {}
    date = js.get('date')
    exchange_rate = js.get('exchangeRate')
    for el in exchange_rate:
        currency = el.get('currency')
        sale_buy = {}
        if currency == 'EUR':
            currency_dict[currency] = sale_buy
            sale_buy['sale'] = el.get('saleRate')
            sale_buy['purchase'] = el.get('purchaseRate')
        elif currency == 'USD':
            currency_dict[currency] = sale_buy
            sale_buy['sale'] = el.get('saleRate')
            sale_buy['purchase'] = el.get('purchaseRate')
        parsed_json[date] = currency_dict
    return parsed_json

async def request(url: str, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            result = await resp.json()
            result = await json_parse(result)
            return result
        else:
            print(f"Error status: {resp.status}")

async def main(days):
    try:
        days = int(days)
        if days < 1 or days > 10:
            raise ValueError(f"Enter number from 1 to 10.")
        async with aiohttp.ClientSession() as session:
            requests = []
            for i in range(1, days+1):
                shift = datetime.now() - timedelta(days=i)
                date = shift.strftime("%d.%m.%Y")
                requests.append(request(url+date, session))
            return await asyncio.gather(*requests)
    except (aiohttp.ClientConnectorError, aiohttp.InvalidURL, ValueError) as err:
            print(str(err))


if __name__ == '__main__':
    # if platform.system() == 'Windows':
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(sys.argv[1]))
    # r = asyncio.run(main(1))
    print(json.dumps(r, indent=4))
