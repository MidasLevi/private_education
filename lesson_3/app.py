import asyncio
from typing import Optional
from loguru import logger

from web3.types import TxParams
from py_eth_async.data.models import Networks, TokenAmount, Unit, Ether
from py_eth_async.client import Client
from pretty_utils.miscellaneous.files import read_json
from py_eth_async.transactions import Tx

from tasks.woofi import WooFi
from data.models import Contracts
from data.config import ABIS_DIR
from private_data import private_key1 #proxy

""""
async def check_balance():
    client = Client(network=Networks.Ethereum, proxy=proxy, check_proxy=False)
    balance = await client.wallet.balance()
    print(f'balance: {balance.Ether} | {client.account.key.hex()} | {client.account.address}')
    if balance.Wei > 0:
        exit(1)


async def bruteforce(count_tasks: int):
    u1 = Unit(amount=1, unit='ether')
    u2 = Unit(amount=2, unit='ether')
    res = u1 * u2
    print(res.Ether)

    # while True:
    #     tasks = []
    #     for _ in range(count_tasks):
    #         tasks.append(asyncio.create_task(check_balance()))
    #     await asyncio.wait(tasks)
"""

async def main():
    client = Client(private_key=private_key1, network=Networks.Arbitrum) # инициализируем подключение к БЧ
    print(client.account.address) # получаем адресс аккаунта
    # print(await client.contracts.get_signature(hex_signature='0x7dc20382')) # получение параметров от нужной сигнатуры
    # print(await client.contracts.parse_function(text_signature='swap(address,address,uint256,uint256,address,address)'))
    # получение распаршенной функции по аналогии с json-ом после
    # print(await client.contracts.get_contract_attributes(contract=Contracts.ARBITRUM_USDC))
    # получение адреса контракта и его ABI в AsynContract и RawContract, для остального передаёт только адрес без ABI
    # print(await client.contracts.get_abi(contract_address=Contracts.ARBITRUM_USDC.address))
    # автоматическое получение ABI (если есть возможность получить ABI, лучне не использовать эту функцию)

    # contract = await client.contracts.get( # возвращает адрес контракта и его ABI
    #     contract_address=Contracts.ARBITRUM_WOOFI.address,
    #     abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    # ) # с помощью этой функции можно работать с отдельными функциями внутри контракта
    # print(await contract.functions.WETH().call()) # пример работы с функцией выше

    # print(await client.contracts.get_functions(contract=Contracts.ARBITRUM_USDC)) # функция в удобной форме

    # print((await client.wallet.balance()).Ether) # получение баланса
    # print(await client.wallet.nonce()) # получение nonce

    # print((await client.transactions.gas_price(w3=client.w3)).Wei) #получение цены газа, веи, гвеи, эфиры
    # print(await client.transactions.max_priority_fee(w3=client.w3)) # фисы для получения первого места в блоке (как понял работает не через мемпул)

    # print(await client.transactions.decode_input_data(
    #     client=client,
    #     contract=Contracts.ARBITRUM_WOOFI,
    #     input_data='0x7dc20382000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000af88d065e77c8cc2239327c5edb3a432268e583100000000000000000000000000000000000000000000000000038d7ea4c6800000000000000000000000000000000000000000000000000000000000001be86500000000000000000000000069c1dc6d723f15d7ef8154ba7194977fcc90d85b00000000000000000000000069c1dc6d723f15d7ef8154ba7194977fcc90d85b'
    # ))

    woofi = WooFi(client=client) # инициализируем переменную которая обращается к классу WooFi из woofi.py
    res_eth_to_usdc = await woofi.swap_eth_to_usdc(amount=TokenAmount(amount=0.03))
    if 'Failed' in res_eth_to_usdc:
        logger.error(res_eth_to_usdc)
    else:
        logger.success(res_eth_to_usdc)

    await asyncio.sleep(5)
    
    res_usdc_to_eth = await woofi.swap_usdc_to_eth() # значений amount нет, свапается весь баланс
    if 'Failed' in res_usdc_to_eth:
        logger.error(res_usdc_to_eth)
    else:
        logger.success(res_usdc_to_eth)

    await asyncio.sleep(5)

    res_eth_to_usdt = await woofi.swap_eth_to_usdt(amount=TokenAmount(amount=0.0001))
    if 'Failed' in res_eth_to_usdt:
        logger.error(res_eth_to_usdt)
    else:
        logger.success(res_eth_to_usdt)

    res_usdt_to_eth = await woofi.swap_usdt_to_eth() # значений amount нет, свапается весь баланс
    if 'Failed' in res_usdt_to_eth:
        logger.error(res_usdt_to_eth)
    else:
        logger.success(res_usdt_to_eth)

    await asyncio.sleep(5)

    res_eth_to_wbtc = await woofi.swap_eth_to_wbtc(amount=TokenAmount(amount=0.001))
    if 'Failed' in res_eth_to_wbtc:
        logger.error(res_eth_to_wbtc)
    else:
        logger.success(res_eth_to_wbtc)

    await asyncio.sleep(5)

    res_wbtc_to_eth = await woofi.swap_wbtc_to_eth()
    if 'Failed' in res_wbtc_to_eth:
        logger.error(res_wbtc_to_eth)
    else:
        logger.success(res_wbtc_to_eth)


""""
    tx_hash = '0xf9bd50990974b8107a8ef1a2d2dc79c5de6114b42d5533827068ddccabe35240'
    tx = Tx(tx_hash=tx_hash)
    print(tx)
    print(await tx.parse_params(client=client))
    print(await tx.decode_input_data(client=client, contract=Contracts.ARBITRUM_WOOFI))
"""

if __name__ == '__main__': # нужно для запуска функции
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main()) #функция в скобках, та что мы запускаем асинхронно
