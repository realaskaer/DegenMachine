import random

from modules import *
from utils.networks import *
from config import OKX_WRAPED_ID, LAYERZERO_WRAPED_NETWORKS
from general_settings import GLOBAL_NETWORK
from settings import (ORBITER_CHAIN_ID_FROM, LAYERSWAP_CHAIN_ID_FROM, RHINO_CHAIN_ID_FROM, ACROSS_CHAIN_ID_FROM,
                      OKX_DEPOSIT_NETWORK, INSCRIPTION_NETWORK)


def get_client(account_number, private_key, network, proxy, bridge_from_evm:bool = False) -> Client | StarknetClient:
    if GLOBAL_NETWORK != 9 or bridge_from_evm:
        return Client(account_number, private_key, network, proxy)
    return StarknetClient(account_number, private_key, network, proxy)


def get_network_by_chain_id(chain_id):
    return {
        0: ArbitrumRPC,
        1: ArbitrumRPC,
        2: Arbitrum_novaRPC,
        3: BaseRPC,
        4: LineaRPC,
        5: MantaRPC,
        6: PolygonRPC,
        7: OptimismRPC,
        8: ScrollRPC,
        9: StarknetRPC,
        10: Polygon_ZKEVM_RPC,
        11: zkSyncEraRPC,
        12: ZoraRPC,
        13: EthereumRPC,
        14: AvalancheRPC,
        15: BSC_RPC,
        16: MoonbeamRPC,
        17: HarmonyRPC,
        18: TelosRPC,
        19: CeloRPC,
        20: GnosisRPC,
        21: CoreRPC,
        22: TomoChainRPC,
        23: ConfluxRPC,
        24: OrderlyRPC,
        25: HorizenRPC,
        26: MetisRPC,
        27: AstarRPC,
        28: OpBNB_RPC,
        29: MantleRPC,
        30: MoonriverRPC,
        31: KlaytnRPC,
        32: KavaRPC,
        33: FantomRPC,
        34: AuroraRPC,
        35: CantoRPC,
        36: DFK_RPC,
        37: FuseRPC,
        38: GoerliRPC,
        39: MeterRPC,
        40: OKX_RPC,
        41: ShimmerRPC,
        42: TenetRPC,
        43: XPLA_RPC,
        44: LootChainRPC,
        45: ZKFairRPC,
        46: BeamRPC
    }[chain_id]


def get_key_by_id_from(args, chain_from_id):
    private_keys = args[0].get('stark_key'), args[0].get('evm_key')
    current_key = private_keys[1]
    if chain_from_id == 9:
        current_key = private_keys[0]
    return current_key


