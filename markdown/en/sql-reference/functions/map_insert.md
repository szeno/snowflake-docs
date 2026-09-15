Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Map)

# MAP\_INSERT

Returns a new [MAP](/sql-reference/data-types-structured) consisting of the input MAP with
a new key-value pair inserted. That is, an existing key is updated with a new value.

## Syntax

Copy code

```
MAP_INSERT( <map> , <key> , <value> [ , <updateFlag> ] )
```

## Arguments

`map`
:   The source map into which the new key-value pair is inserted.

`key`
:   The new key to insert into the map. Must be different from all existing keys in the map, unless `updateFlag` is set to
    TRUE.

`value`
:   The value associated with the key.

**Optional**

`updateFlag`
:   A Boolean flag that, when set to TRUE, specifies the input value is used to update an existing value for a
    key in the map, rather than inserting a new key-value pair.

    The default is FALSE.

## Returns

Returns a MAP consisting of the input MAP with a new key-value pair inserted or an existing key
updated with a new value.

## Usage notes

- The type of the key expression must match the type of the map’s key. If the type is VARCHAR,
  then the types can be different lengths.
- The function supports [JSON null](/user-guide/semistructured-considerations#label-variant-null) values, but not SQL NULL values or keys:

  - If `key` is any string other than NULL and `value` is a JSON null (for example,
    `PARSE_JSON('NULL')`), then the key-value pair is inserted into the returned map.
  - If `key` is any string other than NULL and `value` is a SQL NULL (for example,
    `NULL`), then the value is converted to JSON null, and the key-value pair is inserted into the
    returned map.
  - If `key` is a SQL NULL, the key-value pair is omitted from the returned map.
- If `updateFlag` is set to TRUE, then the existing input `key` is updated
  to the input `value`. If `updateFlag` is omitted or set to FALSE, and the
  input key already exists in the map, then an error is returned.
- If `updateFlag` is set to TRUE, but the corresponding key does not already exist in
  the map, then the key-value pair is added.

## Examples

Insert a third key-value pair into a map containing two key-value pairs:

Copy code

```
SELECT MAP_INSERT({'a':1,'b':2}::MAP(VARCHAR,NUMBER),'c',3);
```

```
+------------------------------------------------------+
| MAP_INSERT({'A':1,'B':2}::MAP(VARCHAR,NUMBER),'C',3) |
|------------------------------------------------------|
| {                                                    |
|   "a": 1,                                            |
|   "b": 2,                                            |
|   "c": 3                                             |
| }                                                    |
+------------------------------------------------------+
```

Insert two new key-value pairs, while omitting one key-value pair, into an empty map:

- `Key_One` consists of a JSON null value.
- `Key_Two` consists of a SQL NULL value, which is converted to a JSON null value.
- `Key_Three` consists of a string containing “null”.

Copy code

```
SELECT MAP_INSERT(MAP_INSERT(MAP_INSERT({}::MAP(VARCHAR,VARCHAR),
  'Key_One', PARSE_JSON('NULL')), 'Key_Two', NULL), 'Key_Three', 'null');
```

```
+---------------------------------------------------------------------------+
| MAP_INSERT(MAP_INSERT(MAP_INSERT({}::MAP(VARCHAR,VARCHAR),                |
|    'KEY_ONE', PARSE_JSON('NULL')), 'KEY_TWO', NULL), 'KEY_THREE', 'NULL') |
|---------------------------------------------------------------------------|
| {                                                                         |
|   "Key_One": null,                                                        |
|   "Key_Three": "null",                                                    |
|   "Key_Two": null                                                         |
| }                                                                         |
+---------------------------------------------------------------------------+
```

Update an existing key-value pair (`"k1": 100`) with a new value (`"string-value"`):

Copy code

```
SELECT MAP_INSERT({'k1':100}::MAP(VARCHAR,VARCHAR), 'k1', 'string-value', TRUE) AS map;
```

```
+------------------------+
| MAP                    |
|------------------------|
| {                      |
|   "k1": "string-value" |
| }                      |
+------------------------+
```

Create a temporary table that contains MAP values:

Copy code

```
CREATE OR REPLACE TEMP TABLE demo_maps(
  id INTEGER,
  attrs MAP(VARCHAR, VARCHAR),
  defaults MAP(VARCHAR, VARCHAR),
  keep_keys ARRAY(VARCHAR),
  ins_key VARCHAR,
  ins_val VARCHAR,
  update_existing BOOLEAN,
  del_key1 VARCHAR,
  del_key2 VARCHAR);

INSERT INTO demo_maps SELECT
  1,
  {'color':'red','size':'M','brand':'Acme'}::MAP(VARCHAR, VARCHAR),
  {'currency':'USD','size':'L'}::MAP(VARCHAR, VARCHAR),
  ['color','brand']::ARRAY(VARCHAR),
  'material',
  'cotton',
  TRUE,
  'size',
  'brand';

INSERT INTO demo_maps SELECT
  2,
  {'color':'blue','brand':'ZenCo'}::MAP(VARCHAR, VARCHAR),
  {'currency':'EUR','size':'M','brand':'ZenCo'}::MAP(VARCHAR, VARCHAR),
  ['brand','currency']::ARRAY(VARCHAR),
  'brand',
  'ZC',
  FALSE,
  'currency',
  'material';
```

Query the table to show the data:

Copy code

```
SELECT * FROM demo_maps;
```

```
+----+---------------------+----------------------+--------------+----------+---------+-----------------+----------+----------+
| ID | ATTRS               | DEFAULTS             | KEEP_KEYS    | INS_KEY  | INS_VAL | UPDATE_EXISTING | DEL_KEY1 | DEL_KEY2 |
|----+---------------------+----------------------+--------------+----------+---------+-----------------+----------+----------|
|  1 | {                   | {                    | [            | material | cotton  | True            | size     | brand    |
|    |   "brand": "Acme",  |   "currency": "USD", |   "color",   |          |         |                 |          |          |
|    |   "color": "red",   |   "size": "L"        |   "brand"    |          |         |                 |          |          |
|    |   "size": "M"       | }                    | ]            |          |         |                 |          |          |
|    | }                   |                      |              |          |         |                 |          |          |
|  2 | {                   | {                    | [            | brand    | ZC      | False           | currency | material |
|    |   "brand": "ZenCo", |   "brand": "ZenCo",  |   "brand",   |          |         |                 |          |          |
|    |   "color": "blue"   |   "currency": "EUR", |   "currency" |          |         |                 |          |          |
|    | }                   |   "size": "M"        | ]            |          |         |                 |          |          |
|    |                     | }                    |              |          |         |                 |          |          |
+----+---------------------+----------------------+--------------+----------+---------+-----------------+----------+----------+
```

Using the keys in the `ins_key` column and the values in the `ins_val` column, insert
or update key-value pairs in the maps in the `attrs` column:

Copy code

```
SELECT id, MAP_INSERT(attrs, ins_key, ins_val, TRUE) AS attrs_insert_or_update
  FROM demo_maps;
```

```
+----+-------------------------+
| ID | ATTRS_INSERT_OR_UPDATE  |
|----+-------------------------|
|  1 | {                       |
|    |   "brand": "Acme",      |
|    |   "color": "red",       |
|    |   "material": "cotton", |
|    |   "size": "M"           |
|    | }                       |
|  2 | {                       |
|    |   "brand": "ZC",        |
|    |   "color": "blue"       |
|    | }                       |
+----+-------------------------+
```
