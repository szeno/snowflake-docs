# Model Explainability

During the training process, machine learning models infer relationships between inputs and outputs, rather than
requiring that these relationships be stated explicitly up front. This allows ML techniques to tackle complicated
scenarios involving many variables without extensive setup, particularly where the causal factors of a particular
outcome are complex or unclear, but the resulting model can be something of a black box. If a model underperforms, it
can be difficult to understand why, and furthermore how to improve its performance. The black box model can also conceal
implicit biases and fail to establish clear reasons for decisions. Industries that have regulations around trustworthy
systems, like finance and healthcare, might require stronger evidence that the model is producing the correct results
for the right reasons.

To help address such concerns, the Snowflake Model Registry includes an explainability function based on
[Shapley values](https://towardsdatascience.com/the-shapley-value-for-ml-models-f1100bff78d1). Shapley values are a
way to attribute the output of a machine learning model to its input features. By considering all possible combinations of
features, Shapley values measure the average marginal contribution of each feature to the model’s prediction. This
approach ensures fairness in attributing importance and provides a solid foundation for understanding complex models.
While computationally intensive, the insights gained from Shapley values are invaluable for model interpretability and
debugging.

For example, assume we have a model for predicting the price of a house, which was trained on the homes’ size, location,
number of bedrooms, and whether pets are allowed. In this example, the average price of houses is $100,000, and the final
prediction of the model was $250,000 for a house that is 2000 square feet, beachside, three bedrooms, and doesn’t allow
pets. Each of these feature values might contribute to the final model prediction as shown in the following table.

| Feature | Value | Contribution vs. an average house |
| --- | --- | --- |
| Size | 2000 | +$50,000 |
| Location | Beachside | +$75,000 |
| Bedrooms | 3 | +$50,000 |
| Pets | No | -$25,000 |

Expand

Show lessSee more

Together, these contributions explain why this particular house is priced $150,000 higher than an average home. Shapley
values can affect the final outcome positively or negatively, adding up to a difference of outcomes compared to an
average. In this example, it is less desirable to live in a house where pets are not allowed, so that feature value’s
contribution is -$25,000.

The average value is calculated using background data, a representative sample of the entire dataset. For more information,
see [Logging models with background data](#label-snowpark-model-registry-model-explainability-background-data).

## Supported model types

This preview release supports the following Python-native model packages.

- XGBoost
- CatBoost
- LightGBM
- Scikit-learn

The following Snowpark ML modeling classes from `snowflake.ml.modeling` are supported.

- XGBoost
- LightGBM
- Scikit-learn

Explainability is available by default for the above models logged using Snowpark ML 1.6.2 and later. The
implementation uses the [SHAP library](https://pypi.org/project/shap/).

## Logging models with background data

Background data, typically a sample of representative data, is an important ingredient of Shapley value-based
explanations. Background data gives the Shapley algorithm an idea of what “average” inputs look like to which it can
compare individual explanations.

The Shapley value is computed by systematically perturbing input features and replacing them with the background data.
Because it reports deviation from background data, it is important to use consistent background data when comparing
Shapley values from multiple data sets.

Some tree-based models implicitly encode background data within their structure during training, and may not require
explicit background data. Most models, however, require background data to be provided separately for useful
explanations, and all models (including tree-based models) can be explained more accurately if you provide background
data.

You can provide up to 1,000 rows of background data when logging a model by passing it in the `sample_input_data`
parameter, as shown below.

Note

If the model is a type that requires explicit background data to calculate Shapley values, explainability cannot be
enabled without this data.

Copy code

```
mv = reg.log_model(
    catboost_model,
    model_name="diamond_catboost_explain_enabled",
    version_name="explain_v0",
    conda_dependencies=["snowflake-ml-python"],
    sample_input_data = xs, # xs will be used as background data
)
```

You can also provide background data while logging the model with a signature, as shown below.

Copy code

```
mv = reg.log_model(
    catboost_model,
    model_name="diamond_catboost_explain_enabled",
    version_name="explain_v0",
    conda_dependencies=["snowflake-ml-python"],
    signatures={"predict": predict_signature, "predict_proba": predict_proba_signature},
    sample_input_data = xs, # xs will be used as background data
    options= {"enable_explainability": True} # you will need to set this flag in order to pass both signatures and background data
)
```

## Retrieving explainability values

Models with explainability have a method named `explain` that returns the Shapley values for the model’s features.

Because Shapley values are explanations of predictions made from specific inputs, you must pass input data to `explain` to
generate the predictions to be explained.

The Snowflake model version object will have a method called `explain`, and you call it using `ModelVersion.run` in Python.

Copy code

```
reg = Registry(...)
mv = reg.get_model("Explainable_Catboost_Model").default
explanations = mv.run(input_data, function_name="explain")
```

The following is an example of retrieving the explanation in SQL.

Copy code

```
WITH MV_ALIAS AS MODEL DATABASE.SCHEMA.DIAMOND_CATBOOST_MODEL VERSION EXPLAIN_V0
SELECT *,
      FROM DATABASE.SCHEMA.DIAMOND_DATA,
          TABLE(MV_ALIAS!EXPLAIN(CUT, COLOR, CLARITY, CARAT, DEPTH, TABLE_PCT, X, Y, Z));
```

Important

If you are using `snowflake-ml-python` prior to version 1.7.0, you may receive the error `UnicodeDecodeError: 'utf-8' codec can't decode byte` with XGBoost models.
This is due to an incompatibility between version 0.42.1 of the [SHAP library](https://pypi.org/project/shap/) and the latest XGBoost version (2.1.1) supported by Snowflake.
If you cannot upgrade `snowflake-ml-python` to version 1.7.0 or later, downgrade the XGBoost version to 2.0.3 and log the model with the `relax_version` option set to `False`,
as shown in the following example.

Copy code

```
mv_new = reg.log_model(
    model,
    model_name="model_with_explain_enabled",
    version_name="explain_v0",
    conda_dependencies=["snowflake-ml-python"],
    sample_input_data = xs,
    options={"relax_version": False}
)
```

## Adding explainability to existing models

Models that were logged in the registry using a version of Snowpark ML older than 1.6.2 do not have the explainability
feature. Since model versions are immutable, you must create a new model version to add explainability to an existing
model. You can use `ModelVersion.load` to retrieve the Python object representing the model’s implementation, then log
that to the registry as a new model version. Be sure to pass your background data as `sample_input_data`. This
approach is shown below.

Important

The Python environment into which you load the model must be exactly the same (that is, the same version of Python
and of all libraries) as the environment where the model is deployed. For details, see
[Loading a model version](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-model-versions-loading).

Copy code

```
mv_old = reg.get_model("model_without_explain_enabled").default
model = mv_old.load()
mv_new = reg.log_model(
    model,
    model_name="model_with_explain_enabled",
    version_name="explain_v0",
    conda_dependencies=["snowflake-ml-python"],
    sample_input_data = xs
)
```

## Logging models without explainability

Explainability is enabled by default if the model supports it. To log a model version in the registry without
explainability, pass `False` for the `enable_explainability` option when logging the model, as shown here.

Copy code

```
mv = reg.log_model(
    catboost_model,
    model_name="diamond_catboost_explain_enabled",
    version_name="explain_v0",
    conda_dependencies=["snowflake-ml-python"],
    sample_input_data = xs,
    options= {"enable_explainability": False}
)
```
