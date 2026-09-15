# CREATE SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Creates a new [Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services)
in the current schema. If a service with that name already exists, use the [DROP SERVICE](/sql-reference/sql/drop-service) command to delete the previously
created service.

You can run more than one instance of your service. Each service instance is a collection of containers, as defined in the
service specification file, that run together on a node in your compute pool. If you run multiple instances of a service, a load
balancer manages incoming traffic.

Note that the command parameters must be specified in specific order. For more information, see the Usage Notes section.

See also:
:   [ALTER SERVICE](/sql-reference/sql/alter-service) , [DESCRIBE SERVICE](/sql-reference/sql/desc-service), [DROP SERVICE](/sql-reference/sql/drop-service) , [SHOW SERVICES](/sql-reference/sql/show-services)

## Syntax

Copy code

```
CREATE SERVICE [ IF NOT EXISTS ] <name>
  IN COMPUTE POOL <compute_pool_name>
  {
     fromSpecification
     | fromSpecificationTemplate
  }
  [ AUTO_SUSPEND_SECS = <num> ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <EAI_name> [ , ... ] ) ]
  [ AUTO_RESUME = { TRUE | FALSE } ]
  [ MIN_INSTANCES = <num> ]
  [ MIN_READY_INSTANCES = <num> ]
  [ MAX_INSTANCES = <num> ]
  [ LOG_LEVEL = '<log_level>' ]
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COMMENT = '{string_literal}']
```

Where:

> Copy code
>
> ```
> fromSpecification ::=
>   {
>     FROM SPECIFICATION_FILE = '<yaml_file_path>' -- for native app service.
>     | FROM @<stage> SPECIFICATION_FILE = '<yaml_file_path>' -- for non-native app service.
>     | FROM SPECIFICATION <specification_text>
>   }
> ```
>
> Copy code
>
> ```
> fromSpecificationTemplate ::=
>   {
>     FROM SPECIFICATION_TEMPLATE_FILE = '<yaml_file_stage_path>' -- for native app service.
>     | FROM @<stage> SPECIFICATION_TEMPLATE_FILE = '<yaml_file_stage_path>' -- for non-native app service.
>     | FROM SPECIFICATION_TEMPLATE <specification_text>
>   }
>   USING ( <key> => <value> [ , <key> => <value> [ , ... ] ]  )
> ```

## Required parameters

`name`
:   String that specifies the identifier (that is, the name) for the service; it must be unique for the schema in which the service
    is created.

    Quoted names for special characters or case-sensitive names are not supported. The same constraint also applies to database
    and schema names where you create a service. That is, database and schema names without quotes are valid when creating a
    service.

`IN COMPUTE POOL compute_pool_name`
:   Specifies the name of the compute pool in your account on which to run the service.

`FROM ...`
:   Identifies the [specification](/developer-guide/snowpark-container-services/specification-reference) or
    the [template](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-using-specification-templates) specification for the service.

    **Using a service specification**

    You can either define the specification either [inline or in a separate file](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-creating-service).

    `SPECIFICATION_FILE = 'yaml_file_path'` or `@stage SPECIFICATION_FILE = 'yaml_file_path'` or `SPECIFICATION specification_text`
    :   Specifies the file containing the service specification or the service specification inline. If your service specification is in a file, use SPECIFICATION\_FILE. For services created in a Snowflake Native App, omit `@stage`, and specify a path relative to the app root directory. For services created in other contexts, specify the Snowflake internal stage and path to the service specification file.

    **Using a service specification template**

    You can either define the [template specification](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-using-specification-templates) either [inline or in a separate file](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-creating-service).

    `SPECIFICATION_TEMPLATE_FILE = 'yaml_file_path'` or `@stage SPECIFICATION_TEMPLATE_FILE = 'yaml_file_path'` or `SPECIFICATION_TEMPLATE specification_text`
    :   Specifies the file containing the service specification template or the service specification template inline. If your service specification template is in a file, use SPECIFICATION\_TEMPLATE\_FILE. For services created in a Snowflake Native App, omit `@stage`, and specify a path relative to the app root directory. For services created in other contexts, specify the Snowflake internal stage and path to the service specification file. When using template specification, you should also include the `USING` parameter.

    `USING ( key => value [ , key => value [ , ... ] ] )`
    :   Specifies the template variables and the values of those variables.

        - `key` is the name of the template variable. The template variable name can optionally be enclosed in double quotes
          (`"`).
        - `value` is the value to assign to the variable in the template. String values must be enclosed in `'` or
          `$$`. The value must either be alphanumeric or valid JSON.

        Use a comma between each key-value pair.

