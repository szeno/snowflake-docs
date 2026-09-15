# DROP APPLICATION PACKAGE

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Removes an application package from the system in the Native Apps Framework.

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package), [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package), [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages),

## Syntax

Copy code

```
DROP APPLICATION PACKAGE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the application package to drop. If the identifier contains spaces, special characters, or mixed-case characters, the entire string must be enclosed in double quotes. Identifiers
    enclosed in double quotes are also case-sensitive.

## Usage notes

- An application package can only be dropped if it is not currently associated with a listing.
- After you run this command, the application package is dropped and becomes unavailable within the
  provider account.

  Any application created from the application package remains visible to the consumer, but is otherwise inaccessible.
  Any attempt to access the application results in an error indicating the application package has been removed.
- A consumer must explicitly run [DROP APPLICATION](/sql-reference/sql/drop-application) to ensure that objects owned by the application
  have been appropriately transferred to other roles or removed.
- UNDROP is not supported for APPLICATION PACKAGE objects. Once dropped, an application package cannot be recovered.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Copy code

```
DROP APPLICATION PACKAGE hello_snowflake_app;
```

```
+-------------------------------------------+
| status                                    |
|-------------------------------------------|
| hello_snowflake_app successfully dropped. |
+-------------------------------------------+
```
