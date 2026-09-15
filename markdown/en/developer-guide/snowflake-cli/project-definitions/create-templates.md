# Create project definition file templates

In some situations, you might want to reference information already present in a project definition file in another place of the file. Snowflake CLI supports templating the project definition file.

Project definition file templates use the `<% … %>` syntax for specifying the templates. The following example uses the `env` section to define a name for a Streamlit application:

Copy code

```
definition_version: 2
env:
  name: "my-app"
entities:
  my_streamlit:
    type: "streamlit"
    identifier: <% ctx.env.name %>
```

The `<% ctx.env.name %>` syntax references a global context object that provides access to the project definition. The `ctx` object has the same structure as the project definition. You can access attributes of defined objects using dot notation. Example uses include:

- `<% ctx.entities.pkg.identifier %>` to access the name of a Native App package with ID *pkg*.
- `<% ctx.entities.function.stage_name %>` to access the stage name for a snowpark UDFs and procedures.
- `<% ctx.entities.my_streamlit.identifier %>` to access the Streamlit dashboard name.

You can override any variable defined in the `snowflake.yml` project definition file `env` section by setting a shell environment variable by the same case-sensitive name. For example, to override the name value defined in the example, you can execute the following shell command:

Copy code

```
export name="other"
```

## Access template defaults

Template defaults let you access default and automatically-generated fields from a project definition file, even if the fields are not explicitly defined. To illustrate, consider the following Snowflake Native App project definition file:

Copy code

```
definition_version: 2
entities:
  pkg:
    type: application package
    artifacts:
      - src: app/*
        dest: ./
  app:
    type: application
    from:
      target: pkg
```

This definition provides enough information to create a Snowflake Native App, so the default values for the application package and application instance are automatically generated when you create the application. You can then access these values using the following syntax:

> Copy code
>
> ```
> <% ctx.entities.app.identifier %>
> <% ctx.entities.pkg.identifier %>
> ```
