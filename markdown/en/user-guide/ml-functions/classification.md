# Classification (Snowflake ML Functions)

Classification uses machine learning algorithms to sort data into different classes using patterns detected in training
data. Binary classification (two classes) and multi-class classification (more than two classes) are supported. Common
use cases of classification include customer churn prediction, credit card fraud detection, and spam detection.

Note

Classification is part of Snowflake’s suite of business analysis tools powered by machine learning.

Classification involves creating a classification model object, passing in a reference to the training data. The model
is fitted to the provided training data. You then use the resulting schema-level classification model object to classify
new data points and to understand the model’s accuracy through its evaluation APIs.

## About the Classification Model

The classification function is powered by a
[gradient boosting machine](https://en.wikipedia.org/wiki/Gradient_boosting).
For binary classification, the model is trained using an
[area-under-the-curve](https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Area_under_the_curve)
loss function. For multi-class classification, the model is trained using a
[logistic loss](https://en.wikipedia.org/wiki/Loss_functions_for_classification#Logistic_loss) function.

Suitable training datasets for use with classification include a target column representing the labeled class of each
data point and at least one feature column.

The classification model supports numeric, Boolean, and string data types for features and labels.

- Numeric features are treated as continuous. To treat numeric features as categorical, cast them to strings.
- String features are treated as categorical. The classification function supports high-cardinality features (for
  example, job titles or fruits). It does not support full free text, like sentences or paragraphs.
- Boolean features are treated as categorical.
- Timestamps must be [TIMESTAMP\_NTZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) type. The model creates additional
  time-based features (epoch, day, week, month), which are used in training and classification. These features appear in
  [SHOW\_FEATURE\_IMPORTANCE](/sql-reference/classes/classification/methods/show_feature_importance) results as
  `derived_features`.
- The cardinality of the label (target) column must be greater than one and less than the number of rows in the dataset.

Inference data must have the same feature names and types as training data. It is not an error for a categorical feature
to have a value that is not present in the training dataset. Columns in the inference data that were not present in the
training dataset are ignored.

Classification models can be evaluated for quality of prediction. In the evaluation process, an additional model is
trained on the original data but with some data points withheld. The withheld data points are then used for inference,
and the predicted classes are compared to the actual classes.

### Current Limitations

- Training and inference data must be numeric, TIMESTAMP\_NTZ, Boolean, or string. Other types must be cast to one of
  these types.
- You cannot choose or modify the classification algorithm.
- Model parameters cannot be manually specified or adjusted.
- In tests, training on a Medium Snowpark-optimized warehouse has succeeded with up to 1,000 columns and 600 million
  rows. It is possible, but unlikely, to run out of memory below this limit.
- Your target column must contain no more than 255 distinct classes.
- SNOWFLAKE.ML.CLASSIFICATION instances cannot be cloned. When you clone or replicate a database containing a
  classification model, the model is currently skipped.

## Preparing for Classification

Before you can use classification, you must:

- [Select a virtual warehouse](#label-cortex-classification-select-warehouse) in which to train and run your models.
- [Grant the privileges](#label-cortex-classification-grant-privileges) required to create classification models.

You might also want to [modify your search path](/sql-reference/snowflake-db-classes#label-update-search-path) to include the SNOWFLAKE.ML schema.

### Selecting a Virtual Warehouse

A Snowflake [virtual warehouse](/user-guide/warehouses) provides the compute resources for training and using
classification machine learning models. This section provides general guidance on selecting the best type and size of
warehouse for classification, focusing on the training step, the most time-consuming and memory-intensive part of the
process.

You should choose the warehouse type based on the size of your training data. Standard warehouses are subject to a lower
Snowpark memory limit, and are appropriate for prototyping with fewer rows or features. Memory limits of standard
warehouses do not increase with warehouse size.

As the number of rows or features increases, consider using a Snowpark-optimized warehouse to ensure training can
succeed. Memory limits of Snowpark-optimized warehouses do not increase above Medium.

For best performance, train your models using a dedicated warehouse without other concurrent workloads.

To minimize costs, we recommend using an X-Small standard warehouse for prototyping. For larger datasets and production
workloads, use a Medium Snowpark-optimized warehouse.

### Granting Privileges to Create Classification Models

Training a classification model results in a schema-level object. Therefore, the role you use to create models must
have the CREATE SNOWFLAKE.ML.CLASSIFICATION privilege on the schema where the model will be created, allowing the
model to be stored there. This privilege is similar to other schema privileges like CREATE TABLE or CREATE VIEW.

Snowflake recommends that you create a role named `analyst` to be used by people who need to create classification
models.

In the following example, the `admin` role is the owner of the schema `admin_db.admin_schema`. The
`analyst` role needs to create models in this schema.

Copy code

```
USE ROLE admin;
GRANT USAGE ON DATABASE admin_db TO ROLE analyst;
GRANT USAGE ON SCHEMA admin_schema TO ROLE analyst;
GRANT CREATE SNOWFLAKE.ML.CLASSIFICATION ON SCHEMA admin_db.admin_schema TO ROLE analyst;
```

To use this schema, a user assumes the role `analyst`:

Copy code

```
USE ROLE analyst;
USE SCHEMA admin_db.admin_schema;
```

If the `analyst` role has CREATE SCHEMA privileges in database `analyst_db`, the role can create a new schema
`analyst_db.analyst_schema` and create classification models in that schema:

Copy code

```
USE ROLE analyst;
CREATE SCHEMA analyst_db.analyst_schema;
USE SCHEMA analyst_db.analyst_schema;
```

To revoke a role’s model creation privilege on the schema, use [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege):

Copy code

```
REVOKE CREATE SNOWFLAKE.ML.CLASSIFICATION ON SCHEMA admin_db.admin_schema FROM ROLE analyst;
```

## Training, Using, Viewing, Deleting, and Updating Models

Note

SNOWFLAKE.ML.CLASSIFICATION runs using limited privileges, so by default, it does not have access to your data. You
must therefore pass tables and views as [references](/developer-guide/stored-procedure/stored-procedures-calling-references),
which pass along the caller’s privileges. You can also provide a [query reference](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-query-references)
instead of a reference to a table or a view.

See the [CLASSIFICATION reference](/sql-reference/classes/classification) for information about training, inference, and evaluation APIs.

Use CREATE SNOWFLAKE.ML.CLASSIFICATION to create and train a model.

Copy code

```
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION <model_name>(...);
```

To run inference (prediction) on a dataset, use the model’s PREDICT method.

Copy code

```
SELECT <model_name>!PREDICT(...);
```

To evaluate a model, call the provided evaluation methods.

Copy code

```
CALL <model_name>!SHOW_EVALUATION_METRICS();
CALL <model_name>!SHOW_GLOBAL_EVALUATION_METRICS();
CALL <model_name>!SHOW_THRESHOLD_METRICS();
CALL <model_name>!SHOW_CONFUSION_MATRIX();
```

To show a model’s feature importance ranking, call its SHOW\_FEATURE\_IMPORTANCE method.

Copy code

```
CALL <model_name>!SHOW_FEATURE_IMPORTANCE();
```

To investigate logs generated during training, use the SHOW\_TRAINING\_LOGS method. If no training logs are available, this call returns NULL.

Copy code

```
CALL <model_name>!SHOW_TRAINING_LOGS();
```

Tip

For examples of using these methods, see [Examples](#label-cortex-classification-examples).

To view all classification models, use the SHOW command.

Copy code

```
SHOW SNOWFLAKE.ML.CLASSIFICATION;
```

To delete a classification model, use the DROP command.

Copy code

```
DROP SNOWFLAKE.ML.CLASSIFICATION <model_name>;
```

Models are immutable and cannot be updated in place. To update a model, drop the existing model and train a new one.
The CREATE OR REPLACE variant of the CREATE command is useful for this purpose.

## Examples

### Setting Up the Data for the Examples

The examples in this topic uses two tables. The first table, `training_purchase_data`, has two feature columns: a
binary label column and a multi-class label column. The second table is called
`prediction_purchase_data` and has two feature columns. Use the SQL below to create these
tables.

Copy code

```
CREATE OR REPLACE TABLE training_purchase_data AS (
    SELECT
        CAST(UNIFORM(0, 4, RANDOM()) AS VARCHAR) AS user_interest_score,
        UNIFORM(0, 3, RANDOM()) AS user_rating,
        FALSE AS label,
        'not_interested' AS class
    FROM TABLE(GENERATOR(rowCount => 100))
    UNION ALL
    SELECT
        CAST(UNIFORM(4, 7, RANDOM()) AS VARCHAR) AS user_interest_score,
        UNIFORM(3, 7, RANDOM()) AS user_rating,
        FALSE AS label,
        'add_to_wishlist' AS class
    FROM TABLE(GENERATOR(rowCount => 100))
    UNION ALL
    SELECT
        CAST(UNIFORM(7, 10, RANDOM()) AS VARCHAR) AS user_interest_score,
        UNIFORM(7, 10, RANDOM()) AS user_rating,
        TRUE AS label,
        'purchase' AS class
    FROM TABLE(GENERATOR(rowCount => 100))
);

CREATE OR REPLACE table prediction_purchase_data AS (
    SELECT
        CAST(UNIFORM(0, 4, RANDOM()) AS VARCHAR) AS user_interest_score,
        UNIFORM(0, 3, RANDOM()) AS user_rating
    FROM TABLE(GENERATOR(rowCount => 100))
    UNION ALL
    SELECT
        CAST(UNIFORM(4, 7, RANDOM()) AS VARCHAR) AS user_interest_score,
        UNIFORM(3, 7, RANDOM()) AS user_rating
    FROM TABLE(GENERATOR(rowCount => 100))
    UNION ALL
    SELECT
        CAST(UNIFORM(7, 10, RANDOM()) AS VARCHAR) AS user_interest_score,
        UNIFORM(7, 10, RANDOM()) AS user_rating
    FROM TABLE(GENERATOR(rowCount => 100))
);
```

### Training and Using a Binary Classifier

First, create a view containing binary data for training.

Copy code

```
CREATE OR REPLACE view binary_classification_view AS
    SELECT user_interest_score, user_rating, label
FROM training_purchase_data;
SELECT * FROM binary_classification_view ORDER BY RANDOM(42) LIMIT 5;
```

The SELECT statement returns results in the following form.

```
+---------------------+-------------+-------+
| USER_INTEREST_SCORE | USER_RATING | LABEL |
|---------------------+-------------+-------|
| 5                   |           4 | False |
| 8                   |           8 | True  |
| 6                   |           5 | False |
| 7                   |           7 | True  |
| 7                   |           4 | False |
+---------------------+-------------+-------+
```

Using this view, create and train a binary classification model.

Copy code

```
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION model_binary(
    INPUT_DATA => SYSTEM$REFERENCE('view', 'binary_classification_view'),
    TARGET_COLNAME => 'label'
);
```

After you’ve created the model, use its PREDICT method to infer labels for the unlabeled purchase data. You can use
[wildcard expansion in an object literal](/sql-reference/data-types-semistructured#label-object-constant-wildcard) to create key-value pairs of features
for the INPUT\_DATA argument.

Copy code

```
SELECT model_binary!PREDICT(INPUT_DATA => {*})
    AS prediction FROM prediction_purchase_data;
```

The model returns output in the following format. The prediction object includes predicted probabilities for each class
and the predicted class based on the maximum predicted probability. The predictions are returned in the same order as
the original features were provided.

```
+-------------------------------------+
| PREDICTION                          |
|-------------------------------------|
| {                                   |
|   "class": "True",                  |
|   "logs": null,                     |
|   "probability": {                  |
|     "False": 1.828038600000000e-03, |
|     "True": 9.981719614000000e-01   |
|   }                                 |
| }                                   |
| {                                   |
|   "class": "False",                 |
|   "logs": null,                     |
|   "probability": {                  |
|     "False": 9.992944771000000e-01, |
|     "True": 7.055229000000000e-04   |
|   }                                 |
| }                                   |
| {                                   |
|   "class": "True",                  |
|   "logs": null,                     |
|   "probability": {                  |
|     "False": 3.429796010000000e-02, |
|     "True": 9.657020399000000e-01   |
|   }                                 |
| }                                   |
| {                                   |
|   "class": "False",                 |
|   "logs": null,                     |
|   "probability": {                  |
|     "False": 9.992687686000000e-01, |
|     "True": 7.312314000000000e-04   |
|   }                                 |
| }                                   |
| {                                   |
|   "class": "False",                 |
|   "logs": null,                     |
|   "probability": {                  |
|     "False": 9.992951615000000e-01, |
|     "True": 7.048385000000000e-04   |
|   }                                 |
| }                                   |
+-------------------------------------+
```

To zip together features and predictions, use a query like the following.

Copy code

```
SELECT *, model_binary!PREDICT(INPUT_DATA => {*})
    AS predictions FROM prediction_purchase_data;
```

```
+---------------------+-------------+-------------------------------------+
| USER_INTEREST_SCORE | USER_RATING | PREDICTIONS                         |
|---------------------+-------------+-------------------------------------|
| 9                   |           8 | {                                   |
|                     |             |   "class": "True",                  |
|                     |             |   "logs": null,                     |
|                     |             |   "probability": {                  |
|                     |             |     "False": 1.828038600000000e-03, |
|                     |             |     "True": 9.981719614000000e-01   |
|                     |             |   }                                 |
|                     |             | }                                   |
| 3                   |           0 | {                                   |
|                     |             |   "class": "False",                 |
|                     |             |   "logs": null,                     |
|                     |             |   "probability": {                  |
|                     |             |     "False": 9.992944771000000e-01, |
|                     |             |     "True": 7.055229000000000e-04   |
|                     |             |   }                                 |
|                     |             | }                                   |
| 10                  |           7 | {                                   |
|                     |             |   "class": "True",                  |
|                     |             |   "logs": null,                     |
|                     |             |   "probability": {                  |
|                     |             |     "False": 3.429796010000000e-02, |
|                     |             |     "True": 9.657020399000000e-01   |
|                     |             |   }                                 |
|                     |             | }                                   |
| 6                   |           6 | {                                   |
|                     |             |   "class": "False",                 |
|                     |             |   "logs": null,                     |
|                     |             |   "probability": {                  |
|                     |             |     "False": 9.992687686000000e-01, |
|                     |             |     "True": 7.312314000000000e-04   |
|                     |             |   }                                 |
|                     |             | }                                   |
| 1                   |           3 | {                                   |
|                     |             |   "class": "False",                 |
|                     |             |   "logs": null,                     |
|                     |             |   "probability": {                  |
|                     |             |     "False": 9.992951615000000e-01, |
|                     |             |     "True": 7.048385000000000e-04   |
|                     |             |   }                                 |
|                     |             | }                                   |
+---------------------+-------------+-------------------------------------+
```

### Training and Using a Multi-Class Classifier

Create a view containing binary data for training.

Copy code

```
CREATE OR REPLACE VIEW multiclass_classification_view AS
    SELECT user_interest_score, user_rating, class
FROM training_purchase_data;
SELECT * FROM multiclass_classification_view ORDER BY RANDOM(42) LIMIT 10;
```

This SELECT statement returns results in the following form.

```
+---------------------+-------------+-----------------+
| USER_INTEREST_SCORE | USER_RATING | CLASS           |
|---------------------+-------------+-----------------|
| 5                   |           4 | add_to_wishlist |
| 8                   |           8 | purchase        |
| 6                   |           5 | add_to_wishlist |
| 7                   |           7 | purchase        |
| 7                   |           4 | add_to_wishlist |
| 1                   |           1 | not_interested  |
| 2                   |           1 | not_interested  |
| 7                   |           3 | add_to_wishlist |
| 2                   |           0 | not_interested  |
| 0                   |           1 | not_interested  |
+---------------------+-------------+-----------------+
```

Now create a multi-class classification model from this view.

Copy code

```
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION model_multiclass(
    INPUT_DATA => SYSTEM$REFERENCE('view', 'multiclass_classification_view'),
    TARGET_COLNAME => 'class'
);
```

After you’ve created the model, use its PREDICT method to infer labels for the unlabeled purchase data. Use
[wildcard expansion in an object literal](/sql-reference/data-types-semistructured#label-object-constant-wildcard) to automatically create key-value pairs
for the INPUT\_DATA argument.

Copy code

```
SELECT *, model_multiclass!PREDICT(INPUT_DATA => {*})
    AS predictions FROM prediction_purchase_data;
```

The model returns output in the following format. The prediction object includes predicted probabilities for each class
and the predicted class based on the maximum predicted probability. The predictions are returned in the same order as the
original features provided and can be joined in the same query.

```
+---------------------+-------------+-----------------------------------------------+
| USER_INTEREST_SCORE | USER_RATING | PREDICTIONS                                   |
|---------------------+-------------+-----------------------------------------------|
| 9                   |           8 | {                                             |
|                     |             |   "class": "purchase",                        |
|                     |             |   "logs": null,                               |
|                     |             |   "probability": {                            |
|                     |             |     "add_to_wishlist": 3.529288000000000e-04, |
|                     |             |     "not_interested": 2.259768000000000e-04,  |
|                     |             |     "purchase": 9.994210944000000e-01         |
|                     |             |   }                                           |
|                     |             | }                                             |
| 3                   |           0 | {                                             |
|                     |             |   "class": "not_interested",                  |
|                     |             |   "logs": null,                               |
|                     |             |   "probability": {                            |
|                     |             |     "add_to_wishlist": 3.201690000000000e-04, |
|                     |             |     "not_interested": 9.994749885000000e-01,  |
|                     |             |     "purchase": 2.048425000000000e-04         |
|                     |             |   }                                           |
|                     |             | }                                             |
| 10                  |           7 | {                                             |
|                     |             |   "class": "purchase",                        |
|                     |             |   "logs": null,                               |
|                     |             |   "probability": {                            |
|                     |             |     "add_to_wishlist": 1.271809310000000e-02, |
|                     |             |     "not_interested": 3.992673600000000e-03,  |
|                     |             |     "purchase": 9.832892333000000e-01         |
|                     |             |   }                                           |
|                     |             | }                                             |
| 6                   |           6 | {                                             |
|                     |             |   "class": "add_to_wishlist",                 |
|                     |             |   "logs": null,                               |
|                     |             |   "probability": {                            |
|                     |             |     "add_to_wishlist": 9.999112027000000e-01, |
|                     |             |     "not_interested": 4.612520000000000e-05,  |
|                     |             |     "purchase": 4.267210000000000e-05         |
|                     |             |   }                                           |
|                     |             | }                                             |
| 1                   |           3 | {                                             |
|                     |             |   "class": "not_interested",                  |
|                     |             |   "logs": null,                               |
|                     |             |   "probability": {                            |
|                     |             |     "add_to_wishlist": 2.049559150000000e-02, |
|                     |             |     "not_interested": 9.759854413000000e-01,  |
|                     |             |     "purchase": 3.518967300000000e-03         |
|                     |             |   }                                           |
|                     |             | }                                             |
+---------------------+-------------+-----------------------------------------------+
```

### Saving Results to a Table and Exploring Predictions

Results of the calls to models’ PREDICT method can be read directly into a query, but saving the results to a table
allows you to conveniently explore predictions.

Copy code

```
CREATE OR REPLACE TABLE my_predictions AS
SELECT *, model_multiclass!PREDICT(INPUT_DATA => {*}) AS predictions FROM prediction_purchase_data;

SELECT * FROM my_predictions;
```

The key and prediction columns can then be explored in further queries. The query below explores predictions.

Copy code

```
SELECT
    predictions:class AS predicted_class,
    ROUND(predictions:probability:not_interested,4) AS not_interested_class_probability,
    ROUND(predictions['probability']['purchase'],4) AS purchase_class_probability,
    ROUND(predictions['probability']['add_to_wishlist'],4) AS add_to_wishlist_class_probability
FROM my_predictions
LIMIT 5;
```

The query above returns results in the following form.

```
+-------------------+----------------------------------+----------------------------+-----------------------------------+
| PREDICTED_CLASS   | NOT_INTERESTED_CLASS_PROBABILITY | PURCHASE_CLASS_PROBABILITY | ADD_TO_WISHLIST_CLASS_PROBABILITY |
|-------------------+----------------------------------+----------------------------+-----------------------------------|
| "purchase"        |                           0.0002 |                     0.9994 |                            0.0004 |
| "not_interested"  |                           0.9995 |                     0.0002 |                            0.0003 |
| "purchase"        |                           0.0002 |                     0.9994 |                            0.0004 |
| "purchase"        |                           0.0002 |                     0.9994 |                            0.0004 |
| "not_interested"  |                           0.9994 |                     0.0002 |                            0.0004 |
| "purchase"        |                           0.0002 |                     0.9994 |                            0.0004 |
| "add_to_wishlist" |                           0      |                     0      |                            0.9999 |
| "add_to_wishlist" |                           0.4561 |                     0.0029 |                            0.5409 |
| "purchase"        |                           0.0002 |                     0.9994 |                            0.0004 |
| "not_interested"  |                           0.9994 |                     0.0002 |                            0.0003 |
+-------------------+----------------------------------+----------------------------+-----------------------------------+
```

### Using Evaluation Functions

By default, evaluation is enabled on all instances. However, evaluation can be manually enabled or disabled using the
config object argument. If the key ‘evaluate’ is specified with the value FALSE, evaluation is not available.

Copy code

```
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION model(
    INPUT_DATA => SYSTEM$REFERENCE('view', 'binary_classification_view'),
    TARGET_COLNAME => 'label',
    CONFIG_OBJECT => {'evaluate': TRUE}
);
```

When evaluation is enabled, evaluation metrics can be obtained using the evaluation APIs shown here.

Copy code

```
CALL model!SHOW_EVALUATION_METRICS();
CALL model!SHOW_GLOBAL_EVALUATION_METRICS();
CALL model!SHOW_THRESHOLD_METRICS();
CALL model!SHOW_CONFUSION_MATRIX();
```

See [Understanding Evaluation Metrics](#label-cortex-classification-understanding-metrics) for a description of the returned metrics.

The evaluation metrics of our multiclass model are as follows..

Copy code

```
CALL model_multiclass!SHOW_EVALUATION_METRICS();
```

```
+--------------+-----------------+--------------+---------------+------+
| DATASET_TYPE | CLASS           | ERROR_METRIC |  METRIC_VALUE | LOGS |
|--------------+-----------------+--------------+---------------+------|
| EVAL         | add_to_wishlist | precision    |  0.8888888889 | NULL |
| EVAL         | add_to_wishlist | recall       |  1            | NULL |
| EVAL         | add_to_wishlist | f1           |  0.9411764706 | NULL |
| EVAL         | add_to_wishlist | support      | 16            | NULL |
| EVAL         | not_interested  | precision    |  1            | NULL |
| EVAL         | not_interested  | recall       |  0.9090909091 | NULL |
| EVAL         | not_interested  | f1           |  0.9523809524 | NULL |
| EVAL         | not_interested  | support      | 22            | NULL |
| EVAL         | purchase        | precision    |  1            | NULL |
| EVAL         | purchase        | recall       |  1            | NULL |
| EVAL         | purchase        | f1           |  1            | NULL |
| EVAL         | purchase        | support      | 22            | NULL |
+--------------+-----------------+--------------+---------------+------+
```

Copy code

```
CALL model_multiclass!SHOW_GLOBAL_EVALUATION_METRICS();
```

```
+--------------+--------------+--------------+---------------+------+
| DATASET_TYPE | AVERAGE_TYPE | ERROR_METRIC |  METRIC_VALUE | LOGS |
|--------------+--------------+--------------+---------------+------|
| EVAL         | macro        | precision    | 0.962962963   | NULL |
| EVAL         | macro        | recall       | 0.9696969697  | NULL |
| EVAL         | macro        | f1           | 0.964519141   | NULL |
| EVAL         | macro        | auc          | 0.9991277911  | NULL |
| EVAL         | weighted     | precision    | 0.9703703704  | NULL |
| EVAL         | weighted     | recall       | 0.9666666667  | NULL |
| EVAL         | weighted     | f1           | 0.966853408   | NULL |
| EVAL         | weighted     | auc          | 0.9991826156  | NULL |
| EVAL         | NULL         | log_loss     | 0.06365200147 | NULL |
+--------------+--------------+--------------+---------------+------+
```

Copy code

```
CALL model_multiclass!SHOW_CONFUSION_MATRIX();
```

```
+--------------+-----------------+-----------------+-------+------+
| DATASET_TYPE | ACTUAL_CLASS    | PREDICTED_CLASS | COUNT | LOGS |
|--------------+-----------------+-----------------+-------+------|
| EVAL         | add_to_wishlist | add_to_wishlist |    16 | NULL |
| EVAL         | add_to_wishlist | not_interested  |     0 | NULL |
| EVAL         | add_to_wishlist | purchase        |     0 | NULL |
| EVAL         | not_interested  | add_to_wishlist |     2 | NULL |
| EVAL         | not_interested  | not_interested  |    20 | NULL |
| EVAL         | not_interested  | purchase        |     0 | NULL |
| EVAL         | purchase        | add_to_wishlist |     0 | NULL |
| EVAL         | purchase        | not_interested  |     0 | NULL |
| EVAL         | purchase        | purchase        |    22 | NULL |
+--------------+-----------------+-----------------+-------+------+
```

Note

For information on threshold metrics, see [SHOW\_THRESHOLD\_METRICS](/sql-reference/classes/classification/methods/show_threshold_metrics).

We can also review feature importance.

Copy code

```
CALL model_multiclass!SHOW_FEATURE_IMPORTANCE();
```

```
+------+---------------------+---------------+---------------+
| RANK | FEATURE             |         SCORE | FEATURE_TYPE  |
|------+---------------------+---------------+---------------|
|    1 | USER_RATING         | 0.9186571982  | user_provided |
|    2 | USER_INTEREST_SCORE | 0.08134280181 | user_provided |
+------+---------------------+---------------+---------------+
```

## Model Roles and Usage Privileges

Each classification model instance includes two model roles, `mladmin` and `mlconsumer`. These roles are scoped to the
model itself: `model!mladmin` and `model!mlconsumer`. The owner of the model object (initially, its creator) is
automatically granted the `model!mladmin` and `model!mlconsumer` roles, and can grant these roles to account roles
and database roles.

The `mladmin` role permits usage of all APIs invocable from the model object, including but not limited to prediction
methods and evaluation methods. The `mlconsumer` role permits usage only on prediction APIs, not other exploratory
APIs.

The following SQL example illustrates the grant of classification model roles to other roles. The role `r1` can create
a classification model, and grants the role `r2` the `mlconsumer` privilege so that the `r2` can call that model’s
PREDICT method. Then `r1` grants the `mladmin` role to another role, `r3`, so `r3` can call all methods of the
model.

First, role `r1` creates a model object, making `r1` the owner of the model `model`.

Copy code

```
USE ROLE r1;
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION model(
    INPUT_DATA => SYSTEM$REFERENCE('TABLE', 'test_classification_dataset'),
    TARGET_COLNAME => 'LABEL'
);
```

You can see by executing the statements below that the role `r2` cannot call the model’s PREDICT method.

Copy code

```
USE ROLE r2;
SELECT model!PREDICT(1);    -- privilege error
```

Next, `r1` grants `r2` the `mlconsumer` instance role, after which `r2` can call the model’s PREDICT method.

Copy code

```
USE ROLE r1;
GRANT SNOWFLAKE.ML.CLASSIFICATION ROLE model!mlconsumer TO ROLE r2;

USE ROLE r2;
CALL model!PREDICT(
    INPUT_DATA => system$query_reference(
    'SELECT {*} FROM test_classification_dataset')
);
```

Similarly, role `r3` cannot see the model’s evaluation metrics without the `mladmin` instance role.

Copy code

```
USE ROLE r3;
CALL model!SHOW_EVALUATION_METRICS();   -- privilege error
```

Role `r1` grants the required role to `r3`, and `r3` can then call the model’s SHOW\_EVALUATION\_METRICS method.

Copy code

```
USE ROLE r1;
GRANT SNOWFLAKE.ML.CLASSIFICATION ROLE model!mladmin TO ROLE r3;

USE ROLE r3;
CALL model!SHOW_EVALUATION_METRICS();
```

You can revoke the privileges as follows.

Copy code

```
USE ROLE r1;
REVOKE SNOWFLAKE.ML.CLASSIFICATION ROLE model!mlconsumer FROM ROLE r2;
REVOKE SNOWFLAKE.ML.CLASSIFICATION ROLE model!mladmin FROM ROLE r3;
```

Use the following commands to see which account roles and database roles have been granted each of these instance roles.

Copy code

```
SHOW GRANTS TO SNOWFLAKE.ML.CLASSIFICATION ROLE <model_name>!mladmin;
SHOW GRANTS TO SNOWFLAKE.ML.CLASSIFICATION ROLE <model_name>!mlconsumer;
```

## Understanding Evaluation Metrics

Metrics measure how accurately a model predicts new data. The Snowflake classification currently evaluates models by selecting a
random sample from the entire dataset. A new model is trained without these rows, and then the rows are used as inference input.
The random sample portion can be configured using the `test_fraction` key in the EVALUATION\_CONFIG object.

### Metrics in `show_evaluation_metrics`

`show_evaluation_metrics` calculates the following values for each class. See
[SHOW\_EVALUATION\_METRICS](/sql-reference/classes/classification/methods/show_evaluation_metrics).

- *Positive Instances*: Instances of data (rows) that belong to the class of interest or the class being predicted.
- *Negative Instances*: Instances of data (rows) that do not belong to the class of interest or are the opposite of what is being predicted.
- *True Positives (TP)*: Correct predictions of positive instances.
- *True Negatives (TN)*: Correct predictions of negative instances,
- *False Positives (FP)*: Incorrect predictions of positive instances
- *False Negatives (FN)*: Incorrect predictions of negative instances.

Using the values above, the following metrics are reported for each class. For each metric, a higher value indicates a
more predictive model.

- *Precision*: The ratio of true positives to the total predicted positives. It measures how many of the predicted
  positive instances are actually positive.
- *Recall (Sensitivity)*: The ratio of true positives to the total actual positives. It measures how many of the actual
  positive instances were correctly predicted.
- *F1 Score*: The harmonic mean of precision and recall. It provides a balance between precision and recall, especially
  when there is an uneven class distribution.

### Metrics in `show_global_evaluation_metrics`

`show_global_evaluation_metrics` calculates overall (global) metrics for all classes predicted by the model by averaging the per-class metrics
calculated by `show_evaluation_metrics`. See
[SHOW\_GLOBAL\_EVALUATION\_METRICS](/sql-reference/classes/classification/methods/show_global_evaluation_metrics).

Currently, `macro` and `weighted` averaging is used for the metrics Precision, Recall, F1, AUC.

Logistic Loss (LogLoss) is calculated for the model as a whole. The objective of prediction is to minimize the loss
function.

### Metrics in `show_threshold_metrics`

`show_threshold_metrics` provides raw counts and metrics for a specific threshold for each class. This can be used to
plot ROC and PR curves or do threshold tuning if desired. The threshold varies from 0 to 1 for each specific class; a
predicted probability is assigned. See [SHOW\_THRESHOLD\_METRICS](/sql-reference/classes/classification/methods/show_threshold_metrics).

The sample is classified as belonging to a class if the predicted probability of being in that class exceeds the
specified threshold. The true and false positives and negatives are computed considering the negative class as
every instance that does not belong to the class being considered. The following metrics are then computed.

- *True positive rate (TPR)*: The proportion of actual positive instances that the model correctly identifies (equivalent to Recall).
- *False positive rate (FPR)*: The proportion of actual negative instances that were incorrectly predicted as positive.
- *Accuracy*: The ratio of correct predictions (both true positives and true negatives) to the total number of
  predictions, an overall measure of how well the model is performing. This metric can be misleading in
  unbalanced cases.
- *Support*: The number of actual occurrences of a class in the specified dataset. Higher support values indicate a larger
  representation of a class in the dataset. Support is not itself a metric of the model but a characteristic of the dataset.

### Confusion Matrix in `show_confusion_matrix`

The confusion matrix is a table used to assess the performance of a model by comparing predicted and actual values and
evaluating its ability to correctly identify positive and negative instances. The objective is to maximize the number of
instances on the diagonal of the matrix while minimizing the number of off-diagonal instances. See
[SHOW\_CONFUSION\_MATRIX](/sql-reference/classes/classification/methods/show_confusion_matrix).

You can visualize the confusion matrix in Snowsight as follows.

Copy code

```
CALL model_binary!SHOW_CONFUSION_MATRIX();
```

The results look like the following.

```
+--------------+--------------+-----------------+-------+------+
| DATASET_TYPE | ACTUAL_CLASS | PREDICTED_CLASS | COUNT | LOGS |
|--------------+--------------+-----------------+-------+------|
| EVAL         | false        | false           |    37 | NULL |
| EVAL         | false        | true            |     1 | NULL |
| EVAL         | true         | false           |     0 | NULL |
| EVAL         | true         | true            |    22 | NULL |
+--------------+--------------+-----------------+-------+------+
```

To visualize the confusion matrix, click on **Chart**, then **Chart Type**, then **Heatgrid**. Under Data, for
**Cell values** select NONE, for **Rows** select PREDICTED\_CLASS, and for **Columns** select ACTUAL\_CLASS. The
result appears similar to the figure below.

![The confusion matrix of a comparison model](/static/images/screens/cortex-classification-confusion-matrix.png)

## Understanding Feature Importance

A classification model can explain the relative importance of all features used in the model, This information is useful
in understanding what factors are really influencing your data.

The [SHOW\_FEATURE\_IMPORTANCE](/sql-reference/classes/classification/methods/show_feature_importance) method counts
the number of times the model’s trees used each feature to make a decision. These feature importance scores are then
normalized to values between 0 and 1 so that their sum is 1. The resulting scores represent an approximate ranking of
the features in your trained model.

Features that are close in score have similar importance. Using multiple features that are very similar to each other
may result in reduced importance scores for those features.

### Limitations

- You cannot choose the technique used to calculate feature importance.
- Feature importance scores can be helpful for gaining intuition about which features are important to your model’s
  accuracy, but the actual values should be considered estimates.

### Example

Copy code

```
CALL model_binary!SHOW_FEATURE_IMPORTANCE();
```

```
+------+---------------------+---------------+---------------+
| RANK | FEATURE             |         SCORE | FEATURE_TYPE  |
|------+---------------------+---------------+---------------|
|    1 | USER_RATING         | 0.9295302013  | user_provided |
|    2 | USER_INTEREST_SCORE | 0.07046979866 | user_provided |
+------+---------------------+---------------+---------------+
```

## Cost Considerations

Training and using classification models incurs compute and storage costs.

Using any APIs from the Classification feature (training a model, predicting with the model, retrieving metrics) all
require an active warehouse. The compute cost of using Classification functions is charged to the warehouse. See
[Understanding Compute Cost](/user-guide/cost-understanding-compute) for general information on Snowflake compute
costs.

For details on costs for using ML functions in general, see [Cost Considerations](/guides-overview-ml-functions#label-ml-functions-costs) in the ML functions overview.
