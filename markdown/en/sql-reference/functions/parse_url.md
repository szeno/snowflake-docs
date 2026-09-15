Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# PARSE\_URL

Returns an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value that consists of all the components (fragment,
host, parameters, path, port, query, scheme) in a valid input URL/URI.

## Syntax

Copy code

```
PARSE_URL(<string>, [<permissive>])
```

## Arguments

**Required:**

`string`
:   String to parse.

**Optional:**

`permissive`
:   Flag that determines how parse errors are handled:

    - If set to `0`, parse errors cause the function to fail.
    - If set to `1`, parse errors result in an object with the `error`
      field set to the respective error message (and no other fields set).

    Default value is `0`.

## Returns

The function returns a value of type OBJECT.

If any input argument is NULL, the function returns NULL.

When an OBJECT value is returned, it contains the following key-value pairs:

| Key | Value |
| --- | --- |
| `fragment` | An anchor that points to a location. |
| `host` | The domain (address of a website or server). |
| `parameters` | Values passed to the website or server. |
| `path` | A resource’s location. |
| `port` | The port (connection endpoint for a process or service). |
| `query` | A query string passed to the website or server. |
| `scheme` | The protocol. |

Expand

Show lessSee more

## Examples

The following examples use the PARSE\_URL function.

### Parse URLs in table data

Create a table and insert rows:

Copy code

```
CREATE OR REPLACE TABLE parse_url_test (id INT, sample_url VARCHAR);

INSERT INTO parse_url_test VALUES
  (1, 'mailto:abc@xyz.com'),
  (2, 'https://www.snowflake.com/'),
  (3, 'http://USER:PASS@EXAMPLE.INT:4345/HELLO.PHP?USER=1'),
  (4, NULL);

SELECT * FROM parse_url_test;
```

```
+----+----------------------------------------------------+
| ID | SAMPLE_URL                                         |
|----+----------------------------------------------------|
|  1 | mailto:abc@xyz.com                                 |
|  2 | https://www.snowflake.com/                         |
|  3 | http://USER:PASS@EXAMPLE.INT:4345/HELLO.PHP?USER=1 |
|  4 | NULL                                               |
+----+----------------------------------------------------+
```

The following query shows the results of PARSE\_URL for the sample URLs:

Copy code

```
SELECT PARSE_URL(sample_url) FROM parse_url_test;
```

```
+------------------------------------+
| PARSE_URL(SAMPLE_URL)              |
|------------------------------------|
| {                                  |
|   "fragment": null,                |
|   "host": null,                    |
|   "parameters": null,              |
|   "path": "abc@xyz.com",           |
|   "port": null,                    |
|   "query": null,                   |
|   "scheme": "mailto"               |
| }                                  |
| {                                  |
|   "fragment": null,                |
|   "host": "www.snowflake.com",     |
|   "parameters": null,              |
|   "path": "",                      |
|   "port": null,                    |
|   "query": null,                   |
|   "scheme": "https"                |
| }                                  |
| {                                  |
|   "fragment": null,                |
|   "host": "USER:PASS@EXAMPLE.INT", |
|   "parameters": {                  |
|     "USER": "1"                    |
|   },                               |
|   "path": "HELLO.PHP",             |
|   "port": "4345",                  |
|   "query": "USER=1",               |
|   "scheme": "http"                 |
| }                                  |
| NULL                               |
+------------------------------------+
```

This query shows the host for each sample URL:

Copy code

```
SELECT PARSE_URL(sample_url):host FROM parse_url_test;
```

```
+----------------------------+
| PARSE_URL(SAMPLE_URL):HOST |
|----------------------------|
| null                       |
| "www.snowflake.com"        |
| "USER:PASS@EXAMPLE.INT"    |
| NULL                       |
+----------------------------+
```

Return the rows where the port is `4345`:

Copy code

```
SELECT *
  FROM parse_url_test
  WHERE PARSE_URL(sample_url):port = '4345';
```

```
+----+----------------------------------------------------+
| ID | SAMPLE_URL                                         |
|----+----------------------------------------------------|
|  3 | http://USER:PASS@EXAMPLE.INT:4345/HELLO.PHP?USER=1 |
+----+----------------------------------------------------+
```

Return the rows where the host is `www.snowflake.com`:

Copy code

```
SELECT *
  FROM parse_url_test
  WHERE PARSE_URL(sample_url):host = 'www.snowflake.com';
```

```
+----+----------------------------+
| ID | SAMPLE_URL                 |
|----+----------------------------|
|  2 | https://www.snowflake.com/ |
+----+----------------------------+
```

### Parse invalid URLs

Parse an invalid URL that is missing the scheme. Set the `permissive`
argument to `0` to indicate that the function fails if the input
is invalid:

Copy code

```
SELECT PARSE_URL('example.int/hello.php?user=12#nofragment', 0);
```

```
100139 (22000): Error parsing URL: scheme not specified
```

Parse an invalid URL, with the `permissive` argument set to `1` to
indicate that the function returns an OBJECT value that contains the error
message:

Copy code

```
SELECT PARSE_URL('example.int/hello.php?user=12#nofragment', 1);
```

```
+----------------------------------------------------------+
| PARSE_URL('EXAMPLE.INT/HELLO.PHP?USER=12#NOFRAGMENT', 1) |
|----------------------------------------------------------|
| {                                                        |
|   "error": "scheme not specified"                        |
| }                                                        |
+----------------------------------------------------------+
```
