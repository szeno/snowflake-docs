# ALTER SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Modifies [Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services)
configuration, upgrades the code for the service, and allows you to suspend or resume a service. You can:

- Apply modifications to a running service. For example, suspend or resume a service, and update the number of service instances
  running.
- Apply modifications that take effect only after service is restarted. For example, specify a default warehouse for queries.
- Apply modifications that cause Snowflake to shut down the service, and restart using new code. For example, you might want to
  deploy updated service code.
- Restart the specified instances of a service using the snapshot provided as the initial content for the specified volume. The service must be suspended before you execute ALTER SERVICE.

See also:
:   [CREATE SERVICE](/sql-reference/sql/create-service) , [DESCRIBE SERVICE](/sql-reference/sql/desc-service), [DROP SERVICE](/sql-reference/sql/drop-service) , [SHOW SERVICES](/sql-reference/sql/show-services)

## Syntax

Copy code

```
ALTER SERVICE [ IF EXISTS ] <name> { SUSPEND | RESUME }

ALTER SERVICE [ IF EXISTS ] <name>
  {
     fromSpecification
     | fromSpecificationTemplate
  }

ALTER SERVICE [IF EXISTS] <service_name> RESTORE VOLUME <volume_name>
                                                 INSTANCES <comma_separated_instance_ids>
                                                 FROM SNAPSHOT <snapshot_name>

ALTER SERVICE [ IF EXISTS ] <name> SET [ MIN_INSTANCES = <num> ]
                                       [ MAX_INSTANCES = <num> ]
                                       [ LOG_LEVEL = '<log_level>' ]
                                       [ AUTO_SUSPEND_SECS = <num> ]
                                       [ MIN_READY_INSTANCES = <num> ]
                                       [ QUERY_WAREHOUSE = <warehouse_name> ]
                                       [ AUTO_RESUME = { TRUE | FALSE } ]
                                       [ EXTERNAL_ACCESS_INTEGRATIONS = ( <EAI_name> [ , ... ] ) ]
                                       [ COMMENT = '<string_literal>' ]

ALTER SERVICE [ IF EXISTS ] <name> UNSET { MIN_INSTANCES                |
                                           AUTO_SUSPEND_SECS            |
                                           MAX_INSTANCES                |
                                           LOG_LEVEL                    |
                                           MIN_READY_INSTANCES          |
                                           QUERY_WAREHOUSE              |
                                           AUTO_RESUME                  |
                                           EXTERNAL_ACCESS_INTEGRATIONS |
                                           COMMENT
                                         }
                                         [ , ... ]

ALTER SERVICE [ IF EXISTS ] <name> SET [ TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]]
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
>     FROM SPECIFICATION_TEMPLATE_FILE = '<yaml_file_path>' -- for native app service.
>     | FROM @<stage> SPECIFICATION_TEMPLATE_FILE = '<yaml_file_path>' -- for non-native app service.
>     | FROM SPECIFICATION_TEMPLATE <specification_text>
>   }
>   USING ( <key> => <value> [ , <key> => <value> [ , ... ] ]  )
> ```

## Parameters

`name`
:   Specifies the identifier for the service to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`{ SUSPEND | RESUME }`
:   Specifies whether to suspend or resume the service.

    When you suspend a service, Snowflake shuts down and deletes the containers. If you later resume a suspended service,Snowflake
    recreates the containers. That is, Snowflake takes the image from your repository and starts the containers. Note that, Snowflake deploys the same image version; it is not a service update operation.

    When you invoke a suspended service using either a service function or invoking the public endpoint (ingress), Snowflake
    automatically resumes the service.

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

`RESTORE VOLUME volume_name INSTANCES comma_separated_instance_ids FROM SNAPSHOT snapshot_name`
:   Restores the snapshot `snapshot_name` on the existing block storage volume `volume_name` for the instances `comma_separated_instance_ids`.

    Snapshots can only be taken for block storage volumes (and not for local, memory, or stage volumes).

    Volume names are case-sensitive. Therefore, double quotes should always be used to match the corresponding name in the service specification.

