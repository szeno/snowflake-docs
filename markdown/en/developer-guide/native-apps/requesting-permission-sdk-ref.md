# Python Permission SDK reference

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides reference information for the functions supported by the `snowflake.permissions`
module of the Python Permission SDK. For information on using the Python Permission SDK to request privileges in the consumer account, see [Create a user interface to request privileges and references](/developer-guide/native-apps/requesting-ui).

## get\_application\_configurations()

Returns all application configurations defined for the app.

Signature:
:   Copy code

    ```
    get_application_configurations()
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   A list of dictionaries, where each dictionary contains the following key/value pairs:

    Copy code

    ```
    {
      "name": "<value>",
      "created_on": "<value>",
      "updated_on": "<value>",
      "type": "<value>",
      "status": "<value>",
      "value": "<value>",
      "value_updated_on": "<value>",
      "label": "<value>",
      "description": "<value>",
      "application_roles": "<value>"
    }
    ```

    Where:

    - `name`: The name of the configuration.
    - `created_on`: Timestamp when the configuration was created.
    - `updated_on`: Timestamp when the configuration was last updated.
    - `type`: Type of configuration. Supported values are: `APPLICATION_NAME`, `STRING`, and `SECRET_AUTHORIZATION`.
    - `status`: Specifies the current status of the configuration. Possible values are `PENDING` and `DONE`.
    - `value`: The current value of the configuration, if set.
    - `value_updated_on`: Timestamp when the value was last updated.
    - `label`: Name of the configuration that is displayed to the consumer in Snowsight.
    - `description`: Description of the configuration that is displayed to the consumer in Snowsight.
    - `application_roles`: The application roles that have access to the configuration.

## get\_application\_specifications()

Returns all app specifications defined for the app.

Signature:
:   Copy code

    ```
    get_application_specifications()
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   A list of dictionaries, where each dictionary contains the following key/value pairs:

    Copy code

    ```
    {
      "name": "<value>",
      "requested_on": "<value>",
      "type": "<value>",
      "sequence_number": "<value>",
      "status": "<value>",
      "status_upgraded_on": "<value>",
      "label": "<value>",
      "description": "<value>",
      "definition": "<value>",
    }
    ```

    Where:

    - `name`: The name of the app specification.
    - `requested_on`: Timestamp when the app specification was requested.
    - `type`: Type of app specification. Supported values are: EXTERNAL ACCESS, SECURITY INTEGRATION, LISTING, and CONNECTION.
    - `sequence_number`: ID for a version of an app specification. This value is incremented each time a provider
      changes the [app specification definition](/developer-guide/native-apps/requesting-app-specs#label-native-apps-app-spec-definition).
    - `status`: Specifies the current status of the app specification. Possible values are:

      - `APPROVED`: The consumer approved the app specification.
      - `DECLINED`: The consumer declined the app specification.
      - `PENDING`: The app specification is waiting for the consumer to approve or decline.
    - `status_updated_on`: Timestamp of the last status change.
    - `label`: Name of the app specification that is displayed to the consumer in Snowsight.
    - `description`: Description of the app specification that is displayed to the consumer in Snowsight.
    - `definition`: Values that are part of the
      [app specification definition](/developer-guide/native-apps/requesting-app-specs#label-native-apps-app-spec-definition). The values of
      this column depend on the type of app specification.

## get\_detailed\_reference\_associations()

Provides detailed information about a reference to an object in the consumer account.

Signature:
:   Copy code

    ```
    get_detailed_reference_associations(reference_name: str) -> List[dict]
    ```

Arguments:
:   A string value containing the name of a reference.

Returns:
:   Returns a JSON object representing a list of dictionaries. Each dictionary contains the following
    key/value pairs:

    Copy code

    ```
    {
      "alias": "<value>",
      "database": "<value>",
      "schema": "<value>",
      "name": "<value>"
    }
    ```

    Where:

    - `alias`: The system-generated alias for the reference.
    - `database`: The parent database name of the consumer object, if the object resides in a database.
      Otherwise, null.
    - `schema`: The parent schema of the consumer object, if the object resides in a schema. Otherwise,
      null.
    - `name`: The name of the consumer object.

## get\_held\_account\_privileges()

Returns the privileges that have been granted to the app.

Signature:
:   Copy code

    ```
    get_held_account_privileges(privilege_names: [str]) -> [str]
    ```

Arguments:
:   A list of string values containing the names of privileges to check.

Returns:
:   Returns a list containing the privileges that have been granted to the Snowflake Native App
    based on the list of privileges passed to the function.

## get\_missing\_account\_privileges()

Returns the privileges that have not been granted to the app.

Signature:
:   Copy code

    ```
    get_missing_account_privileges(privilege_names: [str]) -> [str]
    ```

Arguments:
:   A list of string values containing the names of privileges to check.

Returns:
:   Returns a list containing the privileges that have **not** been granted to the app
    based on the list of privileges passed to the function.

## get\_reference\_associations()

Determines the objects in the consumer account that are associated with a reference.

To get more detailed information about references to objects in the consumer account,
use [get\_detailed\_reference\_associations()](#label-native-apps-get-detailed-reference-associations).

Signature:
:   Copy code

    ```
    get_reference_associations(reference_name: str) -> [str]
    ```

Arguments:
:   A string value containing the name of a reference.

Returns:
:   Returns a list containing Snowflake-generated aliases of objects in the consumer account
    that are bound to the reference.

## is\_application\_all\_mandatory\_telemetry\_event\_definitions\_enabled()

Checks if all mandatory telemetry event definitions are enabled for the app.

For more information on telemetry event sharing, see
[Verify event definitions by using the Permissions SDK](/developer-guide/native-apps/event-develop#label-native-apps-verify-event-definitions).

Signature:
:   Copy code

    ```
    is_application_all_mandatory_telemetry_event_definitions_enabled() -> bool
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   Returns TRUE if all mandatory telemetry event definitions are enabled for the app.
    Returns FALSE, otherwise.

## is\_application\_authorized\_for\_telemetry\_event\_sharing()

Checks if the current application is authorized for telemetry event sharing.

For more information on telemetry event sharing, see [Verify event definitions by using the Permissions SDK](/developer-guide/native-apps/event-develop#label-native-apps-verify-event-definitions).

Signature:
:   Copy code

    ```
    is_application_authorized_for_telemetry_event_sharing() -> bool
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   Returns TRUE if the application is authorized for telemetry event sharing.
    Returns FALSE, otherwise.

## is\_application\_local\_to\_package()

Checks if the app is installed in the same account as the application package.

Signature:
:   Copy code

    ```
    is_application_local_to_package() -> bool
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   Returns TRUE if the app is installed in the same account as the application package.
    Returns FALSE, otherwise.

## is\_event\_sharing\_enabled()

Checks if event sharing is enabled for the app.

Signature:
:   Copy code

    ```
    is_event_sharing_enabled() -> bool
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   Returns TRUE if the SHARE\_EVENTS\_WITH\_PROVIDER property is true and the consumer account has an
    active event table configured. Returns FALSE, otherwise.

## is\_external\_data\_enabled()

Checks if the current application is enabled to use external and iceberg tables.

Signature:
:   Copy code

    ```
    is_external_data_enabled() -> bool
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   Returns TRUE if the app is enabled to use external and iceberg tables.
    Returns FALSE, otherwise.

## is\_viewer\_mode()

Checks if the app is running in the standalone app-viewer context, where permission-request
dialogs aren’t available.

When a consumer opens a Streamlit app using its app-viewer URL outside of Snowsight, the app runs
in a context where the `request_*()` functions can’t display a dialog to the consumer. Use this
function to detect that context and adjust the behavior of your app, for example by hiding
permission-request controls or showing a message that directs the consumer to open the app in
Snowsight.

Signature:
:   Copy code

    ```
    is_viewer_mode() -> bool
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   Returns TRUE if the app is running in the standalone app-viewer context, where the `request_*()`
    functions can’t display a dialog. Returns FALSE, otherwise. If the context can’t be determined,
    this function returns TRUE.

## request\_application\_specification\_review()

Opens a dialog in a Streamlit app that allows the consumer to review an app specification, and then
approve, decline, or take no action. A consumer can only decline an app specification if it is optional.

Signature:
:   Copy code

    ```
    request_application_specification_review(spec_names: [str] = None)
    ```

Arguments:
:   An optional list of string values containing the names of the app specifications to review. If this parameter is
    not specified, the dialog will show all app specifications defined for the app.

Returns:
:   This method does not return a value.

## request\_application\_configuration\_value()

Opens a dialog in a Streamlit app that allows the consumer to review and set values for
application configurations. For more information, see [Application configuration](/developer-guide/native-apps/app-configuration).

Signature:
:   Copy code

    ```
    request_application_configuration_value(config_names: [str] = None)
    ```

Arguments:
:   An optional list of string values containing the names of the configurations to review. If this
    parameter is not specified, the dialog shows all configurations defined for the app.

Returns:
:   This method does not return a value.

## request\_application\_connection\_review()

Opens a dialog in a Streamlit app that allows the consumer to review and approve an application
connection for [inter-app communication](/developer-guide/native-apps/inter-app-communication).

Signature:
:   Copy code

    ```
    request_application_connection_review(config_name: str)
    ```

Arguments:
:   A string value containing the name of the application configuration object associated with
    the connection.

Returns:
:   This method does not return a value.

## request\_aws\_api\_integration()

Requests an API integration from the consumer for the Amazon API Gateway.

You must define the API integration in the manifest file. For more information,
see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) for information on other parameters.

Signature:
:   Copy code

    ```
    request_aws_api_integration(id: str, allowed_prefixes: [str], gateway: AwsGateway, aws_role_arn: str, api_key: str = None, name: str = None, comment: str = None)
    ```

Arguments:
:   - `id`: The name of the API integration defined in the manifest file.
    - `allowed_prefixes`: A list of string values containing the allowed prefixes for the API integration.
    - `gateway`: The type of API Gateway to use. This parameter must be one of the following values:

      - permissions.AwsGateway.API\_GATEWAY
      - permissions.AwsGateway.PRIVATE\_API\_GATEWAY
      - permissions.AwsGateway.GOV\_API\_GATEWAY
      - permissions.AwsGateway.GOV\_PRIVATE\_API\_GATEWAY
    - `aws_role_arn`: The Amazon Resource Name (ARN) of the IAM role that the API Gateway uses to access the
      consumer account.
    - `api_key`: An optional API key for the API Gateway.
    - `name`: An optional name for the API integration.
    - `comment`: An optional comment for the API integration.

    See [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) for information on other possible parameters.

Returns:
:   A string value containing the name of a reference.

## request\_azure\_api\_integration()

Requests an API integration from the consumer for Azure API Management.

You must define the API integration in the manifest file. For more information,
see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) for information on other parameters.

Signature:
:   Copy code

    ```
    request_azure_api_integration(id: str, allowed_prefixes: [str], tenant_id: str, application_id: str, api_key: str = None, name: str = None, comment: str = None)
    ```

Arguments:
:   - `id`: The name of the API integration defined in the manifest file.
    - `allowed_prefixes`: A list of string values containing the allowed prefixes for the API integration.
    - `tenant_id`: The tenant ID for the Azure API Management.
    - `application_id`: The application ID for the Azure API Management.
    - `api_key`: An optional API key for the Azure API Management.
    - `name`: An optional name for the API integration.
    - `comment`: An optional comment for the API integration.

Returns:
:   This method does not return a value.

## request\_event\_sharing()

Opens a dialog in a Streamlit app that allows the consumer to share events with the app.

Signature:
:   Copy code

    ```
    request_event_sharing()
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   This method does not return a value.

## request\_external\_data()

Requests consent from the consumer to use external and iceberg tables.

Signature:
:   Copy code

    ```
    request_external_data()
    ```

Arguments:
:   This function does not take any arguments.

Returns:
:   This method does not return a value.

## request\_google\_api\_integration()

Requests an API integration from the consumer for Google Cloud API Gateway.

You must define the API integration in the manifest file. For more information,
see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) for information on other parameters.

Signature:
:   Copy code

    ```
    request_google_api_integration(id: str, allowed_prefixes: [str], audience: str, name: str = None, comment: str = None, api_key: str = None)
    ```

Arguments:
:   - `id`: The name of the API integration defined in the manifest file.
    - `allowed_prefixes`: A list of string values containing the allowed prefixes for the API integration.
    - `audience`: The audience for the Google Cloud API Gateway.
    - `name`: An optional name for the API integration.
    - `comment`: An optional comment for the API integration.
    - `api_key`: An optional API key for the Google Cloud API Gateway.

Returns:
:   This method does not return a value.

## request\_account\_privileges()

Requests privileges from the consumer specified by a list of strings passed to the function that
contains the privileges. The specified privileges must be listed in the manifest file.

Signature:
:   Copy code

    ```
    request_account_privileges(privileges: [str])
    ```

Arguments:
:   A list of strings containing a list of privileges the app is requesting.

Returns:
:   This method does not return a value.

## request\_reference()

Requests a reference from the consumer specified by the string passed to the function. The
reference passed to the function must be defined in the manifest file.

See [Object types and privileges that a reference can contain](/developer-guide/native-apps/requesting-refs#label-native-apps-supported-privs-references) for a list of the objects that can be
included in a reference and their supported privileges.

Signature:
:   Copy code

    ```
    request_reference(reference: str)
    ```

Arguments:
:   A string value containing the name of a reference to request.

Returns:
:   This method does not return a value.
