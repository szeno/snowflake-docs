# Use versioned schema to manage app objects across versions

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to use versioned schema to manage app state when installing and upgrading a Snowflake Native App.

## About versioned schemas

Versioned schemas are special types of database schema that are designed to handle stateless objects from one version
to another.

A versioned schema contains metadata about the objects in an app that are associated with a specific version.
Version pinning is a feature of versioned schemas that allows an app to know what job, queries, etc. are associated with
these objects.

When an object in a versioned schema runs a query, for example, that query is “pinned” to the version of the app running the query.

Version pinning is important when upgrading an app to a new version. Consider the context where V1 of an app runs a
complex query that takes a long time to complete.

If an upgrade occurs while this query is still running, the upgrade state of the app changes to `COMPLETE` and
the app is upgraded to `v2`. The previous version state changes to `FINALIZING` until all jobs from version
`v1` have completed.

See [Upgrade states](/developer-guide/native-apps/release-channels-upgrade#label-native-apps-upgrade-process) for more information on the upgrade states for an app.

## Stateful and stateless objects

When developing a new version of an app, providers must consider if the components they are modifying need to preserve
their state from one version or patch to another. A typical app contains two types of components:

Stateless objects
:   Stateless objects are recreated for each new version or patch of the app. Stateless objects only need to be available
    for the lifetime of the version and can be recreated as necessary. Stateless objects are typically the code of the app,
    including stored procedures, user-defined functions, Streamlit apps, and similar content.

    Stateless objects should be created in a [versioned schema](#label-native-apps-versioning-versions-schema-about).

Stateful objects
:   Stateful objects are shared from one version or patch of the app to another. Stateful components are intended to have a
    lifetime across multiple versions of the app. For example, if an app uses a table to store configuration information within
    the consumer account, the contents of this table would need to be preserved during upgrade.

    Stateful objects should be created using a regular schema.

## About versioned schemas

When writing the setup script for the new version of the app, providers must account for stateless and stateful components. To
handle stateless objects the Snowflake Native App Framework provides a special type of database schema referred to as versioned schemas. A versioned schema is
similar to a regular database schema with added functionality to handle multiple versions of objects created by different app
versions.

## Restrictions on versioned schemas

- Snowpark Container Services is not supported in versioned schemas.
- Versioned schema are only available within the context of an application object. They are created only within the setup script.
  Each version of an app has its own setup script and contains versioned schema that are specific to that version.
- A versioned schema can only be used within the setup script of an application package. They can only be created within the
  context of an application object.
- Tasks are not supported on versioned schemas. For example, providers cannot include tags when creating or altering a
  versioned schema. However, providers can use tags inside a versioned schema, as long as they only apply those tags objects
  within a versioned schema in the same app.
- Tags and masking policies are not supported in versioned schemas.
- Grants and future grants are not supported in versioned schemas.
- Versioned schemas cannot be used as either the source or destination of a clone operation.
- Dropping a versioned schema is not supported. Dropping a versioned schema would drop all versions of the objects it contains and
  would impact queries running against older versions or patches of the app.

Note

To use application roles, tasks, tags, masking policies and Snowpark Container Services within the setup script of an app, you
must create them in a normal schema.

## Internal implementation of versioned schemas

Internally, versioned schemas contain subschema that correspond to each version of the app.

However, these subschema are not directly accessible to the consumer within the application object. A consumer will only see
objects within the versioned schema that correspond to the version of the app they have installed in their account.

For example, if a consumer uses the [SHOW OBJECTS](/sql-reference/sql/show-objects) command to view the objects
in a versioned schema, they will only see the objects for the version they are currently using.

When writing the setup script, providers must recreate objects in a versioned schema using CREATE OR REPLACE or CREATE IF NOT EXISTS.
This is important because internally, each version of the app has its own objects within the subschema of the versioned schema.

## Using versioned and non-versioned schemas in the setup script

To manage the state of an app during upgrades, the Snowflake Native App Framework uses versioned schemas. A versioned schema
is similar to regular database schema with added functionality to handle multiple versions of objects
created by different application versions.

Versioned schema are only available within the context of an application object. They are created
only within the setup script. Each version of an app has its own setup script and contains versioned
schema that are specific to that version.

When developing a new version of an app, providers must account for changes to the objects that the
app creates using the setup script.

The following example shows a common situation where both versioned and normal schema can be
used in a setup script to create stateless and stateful components:

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA stateless_objects;
CREATE OR REPLACE PROCEDURE stateless_object.py_echo_proc(STR string)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION=3.12
  PACKAGES=('snowflake-snowpark-python')
  HANDLER='echo.echo_proc'
  IMPORTS=('/libraries/echo.py');

CREATE OR ALTER SCHEMA stateful_object;
CREATE TABLE stateful_object.config_props
  prop_name STRING;
  prop_value STRING;
  time_stamp TIMESTAMP;
```

## Create a versioned schema

To create a versioned schema with the setup script, use the
[CREATE OR ALTER VERSIONED SCHEMA](/sql-reference/sql/create-versioned-schema) command as shown in the following example:

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA version_schema;
```

Note

You should always include the CREATE OR ALTER version of this command to ensure that
versioned schemas are compatible across versions and patches.

## Use non-versioned schemas for stateful objects

Objects within an app may need to preserve state across versions. For example, configuration
data or data collected while the app has been running may be to be preserved.

These types of objects must reside in a normal database schema and they should be created to persist
during initial installation and upgrades.

The following example shows how to create a stateful object in the setup script:

Copy code

```
CREATE SCHEMA IF NOT EXISTS stateful_object;

CREATE TABLE IF NOT EXISTS stateful_object.config (
  config_param STRING,
  config_value STRING,
  default_value STRING,
  modified_on  TIMESTAMP);

ALTER TABLE stateful_object.config
  ADD COLUMN IF NOT EXISTS modified_on TIMESTAMP;
```

In this example, the setup script defines a configuration table that would persist from one version
of an app to another. If the previous version of the application did not have a `modified_on` column,
the setup script first attempts to fully create the table (in the case of initial installation) or modify
the existing table by adding the column (in the case of an upgrade).

## Use versioned schemas for stateless objects

Some objects within an app do not persist state between versions of an application. For example, code that
defines the application logic, including stored procedures, functions, etc. can be fully recreated in the
setup script without losing any user data or state.

Snowflake recommends that these objects be contained within a versioned schema.

The following example shows how to create a UDF within a versioned schema.

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA stateless_object;
CREATE FUNCTION IF NOT EXISTS stateless_object.add(x int, y int)
  RETURNS INT
  LANGUAGE SQL
  AS $$ x + y $$;
```

## Version pinning

A versioned schema contains metadata about which objects in a Snowflake Native App are associated
with a specific version. Version pinning is a feature of versioned schemas that allows an
app to know what job, queries, etc. are associated with these objects.

When an object in a versioned schema runs a query, for example, that query is “pinned”
to the version of the app running the query.

Version pinning is important when upgrading an app to a new version. Consider the context
where V1 of an app runs a complex query that takes a long time to complete. If an
upgrade occurs while this query is still running, the app will not upgrade until the query
is complete.
