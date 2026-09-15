# DROP CONTACT

Removes the specified [contact](/user-guide/contacts-using) from the current schema.

See also:
:   [CREATE CONTACT](/sql-reference/sql/create-contact) , [ALTER CONTACT](/sql-reference/sql/alter-contact), [SHOW CONTACTS](/sql-reference/sql/show-contacts)

## Syntax

Copy code

```
DROP CONTACT <name>
```

## Parameters

`name`
:   Specifies the identifier of the contact to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

You must have the OWNERSHIP privilege on a contact to drop it.

## Examples

The following example drops the contact named `mycontact`:

Copy code

```
DROP CONTACT mycontact;
```

```
+---------------------------------+
| status                          |
|---------------------------------|
| MYCONTACT successfully dropped. |
+---------------------------------+
```
