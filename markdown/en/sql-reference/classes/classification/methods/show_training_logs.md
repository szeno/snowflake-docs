# <model\_name>!SHOW\_TRAINING\_LOGS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the logs generated during training, if available.

## Syntax

Copy code

```
<model_name>!SHOW_TRAINING_LOGS();
```

## Output

| Column | Type | Description |
| --- | --- | --- |
| `colname` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The column name that logs are reported for. |
| `logs` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Contains error or warning messages. |

Expand

Show lessSee more
