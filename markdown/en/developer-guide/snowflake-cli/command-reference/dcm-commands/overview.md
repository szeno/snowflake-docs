# snow dcm commands

Snowflake CLI supports the following commands for managing Snowflake DCM project objects:

- [snow dcm create](/developer-guide/snowflake-cli/command-reference/dcm-commands/create)
- [snow dcm deploy](/developer-guide/snowflake-cli/command-reference/dcm-commands/deploy)
- [snow dcm describe](/developer-guide/snowflake-cli/command-reference/dcm-commands/describe)
- [snow dcm drop](/developer-guide/snowflake-cli/command-reference/dcm-commands/drop)
- [snow dcm drop-deployment](/developer-guide/snowflake-cli/command-reference/dcm-commands/drop-deployment)
- [snow dcm list](/developer-guide/snowflake-cli/command-reference/dcm-commands/list)
- [snow dcm list-deployments](/developer-guide/snowflake-cli/command-reference/dcm-commands/list-deployments)
- [snow dcm plan](/developer-guide/snowflake-cli/command-reference/dcm-commands/plan)
- [snow dcm preview](/developer-guide/snowflake-cli/command-reference/dcm-commands/preview)
- [snow dcm purge](/developer-guide/snowflake-cli/command-reference/dcm-commands/purge)
- [snow dcm test](/developer-guide/snowflake-cli/command-reference/dcm-commands/test)

## Project configuration (manifest.yml)

DCM projects use a `manifest.yml` file to define project configuration. For more details, see [DCM Projects files and templates](/user-guide/dcm-projects/dcm-projects-files).

### Project identifier resolution

Most DCM commands accept an optional project identifier argument and a `--target` option. The project name is resolved as follows:

1. If a project identifier is provided as an argument, it is used directly.
2. If `--target` is specified, the `project_name` from that target in `manifest.yml` is used.
3. If neither is provided, the `default_target` from `manifest.yml` is used.

The selected target continues to supply its templating configuration when you pass an explicit project identifier. The CLI still resolves
the manifest and source files.

Targets don’t select the authenticated connection, account, or active role. Use global connection options such as `--connection` and
`--role` separately. The CLI warns when the connected account doesn’t match the target’s `account_identifier` or, during project creation,
when the current role doesn’t match `project_owner`; it doesn’t switch the account or assume the owner role.

**Examples:**

Copy code

```
# Use default_target from manifest.yml
snow dcm deploy

# Use target from manifest.yml
snow dcm deploy --target DEV

# Explicit project name with fully qualified identifier
snow dcm deploy MY_DB.MY_SCHEMA.MY_PROJECT
```

The `--from` option specifies the directory containing the `manifest.yml` and project source files. If omitted, the current directory is used.

Note

Project identifiers can be specified as a fully qualified name (`MY_DB.MY_SCHEMA.MY_PROJECT`) or as a simple name (`MY_PROJECT`). When using a simple name, the database and schema are derived from the active connection context. Using fully qualified names is recommended to avoid ambiguity.
