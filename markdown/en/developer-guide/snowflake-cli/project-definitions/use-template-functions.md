# Use template functions

To enable the concatenation of SQL identifiers such as database names and schema names, and to provide flexibility in using quoted or unquoted identifiers in different contexts, Snowflake CLI provides the following set of utility functions you can use in project template definition templates:

- [fn.concat\_ids()](/developer-guide/snowflake-cli/project-definitions/use-template-functions#label-cli-fn-concat-ids)
- [fn.str\_to\_id()](/developer-guide/snowflake-cli/project-definitions/use-template-functions#label-cli-fn-str-to-id)
- [fn.id\_to\_str()](/developer-guide/snowflake-cli/project-definitions/use-template-functions#label-cli-fn-id-to-str)
- [fn.get\_username()](/developer-guide/snowflake-cli/project-definitions/use-template-functions#label-cli-fn-get-username)
- [fn.sanitize\_id()](/developer-guide/snowflake-cli/project-definitions/use-template-functions#label-cli-fn-sanitize-id)

## `fn.concat_ids()`

- Input: one or more string arguments (SQL ID or plain string)
- Output: a valid SQL ID (quoted or unquoted)

The `fn.concat_ids()` function concatenates multiple string arguments into a single string representing a SQL ID (quoted or unquoted). If any of the input strings is a valid quoted identifier, it will be unescaped before the concatenation. The resulting string is then escaped and quoted if it contains non-SQL safe characters or if any of the input strings was a valid quoted identifier.

Examples:

- Calling `fn.concat_ids('id1_', '"quoted_id2"')` outputs `"id1_quoted_id2"` because one of the input values is a quoted identifier.
- Calling `fn.concat_ids('id1_', 'id2')` outputs `id1_id2` because none of the input values is a quoted identifier and none of the input values contains non-SQL safe characters.

## `fn.str_to_id()`

- Input: one or more string arguments (SQL ID or plain string)
- Output: a valid SQL ID (quoted or unquoted)

The `fn.str_to_id()` function returns a string as an ID. If the input string contains a valid quoted or unquoted identifier, the function returns it as is. However, if the input string contains unsafe SQL characters that are not properly quoted, the function returns a quoted ID that escapes the unsafe characters.

Examples:

- Calling `fn.str_to_id('id1')` returns `id1` because it is a valid unquoted identifier.
- Calling `fn.str_to_id('unsafe"id')` returns `"unsafe""id"` because it contains unsafe SQL characters.

## `fn.id_to_str()`

- Input: one string argument (SQL ID or plain string)
- Output: a plain string

If the input is a valid SQL ID, the function returns an unescaped plain string. Otherwise, the function returns the input string as is.

Examples:

- Calling `fn.id_to_str('id1')` returns `id1` because it is already unquoted.
- Calling `fn.id_to_str('"quoted""id.example"')` returns `quoted"id.example`.

## `fn.get_username()`

- Input: one optional string containing the fallback value
- Output: current username detected from the operating system

Returns the current username from the operating system environment variables. If the current username is not found or is empty, it will either return an empty value or use the fallback value if one is provided.

Examples:

- `fn.get_username('default_user')` returns the current username if found, otherwise, it returns `default_user`.

## `fn.sanitize_id()`

- Input: one string argument
- Output: a valid non-quoted SQL ID

The function `fn.sanitize_id()` removes any unsafe SQL characters from the input and returns it as a valid unquoted SQL ID. If the result does not start with a letter or an underscore, it appends an underscore to it. For very long strings, the function truncates the string to 255 characters.

Examples:

- When using `fn.sanitize_id('Some.id"With_Special_Chars')` the output is `SomeidWith_Special_Chars`.
- When using `fn.sanitize_id('1abc')` the output is `_1abc`.

## Sample use case

The following example shows how to use these functions in `snowflake.yml` project definition files:

Copy code

```
definition_version: 2
entities:
  pkg:
    type: application package
    identifier: <% fn.concat_ids(ctx.env.app_name, ctx.env.pkg_suffix) %>
    artifacts:
      - src: app/*
        dest: ./
  app:
    type: application
    identifier: <% fn.concat_ids(ctx.env.app_name, ctx.env.app_suffix) %>

env:
  app_name: myapp_base_name_<% fn.sanitize_id(fn.get_username()) %>
  app_suffix: _app_instance
  pkg_suffix: _pkg
```

The following example illustrates how to use the functions in a SQL file:

Copy code

```
DESC APPLICATION <% fn.str_to_id(ctx.entities.app.identifier) %>;
DESC APPLICATION PACKAGE <% fn.str_to_id(ctx.entities.pkg.identifier) %>;
```
