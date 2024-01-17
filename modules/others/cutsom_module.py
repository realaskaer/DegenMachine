import random

from config import ETH_PRICE, TOKENS_PER_CHAIN, ORBITER_CHAINS_INFO, LAYERZERO_WRAPED_NETWORKS
from modules import Logger, Aggregator
from general_settings import GLOBAL_NETWORK, AMOUNT_PERCENT_WRAPS
from settings import (
    MEMCOIN_AMOUNT,
    OKX_MULTI_WITHDRAW,
    INSCRIPTION_NETWORK_ORBITER
)
from utils.tools import helper, gas_checker, sleep


class Custom(Logger, Aggregator):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        Aggregator.__init__(self, client)

    async def swap(self):
        pass

    async def collect_eth_util(self):
        from functions import swap_odos, swap_oneinch, swap_openocean, swap_xyfinance, swap_rango, swap_avnu

        self.logger_msg(*self.client.acc_info, msg=f"Start collecting tokens in ETH")

        func = {
            3: [swap_odos, swap_oneinch, swap_openocean, swap_xyfinance],
            4: [swap_rango, swap_openocean, swap_xyfinance],
            8: [swap_openocean, swap_xyfinance],
            9: [swap_avnu],
            11: [swap_openocean, swap_xyfinance, swap_odos, swap_oneinch]
        }[GLOBAL_NETWORK]

        wallet_balance = {k: await self.client.get_token_balance(k, False)
                          for k, v in TOKENS_PER_CHAIN[self.client.network.name].items()}
        valid_wallet_balance = {k: v[1] for k, v in wallet_balance.items() if v[0] != 0}
        eth_price = ETH_PRICE

        if 'ETH' in valid_wallet_balance:
            valid_wallet_balance['ETH'] = valid_wallet_balance['ETH'] * eth_price

        if valid_wallet_balance['ETH'] < 0.5:
            self.logger_msg(*self.client.acc_info, msg=f'Account has not enough ETH for swap', type_msg='warning')
            return True

        if len(valid_wallet_balance.values()) > 1:

            for token_name, token_balance in valid_wallet_balance.items():
                if token_name != 'ETH':
                    amount_in_wei = wallet_balance[token_name][0]
                    amount = float(f"{(amount_in_wei / 10 ** await self.client.get_decimals(token_name)):.6f}")
                    amount_in_usd = valid_wallet_balance[token_name]
                    if amount_in_usd > 1:
                        from_token_name, to_token_name = token_name, 'ETH'
                        data = from_token_name, to_token_name, amount, amount_in_wei
                        counter = 0
                        while True:
                            result = False
                            module_func = random.choice(func)
                            try:
                                self.logger_msg(*self.client.acc_info, msg=f'Launching swap module', type_msg='warning')
                                result = await module_func(self.client.account_name, self.client.private_key,
                                                           self.client.network, self.client.proxy_init, swapdata=data)
                                if not result:
                                    counter += 1
                            except:
                                counter += 1
                                pass
                            if result or counter == 3:
                                break
                    else:
                        self.logger_msg(*self.client.acc_info, msg=f"{token_name} balance < 1$")

            return True
        else:
            raise RuntimeError('Account balance already in ETH!')

    @helper
    @gas_checker
    async def collect_eth(self):
        await self.collect_eth_util()

    @helper
    @gas_checker
    async def wraps_abuser(self):
        from functions import swap_odos, swap_oneinch, swap_xyfinance, swap_avnu

        func = {
            3: [swap_odos, swap_oneinch, swap_xyfinance],
            4: [swap_xyfinance],
            8: [swap_xyfinance],
            9: [swap_avnu],
            11: [swap_oneinch, swap_xyfinance]
        }[GLOBAL_NETWORK]

        current_tokens = list(TOKENS_PER_CHAIN[self.client.network.name].items())[:2]

        wallet_balance = {k: await self.client.get_token_balance(k, False) for k, v in current_tokens}
        valid_wallet_balance = {k: v[1] for k, v in wallet_balance.items() if v[0] != 0}
        eth_price = ETH_PRICE

        if 'ETH' in valid_wallet_balance:
            valid_wallet_balance['ETH'] = valid_wallet_balance['ETH'] * eth_price

        if 'WETH' in valid_wallet_balance:
            valid_wallet_balance['WETH'] = valid_wallet_balance['WETH'] * eth_price

        max_token = max(valid_wallet_balance, key=lambda x: valid_wallet_balance[x])
        percent = round(random.uniform(*AMOUNT_PERCENT_WRAPS), 9) / 100 if max_token == 'ETH' else 1
        amount_in_wei = int(wallet_balance[max_token][0] * percent)
        amount = float(f"{amount_in_wei / 10 ** 18:.6f}")

        if max_token == 'ETH':
            msg = f'Wrap {amount:.6f} ETH'
            from_token_name, to_token_name = 'ETH', 'WETH'
        else:
            msg = f'Unwrap {amount:.6f} WETH'
            from_token_name, to_token_name = 'WETH', 'ETH'

        self.logger_msg(*self.client.acc_info, msg=msg)

        if (max_token == 'ETH' and valid_wallet_balance[max_token] > 1
                or max_token == 'WETH' and valid_wallet_balance[max_token] != 0):
            data = from_token_name, to_token_name, amount, amount_in_wei
            counter = 0
            result = False
            while True:
                module_func = random.choice(func)
                try:
                    result = await module_func(self.client.account_name, self.client.private_key,
                                               self.client.network, self.client.proxy_init, swapdata=data)

                except:
                    pass
                if result or counter == 3:
                    break

        else:
            self.logger_msg(*self.client.acc_info, msg=f"{from_token_name} balance is too low (lower 1$)")

        return True

    @helper
    @gas_checker
    async def mint_token_avnu(self):
        from functions import swap_avnu

        amount, amount_in_wei = MEMCOIN_AMOUNT, int(MEMCOIN_AMOUNT * 10 ** 18)
        data = 'ETH', 'MEMCOIN', amount, amount_in_wei

        return await swap_avnu(self.client.account_name, self.client.private_key,
                               self.client.network, self.client.proxy_init, swapdata=data)

    @helper
    @gas_checker
    async def swap_bridged_usdc(self):
        from functions import swap_oneinch

        amount_in_wei, amount, _ = await self.client.get_token_balance('USDC')
        data = 'USDC', 'USDC.e', amount, amount_in_wei

        if amount_in_wei == 0:
            raise RuntimeError("Insufficient USDC balances")

        return await swap_oneinch(self.client.account_name, self.client.private_key,
                                  self.client.network, self.client.proxy_init, swapdata=data)

    @helper
    async def okx_multi_withdraw(self, random_network:bool = False):
        from functions import okx_withdraw

        if random_network:
            shuffle_withdraw = list(OKX_MULTI_WITHDRAW.items())
            shuffle_withdraw = random.choice(shuffle_withdraw)
        else:
            shuffle_withdraw = list(OKX_MULTI_WITHDRAW.items())
            random.shuffle(shuffle_withdraw)

        multi_withdraw_data = {}

        for network, amount in shuffle_withdraw:
            multi_withdraw_data['network'] = network
            multi_withdraw_data['amount'] = amount

            try:
                await okx_withdraw(self.client.account_name, self.client.private_key,
                                   self.client.network, self.client.proxy_init, multi_withdraw_data=multi_withdraw_data)
            except Exception as error:
                self.logger_msg(
                    *self.client.acc_info, msg=f"Withdraw from OKX failed. Error: {error}", type_msg='error')

            await sleep(self)

        return True

    @helper
    @gas_checker
    async def mint_orbiter_inscription(self):

        contract_address = '0x0a88BC5c32b684D467b43C06D9e0899EfEAF59Df'

        to_chain_id = ORBITER_CHAINS_INFO[LAYERZERO_WRAPED_NETWORKS[INSCRIPTION_NETWORK_ORBITER]]['id']
        to_chain_name = ORBITER_CHAINS_INFO[LAYERZERO_WRAPED_NETWORKS[INSCRIPTION_NETWORK_ORBITER]]['name']

        self.logger_msg(
            *self.client.acc_info,
            msg=f'Claim inscription on Orbiter. Mint chain: {self.client.network.name}. Dst chain: {to_chain_name}')

        destination_code = 9000 + to_chain_id

        value = int(0.00023 * 10 ** 18 + destination_code)

        transaction = (await self.client.prepare_transaction(value=value)) | {
            'data': '0x' + 'data:,{"p":"layer2-20","op":"claim","tick":"$L2","amt":"1000"}'.encode('utf-8').hex(),
            'to': contract_address
        }

        return await self.client.send_transaction(transaction)
