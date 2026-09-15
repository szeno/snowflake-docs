# Specifying model signatures

To ensure a consistent experience no matter where a model is run, the Snowflake Model Registry needs to know the input
and output schema of the model’s inference methods: that is, the name and type of all columns in the input or output
DataFrame. This allows these columns to be mapped between Python and SQL data types when necessary. This schema is
referred to as a *signature* by analogy to the arguments of a function and their types. Signatures can also include
optional *parameters* that control inference behavior, such as a temperature setting.

For certain ML frameworks, the model registry can infer these schemas, either from data structures in the model itself
or from sample input data. However, models often accept or return objects that lack this information, such as NumPy
arrays. In these cases, Snowpark ML infers the input feature names as `input_feature_1`, `input_feature_2`, and so
on. Similarly, output features are named `output_feature_1`, `output_feature_2`, and so on.

To use more meaningful names in your custom models, you can use one of the following methods:

- Update `sample_input_data` with column names, usually by converting the dataset to a pandas or
  [Snowpark DataFrame](/developer-guide/snowpark/python/working-with-dataframes).
- Explicitly pass signatures to `log_model`. When a model does not produce names in its output, explicit signatures
  might be the only option.

## Inferring a signature

Like the model registry itself, you can generate signatures automatically. Use
`snowflake.ml.model.model_signature.infer_signature` to infer a signature based on provided sample input, output, and
column names, and then apply that signature to the appropriate methods when logging the model, as in the following example:

Copy code

```
import pandas as pd
from sklearn import svm, datasets

from snowflake.ml.model import model_signature

digits = datasets.load_digits()
target_digit = 6

def one_vs_all(dataset, digit):
    return [x == digit for x in dataset]

train_features = digits.data[:10]
train_labels = one_vs_all(digits.target[:10], target_digit)
clf = svm.SVC(gamma=0.001, C=10.0, probability=True)
clf.fit(train_features, train_labels)

sig = model_signature.infer_signature(
    train_features,
    train_labels,
    input_feature_names=['column1', 'column2', ...],
    output_feature_names=['is_target_digit'])

# Supply a signature for every function the model exposes, in this case only `predict`.
mv = reg.log_model(
    clf,
    model_name='my_model',
    version_name='v1',
    signatures={"predict": sig}
)
```

This example applies the signature to only one method, but you can infer a signature for each method your model exposes.
You can use the same signature object (`sig` in the example) for all methods that have the same signature.

Note

For Snowpark DataFrames, `infer_signature` must run the DataFrame’s query to obtain the data from which the
signature is inferred. This can incur significant cost depending on the size of the dataset. Most training datasets
are large enough to make this a consideration.

To avoid such large queries, `infer_signature` considers only the first hundred rows of the data by adding LIMIT
100 to the query. However, if these rows are not representative of the data, the inferred signature might not be
accurate. This commonly occurs when the dataset contains many NULL values and a column in the dataset has only NULL
values in the first hundred rows. In this case, the inferred signature incorrectly omits that column. Provide the
signature explicitly, as shown in the next section, to avoid this issue.

## Constructing a signature

You can also manually construct a signature by using `snowflake.ml.model.model_signature.ModelSignature`. Both scalar and
tensor types (including ragged tensors) are supported.

Example:

Copy code

```
from snowflake.ml.model.model_signature import ModelSignature, FeatureSpec, DataType

sig = ModelSignature(
    inputs=[
        FeatureSpec(dtype=DataType.DOUBLE, name=f_0),
        FeatureSpec(dtype=DataType.INT64, name=sparse_0_fixed_len, shape=(5, 5)),
        FeatureSpec(dtype=DataType.INT64, name=sparse_1_variable_len, shape=(-1,)),
    ],
    outputs=[
        FeatureSpec(dtype=DataType.FLOAT, name=output),
    ]
)
```

Then pass the signature object, `sig`, to `log_model` with the `signatures` argument as in the example above
for the methods to which it applies.

## Specifying parameters with ParamSpec

In addition to input and output features, model signatures can include *parameters*. Parameters define optional
configuration values that you can pass to model inference methods when you make an inference request.
Unlike input features, which specify the data being processed, parameters control inference behavior, such as the number of results to return or a temperature setting.

