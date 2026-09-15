Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# OBJECT\_DELETE

Returns an object containing the contents of the input (that is, source) object with
one or more keys removed.

## Syntax

Copy code

```
OBJECT_DELETE( <object>, <key1> [, <key2>, ... ] )
```

## Arguments

`object`
:   The source object.

`key1`, `key2`
:   Keys to be omitted from the returned object.

## Returns

This function returns a value of type OBJECT.

## Usage notes

For [structured OBJECTs](/sql-reference/data-types-structured):

- For the arguments that are keys, you must specify constants.
- If the specified key isn’t part of the OBJECT type definition, the call fails. For example, the following call fails because
  the OBJECT value doesn’t contain the specified key `zip_code`:

  Copy code

  ```
  SELECT OBJECT_DELETE( {'city':'San Mateo','state':'CA'}::OBJECT(city VARCHAR,state VARCHAR), 'zip_code' );
  ```

  ```
  093201 (23001): Function OBJECT_DELETE: expected structured object to contain field zip_code but it did not.
  ```
- The function returns a structured OBJECT value. The type of the OBJECT value excludes the deleted key. For example, suppose that you
  remove the `city` key:

  Copy code

  ```
  SELECT
    OBJECT_DELETE(
   {'city':'San Mateo','state':'CA'}::OBJECT(city VARCHAR,state VARCHAR),
   'city'
    ) AS new_object,
    SYSTEM$TYPEOF(new_object);
  ```

  The function returns an OBJECT value of the type `OBJECT(state VARCHAR)`, which doesn’t include the `city` key.

  ```
  +-----------------+----------------------------+
  | NEW_OBJECT      | SYSTEM$TYPEOF(NEW_OBJECT)  |
  |-----------------+----------------------------|
  | {               | OBJECT(state VARCHAR)[LOB] |
  |   "state": "CA" |                            |
  | }               |                            |
  +-----------------+----------------------------+
  ```
- If the function removes all keys from the OBJECT value, the function returns an empty structured OBJECT value of the type `OBJECT()`.

  Copy code

  ```
  SELECT
    OBJECT_DELETE(
   {'state':'CA'}::OBJECT(state VARCHAR),
   'state'
    ) AS new_object,
    SYSTEM$TYPEOF(new_object);
  ```

  ```
  +------------+---------------------------+
  | NEW_OBJECT | SYSTEM$TYPEOF(NEW_OBJECT) |
  |------------+---------------------------|
  | {}         | OBJECT()[LOB]             |
  +------------+---------------------------+
  ```

  When the type of a structured OBJECT value includes key-value pairs, the names and types of those pairs are included in parentheses
  in the type (for example, OBJECT(city VARCHAR)). Because an empty structured OBJECT value contains no key-value pairs, the
  parentheses are empty.

## Examples

This query returns an object that excludes the keys `a` and `b` from the source object:

Copy code

```
SELECT OBJECT_DELETE(OBJECT_CONSTRUCT('a', 1, 'b', 2, 'c', 3), 'a', 'b') AS object_returned;
```

```
+-----------------+
| OBJECT_RETURNED |
|-----------------|
| {               |
|   "c": 3        |
| }               |
+-----------------+
```

