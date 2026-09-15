# Organize your Streamlit app files

When you deploy an app to Streamlit in Snowflake, the app’s entrypoint file can have any name that follows
standard file naming conventions and can be located anywhere in the app’s source directory.
The app’s source directory can contain additional files, such as page scripts, Python modules,
media files, and configuration files.

The root of your app’s source directory is Streamlit’s working directory. If you develop and run
your app locally, this means you must execute the `streamlit run` command from the root of
your source directory to ensure that all paths are correct.

When you initialize a Streamlit app from Snowsight or use CREATE STREAMLIT
without specifying a source location, the embedded stage of the Streamlit object
contains an entrypoint file in its root. You can use the file explorer to add
additional files. If you need to rename or move your entrypoint file, you must use
SQL commands to update your Streamlit object’s MAIN\_FILE value.

Note

If you use the CREATE STREAMLIT command with the ROOT\_LOCATION parameter, your app can only
use a warehouse runtime and is subject to additional limitations. This page covers apps
created with the FROM parameter. For more information, see [Understanding the different types of Streamlit objects](/developer-guide/streamlit/migrations-and-upgrades/overview).

## Container runtime file structure

Feature — Generally Available

Not supported in government regions.

When you use a container runtime, your entrypoint file can have any name that follows
standard file naming conventions and can be located anywhere in your source
directory. However, with the introduction of `st.navigation`\_ in Streamlit v1.36, the most common
practice is to use `streamlit_app.py` as the entrypoint file because page names don’t have to be
inferred from the file names.

Snowflake executes the `streamlit run` command from the root of the source directory, so
you must handle paths accordingly.

- Your entrypoint file can have any name and be located anywhere in your source directory.
- Your dependency files can be in any directory between the root of your source directory
  and directory containing your entrypoint file. For more information, see
  [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).
- You can have one or more `.streamlit/` directories between the root of
  your source directory and the directory containing your entrypoint file.
- The root of your source directory is Streamlit’s working directory.

The following directory structure is valid for a container-runtime Streamlit app:

Copy code

```
source_directory/
├── .streamlit/           # Optional configuration
│   ├── config.toml
│   └── secrets.toml
├── page_1.py             # Page 1
├── page_2.py             # Page 2
├── pyproject.toml        # Python dependencies
├── streamlit_app.py      # Entrypoint file
└── uv.lock               # Auto-generated lockfile
```

The following directory structure shows two apps in one source directory, each with its own entrypoint file
and dependencies. In this example, two different Streamlit objects exist. Both Streamlit objects set FROM to the location
represented by `source_directory`, but each object sets MAIN\_FILE to a different `streamlit_app.py` file.
The first app uses a `pyproject.toml` file for dependencies, while the second app uses a `requirements.txt` file.

Copy code

```
source_directory/
├── .streamlit/           # Shared configuration
│   ├── config.toml
│   └── secrets.toml
├── app_one/              # First app source directory
│   ├── .streamlit/       # Overriding first-app configuration
│   │   ├── config.toml
│   │   └── secrets.toml
│   ├── page_1.py
│   ├── page_2.py
│   ├── pyproject.toml     # Python dependencies for first app
│   ├── streamlit_app.py   # Entrypoint file for first app
│   └── uv.lock
├──  app_two/              # Second app source directory
│   ├── requirements.txt   # Python dependencies for second app
│   ├── page_1.py
│   ├── page_2.py
│   ├── streamlit_app.py   # Entrypoint file for second app
│   └── uv.lock
└── utils/                 # Shared modules
    └── helper.py
```

Important

Some Streamlit features require paths relative to the working directory while others
require paths relative to the entrypoint file.

Typically, paths to images and other media within your app should be relative to the
working directory (the root of your source directory). However, paths to other pages in a
multipage app are relative to the location of the entrypoint file.

To avoid confusion, consider organizing your app files so that the entrypoint file
is in the root of your source directory. You can save multiple apps in one Git
repository and pass a subdirectory to the FROM parameter when you create the
Streamlit object. That subdirectory is then your app’s source directory. In the
previous example, this means using `source_directory/app_one` and
`source_directory/app_two` in the FROM parameter. Although in that case, the apps
would lose access to the shared modules in `source_directory/utils`.

## Warehouse runtime file structure

When you use a warehouse runtime, your entrypoint file can have any name but must be located in the root of your
source directory. Your Python version and dependencies are specified in an `environment.yml` file in the root
of your source directory. If you don’t include an `environment.yml` file, your app will run on the latest
version of Python and latest version of Streamlit that are currently supported in Streamlit in Snowflake. If you use the
[package picker](/developer-guide/streamlit/app-development/dependency-management#label-snowsight-streamlit-package-picker) in Snowsight to add packages, the
`environment.yml` file is automatically updated or created for you.

The following directory structure is valid for a warehouse-runtime Streamlit app:

Copy code

```
source_directory/
├── .streamlit/           # Optional configuration
│   └── config.toml
├── environment.yml       # Conda dependencies
├── page_1.py
├── page_2.py
└── streamlit_app.py      # Entrypoint file
```

### Importing modules and files from other stages

The CREATE STREAMLIT and ALTER STREAMLIT commands support the IMPORTS parameter, which allows you to
import additional files from other stages into your app’s source directory. If you have a set of
common modules or files that you want to share across multiple apps, you can store them in a stage
and import them into each app using the IMPORTS parameter. However, this is only supported for apps
using a warehouse runtime.

## Multipage apps

Streamlit supports two methods for creating multipage apps:

- Using `st.navigation`: You can use the `st.navigation` command to create a custom navigation structure within your app. This
  allows you to define pages programmatically and control the navigation flow. The entrypoint file acts like a page router and the pages of your
  app can be defined as functions or Python scripts anywhere in your source directory. This is the recommended method for creating multipage
  apps, because it provides the most flexibility.
- Using a `pages/` directory: You can create a directory named `pages/` adjacent to your app’s entrypoint file. The
  entrypoint file is treated as the home page of your app. Each Python file in the `pages/` directory is treated as an additional page in the app.
  Page names are derived from the filenames.

You can’t mix the two methods for creating multipage apps. For more information on multipage apps, see
[Overview of multipage apps](https://docs.streamlit.io/develop/concepts/multipage-apps/overview)
in the Streamlit documentation.

Note

When you host multipage apps in Streamlit in Snowflake, URL pathnames are prefixed with `/!`. For example, if the relative path to a page is `/page2`
in a multipage app, its relative path in Streamlit in Snowflake becomes `/!/page2` as shown in the following URL: `https://app.snowflake.com/org/account_name/#/streamlit-apps/DB.SCHEMA.APP_NAME/!/page_2`

## Update your entrypoint file

If you rename or move your entrypoint file, you must use SQL commands to update your Streamlit
object to use the new entrypoint file. You must use a container runtime if you move your
entrypoint file to a subdirectory.

1. Use the [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) command to change the MAIN\_FILE parameter
   of your Streamlit object, as shown in the following example:

   Copy code

   ```
   ALTER STREAMLIT my_streamlit_app
   SET MAIN_FILE = 'subdir/new_entrypoint.py';
   ```

   This example changes the entrypoint file of the `my_streamlit_app` Streamlit object
   to `subdir/new_entrypoint.py`.
