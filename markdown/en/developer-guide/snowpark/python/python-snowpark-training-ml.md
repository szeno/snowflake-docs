# Training Machine Learning Models with Snowpark Python

This topic explains how to train machine learning (ML) models with Snowpark.

Note

[Snowpark ML](/developer-guide/snowflake-ml/overview) is a companion to Snowpark Python built specifically for
machine learning in Snowflake. This topic still contains useful general information about machine learning with
Snowpark Python, particularly if you prefer to write your own stored procedures for machine learning.

## Snowpark-Optimized Warehouses

Training machine learning (ML) models can sometimes be very resource intensive.
Snowpark-optimized warehouses are a type of Snowflake virtual warehouse that can be used for workloads
that require a large amount of memory and compute resources. For example, you can use them to train
an ML model using custom code on a single node.

These optimized warehouses can also benefit some UDF and UDTF scenarios.

For more information about how to create a Snowpark-optimized warehouse, see [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized).

## Using Snowpark Python Stored Procedures for ML Training

[Snowpark Python stored procedures](/developer-guide/stored-procedure/python/procedure-python-overview) can be used to run custom code using a Snowflake warehouse.
Snowpark-optimized warehouses make it possible to use Snowpark stored procedures to run
single-node ML training workloads directly in Snowflake.

A Python stored procedure can run nested queries, using the [Snowpark API for Python](/developer-guide/snowpark/python/index), to load and
transform the dataset, which is then loaded into the stored procedure memory to perform
pre-processing and ML training.
The trained model can be uploaded into a Snowflake stage, and can be used to create UDFs to perform inference.

While Snowpark-optimized warehouses can be used to execute pre-processing and training logic, it
may be necessary to execute nested queries in a separate warehouse to achieve better performance
and resource utilization. A separate query warehouse can be tuned and scaled independently based
on the dataset size.

### Guidelines

Follow these guidelines to perform single-node ML training workloads:

- Set WAREHOUSE\_SIZE = MEDIUM to ensure that the Snowpark-optimized warehouse consists of 1 Snowpark-optimized node.
- Consider setting up the warehouse as [multi-cluster warehouse](/user-guide/warehouses-multicluster) to support the desired concurrency
  if needed.
- Consider using a separate warehouse for executing nested queries from the stored procedure:

  - Use the [session.use\_warehouse()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.Session.use_warehouse) API
    to select the warehouse for the query inside the stored procedure.
- Don’t mix other workloads on the Snowpark-optimized warehouse that is used to run ML training stored procedures.

#### Example

The following example creates and uses a Snowpark-optimized warehouse. The example then creates a stored procedure that trains a linear regression model.
The stored procedure uses data in a table named `MARKETING_BUDGETS_FEATURES` (not shown here).

Copy code

```
CREATE OR REPLACE WAREHOUSE snowpark_opt_wh WITH
  WAREHOUSE_SIZE = 'MEDIUM'
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
  MAX_CONCURRENCY_LEVEL = 1;

CREATE OR REPLACE PROCEDURE train()
  RETURNS VARIANT
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('snowflake-snowpark-python', 'scikit-learn', 'joblib')
  HANDLER = 'main'
AS $$
import os
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from joblib import dump

def main(session):
 # Load features
 df = session.table('MARKETING_BUDGETS_FEATURES').to_pandas()
 X = df.drop('REVENUE', axis = 1)
 y = df['REVENUE']

 # Split dataset into training and test
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)

 # Preprocess numeric columns
 numeric_features = ['SEARCH_ENGINE','SOCIAL_MEDIA','VIDEO','EMAIL']
 numeric_transformer = Pipeline(steps=[('poly',PolynomialFeatures(degree = 2)),('scaler', StandardScaler())])
 preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features)])

 # Create pipeline and train
 pipeline = Pipeline(steps=[('preprocessor', preprocessor),('classifier', LinearRegression(n_jobs=-1))])
 model = GridSearchCV(pipeline, param_grid={}, n_jobs=-1, cv=10)
 model.fit(X_train, y_train)

 # Upload trained model to a stage
 model_file = os.path.join('/tmp', 'model.joblib')
 dump(model, model_file)
 session.file.put(model_file, "@ml_models",overwrite=True)

 # Return model R2 score on train and test data
 return {"R2 score on Train": model.score(X_train, y_train),"R2 score on Test": model.score(X_test, y_test)}
$$;
```

To call the stored procedure, execute the following command:

Copy code

```
CALL train();
```

Note

Various other Snowpark Python demos are available in the
[Snowflake-Labs GitHub repository](https://github.com/Snowflake-Labs/snowpark-python-demos).
The [Advertising Spend and ROI Prediction](https://github.com/Snowflake-Labs/snowpark-python-demos/blob/main/Advertising-Spend-ROI-Prediction/Snowpark_For_Python.ipynb)
example demonstrates how to create a stored procedure that trains a linear regression model.
