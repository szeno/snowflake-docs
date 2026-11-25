# Privileges

Snowflake App Runtime adds the Application Service object for running deployed
apps. The [deploy pipeline](/developer-guide/snowflake-app-runtime/deploy)
packages your application during the build phase and creates the service in the
deploy phase. You don’t provision build or packaging infrastructure yourself.

Have an account administrator complete
[account setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
so `snow app setup` and `snow app deploy` use shared account defaults. Until an
administrator completes setup, deploys go to a
[personal database](/user-guide/personal-databases), which you can’t share with
other roles.

This topic covers Application Service privileges and what deploy roles need.

## Application Service privileges

Use these privileges to share, operate, and monitor deployed apps. For grant
examples, see [Share a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/access-control).

| Privilege | Effect |
| --- | --- |
| USAGE | Appear in `SHOW APPLICATION SERVICES` results and access public endpoints exposed by the service. |
| MONITOR | View runtime status and read container logs with [SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS](/sql-reference/functions/system_get_application_service_logs). |
| OPERATE | `ALTER APPLICATION SERVICE` (`SUSPEND`, `RESUME`, `UPGRADE`, `SET`, `UNSET`). For apps on serverless compute (Public Preview), `DISABLE` and `ENABLE` replace `SUSPEND` and `RESUME`. |
| OWNERSHIP | `DROP` the service. The owning role also implicitly has every other privilege on the service. |

Expand

Show lessSee more

You can grant `USAGE`, `MONITOR`, and `OPERATE` on one Application Service, on
all of them in a schema, or on those created later. See
[Grant access to many apps](/developer-guide/snowflake-app-runtime/access-control#label-snowflake-app-runtime-access-control-bulk-grants).

## Deploy with the CLI

For the recommended team path (`snow app setup` then `snow app deploy` to shared
account defaults), you need:

- [Account administrator setup for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/account-admin-setup)
  completed (or equivalent account defaults and grants).
- A deploy role that was selected during that setup (or equivalent privileges).
- A project with an `app.yml` file.

Personal-database deploys don’t require administrator setup, but you can’t share
apps deployed there. See
[Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).

Deploy roles receive the grants they need during Snowsight setup. When you run
`snow app deploy`, Snowflake provisions the artifact repository and runs the
remote build for you.

## Create an Application Service with SQL

If you run [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service) directly (without
`snow app deploy`), the creating role needs the privileges listed on that
command page. Schema-level `CREATE` privileges for deploy roles are normally
granted during
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup).

## Artifact repository privileges for SQL workflows

The `snow app deploy` workflow provisions one artifact repository per
application and runs the remote build for you. You only need artifact
repository privileges if you publish packages or manage repositories with SQL.
In that case, `CREATE APPLICATION SERVICE` may require `READ` on a repository that already contains the package.
See [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository) and
[Artifact repository commands](/sql-reference/commands-snowflake-apps#label-snowflake-apps-sql-commands-artifact-repository).

## Preview in Snowsight Workspaces

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Preview works in your own workspaces with no extra grants. Your role needs
more only in these cases:

- In a shared workspace: `WRITE` on the workspace.
- For each external access integration listed in `app.yml`: `USAGE` on it.
- For each secret listed in `app.yml`: `READ` on it.

To deploy from the workspace, your role also needs the privileges in
[Deploy with the CLI](#label-snowflake-app-runtime-privileges-cli-deploy).
See [Develop Snowflake App Runtime apps in Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces).

## Next steps

- Grant other roles access to an app: [Share an app](/developer-guide/snowflake-app-runtime/access-control).
