# DROP APPLICATION

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Removes an application from the system in the Native Apps Framework.

See also:
:   [ALTER APPLICATION](/sql-reference/sql/alter-application), [CREATE APPLICATION](/sql-reference/sql/create-application),
    [SHOW APPLICATIONS](/sql-reference/sql/show-applications)

## Syntax

Copy code

```
DROP APPLICATION [ IF EXISTS ] <name> [ CASCADE ]
```

## Required parameters

`name`
:   Specifies the identifier for the application object to drop. If the identifier contains spaces,
    special characters, or mixed-case characters, the entire string must be enclosed in double
    quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Optional parameters

`CASCADE`
:   Drops the application object and all objects owned by the app, including tables with primary or unique
    keys that are referenced by foreign keys in other tables.

    If `CASCADE` is not specified, this command returns an error if the app owns
    objects outside of itself.

    If `CASCADE` is specified, all objects owned by the app are dropped, even if those
    objects contain other objects owned by the consumer. For example, if the consumer transfers
    ownership of a schema or table to an account role, but leaves the parent database owned
    by the app, running this command with `CASCADE` also drops those objects.

    To retain objects owned by the application, use the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership)
    command to transfer ownership of those objects, then run this command without `CASCADE`.

## Usage notes

- This command can be run by the app owner or a user with the MANAGE GRANTS privilege on the
  app.
- All app roles are dropped when the application object is dropped. Any access granted
  by those roles on objects in the consumer account is lost.
- UNDROP is not supported for APPLICATION objects. Once dropped, an application cannot be recovered.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Copy code

```
DROP APPLICATION hello_snowflake_app;
```

```
+-------------------------------------------+
| status                                    |
|-------------------------------------------|
| hello_snowflake_app successfully dropped. |
+-------------------------------------------+
```
