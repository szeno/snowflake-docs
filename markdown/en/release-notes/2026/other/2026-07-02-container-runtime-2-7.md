# Jul 2, 2026: Snowflake Container Runtime version 2.7

Snowflake Container Runtime CPU and GPU version 2.7 is now available. This release includes the following changes:

- Added support for ipywidgets in notebooks.
- The PyTorch backend now defaults to Ray Train. To opt out, set `PYTORCH_USE_LEGACY_TRAINER=1`. The legacy path will be removed in an upcoming release.
- `TunerConfig` now defaults `resource_per_trial` to `{"CPU": 1}` when `uses_snowflake_trainer=True`.
- Fixed an issue where `get_session()` could overwrite the notebook database and schema context.

For the full package lists and details, see [Snowflake Container Runtime release notes](/developer-guide/snowflake-ml/container-runtime/releases).