async def swap_odos(account_number, private_key, network, proxy, **kwargs):
    worker = Odos(get_client(account_number, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def swap_xyfinance(account_number, private_key, network, proxy, **kwargs):
    worker = XYfinance(get_client(account_number, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def swap_rango(account_number, private_key, network, proxy, **kwargs):
    worker = Rango(get_client(account_number, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def swap_openocean(account_number, private_key, network, proxy, **kwargs):
    worker = OpenOcean(get_client(account_number, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def swap_oneinch(account_number, private_key, network, proxy, **kwargs):
    worker = OneInch(get_client(account_number, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def bridge_layerswap(account_number, _, __, proxy, *args, **kwargs):
    chain_from_id = random.choice(LAYERSWAP_CHAIN_ID_FROM)
    network = get_network_by_chain_id(chain_from_id)

    bridge_from_evm = True if 9 not in LAYERSWAP_CHAIN_ID_FROM else False
    private_key = get_key_by_id_from(args, chain_from_id)

    worker = LayerSwap(get_client(account_number, private_key, network, proxy, bridge_from_evm))
    return await worker.bridge(chain_from_id, *args, **kwargs)


async def bridge_orbiter(account_number, _, __, proxy, *args, **kwargs):
    chain_from_id = random.choice(ORBITER_CHAIN_ID_FROM)
    network = get_network_by_chain_id(chain_from_id)

    bridge_from_evm = True if 9 not in ORBITER_CHAIN_ID_FROM else False
    private_key = get_key_by_id_from(args, chain_from_id)

    worker = Orbiter(get_client(account_number, private_key, network, proxy, bridge_from_evm))
    return await worker.bridge(chain_from_id, *args, **kwargs)


async def bridge_rhino(account_number, _, __, proxy, *args, **kwargs):
    chain_from_id = random.choice(RHINO_CHAIN_ID_FROM)
    network = get_network_by_chain_id(chain_from_id)

    bridge_from_evm = True if 9 not in RHINO_CHAIN_ID_FROM else False
    private_key = get_key_by_id_from(args, chain_from_id)

    worker = Rhino(get_client(account_number, private_key, network, proxy, bridge_from_evm))
    return await worker.bridge(chain_from_id, *args, **kwargs)


async def bridge_across(account_number, _, __, proxy, *args, **kwargs):
    chain_from_id = random.choice(ACROSS_CHAIN_ID_FROM)
    network = get_network_by_chain_id(chain_from_id)

    bridge_from_evm = True if 9 not in ACROSS_CHAIN_ID_FROM else False
    private_key = get_key_by_id_from(args, chain_from_id)

    worker = Across(get_client(account_number, private_key, network, proxy, bridge_from_evm))
    return await worker.bridge(chain_from_id, *args, **kwargs)

async def okx_withdraw(account_number, private_key, network, proxy, *args, **kwargs):
    worker = OKX(get_client(account_number, private_key, network, proxy))
    return await worker.withdraw(*args, **kwargs)


async def okx_multi_withdraw(account_number, private_key, network, proxy):
    worker = Custom(get_client(account_number, private_key, network, proxy))
    return await worker.okx_multi_withdraw()


async def okx_deposit(account_number, private_key, _, proxy, dep_network=OKX_DEPOSIT_NETWORK, **kwargs):
    network = get_network_by_chain_id(OKX_WRAPED_ID[dep_network])

    worker = OKX(get_client(account_number, private_key, network, proxy))
    return await worker.deposit(**kwargs)


async def okx_collect_from_sub(account_number, private_key, network, proxy):
    worker = OKX(get_client(account_number, private_key, network, proxy))
    return await worker.collect_from_sub()


async def swap_avnu(account_number, private_key, network, proxy, **kwargs):
    worker = AVNU(get_client(account_number, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def zksync_rhino_checker(account_number, private_key, network, proxy):

    worker = Rhino(get_client(account_number, private_key, network, proxy))
    return await worker.check_eligible()


async def zksync_rhino_mint(account_number, private_key, network, proxy):

    worker = Rhino(get_client(account_number, private_key, network, proxy))
    return await worker.mint_common()


async def zksync_rhino_mint_pro(account_number, private_key, network, proxy):

    worker = Rhino(get_client(account_number, private_key, network, proxy))
    return await worker.mint_rare()


async def collector_eth(account_number, private_key, network, proxy):

    worker = Custom(get_client(account_number, private_key, network, proxy))
    return await worker.collect_eth()


async def make_balance_to_average(account_number, private_key, network, proxy):

    worker = Custom(get_client(account_number, private_key, network, proxy))
    return await worker.balance_average()


async def wrap_abuser(account_number, private_key, network, proxy):

    worker = Custom(get_client(account_number, private_key, network, proxy))
    return await worker.wraps_abuser()


async def mint_token_avnu(account_number, private_key, network, proxy):

    worker = Custom(get_client(account_number, private_key, network, proxy))
    return await worker.mint_token_avnu()


async def swap_bridged_usdc(account_number, private_key, network, proxy):
    worker = Custom(get_client(account_number, private_key, network, proxy))
    return await worker.swap_bridged_usdc()


async def mint_inscription(account_number, private_key, _, proxy):
    network = get_network_by_chain_id(LAYERZERO_WRAPED_NETWORKS[INSCRIPTION_NETWORK])

    worker = Inscription(get_client(account_number, private_key, network, proxy))
    return await worker.mint_inscribe()


async def mint_scroll_nft(account_number, private_key, network, proxy):

    worker = ScrollNFT(get_client(account_number, private_key, network, proxy))
    return await worker.mint()


async def claim_refund_zkfair(account_number, private_key, _, proxy):

    worker = ZKFair(get_client(account_number, private_key, ZKFairRPC, proxy))
    return await worker.claim_refund()


async def claim_drop_zkfair(account_number, private_key, _, proxy):
    worker = ZKFair(get_client(account_number, private_key, ZKFairRPC, proxy))
    return await worker.claim_drop()


async def stake_zkfair(account_number, private_key, _, proxy):
    worker = ZKFair(get_client(account_number, private_key, ZKFairRPC, proxy))
    return await worker.stake_tokens()


async def mint_orbiter_inscription(account_number, private_key, _, proxy):
    network = get_network_by_chain_id(LAYERZERO_WRAPED_NETWORKS[INSCRIPTION_NETWORK])

    worker = Custom(get_client(account_number, private_key, network, proxy))
    return await worker.mint_orbiter_inscription()
