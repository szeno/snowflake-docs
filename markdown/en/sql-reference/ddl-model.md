# Machine learning model DDL

The following DDL commands are used to create, view, and manage machine-learning models and their versions.

A model is a schema-level object that contains a machine learning model that has been trained and stored in the Snowpark
ML Registry. Model commands let you create and manage models in SQL. You can also create and manage models in Python
using the Snowpark ML Registry API.

Model monitors allow you to monitor the performance of machine learning models you have deployed in Snowflake.

## Machine learning models

|  |  |
| --- | --- |
| [CREATE MODEL](/sql-reference/sql/create-model) | Creates a new machine learning model in the current/specified schema or replaces an existing model. |
| [ALTER MODEL](/sql-reference/sql/alter-model) | Modifies the properties for an existing model, including its name, tags, default version, or comment. |
| [SHOW MODELS](/sql-reference/sql/show-models) | Lists the machine learning models that you have privileges to access. |
| [DROP MODEL](/sql-reference/sql/drop-model) | Removes a machine learning model from the current/specified schema. |

Expand

Show lessSee more

## Machine learning model versions

|  |  |
| --- | --- |
| [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version) | Adds a new version to an existing model from an internal stage. |
| [ALTER MODEL … DROP VERSION](/sql-reference/sql/alter-model-drop-version) | Removes a version from an existing model. |
| [ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version) | Modifies a version of a model, changing the version’s comment or metadata. |
| [SHOW VERSIONS IN MODEL](/sql-reference/sql/show-versions-in-model) | Lists the versions in a machine learning model. |

Expand

Show lessSee more

## Machine learning model functions

|  |  |
| --- | --- |
| [SHOW FUNCTIONS IN MODEL](/sql-reference/sql/show-functions-in-model) | Shows the models (methods) attached to a machine learning model. |

Expand

Show lessSee more

## Machine learning model monitors

|  |  |
| --- | --- |
| [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor) | Create a new model monitor. |
| [ALTER MODEL MONITOR](/sql-reference/sql/alter-model-monitor) | Modify the properties of an existing model monitor, including its refresh interval and warehouse, or suspend or resume it. |
| [SHOW MODEL MONITORS](/sql-reference/sql/show-model-monitors) | Lists the model monitors that you have privileges to access. |
| [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor) | Shows the properties of a model monitor. |
| [DROP MODEL MONITOR](/sql-reference/sql/drop-model-monitor) | Removes a model monitor from the current/specified schema. |

Expand

Show lessSee more
