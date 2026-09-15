# model\_name!PREDICT

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Generates a classification prediction from the previously trained model `model_name`.

## Syntax

Copy code

```
<model_name>!PREDICT(
    INPUT_DATA => <input_data>,
    [CONFIG_OBJECT => <config_object>]
)
```

## Arguments

*Required*

INPUT\_DATA
:   An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing key-value pairs that map feature names to their values. Use
    [wildcard expansion in an object literal](/sql-reference/data-types-semistructured#label-object-constant-wildcard) to automatically create key-value pairs from a table, as in:

    Copy code

    ```
    SELECT model_binary!PREDICT(INPUT_DATA => {*})
        as prediction from prediction_purchase_data;
    ```

    The feature names in the object must match the names and types specified at training time. Missing or extraneous features are ignored.

*Optional*

CONFIG\_OBJECT
:   An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) whose key-value pairs specify additional training options.

    | Key | Type | Default | Description |
    | --- | --- | --- | --- |
    | `on_error` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | `'ABORT'` | String (constant) that specifies the error handling method for the model inference task. Supported values are:   - `'ABORT'`: Abort the entire prediction operation if any row results in an error. - `'SKIP'`: Skip rows that result in an error. The error is shown instead of the results. |

    Expand

    Show lessSee more

## Output

> | Key | Type | Description |
> | --- | --- | --- |
> | `class` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | The predicted label with the highest probability. |
> | `probability` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing the probabilities of each predicted class. For each class, the key is the class name, and the value is the predicted probability of the class. |
>
> Expand
>
> Show lessSee more
>
> | Key | Type | Description |  |
> | --- | --- | --- | --- |
> | `class` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | The predicted label with the highest probability. |  |
> | `probability` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing the probabilities of each predicted class. For each class, the key is the class name, and the value is the predicted probability of the class. | An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing the probabilities of each predicted class. For each class, the key is the class name, and the value is the predicted probability of the class. |
> | `probability` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing the probabilities of each predicted class. For each class, the key is the class name, and the value is the predicted probability of the class. | An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing the probabilities of each predicted class. For each class, the key is the class name, and the value is the predicted probability of the class. |
> | LOGS | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Contains error or warning messages. |  |
>
> Expand
>
> Show lessSee more

## Examples

See [Examples](/user-guide/ml-functions/classification#label-cortex-classification-examples).
