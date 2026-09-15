# Migrating between runtime environments

Feature — Generally Available

Not supported in government regions.

You can migrate a Streamlit app between warehouse runtimes and container runtimes by
updating the app’s RUNTIME\_NAME and COMPUTE\_POOL properties. However, some features
are only supported in one type of runtime environment, so there are some considerations
when migrating an app between runtime environments.

This page provides a checklist for migrating from warehouse to container runtime.
Each item provides a brief summary and a link to detailed information when needed.

Note

If a user is viewing an app with a warehouse runtime and the app is altered on another tab to use a
container runtime, the warehouse instance continues to run until one of the following events happens: the user
navigates away, the tab is closed, the page is refreshed, or the WebSocket times out. In this case, source code changes made from the
warehouse view will update the new container instance, but the warehouse preview won’t reflect any changes,
even if the user selects **Run**.

## Prerequisites

Before you begin, adjust your warehouse runtime app in place to prepare for migration.

Optional: Back up your app’s code
:   If your app’s source code isn’t already stored in a version control system, an external
    repository, or a local directory, back it up to avoid any potential data loss during migration.

Ensure that your app wasn’t created with ROOT\_LOCATION
:   Apps created with the ROOT\_LOCATION parameter can only use warehouse runtimes.
    If your app was created with ROOT\_LOCATION, upgrade it to use the FROM parameter.

    See: [Understanding the different types of Streamlit objects](/developer-guide/streamlit/migrations-and-upgrades/overview)

Upgrade your app to Streamlit 1.50+
:   Ensure your app and all dependencies are
    compatible with Streamlit 1.50+.

    See: [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management)

Update your app to Python 3.11 only
:   Container runtimes only support Python 3.11, while warehouse runtimes support
    Python 3.9, 3.10, and 3.11. Ensure your app and all dependencies are compatible
    with Python 3.11.

    See: [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management)

Optional: Locally install Snowflake CLI 3.14.0+
:   If you deploy apps using Snowflake CLI, you need version 3.14.0 or later to
    support the container runtime deployment syntax. Check your version with
    `snow --version`. Optionally, you can use versions 3.12.0 - 3.13.1 if you
    use the `--experimental` flag.

    See: [Create your Streamlit app](/developer-guide/streamlit/app-development/creating-your-app)

## Resources and permissions

Your app can continue to use its existing query warehouse, but you need to set up
a compute pool for the container runtime.

Create and grant access to a compute pool
:   The app owner needs USAGE privileges on the compute pool where the container
    runtime will run. App viewers don’t need any compute pool permissions.

    See: [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges)

Create and grant access to an external access integration
:   Container runtimes ship with a minimal set of pre-installed packages. If your app
    requires additional packages or different versions of the pre-installed packages,
    you must use an external package index like PyPI. To allow your app to access
    an external package index, you must create an external access integration (EAI) and
    grant USAGE privileges on the EAI to the app owner.

    See: [External network access in Streamlit in Snowflake](/developer-guide/streamlit/features/external-access)

## Dependency management

Replace `environment.yml` with `pyproject.toml` or `requirements.txt`
:   If you need to lock any dependency versions or specify additional dependencies, you must
    add a `pyproject.toml` or `requirements.txt` file to the root of your project
    directory. Packages can have different names between Conda and PyPI, so ensure you use
    the correct package names for your artifact repository.

    See: [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management)

Alter your app to set its external access integrations
:   If your dependencies include any version specifiers, or if you install any additional
    packages, you must assign an external access integration to your app. This is so that it
    can access the package index specified in your dependency file. PyPI is the default package
    index.

    See: [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management)

## Code changes

Replace `get_active_session()` with `st.connection("snowflake").session()`
:   When you use a container runtime, the Streamlit server handles multiple viewers
    concurrently. `get_active_session()` isn’t thread-safe, so you must use
    `st.connection("snowflake")` to manage your connection instead.

    See: [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration)

Review your code and implement caching
:   Because container runtimes share disk, compute, and memory resources between viewer sessions,
    you should use `st.cache_resource` or `st.cache_data` to cache expensive computations
    or data that doesn’t change frequently.

    See: [Understanding Streamlit’s client-server architecture](https://docs.streamlit.io/develop/concepts/architecture/architecture) and
    [Caching overview](https://docs.streamlit.io/develop/concepts/architecture/caching) in the Streamlit documentation.

Ensure thread-safety
:   When using a container runtime, your app code must be thread-safe to handle multiple
    viewers concurrently. While each viewer gets a unique instance of
    the app script, you should review any imported code for shared state or global variables that
    could lead to race conditions or inconsistent behavior. If you introduce new threads
    into a Streamlit app, review Streamlit’s architecture and don’t use Streamlit commands
    in your custom threads.

    See: [Multithreading in Streamlit](https://docs.streamlit.io/develop/concepts/design/multithreading) in the Streamlit documentation.

Replace `_snowflake` usage with native Python equivalents
:   `_snowflake` is a private module that is only available in user-defined functions (UDFs)
    and stored procedures. Warehouse runtimes inherit access to `_snowflake`, but container
    runtimes don’t. If your app uses `_snowflake`, replace it with native Python
    equivalents, such as the Snowflake Python Connector. If needed, use stored procedures to
    access secrets.

    See: [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration)

Update file paths and organization
:   The root of your source location is the working directory for your app.
    For most Python libraries, your app will need to use relative paths from the
    root of your source location. However, some Streamlit commands require paths
    relative to the entrypoint file. If your entrypoint file is in a subdirectory,
    check the paths in your code accordingly.

    Verify `secrets.toml` and `config.toml` locations.

    See: [Organize your Streamlit app files](/developer-guide/streamlit/app-development/file-organization)

## App configuration changes

Alter your app to set its compute pool, query warehouse, and runtime
:   When you are ready to switch the runtime type of your app, you can use Snowsight or SQL.

    SnowsightSQL

    1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Projects** » **Streamlit**, and then select your app.
    3. In the upper-right corner, select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) menu, and then select **App settings**.
    4. For the **Python environment**, select **Run on container**.
    5. In the **Compute pool** dropdown, select your compute pool.
    6. In the **Query warehouse** dropdown, select your query warehouse.
    7. To save your changes and close the dialog, select **Save**.

    Copy code

    ```
    ALTER STREAMLIT my_app
    COMPUTE_POOL = my_compute_pool
    QUERY_WAREHOUSE = my_warehouse
    RUNTIME_NAME = SYSTEM$ST_CONTAINER_RUNTIME_PY3_11;
    ```

    Your app will take a couple minutes to reboot and build its new container.

    See: [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments)
