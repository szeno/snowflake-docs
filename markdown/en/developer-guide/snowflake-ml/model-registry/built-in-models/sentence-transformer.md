# Sentence Transformer

The Snowflake Model Registry supports models that use Sentence Transformers (`sentence_transformers.SentenceTransformer`).
For more information, see the [Sentence Transformers documentation](https://sbert.net/).

For the registry to know the signatures of the target methods, you must specify either sample input data or the signatures that define the input and output schema for the model’s methods.

For sample input data, specify a Snowpark DataFrame as the value for the `sample_input_data` parameter. For example you can specify a value such as `sample_input = pd.DataFrame(["This is a sample sentence."], columns=["TEXT"])`.

If you’re using the signatures parameter, specify a dictionary as the value for the `signatures` parameter. The dictionary defines the input and output methods for the model. For example, the following code defines the input and output schema for the model’s `encode` method:

Copy code

```
from snowflake.ml.model.model_signature import ModelSignature, FeatureSpec, DataType

  signatures = {
      "encode": ModelSignature(
          inputs=[FeatureSpec(dtype=DataType.STRING, name='TEXT')],
          outputs=[FeatureSpec(dtype=DataType.FLOAT, name='EMBEDDINGS', shape=(-1,))]
      )
  }
```

When you call `log_model`, you can use the following additional options in the `options` dictionary:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. Sentence Transformer models have the following target method by default, assuming the method exists: `encode`. |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with a GPU; defaults to 11.8. If manually set to `None`, the model cannot be deployed to a platform having a GPU. |

Expand

Show lessSee more

The following example:

- Loads a pre-trained Sentence Transformer model.
- Logs it to the Snowflake ML Model Registry
- Uses the logged model for inference.

Note

In the example, `reg` is an instance of `snowflake.ml.registry.Registry`. For information on
creating a registry object, see [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).

Copy code

```
from sentence_transformers import SentenceTransformer
import pandas as pd

# 1. Initialize the model
# This example uses the 'all-MiniLM-L6-v2' model, which is a popular
# and efficient model for generating sentence embeddings.
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Prepare sample input data
# Sentence Transformers expect a single column of text data for the 'encode' method.
sentences = ["This is an example sentence", "Each sentence is converted into a vector"]
sample_input = pd.DataFrame(sentences, columns=["TEXT"])

# 3. Log the model
# Provide the model object, a name, and a version.
# Including sample_input_data allows the registry to infer the input/output signatures.
model_ref = reg.log_model(
    model=model,
    model_name="my_sentence_transformer",
    version_name="v1",
    sample_input_data=sample_input,
)

# 4. Use the model for inference
# The 'run' method executes the default 'encode' function on the input data.
result_df = model_ref.run(sample_input, function_name="encode")

# The result is a DataFrame where the output column (usually named 'outputs')
# contains the embeddings as arrays of floats.
print(result_df)
```
