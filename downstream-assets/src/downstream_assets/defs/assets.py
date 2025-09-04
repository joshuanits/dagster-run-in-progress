import dagster as dg



@dg.asset(
    deps=["source_asset"],
    automation_condition=dg.AutomationCondition.eager(),
)
def downstream_asset(context: dg.AssetExecutionContext) -> dg.MaterializeResult: 
    context.log.info("Running downstream_asset")
    return dg.MaterializeResult()

@dg.asset(
    deps=["source_multi_asset_0"],
    automation_condition=dg.AutomationCondition.eager(),
)
def multi_downstream_asset(context: dg.AssetExecutionContext) -> dg.MaterializeResult: 
    context.log.info("Running multi_downstream_asset")
    return dg.MaterializeResult()

automation_sensor = dg.AutomationConditionSensorDefinition(
    name="downstream_automation_sensor",
    target=dg.AssetSelection.all(),
    minimum_interval_seconds=5,
    default_status=dg.DefaultSensorStatus.RUNNING,
)

@dg.definitions
def defs():
    return dg.Definitions(
        assets=[downstream_asset, multi_downstream_asset],
        sensors=[automation_sensor],
    )
