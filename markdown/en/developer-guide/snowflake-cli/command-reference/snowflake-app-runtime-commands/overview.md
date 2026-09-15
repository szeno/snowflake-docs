# Snowflake Apps CLI commands

The Snowflake CLI provides `snow app` subcommands for creating, deploying, and
managing Snowflake App Runtime projects. When you build with
[Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) or
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps), the bundled
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill runs `snow app` commands for you as you scaffold, deploy, or manage apps from chat.

`snow app` commands support both Snowflake Native Apps and Snowflake App Runtime.
The CLI selects the correct flow automatically.

Use the latest Snowflake CLI. Confirm with
[`snow helpers check-version`](/developer-guide/snowflake-cli/command-reference/helpers-commands/check-version).
If that command isn’t recognized, upgrade before you rely on `app.yml`. An older
CLI ignores the deployment keys in `app.yml` and still expects `snowflake.yml`.

For Snowflake App Runtime, use [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml).
Named `targets` are optional; pass `--target` only when the file defines them.
Native App projects use `snowflake.yml`; see
[snow app commands](/developer-guide/snowflake-cli/command-reference/native-apps-commands/overview).
If the project still has a `snowflake-app` entity, see
[Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml).

These pages document the Snowflake App Runtime behavior of each command.

## Project definition

For the structure of `app.yml`, see the
[app.yml reference](/developer-guide/snowflake-app-runtime/app-yml).

## Project setup

- [snow app setup](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/setup): Initialize an `app.yml` for a new Snowflake App Runtime project

## Deployment

- [snow app deploy](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy): Upload source, build remotely, and create or alter the Application Service
- [snow app bundle](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/bundle): Copy resolved artifacts into a local output directory for inspection
- [snow app validate](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/validate): Check that the project can be bundled and the target database and schema exist

## Lifecycle management

- [snow app open](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/open): Open the deployed app in a browser
- [snow app events](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/events): Fetch recent container logs
- [snow app teardown](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/teardown): Drop the Application Service and clean up associated objects
