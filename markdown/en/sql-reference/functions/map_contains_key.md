Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Map)

# MAP\_CONTAINS\_KEY

Determines whether the specified [MAP](/sql-reference/data-types-structured) contains the specified key.

## Syntax

Copy code

```
MAP_CONTAINS_KEY( <key> , <map> )
```

## Arguments

`key`
:   The key to find.

`map`
:   The map to be searched.

## Returns

- Returns TRUE if the specified map contains the specified key.
- Returns FALSE if the specified map doesn’t contain the specified key.

## Usage notes

- The type of the key expression must match the type of the map’s key. If the type is VARCHAR, the types can be different lengths.
- For NULL input, the output is NULL.

## Examples

The function searches for the `k1` key and finds it in the map:

Copy code

```
SELECT MAP_CONTAINS_KEY(
  'k1',{'k1':'v1','k2':'v2','k3':'v3'}::MAP(VARCHAR,VARCHAR))
  AS contains_key;
```

```
+--------------+
| CONTAINS_KEY |
|--------------|
| True         |
+--------------+
```

The function searches for the `k1` key and doesn’t find it in the map:

Copy code

```
SELECT MAP_CONTAINS_KEY(
  'k1',{'ka':'va','kb':'vb','kc':'vc'}::MAP(VARCHAR,VARCHAR))
  AS contains_key;
```

```
+--------------+
| CONTAINS_KEY |
|--------------|
| False        |
+--------------+
```

A SELECT statement passes in a key that uses a different type than the key in the map:

Copy code

```
SELECT MAP_CONTAINS_KEY(
  'k1',{'1':'va','2':'vb','3':'vc'}::MAP(NUMBER,VARCHAR))
  AS contains_key;
```

```
001065 (22023): SQL compilation error:
Function MAP_CONTAINS_KEY cannot be used with arguments of types VARCHAR(2) and MAP(NUMBER(38,0), VARCHAR(134217728))
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

Determine whether the map in the `attrs` column contains the key in the `ins_key` column:

Copy code

```
SELECT id, MAP_CONTAINS_KEY(ins_key, attrs) AS has_key
  FROM demo_maps;
```

```
+----+---------+
| ID | HAS_KEY |
|----+---------|
|  1 | False   |
|  2 | True    |
+----+---------+
```

The output shows the following:

- The map in the `attrs` column in row `1` doesn’t contain the key (`material`)
  in the `ins_key` column.
- The map in the `attrs` column in row `2` contains the key (`brand`)
  in the `ins_key` column.
