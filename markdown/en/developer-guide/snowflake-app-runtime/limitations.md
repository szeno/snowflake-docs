# Limitations

This topic lists known limitations of Snowflake App Runtime.

## General

- Snowflake App Runtime is available on paid accounts in Amazon Web Services
  (AWS), Microsoft Azure, and Google Cloud commercial regions. It isn’t
  available in government regions or on
  [trial accounts](/user-guide/admin-trial-account).
- Deployable projects use **Node.js** (typically Next.js) or **Python**.
  Python apps run on serverless compute (Public Preview).
- The `TYPE` of an artifact repository can’t be changed after creation.

## Packaging

- Each build produces an immutable version. You can’t overwrite an existing
  version; you must produce a new build.
- When your uploaded source includes an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
  manifest, Snowflake validates it during the remote build. Invalid YAML,
  unsupported `icon` paths, or other manifest errors fail the build
  before Snowflake creates or alters the service.

## Deployment

- Standard SPCS commands (`CREATE SERVICE`, `ALTER SERVICE`) don’t work
  with Application Services. Use the `APPLICATION SERVICE` variants instead.
- An Application Service deploys exactly one package at a time.
- `CREATE OR REPLACE APPLICATION SERVICE` isn’t supported. Use
  [CREATE OR ALTER APPLICATION SERVICE](/sql-reference/sql/create-application-service#label-create-or-alter-application-service-syntax)
  to create a service if it doesn’t exist or update it if it does.
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
  [Deploy an app](/developer-guide/snowflake-app-runtime/deploy).
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

## Serverless compute and scaling

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

These limits apply to
[serverless compute](/developer-guide/snowflake-app-runtime/serverless):

- Every app gets 2 vCPU and 4 GiB of memory. You can’t change the size.
- An app runs as one instance. `min_instances` and `max_instances` don’t
  apply.
- `auto_suspend_secs` has a restricted range, and `auto_resume: false` isn’t
  allowed. See
  [`auto_suspend_secs`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-auto-suspend-secs).
- `SUSPEND` and `RESUME` aren’t supported. Use `DISABLE` and `ENABLE`. You
  can’t upgrade, redeploy, or change the configuration of a disabled app.
- The event table receives logs only.
  `SYSTEM$GET_APPLICATION_SERVICE_EVENT_TABLE_DATA` returns them with the
  `LOG` type. Metrics, restart counts, and container lifecycle events aren’t
  available, and neither are the `--type metric` and `--type lifecycle`
  options of `snow app events`. See
  [On serverless compute, live logs come from the running instance, so you can](/developer-guide/snowflake-app-runtime/observability#label-snowflake-app-runtime-observability-serverless-logs).
- An existing Application Service keeps its compute type. To move an app to
  serverless compute, deploy a new service. See
  [Move an existing app to serverless compute](/developer-guide/snowflake-app-runtime/serverless#label-snowflake-app-runtime-serverless-switch).
- Local state doesn’t survive a stop. See
  [Design for ephemeral compute](/developer-guide/snowflake-app-runtime/serverless#label-snowflake-app-runtime-serverless-state-caching).

## Workspaces preview

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

- **Next.js only.** Other projects with a `dev` script might run, but they
  aren’t supported.
- **One preview per user per project.** You can’t share a preview. Teammates
  who preview the same project get their own preview.
- **One instance.** Preview doesn’t scale out. The dev server gets 2 vCPU and
  4 GiB of memory. You can’t change the size.
- **No event table.** Logs appear in the Preview pane only while the dev server
  runs.
- **No caller’s rights.** Apps from the **Next.js App** template run
  caller’s rights queries with the preview’s own credentials, so results can
  differ from a deployed app.
- **No CLI command.** There’s no `snow app preview`. Preview runs from the
  Snowsight UI and from Cortex Code in Snowsight.
- **Crash limit.** After three crashes in a row, each within 10 seconds of
  starting, Snowflake stops restarting the dev server. See
  [Preview stops restarting after crashes](/developer-guide/snowflake-app-runtime/troubleshooting#label-snowflake-app-runtime-troubleshooting-preview-restarts).

For how preview works, see [Develop Snowflake App Runtime apps in Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces).

## Next steps

- Fix common errors: [Troubleshoot Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/troubleshooting).
