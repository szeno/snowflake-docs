# DROP SNOWFLAKE.ML.FORECAST

Removes the specified model from the current or specified schema. Dropped models cannot be recovered; they must be recreated.

## Syntax

Copy code

```
DROP SNOWFLAKE.ML.FORECAST [ IF EXISTS ] <model_name>;
```

## Parameters

`model_name`
:   Specifies the identifier for the model to drop. If the identifier contains spaces, special characters, or mixed-case
    characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also
    case-sensitive.

    If the model identifier is not fully qualified (in the form of `db_name.schema_name.name` or
    `schema_name.name`)), the command looks for the model in the current schema for the session.

## Examples

See [Examples](/user-guide/ml-functions/forecasting#label-analysis-forecasting-examples).
