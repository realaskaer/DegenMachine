import json

from utils.tools import clean_progress_file
from functions import *
from config import ACCOUNT_NAMES
from modules import Logger
from general_settings import SHUFFLE_ROUTE
from settings import CLASSIC_ROUTES_MODULES_USING

AVAILABLE_MODULES_INFO = {
    # module_name                       : (module name, priority, tg info, can be help module, supported network)
    okx_withdraw                        : (okx_withdraw, -3, 'OKX Withdraw', 0, [2, 3, 4, 8, 9, 11, 12]),
    okx_multi_withdraw                  : (okx_multi_withdraw, 0, 'OKX Multi Withdraw', 0, [2, 3, 4, 8, 9, 11, 12]),
    make_balance_to_average             : (make_balance_to_average, -2, 'Check and make wanted balance', 0, [0]),
    collector_eth                       : (collector_eth, -1, 'Collect ETH from tokens', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_rhino                        : (bridge_rhino, 1, 'Rhino Bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_layerswap                    : (bridge_layerswap, 1, 'LayerSwap Bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_orbiter                      : (bridge_orbiter, 1, 'Orbiter Bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_across                       : (bridge_across, 1, 'Across Bridge', 0, [2, 3, 11, 12]),
    swap_avnu                           : (swap_avnu, 2, 'AVNU Swap', 1, [9]),
    swap_odos                           : (swap_odos, 2, 'ODOS Swap', 1, [3, 11]),
    swap_oneinch                        : (swap_oneinch, 2, '1inch Swap', 1, [3, 11]),
    swap_openocean                      : (swap_openocean, 2, 'OpenOcean Swap', 0, [3, 4, 8, 11]),
    swap_rango                          : (swap_rango, 2, 'Rango Swap', 1, [4, 11]),
    swap_xyfinance                      : (swap_xyfinance, 2, 'XYfinance Swap', 0, [11]),
    swap_bridged_usdc                   : (swap_bridged_usdc, 2, 'Swap USDC to Bridged', 1, [0]),
    mint_inscription                    : (mint_inscription, 2, 'Mint EVM Inscription', 0, [0]),
    mint_scroll_nft                     : (mint_scroll_nft, 2, 'Mint Scroll Origins NFT', 0, [0]),
    wrap_abuser                         : (wrap_abuser, 2, 'Wrap Abuse =)', 0, [0]),
    zksync_rhino_checker                : (zksync_rhino_checker, 3, 'Rhino Checker', 0, [11]),
    zksync_rhino_mint                   : (zksync_rhino_mint, 3, 'Rhino Mint zkSync Hunter NFT', 0, [11]),
    zksync_rhino_mint_pro               : (zksync_rhino_mint_pro, 3, 'Rhino Mint zkSync Pro Hunter NFT', 0, [11]),
    claim_refund_zkfair                 : (claim_refund_zkfair, 3, 'Claim Refund on ZKFair', 0, [11]),
    stake_zkfair                        : (stake_zkfair, 3, 'Stake ZKF on ZKFair', 0, [11]),
    mint_orbiter_inscription            : (mint_orbiter_inscription, 3, 'Mint Inscription on Orbiter', 0, [11]),
    mint_token_avnu                     : (mint_token_avnu, 3, 'Looooot a new one shit coin =)', 0, [0]),
    okx_deposit                         : (okx_deposit, 4, 'OKX Deposit', 0, [2, 3, 4, 8, 9, 11, 12]),
    okx_collect_from_sub                : (okx_collect_from_sub, 5, 'OKX Collect money', 0, [2, 3, 4, 8, 9, 11, 12])
}


def get_func_by_name(module_name, help_message:bool = False):
    for k, v in AVAILABLE_MODULES_INFO.items():
        if k.__name__ == module_name:
            if help_message:
                return v[2]
            return v[0]


class RouteGenerator(Logger):
    def __init__(self):
        Logger.__init__(self)

    @staticmethod
    def classic_generate_route():
        route = []
        for i in CLASSIC_ROUTES_MODULES_USING:
            module_name = random.choice(i)
            if module_name is None:
                continue
            module = get_func_by_name(module_name)
            route.append(module.__name__)
        return route

    def classic_routes_json_save(self):
        clean_progress_file()
        with open('./data/services/wallets_progress.json', 'w') as file:
            accounts_data = {}
            for account_name in ACCOUNT_NAMES:
                if isinstance(account_name, (str, int)):
                    classic_route = self.classic_generate_route()
                    if SHUFFLE_ROUTE:
                        random.shuffle(classic_route)
                    account_data = {
                        "current_step": 0,
                        "route": classic_route
                    }
                    accounts_data[str(account_name)] = account_data
            json.dump(accounts_data, file, indent=4)
        self.logger_msg(
            None, None,
            f'Successfully generated {len(accounts_data)} classic routes in data/services/wallets_progress.json\n',
            'success')
