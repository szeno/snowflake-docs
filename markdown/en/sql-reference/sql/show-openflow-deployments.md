# SHOW OPENFLOW DEPLOYMENTS

See also:
:   [CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment), [ALTER OPENFLOW DEPLOYMENT](/sql-reference/sql/alter-openflow-deployment), [DROP OPENFLOW DEPLOYMENT](/sql-reference/sql/drop-openflow-deployment), [DESCRIBE OPENFLOW DEPLOYMENT](/sql-reference/sql/desc-openflow-deployment)

Lists gen 2 deployments visible to the current user.

## Syntax

Copy code

```
SHOW OPENFLOW DEPLOYMENTS
  [ LIKE '<pattern>' ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

The command output provides deployment properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Deployment identifier. |
| `type` | `SNOWFLAKE` or `BYOC`. |
| `status` | `CREATING`, `ACTIVE`, `TERMINATED`, and other lifecycle states. |
| `vpc_type` | BYOC VPC type. |
| `display_name` | UI display name. |
| `use_private_link` | Whether PrivateLink is enabled. |
| `use_user_auth_over_private_link` | Whether user authentication over PrivateLink is enabled. |
| `custom_ingress_hostname` | BYOC custom hostname. |
| `key` | Internal key. |
| `owner` | Role that owns the deployment. |
| `comment` | Comment for the deployment. |
| `created_on` | Date and time when the deployment was created. |
| `updated_on` | Date and time when the deployment was last updated. |

Expand

Show lessSee more

## Usage notes

- Results are scoped to the privileges available in your current session. If you don’t see an
  expected deployment, verify that the role you’re using (or one of your active secondary roles)
  has been granted at least one privilege on the object. To check whether any of your granted
  roles can see it, run `USE SECONDARY ROLES ALL` and retry the query.
