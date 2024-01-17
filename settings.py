"""
--------------------------------------------------OKX CONTROL-----------------------------------------------------------
    Выберите сети/суммы для вывода и ввода с OKX. Не забудьте вставить API ключи снизу.

    1 - ETH-ERC20              9  - CELO-Celo           17 - KLAY-Klaytn        26 - USDT-Arbitrum One
    2 - ETH-Arbitrum One       10 - ONE-Harmony         18 - FTM-Fantom         27 - USDC-ERC20
    3 - ETH-zkSync Lite        11 - GLMR-Moonbeam       19 - AVAX-Avalanche     28 - USDC-Optimism
    4 - ETH-Optimism           12 - MOVR-Moonriver      20 - ASTR-Astar         29 - USDC-Avalanche
    5 - ETH-Starknet           13 - METIS-Metis         21 - BNB-BSC            30 - USDC-Arbitrum One
    6 - ETH-zkSync Era         14 - CORE-CORE           22 - MATIC-Polygon      31 - USDC-Polygon
    7 - ETH-Linea              15 - CFX-Conflux         23 - USDT-Polygon       32 - USDC-Polygon (Bridged)
    8 - ETH-Base               16 - ZEN-Horizen         24 - USDT-Optimism      33 - USDC-Optimism (Bridged)
                                                        25 - USDT-Avalanche     34 - USDT-ERC20

------------------------------------------------------------------------------------------------------------------------
"""
OKX_WITHDRAW_NETWORK = 22      # Сеть вывода из OKX
OKX_WITHDRAW_AMOUNT = (1, 1)   # (минимальная, максимальная) сумма для вывода из OKX (кол-во)

OKX_MULTI_WITHDRAW = {  # Сеть вывода: (минимум, максимум) в токене для вывода (кол-во)
    9: (1, 1.011),
    4: (0.0001, 0.000111),
}

OKX_DEPOSIT_NETWORK = 32                  # Сеть из которой планируется пополнение OKX
OKX_DEPOSIT_AMOUNT = ('100', '100')    # (минимальная, максимальная) сумма для пополнения OKX (% или кол-во)

"""
------------------------------------------------BRIDGE CONTROL----------------------------------------------------------
    Проверьте руками, работает ли сеть на сайте. (Софт сам проверит, но зачем его напрягать?)
    Софт работает только с нативным токеном(ETH). Не забудьте вставить API ключ для LayerSwap.
    Для каждого моста поддерживается уникальная настройка
    
    Можно указать минимальную/максимальную сумму или минимальный/максимальный % от баланса
    
    Количество - (0.01, 0.02)
    Процент    - ("10", "20") ⚠️ Значения в скобках
       
     (A)Arbitrum = 1                    Polygon ZKEVM = 10 
        Arbitrum Nova = 2            (A)zkSync Era = 11     
     (A)Base = 3                       *Zora = 12 
        Linea = 4                       Ethereum = 13
        Manta = 5                      *Avalanche = 14
       *Polygon = 6                     BNB Chain = 15
     (A)Optimism = 7                 (O)Metis = 26        
        Scroll = 8                     *OpBNB = 28
        Starknet = 9                   *Mantle = 29
                                        ZKFair = 45   
    
    * - не поддерживается в Rhino.fi
    (A) - сети, поддерживаемые Across мостом
    (0) - поддерживается только для Orbiter моста
    ORBITER_CHAIN_ID_FROM(TO) = [2, 4, 16] | Одна из сетей будет выбрана
"""

ORBITER_CHAIN_ID_FROM = [7]                # Исходящая сеть
ORBITER_CHAIN_ID_TO = [45]                  # Входящая сеть
ORBITER_DEPOSIT_AMOUNT = (1, 1)          # (минимум, максимум) (% или кол-во)
ORBITER_TOKEN_NAME = 'USDC'

LAYERSWAP_CHAIN_ID_FROM = [1]                # Исходящая сеть
LAYERSWAP_CHAIN_ID_TO = [4]                  # Входящая сеть
LAYERSWAP_DEPOSIT_AMOUNT = (0.002, 0.002)    # (минимум, максимум) (% или кол-во)

RHINO_CHAIN_ID_FROM = [1]                # Исходящая сеть
RHINO_CHAIN_ID_TO = [11]                  # Входящая сеть
RHINO_DEPOSIT_AMOUNT = (0.012, 0.022)    # (минимум, максимум) (% или кол-во)

ACROSS_CHAIN_ID_FROM = [9]                # Исходящая сеть
ACROSS_CHAIN_ID_TO = [4]                  # Входящая сеть
ACROSS_DEPOSIT_AMOUNT = (0.002, 0.002)    # (минимум, максимум) (% или кол-во)

