# ALTER SNOWFLAKE.ML.CLASSIFICATION

You can change the name, description, and tags of a classification model object using forms of the ALTER command. Models
themselves are immutable and cannot be updated in place. To update a model, drop the existing model and train a new one.

See also:
:   [CREATE SNOWFLAKE.ML.CLASSIFICATION](/sql-reference/classes/classification/commands/create-classification)

## Syntax

Rename a model:

Copy code

```
ALTER SNOWFLAKE.ML.CLASSIFICATION [ IF EXISTS ] <name>
    RENAME TO '<new_model_name>';
```

Set or change a [tag](/user-guide/object-tagging/introduction) value on a model:

Copy code

```
ALTER SNOWFLAKE.ML.CLASSIFICATION  [ IF EXISTS ] <name>
    SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ];
```

Set or change a model’s comment:

Copy code

```
ALTER SNOWFLAKE.ML.CLASSIFICATION [ IF EXISTS ] <name>
    SET COMMENT = '<string_literal>';
```

Remove a [tag](/user-guide/object-tagging/introduction) from a model:

Copy code

```
ALTER SNOWFLAKE.ML.CLASSIFICATION [ IF EXISTS ] <name>
    UNSET TAG <tag_name> [ , <tag_name> ... ];
```

Remove a model’s comment:

Copy code

```
ALTER SNOWFLAKE.ML.CLASSIFICATION [ IF EXISTS ] <name>
    UNSET COMMENT;
```
