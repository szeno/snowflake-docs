Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# NETWORK\_RULE\_REFERENCES

Returns a row for each object with which the specified network rule is associated or returns a row for each network rule associated
with the specified container.

See also:

- [NETWORK\_RULE\_REFERENCES view](/sql-reference/account-usage/network_rule_references) (Account Usage View)
- [NETWORK\_RULE\_REFERENCES view](/sql-reference/organization-usage/network_rule_references) (Organization Usage View)

## Syntax

Copy code

```
NETWORK_RULE_REFERENCES(
  NETWORK_RULE_NAME => '<string>'
)

NETWORK_RULE_REFERENCES(
  CONTAINER_NAME => '<container_name>' ,
  CONTAINER_TYPE => { 'INTEGRATION' | 'NETWORK_POLICY' }
)
```

## Arguments

`NETWORK_RULE_NAME => 'string'`
:   Specifies the identifier for the [network rule](/sql-reference/sql/create-network-rule).

    - The entire network rule name must be enclosed in single quotes.
    - If the network rule name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes, such as `'"name"'`.

`CONTAINER_NAME => 'container_name'`
:   Specifies the name of the external access integration or network policy to which the network rule is associated.

    - The entire network rule name must be enclosed in single quotes.
    - If the object name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quote, such as `'"<name>"'`.

`CONTAINER_TYPE => { 'INTEGRATION' | 'NETWORK_POLICY' }`
:   Specifies the object type (domain) to which the network rule is associated.

## Output

The function returns the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `container_name` | VARCHAR | The name of the container to which the network policy is associated. |
| `container_type` | VARCHAR | One of the following: `NETWORK_POLICY` or `INTEGRATION`. |
| `network_rule_name` | VARCHAR | Name of the network rule. |
| `action_type` | VARCHAR | One of the following: `ALLOW` or `BLOCK`. |
| `database_name` | VARCHAR | Name of the database that contains the network rule. |
| `schema_name` | VARCHAR | Name of the schema that contains the network rule. |

Expand

Show lessSee more

## Usage notes

Use one syntax or the other. Do not mix arguments.

## Examples

Returns a row for each object to which the specified network rule is associated:

> Copy code
>
> ```
> USE ROLE network_admin;
> USE DATABASE securitydb;
> SELECT *
>   FROM TABLE(
>     securitydb.INFORMATION_SCHEMA.NETWORK_RULE_REFERENCES(
>       NETWORK_RULE_NAME => 'securitydb.myrules.cloud_rule'
>     )
>   );
> ```

Returns a row for each network rule associated to the specified container:

> Copy code
>
> ```
> USE ROLE network_admin;
> USE DATABASE securitydb;
> SELECT *
>   FROM TABLE(
>     securitydb.INFORMATION_SCHEMA.NETWORK_RULE_REFERENCES(
>       CONTAINER_NAME => 'my_network_policy' ,
>       CONTAINER_TYPE => 'NETWORK_POLICY'
>     )
>   );
> ```
