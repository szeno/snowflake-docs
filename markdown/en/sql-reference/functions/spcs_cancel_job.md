Categories:
:   [Table functions](/sql-reference/functions-table)

# <service\_name>!SPCS\_CANCEL\_JOB

Cancels a [Snowpark Container Services job](/developer-guide/snowpark-container-services/working-with-services); also referred to as job service. When you cancel a job, Snowflake stops the job from running and removes the resources allocated for running the job.

See also:
:   [Run a job service](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-creating-job), [Working with services](/developer-guide/snowpark-container-services/working-with-services)

## Syntax

Copy code

```
<service_name>!SPCS_CANCEL_JOB();
```

## Returns

Returns a string that indicates whether or not the job was canceled.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OPERATE | Service | To cancel the job service, you must use a role that was granted this privilege. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Cancel the `my_job` job.

Copy code

```
SELECT my_job!SPCS_CANCEL_JOB();
```
