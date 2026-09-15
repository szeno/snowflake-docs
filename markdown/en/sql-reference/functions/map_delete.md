Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Map)

# MAP\_DELETE

Returns a [MAP](/sql-reference/data-types-structured) based on an existing MAP with one or more keys removed.

## Syntax

Copy code

```
MAP_DELETE( <map>, <key1> [, <key2>, ... ] )
```

## Arguments

`map`
:   The map that contains the key to remove.

`keyN`
:   The key to be omitted from the returned map.

## Returns

Returns a MAP that contains the contents of the input (source) map with one or more keys removed.

## Usage notes

- The type of the key expression must match the type of the map’s key. If the type is VARCHAR,
  then the types can be different lengths.
- Key values that aren’t found in the map are ignored.

## Examples

Remove two key-value pairs from a map containing three key-value pairs:

Copy code

```
SELECT MAP_DELETE({'a':1,'b':2,'c':3}::MAP(VARCHAR,NUMBER),'a','b');
```

```
+--------------------------------------------------------------+
| MAP_DELETE({'A':1,'B':2,'C':3}::MAP(VARCHAR,NUMBER),'A','B') |
|--------------------------------------------------------------|
| {                                                            |
|   "c": 3                                                     |
| }                                                            |
+--------------------------------------------------------------+
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

Remove the keys in the `del_key1` and `del_key2` columns from the MAP values in the `attrs` column:

Copy code

```
SELECT id, MAP_DELETE(attrs, del_key1, del_key2) AS attrs_after_delete
  FROM demo_maps;
```

```
+----+---------------------+
| ID | ATTRS_AFTER_DELETE  |
|----+---------------------|
|  1 | {                   |
|    |   "color": "red"    |
|    | }                   |
|  2 | {                   |
|    |   "brand": "ZenCo", |
|    |   "color": "blue"   |
|    | }                   |
+----+---------------------+
```
