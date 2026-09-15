# Sep 01, 2026: Snowflake App Runtime (*General availability*)

[Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime)
is now generally available and is no longer in
[Preview](/release-notes/preview-features).

Build and deploy Node.js web applications (with a focus on Next.js) directly on
Snowflake using [Cortex Code](/user-guide/cortex-code/cortex-code-cli) or the
[Snowflake CLI](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/overview).
Describe an app in natural language, test it locally, and deploy to a live,
SSO-backed URL. Python support is planned.

This release includes the following capabilities:

- A single [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) manifest
  for deploy and remote-build configuration, including named
  [targets](/developer-guide/snowflake-app-runtime/deploy-targets) and
  [personal databases](/user-guide/personal-databases).
- Query Snowflake as the service or as the signed-in user. See
  [Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake).
- SQL commands for Application Services and artifact repositories. See
  [Snowflake Apps SQL commands](/sql-reference/commands-snowflake-apps).
- Sharing, privileges, and account administrator setup. See
  [Access control for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/access-control) and
  [Account administrator setup for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/account-admin-setup).

Snowflake App Runtime is available in Amazon Web Services (AWS), Microsoft Azure,
and Google Cloud commercial regions. It isn’t available in government regions or
on trial accounts.

For more information, see
[Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime).
