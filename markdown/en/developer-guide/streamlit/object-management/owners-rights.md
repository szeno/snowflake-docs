# Understanding owner’s rights and Streamlit in Snowflake apps

## Introduction

The model for Streamlit in Snowflake closely maps to the owner’s rights model in
[stored procedures](/developer-guide/stored-procedure/stored-procedures-rights). This eliminates
the need for service account tokens and integrates with the authentication, access control,
and network policy features that Snowflake provides.

## About owner’s rights in Streamlit in Snowflake

By default, Streamlit apps adhere to the following rules within a session:

- Run with the privileges of the owner, not the privileges of the caller. To run a container-runtime
  app with restricted caller’s rights instead, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).
- Run with the warehouse provisioned by the app owner.
- Use the database and schema that the Streamlit in Snowflake app was created in, not the database and
  schema that the caller is currently using.

## About app creation

Streamlit apps are schema-level objects. To create a Streamlit app, you need appropriate
privileges on the database, schema, and warehouse. When an app is created, it runs with
the role of the user who originally created the app.

For more information, see [Privileges required to create a Streamlit app](/developer-guide/streamlit/object-management/privileges#label-streamlit-access-privs-create).

## Viewing an app

The app owner can choose which roles have permission to use the app. Viewers can interact
with the app and see anything displayed on the screen. All of the privileges of the app owner’s role
can be used by the app when shared with other roles, regardless of whether the privilege has WITH GRANT enabled.

For more information, see [Privileges required to view a Streamlit app](/developer-guide/streamlit/object-management/privileges#label-streamlit-access-privs-view).

## Restrictions on owner’s rights

Because apps run with owner’s rights, they have several additional restrictions.
If you use any context functions, you must grant the global READ SESSION privilege
to the app owner role. For more information, see [Row access policies in Streamlit in Snowflake](/developer-guide/streamlit/features/row-access).

Warehouse-runtime apps run as a stored procedure and are subject to the same restrictions as
owner’s rights stored procedures. For example, the following items are affected:

- The built-in functions that can be called from inside a stored procedure.
- The ability to execute [ALTER USER](/sql-reference/sql/alter-user) statements.
- DESCRIBE, SHOW, and LIST commands.
- The types of SQL statements that can be called from inside a stored procedure.

For more information, see [Additional restrictions on owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-additional-restrictions).
Container-runtime apps don’t run as stored procedures and aren’t subject to these
additional restrictions.

## Owner’s rights and app security

Streamlit apps running in Streamlit in Snowflake run with owner’s rights and follow the same security model as other
Snowflake objects that run with owner’s rights.

Although Snowflake provides security features like authentication, role-based access control, and
admin controls, responsibility for the security of apps is shared with app creators and owners.

Use caution, for example, when granting a role with write privileges to another Snowflake user. Write
privileges allow the user to modify the Streamlit app.

In general, Snowflake recommends using role-based access control and dedicated roles for creating and
viewing Streamlit apps. Additionally, you should follow appropriate security practices while developing
Streamlit apps inside Snowflake and perform regular security audits of the Streamlit apps in your account.
