# Project definition files

A project definition file called `snowflake.yml` declares a directory as a Snowflake Native App project. It is a version-controlled file that resides at the root of a Snowflake Native App project directory and can either be created manually or by Snowflake CLI as part of project initialization. As long as you provide this structured file in the directory, you can use your own independent project structure and Snowflake CLI can discover the relevant files and carry out its functionality as usual.

For Native Apps, your `snowflake.yml` would look similar to the following:

Copy code

```
definition_version: 2
entities:
  pkg:
    type: application package
    identifier: <name_of_app_pkg>
    stage: app_src.stage
    manifest: app/manifest.yml
    artifacts:
      - src: app/*
        dest: ./
      - src: src/module-add/target/add-1.0-SNAPSHOT.jar
        dest: module-add/add-1.0-SNAPSHOT.jar
      - src: src/module-ui/src/*
        dest: streamlit/
    meta:
      role: <your_app_pkg_owner_role>
      warehouse: <your_app_pkg_warehouse>
      post_deploy:
        - sql_script: scripts/any-provider-setup.sql
        - sql_script: scripts/shared-content.sql
  app:
    type: application
    identifier: <name_of_app>
    from:
      target: pkg
    debug: <true|false>
    meta:
      role: <your_app_owner_role>
      warehouse: <your_app_warehouse>
```

## Common entity properties

The following table describes common properties available for project definition entities for Native Apps. See [Specify entities](/developer-guide/snowflake-cli/project-definitions/specify-entities) for more information on project definition entities.

**Common entity properties**

