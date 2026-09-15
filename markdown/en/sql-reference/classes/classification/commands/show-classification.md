# SHOW SNOWFLAKE.ML.CLASSIFICATION

Lists all classification models.

SHOW SNOWFLAKE.ML.CLASSIFICATION INSTANCES is an alias for SHOW SNOWFLAKE.ML.CLASSIFICATION.

See also:
:   [CREATE SNOWFLAKE.ML.CLASSIFICATION](/sql-reference/classes/classification/commands/create-classification)

## Syntax

Copy code

```
{
  SHOW SNOWFLAKE.ML.CLASSIFICATION           |
  SHOW SNOWFLAKE.ML.CLASSIFICATION INSTANCES
}
                                 [ LIKE <pattern> ]
                                 [ IN
                                     {
                                         ACCOUNT                  |

                                         DATABASE                 |
                                         DATABASE <database_name> |

                                         SCHEMA                   |
                                         SCHEMA <schema_name>     |
                                         <schema_name>
                                      }
                                  ]
```

## Usage notes

The order of results is not guaranteed.

## Output

The command output provides model properties and metadata in the following columns.

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the model was created. |
| `name` | Name of the model. |
| `database_name` | Database in which the model is stored. |
| `schema_name` | Schema in which the model is stored. |
| `current_version` | The version of the model. |
| `comment` | Comment for the model. |
| `owner` | The role that owns the model. |

Expand

Show lessSee more
