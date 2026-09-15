Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SHOW\_SENSITIVE\_DATA\_MONITORED\_ENTITIES

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns a JSON array of databases or schemas that are associated with a classification profile, which indicates that objects in these
entities are monitored by [sensitive data classification](/user-guide/classify-intro).

## Syntax

Copy code

```
SYSTEM$SHOW_SENSITIVE_DATA_MONITORED_ENTITIES( [ '<entity_type>' ] )
```

## Arguments

`'entity_type'`
:   Optional. A string specifying the type of entity to return. Possible values are `DATABASE` and `SCHEMA`.

    If omitted, returns all entities monitored by sensitive data classification.

## Returns

A JSON string containing an array of monitored entities and their associated classification profiles. Each object in the array contains
the following fields:

- `name`: Name of the monitored entity (that is, a database or schema).
- `type`: Type of the entity (DATABASE or SCHEMA).
- `profile_name`: Fully qualified name of the associated classification profile.

## Usage notes

- Only objects associated with a classification profile are shown.
- The current role must have access to both the entity and the classification profile associated with it for the entity to be included in
  the output.

## Examples

Show all databases that are monitored by sensitive data classification:

Copy code

```
SELECT SYSTEM$SHOW_SENSITIVE_DATA_MONITORED_ENTITIES('DATABASE');
```

```
[
{"name":"TESTDB","type":"DATABASE","profile_name":"TESTDB.TESTSCHEMA.MY_CLASSIFICATION_PROFILE"},
{"name":"TEST","type":"DATABASE","profile_name":"TEST.PUBLIC.TEST_PROFILE"}
]
```

Show all schemas that are monitored by sensitive data classification:

Copy code

```
SELECT SYSTEM$SHOW_SENSITIVE_DATA_MONITORED_ENTITIES('SCHEMA');
```

```
[
{"name":"TESTDB.TESTSCHEMA","type":"SCHEMA","profile_name":"TESTDB.TESTSCHEMA.MY_CLASSIFICATION_PROFILE"}
]
```

Show all entities (databases and schemas) that are monitored by sensitive data classification:

Copy code

```
SELECT SYSTEM$SHOW_SENSITIVE_DATA_MONITORED_ENTITIES();
```

```
[
{"name":"TESTDB","type":"DATABASE","profile_name":"TESTDB.TESTSCHEMA.MY_CLASSIFICATION_PROFILE"},
{"name":"TESTDB.TESTSCHEMA","type":"SCHEMA","profile_name":"TESTDB.TESTSCHEMA.TEST_PROFILE"}
]
```
