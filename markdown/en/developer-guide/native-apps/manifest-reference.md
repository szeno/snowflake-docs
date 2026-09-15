# Snowflake Native App manifest reference

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

A manifest file is a text-based [YAML](https://yaml.org/spec/) file with the filename: `manifest.yml`. The manifest file is used to define a Snowflake Native App and its associated data and logic. This topic describes the structure and fields of the manifest file.

For information about creating the manifest file for an app, see [Create the manifest file for an app](/developer-guide/native-apps/manifest-overview).

## Snowflake Native App manifest

The general format of a Snowflake Native App manifest is:

Copy code

```
manifest_version:           # required manifest version
version:                    # optional version metadata
artifacts:                  # required app resources and scripts
configuration:              # optional logging/tracing/metrics and callbacks
lifecycle_callbacks:        # optional lifecycle callbacks
privileges:                 # optional requested privileges in consumer account
snowflake_database:         # optional requested roles in the SNOWFLAKE database
references:                 # optional requested references in consumer account
restricted_callers_rights:  # optional restricted callers rights config
restricted_features:        # optional restricted features config
```

## Manifest fields

Snowflake Native App manifests include the following fields. Each section below describes a field’s purpose and structure, and provides an example.

### `manifest_version` field

The `manifest_version` field (Integer, required) specifies the version of the Snowflake Native App manifest file format. This value controls which manifest features are available and how Snowflake interprets the rest of the manifest.

#### `manifest_version: 1`

This version of the manifest file supports the current and legacy
functionality of Snowflake Native Apps.

#### `manifest_version: 2`

This version of the manifest file provides support for additional
features, including automated granting of privileges.

Caution

Before using version 2 of the manifest file, consider the security
implications described in [About the manifest file](/developer-guide/native-apps/manifest-overview#label-native-apps-manifest-about).

#### `manifest_version` field example

Copy code

```
manifest_version: 2
```

### `version` field

The `version` field (block, optional) defines metadata about the version of the Snowflake Native App being published, including the version name, default patch number, display label, and an optional comment. When present, this block helps providers track and present releases. For more information about versions and patches, see [Update an app (Legacy)](/developer-guide/native-apps/update-app).

Note

Versions and patches defined using the
[CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package) or
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) commands take
precedence over those defined in the manifest file.

#### `version.name` field

Specifies the name of the version. The version name can
only contain alphanumeric characters, underscores (\_), hyphens (-), dollar signs ($), periods (.), and spaces.

This field is optional.

Example: `name: v1`

#### `version.patch` field

Specifies the default patch number.

This field is optional.

Example: `patch: 1`

#### `version.label` field

Specifies a name for the version that is displayed to consumers.

This field is optional.

Example: `label: "Initial Release"`

#### `version.comment` field

Specifies a comment for the version. This comment is visible in Snowsight or when the provider runs the [SHOW VERSIONS IN APPLICATION PACKAGE](/sql-reference/sql/show-versions) command.

This field is optional.

Example: `comment: "This is the initial release of the app."`

#### `version` field example

Copy code

```
version:
  name: v1
  patch: 1
  label: "Initial Release"
  comment: "This is the initial release of the app."
```

### `artifacts` field

The `artifacts` field (block, required) defines the core resources that the Snowflake Native App uses, such as the setup script, readme, default Streamlit app, and any container image configuration. This block tells Snowflake where to find the code and assets needed to install, upgrade, and run the app.

#### `artifacts.setup_script` field

Specifies the path and filename of the setup script that is run when
the Snowflake Native App is installed or upgraded. If you do not specify a
value, the app uses the default value of `setup.sql` in the same
directory as the manifest file. The setup script name and path
can only contain alphanumeric characters, underscores (\_), hyphens (-), periods (.), backslashes (), and forward slashes (/).

Example: `setup_script: scripts/setup.sh`

#### `artifacts.readme` field

Specifies a path to a Markdown readme file that provides an overview of the app and its functionality.

In the case of a Streamlit app, if no value is specified for the `default_streamlit` property, the contents of this file is displayed to consumers when viewing the installed Snowflake Native App.

The location of this file is specified relative to the location of the manifest file.

This field is optional, however Snowflake recommends that you include a readme file with your app.

Example: `readme: docs/README.md`

#### `artifacts.default_streamlit_app` field

If the Snowflake Native App includes a Streamlit app, this property specifies
the schema and name of the default Streamlit app available to consumers.

This field is required if the app includes a Streamlit app.

#### `artifacts.extension_code` field

Enables or disables the use of extension code languages, including Java, Python, and Scala.

Example: `extension_code: true`

#### `artifacts.container_services` field

Specifies the location of the container images used by an app with containers. See [Specify the container images used by an app with containers](/developer-guide/native-apps/manifest-overview#label-native-apps-container-manifest-image-path)
for more information.

This field is required for an app with containers.

##### `artifacts.container_services.uses_gpu` field

Indicates that the app with containers uses a GPU.

This field is required for an app with containers.

Example: `uses_gpu: true`

##### `artifacts.container_services.images` field

Specifies the path to each of the container images used by an app with
containers.

This field is required for an app with containers.

Example:

Copy code

```
images:
- /spcs_app/napp/img_repo/eap_frontend
- /spcs_app/napp/img_repo/eap_backend
- /spcs_app/napp/img_repo/eap_router
```

#### `artifacts` field example

Copy code

```
artifacts:
  setup_script: scripts/setup.sql
  readme: docs/README.md
  default_streamlit_app: apps/main.py
  extension_code: true
  container_services:
    uses_gpu: true
    images:
      - /spcs_app/napp/img_repo/eap_frontend
      - /spcs_app/napp/img_repo/eap_backend
```

### `configuration` field

The `configuration` field (block, optional) specifies runtime configuration for the Snowflake Native App, including logging, tracing, and metrics levels, and — when applicable — the callback used to provision container resources. Providers use this block to control how much operational telemetry the app emits and how certain setup tasks are performed during installation.

#### `configuration.log_level` field

Specifies the logging level to use for the app Snowflake Native App.

If you do not set a value for this property, the default log data is
not captured.

For information about supported values, see
[Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

#### `configuration.trace_level` field

Specifies the trace event level to use for the app. When a provider
enables tracing, the app automatically captures the start and end times
for all queries and stored procedure calls.

Caution

Publishing an app with the `trace_level` property set to a
value other than `OFF` might expose calls to hidden stored procedures to any user in the consumer account who can view
the event table.

If you do not set a value for this property, trace events are not captured.

For the supported values of the `trace_level` property, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

#### `configuration.metric_level` field

Specifies the metric level to use for the app. When a provider enables
metrics the app automatically emits auto-instrumented resource metrics
data points to the event table.

See [Set the log and trace levels for an app](/developer-guide/native-apps/event-definition#label-nativeapps-provider-logging-configure) for more information.

For the supported values of the `metric_level` property, see
[Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

### `log_event_level:`

Specifies the event logging level to use for the Snowflake Native App.

If you do not set a value for this property, log events are not captured.

For the supported values of the `log_event_level` property, see
[LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level).

### `grant_callback:`

#### `configuration.grant_callback` field

Specifies the schema and name of the callback function for an app with
containers. The callback function is a stored procedure that can create
compute pools, services, and perform other setup tasks required by the
application.

This field is required for an app with containers.

For more information, see [Create a service by using the `grant\_callback` property](/developer-guide/native-apps/container-services#label-native-apps-container-service-grant-callback).

Example: `grant_callback: my_schema.my_grant_callback`

#### `configuration` field example

Copy code

```
configuration:
  log_level: INFO
  trace_level: OFF
  metric_level: BASIC
  log_event_level: INFO
  grant_callback: my_schema.my_grant_callback
```

### `lifecycle_callbacks` field

The `lifecycle_callbacks` field (block, optional) defines stored procedures that Snowflake runs at specific points in the Snowflake Native App lifecycle. Each entry in this block names a lifecycle callback and points to the procedure that implements it, allowing the app to validate configuration changes, prepare resources, or react to other lifecycle events when those callbacks are invoked.

For more information, see [Callbacks](/developer-guide/native-apps/callbacks).

#### `lifecycle_callbacks.\<callback_name\>` field

Specifies the name of a lifecycle callback for the app.

This field is required if the `lifecycle_callbacks` property is specified.

#### `lifecycle_callbacks` field example

Copy code

```
lifecycle_callbacks:
  before_configuration_change: app_schema.before_config_change_callback
```

### `privileges` field

The `privileges` field (block, optional) defines the privileges that the Snowflake Native App requests in a consumer account. Each entry in this block describes a specific privilege, along with a human-readable explanation of why the app needs it, so consumers can make informed decisions when granting access.

This field is required if the app requests privileges in the consumer account.

#### `privileges.\<privilege_name\>` field

Specifies the name of a privilege that the app requests in a consumer account.

This field is required if the `privileges` property is specified.

#### `privileges.description` field

Provides a description of the privilege being requested. The text
specified in `description` is displayed to the consumer when the
privilege is displayed in Snowsight using the Python Permission SDK, or
when the [SHOW PRIVILEGES](/sql-reference/sql/show-privileges) command is run.

As a provider, you should include as much information as possible about why the Snowflake Native App needs this privilege and if the privilege is required or optional.

This field is required if the `privileges` field is specified.

#### `privileges` field example

Copy code

```
privileges:
- CREATE TABLE:
  description: 'Required to create tables in the consumer account.'
- CREATE COMPUTE POOL:
  description: 'Required to allow the app to create a compute pool in the consumer account.'
- BIND SERVICE ENDPOINT:
  description: 'Required to allow endpoints to be externally accessible.'
```

### `snowflake_database` field

The `snowflake_database` field (block, optional) defines the database roles and application roles in the SNOWFLAKE database that the Snowflake Native App requests to be granted to the application. Similar to how an app requests account-level [privileges](#label-manifest-native-app-manifest-fields-privileges), the roles requested here are presented to consumers, who can review, grant, and revoke them.

This field is required if the app requests roles in the SNOWFLAKE database.

#### `snowflake_database.roles` field

Specifies a list of the database roles and application roles in the SNOWFLAKE database that the app requests. Each entry specifies a role name and an optional description.

This field is required if the `snowflake_database` field is specified.

#### `snowflake_database.roles.\<role_name\>` field

Specifies the name of a role in the SNOWFLAKE database that the app requests.

This field is required if the `snowflake_database` field is specified.

#### `snowflake_database.roles.\<role_name\>.description` field

Provides a description of the role being requested. The text specified in `description` is displayed to the consumer when they review the requested roles for the listing.

This field is optional.

#### `snowflake_database` field example

Copy code

```
snowflake_database:
  roles:
    - CORTEX_USER:
        description: 'Required to call Snowflake Cortex AI functions.'
```

### `references` field

The `references` field (block, optional) describes the external objects in a consumer account — such as tables, views, secrets, or integrations — that the Snowflake Native App expects to bind to. Each reference entry specifies a label, description, required privileges, and other properties that guide consumers through providing the correct objects and permissions.

This field is required if the app requests references in the consumer
account.

#### `references.\<reference_name\>` field

Specifies the name of a reference that the app is requesting in a
consumer account.

This field is required if the `references` property is specified.

#### `references.\<reference_name\>.label` field

Specifies a label for the reference that is displayed to consumers.

This field is required if the `references` property is specified.

Example: `label: "Orders table"`

#### `references.\<reference_name\>.description` field

Provides a description of the reference being requested. The text
specified in `description` is displayed to the consumer when the
reference is displayed in Snowsight using the Python Permission SDK, or
when the [SHOW REFERENCES](/sql-reference/sql/show-references) command is run.

This field is required if the `references` property is specified.

#### `references.\<reference_name\>.privileges` field

Specifies a list of privileges that the app requires on the object to
which the reference is bound in the consumer account.

This field is required if the `references` property is specified.

Example:

Copy code

```
privileges:
  - SELECT
  - INSERT
```

#### `references.\<reference_name\>.object_type` field

Specifies the type of object associated with the reference, such as a schema and table, or an API integration.

This field is required if the `references` field is specified.

Example: `object_type: TABLE`

For more information, see
[Object types and privileges that a reference can contain](/developer-guide/native-apps/requesting-refs#label-native-apps-supported-privs-references).

#### `references.\<reference_name\>.multi_valued` field

Allows more than one object to be associated with the reference.
Use this property to bind multiple consumer objects to the same reference. When this property is specified, the same operations are
performed on objects with a single value reference. The property
can also be used with objects with multi-valued references.

This field is optional. The default value is `false`.

For more information, see
[Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

Example: `multi_valued: true`

#### `references.\<reference_name\>.register_callback` field

Specifies the schema and name of the callback stored procedure that is run
when the consumer binds the reference to an object in their account.

This field is required if the `references` property is specified.

Example: `register_callback: my_schema.my_register_callback`

#### `references.\<reference_name\>.configuration_callback` field

Specifies the name of the callback function that provides the desired configuration for the object to bind to this reference.

This property is required if `object_type` is
`EXTERNAL ACCESS INTEGRATION` or `SECRET`. This property is not applicable to other types of objects.

#### `references.\<reference_name\>.required_at_setup` field

Indicates that references must be bound when the app is installed.

Example: `required_at_setup: true`

#### `references` field example

Copy code

```
references:
- ORDERS_TABLE:
    label: "Orders table"
    description: "Orders table in TPC-H samples"
    privileges:
      - SELECT
    object_type: VIEW
    multi_valued: false
    register_callback: v1.register_single_callback

- EXTERNAL_ENDPOINT_EAI:
    label: "Allows egress to an external API"
    description: "EAI for Egress from NA+SPCS"
    privileges: [USAGE]
    object_type: EXTERNAL_ACCESS_INTEGRATION
    register_callback: v1.register_single_callback
    configuration_callback: v1.get_configuration
    required_at_setup: true
```

### `restricted_callers_rights` field

The `restricted_callers_rights` field (block, optional) controls whether the Snowflake Native App is allowed to create executables — such as stored procedures or services — that run with restricted callers’ rights. Providers use this block to declare that the app needs to run certain logic with the caller’s privileges and to explain why that behavior is required.

This field is required if the app creates stored procedures or Snowpark Container Services
services that run with restricted caller’s rights.

For more information, see
[Use owner’s rights and restricted caller’s rights in an app](/developer-guide/native-apps/restricted-callers-rights).

#### `restricted_callers_rights.enabled` field

Specifies whether the app is allowed to create executables with restricted caller’s rights.

Providers must set this property to `true` if the app creates stored procedures or Snowpark Container Services services that run with restricted caller’s rights.

#### `restricted_callers_rights.description` field

Provides a description of why the app needs to create executables with
restricted caller’s rights.

#### `restricted_callers_rights` field example

Copy code

```
restricted_callers_rights:
  enabled: true
  description: "Required to create stored procedures that run with restricted caller's rights."
```

### `restricted_features` field

The `restricted_features` field (block, optional) declares any features that require explicit consumer approval before the Snowflake Native App can enable them, such as access to external or Apache Iceberg™ data. This block helps providers document potentially sensitive capabilities and allows consumers to review and consent to their use during installation.

#### `restricted_features.external_data` field

If present, specifies that the app shares external tables or Iceberg tables. For more information, see
[Request access to external and Apache Iceberg™ tables](/developer-guide/native-apps/requesting-external-tables).

#### `restricted_features.external_data.description` field

Provides a description of the external or Iceberg table being requested.

This field is required if the `restricted_features.external_data` property is specified.

#### `restricted_features` field example

Copy code

```
restricted_features:
  - external_data:
      description: "The reason for enabling an external or Iceberg table."
```

## Manifest file example

The following code block is an example of a Snowflake Native App manifest file.

Copy code

```
manifest_version: 2

version:
  name: v1
  patch: 1
  label: "Initial Release"
  comment: "This is the initial release of the app."

artifacts:
  setup_script: scripts/setup.sql
  readme: docs/README.md
  default_streamlit_app: apps/main.py
  extension_code: true
  container_services:
    uses_gpu: true
    images:
      - /spcs_app/napp/img_repo/eap_frontend
      - /spcs_app/napp/img_repo/eap_backend
      - /spcs_app/napp/img_repo/eap_router

configuration:
  log_level: INFO
  trace_level: OFF
  metric_level: BASIC
  grant_callback: my_schema.my_grant_callback

lifecycle_callbacks:
  <callback_name>:
    # See callbacks documentation for the full shape of each callback entry.
    # This is a placeholder showing that callback names appear under lifecycle_callbacks.
    # Example:
    #   procedure: v1.before_configuration_change

privileges:
  - CREATE TABLE:
      description: "Required to create tables in the consumer account."
  - CREATE COMPUTE POOL:
      description: "Required to allow the app to create a compute pool in the consumer account."
  - BIND SERVICE ENDPOINT:
      description: "Required to allow endpoints to be externally accessible."

references:
  - ORDERS_TABLE:
      label: "Orders table"
      description: "Orders table in TPC-H samples"
      privileges:
        - SELECT
      object_type: VIEW
      multi_valued: false
      register_callback: v1.register_single_callback

  - EXTERNAL_ENDPOINT_EAI:
      label: "Allows egress to an external API"
      description: "EAI for Egress from NA+SPCS"
      privileges: [USAGE]
      object_type: EXTERNAL_ACCESS_INTEGRATION
      register_callback: v1.register_single_callback
      configuration_callback: v1.get_configuration
      required_at_setup: true

restricted_callers_rights:
  enabled: true
  description: "Required to create stored procedures that run with restricted caller's rights."

restricted_features:
  - external_data:
      description: "The reason for enabling an external or Iceberg table."
```
