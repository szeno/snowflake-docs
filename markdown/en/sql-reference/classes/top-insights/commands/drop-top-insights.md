# DROP SNOWFLAKE.ML.TOP\_INSIGHTS

Removes the specified Top Insights instance from the current or specified schema. Dropped instances cannot be recovered.

## Syntax

Copy code

```
DROP SNOWFLAKE.ML.TOP_INSIGHTS [ IF EXISTS ] <instance_name>;
```

## Parameters

`instance_name`
:   Specifies the identifier for the instance to drop. If the identifier contains spaces, special characters, or mixed-case
    characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also
    case-sensitive.

    If the instance identifier is not fully qualified (in the form of `db_name.schema_name.name` or
    `schema_name.name`)), the command looks for the instance in the current schema for the session.
