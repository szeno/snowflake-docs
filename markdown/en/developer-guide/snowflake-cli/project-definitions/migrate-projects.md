# Migrating project definition files from version 1.x to 2.0

To convert a version 1.x project definition file to the version 2 format, do the following:

1. Go to your project directory that contains the version 1.x `snowflake.yml` file.
2. Enter the `snow helpers v1-to-v2` command.
   - If the version 1.x file conversion succeeds, the command displays a message similar to the following:

     Copy code

     ```
     cd <project-directory>
     snow helpers v1-to-v2
     ```

     ```
     Project definition migrated to version 2.
     ```
   - If your project definition file is already updated to version 2, the command displays the following message:

     Copy code

     ```
     cd <project-directory>
     snow helpers v1-to-v2
     ```

     ```
     Project definition is already at version 2.
     ```

> - If you try to convert a project file that contains a *snowflake.local.yml* file, without using the `--[no]-migrate-local-overrides` option, the command generates an error similar to the following:
>
> > - If you try to convert a project file that contains templates, without using the `--accept-templates` option, the command generates an error similar to the following:
> >
> >   Copy code
> >
> >   ```
> >   cd <project-directory>
> >   snow helpers v1-to-v2
> >   ```
> >
> >   ```
> >   +- Error-------------------------------------------------------------------+
> >   | snowflake.local.yml file detected, please specify                        |
> >   | --migrate-local-overrides to include or --no-migrate-local-overrides to  |
> >   | exclude its values.                                                      |
> >   +--------------------------------------------------------------------------+
> >   ```
> > - If you convert a project definition file that contains templates, and use the `--accept-templates` option, the command converts the file and displays a warning message similar to the following:
> >
> >   Copy code
> >
> >   ```
> >   cd <project-directory>
> >   snow helpers v1-to-v2
> >   ```
> >
> >   ```
> >   WARNING  snowflake.cli._plugins.workspace.commands:commands.py:60 Your V1 definition contains templates. We cannot guarantee the correctness of the migration.
> >   Project definition migrated to version 2
> >   ```

## Convert Native App projects

This section shows an example from a V1 to V2 conversion of a Snowflake Native App project, lists the changes in property names, and offers some tips to help with migration.

### Snowflake Native App conversion example

**Native Apps project conversion example**

| V1 project file | V2 project file |
| --- | --- |
| Copy code  ``` definition_version: 1 native_app:   name: myapp   source_stage: app_src.stage   artifacts:     - src: app/*       dest: ./       processors:         - native app setup         - name: templates           properties:             foo: bar   package:     role: pkg_role     distribution: external   application:     name: myapp_app     warehouse: app_wh ``` | Copy code  ``` definition_version: 2 entities:   pkg:     type: application package     meta:       role: pkg_role     identifier: <% fn.concat_ids('myapp', '_pkg_', fn.sanitize_id(fn.get_username('unknown_user')) | lower) %>     manifest: app/manifest.yml     artifacts:     - src: app/*       dest: ./       processors:       - name: native app setup       - name: templates         properties:           foo: bar     stage: app_src.stage   app:     meta:       warehouse: app_wh     identifier: myapp_app     type: application     from:       target: pkg ``` |

Expand

Show lessSee more

### Native App project definition V1 to V2 property changes

**Native App project definition V1 to V2 property changes**

| V1 property | V2 property |
| --- | --- |
| `native_app.name` | No equivalent. Use a template variable to port, if required. |
| `native_app.deploy_root` | `<package entity>.deploy_root` |
| `native_app.generated_root` | `<package entity>.generated_root` |
| `native_app.bundle_root` | `<package entity>.bundle_root` |
| `native_app.source_stage` | `<package entity>.source_stage` |
| `native_app.scratch_stage` | `<package entity>.scratch_stage` |
| `native_app.artifacts` | `<package entity>.artifacts` |
| `native_app.application.debug` | `<application entity>.debug` |
| `native_app.application.name` | `<application entity>.identifier` |
| `native_app.application.post_deploy` | `<application entity>.meta.post_deploy` (see above notes) |
| `native_app.application.role` | `<application entity>.meta.role` |
| `native_app.application.warehouse` | `<application entity>.meta.warehouse` |
| `native_app.package.distribution` | `<package entity>.distribution` |
| `native_app.package.name` | `<package entity>.identifier` |
| `native_app.package.post_deploy` | `<package entity>.meta.post_deploy` (see above notes) |
| `native_app.package.role` | `<package entity>.meta.role` |
| `native_app.package.scripts` | `<package entity>.meta.post_deploy` (see above notes) |
| `native_app.package.warehouse` | `<package entity>.meta.warehouse` |

Expand

Show lessSee more

### Migration tips

- When migrating Snowflake Native App package scripts, the `v1-to-v2` command converts them to `package post-deploy` hooks and replaces `{{package_name}}` in the package script file with the equivalent template expression.
- When migrating existing template expressions, `ctx.native_app`, `ctx.streamlit`, and `ctx.snowpark` variables are no longer
  accepted. The `v1-to-v2` command with equivalent template expressions that reference the specific entity name instead.
  For example, `ctx.native_app.package.name` could be replaced with `ctx.entities.pkg.identifier` if the package was migrated to an entity named `pkg` in the `snowflake.yml` file.

## Convert Streamlit projects

