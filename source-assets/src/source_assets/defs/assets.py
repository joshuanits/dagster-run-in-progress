from collections.abc import Iterator
import dagster as dg
from time import sleep

def unrelated_asset_factory(i) -> dg.AssetsDefinition:
    @dg.asset(
        name=f"unrelated_asset_{i}",
        pool="unrelated"
    )
    def _asset(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
        context.log.info(f"Running asset {i}")
        sleep(10)
        return dg.MaterializeResult()

    return _asset

@dg.asset
def source_asset() -> dg.MaterializeResult:
    return dg.MaterializeResult()

multi_asset_keys = [f"source_multi_asset_{i}" for i in range(5)]
@dg.multi_asset(specs=[dg.AssetSpec(key) for key in multi_asset_keys])
def source_multi_asset(context: dg.AssetExecutionContext) -> Iterator[dg.MaterializeResult]:
    for key in multi_asset_keys:
        context.log.info(f"Running {key}")
        yield dg.MaterializeResult(asset_key=key)
        sleep(10)

source_assets_job = dg.define_asset_job(name="source_assets_job")
    
@dg.definitions
def defs():
    return dg.Definitions(
        assets=[unrelated_asset_factory(i) for i in range(5)] + [source_asset, source_multi_asset],
        jobs=[source_assets_job],
    )
