from hyperliquid.info import Info
from hyperliquid.utils import constants



info = Info(
    constants.MAINNET_API_URL,
    skip_ws=True,
)

meta ,contexts = info.meta_and_asset_ctxs()
with open("./data/hyper/meta.txt","w",encoding="utf-8") as f:
    print(meta,file=f)
with open("./data/hyper/asset.txt","w",encoding="utf-8") as g:
    print(contexts,file=g)