Create a table and insert rows with OBJECT values. This example uses [OBJECT constants](/sql-reference/data-types-semistructured#label-object-constant)
in the INSERT statements.

Copy code

```
CREATE OR REPLACE TABLE object_delete_example (
  id INTEGER,
  ov OBJECT);

INSERT INTO object_delete_example (id, ov)
  SELECT
    1,
    {
      'employee_id': 1001,
      'employee_date_of_birth': '12-10-2003',
      'employee_contact':
        {
          'city': 'San Mateo',
          'state': 'CA',
          'phone': '800-555-0100'
        }
    };

INSERT INTO object_delete_example (id, ov)
  SELECT
    2,
    {
      'employee_id': 1002,
      'employee_date_of_birth': '01-01-1990',
      'employee_contact':
        {
          'city': 'Seattle',
          'state': 'WA',
          'phone': '800-555-0101'
        }
    };
```

Query the table to see the data:

Copy code

```
SELECT * FROM object_delete_example;
```

```
+----+-------------------------------------------+
| ID | OV                                        |
|----+-------------------------------------------|
|  1 | {                                         |
|    |   "employee_contact": {                   |
|    |     "city": "San Mateo",                  |
|    |     "phone": "800-555-0100",              |
|    |     "state": "CA"                         |
|    |   },                                      |
|    |   "employee_date_of_birth": "12-10-2003", |
|    |   "employee_id": 1001                     |
|    | }                                         |
|  2 | {                                         |
|    |   "employee_contact": {                   |
|    |     "city": "Seattle",                    |
|    |     "phone": "800-555-0101",              |
|    |     "state": "WA"                         |
|    |   },                                      |
|    |   "employee_date_of_birth": "01-01-1990", |
|    |   "employee_id": 1002                     |
|    | }                                         |
+----+-------------------------------------------+
```

To delete the `employee_date_of_birth` key from the query output, execute the following query:

Copy code

```
SELECT id,
       OBJECT_DELETE(ov, 'employee_date_of_birth') AS contact_without_date_of_birth
  FROM object_delete_example;
```

```
+----+-------------------------------+
| ID | CONTACT_WITHOUT_DATE_OF_BIRTH |
|----+-------------------------------|
|  1 | {                             |
|    |   "employee_contact": {       |
|    |     "city": "San Mateo",      |
|    |     "phone": "800-555-0100",  |
|    |     "state": "CA"             |
|    |   },                          |
|    |   "employee_id": 1001         |
|    | }                             |
|  2 | {                             |
|    |   "employee_contact": {       |
|    |     "city": "Seattle",        |
|    |     "phone": "800-555-0101",  |
|    |     "state": "WA"             |
|    |   },                          |
|    |   "employee_id": 1002         |
|    | }                             |
+----+-------------------------------+
```

To query the `employee_contact` nested object, remove the `phone` key from it, and
return only the nested inner key-value pairs, execute the following query:

Copy code

```
SELECT id,
       OBJECT_DELETE(ov:"employee_contact", 'phone') AS contact_without_phone
  FROM object_delete_example;
```

```
+----+------------------------+
| ID | CONTACT_WITHOUT_PHONE  |
|----+------------------------|
|  1 | {                      |
|    |   "city": "San Mateo", |
|    |   "state": "CA"        |
|    | }                      |
|  2 | {                      |
|    |   "city": "Seattle",   |
|    |   "state": "WA"        |
|    | }                      |
+----+------------------------+
```

To query the `employee_contact` nested object, remove the `phone` key from it, and
return the full object instead of just the nested inner key-value pairs, run a query
that performs the following actions:

- Call the [OBJECT\_INSERT](/sql-reference/functions/object_insert) function and specify the `ov` column
  for the first argument. The function starts with the whole object in each row.
- For the second argument in the OBJECT\_INSERT call, specify `employee_contact` for the existing key to update.
- For the third argument in the OBJECT\_INSERT call, call the OBJECT\_DELETE function to remove the `phone` key from the nested object.
- For the last argument in the OBJECT\_INSERT call, specify `true` to replace the old object with the new one.

Execute the following query to perform these actions:

Copy code

```
SELECT id,
       OBJECT_INSERT(
         ov,
         'employee_contact',
         OBJECT_DELETE(
           ov:employee_contact,
           'phone'
         ),
         true
      ) AS full_object_without_phone
  FROM object_delete_example;
```

```
+----+-------------------------------------------+
| ID | FULL_OBJECT_WITHOUT_PHONE                 |
|----+-------------------------------------------|
|  1 | {                                         |
|    |   "employee_contact": {                   |
|    |     "city": "San Mateo",                  |
|    |     "state": "CA"                         |
|    |   },                                      |
|    |   "employee_date_of_birth": "12-10-2003", |
|    |   "employee_id": 1001                     |
|    | }                                         |
|  2 | {                                         |
|    |   "employee_contact": {                   |
|    |     "city": "Seattle",                    |
|    |     "state": "WA"                         |
|    |   },                                      |
|    |   "employee_date_of_birth": "01-01-1990", |
|    |   "employee_id": 1002                     |
|    | }                                         |
+----+-------------------------------------------+
```
