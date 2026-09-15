# Create, train and use a Snowflake ML model in an app

This topic provides an example of how to train a Snowflake ML model within a Snowflake Native App
using the `scikit-learn` Python package. The example in this topic can be used to
train models on data in the consumer or provider accounts.

## Create a versioned schema to hold the stored procedures

Within the setup script create a versioned schema that contains the stored
procedure as shown in the following example:

1. Create a versioned schema for the stored procedure:

   Copy code

   ```
   CREATE OR ALTER VERSIONED SCHEMA core;
   GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;
   ```

## Create a stored procedure to create and train a model

1. Create a stored procedure for the Python function you are using to train a
   model as shown in the following example:

> Copy code
>
> ```
> CREATE OR REPLACE PROCEDURE core.py_log_model(mname STRING, mvname STRING)
> RETURNS STRING
> LANGUAGE python
> RUNTIME_VERSION = 3.11
> HANDLER = 'log_model'
> PACKAGES = ('snowflake-snowpark-python','scikit-learn', 'snowflake-ml-python >=1.6.2', 'pandas', 'numpy', 'xgboost')
> AS '
>   -- <body of the stored procedure>
> ';
> ```
>
> This example creates a stored procedure named `py_log_model` and declares the Python packages required to train a model using `scikit-learn`:
>
> - snowflake-snowpark-python
> - scikit-learn
> - snowflake-ml-python
> - pandas
> - numpy
> - xgboost
>
> After creating a stored procedure, add the following code to the body
> of the stored procedure:

1. Add Python code to the body of the stored procedure:

> Copy code
>
> ```
> import _snowflake
> from snowflake.ml.registry import Registry
> import pandas as pd
> import numpy as np
> from sklearn import datasets
> from snowflake.ml.modeling.xgboost import XGBClassifier
>
> def log_model(sp_session, mname, mvname):
>     reg = Registry(session=sp_session, schema_name=''stateful_schema'')
>
>     iris = datasets.load_iris()
>     df = pd.DataFrame(data=np.c_[iris["data"], iris["target"]], columns=iris["feature_names"] + ["target"])
>     df.columns = [s.replace(" (CM)", "").replace(" ", "") for s in df.columns.str.upper()]
>     input_cols = ["SEPALLENGTH", "SEPALWIDTH", "PETALLENGTH", "PETALWIDTH"]
>     label_cols = "TARGET"
>     output_cols = "PREDICTED_TARGET"
>
>     clf_xgb = XGBClassifier(
>         input_cols=input_cols, output_cols=output_cols, label_cols=label_cols, drop_input_cols=True
>     )
>     clf_xgb.fit(df)
>     model_ref = reg.log_model(
>         clf_xgb,
>         model_name=f"{mname}",
>         version_name=f"{mvname}",
>         options={"enable_explainability": False},
>     )
>     return "success"
> ```
>
> The `log_model` function performs the following:
>
> - Uses `pandas` and `numpy` to create a DataFrame to serve as the
>   training data for the model.
> - Creates an instance of the XGBoost classifier to serve as the training algorithm for the data.
> - Calls the `fit()` function of XGBoost to create a model and train it on the dataset.
> - Calls the `log_model()` function of Snowflake Model Registry to add the model to the
>   model registry.
>
> Note
>
> Models created by an app must be stored in a model registry. Apps cannot access models that are
> stored on a stage.

1. Optional: To allow consumers to run the stored procedure to train the model, grant the USAGE privilege
   on the stored procedure:

   Copy code

   ```
   GRANT USAGE ON PROCEDURE core.py_log_model(STRING, STRING) TO APPLICATION ROLE app_public;
   ```

## Create a stored procedure to run a model

1. Create a stored procedure for the Python function you use to call the model.

Copy code

```
  CREATE OR REPLACE PROCEDURE core.py_call_predict(mname STRING, mvname STRING)
  RETURNS TABLE()
  LANGUAGE python
  RUNTIME_VERSION = 3.11
  HANDLER = 'run_model'
  PACKAGES = ('snowflake-snowpark-python','scikit-learn', 'snowflake-ml-python>=1.6.2', 'pandas', 'xgboost')
  AS
'
-- <body of the stored procedure>
';
```

1. Add the Python code you use to call the model:

> Copy code
>
> ```
> import _snowflake
> from snowflake.ml.registry import Registry
> import pandas as pd
> from sklearn import datasets
>
> def run_model(sp_session, mname, mvname):
>   iris = datasets.load_iris()
>   df = pd.DataFrame(data=iris["data"], columns=iris["feature_names"])
>   df.columns = [s.replace(" (CM)", "").replace(" ", "") for s in df.columns.str.upper()]
>
>   reg = Registry(session=sp_session, schema_name="stateful_schema")
>   mv = reg.get_model(mname).version(mvname)
>
>   pred = mv.run(df.head(10), function_name="predict")
>   return sp_session.create_dataframe(pred)
> ```
>
> The `run_model` function does the following:
>
> - Runs the `load_iris()` function to
>   [load the iris machine learning dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html).
> - Uses `pandas` to create a DataFrame based on the iris data set.
> - Runs the `get_model()` function to retrieve the model from the registry.
> - Runs the predict function on the model.
> - Returns the result.

1. Optional: To allow consumers to run the stored procedure to train the model, grant the USAGE privilege
   on the stored procedure:

   Copy code

   ```
   GRANT USAGE ON PROCEDURE core.py_call_predict(STRING, STRING) TO APPLICATION ROLE app_public;
   ```

## Run the stored procedures

If the app grants the USAGE privilege on these stored procedures to an application role, consumers can
call the stored procedures to train and run the models as shown in the following examples:

Copy code

```
CALL my_app.core.py_log_model('md1', 'V1');
```

This command calls the `py_log_model` stored procedure to train the model.

Copy code

```
CALL my_app.core.py_call_predict('md1', 'V1');
```

This command calls the `py_call_predict` stored procedure to call the predict function on the model.
