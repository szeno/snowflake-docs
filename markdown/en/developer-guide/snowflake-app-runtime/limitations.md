# Snowflake App Runtime limitations

This topic lists known limitations of Snowflake App Runtime.

## General

- Snowflake App Runtime is available in Amazon Web Services (AWS), Microsoft
  Azure, and Google Cloud commercial regions. It isn’t available in government
  regions.
- Snowflake App Runtime isn’t available on [trial accounts](/user-guide/admin-trial-account).
  Use a paid Snowflake account to deploy Application Services.
- Deployable projects use **Node.js** (typically Next.js). Support for
  **Python** is planned.
- The `TYPE` of an artifact repository can’t be changed after creation.

## Packaging

- Each build produces an immutable version. You can’t overwrite an existing
  version; you must produce a new build.
- The list of supported project types might grow over time. Check the release
  notes for the current set.
- When your uploaded source includes an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
  manifest, Snowflake validates it during the remote build. Invalid YAML,
  unsupported `icon` paths, or other manifest errors fail the build
  before the service is created or altered.

## Deployment

- Standard SPCS commands (`CREATE SERVICE`, `ALTER SERVICE`) don’t work
  with Application Services. Use the `APPLICATION SERVICE` variants instead.
- An Application Service deploys exactly one package at a time.
- `CREATE OR REPLACE APPLICATION SERVICE` isn’t supported.
- `UNDROP` isn’t supported for Application Services. After a service is
  dropped, it can’t be recovered.
- Transferring ownership of an Application Service isn’t supported.
- Remote builds have a maximum running time after the builder pod becomes
  ready (containers running). Queueing, scheduling, image pull, and container
  startup don’t count toward the limit. The default maximum is about 12 hours.
  Builds that exceed the limit can be canceled and fail the deploy.
- Remote builds have scoped outbound network access by default during the
  install and build steps. Account administrators can disable that automatic
  access; builds that need npm or Google Fonts then fail unless developers
  supply an EAI through `build_eai`. See
  [Deploying with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/deploy).
- `ALTER APPLICATION SERVICE ... RESUME` can fail when the deployed runtime
  image is blocked. Upgrade the service to a new package version before
  resuming.

## Access control

- Privileges on an Application Service and on its backing artifact repository
  are independent when you manage objects with SQL. A role that has access to
  the running service doesn’t implicitly have access to the repository, and the
  reverse is also true. The `snow app deploy` workflow manages repository access
  when it runs the remote build.
- You can’t grant privileges on an Application Service that lives in a
  [personal database](/user-guide/personal-databases).
  If you need to share an app with other roles using `GRANT USAGE`, `GRANT MONITOR`, or `GRANT OPERATE`, deploy the Application Service to a standard
  database and schema instead of a personal database.
- `GRANT` on future Application Services (`GRANT ... ON FUTURE APPLICATION SERVICES IN SCHEMA ...`) isn’t supported.
