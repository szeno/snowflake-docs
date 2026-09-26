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

See [Unsupported Streamlit features](#label-streamlit-unsupported-features-na) for information on unsupported Streamlit features.

## Choose a runtime for your Streamlit app

Streamlit in Snowflake offers two runtime environments, and both are available inside a Snowflake Native App:

- **Warehouse runtime**: Runs your app code on a virtual warehouse and creates a personal
  instance of the app for each viewer. Generally available.
- **Container runtime**: Runs your app code as a long-running Snowpark Container Services service on a compute pool that
  the app creates in the consumer account. All viewers share one instance of the app.

Note

Container runtimes for Streamlit apps in a Snowflake Native App are in preview. See
[Container runtime](#label-streamlit-container-runtime-na).

The following table summarizes the differences that matter most when you choose a runtime for a
Streamlit app inside a Snowflake Native App. For a general comparison of the two runtimes that isn’t
specific to the Snowflake Native App Framework, see [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).

| Consideration | Warehouse runtime | Container runtime |
| --- | --- | --- |
| Release stage | Generally available. | Preview. |
| Compute for app code | A virtual warehouse. | A [compute pool](/developer-guide/native-apps/container-compute-pool) that the app creates and owns in the consumer account. |
| Compute for queries | The same warehouse that runs the app code, unless the app activates a different warehouse. | A virtual warehouse, separate from the compute pool that runs the app code. |
| Consumer privileges the app must request | None specific to Streamlit. | `CREATE COMPUTE POOL` and `BIND SERVICE ENDPOINT`, plus `CREATE WAREHOUSE` if the app creates its query warehouse and `CREATE EXTERNAL ACCESS INTEGRATION` if the app installs Python packages. Granted automatically with `manifest_version: 2`. |
| Python packages | Packages from the [Snowflake Anaconda Channel](https://repo.anaconda.com/pkgs/snowflake/) via `environment.yml`. | Packages from PyPI via `requirements.txt` or `pyproject.toml`. Requires an external access integration if using Permission SDK. |
| Streamlit library versions | A limited selection of versions, starting at 1.22. | Any version supported by the container runtime, starting at 1.50. |
| Query execution rights | Owner’s rights only. | Owner’s rights, plus optional [restricted caller’s rights](/developer-guide/native-apps/restricted-callers-rights). |
| Warehouse selection | Consumers may be prompted to select a warehouse when they open the app. | Consumers aren’t prompted. The warehouse selector doesn’t affect the app’s SQL. |

Expand

Show lessSee more

## Supported versions of the Streamlit library

The Snowflake Native App Framework supports the same versions of the Streamlit library as Streamlit in Snowflake. For more
information, see [Supported versions of the Streamlit library in warehouse runtimes](/developer-guide/streamlit/app-development/dependency-management#label-streamlit-supported-streamlit-versions-on-warehouses).

Support for newer versions of the Streamlit library will be included as they are released.

See [Set the Streamlit version for an app](#label-streamlit-set-version-na) for information on how to set the version for a Streamlit app.

If your app uses a container runtime, you don’t need to declare `streamlit` in your
`requirements.txt` file. The container image already includes it.

## Supported external packages

By default, a Streamlit app that is included within a Snowflake Native App includes the `python`, `streamlit`,
and `snowflake-snowpark-python` packages pre-installed in the consumer environment. The consumer environment
also has access to the dependencies required by these packages.

- A warehouse runtime can add packages only from the
  [Snowflake Anaconda Channel](https://repo.anaconda.com/pkgs/snowflake/).
- A container runtime can add
  packages from PyPI, but doing so requires an external access
  integration. See [Specify Python packages](#label-streamlit-container-packages-na).

## Unsupported Streamlit features

Unsupported Streamlit features depend on the runtime. The following additional restrictions apply
when using Streamlit in a Snowflake Native App:

- Custom components are not supported.
- Using [Azure Private Link](/user-guide/privatelink-azure) and
  [Google Cloud Private Service Connect](/user-guide/private-service-connect-google) to access a Streamlit app is
  not supported.

### Warehouse runtime unsupported features

The following list applies only to Streamlit apps that use a warehouse runtime in a Snowflake Native App:

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

### Container runtime unsupported features

For general Streamlit feature limitations with a container runtime, see
[Unsupported Streamlit features](/developer-guide/streamlit/limitations#label-streamlit-unsupported-features)
and [Limitations and changes that vary by runtime](/developer-guide/streamlit/limitations#label-streamlit-runtime-limitations). The warehouse-runtime
list doesn’t apply to container-runtime apps. Native App-specific restrictions still apply.

A container runtime supports network access via the internet when you attach an external access
integration to the Streamlit object. For limitations that are specific to container runtimes in an
app, see [Limitations for container runtimes in an app](#label-streamlit-container-limitations-na).

## Warehouse runtime

A warehouse runtime provides an on-demand, personal instance of the Streamlit app for each viewer.
Streamlit apps that use a warehouse runtime run on a Snowflake warehouse. The same warehouse
considerations apply to both Streamlit in Snowflake and Streamlit in a Snowflake Native App. See
[Guidelines for selecting resources in Streamlit in Snowflake](/developer-guide/streamlit/app-development/runtime-environments#label-streamlit-guidelines-wh) for more information.

Note

Streamlit apps in a Snowflake Native App support the [USE WAREHOUSE](/sql-reference/sql/use-warehouse) command. However, references to warehouses
are not supported.

### Workflow to add a Streamlit app to a Snowflake Native App

The following workflow describes how to add a warehouse-runtime Streamlit app to a Snowflake Native App:

1. Develop your native app.

   This includes adding the data content that you want consumers to access using Streamlit. See
   [Snowflake Native App Framework workflow](/developer-guide/native-apps/native-apps-workflow) for more information.
2. Review the following sections to understand the supported version of the Streamlit library and
   unsupported features:

   - [Supported versions of the Streamlit library](#label-streamlit-supported-version-na)
   - [Unsupported Streamlit features](#label-streamlit-unsupported-features-na)
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

### Example directory structure for a Streamlit app

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

### Create the Streamlit object in the setup script

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

### Add additional packages to a Streamlit app

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

### Set the Streamlit version for an app

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

## Container runtime

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

A container runtime serves your Streamlit app as a long-running Snowpark Container Services service. Instead of creating
a separate instance of the app for each viewer, the app runs once on a compute pool and all viewers
connect to the same instance. Viewers connect to an app that’s already live, so they don’t wait for
the app to start.

Use a container runtime for a Streamlit app in a Snowflake Native App when you want to do any of the following:

- Install Python packages from PyPI or another external package index instead of being limited to the
  Snowflake Anaconda Channel.
- Query consumer data on behalf of the viewer with
  [restricted caller’s rights](/developer-guide/native-apps/restricted-callers-rights).

A container-runtime Streamlit app in a Snowflake Native App runs on a compute pool that the app creates and
owns in the consumer account. It can’t use the consumer account’s default Streamlit compute pool. The
app declares the privileges it needs to create that pool in its manifest file, and Snowflake grants
them automatically when the manifest version is 2. See [Size and manage the compute pool](#label-streamlit-container-pool-na).

### Convert a Streamlit app to a container runtime

To move a Streamlit app in a Snowflake Native App from a warehouse runtime to a container runtime, review the
following changes:

1. **Declare the privileges.** Set `manifest_version` to `2` and declare the privileges the app needs
   to create a compute pool and query warehouse. See [Declare privileges in the manifest file](#label-streamlit-container-privileges-na).
2. **Create the compute resources and declare the runtime.** Add the `RUNTIME_NAME`, `COMPUTE_POOL`,
   and `QUERY_WAREHOUSE` parameters to the `CREATE STREAMLIT` statement, and create the pool and
   warehouse first. See [Create the compute resources and Streamlit object in the setup script](#label-streamlit-container-create-na).
3. **Replace the dependency file.** Replace `environment.yml` with `requirements.txt` or
   `pyproject.toml`, and use PyPI package names instead of Conda package names. See
   [Specify Python packages](#label-streamlit-container-packages-na).
4. **Add external access if you install packages.** If your dependency file lists any package at
   all, the container needs access to the package index, which requires an external access
   integration and consumer approval. See [Allow access to a package index](#label-streamlit-container-eai-na).
5. **Review your app code for container-runtime compatibility.** If your code uses
   `get_active_session()`, replace it with `st.connection("snowflake").session()`. Review shared state
   for thread safety because the container runtime serves multiple viewers concurrently. For more
   information, see [Migrating between runtime environments](/developer-guide/streamlit/migrations-and-upgrades/runtime-migration).

Your permission callbacks and object references are unchanged by the runtime switch.

### Example directory structure for a container-runtime Streamlit app

The directory structure is the same as for a warehouse runtime, except that the dependency file is
`requirements.txt` or `pyproject.toml` instead of `environment.yml`:

Copy code

```
@myapp_package.app_code.app_stage:
└── /
    ├── manifest.yml
    ├── setup.sql
    └── code_artifacts/
        └── streamlit/
            ├── requirements.txt
            └── streamlit_app.py
```

The FROM clause of the CREATE STREAMLIT statement must use a path relative to the root directory of
the application package stage, such as `'/code_artifacts/streamlit'`. Snowflake resolves the
relative path against the application package stage and copies the files into a stage that it
manages for the Streamlit object.

Important

For a container runtime, you must use the FROM clause. The ROOT\_LOCATION parameter isn’t supported.

The dependency file must be in the same directory as the main file of your Streamlit app, or in a
parent directory of it. This is more permissive than a warehouse runtime, which requires the
`environment.yml` file to be in the same directory as the main file.

### Declare privileges in the manifest file

Set `manifest_version` to `2` and declare the privileges that the app needs to create and use its
compute pool and query warehouse. With `manifest_version: 2`, Snowflake grants these privileges to the
app automatically during installation and upgrade, so the setup script can create these resources
directly.

Copy code

```
manifest_version: 2

artifacts:
  setup_script: setup.sql
  default_streamlit: core.app_ui

privileges:
  - CREATE COMPUTE POOL:
      description: "Creates the compute pool that runs the Streamlit app"
  - BIND SERVICE ENDPOINT:
      description: "Binds the endpoint that viewers use to reach the Streamlit app"
  - CREATE WAREHOUSE:
      description: "Creates the warehouse that executes queries from the Streamlit app"
```

If your app installs Python packages, also declare the CREATE EXTERNAL ACCESS INTEGRATION privilege
and an app specification. See [Allow access to a package index](#label-streamlit-container-eai-na).

For more information about these privileges, see [Configure an app to request the CREATE COMPUTE POOL privilege](/developer-guide/native-apps/container-compute-pool#label-native-apps-cont-req-compute-pool).

### Create the compute resources and Streamlit object in the setup script

Create the compute pool, query warehouse, and Streamlit object directly in the setup script. Create
the Streamlit object in a [versioned schema](/developer-guide/native-apps/versioned-schema) so that
each application version has its own Streamlit object. An upgrade then doesn’t interrupt viewers who
are using the previous version.

Set `RUNTIME_NAME` to `'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'` to select the container runtime. Set
`COMPUTE_POOL` to the pool that runs the app code, and set `QUERY_WAREHOUSE` to the warehouse that
executes SQL queries issued by the app:

Copy code

```
CREATE APPLICATION ROLE IF NOT EXISTS app_public;
CREATE OR ALTER VERSIONED SCHEMA core;

CREATE COMPUTE POOL IF NOT EXISTS myapp_streamlit_pool
  MIN_NODES       = 1
  MAX_NODES       = 3
  INSTANCE_FAMILY = CPU_X64_S
  AUTO_RESUME     = TRUE
  COMMENT         = 'Compute pool for the Streamlit app';

CREATE WAREHOUSE IF NOT EXISTS myapp_query_warehouse
  WAREHOUSE_SIZE      = XSMALL
  AUTO_SUSPEND        = 60
  AUTO_RESUME         = TRUE
  INITIALLY_SUSPENDED = TRUE;

CREATE OR REPLACE STREAMLIT core.app_ui
  FROM            '/code_artifacts/streamlit'
  MAIN_FILE       = 'streamlit_app.py'
  RUNTIME_NAME    = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL    = myapp_streamlit_pool
  QUERY_WAREHOUSE = myapp_query_warehouse;

GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;
GRANT USAGE ON STREAMLIT core.app_ui TO APPLICATION ROLE app_public;
```

Use `IF NOT EXISTS` when creating the compute pool and query warehouse so that an upgrade reuses
them rather than recreating them. The example creates a warehouse owned by the app; choose its size
based on your query workload.

The `MAX_NODES = 3` value is an example, not a sizing recommendation for every app. Choose a value
that accounts for your upgrade frequency and the nodes retained by earlier application versions. See
[Size and manage the compute pool](#label-streamlit-container-pool-na). If you can interrupt active viewers during upgrades, you can
instead use a non-versioned schema to avoid retaining runtimes from earlier application versions. See
[Alternative: Create the Streamlit object in a non-versioned schema](#label-streamlit-container-non-versioned-na).

If your app installs Python packages, create the external access integration before the Streamlit
object, as described in [Allow access to a package index](#label-streamlit-container-eai-na). Add the
`EXTERNAL_ACCESS_INTEGRATIONS` parameter to the `CREATE STREAMLIT` statement:

Copy code

```
CREATE OR REPLACE STREAMLIT core.app_ui
  FROM            '/code_artifacts/streamlit'
  MAIN_FILE       = 'streamlit_app.py'
  RUNTIME_NAME    = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL    = myapp_streamlit_pool
  QUERY_WAREHOUSE = myapp_query_warehouse
  EXTERNAL_ACCESS_INTEGRATIONS = (core.pypi_eai);
```

Important

The COMPUTE\_POOL parameter of the CREATE STREAMLIT command requires a literal object name. You can’t
pass the pool name with `IDENTIFIER(:variable)`, so you can’t use the naming pattern described in
[Add the CREATE COMPUTE POOL command to the setup script](/developer-guide/native-apps/container-compute-pool#label-native-apps-cont-create-compute-pool-setup-script) to prefix the pool name with the
application name. Because compute pools are account-level objects, choose a name that’s unlikely to
collide with a pool created by another app in the same consumer account.

### Specify Python packages

A container runtime installs Python packages from PyPI rather than the Snowflake Anaconda Channel.
List them in a `requirements.txt` file:

Copy code

```
snowflake-native-apps-permission==0.1.14
pandas==2.2.3
plotly==5.24.1
```

You can use a `pyproject.toml` file instead:

Copy code

```
[project]
name = "my-streamlit-app"
version = "1.0.0"
dependencies = [
    "snowflake-native-apps-permission==0.1.14",
    "pandas==2.2.3",
    "plotly==5.24.1",
]
```

To use a specific version of the Streamlit library, pin it in your dependency file.

Note the following differences from a warehouse runtime:

- Use PyPI package names, not Conda package names.
- Pin versions with the `==` operator rather than `=`.
- Express version ranges with `<`, `<=`, `>=`, `>`, and comma-separated lists rather than the `*`
  wildcard.

Important

If your dependency file lists any package, the container must reach the package index, which
requires an external access integration that the consumer approves. An app whose dependency file is
empty or absent runs without one. See [Allow access to a package index](#label-streamlit-container-eai-na).

### Use the Permission SDK

Streamlit apps use the `snowflake-native-apps-permission` SDK to request privileges and object
references from the consumer. With a container runtime, you must list the SDK in your dependency
file, the same way you list it in `environment.yml` for a warehouse runtime:

Copy code

```
snowflake-native-apps-permission==0.1.14
```

Your app code doesn’t change:

Copy code

```
import snowflake.permissions as permissions
```

Note

If you forget to list the SDK, the app fails at runtime with
`ModuleNotFoundError: No module named 'snowflake.permissions'`. Because the SDK is itself installed
from PyPI, the app also needs external access before any permission dialog can work.

For more information about requesting privileges and references, see
[Create and access objects in a consumer account](/developer-guide/native-apps/requesting-about).

### Allow access to a package index

To install packages, the app needs an external access integration for the package index, and the
consumer must approve it. The app creates the network rule, the integration, and an app
specification that names the endpoints it needs. The consumer reviews that specification and
approves it.

1. In the manifest file, add the CREATE EXTERNAL ACCESS INTEGRATION privilege to the privileges you
   already declare:

   Copy code

   ```
   manifest_version: 2

   artifacts:
     setup_script: setup.sql
     default_streamlit: core.app_ui

   privileges:
     - CREATE COMPUTE POOL:
         description: "Creates the compute pool that runs the Streamlit app"
     - BIND SERVICE ENDPOINT:
         description: "Binds the endpoint that viewers use to reach the Streamlit app"
     - CREATE WAREHOUSE:
         description: "Creates the warehouse that executes queries from the Streamlit app"
     - CREATE EXTERNAL ACCESS INTEGRATION:
         description: "Creates an EAI so the app can install Python packages from PyPI"
   ```
2. In the setup script, create the network rule, the integration, and the app specification after
   creating the `core` schema and before creating the Streamlit object. All three statements succeed
   at installation time. The integration stays inert until the consumer approves the specification,
   so you don’t need callbacks or conditional logic:

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE core.pypi_network_rule
     MODE       = EGRESS
     TYPE       = HOST_PORT
     VALUE_LIST = ('pypi.org', 'files.pythonhosted.org');

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION core.pypi_eai
     ALLOWED_NETWORK_RULES = (core.pypi_network_rule)
     ENABLED               = TRUE;

   ALTER APPLICATION SET SPECIFICATION pypi_access
     TYPE        = EXTERNAL_ACCESS
     LABEL       = 'Python package access (PyPI)'
     DESCRIPTION = 'Required to install Python dependencies for the Streamlit app'
     HOST_PORTS  = ('pypi.org', 'files.pythonhosted.org');
   ```

   Every hostname in HOST\_PORTS must match a value in the `VALUE_LIST` property of the network rule
   that the integration uses.
3. Reference the integration from the CREATE STREAMLIT statement with the
   EXTERNAL\_ACCESS\_INTEGRATIONS parameter, as shown in
   [Create the compute resources and Streamlit object in the setup script](#label-streamlit-container-create-na).

The consumer then installs the app, opens it in Snowsight, reviews the endpoints your app
declared, and approves them. After approval, the container can install packages the next time the
service starts.

Important

An app that lists packages doesn’t work until the consumer approves the specification. It fails both
when no integration exists and when an integration exists but the specification isn’t approved.
Because the Permission SDK is itself installed from PyPI, the app can’t display its own approval
request on the first launch. Tell consumers to approve external access as part of your installation
instructions.

For more information about network rules, external access integrations, and app specifications, see
[Request external access](/developer-guide/native-apps/requesting-app-specs-eai).

### Size and manage the compute pool

The app creates the compute pool that runs its Streamlit app, as shown in
[Create the compute resources and Streamlit object in the setup script](#label-streamlit-container-create-na). A container-runtime Streamlit app can’t run on the consumer
account’s default Streamlit compute pool.

Compute pools that an app creates are owned exclusively by that app, and the consumer can’t use them
directly. The pool also can’t be shared with a different app.

If you create the Streamlit object in a versioned schema, account for application versions that
coexist after upgrades, not just the current version. An upgrade doesn’t immediately suspend the
Streamlit container runtime from the previous application version. The runtime continues to occupy a
compute pool node until it suspends after three days of viewer inactivity. If you upgrade several
times within that period, runtimes from multiple application versions can occupy nodes at the same
time.

Set `MAX_NODES` to a value greater than the number of application versions whose Streamlit container
runtimes you expect to coexist, including the current version and earlier versions that haven’t
suspended. This leaves capacity to start the runtime for the next upgrade. This guidance assumes one
container-runtime Streamlit object per application version. If your app has multiple Streamlit
objects that use the same pool, account for a node for each container-runtime object in each version.

For example, if you upgrade an app twice within three days, the original version and the two newer
versions can occupy three nodes. For an app with one container-runtime Streamlit object per version,
set `MAX_NODES` to at least `4` to leave capacity for another upgrade before the older runtimes suspend.
Insufficient capacity or frequent upgrades can fill the compute pool and prevent a new version’s
Streamlit runtime from starting. Increase `MAX_NODES` or space upgrades to allow older runtimes to
suspend before the pool runs out of nodes.

To increase the capacity of an existing pool, use [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool) in your
app’s setup script. Changing `MAX_NODES` in a `CREATE COMPUTE POOL IF NOT EXISTS` statement
doesn’t update an existing pool.

For guidance on choosing an instance family and the costs involved, see
[Best practices for using compute pools in an app with containers](/developer-guide/native-apps/container-compute-pool#label-native-apps-container-best-pracs) and
[Guidelines for selecting resources in Streamlit in Snowflake](/developer-guide/streamlit/app-development/runtime-environments#label-streamlit-guidelines-wh).

#### Alternative: Create the Streamlit object in a non-versioned schema

To avoid retaining runtimes from earlier application versions, create the Streamlit object in a
non-versioned schema. During an upgrade, `CREATE OR REPLACE STREAMLIT` replaces the existing object
instead of keeping a separate object for each application version. This avoids the additional compute
pool nodes occupied by coexisting versions.

The tradeoff is interruption: replacing the object shuts down the running Streamlit app and switches
to the new version. Active viewers are interrupted rather than continuing to use the previous version.
Use this alternative when that interruption is acceptable.

For this alternative, use the following Streamlit creation and grant statements instead of those for
`core.app_ui` in [Create the compute resources and Streamlit object in the setup script](#label-streamlit-container-create-na). Reuse the compute pool, query warehouse,
and application role from that example. Create a separate non-versioned schema for the Streamlit
object; this example doesn’t convert the existing `core` schema:

Copy code

```
CREATE SCHEMA IF NOT EXISTS streamlit_ui;

CREATE OR REPLACE STREAMLIT streamlit_ui.app_ui
  FROM            '/code_artifacts/streamlit'
  MAIN_FILE       = 'streamlit_app.py'
  RUNTIME_NAME    = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL    = myapp_streamlit_pool
  QUERY_WAREHOUSE = myapp_query_warehouse;

GRANT USAGE ON SCHEMA streamlit_ui TO APPLICATION ROLE app_public;
GRANT USAGE ON STREAMLIT streamlit_ui.app_ui TO APPLICATION ROLE app_public;
```

If your app installs Python packages, also set `EXTERNAL_ACCESS_INTEGRATIONS` on
`streamlit_ui.app_ui`, as shown in [Create the compute resources and Streamlit object in the setup script](#label-streamlit-container-create-na).

In the manifest file, update `default_streamlit` to reference the object in the non-versioned schema:

Copy code

```
artifacts:
  setup_script: setup.sql
  default_streamlit: streamlit_ui.app_ui
```

### Use owner’s rights and restricted caller’s rights

By default, SQL that a Streamlit app submits runs with the privileges of the application, which is
owner’s rights. A container-runtime Streamlit app can also run queries with
[restricted caller’s rights](/developer-guide/native-apps/restricted-callers-rights), which lets
the app read consumer data on behalf of the viewer without the app being granted access to that
data outright.

Select which set of privileges a query uses by choosing a connection:

Copy code

```
import streamlit as st

# Runs with the privileges of the application.
owner_session = st.connection("snowflake").session()

# Runs with the viewer's privileges, restricted to what caller grants allow.
caller_session = st.connection("snowflake-callers-rights").session()
```

Create both connections at the top level of your script. The token that backs the
restricted caller’s rights connection is created when the app session starts and is short-lived.

To use restricted caller’s rights, declare it in the manifest file:

Copy code

```
restricted_callers_rights:
  enabled: true
  description: "Reads consumer data on behalf of the signed-in viewer"
```

A user with the MANAGE CALLER GRANTS privilege then adds a caller grant for every object in the
path:

Copy code

```
GRANT CALLER USAGE ON DATABASE consumer_db TO APPLICATION myapp;
GRANT CALLER USAGE ON SCHEMA consumer_db.public TO APPLICATION myapp;
GRANT CALLER SELECT ON TABLE consumer_db.public.consumer_table TO APPLICATION myapp;
```

Important

Caller grants alone aren’t enough. The viewer’s own role must also hold ordinary privileges on the
same objects. Restricted caller’s rights uses the viewer’s DEFAULT\_ROLE, not the role that the
viewer has selected in Snowsight, so grant the ordinary privileges to the viewer’s
DEFAULT\_ROLE:

Copy code

```
GRANT USAGE ON DATABASE consumer_db TO ROLE viewer_default_role;
GRANT USAGE ON SCHEMA consumer_db.public TO ROLE viewer_default_role;
GRANT SELECT ON TABLE consumer_db.public.consumer_table TO ROLE viewer_default_role;
```

For more information, see [Use owner’s rights and restricted caller’s rights in an app](/developer-guide/native-apps/restricted-callers-rights) and
[Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

### What consumers experience

Consumers install an app that contains a container-runtime Streamlit app with the same
[CREATE APPLICATION](/sql-reference/sql/create-application) command as any other app. From there, the differences from
a warehouse runtime are as follows:

- Consumers aren’t prompted to select a warehouse. The app specifies its query warehouse through
  `QUERY_WAREHOUSE`.
- If your app installs Python packages, consumers review and approve the external access
  specification before the app can start.
- If the compute pool is cold, consumers see a loading state while the service starts.
- If the provider uses a non-versioned schema for the Streamlit object, an upgrade shuts down the
  running Streamlit app and switches to the new version, interrupting active viewers. See
  [Alternative: Create the Streamlit object in a non-versioned schema](#label-streamlit-container-non-versioned-na).

### Limitations for container runtimes in an app

For general Streamlit limitations and differences between runtimes, see
[Limitations and changes that vary by runtime](/developer-guide/streamlit/limitations#label-streamlit-runtime-limitations).

The following additional limitations apply to container-runtime Streamlit apps in a Snowflake Native App:

- The app must create its own compute pool. A container-runtime Streamlit app in a Snowflake Native App can’t
  run on the consumer account’s default Streamlit compute pool.
- The COMPUTE\_POOL parameter of CREATE STREAMLIT requires a literal object name, so you can’t
  generate the pool name from the application name.
- A compute pool that the app creates can’t be shared with a different app.
- The warehouse selector in Snowsight has no effect on the SQL that a container-runtime
  Streamlit app runs.
- If the app installs Python packages from PyPI, it doesn’t work until the consumer approves the external
  access specification, and it can’t request that approval from within the Streamlit app on the
  first launch.

For general limitations that apply to apps with containers, see
[Known limitations in Snowflake Native Apps with Snowpark Container Services](/developer-guide/native-apps/limitations#label-native-apps-limitations-spcs).

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

Note

If your container-runtime Streamlit app installs Python packages, it can’t start until the consumer
approves the external access specification. When you test in your own account, approve the
specification before you open the app. See [Allow access to a package index](#label-streamlit-container-eai-na).

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

### Container runtime doesn’t start

If a container-runtime Streamlit app doesn’t start, check the compute pool first, then the app’s
dependencies.

To check the compute pool, run [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool) as a role that can see the
app’s pools:

Copy code

```
DESCRIBE COMPUTE POOL myapp_streamlit_pool;
```

Look at the `state` column. The service can only run once the pool reaches ACTIVE or IDLE, so a pool
that stays in STARTING, RESIZING, or SUSPENDED explains an app that never loads. The
`status_message` column reports the reason when Snowflake can’t provision or scale up the pool, for
example a capacity error. For what each state means, see
[Compute pool lifecycle](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-lifecycle).

If the Streamlit object is in a versioned schema and the pool is full after repeated upgrades,
runtimes from earlier application versions might still be occupying nodes during the three-day
inactivity period. Check whether `MAX_NODES` allows for those runtimes as well as the new version.
Increase the pool’s capacity or allow older runtimes to suspend before another upgrade. See
[Size and manage the compute pool](#label-streamlit-container-pool-na). If interrupting active viewers during upgrades is acceptable,
consider the non-versioned schema alternative in [Alternative: Create the Streamlit object in a non-versioned schema](#label-streamlit-container-non-versioned-na).

If the pool is healthy, check the app’s dependencies:

- If the app installs Python packages, confirm that the consumer approved the external access
  specification. Run `SHOW SPECIFICATIONS IN APPLICATION <app_name>` to check the status. Without
  approval, the service can’t download the packages listed in your dependency file.
- Confirm that the dependency file lists `snowflake-native-apps-permission` if your app imports
  `snowflake.permissions`. A missing entry produces
  `ModuleNotFoundError: No module named 'snowflake.permissions'`.
- Confirm that the dependency file is in the same directory as your main file or in a parent
  directory of it, and that it uses PyPI package names rather than Conda package names.
- Confirm that every package in your dependency file resolves for the Python version that the
  container runtime provides. Pinning a version that isn’t available for that Python version causes
  the install to fail when the service starts.

To read the container’s own logs, including the output of package installation, see
[Live logs in Snowsight](/developer-guide/streamlit/features/logging-tracing#label-streamlit-container-live-logs). For problems that aren’t specific to the Snowflake Native App Framework, see
[Troubleshooting Streamlit in Snowflake](/developer-guide/streamlit/troubleshooting).
