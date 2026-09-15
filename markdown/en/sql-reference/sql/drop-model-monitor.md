# DROP MODEL MONITOR

Removes the specified model monitor from the current or specified schema. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors. Dropped monitors cannot be recovered; they must be recreated.

See also:
:   [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor),
    [ALTER MODEL MONITOR](/sql-reference/sql/alter-model-monitor),
    [SHOW MODEL MONITORS](/sql-reference/sql/show-model-monitors),
    [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor)

## Syntax

Copy code

```
DROP MODEL MONITOR [ IF EXISTS ] <monitor_name>;
```

## Parameters

`monitor_name`
:   Specifies the identifier for the model monitor to drop. If the identifier contains spaces, special characters, or
    mixed-case characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are
    also case-sensitive.

    If the model identifier is not fully qualified (in the form of `db_name.schema_name.monitor_name` or
    `schema_name.monitor_name`)), the command looks for the model in the current schema for the session.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Model monitor | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.
