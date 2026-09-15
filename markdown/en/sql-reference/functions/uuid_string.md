Categories:
:   [String & binary functions](/sql-reference/functions-string) (General) , [Data generation functions](/sql-reference/functions-data-generation)

# UUID\_STRING

Generates either a version 4 (random) or version 5 (named) RFC 4122-compliant universally unique identifier (UUID)
as a formatted string.

## Syntax

Copy code

```
UUID_STRING()

UUID_STRING( '<uuid>' , '<name>' )
```

## Arguments

`'uuid'`
:   A valid UUID string. This value is the namespace used to generate the returned UUID.

`'name'`
:   The name used to generate the returned UUID.

## Returns

This function returns a 128-bit value, formatted as a string (VARCHAR data type).

## Usage notes

UUID\_STRING supports generating two versions of UUIDs, both compliant with RFC 4122:

- A version 4 (random) UUID is returned when no arguments are provided to the function. For random-number generation, the
  64-bit [Mersenne twister](http://en.wikipedia.org/wiki/Mersenne_twister) known as MT19937-64 is used.
- A version 5 (named) UUID can be produced by providing a `uuid` string (known as the namespace) as the first
  argument and a `name` string as the second argument.

## Examples

Generate a random UUID:

Copy code

```
SELECT UUID_STRING();
```

```
+--------------------------------------+
| UUID_STRING()                        |
|--------------------------------------|
| d47f4e30-306f-4940-8921-c154094df1a1 |
+--------------------------------------+
```

Generate a named UUID:

Copy code

```
SELECT UUID_STRING('fe971b24-9572-4005-b22f-351e9c09274d','foo');
```

```
+-----------------------------------------------------------+
| UUID_STRING('FE971B24-9572-4005-B22F-351E9C09274D','FOO') |
|-----------------------------------------------------------|
| dc0b6f65-fca6-5b4b-9d37-ccc3fde1f3e2                      |
+-----------------------------------------------------------+
```

Create a table and insert random UUIDs:

Copy code

```
CREATE OR REPLACE TABLE uuid_insert_test(random_uuid VARCHAR(36), test VARCHAR(10));

INSERT INTO uuid_insert_test (random_uuid, test) SELECT UUID_STRING(), 'test1';
INSERT INTO uuid_insert_test (random_uuid, test) SELECT UUID_STRING(), 'test2';
INSERT INTO uuid_insert_test (random_uuid, test) SELECT UUID_STRING(), 'test3';
INSERT INTO uuid_insert_test (random_uuid, test) SELECT UUID_STRING(), 'test4';
INSERT INTO uuid_insert_test (random_uuid, test) SELECT UUID_STRING(), 'test5';

SELECT * FROM uuid_insert_test;
```

```
+--------------------------------------+-------+
| RANDOM_UUID                          | TEST  |
|--------------------------------------+-------|
| 7745a0cf-d136-406b-9289-38072d242871 | test1 |
| 8c31e031-a6bf-479d-9abb-b7909f298ba1 | test2 |
| e65d5641-01c0-4126-b80d-c5ae6d4848be | test3 |
| bd02bf4e-fa5d-498d-8a9a-d38200f1ca30 | test4 |
| 4df2a34e-ad65-46b4-a51a-3eb9394aeb83 | test5 |
+--------------------------------------+-------+
```