Use `ParamSpec` from [snowflake.ml.model.model\_signature.ModelSignature](https://docs.snowflake.com/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.ml.model.model_signature.ModelSignature) to define a parameter.

Each `ParamSpec` requires a name,
a data type, and a default value. The default value is used when the parameter is not explicitly provided at inference
time.

### Constructing a signature with parameters

The following example creates a model signature that includes both input/output features and parameters:

Copy code

```
from snowflake.ml.model.model_signature import ModelSignature, FeatureSpec, ParamSpec, DataType

sig = ModelSignature(
    inputs=[
        FeatureSpec(dtype=DataType.STRING, name="input_text"),
    ],
    outputs=[
        FeatureSpec(dtype=DataType.STRING, name="output_text"),
    ],
    params=[
        ParamSpec(name="temperature", dtype=DataType.DOUBLE, default_value=0.7),
        ParamSpec(name="max_tokens", dtype=DataType.INT32, default_value=256),
    ]
)

mv = reg.log_model(
    my_model,
    model_name='my_model',
    version_name='v1',
    signatures={"predict": sig}
)
```

You can also include parameters when inferring a signature with `infer_signature`:

Copy code

```
from snowflake.ml.model.model_signature import ParamSpec, DataType
from snowflake.ml.model import model_signature

params = [
    ParamSpec(name="top_k", dtype=DataType.INT32, default_value=10),
    ParamSpec(name="threshold", dtype=DataType.DOUBLE, default_value=0.5),
]

sig = model_signature.infer_signature(
    input_data,
    output_data,
    params=params
)
```

Note

Parameter names must be unique within the signature and cannot share names with input features. If a parameter name
conflicts with an input feature name, a `ValueError` is raised.

For a full list of `ParamSpec` arguments, see the
[API reference](https://docs.snowflake.com/developer-guide/snowpark-ml/reference/latest/model).

For details on passing parameter values at inference time, see
[Passing parameters during inference](/developer-guide/snowflake-ml/inference/native-batch-inference-sql#label-inference-passing-params-python) and
[Passing parameters in SQL](/developer-guide/snowflake-ml/inference/native-batch-inference-sql#label-inference-passing-params-sql).

## Data type mappings

This section describes the equivalence of types in the Snowflake Model Registry for supported type systems.

### Column data types

The following table shows the equivalence of model signature type, pandas DataFrames (NumPy) type, and Snowpark
Python type.

| Model signature type | pandas DataFrame (NumPy) type | Snowpark Python type |
| --- | --- | --- |
| INT8 | `np.int8` | `ByteType` |
| INT16 | `np.int16` | `ShortType` |
| INT32 | `np.int32` | `IntegerType` |
| INT64 | `np.int64` | `LongType` |
| FLOAT | `np.float32` | `FloatType` |
| DOUBLE | `np.float64` | `DoubleType` |
| UINT8 | `np.uint8` | `ByteType` |
| UINT16 | `np.uint16` | `ShortType` |
| UINT32 | `np.uint32` | `IntegerType` |
| UINT64 | `np.uint64` | `LongType` |
| BOOL | `np.bool_` | `BooleanType` |
| STRING | `np.str_` | `StringType` |
| BYTES | `np.bytes_` | `BinaryType` |
| TIMESTAMP\_NTZ | `np.datetime64` | `TimestampType` |

Expand

Show lessSee more

The representation of tensor features where the shape is specified uses `np.object_`.

### Missing values

If `sample_input_data` is used to infer model signature, it generally should not contain any NULL values.
The model registry attempts to infer signatures from the data provided, but it may not always be able to so
completely. It is good practice to prevent NULLs from being included in the sample data as early as possible,
for example at data input time, whenever possible.

### Conversion from NumPy

If the NumPy data type can be safely cast to a NumPy type shown in [Column data types](#label-model-registry-column-data-types), it is
inferred as the corresponding data type.

### Conversion from PyTorch

| PyTorch type | Model signature type |
| --- | --- |
| `torch.uint8` | UINT8 |
| `torch.int8` | INT8 |
| `torch.int16` | INT16 |
| `torch.int32` | INT32 |
| `torch.int64` | INT64 |
| `torch.float32` | FLOAT |
| `torch.float64` | DOUBLE |
| `torch.bool` | BOOL |

Expand

Show lessSee more

### Conversion from Snowpark

In addition to the mappings shown in [Column data types](#label-model-registry-column-data-types), the following conversions apply:

- `DecimalType` with scale of 0 maps to INT64.
- `DecimalType` with scale greater than 0 maps to DOUBLE.
