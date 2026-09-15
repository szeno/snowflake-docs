# Understanding the different types of Streamlit objects

Streamlit objects in Snowflake have two important differences that
influence their capabilities, limitations, and management:

- How the source location is specified: using the ROOT\_LOCATION parameter (legacy) or
  the FROM parameter (recommended).
- The runtime environment: warehouse runtime or container runtime.

This page explains the differences between the source location specifications, which
in turn affect the runtime environments that can be used.

For more information about runtime environments, see [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).
For a checklist to migrate from warehouse to container runtimes, see [Migrating between runtime environments](/developer-guide/streamlit/migrations-and-upgrades/runtime-migration).

## Source location

When you create Streamlit apps in Snowflake, you can use two different parameters to
specify the location of your source files: ROOT\_LOCATION or FROM. ROOT\_LOCATION is a
legacy parameter that has several restrictions. Currently, FROM is the recommended
parameter for new apps and is required to access the latest Streamlit in Snowflake features, including
container runtimes. This page explains how to differentiate between the two types
of apps. To enable the latest Streamlit in Snowflake features, you must upgrade your legacy Streamlits.
For more information, see [Migrating between runtime environments](/developer-guide/streamlit/migrations-and-upgrades/runtime-migration).

### FROM parameter (recommended)

The FROM parameter copies files from a specified location into an embedded stage
within the Streamlit object. This is the current recommended approach for creating
Streamlit apps.

**Benefits:**

- Supports both warehouse and container runtimes.
- Enables multi-file editing in Snowsight.
- Compatible with Git integration features.
- Uses an embedded, versioned stage within the Streamlit object.

**Syntax:**

Copy code

```
CREATE STREAMLIT my_app
FROM '@my_stage/app_folder'
MAIN_FILE = 'streamlit_app.py';
```

### ROOT\_LOCATION parameter (legacy)

The ROOT\_LOCATION parameter creates an app that references an internal stage as
its source. This is a legacy approach with several limitations. If you created
your app using an older version of Snowsight, your app’s root location
might be a snow URL (`snow://`) instead of a named stage.

**Limitations:**

- Only supports warehouse runtime (can’t use container runtime).
- No multi-file editing support in Snowsight.
- Can’t use Git integration features.
- Requires ongoing access to the internal stage.

**Syntax:**

Copy code

```
CREATE STREAMLIT my_app
ROOT_LOCATION = '@my_stage/app_folder'
MAIN_FILE = '/streamlit_app.py';
```

## Identifying your app’s source location type

You can determine which parameter was used to create your app by examining the
[DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit) output:

Copy code

```
DESCRIBE STREAMLIT my_app;
```

- ROOT\_LOCATION-based apps return fewer columns and include a `root_location` column.
- FROM-based apps return more columns and include a `live_version_location_uri` column.

When you edit an app in Snowsight, you are pushing updates to either the `root_location`
or the `live_version_location_uri`, depending on the app type. You can update both types of apps
using SQL commands to PUT or COPY FILES to these locations.
