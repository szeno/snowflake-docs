# SHOW ENDPOINTS

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Lists the endpoints in a
[Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services) (or a job service). Use the command to list endpoints in a service or service running as a job.

See also:
:   [CREATE SERVICE](/sql-reference/sql/create-service) , [ALTER SERVICE](/sql-reference/sql/alter-service), [DROP SERVICE](/sql-reference/sql/drop-service) , [SHOW SERVICES](/sql-reference/sql/show-services)

## Syntax

Copy code

```
SHOW ENDPOINTS IN SERVICE <name>
```

## Parameters

`name`
:   Specifies the identifier for the service whose endpoints to list.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command output provides service properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | User-friendly endpoint name that represents the corresponding port. |
| `port` | The network port the service is listening on. NULL, when `portRange` is specified. |
| `port_range` | The network port range the service is listening on. NULL, when `port` is specified. |
| `protocol` | Supported network protocol (TCP, HTTP, or HTTPS). The default is HTTP. Public endpoints and service functions (see [Using a service](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating)) require HTTP or HTTPS. |
| `is_public` | True, if the endpoint is public, accessible from internet. |
| `ingress_url` | Endpoint URL accessible from the internet. |
| `privatelink_ingress_url` | Endpoint URL accessible via Private Connectivity. The column is returned only for [Business Critical](/user-guide/intro-editions) accounts. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Service |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

The following example lists endpoints exposed by `echo_service` service:

Copy code

```
SHOW ENDPOINTS IN SERVICE echo_service;
```

```
+--------------+------+------------+----------+-----------+------------------------------------------------------------------------------+-----------------------------------------------+
| name         | port | port_range | protocol | is_public | ingress_url                                                                  | privatelink_ingress_url                       |
|--------------+------+------------+----------+-----------+------------------------------------------------------------------------------|-----------------------------------------------*
| echoendpoint | 8080 |            | HTTP     | true      | d7qoajz-orgname-acctname.pp-snowflakecomputing.app                           | d7qoajz.spcs.pdxaac.privatelink.snowflake.app |
+--------------+------+------------+----------+-----------+------------------------------------------------------------------------------+-----------------------------------------------*
```
