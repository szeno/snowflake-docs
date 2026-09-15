# Add a Streamlit app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to include a [Streamlit](https://streamlit.io/) app within a Snowflake Native App.

## About Streamlit and the Snowflake Native App Framework

[Streamlit](https://streamlit.io/) is an open-source Python library that makes it easy to create
and share custom web apps for machine learning and data science. By using Streamlit you can quickly
build and deploy powerful data applications.

For information about the open-source library, see the [Streamlit Library documentation](https://docs.streamlit.io/).

Within the Snowflake Native App Framework you can use Streamlit to perform the following:

- Create a front-end web app that enables consumers to visualize the data provided by your Snowflake Native App.
- Create a user interface that allows consumers to grant privileges and create references to objects within
  their account that are used by the Snowflake Native App.

  See [Create and access objects in a consumer account](/developer-guide/native-apps/requesting-about) for more information.

Note

See [Unsupported Streamlit Features](#label-streamlit-unsupported-features-na) for information on unsupported Streamlit features.

### Considerations for warehouses when using Streamlit in a Snowflake Native App

Streamlit apps in a Snowflake Native App run using a Snowflake warehouse. The same warehouse considerations apply to both
Streamlit in Snowflake and Streamlit in a Snowflake Native App. See [Guidelines for selecting resources in Streamlit in Snowflake](/developer-guide/streamlit/app-development/runtime-environments#label-streamlit-guidelines-wh) for more information.

Note

Streamlit apps in a Snowflake Native App support the [USE WAREHOUSE](/sql-reference/sql/use-warehouse) command. However, references to warehouses
are not supported.

## Supported versions of the Streamlit library

The Snowflake Native App Framework supports the same versions of the Streamlit library as Streamlit in Snowflake. For more
information, see [Supported versions of the Streamlit library in warehouse runtimes](/developer-guide/streamlit/app-development/dependency-management#label-streamlit-supported-streamlit-versions-on-warehouses).

Support for newer versions of the Streamlit library will be included as they are released.

See [Set the Streamlit version for an app](#label-streamlit-set-version-na) for information on how to set the version for a Streamlit app.

## Supported external packages

By default, a Streamlit app that is included within a Snowflake Native App includes the `python`, `streamlit`,
and `snowflake-snowpark-python` packages pre-installed in the consumer environment. The consumer environment
also has access to the dependencies required by these packages.

## Unsupported Streamlit Features

The following Streamlit features are not currently supported when using Streamlit in a
Snowflake Native App:

- Custom components are not supported.
- Using [Azure Private Link](/user-guide/privatelink-azure) and
  [Google Cloud Private Service Connect](/user-guide/private-service-connect-google) to access a Streamlit app is
  not supported.

- [st.bokeh\_chart](https://docs.streamlit.io/library/api-reference/charts/st.bokeh_chart)
- [st.cache\_data](https://docs.streamlit.io/library/api-reference/performance/st.cache_data)
- [st.cache\_resource](https://docs.streamlit.io/library/api-reference/performance/st.cache_resource)
- [st.camera\_input](https://docs.streamlit.io/library/api-reference/widgets/st.camera_input)
- [st.download\_button](https://docs.streamlit.io/library/api-reference/widgets/st.download_button) (only supported in Streamlit version 1.26 or later)
- [st.file\_uploader](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader)
- [st.image](https://docs.streamlit.io/library/api-reference/media/st.image)
- [st.pyplot](https://docs.streamlit.io/library/api-reference/charts/st.pyplot)
- [st.scatter\_chart](https://docs.streamlit.io/library/api-reference/charts/st.scatter_chart)
- [st.set\_page\_config](https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config)

> The `page_title` and `page_icon` properties of the
> [st.set\_page\_config](https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config)
> command are not supported.

- [st.video](https://docs.streamlit.io/library/api-reference/media/st.video)
- [Custom Components](https://docs.streamlit.io/library/components), including:

> - [component.html()](https://docs.streamlit.io/library/components/components-api#stcomponentsv1html)
> - [component.iframe()](https://docs.streamlit.io/library/components/components-api#stcomponentsv1iframe)

- [Configuration files](https://docs.streamlit.io/library/advanced-features/configuration)
- The following experimental features:

> - [st.experimental\_set\_query\_params](https://docs.streamlit.io/library/api-reference/utilities/st.experimental_set_query_params)
> - [st.experimental\_get\_query\_params](https://docs.streamlit.io/library/api-reference/utilities/st.experimental_get_query_params)

- Network access via the internet
- Anchor links

## Workflow to add a Streamlit app to a Snowflake Native App

The following workflow describes how to add a Streamlit app to a Snowflake Native App:

1. Develop your native app.

   This includes adding the data content that you want consumers to access using Streamlit. See
   [Snowflake Native App Framework workflow](/developer-guide/native-apps/native-apps-workflow) for more information.
2. Review the following sections to understand the supported version of the Streamlit library and
   unsupported features:

   - [Supported versions of the Streamlit library](#label-streamlit-supported-version-na)
   - [Unsupported Streamlit Features](#label-streamlit-unsupported-features-na)
   - [Supported external packages](#label-streamlit-supported-external-packages-na)
3. Develop a Streamlit app.

   See the [Streamlit Library documentation](https://docs.streamlit.io/) for information on using the
   Streamlit open-source library.
4. Create a local directory structure for the Streamlit app.

   See [Example directory structure for a Streamlit app](#label-streamlit-example-dir-structure) for recommendations on how to organize your Streamlit
   files within the structure of your app.
5. Add a CREATE STREAMLIT statement to the setup script.

   When running the [CREATE APPLICATION](/sql-reference/sql/create-application) command, the setup script runs
   the [CREATE STREAMLIT](/sql-reference/sql/create-streamlit) statement to create a Streamlit object. This object
   contains the schema and Python files required by the Streamlit app.
6. Configure the `environment.yml` file to include additional libraries in your Streamlit app.

   See [Add additional packages to a Streamlit app](#label-streamlit-add-packages-na) for more information.
7. Optional: Add the Streamlit object name as an entry in the manifest
   file to display the Streamlit
   app as the default app in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).

   See [Add a Streamlit app to the manifest file](#label-streamlit-add-to-manifest) for more information.
8. Upload the Streamlit files, `environment.yml` file, setup
   script, and manifest file.
   files to a named stage. To include Streamlit code files in an application package, the files must be
   uploaded to a named stage.
9. Test the application package.

   After creating the files required by the application package and Streamlit app, create an application
   object to test the setup script and manifest file.

   See [Test the application package containing the Streamlit app](#label-streamlit-test-app-package-na) for more information.
10. View the Streamlit app in Snowsight.

To test the Streamlit app, view the app in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). See
[Test the Streamlit app in Snowsight](#label-streamlit-test-streamlit-na).

## Example directory structure for a Streamlit app

Like other Python modules, to add a Streamlit app to an application package you must upload
your Streamlit code files to a named stage. See [PUT](/sql-reference/sql/put) for information
on how to upload files to a stage.

To account for multiple versions of a Snowflake Native App, consider using a directory structure similar to the following
to maintain your Streamlit apps and related application files:

Copy code

```
@test.schema1.stage1:
└── /
    ├── manifest.yml
    ├── readme.md
    ├── scripts/setup_script.sql
    └── code_artifacts/
        └── streamlit/
            └── environment.yml
            └── streamlit_app.py
```

Note that the directory structure you create depends on the requirements of your app and
development environment.

Note

The `environment.yml` file must be at the same level as your main file of your Streamlit app.

See [Reference external code files](/developer-guide/native-apps/adding-application-logic#label-native-apps-reference-app-files) for more information on relative paths.

## Create the Streamlit object in the setup script

The following example shows how to use [CREATE STREAMLIT](/sql-reference/sql/create-streamlit) within the setup
script of an app.

Copy code

```
CREATE OR REPLACE STREAMLIT app_schema.my_test_app_na
     FROM '/code_artifacts/streamlit'
     MAIN_FILE = '/streamlit_app.py';

GRANT USAGE ON SCHEMA APP_SCHEMA TO APPLICATION ROLE app_public;
GRANT USAGE ON STREAMLIT APP_SCHEMA.MY_TEST_APP_NA TO APPLICATION ROLE app_public;
```

This example creates a Streamlit object within a schema named `app_schema`.
The [CREATE STREAMLIT](/sql-reference/sql/create-streamlit) command uses the Streamlit app specified by the
MAIN\_FILE clause. The directory location is specified by the value of the FROM clause.

See [Example directory structure for a Streamlit app](#label-streamlit-example-dir-structure) for information on creating the directory
structure for a Streamlit app within an application package.

This example also grants the required privileges on the schema and Streamlit object to an
application role.

## Add additional packages to a Streamlit app

Use the `environment.yml` file to add additional Python packages to a Streamlit app. For
example, to add the `scikit-learn` library to a Streamlit app, add the following to the
`environment.yml` file:

Copy code

```
name: sf_env
channels:
- snowflake
dependencies:
- scikit-learn
```

The `name` and `channels` properties are both required.

Also, the `- snowflake` key is required under the `channels` property. This indicates the
[Snowflake Anaconda Channel](https://repo.anaconda.com/pkgs/snowflake/).

Note

You can only install packages listed in the
[Snowflake Anaconda Channel](https://repo.anaconda.com/pkgs/snowflake/).
Snowflake does not support external Anaconda channels in Streamlit.

## Set the Streamlit version for an app

The Snowflake Native App Framework supports multiple versions of the Streamlit library. To set the Streamlit version within
a Snowflake Native App add `streamlit` to the `dependencies` section of the `environment.yml` file
as shown in the following example:

Copy code

```
name: sf_env
channels:
- snowflake
dependencies:
- streamlit=1.35.0
```

Snowflake recommends explicitly setting the Streamlit version for your app. However, currently, if you
do not explicitly set the version of the Streamlit library, Streamlit version 1.22.0 is set as the default.

## Add a Streamlit app to the manifest file

To specify the default Streamlit app launched by your app, add the following entries in the manifest file:

Copy code

```
artifacts:
  ...
  default_streamlit: app_schema.streamlit_app_na
  ...
```

The `default_streamlit: app_schema.streamlit_app_na` entry specifies the location of the
schema containing your Streamlit app.

## Test the application package containing the Streamlit app

To test the application package containing the Streamlit app, create an application object using
the files on a named stage by running the [CREATE APPLICATION](/sql-reference/sql/create-application) as shown
in the following example:

> Copy code
>
> ```
> CREATE APPLICATION hello_snowflake_app
>   FROM APPLICATION PACKAGE hello_snowflake_package
>   USING '@hello_snowflake_code.core.hello_snowflake_stage';
> ```

Depending on what you need to test, you can create the application object using other
forms of the [CREATE APPLICATION](/sql-reference/sql/create-application). For example, you may want to
test the Streamlit app as part of a version or upgrade. See
[Install and test an app locally](/developer-guide/native-apps/installing-testing-application).

## Test the Streamlit app in Snowsight

To test the Streamlit app, view the app in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) by doing the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the Streamlit app you want to view.

   The main Streamlit app opens in the Snowsight.
4. Optional: If you are viewing a multipage Streamlit app, select a tab to view additional pages.

## Troubleshoot a Streamlit app in the Snowflake Native App Framework

If the app displays an unknown error, make sure you have tried the solutions described in the following
sections.

### Acknowledge the Terms of Service

To use Streamlit and packages provided by Anaconda in Snowflake, you must acknowledge the
[External Offerings Terms](https://www.snowflake.com/legal/external-offering-terms/).
To learn more, see [Using third-party packages from Anaconda](/developer-guide/udf/python/udf-python-packages#label-python-udfs-anaconda-terms).

### Firewall allowlisting

Each Streamlit app uses a unique subdomain. If you use strict firewalls, add \*.snowflake.app
to your firewall allowlist. Adding this entry to your allowlist allows your apps to communicate with
Snowflake servers without any restrictions.
