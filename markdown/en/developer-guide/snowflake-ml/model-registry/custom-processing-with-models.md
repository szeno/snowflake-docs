# Pre-processing and post-processing with models

This topic explains how to create models, log them to the Snowflake Model Registry, and deploy them, using a number of
model types and scenarios as examples. These include:

- In-memory scikit-learn models and pipelines.
- Your own custom models.
- More than one model.

## In-memory scikit-learn models and pipelines

Snowflake ML allows seamless integration of in-memory `scikit-learn` models into the Model Registry by using keyword
arguments with `ModelContext` class. Below is an example of passing an in-memory `scikit-learn` model as a keyword
argument to model context and calling it in a custom model class.

Copy code

```
from sklearn import datasets, svm
import pandas as pd
from snowflake.ml.model import custom_model

# Step 1: Import the Iris dataset
iris_X, iris_y = datasets.load_iris(return_X_y=True)

# Step 2: Initialize a scikit-learn LinearSVC model and train it
svc = svm.LinearSVC()
svc.fit(iris_X, iris_y)

# Step 3: Initialize ModelContext with keyword arguments
mc = custom_model.ModelContext(
    my_model=svc,
)

# Step 4: Define a custom model class to utilize the context
class ExampleSklearnModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)

    @custom_model.inference_api
    def predict(self, input: pd.DataFrame) -> pd.DataFrame:
        # Use the model from the context for predictions
        model_output = self.context['my_model'].predict(input)
        # Return the predictions in a DataFrame
        return pd.DataFrame({'output': model_output})
```

## Using `scikit-learn` pipelines with Snowflake ML

Below is an example showing how to use scikit-learn pipelines within Snowflake ML. This involves preprocessing
steps such as scaling or imputing, followed by a predictive model, all managed within a custom model class using the
`ModelContext`.

Copy code

```
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
from snowflake.ml.model import custom_model

# Step 1: Load the Iris dataset
iris_X, iris_y = datasets.load_iris(return_X_y=True)

# Step 2: Create a scikit-learn pipeline
# The pipeline includes:
# - A SimpleImputer to handle missing values
# - A StandardScaler to standardize the data
# - A Support Vector Classifier (SVC) for predictions
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('classifier', SVC(kernel='linear', probability=True))
])

# Step 3: Fit the pipeline to the dataset
pipeline.fit(iris_X, iris_y)

# Step 4: Initialize ModelContext with the pipeline
mc = custom_model.ModelContext(
    pipeline_model=pipeline,
)

# Step 5: Define a custom model class to utilize the pipeline
class ExamplePipelineModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)

    @custom_model.inference_api
    def predict(self, input: pd.DataFrame) -> pd.DataFrame:
        # Use the pipeline from the context to process input and make predictions
        predictions = self.context['pipeline_model'].predict(input)
        probabilities = self.context['pipeline_model'].predict_proba(input)

        # Return predictions and probabilities as a DataFrame
        return pd.DataFrame({
            'predictions': predictions,
            'probability_class_0': probabilities[:, 0],
            'probability_class_1': probabilities[:, 1]
        })

# Example usage:
# Convert new input data into a DataFrame
new_input = pd.DataFrame(iris_X[:5])  # Using the first 5 samples for demonstration

# Initialize the custom model and run predictions
custom_pipeline_model = ExamplePipelineModel(context=mc)
result = custom_pipeline_model.predict(new_input)

print(result)
```

## Using your own models

The following example uses your own model as a custom model.

Copy code

```
mc = custom_model.ModelContext(
    my_model=your_own_model,
)

from snowflake.ml.model import custom_model
import pandas as pd
import json

class ExampleYourOwnModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)

    @custom_model.inference_api
    def predict(self, input: pd.DataFrame) -> pd.DataFrame:
        model_output = self.context['my_model'].predict(features)
        return pd.DataFrame({'output': model_output})
```

## Using more than one model

Below is a custom model that combines multiple models and uses a configuration file to apply bias when generating
predictions.

Copy code

```
mc = custom_model.ModelContext(
    model1=model1,
    model2=model2,
    feature_preproc=preproc
    }
)
```

Note

`model1` and `model2` are objects of any type of model natively supported by the registry. `feature_preproc`
is a `scikit-learn pipeline` object.

Copy code

```
from snowflake.ml.model import custom_model
import pandas as pd
import json

class ExamplePipelineModel(custom_model.CustomModel):

    @custom_model.inference_api
    def predict(self, input: pd.DataFrame) -> pd.DataFrame:
        ...
        return pd.DataFrame(...)

# Here is the fully-functional custom model that uses both model1 and model2
class ExamplePipelineModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)

    @custom_model.inference_api
    def predict(self, input: pd.DataFrame) -> pd.DataFrame:
        features = self.context['feature_preproc'].transform(input)
        model_output = self.context['model1'].predict(
            self.context['model2'].predict(features)
        )
        return pd.DataFrame({'output': model_output})
```
