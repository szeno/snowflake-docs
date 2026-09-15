# Migrate your app from ROOT\_LOCATION to FROM

To convert your Streamlit object, use [CREATE OR REPLACE STREAMLIT](/sql-reference/sql/create-streamlit)
with the FROM parameter. For simplicity, this procedure assumes you will use a warehouse runtime.
If you want to upgrade to a container runtime, you will need to alter your app code
for compatibility. See the [Migrating between runtime environments](/developer-guide/streamlit/migrations-and-upgrades/runtime-migration) page.

If your app code is compatible with a container runtime, you can modify this procedure by
adding the following parameters to your CREATE OR REPLACE STREAMLIT command:

Copy code

```
RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
COMPUTE_POOL = my_compute_pool
EXTERNAL_ACCESS_INTEGRATIONS = (pypi_access_integration)
```

To migrate your app from ROOT\_LOCATION to FROM do the following steps:

1. To identify your app’s current configuration, run the following command:

   Copy code

   ```
   DESCRIBE STREAMLIT streamlit_db.streamlit_schema.my_app;
   ```

   Replace `streamlit_db.streamlit_schema.my_app` with your Streamlit object.
2. For use in a later step, open a text editor and note the following values. Sample
   values are shown so you can identify and replace them with your values in later steps:

   | Column | Value |
   | --- | --- |
   | `name` | `my_app` |
   | `title` | `My Streamlit App` |
   | `root_location` | `@db1.schema1/my_app_folder` |
   | `main_file` | `streamlit_app.py` |
   | `query_warehouse` | `my_warehouse` |
   | `user_packages` | `streamlit==1.45.0, pandas==2.2.0` |
   | `import_urls` | `@db2.schema2/packages/package1.zip, @db3.schema3/packages/package2.zip` |
   | `external_access_integration` | `eai_name_1, eai_name_2` |
   | `external_access_secrets` | `secret1, secret2` |

   Expand

   Show lessSee more

   If your Streamlit object did not return a `root_location` column, your app
   was created using the FROM parameter and doesn’t require conversion.
3. Confirm that entrypoint file is in the root of your app’s source directory. (You can
   skip this step if you will use a container runtime.)

   The entrypoint file is specified by the `main_file` value from the previous step.
   To create an app using FROM, `main_file` must declare a file in the root of the
   source directory. If your entrypoint file is in a subdirectory, you must rearrange
   your app’s files and update your app’s code accordingly before proceeding.
4. To convert your app, use CREATE OR REPLACE STREAMLIT with the FROM parameter.

   In the simplest case, your app may have null values for `title`, `user_packages`,
   `import_urls`, `external_access_integration`, and `external_access_secrets`. In
   this case, you can run the following command, replacing the placeholders with
   your app’s values:

   Copy code

   ```
   CREATE OR REPLACE STREAMLIT my_app
   FROM '@db1.schema1/my_app_folder'
   MAIN_FILE = 'streamlit_app.py'
   QUERY_WAREHOUSE = my_warehouse;
   ```

   If your app has non-null values for any of the optional parameters, include them
   in the CREATE OR REPLACE STREAMLIT command. For example:

   Copy code

   ```
   CREATE OR REPLACE STREAMLIT my_app
   FROM '@db1.schema1/my_app_folder'
   MAIN_FILE = 'streamlit_app.py'
   TITLE = 'My Streamlit App'
   QUERY_WAREHOUSE = my_warehouse
   IMPORTS = ('@db2.schema2/packages/package1.zip', '@db3.schema3/packages/package2.zip')
   EXTERNAL_ACCESS_INTEGRATION = ('eai_name_1', 'eai_name_2')
   SECRETS = ('secret1', 'secret2');
   ```
5. If your app isn’t loading, confirm your dependencies.

   For more information about dependency management, see [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).
