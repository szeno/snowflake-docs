# Include a trained model in an app

This topic describes how to include a previously trained model in a Snowflake Native App.

## Workflow: add a model to an app

The following procedure outlines the typical workflow a provider follows to create and add
a Snowflake ML model to an app:

1. The provider develops a Snowflake ML model and logs it in the
   [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).
2. The provider exports the model artifacts from the Snowflake Model
   Registry and uploads them to
   a stage so that they are accessible to the application package.
3. The provider creates the model in the setup script of the app.
4. The app creates a model from these artifacts in the consumer account during installation
   or after an upgrade. Optionally, the app can grant access on the model to an application role.
5. The consumer uses the machine learning model if the provider configures the app to grant access to it.

Note

A provider is not required to grant access on the model to the consumer. The model can be created as an
object that the app uses internally, but is not accessible to the consumer.

## Develop a machine learning model

Providers can develop new machine learning models or include existing models in an app.

- For information about developing models, see [Snowflake ML Model Development](/developer-guide/snowflake-ml/modeling).
- For information about managing models in a Snowflake Model Registry, see
  [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).

## Export the model artifacts and upload to a stage

To include a model in an app, providers must export the model artifacts and upload them to
a stage where they are accessible to the application package.

### Manually export the model artifacts and upload them to a stage

1. Download the model artifacts. See [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview)
2. Use one of the following methods to upload the machine learning artifacts to the stage where your app resources are located:
   - To upload the files using Snowsight, see [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui).
   - To upload the files using the Snowflake CLI, use the `snow app deploy` command. See
     [How to create an application package and an application object together](/developer-guide/snowflake-cli/native-apps/create-package#label-snowcli-create-package).
   - To upload the files using SQL, see [Staging data files from a local file system](/user-guide/data-load-local-file-system-stage).

### Use a stored procedure to export the model artifacts and upload them to a stage

Providers can use the following stored procedure example as a template for automating the process of
downloading the model artifacts and uploading them to a stage:

Copy code

```
CREATE OR REPLACE PROCEDURE copy_model_artifacts_to_stage(src_registry_schema_fqn string, src_model string, src_model_version string, dst string)
  RETURNS STRING
  LANGUAGE python
  runtime_version = 3.11
  handler = 'copy_model_artifacts_to_stage'
  packages = ('snowflake-snowpark-python')
  execute as caller
as
$$

def copy_model_artifacts_to_stage(session, src_registry_schema_fqn, src_model, src_model_version, dst):
  session.use_schema(src_registry_schema_fqn)
  list_files = session.sql(f"list 'snow://model/{src_model}/versions/{src_model_version}/'")
  list_files.collect()
  for row in list_files.toLocalIterator():
     parts = row["name"].rsplit('/', 1)
     directory = parts[0]
     filename = parts[1]
     session.file.get(f"snow://model/{src_model}/{directory}/{filename}", f"/tmp/{directory}")
     session.file.put(f"/tmp/{directory}/{filename}", f"{dst}/{src_model}/{directory}", auto_compress=False, overwrite=True, source_compression="NONE")

  return f"Copied [snow://model/{src_model}/versions/{src_model_version}/*] to [{dst}/{src_model}/{directory}/]"
$$;

CALL copy_model_artifacts_to_stage('my_db.my_model_registry', 'my_model', 'V1', '@my_app_pkg.source_schema.source_stage/models');
```

## Create the model objects in the consumer account

To create the model objects in the consumer account, the provider adds the necessary
SQL commands to the setup script as shown in the following example:

Copy code

```
CREATE APPLICATION ROLE IF NOT EXISTS app_user;

CREATE OR ALTER VERSIONED SCHEMA app_code;
GRANT USAGE ON SCHEMA app_code TO APPLICATION ROLE app_user;

CREATE OR REPLACE MODEL app_code.my_model FROM '/models/my_model/versions/V1';
```

Optionally, providers can grant access on the model to consumers by granting the
USAGE privilege on the model to an application role:

Copy code

```
GRANT USAGE ON MODEL app_code.my_model TO APPLICATION ROLE app_user;
```

## Access the model within the app

To use the model internally as part of the app, providers add a SELECT statement
to the setup script as shown in the following example:

Copy code

```
SELECT app_code.my_model!predict(...);
```

## Use the model as a consumer

If a provider grants the USAGE privilege on the model to a consumer, the consumer can run the
following command to access the model:

Copy code

```
SELECT app_code.my_model!predict(...);
```

To run this command, consumers must use a role that has one of the following:

- The USAGE privilege granted on the model.
- The OWNERSHIP privilege on the application object.