"""
--------------------------------------------------DEGEN SETTINGS--------------------------------------------------------
    
    Поддерживаемые сети для работы модулей. Перед настройкой, проверьте работает ли сайт с указанной сетью!
    
        Arbitrum = 1                  Goerli = 16                        OKX = 30
        Arbitrum Nova = 2             Gnosis = 17                        Optimism = 31
        Astar = 3                     Harmony = 18                       Orderly = 32
        Aurora = 4                    Horizen = 19                       Polygon = 33  
        Avalanche = 5                 Kava = 20                          Polygon zkEVM = 34
        BNB = 6                       Klaytn = 21                        Scroll = 35
        Base = 7                      Linea = 22                         ShimmerEVM = 36
        Canto = 8                     Loot = 23                          Telos = 37
        Celo = 9                      Manta = 24                         TomoChain = 38 
        Conflux = 10                  Mantle = 25                        Tenet = 39
        CoreDAO = 11                  Meter = 26                         XPLA = 40
        DFK = 12                      Metis = 27                         Zora = 41  
        Ethereum = 13                 Moonbeam = 28                      opBNB = 42
        Fantom = 14                   Moonriver = 29                     zkSync = 43
        Fuse = 15                                                        Beam = 44
            
    INSCRIPTION_DATA | Указывайте дату для минта. Обычно ее дают на сайтах. Поддерживаются форматы в виде json и hex.
        В формате json - 'data....'
        В формате hex - 0x123
    INSCRIPTION_NETWORK | Сеть в которой планируется минтить инскрипшен. Поддерживаются все сети из OMNI-CHAIN CONTROL    
    
    MEMCOIN_AMOUNT | Сумма в ETH, на которую планируете покупать мемкоин.
"""
INSCRIPTION_DATA = ''  # Json или Hex формат
INSCRIPTION_NETWORK = 1  # сеть для минта Inscription (номера в DEGEN SETTINGS)
INSCRIPTION_NETWORK_ORBITER = 7  # входящая сеть для Orbiter Inscription (номера в DEGEN SETTINGS)

MEMCOIN_AMOUNT = 0.01  # сумма в ETH

ZKFAIR_STAKE_PERIOD = 90  # кол-во дней для стейкинга (месяц = 30)
ZKFAIR_STAKE_AMOUNT = 50  # процент от баланса ZKF для стейкинга
ZKFAIR_CLAIM_REFUND_PHASES = [1, 2, 3, 4]  # фазы для клейма рефаунда


"""
--------------------------------------------CLASSIC-ROUTES CONTROL------------------------------------------------------

---------------------------------------------------HELPERS--------------------------------------------------------------        

    okx_withdraw                     # смотри OKX CONTROL
    okx_multi_withdraw               # вывод в несколько сетей. Смотри OKX CONTROL (OKX_MULTI_WITHDRAW)
    collector_eth                    # сбор всех токенов в ETH
    bridge_across                    # смотри BRIDGE CONTROL
    bridge_rhino                     # смотри BRIDGE CONTROL
    bridge_layerswap                 # смотри BRIDGE CONTROL
    bridge_orbiter                   # смотри BRIDGE CONTROL
    okx_deposit                      # ввод средств на биржу
    okx_collect_from_sub             # сбор средств на субАккаунтов на основной счет
    
---------------------------------------------------CUSTOM---------------------------------------------------------------        
    
    mint_token_avnu                  # обмен щитка на AVNU. см. MEMCOIN_AMOUNT. Контракт менять в config.py -> TOKENS_PER_CHAIN
    mint_scroll_nft                  # минт Scroll NFT за деплой контрактов
    mint_inscription                 # минт инскрипшена в сети INSCRIPTION_NETWORK(номера из L0).
    mint_orbiter_inscription         # минт инскрипшена на Orbiter см. INSCRIPTION_NETWORK, INSCRIPTION_NETWORK_ORBITER.
    zksync_rhino_checker             # проверка на eligible для минта Rhino.fi Pro Hunter NFT 
    zksync_rhino_mint                # минт Rhino.fi Hunter NFT
    zksync_rhino_mint_pro            # проверка на eligible и минт Rhino.fi Pro Hunter NFT
    claim_refund_zkfair              # клейм рефанда за участие в раздаче ZKFair. см. ZKFAIR_CLAIM_REFUND_PHASES
    stake_zkfair                     # стейкинг токена ZKF в сети ZKFair. см. ZKFAIR_STAKE_PERIOD, ZKFAIR_STAKE_AMOUNT

    Выберите необходимые модули для взаимодействия
    Вы можете создать любой маршрут, софт отработает строго по нему. Для каждого списка будет выбран один модуль в
    маршрут, если софт выберет None, то он пропустит данный список модулей. 
    Список модулей сверху.
    
    CLASSIC_ROUTES_MODULES_USING = [
        ['okx_withdraw'],
        ['bridge_layerswap', 'bridge_oribter', None],
        ['stake_zkfair', 'zksync_rhino_mint_pro']
        ...
    ]
"""
CLASSIC_ROUTES_MODULES_USING = [
    ['okx_withdraw'],
    ['bridge_layerswap', 'bridge_oribter', None],
    ['stake_zkfair', 'zksync_rhino_mint_pro']
]
