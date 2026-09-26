from web3 import Web3

w3 = Web3(Web3.HTTPProvider(RPC_URL))

factory = w3.eth.contract(
    address=FACTORY_ADDRESS,
    abi=FACTORY_ABI,
)

pool = factory.functions.getPool(
    WETH_ADDRESS,
    USDC_ADDRESS,
    3000,  # 0.30%
).call()

print(pool)