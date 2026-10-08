Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_REFERENCED\_OBJECT\_ID\_HASH

Returns the hash of the entity ID of the consumer object currently resolved by the reference.

This function is useful for an app to determine whether the object bound to a reference has changed. The app can save the value and then compare the current value to the previously known value.

## Syntax

Copy code

```
SYSTEM$GET_REFERENCED_OBJECT_ID_HASH('<reference_name>'[, '<alias>'])
```

## Arguments

**Required**

`'reference_name'`
:   The name of the reference as specified in the `manifest.yml` file of the app.

**Optional**

`'alias'`
:   The system-generated alias of the association. This argument is required for a multi-valued reference.
    To get the aliases of the associations for a reference, call
    [SYSTEM$GET\_ALL\_REFERENCES](/sql-reference/functions/system_get_all_references).

## Returns

Returns a `VARCHAR` value that contains the hexadecimal-encoded SHA-256 hash of the identifier of the consumer object.

## Usage notes

The hash identifies the object, not its data. Changing rows in the same table doesn’t change
the object identifier. Replacing the table with a different table of the same name changes
the identifier and therefore the hash.

## Examples

### Compare the object bound to a single-valued reference

This example assumes that the app has a single-valued `consumer_table` reference bound to an
existing consumer table. The following statements run in provider-written code executing in
the installed app’s context, such as the body of an app-owned stored procedure with owner’s
rights. They aren’t standalone statements for a consumer worksheet.

Get the identifier hash before initializing app state that depends on the consumer table:

Copy code

```
SELECT SYSTEM$GET_REFERENCED_OBJECT_ID_HASH('consumer_table');
```

The app persists this value in its own state. Before using that state in a later operation,
it retrieves the saved hash and compares it to the current hash. For example, the following
Snowflake Scripting fragment can be part of an app-owned procedure. The surrounding procedure
must declare `saved_object_hash` as a `VARCHAR` variable and load the previously persisted
hash before this block runs:

Copy code

```
DECLARE
  current_object_hash VARCHAR;
  reference_object_changed EXCEPTION (-20001, 'The referenced table was replaced.');
BEGIN
  current_object_hash := (SELECT SYSTEM$GET_REFERENCED_OBJECT_ID_HASH('consumer_table'));

  IF (saved_object_hash IS NULL OR current_object_hash <> saved_object_hash) THEN
    RAISE reference_object_changed;
  END IF;
END;
```

This example stops processing if the saved hash is missing or the consumer replaced the
table with a different table of the same name. An app can instead implement its own
replacement-handling logic, such as rebuilding table-dependent state before continuing.
The actual hash depends on the consumer object’s identifier.

### Get the hash for a multi-valued association

For a multi-valued reference, pass the association alias. For example, use this statement
in an app-owned procedure, replacing the illustrative UUID with an existing alias:

Copy code

```
SELECT SYSTEM$GET_REFERENCED_OBJECT_ID_HASH(
  'consumer_tables', '6f3b7c2a-9d41-4e8f-a625-1b0c7d9e2345'
);
```
