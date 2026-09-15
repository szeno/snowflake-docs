# Native SDK for Connectors release notes

Release notes of the Native SDK Example Java GitHub Connector.

## December 10th, 2024

### General changes

- Replaced the SnowSQL tool with new Snowflake CLI tool.
- Updated the example connector to the [newest SDK release](/release-notes/native-sdk-for-connectors/native_sdk_for_connectors_java#label-connectors-java-library-v2-2-0).
- Updated Java dependencies.

### Bug fixes

- Explicitly specified Java 11 as the target build version.
- Added missing grant for the `VIEWER` and `DATA_READER` app roles on the Streamlit UI.

## July 15th, 2024

### Behavior changes

- Adopted changes related to a new Identifiers approach introduced in the [Connectors Native SDK library version 2.1.0](/release-notes/native-sdk-for-connectors/native_sdk_for_connectors_java#label-connectors-java-library-v2-1-0).
- Implemented OAuth as an authentication mechanism in the Connection Configuration step of the Wizard.
  The connector no longer requires the user to create an `EXTERNAL ACCESS INTEGRATION` and `SECRET` objects with GitHub credentials.

### New features

- Added backend internal implementations of resource management procedures handlers and their callbacks:

  - Implementations for `PUBLIC.CREATE_RESOURCE()` callbacks available in [com.snowflake.connectors.example.ingestion.create](https://github.com/snowflakedb/connectors-native-sdk/tree/main/templates/connectors-native-sdk-template/src/main/java/com/snowflake/connectors/example/ingestion/create).
  - Implementations for `PUBLIC.ENABLE_RESOURCE()` procedure and its’ callbacks available in [com.snowflake.connectors.example.ingestion.enable](https://github.com/snowflakedb/connectors-native-sdk/tree/main/templates/connectors-native-sdk-template/src/main/java/com/snowflake/connectors/example/ingestion/enable).
  - Implementations for `PUBLIC.DISABLE_RESOURCE()` procedure and its’ callbacks available in [com.snowflake.connectors.example.ingestion.disable](https://github.com/snowflakedb/connectors-native-sdk/tree/main/templates/connectors-native-sdk-template/src/main/java/com/snowflake/connectors/example/ingestion/disable).
  - Implementations for `PUBLIC.UPDATE_RESOURCE()` procedure and its’ callbacks available in [com.snowflake.connectors.example.ingestion.update](https://github.com/snowflakedb/connectors-native-sdk/tree/main/templates/connectors-native-sdk-template/src/main/java/com/snowflake/connectors/example/ingestion/update).
- Changes in UI `Data sync` tab related to resource management:

  - Displaying values of `resource_id`, `name` and `resource_ingestion_definition_id` for each created resource in resources list.
  - Added functionality of enabling and disabling created resources.

### Bug fixes

- Correction to `setup.sql` script which was failing during the application version upgrade/downgrade.

## May 24th, 2024

Initial release.
