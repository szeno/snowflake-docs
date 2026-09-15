# DESCRIBE OPENFLOW DEPLOYMENT

See also:
:   [CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment), [ALTER OPENFLOW DEPLOYMENT](/sql-reference/sql/alter-openflow-deployment), [DROP OPENFLOW DEPLOYMENT](/sql-reference/sql/drop-openflow-deployment), [SHOW OPENFLOW DEPLOYMENTS](/sql-reference/sql/show-openflow-deployments)

Returns properties for a single deployment.

## Syntax

Copy code

```
DESCRIBE OPENFLOW DEPLOYMENT <name>
```

## Output

The command output provides deployment properties in the following columns. Output matches
`SHOW OPENFLOW DEPLOYMENTS` except `created_on` and `updated_on` are omitted.

| Column | Description |
| --- | --- |
| `name` | Deployment identifier. |
| `type` | `SNOWFLAKE` or `BYOC`. |
| `status` | Current lifecycle state. |
| `vpc_type` | BYOC VPC type. |
| `display_name` | UI display name. |
| `use_private_link` | Whether PrivateLink is enabled. |
| `use_user_auth_over_private_link` | Whether user authentication over PrivateLink is enabled. |
| `custom_ingress_hostname` | BYOC custom hostname. |
| `key` | Internal key. |
| `owner` | Role that owns the deployment. |
| `comment` | Comment for the deployment. |

Expand

Show lessSee more