## Optional parameters

`AUTO_SUSPEND_SECS = num`
:   Specifies the number of seconds of inactivity (service is idle) after which Snowflake automatically suspends the service. Inactivity means no queries (that invoke a service function) executed for the time period specified by AUTO\_SUSPEND\_SECS. You can configure this value to 300 seconds or more to enable auto-suspension. For more information, see [Suspending a service](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-suspend-service).

    Default: 0 seconds, which indicates Snowflake does not suspend the service automatically.

    [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Configuring the automatic suspension of a Snowpark Container Services service using the AUTO\_SUSPEND\_SECS property is a [preview feature](/release-notes/preview-features).

`EXTERNAL_ACCESS_INTEGRATIONS = ( EAI_name [ , ... ] )`
:   Specifies the names of the [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access) that allow your service to access external sites.
    The names in this list are case-sensitive. By default, application containers don’t have
    permission to access the internet. If you want to allow your service to access an external site, create an External Access Integration
    (EAI), and configure your service to use that integration. For more
    information, see [Configure service egress](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress).

`AUTO_RESUME = { TRUE | FALSE }`
:   Specifies whether to automatically resume a service when user performs one of the following actions that depend on the service:

    - Executing a query is that uses a [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function).
    - Sending a request to the public endpoint exposed by the service ([ingress](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-ingress)).

    If AUTO\_RESUME is FALSE, you need to explicitly resume the service (using [ALTER SERVICE … RESUME](/sql-reference/sql/alter-service)).

    Default: TRUE.

`MIN_INSTANCES = num`
:   Specifies the minimum number of service instances to run.

    Default: 1.

`MIN_READY_INSTANCES = num`
:   Indicates the minimum service instances that must be ready for Snowflake to consider the service is ready to process requests.
    MIN\_READY\_INSTANCES must be equal to or less than MIN\_INSTANCES. For more information, see [Scaling services](/developer-guide/snowpark-container-services/working-with-services#scaling-services).

    Default: The value of the MIN\_INSTANCES property.

`MAX_INSTANCES = num`
:   Specifies the maximum number of service instances to run.

    Default: The value of the MIN\_INSTANCES property.

`LOG_LEVEL = 'log_level'`
:   Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at
    the specified level (and at more severe levels) are ingested.
    Currently, LOG\_LEVEL is supported only for [platform events](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-monitoring-services-access-platform-events), Changing LOG\_LEVEL for [container logs](/developer-guide/snowpark-container-services/monitoring-services#label-snowpark-containers-working-with-services-local-logs) is not supported.

    For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting the log level, see
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

`QUERY_WAREHOUSE = warehouse_name`
:   Warehouse to use if a service container connects to Snowflake to execute a query but does not explicitly specify a warehouse
    to use. This parameter also supports object references in Native Apps. For more information, see [Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

    Default: none.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`COMMENT = 'string_literal'`
:   Specifies a comment for the service.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SERVICE | Schema |  |
| USAGE | Compute pool |  |
| READ | Stage | This is the stage where the specification is stored. |
| READ | Image repository | Repository of images referenced by the specification. |
| BIND SERVICE ENDPOINT | Account | A role must have this privilege to create a service with public endpoints. This allows the service access through the public endpoints. If the service’s owner role loses this privilege, the public endpoints will not be accessible. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When calling CREATE SERVICE, the parameters should be provided in this order: specify compute pool, followed by the service specification (either provider specification file on stage or inline specification), and then other properties.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a service with two service instances running:

Copy code

```
CREATE SERVICE echo_service
  IN COMPUTE POOL tutorial_compute_pool
  FROM @tutorial_stage
  SPECIFICATION_FILE='echo_spec.yaml'
  MIN_INSTANCES=2
  MAX_INSTANCES=2
```
