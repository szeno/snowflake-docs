# Engineer features

Snowflake ML allows you to transform your raw data into features, allowing for efficient use by machine learning models.
You can transform data using several approaches, each suited for different scales and requirements:

- **Open Source Software (OSS) preprocessors** - For small to medium datasets and quick prototyping, use familiar Python ML libraries that run locally or on single nodes within Container Runtime.
- **Snowflake ML Preprocessors** - For larger datasets, use Snowflake ML’s preprocessing APIs that execute natively on the Snowflake platform. These APIs distribute the processing across warehouse compute resources.
- **Ray map\_batches** - For highly customizable large-scale processing, especially with unstructured data, use parallel, resource-managed execution across single-node or multi-node Container Runtime environments.

Choose the approach that best matches your data size, performance requirements, and need for custom transformation logic.

The following table shows detailed comparisons of three main approaches for feature engineering in Snowflake ML:

| Feature/Aspect | OSS (including scikit-learn) | Snowflake ML preprocessors | Ray `map_batches` |
| --- | --- | --- | --- |
| Scale | Small & medium datasets | Large/distributed data | Large/distributed data |
| Execution Environment | In memory | Pushdown to the default warehouse that you’re using to run SQL queries | Across nodes in a compute pool |
| Compute Resources | Snowpark Container Services (Compute Pool) | Warehouse | Snowpark Container Services (Compute Pool) |
| Integration | Standard Python ML ecosystem | Integrates natively with Snowflake ML | Both with Python ML and Snowflake |
| Performance | Fast for local, in-memory workloads; scale limited and non-distributed | Designed for scalable, distributed feature engineering | Highly parallel and resource-managed, excels on large/unstructured data |
| Use Case Suitability | Quickly prototyping and experimentation | Production workflows with large datasets | Large data workflows that require custom resource controls |

Expand

Show lessSee more

The following examples demonstrate how to implement feature transformations using each approach:

OSS scikit-learnSnowflake ML PreprocessorsRay map\_batches

Use the following code to implement scikit-learn for your preprocessing workflows:

Copy code

```
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Load your data locally into a Pandas DataFrame
df = pd.DataFrame({
    'age': [34, 23, 54, 31],
    'city': ['SF', 'NY', 'SF', 'LA'],
    'income': [120000, 95000, 135000, 99000]
})

# Define preprocessing steps
numeric_features = ['age', 'income']
numeric_transformer = StandardScaler()

categorical_features = ['city']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
])

# Preprocess the data
X_processed = pipeline.fit_transform(df)
print(X_processed)
```

Snowflake ML preprocessors handle distributed transformations directly within Snowflake. These preprocessors are pushed down to scale across warehouses.
Use Snowflake ML preprocessors for large datasets and production workloads.

Note

The Snowflake ML preprocessors are a subset of the preprocessors available in scikit-learn, but they cover the most common use cases.
For information about the available preprocessors, see [Snowflake ML modeling preprocessing](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/modeling#snowflake-ml-modeling-preprocessing).

The following code uses the `StandardScaler` and `OneHotEncoder` libraries.

Copy code

```
from snowflake.snowpark import Session
from snowflake.ml.modeling.preprocessing import StandardScaler, OneHotEncoder
from snowflake.ml.modeling.pipeline import Pipeline

# Assume your Snowflake connection details are configured
session = Session.builder.configs(...).create()

# Load your data from a Snowflake table as a DataFrame
df = session.table('CUSTOMER_DATA')

# Define Snowflake ML preprocessors
scaler = StandardScaler(input_cols=['AGE', 'INCOME'], output_cols=['AGE_SCALED', 'INCOME_SCALED'])
encoder = OneHotEncoder(input_cols=['CITY'], output_cols=['CITY_ENCODED'])

pipeline = Pipeline(steps=[
    ('scaling', scaler),
    ('encoding', encoder)
])

# Fit and transform data in Snowflake (distributed)
result = pipeline.fit_transform(df)
result.show()
```

Use Ray for distributed, parallel processing with custom transformations. Ray `map_batches` uses lazy execution, meaning processing won’t happen until you materialize the datasets, which helps reduce memory usage. This approach is ideal for large-scale data processing with custom logic:

Copy code

```
import ray
from snowflake.ml.ray.datasource.stage_parquet_file_datasource import SFStageParquetDataSource
from snowflake.ml.data.data_connector import DataConnector

# Example for data transform
def preprocess_batch(batch: pd.DataFrame) -> pd.DataFrame:
    batch['AGE_SCALED'] = (batch['age'] - batch['age'].mean()) / batch['age'].std()
    return batch

# Example of filtering
def filter_by_value(row):
    return row['city'] != 'LA'

# Build Ray dataset from provided datasources
ray_ds = ray.data.read_datasource(data_source)

# Setup filter operations, not executed yet
filtered_ds = ray_ds.filter(filter_by_value)

transformed_ds = filtered_ds.map_batches(example_transform_batch_function)

# Create DataConnector directly from ray dataset
data_connector = DataConnector.from_ray_dataset(transformed_ds)
```