`SET ...`
:   Sets one or more specified properties or parameters for the service:

    `MIN_INSTANCES = num`
    :   Specifies the minimum number of service instances.

    `MAX_INSTANCES = num`
    :   Specifies the maximum number of service instances.

    `LOG_LEVEL = 'log_level'`
    :   Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at
        the specified level (and at more severe levels) are ingested.
        Currently, LOG\_LEVEL is supported only for [platform events](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-monitoring-services-access-platform-events), Changing LOG\_LEVEL for [container logs](/developer-guide/snowpark-container-services/monitoring-services#label-snowpark-containers-working-with-services-local-logs) is not supported.

        > For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting the log level, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

    `AUTO_SUSPEND_SECS = num`
    :   Specifies the number of seconds of inactivity (service is idle) after which Snowflake automatically suspends the service. When AUTO\_SUSPEND\_SECS is 0 (default), Snowflake does not auto-suspend the service. You can configure this value to 300 seconds or more to enable auto-suspension. For more information, see [Suspending a service](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-suspend-service).

        [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

        Configuring the automatic suspension of a Snowpark Container Services service using the AUTO\_SUSPEND\_SECS property is a [preview feature](/release-notes/preview-features).

    `MIN_READY_INSTANCES = num`
    :   Specifies the minimum service instances that must be ready for Snowflake to consider the service ready to process requests. For more information, see [Scaling services](/developer-guide/snowpark-container-services/working-with-services#scaling-services).

    `QUERY_WAREHOUSE = warehouse_name`
    :   Warehouse to use if a service container connects to Snowflake to execute a query but does not explicitly specify a warehouse to use.

    `AUTO_RESUME = { TRUE | FALSE }`
    :   Specifies whether to automatically resume a service when user performs one of the following actions that depend on the service:

        - Executing a query is that uses a [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function).
        - Sending a request to the public endpoint exposed by the service ([ingress](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-ingress)).

        If AUTO\_RESUME is FALSE, you need to explicitly resume the service (using ALTER SERVICE … RESUME).

        Default: TRUE.

    `EXTERNAL_ACCESS_INTEGRATIONS = ( EAI_name [ , ... ] )`
    :   Specifies the names of the [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access) that allow your service to access external sites.
        Snowflake replaces all the existing EAIs with those specified in this parameter.
        The names in this list are case-sensitive. For more information, see [Configure service egress](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress).
        Note that this changes the allowed network access for all running instances of the service. You don’t need to explicitly suspend and resume the service.

    `COMMENT = 'string_literal'`
    :   Specifies a comment for the service.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more properties and/or parameters to unset for the service, which resets them to the defaults (see
    [CREATE SERVICE](/sql-reference/sql/create-service)):

    - `MIN_INSTANCES`
    - `MAX_INSTANCES`
    - `AUTO_SUSPEND_SECS`

      [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

      Configuring the automatic suspension of a Snowpark Container Services service using the AUTO\_SUSPEND\_SECS property is a [preview feature](/release-notes/preview-features).
    - `MIN_READY_INSTANCES`
    - `QUERY_WAREHOUSE`
    - `AUTO_RESUME`
    - `EXTERNAL_ACCESS_INTEGRATIONS`
    - `COMMENT`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Snapshot | To restore a snapshot, the role requires this privilege on the snapshot. |
| OWNERSHIP | Service | To alter the service and set/unset properties and tags, the role requires this privilege. |
| OPERATE | Service | To alter the service, except set/unset properties, the role requires this privilege. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Suspend a service.

Copy code

```
ALTER SERVICE echo_service SUSPEND;
```

Modify the MIN\_INSTANCES and MAX\_INSTANCES properties of an existing service.

Copy code

```
ALTER SERVICE echo_service SET MIN_INSTANCES=3 MAX_INSTANCES=5;
```

Restore a snapshot on an existing block volume associated with instances 0 and 2 of the `example_service` service.

Copy code

```
ALTER SERVICE example_service
  RESTORE VOLUME "myvolume"
  INSTANCES 0,2
  FROM SNAPSHOT my_snapshot;
```
