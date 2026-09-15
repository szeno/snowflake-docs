# Creating or connecting to a feature store

Create a feature store or connect to an existing feature store by using the `FeatureStore` constructor, providing a
Snowpark session, database name, feature store name, and default warehouse name. The `mode` parameter determines
whether the feature store is created if it does not already exist.

| Mode | Description |
| --- | --- |
| `CreationMode.FAIL_IF_NOT_EXIST` | Throws an exception if the specified feature store does not exist. Default. |
| `CreationMode.CREATE_IF_NOT_EXIST` | Creates the feature store if it does not exist. |

Expand

Show lessSee more

To create a feature store, use the `CreationMode.CREATE_IF_NOT_EXIST` mode when instantiating `FeatureStore`.
Creating a feature store creates a schema in the specified database with the specified feature store name. Generally,
an administrator role will create the feature store schema and corresponding roles.

You can subsequently connect to the existing feature store by using the default mode, `CreationMode.FAIL_IF_NOT_EXIST`.

The following Python code creates a feature store:

Copy code

```
from snowflake.ml.feature_store import FeatureStore, CreationMode

fs = FeatureStore(
        session=session,
        database="MY_DB",
        name="MY_FEATURE_STORE",
        default_warehouse="MY_WH",
        creation_mode=CreationMode.CREATE_IF_NOT_EXIST,
     )
```

Tip

Storing your feature stores in a dedicated database will make it simpler to [replicate them](/developer-guide/snowflake-ml/feature-store/replication-sharing).

After you have created a feature store, use code like the following to access it:

Copy code

```
from snowflake.ml.feature_store import FeatureStore, CreationMode

fs = FeatureStore(
        session=session,
        database="MY_DB",
        name="MY_FEATURE_STORE",
        default_warehouse="MY_WH",
      )
```
