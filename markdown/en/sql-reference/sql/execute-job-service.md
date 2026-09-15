# EXECUTE JOB SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Executes a Snowpark Container Services service as a job.

A service, created using [CREATE SERVICE](/sql-reference/sql/create-service), is long-running and you must explicitly stop it when it is no longer needed. On the other hand, a job, created using EXECUTE JOB SERVICE, is a service that terminates when your code exits, similar to a stored procedure. When all containers exit, the job is done.

By default, the job runs synchronously; the EXECUTE JOB SERVICE command finishes only after all containers exit.

Alternatively, you can run the job service asynchronously by specifying the optional `ASYNC` parameter. In this case, the command returns immediately while the job is running. You can use the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) command to poll for job completion and then call the [SYSTEM$WAIT\_FOR\_SERVICES](/sql-reference/functions/system_wait_for_services) function to wait for the job to complete.

After a job service completes, Snowflake automatically cleans up the resources allocated to the job service to help reduce costs. You can still access job metadata for up to 30 days by using the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) and [SHOW SERVICES](/sql-reference/sql/show-services) commands. After 30 days, Snowflake automatically deletes the job.

When the job is done, if no other jobs or services are running on that compute pool node, Snowflake might consider the node is idle and reclaim it. When that happens, SYSTEM$GET\_SERVICE\_LOGS will not return local container logs from the job containers. You might consider persisting the container logs to an event table. For more information, see [Publishing and accessing container logs](/developer-guide/snowpark-container-services/monitoring-services#label-snowpark-containers-working-with-services-local-logs).

Note that the command parameters must be specified in a specific order. For more information, see [Usage Notes](#usage-notes).

See also:
:   [SYSTEM$GET\_SERVICE\_STATUS — Deprecated](/sql-reference/functions/system_get_service_status) , [SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs)

## Syntax

Copy code

```
EXECUTE JOB SERVICE
  IN COMPUTE POOL <compute_pool_name>
  {
     fromSpecification
     | fromSpecificationTemplate
  }
  [ NAME = [<db>.<schema>.]<name> ]
  [ ASYNC = { TRUE | FALSE } ]
  [ REPLICAS = = <num> ]
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ COMMENT = '<string_literal>']
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <EAI_name> [ , ... ] ) ]
```

Where:

> Copy code
>
> ```
> fromSpecification ::=
>   {
>     FROM @<stage> SPECIFICATION_FILE = '<yaml_file_stage_path>'
>     | FROM SPECIFICATION <specification_text>
>   }
> ```
>
> Copy code
>
> ```
> fromSpecificationTemplate ::=
>   {
>     FROM @<stage> SPECIFICATION_TEMPLATE_FILE = '<yaml_file_stage_path>'
>     | FROM SPECIFICATION_TEMPLATE <specification_text>
>   }
>   USING ( <key> => <value> [ , <key> => <value> [ , ... ] ]  )
> ```

## Required parameters

`IN COMPUTE POOL compute_pool_name`
:   Specifies the name of the compute pool in your account on which to run the service.

`FROM stage`
:   Specifies the Snowflake internal stage where the specification file is stored; for example, `@tutorial_stage`.

`SPECIFICATION_FILE = 'yaml_file_stage_path'`
:   Specifies the path to the [service specification](/developer-guide/snowpark-container-services/specification-reference)
    file on the stage; for example, `'some-dir/echo_spec.yaml'`.

`SPECIFICATION_TEMPLATE_FILE = 'yaml_file_stage_path'`
:   Specifies the path to the [service specification](/developer-guide/snowpark-container-services/specification-reference)
    template file on the stage; for example, `'some-dir/echo_template_spec.yaml'`. When `SPECIFICATION_TEMPLATE_FILE` is specified, the `USING` parameter is required.

`FROM SPECIFICATION specification_text`
:   Specifies [service specification](/developer-guide/snowpark-container-services/specification-reference). You can use
    a [pair of dollar signs](/sql-reference/data-types-text#label-dollar-quoted-string-constants) (`$$`) to delimit the beginning and ending of the
    specification string.

`FROM SPECIFICATION_TEMPLATE specification_text`
:   Specifies [service specification](/developer-guide/snowpark-container-services/specification-reference). You can use a
    [pair of dollar signs](/sql-reference/data-types-text#label-dollar-quoted-string-constants) (`$$`) to delimit the beginning and ending of the
    specification string. When `SPECIFICATION_TEMPLATE` is specified, the `USING` parameter is required.

## Optional parameters

`NAME = [db.schema.]name`
:   The name (that is the identifier) for the service, that executes like a job; it must be unique for the schema in which the service
    is created.

    Quoted names for special characters or case-sensitive names are not supported. The same constraint also applies to database
    and schema names where you create a service. That is, database and schema names without quotes are valid when creating a
    service.

    Default: If not specified, Snowflake generates a name for the service in a format `JOB_<query_job_uuid>`.

`ASYNC = { TRUE | FALSE }`
:   Specifies whether to execute the job asynchronously.

    Default: FALSE

`REPLICAS = num`
:   Specifies the number of job replicas to run. For more information,
    see [Run multiple replicas of a job service (batch jobs)](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-creating-batch-jobs).

    Default: 1.

`QUERY_WAREHOUSE = warehouse_name`
:   Warehouse to use if a service container connects to Snowflake to execute a query but does not explicitly specify a warehouse
    to use. This parameter also supports object references in Native Apps. For more information, see [Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

    Default: none.

`EXTERNAL_ACCESS_INTEGRATIONS = ( EAI_name [ , ... ] )`
:   Specifies the names of the [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access)
    that allow your job to access external sites. The names in this list are case-sensitive. By default, application containers don’t have
    permission to access the internet. If you want to allow your job to access an external site, create an External Access Integration
    (EAI), and configure your job to use that integration. For more
    information, see [Configure service egress](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress).

`COMMENT = 'string_literal'`
:   Specifies a comment for the service.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`USING ( key => value [ , key => value [ , ... ] ] )`
:   Lets you provide values to parameterize specification template expansion.

    `USING` is required when using a specification template (`FROM SPECIFICATION_TEMPLATE_FILE` or `FROM SPECIFICATION_TEMPLATE`). The key-value pairs must form a comma-separated list.

    Where:

    - `key` is the name of the template variable. The template variable name can optionally be enclosed in double quotes
      (`"`).
    - `value` is the value to assign to the variable in the template. String values must be enclosed in `'` or
      `$$`. The value must either be alphanumeric or valid JSON.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SERVICE | Schema |  |
| USAGE | Compute pool |  |
| READ | Stage | This is the stage where the specification is stored. |
| READ | Image Repository | Repository of images referenced by the specification. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When calling EXECUTE JOB SERVICE, the parameters should be provided in this order: specify compute pool, followed by other properties, and finally the service specification (either provide specification file name on stage or inline specification).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Execute a job asynchronously

Execute a Snowpark Container Services job service asynchronously.

Copy code

```
EXECUTE JOB SERVICE
  IN COMPUTE POOL tutorial_compute_pool
  NAME = tutorial_db.data_schema.example_job
  ASYNC = TRUE
  FROM @tutorial_stage
  FROM SPECIFICATION $$
  <job specification>
  $$;
```

### Execute a job with block storage mounted

Execute a job service with block storage configured in the specification.

Copy code

```
EXECUTE JOB SERVICE
  IN COMPUTE POOL tutorial_compute_pool
  NAME=tutorial_job_service
  FROM SPECIFICATION $$
  spec:
    container:
    - name: main
      image: /tutorial_db/data_schema/tutorial_repository/my_job_image:latest
      volumeMounts:
        - name: block-vol1
          mountPath: /opt/block/path
    volumes:
    - name: block-vol1
      source: block
      size: 10Gi
      blockConfig:
        iops: 4000
        throughput: 200
  $$;
```

The command does not specify the optional `ASYNC` parameter. Therefore, Snowflake executes the command synchronously.

### Execute a batch job

Run 3 instances of a job service by specifying REPLICAS parameter.

Copy code

```
EXECUTE JOB SERVICE
  IN COMPUTE POOL my_pool
  NAME = tutorial_2_job_service
  REPLICAS = 3
  FROM SPECIFICATION $$
  spec:
    containers:
    - name: main
      image: my_repo/my_job_image:latest
$$;
```

Use [SHOW SERVICE INSTANCES IN SERVICE](/sql-reference/sql/show-service-instances-in-service) command to find the status of each job service replica.

Copy code

```
SHOW SERVICE INSTANCES IN SERVICE tutorial_2_job_service;
```

Example output:

```
+---------------+-------------+------------------------+----------------+-------------+-----------+------------------------------------------------------------------+----------------------+----------------------+--------------+
| database_name | schema_name | service_name           | service_status | instance_id | status    | spec_digest                                                      | creation_time        | start_time           | ip_address   |
|---------------+-------------+------------------------+----------------+-------------+-----------+------------------------------------------------------------------+----------------------+----------------------+--------------|
| TUTORIAL_DB   | DATA_SCHEMA | TUTORIAL_2_JOB_SERVICE | DONE           | 0           | SUCCEEDED | 80b42d8e1ec39dbaa7e2b9b6591e4b0cc11f74304703f56b50e1dfc10f421ac5 | 2025-08-07T00:44:49Z | 2025-08-07T00:44:49Z | 10.244.0.11  |
| TUTORIAL_DB   | DATA_SCHEMA | TUTORIAL_2_JOB_SERVICE | DONE           | 1           | SUCCEEDED | 80b42d8e1ec39dbaa7e2b9b6591e4b0cc11f74304703f56b50e1dfc10f421ac5 | 2025-08-07T00:44:49Z | 2025-08-07T00:44:57Z | 10.244.0.12  |
| TUTORIAL_DB   | DATA_SCHEMA | TUTORIAL_2_JOB_SERVICE | DONE           | 2           | SUCCEEDED | 80b42d8e1ec39dbaa7e2b9b6591e4b0cc11f74304703f56b50e1dfc10f421ac5 | 2025-08-07T00:44:49Z | 2025-08-07T00:44:49Z | 10.244.0.203 |
+---------------+-------------+------------------------+----------------+-------------+-----------+------------------------------------------------------------------+----------------------+----------------------+--------------+
```

In the output, the `instance_id` and `status` columns show the replica number and its status.
