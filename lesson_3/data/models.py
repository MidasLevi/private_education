from pretty_utils.type_functions.classes import Singleton
from py_eth_async.data.models import RawContract, DefaultABIs # нужно для взаимодействие с ERC-20 токенами
from pretty_utils.miscellaneous.files import read_json

from data.config import ABIS_DIR

""""
Папка для всех контрактов которые используются в скрипте
Необходимо для того, чтобы было удобно вносить корректировки и добавлять нужные исходные данные для работы скрипта
"""
class Contracts(Singleton):
    ARBITRUM_WOOFI = RawContract( # контракт для исполнения трансфера ETH -> USDC
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30', abi=read_json(path=(ABIS_DIR, 'woofi.json'))
        # путь до JSON файла с ABI нужного контракта
    )

    ARBITRUM_USDC = RawContract( # контракт USDC в арбитруме
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831', abi=DefaultABIs.Token
    )

    ARBITRUM_USDT = RawContract( # контракт USDC в арбитруме
        address='0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9', abi=DefaultABIs.Token
    )

    ARBITRUM_WBTC = RawContract(  # контракт USDC в арбитруме
        address='0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f', abi=DefaultABIs.Token
    )

    ARBITRUM_ETH = RawContract( # контракт ETH в арбитруме
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', abi=DefaultABIs.Token
    )
