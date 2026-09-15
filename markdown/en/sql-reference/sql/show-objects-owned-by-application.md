# SHOW OBJECTS OWNED BY APPLICATION

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the objects owned by an app that exists outside the app.

See also:
:   [SHOW APPLICATIONS](/sql-reference/sql/show-applications)

## Syntax

Copy code

```
SHOW OBJECTS OWNED BY APPLICATION <app_name>
```

## Parameters

`app_name`
:   The name of the app whose objects you want to list.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MANAGE GRANTS | App | One of these privileges is required to view the objects owned by the app. |

Expand

Show lessSee more

## Output

| Column | Description |
| --- | --- |
| `created_on` | The timestamp when the object was created. |
| `name` | The name of the object owned by the app |
| `type` | The type of object, for example COMPUTE\_POOL. |

Expand

Show lessSee more

## Examples

Copy code

```
SHOW OBJECTS OWNED BY APPLICATION hello_snowflake_app;
```

```
+---------------------------------+----------------------+---------------------+
| created_on                      | name                 | object_type         |
|---------------------------------|----------------------|---------------------|
| 2024-11-20 17:56:08.887 -0800   | HELLO_SNOWFLAKE_APP  | COMPUTE_POOL        |
+---------------------------------+----------------------+---------------------+
```