This section shows an example from a V1 to V2 conversion of a Streamlit project, lists the changes in property names, and offers some tips to help with migration.

### Streamlit conversion example

**Streamlit project conversion example**

| V1 project file | V2 project file |
| --- | --- |
| Copy code  ``` definition_version: 1 streamlit:   name: test_streamlit   stage: streamlit   query_warehouse: test_warehouse   main_file: "streamlit_app.py"   title: "My Fancy Streamlit" ``` | Copy code  ``` definition_version: 2 entities:   test_streamlit:     identifier:       name: test_streamlit     type: streamlit     title: My Fancy Streamlit     query_warehouse: test_warehouse     main_file: streamlit_app.py     pages_dir: None     stage: streamlit     artifacts:     - streamlit_app.py ``` |

Expand

Show lessSee more

### Streamlit project definition V1 to V2 property changes

**Streamlit project definition V1 to V2 property changes**

| V1 property | V2 property |
| --- | --- |
| `streamlit.name` | `<streamlit entity>.identifier.name` |
| `streamlit.schema` | `<streamlit entity>.identifier.schema` |
| `streamlit.database` | `<streamlit entity>.identifier.database` |
| `streamlit.comment` | `<streamlit entity>.comment` |
| `streamlit.title` | `<streamlit entity>.title` |
| `streamlit.query_warehouse` | `<streamlit entity>.query_warehouse` |
| `streamlit.main_file` | `<streamlit entity>.main_file` and `<streamlit entity>.artifacts` |
| `streamlit.stage` | `<streamlit entity>.stage` |
| `streamlit.env_file` | `<streamlit entity>.artifacts` |
| `streamlit.pages_dir` | `<streamlit entity>.pages_dir` and `<streamlit entity>.artifacts` |
| `streamlit.additional_source_files` | `<streamlit entity>.artifacts` |

Expand

Show lessSee more

### Streamlit migration tips

None.

## Convert Snowpark projects

This section shows an example from a V1 to V2 conversion of a Snowpark project, lists the changes in property names, and offers some tips to help with migration.

### Snowpark conversion example

**Snowpark project conversion example**

| V1 project file | V2 project file |
| --- | --- |
| Copy code  ``` definition_version: 1 snowpark:   project_name: "my_snowpark_project"   stage_name: "dev_deployment"   src: "app/"   functions:     - name: func1       handler: "app.func1_handler"       signature:         - name: "a"           type: "string"           default: "default value"         - name: "b"           type: "variant"       returns: string       runtime: 3.10   procedures:     - name: procedureName       handler: "hello"       signature:         - name: "name"           type: "string"       returns: string ``` | Copy code  ``` definition_version: 2 entities:   procedureName:     imports: []     external_access_integrations: []     secrets: {}     meta:       use_mixins:       - snowpark_shared     identifier:       name: procedureName     handler: hello     returns: string     signature:     - name: name       type: string     stage: dev_deployment     artifacts:     - src: app       dest: my_snowpark_project     type: procedure     execute_as_caller: false   func1:     imports: []     external_access_integrations: []     secrets: {}     meta:       use_mixins:       - snowpark_shared     identifier:       name: func1     handler: app.func1_handler     returns: string     signature:     - name: a       type: string       default: default value     - name: b       type: variant     runtime: '3.10'     stage: dev_deployment     artifacts:     - src: app       dest: my_snowpark_project     type: function mixins:   snowpark_shared:     stage: dev_deployment     artifacts:     - src: app/       dest: my_snowpark_project ``` |

Expand

Show lessSee more

### Snowpark project definition V1 to V2 property changes

**Snowpark project definition V1 to V2 property changes**

| V1 property | V2 property |
| --- | --- |
| `snowpark.project_name` | `<function or procedure entity>.artifacts.dest` for each function and/or procedure migrated from the project. See above notes regarding Snowpark migration. Each function or procedure should declare an artifact with `dest` defined as the `snowpark.project_name` value, and `src` defined as the `snowpark.src` value. Use of a mixin is recommended. |
| `snowpark.stage_name` | `<function or procedure entity>.stage` for each function and/or procedure migrated from the project. |
| `snowpark.src` | `<function or procedure entity>.artifacts.src` for each function and/or procedure migrated from the project. (see `snowpark.project_name above`) |
| `snowpark.functions` (list) | `<function entities> (top-level)` |
| `snowpark.procedures` (list) | `<procedure entities> (top-level)` |

Expand

Show lessSee more

**Snowpark function and procedure definition V1 to V2 property changes**

| V1 property | V2 property |
| --- | --- |
| `name` | `identifier.name` |
| `schema` | `identifier.schema` |
| `database` | `identifier.database` |
| `handler` | `handler` |
| `returns` | `returns` |
| `signature` | `signature` |
| `runtime` | `runtime` |
| `external_access_integrations` | `external_access_integrations` |
| `secrets` | `secrets` |
| `imports` | `imports` |
| `execute_as_caller` | `execute_as_caller` (only for procedures) |

Expand

Show lessSee more

### Snowpark migration tips

- When migrating Snowpark projects, each function (from the `snowpark.functions` array) or procedure (from the `snowpark.procedures` array) maps to a top-level entity.
- All top-level Snowpark project properties (e.g. `src`) are now defined for each function and procedure. To reduce duplication,
  Snowflake recommends that you declare a `mixin` and include it in each of the migrated function and procedure entities.
