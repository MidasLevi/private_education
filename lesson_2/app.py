import asyncio

from web3 import Web3

from sdk.data.models import Networks
from sdk.client import Client
import random

#from private_data import private_key1, private_key2, private_key3, proxy


async def check_balance(): # создаем функцию для поиска аккаунта с балансом
    client = Client(network=Networks.Ethereum) # создаем аккаунты
    balance = await client.wallet.balance() # асинхронно получаем балансы
    print(f'{balance.Ether} | {client.account.key.hex()} | {client.account.address}') # принутем балансы, приватник, адрес
    if balance.Wei > 0: # условие для выхода из функции, если баланс в веях больше 1
        exit(1)

async def brute_force(count: int): # функция брут-форса
    tasks = [] # список для задач брут форса
    for _ in range(count): # цикл для задач
        tasks.append(asyncio.create_task(check_balance())) # добавление задач в список и создание асинхронных задач по поиску аккаунтов с балансом
    await asyncio.wait(tasks)

"""
async def main():
    client = Client(private_key=private_key1, network=Networks.Optimism, proxy=proxy)
    # print(await client.wallet.balance(token_address='0xaf88d065e77c8cc2239327c5edb3a432268e5831'))
    balance = await client.wallet.balance()
    balance = await client.wallet.balance()
    balance = await client.wallet.balance()
"""

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(brute_force(10))

'''
    asyncio.gather() принимает список асинхронных задач (coroutines) в качестве аргументов и запускает их одновременно.
    Она возвращает список результатов, соответствующих выполненным задачам в том же порядке, в котором задачи были переданы в функцию.
    Если во время выполнения задачи возникает исключение, asyncio.gather() прекращает выполнение остальных задач и сразу же выбрасывает исключение.

    asyncio.wait() принимает список асинхронных задач (coroutines) в качестве аргументов и запускает их одновременно.
    Она возвращает кортеж из двух множеств: множество выполненных задач и множество невыполненных задач.
    Если во время выполнения задачи возникает исключение, asyncio.wait() продолжает выполнение остальных задач и не выбрасывает исключение.
    
    Написать код, который сам генерирует приватный ключ и адрес к нему и после этого проверяет баланс эфира в сети эфира 
    Код должен работать асинхронно 

 '''









