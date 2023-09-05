import asyncio
from typing import Optional
from web3.types import TxParams
from py_eth_async.data.models import TxArgs, TokenAmount

from data.models import Contracts
from tasks.base import Base

""""
Алгоритм для реализации логики свапов на вуфи
"""
class WooFi(Base):
    async def swap_eth_to_usdc(self, amount: TokenAmount , slippage: float = 1): # кол-во свапа, для нативного токена количество передается в аргументах и проскальзывание
        failed_text = 'Failed swap ETH to USDC via WooFi' # команда при реджекте транзакции

        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI) # функция которая получает нужный контракт для свапа (контракт вуфи который исполняет трансфер eth в usdc)
        from_token = Contracts.ARBITRUM_ETH # один из аргументов ABI, токен который свапаем
        to_token = Contracts.ARBITRUM_USDC # один из аргументов ABI, токен на который свапаем

        eth_price = await self.get_token_price(token='ETH') # берем цену с бинанса
        min_to_amount = TokenAmount( # минимальное количество которое получаем при свапе (?)
            amount=eth_price * float(amount.Ether) * (1 - slippage / 100), # формула для свапа
            decimals=await self.get_decimals(contract_address=to_token.address) # получаем децималы из контракта
        )

        args = TxArgs( # переменная аргументов транзакций
            fromToken=from_token.address, # адрес контракта, строка 15
            toToken=to_token.address, # адрес контракта, строка 16
            fromAmount=amount.Wei, # какое количество свапаем, строка 11, параметр amount
            minToAmount=min_to_amount.Wei, # минимальное количество для свапа, строки 18-21
            to=self.client.account.address, # адрес куда, наш адрес
            rebateTo=self.client.account.address, # непонятная переменная, но тоже собственный адрес
        )

        tx_params = TxParams( # переменная параметров транзакций
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
            value=amount.Wei
        )
        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} ETH was swaped to {min_to_amount.Ether} USDC via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def swap_usdc_to_eth(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        failed_text = 'Failed swap USDC to ETH via WooFi'
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)
        from_token = Contracts.ARBITRUM_USDC
        to_token = Contracts.ARBITRUM_ETH

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount)
        await asyncio.sleep(5)

        eth_price = await self.get_token_price(token='ETH')
        min_to_amount = TokenAmount(
            amount=float(amount.Ether) / eth_price * (1 - slippage / 100) # количество в эфире, делим на эфир и умножаем на проскальзывание
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple())
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} USDC was swaped to {min_to_amount.Ether} ETH via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def swap_eth_to_usdt(self, amount: TokenAmount , slippage: float = 1): # кол-во свапа, для нативного токена количество передается в аргументах и проскальзывание
        failed_text = 'Failed swap ETH to USDT via WooFi' # команда при реджекте транзакции

        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI) # функция которая получает нужный контракт для свапа (контракт вуфи который исполняет трансфер eth в usdc)
        from_token = Contracts.ARBITRUM_ETH # один из аргументов ABI, токен который свапаем
        to_token = Contracts.ARBITRUM_USDT # один из аргументов ABI, токен на который свапаем

        eth_price = await self.get_token_price(token='ETH') # берем цену с бинанса
        min_to_amount = TokenAmount( # минимальное количество которое получаем при свапе (?)
            amount=eth_price * float(amount.Ether) * (1 - slippage / 100), # формула для свапа
            decimals=await self.get_decimals(contract_address=to_token.address) # получаем децималы из контракта
        )

        args = TxArgs( # переменная аргументов транзакций
            fromToken=from_token.address, # адрес контракта, строка 89
            toToken=to_token.address, # адрес контракта, строка 90
            fromAmount=amount.Wei, # какое количество свапаем, строка 11, параметр amount
            minToAmount=min_to_amount.Wei, # минимальное количество для свапа, строки 18-21
            to=self.client.account.address, # адрес куда, наш адрес
            rebateTo=self.client.account.address, # непонятная переменная, но тоже собственный адрес
        )

        tx_params = TxParams( # переменная параметров транзакций
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
            value=amount.Wei
        )
        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} ETH was swaped to {min_to_amount.Ether} USDT via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def swap_usdt_to_eth(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        failed_text = 'Failed swap USDT to ETH via WooFi'
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)
        from_token = Contracts.ARBITRUM_USDT
        to_token = Contracts.ARBITRUM_ETH

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount)
        await asyncio.sleep(5)

        eth_price = await self.get_token_price(token='ETH')
        min_to_amount = TokenAmount(
            amount=float(amount.Ether) / eth_price * (1 - slippage / 100) # количество в эфире, делим на эфир и умножаем на проскальзывание
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple())
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} USDT was swaped to {min_to_amount.Ether} ETH via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def swap_eth_to_wbtc(self, amount: TokenAmount , slippage: float = 1): # кол-во свапа, для нативного токена количество передается в аргументах и проскальзывание
        failed_text = 'Failed swap ETH to WBTC via WooFi' # команда при реджекте транзакции

        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI) # функция которая получает нужный контракт для свапа (контракт вуфи который исполняет трансфер eth в usdc)
        from_token = Contracts.ARBITRUM_ETH # один из аргументов ABI, токен который свапаем
        to_token = Contracts.ARBITRUM_WBTC # один из аргументов ABI, токен на который свапаем

        eth_price = await self.get_token_price(token='ETH') # берем цену с бинанса
        btc_price = await self.get_token_price(token='BTC')
        min_to_amount = TokenAmount( # минимальное количество которое получаем при свапе (?)
            amount=(eth_price / btc_price) * float(amount.Ether) * (1 - slippage / 100), # формула для свапа цену эфира / на цену нужного токена
            decimals=await self.get_decimals(contract_address=to_token.address) # получаем децималы из контракта
        )

        args = TxArgs( # переменная аргументов транзакций
            fromToken=from_token.address, # адрес контракта, строка 89
            toToken=to_token.address, # адрес контракта, строка 90
            fromAmount=amount.Wei, # какое количество свапаем, строка 11, параметр amount
            minToAmount=min_to_amount.Wei, # минимальное количество для свапа, строки 18-21
            to=self.client.account.address, # адрес куда, наш адрес
            rebateTo=self.client.account.address, # непонятная переменная, но тоже собственный адрес
        )

        tx_params = TxParams( # переменная параметров транзакций
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
            value=amount.Wei
        )
        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} ETH was swaped to {min_to_amount.Ether} WBTC via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def swap_wbtc_to_eth(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        failed_text = 'Failed swap WBTC to ETH via WooFi'
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)
        from_token = Contracts.ARBITRUM_WBTC
        to_token = Contracts.ARBITRUM_ETH

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount)
        await asyncio.sleep(5)

        eth_price = await self.get_token_price(token='ETH')
        btc_price = await self.get_token_price(token='BTC')
        min_to_amount = TokenAmount(
            amount=(btc_price / eth_price) * float(amount.Ether) * (1 - slippage / 100),
            # формула для свапа цену эфира / на цену нужного токена
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple())
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} WBTC was swaped to {min_to_amount.Ether} ETH via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'