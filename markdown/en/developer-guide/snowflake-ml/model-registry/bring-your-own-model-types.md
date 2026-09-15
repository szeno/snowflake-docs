# Bring your own model types via serialized files

The model registry supports logging [built-in model types](/developer-guide/snowflake-ml/model-registry/built-in-models/overview) directly in the registry.
We also provide a method of logging other model types with `snowflake.ml.model.custom_model.CustomModel`. Serializable models trained using external tools or obtained from open source repositories can be used with *CustomModel*.

This guide explains how to:

- Create a custom model.
- Create model context with files and model objects.
- Include additional code with your model using `code_paths`.
- Log the custom model to the Snowflake Model Registry.
- Deploy the model for inference.

Note

[This quickstart](https://quickstarts.snowflake.com/guide/deploying_custom_models_to_snowflake_model_registry/) provides an example of logging a custom PyCaret model.

## Defining model context by keyword arguments

The `snowflake.ml.model.custom_model.ModelContext` can be instantiated with user-defined keyword arguments. The values can either be string file paths or instances of [supported model types](/developer-guide/snowflake-ml/model-registry/built-in-models/overview). The files and serialized models will be packaged with the model for use in the model inference logic.

### Using in-memory model objects

When working with [built-in model types](/developer-guide/snowflake-ml/model-registry/built-in-models/overview), the recommended approach is to pass in-memory model objects directly to the `ModelContext`. This allows Snowflake ML to handle serialization automatically.

Copy code

```
import pandas as pd
from snowflake.ml.model import custom_model

# Initialize ModelContext with an in-memory model object
# my_model can be any supported model type (e.g., sklearn, xgboost, lightgbm, and others)
model_context = custom_model.ModelContext(
    my_model=my_model,
)

# Define a custom model class that utilizes the context
class ExampleBringYourOwnModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)

    @custom_model.inference_api
    def predict(self, input: pd.DataFrame) -> pd.DataFrame:
        # Use the model with key 'my_model' from the context to make predictions
        model_output = self.context['my_model'].predict(input)
        return pd.DataFrame({'output': model_output})

# Instantiate the custom model with the model context. This instance can be logged in the model registry.
my_model = ExampleBringYourOwnModel(model_context)
```

Note

In your custom model class, always access model objects through the model context. For example, use `self.model = self.context['my_model']`
instead of directly assigning `self.model = model` (where `model` is an in-memory model object). Accessing the model
directly captures a second copy of the model in a closure, which results in significantly larger model files during serialization.

### Using serialized files

For models or data that are stored in serialized files like Python pickles or JSON, you can provide file paths to your `ModelContext`. Files can be serialized models, configuration files, or files containing parameters. This is useful when working with pre-trained models saved to disk or configuration data.

Copy code

```
import pickle
import pandas as pd
from snowflake.ml.model import custom_model

# Initialize ModelContext with a file path
# my_file_path is a local pickle file path
model_context = custom_model.ModelContext(
    my_file_path='/path/to/file.pkl',
)

# Define a custom model class that loads the pickled object
class ExampleBringYourOwnModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)

        # Use 'my_file_path' key from the context to load the pickled object
        with open(self.context['my_file_path'], 'rb') as f:
            self.obj = pickle.load(f)

    @custom_model.inference_api
    def predict(self, input: pd.DataFrame) -> pd.DataFrame:
        # Use the loaded object to make predictions
        model_output = self.obj.predict(input)
        return pd.DataFrame({'output': model_output})

# Instantiate the custom model with the model context. This instance can be logged in the model registry.
my_model = ExampleBringYourOwnModel(model_context)
```

Important

When you combine a supported model type (such as XGBoost) with unsupported models or data, you don’t need to
serialize the supported model yourself. Set the supported model object directly in the context (e.g., `base_model = my_xgb_model`) and it is serialized automatically.

Important

Methods decorated with `@custom_model.inference_api` should always be written to work on multi-row dataframe.
Don’t assume that the input DataFrame will always contain a single row. Because of server-side batching,
specifically in real-time inference, even single-record requests from multiple sources can be batched together into one DataFrame.

## Defining inference parameters

Custom model inference methods can accept optional parameters that control inference behavior, such as a temperature
setting or maximum number of tokens. Define parameters as keyword-only arguments (after `*`) on the
`@inference_api` method, with type annotations and default values.

Copy code

```
import pandas as pd
from snowflake.ml.model import custom_model

class TextGenerationModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)

    @custom_model.inference_api
    def predict(
        self,
        input: pd.DataFrame,
        *,
        temperature: float = 0.7,
        max_tokens: int = 256,
    ) -> pd.DataFrame:
        # Use temperature and max_tokens to control generation behavior
        output = self.context['my_model'].generate(
            input["input_text"],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return pd.DataFrame({"output_text": output})
```

When this model is logged, the parameters are automatically included in the model signature. Callers can override
them at inference time, or omit them to use the defaults. For more information, see
[Specifying model signatures](/developer-guide/snowflake-ml/model-registry/model-signature).

The following requirements apply to inference parameters:

- They must be keyword-only (defined after `*` in the method signature).
- They must have a type annotation. Supported types are `int`, `float`, `str`, `bool`, `bytes`,
  `datetime.datetime`, and `list` with a supported element type (for example, `list[str]`,
  `list[list[int]]`).
- They must have a default value.

## Testing and logging a custom model

You can test a custom model by running it locally.

Copy code

```
my_model = ExampleBringYourOwnModel(model_context)
output_df = my_model.predict(input_df)
```

When the model works as intended, log it to the Snowflake Model Registry. As shown in the next code
example, provide `conda_dependencies` (or `pip_requirements`) to specify the libraries that the model class needs.
Provide `sample_input_data` (a pandas or Snowpark DataFrame) to infer the input signature for the model. Alternatively,
provide a [model signature](/developer-guide/snowflake-ml/model-registry/model-signature).

Copy code

```
reg = Registry(session=sp_session, database_name="ML", schema_name="REGISTRY")
mv = reg.log_model(my_model,
            model_name="my_custom_model",
            version_name="v1",
            conda_dependencies=["scikit-learn"],
            comment="My Custom ML Model",
            sample_input_data=train_features)
output_df = mv.run(input_df)
```

## Including additional code with code\_paths

Use the `code_paths` parameter in [Registry.log\_model](https://docs.snowflake.com/developer-guide/snowpark-ml/reference/latest/api/registry/snowflake.ml.registry.Registry#snowflake.ml.registry.Registry.log_model) to
package Python code, such as helper modules, utilities, and configuration files with your model. You can import this code just as you would locally.

You can either provide string paths to copy files or directories, or :class:`~snowflake.ml.model.CodePath` objects. The objects provide more control over which subdirectories or files are included, and the import paths that will be used by the model.

### Using string paths

Pass a list of string paths to include files or directories. The last component of each path becomes the
importable module name.

Copy code

```
mv = reg.log_model(
    my_model,
    model_name="my_model",
    version_name="v1",
    code_paths=["src/mymodule"],  # import with: import mymodule
)
```

### Using CodePath with filter

Use the :class:`~snowflake.ml.model.CodePath` class when you want to package only part of a directory tree
or control the import paths used by your model.

Copy code

```
from snowflake.ml.model import CodePath
```

A `CodePath` has two parameters:

- `root`: A directory or file path.
- `filter` (optional): A relative path under `root` that selects a subdirectory or file.

When `filter` is provided, the source is `root/filter`, and the `filter` value determines the import path.
For example, `filter="utils"` allows you to `import utils`, and `filter="pkg/subpkg"` allows you to
`import pkg.subpkg`.

**Example:** Given this project structure:

```
my_project/src/
├── utils/
│   └── preprocessing.py
├── models/
│   └── classifier.py
└── tests/          # Not needed for inference
```

To package only `utils/` and `models/`, excluding `tests/`:

Copy code

```
mv = reg.log_model(
    my_model,
    model_name="my_model",
    version_name="v1",
    code_paths=[
        CodePath("my_project/src/", filter="utils/"),
        CodePath("my_project/src/", filter="models/"),
    ],
)
```

You can also filter a single file:

Copy code

```
code_paths=[
    CodePath("my_project/src/", filter="utils/preprocessing.py"),
]
# Import with: import utils.preprocessing
```

## Example: Logging a PyCaret model

The following example uses PyCaret to log a custom model type. PyCaret is a low-code, high-efficiency third-party package that Snowflake doesn’t support natively.
You can bring your own model types using similar methods.

### Step 1: Define the model context

Before you log your model, define the model context. The model context refers to your own custom model type.
The following example specifies the path to the serialized (pickled) model using the context’s `model_file` attribute. You can choose any
name for the attribute as long as the name is not used for anything else.

Copy code

```
pycaret_model_context = custom_model.ModelContext(
  model_file = 'pycaret_best_model.pkl',
)
```

### Step 2: Create a custom model class

Define a custom model class to log a model type without native support. In this example, a `PyCaretModel` class,
derived from `CustomModel`, is defined so the model can be logged in the registry.

Copy code

```
from pycaret.classification import load_model, predict_model

class PyCaretModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)
        model_dir = self.context["model_file"][:-4]  # Remove '.pkl' suffix
        self.model = load_model(model_dir, verbose=False)
        self.model.memory = '/tmp/'  # Update memory directory

    @custom_model.inference_api
    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        model_output = predict_model(self.model, data=X)
        return pd.DataFrame({
            "prediction_label": model_output['prediction_label'],
            "prediction_score": model_output['prediction_score']
        })
```

Note

As shown, set the model’s memory directory to `/tmp/`. Snowflake’s warehouse nodes have restricted directory
access. `/tmp` is always writeable and is a safe choice when the model needs a place to write files. This might
not be necessary for other types of models.

### Step 3: Test the custom model

Test the PyCaret model locally using code like the following.

Copy code

```
test_data = [
    [1, 237, 1, 1.75, 1.99, 0.00, 0.00, 0, 0, 0.5, 1.99, 1.75, 0.24, 'No', 0.0, 0.0, 0.24, 1],
    # Additional test rows...
]
col_names = ['Id', 'WeekofPurchase', 'StoreID', 'PriceCH', 'PriceMM', 'DiscCH', 'DiscMM',
            'SpecialCH', 'SpecialMM', 'LoyalCH', 'SalePriceMM', 'SalePriceCH',
            'PriceDiff', 'Store7', 'PctDiscMM', 'PctDiscCH', 'ListPriceDiff', 'STORE']

test_df = pd.DataFrame(test_data, columns=col_names)

my_pycaret_model = PyCaretModel(pycaret_model_context)
output_df = my_pycaret_model.predict(test_df)
```

### Step 4: Define a model signature

In this example, use the sample data to infer a [model signature](/developer-guide/snowflake-ml/model-registry/model-signature) for input validation:

Copy code

```
predict_signature = model_signature.infer_signature(input_data=test_df, output_data=output_df)
```

### Step 5: Log the model

The following code logs (registers) the model in the Snowflake Model Registry.

Copy code

```
snowml_registry = Registry(session)

custom_mv = snowml_registry.log_model(
    my_pycaret_model,
    model_name="my_pycaret_best_model",
    version_name="version_1",
    conda_dependencies=["pycaret==3.0.2", "scipy==1.11.4", "joblib==1.2.0"],
    options={"relax_version": False},
    signatures={"predict": predict_signature},
    comment = 'My PyCaret classification experiment using the CustomModel API'
)
```

### Step 6: Verify the model in the registry

To verify that the model is available in the Model Registry, use `show_models` function.

Copy code

```
snowml_registry.show_models()
```

### Step 7: Make predictions with the registered model

Use the `run` function to call the model for prediction.

Copy code

```
snowpark_df = session.create_dataframe(test_data, schema=col_nms)

custom_mv.run(snowpark_df).show()
```

## Next Steps

After deploying a PyCaret model by way of the Snowflake Model Registry, you can view the model in Snowsight.
In the navigation menu, select **AI & ML** » **Models**. If you do not see it there, make sure you are using the ACCOUNTADMIN role or the
role you used to log the model.

To use the model from SQL, use SQL like the following:

Copy code

```
SELECT
    my_pycaret_model!predict(*) AS predict_dict,
    predict_dict['prediction_label']::text AS prediction_label,
    predict_dict['prediction_score']::double AS prediction_score
from pycaret_input_data;
```