| Property | Definition |
| --- | --- |
| **type**  *required*, *string* | The type of entity to manage. For Snowflake Native App, valid values include:   - `application package`. For more information about application package properties, see [Application package entity properties](#label-cli-app-pkg-entity-props). - `application`. For more information about application properties, see [Application entity properties](#label-cli-app-entity-props). |
| **identifier**  *optional*, *string* | Optional Snowflake identifier for the entity, both unquoted and quoted identifiers are supported. To use quoted identifiers, include the surrounding quotes in the YAML value (for example, `’”My Native Application Package”’`).  If not specified, the entity ID in the project definition is used as the identifier. |
| **meta.warehouse**  *optional*, *string* | Warehouse used to run the scripts provided as part of `meta.post_deploy`, if any SQL commands within these scripts require use of a warehouse.  Default: Warehouse specified for the connection in the Snowflake CLI `config.toml` file.  Note  If you do not specify a warehouse, the application passes validation, but fails to install.  Typically, you specify this value in the `snowflake.local.yml` as described in [Project definition overrides](#project-definition-overrides). |
| **meta.role**  *optional*, *string* | Role to use when creating the entity and provider-side objects.  Note  If you do not specify a role, Snowflake CLI attempts to use the default role assigned to your user in your Snowflake account.  Typically, you specify this value in the `snowflake.local.yml` as described in [Project definition overrides](#project-definition-overrides).  Default: Role specified in the [Snowflake CLI connection](/developer-guide/snowflake-cli/connecting/connect) |
| **meta.post\_deploy**  *optional*, *sequence* | List of SQL scripts to execute after the entity has been created. The following example shows how to define these scripts in the project definition file:  Copy code  ``` definition_version: 2 entities:   myapp_pkg:     type: application package     ...     meta:       post_deploy:         - sql_script: scripts/post_deploy1.sql         - sql_script: scripts/post_deploy2.sql ```  These scripts are invoked by commands that create or update an entity. For example, running the `snow app deploy` command executes these scripts after creating or updating a package. They are also executed by `snow app run` if the application instance is not being directly installed from a version or release directive.  Caution  Post-deploy scripts execute SQL from your project directory and can access subdirectories of the current working directory. Only run `snow app deploy` and `snow app run` with projects and SQL scripts you trust.  You can also use templates in the post-deploy SQL scripts as well, as shown in the following sample script content:  Copy code  ``` GRANT reference_usage on database provider_data to share in entity <% fn.str_to_id(ctx.entities.myapp_pkg.identifier) %> ``` |
| **meta.use\_mixins**  *optional*, *sequence* | Names of mixins to apply to this entity. See [Project mixins](/developer-guide/snowflake-cli/project-definitions/specify-entities#label-cli-project-mixins) for more information |

Expand

Show lessSee more

## Application package entity properties

The following table describes common properties available for application package entities for Native Apps. See [Specify entities](/developer-guide/snowflake-cli/project-definitions/specify-entities) for more information on project definition entities.

**Properties for *application package* entities**

| Property | Definition |
| --- | --- |
| **type**  *required*, *string* | Must be `application package`. |
| **manifest**  *optional*, *string* | The location of the Snowflake Native App `manifest.yml` file in your project.  Note  With version 3.2, this property switched from required to optional. |
| **deploy\_root**  *optional*, *string* | Subdirectory at the root of your project where the build step copies the artifacts. Once copied to this location, you can deploy them to a Snowflake stage.  Default: `output/deploy` |
| **generated\_root**  *optional*, *string* | Subdirectory of the deploy root where Snowflake CLI writes generated files.  Default: `__generated` |
| **stage**  *optional*, *string* | Identifier of the stage that stores the application artifacts. The value uses the form `<schema_name>.<stage_name>`. The stage lives within the Application Package object. You can change the name to avoid name collisions.  Default: `app_src.stage` |
| **artifacts**  *required*, *sequence* | List of file source and destination pairs to add to the deploy root, as well as an optional Snowpark annotation processor. You can use the following artifact properties:   - `src`: Path to the code source file or files - `dest`: Path to the directory to deploy the artifacts.   Destination paths that reference directories must end with a `/`. A glob pattern’s destination that does not end with a `/` results in an error. If omitted, `dest` defaults to the same string as `src`.  You can also pass in a string for each item instead of a `dict`, in which case the value is treated as both `src` and `dest`.   - `processors`: Name of the processor to use to process the `src` code files. See [More information about artifacts processors](#label-cli-na-artifacts-processors) for more details.   If `src` refers to just one file (not a glob), `dest` can refer to a target `<path>` or a `<path/name>`.  You can also pass in a string for each item instead of a `dict`, in which case, the value is treated as both `src` and `dest`.  Example without a processor:  Copy code  ``` pkg:   artifacts:     - src: app/*       dest: ./     - src: streamlit/*       dest: streamlit/     - src: src/resources/images/snowflake.png       dest: streamlit/ ```  Example with a processor:  Copy code  ``` pkg:   artifacts:     - src: qpp/*       dest: ./       processors:           - name: snowpark             properties:               env:                 type: conda                 name: <conda_name> ``` |
| **distribution**  *optional*, *string* | Distribution of the application package created by the Snowflake CLI. When running `snow app` commands, Snowflake CLI warns you if the application package you are working with has a different value for distribution than is set in your resolved project definition.  Default: `Internal` |
| **scratch\_stage**  *optional*, *string* | Identifier of the stage that stores temporary scratch data used by Snowflake CLI. The value uses the form `<schema_name>.<stage_name>`. The stage lives within the Application Package object. You can change the name to avoid name collisions.  Default: `app_src.stage_snowflake_cli_scratch` |
| **stage\_subdirectory**  *optional*, *string* | Name of the folder for Snowflake CLI to add as a subdirectory under the stage to hold the artifacts specified in this Application Package Entity. If none are specified, the artifacts are uploaded to the root of the stage.  Default: `""` (empty string) |
| **enable\_release\_channels**  *optional*, *bool* | Whether to enable publishing this application package in [release channels](/developer-guide/snowflake-cli/native-apps/publish-app#label-snowcli-native-app-release-channel).  Default: Unset |

Expand

Show lessSee more

## Application entity properties

The following table describes common properties available for application entities for Native Apps. See [Specify entities](/developer-guide/snowflake-cli/project-definitions/specify-entities) for more information on project definition entities.

**Properties for *application* entities**

| Property | Definition |
| --- | --- |
| **type**  *required*, *string* | Must be `application`. |
| **from.target**  *required*, *string* | Application package from which to create this application entity. In the following example, `target` defines the name of an entity in the `snowflake.yml` file.  Copy code  ``` from:   target: my_pkg ``` |
| **telemetry.share\_mandatory\_events**  *optional*, *boolean* | Whether to enable event sharing at the application level. When this is set to `true`, all mandatory events are automatically shared with the application package provider.  Copy code  ``` telemetry:   share_mandatory_events: true ``` |
| **telemetry.optional\_shared\_events**  *optional*, *sequence* | List of optional events to share with the provider in addition to the mandatory events. All events listed here must be declared in the `configuration.telemetry_event_definitions` section of the `manifest.yml` file. This field is supported only when `share_mandatory_events` is set to `true`.  Copy code  ``` telemetry:   share_mandatory_events: true   optional_shared_events:     - DEBUG_LOGS ``` |
| **debug**  *optional*, *boolean* | Whether to enable debug mode when using a named stage to create an application.  Default: `true` |

Expand

Show lessSee more

### Sharing events with providers

Note

Snowflake CLI supports event sharing only in `snowflake.yml` files based on definition version 2 or later. If you currently use an earlier version, see [Migrating project definition files from version 1.x to 2.0](/developer-guide/snowflake-cli/project-definitions/migrate-projects).

[Event sharing](/developer-guide/native-apps/event-definition) allows applications to send telemetry events back to application package owners. When testing an application with an application package requiring event sharing, you must explicitly enable event sharing for the application installation to succeed.

To enable sharing of specific events, you must also have the events configured in the `configuration.telemetry_event_definitions` section in the `manifest.yml` file for the application package. You must also have the MANAGE EVENT SHARING global privilege to authorize event sharing for the application.

After event sharing is enabled in your application’s manifest, you must add a `telemetry` section to your `snowflake.yml` file that specifies the events you want to share from your application. The following code shows a sample `telemetry` section:

Copy code

```
definition_version: 2
entities:
  app:
    type: application
    from:
      target: pkg
    telemetry:
      share_mandatory_events: true
      optional_shared_events:
        - DEBUG_LOGS

...
```

The following examples illustrate different ways to share events in the `snowflake.yml` file. All of the examples are based on the following section in the application package’s `manifest.yml` file:

Copy code

```
configuration:
    telemetry_event_definitions:
        - type: ERRORS_AND_WARNINGS
          sharing: MANDATORY
        - type: DEBUG_LOGS
          sharing: OPTIONAL
```

- Authorize telemetry and share all mandatory events with the provider. In this case, only `ERRORS_AND_WARNINGS` events are shared.

  Copy code

  ```
  definition_version: 2
  entities:
    app:
   type: application
   from:
     target: pkg
   telemetry:
     share_mandatory_events: true
  ```
- Share both `DEBUG_LOGS` and `ERRORS_AND_WARNINGS` events with the application package provider. Setting `share_mandatory_events` to `true` enables sharing of mandatory `ERRORS_AND_WARNINGS` events, while the `optional_shared_events` section enables optional events like `DEBUG_LOGS`.

  Copy code

  ```
  definition_version: 2
  entities:
    app:
   type: application
   from:
     target: pkg
   telemetry:
     share_mandatory_events: true
     optional_shared_events:
       - DEBUG_LOGS
  ```

## More information about artifacts processors

If you include the `artifacts.processors` field in the project definition file, the `snow app bundle` command invokes custom processing for Python code files in the `src` directory or file.

This section covers a list of supported processors.

### Snowpark processor

Note

The Snowpark processor has been deprecated and will be removed in a future release.

One of the processors supported by Snowflake CLI is `snowpark`, which applies Snowpark annotation processing to Python files. The following code examples show the basic structure and syntax for different processing environments:

- To execute code in a conda environment, use the following:

  Copy code

  ```
  pkg:
    artifacts:
   - src: <some_src>
     dest: <some_dest>
     processors:
         - name: snowpark
           properties:
             env:
               type: conda
               name: <conda_name>
  ```

  where `<conda_name>` is the name of the conda environment containing the Python interpreter and the Snowpark library you want to use for Snowpark annotation processing.
- To execute code in a Python virtual environment, use the following:

  Copy code

  ```
  pkg:
    artifacts:
   - src: <some_src>
     dest: <some_dest>
     processors:
         - name: snowpark
           properties:
             env:
               type: venv
               path: <venv_path>
  ```

  where `<venv_path>` is the path of the Python virtual environment containing the Python interpreter and the Snowpark library you want to use for Snowpark annotation processing. The path can be absolute or relative to the project directory.
- To execute code in the currently active environment, use any of the following equivalent definitions:

  Copy code

  ```
  pkg:
    artifacts:
   - src: <some_src>
     dest: <some_dest>
     processors:
         - name: snowpark
           properties:
             env:
               type: current
  ```

  or

  Copy code

  ```
  pkg:
    artifacts:
   - src: <some_src>
     dest: <some_dest>
     processors:
         - name: snowpark
  ```

  or

  Copy code

  ```
  pkg:
    artifacts:
   - src: <some_src>
     dest: <some_dest>
     processors:
         - snowpark
  ```

For more information about custom processing, see [Automatic SQL code generation](/developer-guide/snowflake-cli/native-apps/bundle-app#label-cli-nativeapp-bundle-codegen) and the [snow app bundle](/developer-guide/snowflake-cli/command-reference/native-apps-commands/bundle-app) command.

### Templates processor

Snowflake Native App projects support templates in arbitrary files, which lets you expand templates in all files in an artifact’s `src` directory.
You can enable this feature by including a `templates` processor in the desired `artifacts` definition, as shown in the following example:

Copy code

```
definition_version: 2
entities:
  pkg:
    type: application package
    identifier: myapp_pkg
    artifacts:
      - src: app/*
        dest: ./
        processors:
          - templates
    manifest: app/manifest.yml
  app:
    type: application
    identifier: myapp_<% fn.get_username() %>
    from:
      target: pkg
```

When Snowflake CLI uploads the files to a stage, it automatically expands the templates before uploading them. For example, suppose your application contained an
`app/README.md` file with the following content that includes the `<% ctx.entities.pkg.identifier %>` template:

Copy code

```
This is a README file for application package <% ctx.entities.pkg.identifier %>.
```

The template is then expanded to the following before uploading the file to a stage:

Copy code

```
This is a README file for application package myapp_pkg.
```

## Project definition overrides

Though your project directory must have a `snowflake.yml` file, you can choose to customize the behavior of the Snowflake CLI by providing local overrides to `snowflake.yml`, such as a new role to test out your own application package. These overrides must be put in the `snowflake.local.yml` file that lives beside the base project definition. Snowflake suggests that you add it to your `.gitignore` file so it won’t be version-controlled by git. All templates provided by Snowflake already include it in the `.gitignore` file.

This overrides file must live in the same location as your `snowflake.yml` file.

The `snowflake.local.yml` file shares the exact schema as `snowflake.yml`, except that every value that was required is now optional, in addition to the already optional ones. The following shows a sample `snowflake.local.yml` file:

Copy code

```
entities:
  pkg:
    meta:
      role: <your_app_pkg_owner_role>
      name: <name_of_app_pkg>
      warehouse: <your_app_pkg_warehouse>
  app:
    debug: <true|false>
    meta:
      role: <your_app_owner_role>
      name: <name_of_app>
      warehouse: <your_app_warehouse>
```

Every `snow app` command prioritizes the parameters in this file over those set in base `snowflake.yml` configuration file. Sensible defaults already provide isolation between developers using the same Snowflake account to develop the same application project, so if you are just getting started we suggest not including an overrides file.

The final definition schema obtained after overriding `snowflake.yml` with `snowflake.local.yml` is called the resolved project definition.

### Limitations

Currently, Snowflake CLI does not support

- Multiple override files.
- A blank override file. Only create this file if you want to override a value from `snowflake.yml`.
