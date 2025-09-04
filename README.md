# Dagster run_in_progress issue example

This repository contains a minimal example to reproduce an issue with Dagster's automation evaluations when using `run_in_progress` in asset dependencies, where the any_deps_match(run_in_progress) condition does not return true when a dependency materalizes during an ongoing run.

## Structure

source-assets:
- `source_asset` is an asset that instantly materializes
- `source_multi_asset_x` is a multi-asset that materializes a series of assets, delaying between each
- `unrelated_asset_x` assets are included to delay the end of the run
- `source_assets_job` runs all source assets

downstream-assets:
- `downstream_asset` depends on `source_asset` and has automation_condition eager
- `multi_downstream_asset` depends on `source_multi_asset_0` and has automation_condition eager

## Observed behavior
- When `source_asset` materializes, `downstream_asset` automation evaluation requests a run, even if the source run is still in progress
- When `source_multi_asset_0` materializes, `multi_downstream_asset` automation evaluation requests a run, even if the source run is still in progress

## Expected behavior
- When `source_asset` materializes, `downstream_asset` automation evaluation requests a run only when the source run is complete
- When `source_multi_asset_0` materializes, `multi_downstream_asset` automation evaluation requests a run only when the source run is complete

Multi assets are included to show that issue still occurs when the op is still in progress

## Running the example
1. ```shell
   uv sync
   source .venv/bin/activate
   export DAGSTER_HOME=$(pwd)
   dagster dev
   ```
2. Launch `source_assets_job`
3. Check automation evaluations for `downstream_asset` and `multi_downstream_asset`, will have requested runs as soon as `source_asset` and `source_multi_asset_0` respectively have materialized, even if run is still in progress.


