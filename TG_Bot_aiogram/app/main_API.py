import aiohttp
import asyncio

class CurrencyAPI:
    cache = {}

    def __init__(self, api_key, api_name):
        self.api_key = api_key
        self.api_name = api_name

    @classmethod
    def set_to_cache(cls, key, value):
        cls.cache[key] = value

    @classmethod
    def get_from_cache(cls, key):
        return cls.cache.get(key, None)

    @staticmethod
    async def status_code(status_code: int):
        if status_code == 200:
            print('Status code 200: Success!!!')
        elif status_code == 404:
            print('Error 404: Wrong URL!!!')
        elif status_code == 428:
            print('Let\'s wait 4 seconds')
            await asyncio.sleep(4)

    def __repr__(self):
        return f"CurrencyAPI(api_key='{self.api_key}', api_name='{self.api_name}')"


class PrivatAPI(CurrencyAPI):
    def __init__(self, api_name, api_key, url):
        super().__init__(api_name, api_key)
        self.url = url
        self.data = None

    async def get_currency(self, curr1, curr2):
        try:
            if self.get_from_cache('Privat_curr_rate'):
                self.data = self.cache['Privat_curr_rate']  # Використовуємо кеш
                print('Received PrivatBank CACHE data!')
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url) as response:
                        self.data = await response.json()
                        self.set_to_cache('Privat_curr_rate', self.data)  # Кешуємо дані
                        print('Received PrivatBank API data!')
                        await self.status_code(response.status)

            return await self.parsing_data(curr1, curr2)
        except Exception as e:
            print(f'Something went wrong: {e}')
            return None

    async def parsing_data(self, curr1_name, curr2_name):
        for curr in self.data:
            if curr["ccy"] == curr1_name and curr["base_ccy"] == curr2_name:
                return f'{curr1_name} -> {curr2_name}\n\t' \
                       f'Buy: {curr["buy"]}\n\tSell: {curr["sale"]}'
        return "Currency data not found."



class MonoAPI(CurrencyAPI):
    def __init__(self, api_name, api_key, url):
        super().__init__(api_name, api_key)
        self.url = url
        self.data = None

    async def get_currency(self, curr1, curr2):
        try:
            if self.get_from_cache('Mono_curr_rate'):
                self.data = self.cache['Mono_curr_rate']  # Використовуємо кеш
                print('Received MonoBank CACHE data!')
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url) as response:
                        self.data = await response.json()
                        self.set_to_cache('Mono_curr_rate', self.data)  # Кешуємо дані
                        print('Received MonoBank API data!')
                        await self.status_code(response.status)

            return await self.parsing_data(curr1, curr2)
        except Exception as e:
            print(f'Something went wrong: {e}')
            return None

    async def parsing_data(self, curr1_name, curr2_name):
        curr_codes = {'USD': 840, 'EUR': 978, 'UAH': 980}
        codeA = curr_codes[curr1_name]
        codeB = curr_codes[curr2_name]

        for curr in self.data:
            if curr["currencyCodeA"] == codeA and curr["currencyCodeB"] == codeB:
                return f'Data obtained:\n\tCurrencyA: {curr1_name}\n\tCurrencyB: {curr2_name}\n\t' \
                       f'rateBuy: {curr["rateBuy"]}\n\trateSell: {curr["rateSell"]}'
        return "Currency data not found."


# curr_mono = MonoAPI('Monobank', '', 'https://api.monobank.ua/bank/currency')
#
# async def main():
#     result = await curr_mono.get_currency('USD', 'UAH')  # Додаємо await
#     print(result)  # Виводимо курс валют
#
# asyncio.run(main())  # Запускаємо асинхронний код

