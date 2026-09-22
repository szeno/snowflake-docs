# Access control for Snowflake App Runtime

This topic describes common access control patterns for delegating operations
and viewing access on Snowflake App Runtime. For the full list of privileges, see
[Snowflake App Runtime privileges](/developer-guide/snowflake-app-runtime/privileges). For how the running app
queries Snowflake (owner’s rights, caller’s rights, and caller grants), see
[Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake).

## Deploy to a standard database when sharing with other roles

Until an administrator completes
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup),
`snow app setup` resolves the destination to a
[personal database](/user-guide/personal-databases) (`USER$<login_name>`). Unlike most
other PDB object types, you can’t use `GRANT` to give other roles access to an Application
Service in a personal database.

To delegate view, operate, or monitor access to other roles, deploy the
Application Service to a standard database and schema. Configure the destination
through
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
before deploying, or explicitly in your [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
`database` and `schema` (or a named target).

## Execution context

When the app queries Snowflake, each query runs under one of two identities.

- **Owner’s rights**: the query runs as the app’s execution role. Use this
  for work the app does on its own behalf.
- **Caller’s rights**: the query runs as the signed-in user, with that
  user’s default role. Use this to act on behalf of the user accessing the
  app.

The execution role anchors both modes. Owner’s rights queries run as the
execution role directly; no secondary roles are activated. Caller’s rights
queries run as the signed-in user but are bounded by the
[restricted caller’s rights](/developer-guide/restricted-callers-rights)
grants on the execution role.

Where the execution role comes from depends on where the app is deployed:

- **Standard database**: the execution role is the role that owns the app,
  which is the creator’s session primary role.
- **[Personal database](/user-guide/personal-databases) (PDB)**: the app is
  owned by the user who created it, not by a role, so you specify the execution
  role using `EXECUTE_AS_ROLE` in
  [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service). If you don’t set it,
  Snowflake uses the creator’s session primary role. The execution role must be
  granted to the owning user.

Important

Once the app is created, its execution role can’t be changed. To use a
different role, drop and recreate the app with the new role.

To set the execution role for a PDB app, grant the execution role to the owning
user and set `EXECUTE_AS_ROLE`:

Copy code

```
GRANT ROLE my_app_role TO USER <owning_user>;

CREATE APPLICATION SERVICE my_db.my_schema.my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  EXECUTE_AS_ROLE = my_app_role;
```

For caller’s rights, grant the execution role the privileges it may use on a
caller’s behalf with [GRANT CALLER](/sql-reference/sql/grant-caller). Without those
grants, the user can sign in but the query has no privileges to act on.

## Share view-only access to a running app

Grant `USAGE` on the Application Service, plus `USAGE` on the database and schema
that contain it, to let a role open the app. The service must be in a standard
database, not a personal database. In [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli)
or [Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps), you can
ask the agent to grant access for other roles, or use the Apps view in Desktop
to manage sharing.

Copy code

```
GRANT USAGE ON DATABASE my_db TO ROLE app_viewer;
GRANT USAGE ON SCHEMA my_db.my_schema TO ROLE app_viewer;
GRANT USAGE ON APPLICATION SERVICE my_db.my_schema.my_app TO ROLE app_viewer;
```

## Delegate lifecycle control

Grant `OPERATE` to let a role suspend, resume, alter, and configure the
service without transferring ownership:

Copy code

```
GRANT OPERATE ON APPLICATION SERVICE my_db.my_schema.my_app TO ROLE app_ops;
```

An `OPERATE` role can run:

Copy code

```
ALTER APPLICATION SERVICE my_db.my_schema.my_app SUSPEND;
ALTER APPLICATION SERVICE my_db.my_schema.my_app RESUME;
ALTER APPLICATION SERVICE my_db.my_schema.my_app UPGRADE TO VERSION LATEST;
ALTER APPLICATION SERVICE my_db.my_schema.my_app SET AUTO_SUSPEND_SECS = 900;
```

For what those lifecycle settings do, see
[Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).

## Delegate monitoring

Grant `MONITOR` to let a role view runtime status and read container logs:

Copy code

```
GRANT MONITOR ON APPLICATION SERVICE my_db.my_schema.my_app TO ROLE app_monitor;
```

## Grant access to multiple Application Services

You can grant `USAGE`, `MONITOR`, or `OPERATE` across the Application Services in a schema
instead of one service at a time. The services must be in a standard database, and the
grantee role still needs `USAGE` on the database and schema to resolve their names. Ownership
transfer isn’t supported for Application Services.

### Grant on the services that exist now

Copy code

```
GRANT USAGE ON ALL APPLICATION SERVICES IN SCHEMA my_db.my_schema TO ROLE app_viewer;
```

This is a one-time operation. Services created afterward aren’t included.

### Grant on services created later

A future grant applies to Application Services created in the schema after you issue it:

Copy code

```
GRANT MONITOR ON FUTURE APPLICATION SERVICES IN SCHEMA my_db.my_schema TO ROLE app_monitor;
```

To list the future grants on a schema, use [SHOW GRANTS](/sql-reference/sql/show-grants). Application
Service rows report `APPLICATION_SERVICE` in the `grant_on` column.

Revoking a future grant stops Snowflake from applying the privilege to services created
later. Grants that already materialized remain in place and must be revoked separately.

Copy code

```
REVOKE MONITOR ON FUTURE APPLICATION SERVICES IN SCHEMA my_db.my_schema FROM ROLE app_monitor;
```

### Cover existing and future services with one grant

`ON ALL` covers only current services and `ON FUTURE` only later ones, so keeping a role’s
access complete means maintaining both. If your account has
[inherited grants](/user-guide/inherited-grants-intro) enabled, one grant covers both:

Copy code

```
GRANT INHERITED USAGE ON ALL APPLICATION SERVICES IN SCHEMA my_db.my_schema TO ROLE app_viewer;
```

## Revoke access

Copy code

```
REVOKE { USAGE | MONITOR | OPERATE }
  ON APPLICATION SERVICE my_db.my_schema.my_app
  FROM ROLE <role_name>;
```

For general RBAC concepts, see
[Overview of Access Control](/user-guide/security-access-control-overview). For administrator guidance on
managing the risks that applications introduce (including caller grant
restrictions, feature policies, and external access controls), see
[Securing Snowflake App Runtime applications](/developer-guide/snowflake-app-runtime/security).
