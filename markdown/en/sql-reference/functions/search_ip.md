Categories:
:   [String & binary functions](/sql-reference/functions-string) (Full-Text Search)

# SEARCH\_IP

Searches for valid IPv4 and IPv6 addresses in specified character-string columns from one or more tables, including fields
in VARIANT, OBJECT, and ARRAY columns. The search is based on a single IP address or a range of IP addresses
that you specify. If an IP address in the column or field matches a specified IP address or is in a specified range,
then the function returns TRUE.

For more information about using this function, see [Using full-text search](/user-guide/querying-with-search-functions).

## Syntax

Copy code

```
SEARCH_IP( <search_data>, '<search_string>' )
```

## Arguments

`search_data`
:   The data you want to search, expressed as a comma-delimited list of string literals, column names, or
    [paths](/user-guide/querying-semistructured#label-traversing-semistructured-data) to fields in VARIANT columns. The search data can
    also be a single literal string, which can be useful when you are testing the function.

    You can specify the wildcard character (`*`), where `*` expands to all qualifying columns in all of the
    tables that are in scope for the function. Qualifying columns are those that have VARCHAR (text), VARIANT,
    ARRAY, and OBJECT data types. VARIANT, ARRAY, and OBJECT data is converted to text for searching. You can
    also use the ILIKE and EXCLUDE keywords for filtering.

    For more information about this argument, see the `search_data` description for the
    [SEARCH](/sql-reference/functions/search) function.

`'search_string'`
:   A VARCHAR string that contains one of the following addresses:

    - A complete and valid IP address in standard IPv4 or IPv6 format, such as `192.0.2.1` or
      `2001:0db8:85a3:0000:0000:8a2e:0370:7334`.
    - A valid IP address in standard IPv4 or IPv6 format with a Classless Inter-Domain Routing (CIDR) range,
      such as `192.0.2.1/24` or `2001:db8:85a3::/64`.
    - A valid IP address in standard IPv4 or IPv6 format with leading zeros, such as `192.000.002.001`
      instead of `192.0.2.1` or `2001:0db8:85a3:0333:4444:8a2e:0370:7334` instead of
      `2001:db8:85a3:333:4444:8a2e:370:7334`. The function accepts up to three digits for each part of an IPv4
      address, and up to four digits for each part of an IPv6 address.
    - A valid compressed IPv6 address, such as `2001:db8:85a3:0:0:0:0:0` or `2001:db8:85a3::` instead of
      `2001:db8:85a3:0000:0000:0000:0000:0000`.
    - An IPv6 dual address that combines an IPv6 and an IPv4 address, such as `2001:db8:85a3::192.0.2.1`.

    This argument must be a literal string. Specify one pair of single quotes around the string.

    The following types of arguments aren’t supported:

    - Column names
    - Empty strings
    - More than one IP address
    - Partial IPv4 and IPv6 addresses

## Returns

Returns a BOOLEAN:

- Returns TRUE if a valid IP address is specified in `search_string` and a matching IP address is found in
  `search_data`.
- Returns TRUE if a valid IP address with a CIDR range is specified in `search_string` and an IP address in
  the specified range is found in `search_data`.
- Returns NULL if either of these arguments is NULL.
- Otherwise, returns FALSE.

## Usage notes

- The SEARCH\_IP function operates only on VARCHAR (text), VARIANT, ARRAY, and OBJECT data. The function returns an error if the
  `search_data` argument doesn’t contain data of these data types. When the `search_data` argument includes
  data of both supported data types and unsupported data types, the function searches the data of the supported data
  types and silently ignores the data of the unsupported data types. For examples, see [Examples of expected error cases](#label-search-ip-function-error-examples).
- The function returns an error if the `search_string` argument isn’t a valid IP address. For examples, see
  [Examples of expected error cases](#label-search-ip-function-error-examples).
- You can add a FULL\_TEXT search optimization on columns that are the target of SEARCH\_IP function calls by using an ALTER TABLE command
  that specifies the ENTITY\_ANALYZER. For example:

  Copy code

  ```
  ALTER TABLE ipt ADD SEARCH OPTIMIZATION ON FULL_TEXT(
    ipv4_source,
    ANALYZER => 'ENTITY_ANALYZER');
  ```

  The ENTITY\_ANALYZER recognizes only the entities (for example, IP addresses). Therefore, the search access path is typically
  much smaller than FULL\_TEXT search optimization with a different analyzer.

  For more information, see [enable FULL\_TEXT search optimization](/user-guide/search-optimization/enabling#label-enable-full-text-search).

## Examples

The following examples use the SEARCH\_IP function:

- [Search for matching IP addresses in VARCHAR columns](#label-search-ip-function-varchar-examples)
- [Search for matching IP addresses in a VARIANT column](#label-search-ip-function-variant-examples)
- [Search for matching IP addresses in long strings of text](#label-search-ip-function-long-strings-examples)
- [Examples of expected error cases](#label-search-ip-function-error-examples)

### Search for matching IP addresses in VARCHAR columns

The following examples show how to use the SEARCH\_IP function to query VARCHAR (text) columns.

First, create a table named `ipt` that has two columns that store IPv4 addresses and one column that
stores IPv6 addresses:

Copy code

```
CREATE OR REPLACE TABLE ipt(
  id INT,
  ipv4_source VARCHAR(20),
  ipv4_target VARCHAR(20),
  ipv6_target VARCHAR(40));
```

Insert two rows into the table:

Copy code

```
INSERT INTO ipt VALUES(
  1,
  '192.0.2.146',
  '203.0.113.5',
  '2001:0db8:85a3:0000:0000:8a2e:0370:7334');

INSERT INTO ipt VALUES(
  2,
  '192.0.2.111',
  '192.000.002.146',
  '2001:db8:1234::5678');
```

Query the table:

Copy code

```
SELECT * FROM ipt;
```

```
+----+-------------+-----------------+-----------------------------------------+
| ID | IPV4_SOURCE | IPV4_TARGET     | IPV6_TARGET                             |
|----+-------------+-----------------+-----------------------------------------|
|  1 | 192.0.2.146 | 203.0.113.5     | 2001:0db8:85a3:0000:0000:8a2e:0370:7334 |
|  2 | 192.0.2.111 | 192.000.002.146 | 2001:db8:1234::5678                     |
+----+-------------+-----------------+-----------------------------------------+
```

The following sections run queries that use the SEARCH\_IP function on this table data:

- [Search for matching IP addresses by using the function in a SELECT list](#label-search-ip-function-varchar-examples-select-list)
- [Search for matching IP addresses by using the function in the WHERE clause](#label-search-ip-function-varchar-examples-where-clause)
- [Enable FULL\_TEXT search optimization on VARCHAR columns](#label-search-ip-function-varchar-examples-enable-so)

#### Search for matching IP addresses by using the function in a SELECT list

Run a query that uses the SEARCH\_IP function in the SELECT list and searches
the three VARCHAR columns in the table:

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target,
       SEARCH_IP((ipv4_source, ipv4_target, ipv6_target), '192.0.2.146') AS "Match found?"
  FROM ipt
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+-----------------------------------------+--------------+
| IPV4_SOURCE | IPV4_TARGET     | IPV6_TARGET                             | Match found? |
|-------------+-----------------+-----------------------------------------+--------------|
| 192.0.2.111 | 192.000.002.146 | 2001:db8:1234::5678                     | True         |
| 192.0.2.146 | 203.0.113.5     | 2001:0db8:85a3:0000:0000:8a2e:0370:7334 | True         |
+-------------+-----------------+-----------------------------------------+--------------+
```

Notice that `search_data` `192.000.002.146` is a match for `search_string`
`192.0.2.146`, even though `192.000.002.146` has leading zeros.

Run a query that searches for IPv6 addresses that match *2001:0db8:85a3:0000:0000:8a2e:0370:7334*:

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target,
       SEARCH_IP((ipv6_target), '2001:0db8:85a3:0000:0000:8a2e:0370:7334') AS "Match found?"
  FROM ipt
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+-----------------------------------------+--------------+
| IPV4_SOURCE | IPV4_TARGET     | IPV6_TARGET                             | Match found? |
|-------------+-----------------+-----------------------------------------+--------------|
| 192.0.2.111 | 192.000.002.146 | 2001:db8:1234::5678                     | False        |
| 192.0.2.146 | 203.0.113.5     | 2001:0db8:85a3:0000:0000:8a2e:0370:7334 | True         |
+-------------+-----------------+-----------------------------------------+--------------+
```

The following query is the same as the previous query, but it excludes the leading zeros and zero segments
in the `search_string`:

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target,
       SEARCH_IP((ipv6_target), '2001:db8:85a3::8a2e:370:7334') AS "Match found?"
  FROM ipt
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+-----------------------------------------+--------------+
| IPV4_SOURCE | IPV4_TARGET     | IPV6_TARGET                             | Match found? |
|-------------+-----------------+-----------------------------------------+--------------|
| 192.0.2.111 | 192.000.002.146 | 2001:db8:1234::5678                     | False        |
| 192.0.2.146 | 203.0.113.5     | 2001:0db8:85a3:0000:0000:8a2e:0370:7334 | True         |
+-------------+-----------------+-----------------------------------------+--------------+
```

The following query shows that a `search_string` with a CIDR range for IPv4 addresses:

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       SEARCH_IP((ipv4_source, ipv4_target), '192.0.2.1/20') AS "Match found?"
  FROM ipt
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+--------------+
| IPV4_SOURCE | IPV4_TARGET     | Match found? |
|-------------+-----------------+--------------|
| 192.0.2.111 | 192.000.002.146 | True         |
| 192.0.2.146 | 203.0.113.5     | True         |
+-------------+-----------------+--------------+
```

The following query shows that a `search_string` with leading zeros returns `True` for
IPv4 addresses that omit the leading zeros:

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       SEARCH_IP((ipv4_source, ipv4_target), '203.000.113.005') AS "Match found?"
  FROM ipt
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+--------------+
| IPV4_SOURCE | IPV4_TARGET     | Match found? |
|-------------+-----------------+--------------|
| 192.0.2.111 | 192.000.002.146 | False        |
| 192.0.2.146 | 203.0.113.5     | True         |
+-------------+-----------------+--------------+
```

#### Search for matching IP addresses by using the function in the WHERE clause

The following query uses the function in the WHERE clause and searches the `ipv4_target` column only.

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target
  FROM ipt
  WHERE SEARCH_IP(ipv4_target, '203.0.113.5')
  ORDER BY ipv4_source;
```

```
+-------------+-------------+-----------------------------------------+
| IPV4_SOURCE | IPV4_TARGET | IPV6_TARGET                             |
|-------------+-------------+-----------------------------------------|
| 192.0.2.146 | 203.0.113.5 | 2001:0db8:85a3:0000:0000:8a2e:0370:7334 |
+-------------+-------------+-----------------------------------------+
```

When the function is used in the WHERE clause and there is no match, no values are returned:

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target
  FROM ipt
  WHERE SEARCH_IP(ipv4_target, '203.0.113.1')
  ORDER BY ipv4_source;
```

```
+-------------+-------------+-------------+
| IPV4_SOURCE | IPV4_TARGET | IPV6_TARGET |
|-------------+-------------+-------------|
+-------------+-------------+-------------+
```

The following query uses the function in the WHERE clause and searches the `ipv6_target` column only.

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target
  FROM ipt
  WHERE SEARCH_IP(ipv6_target, '2001:db8:1234::5678')
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+---------------------+
| IPV4_SOURCE | IPV4_TARGET     | IPV6_TARGET         |
|-------------+-----------------+---------------------|
| 192.0.2.111 | 192.000.002.146 | 2001:db8:1234::5678 |
+-------------+-----------------+---------------------+
```

You can use the `*` character (or `table.*`) as the first argument to the SEARCH function, as shown in the following example.
The search operates on all of the qualifying columns in the table that you are selecting from:

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target
  FROM ipt
  WHERE SEARCH_IP((*), '192.0.2.146')
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+-----------------------------------------+
| IPV4_SOURCE | IPV4_TARGET     | IPV6_TARGET                             |
|-------------+-----------------+-----------------------------------------|
| 192.0.2.111 | 192.000.002.146 | 2001:db8:1234::5678                     |
| 192.0.2.146 | 203.0.113.5     | 2001:0db8:85a3:0000:0000:8a2e:0370:7334 |
+-------------+-----------------+-----------------------------------------+
```

You can also use the ILIKE and EXCLUDE keywords for filtering. For more information about
these keywords, see [SELECT](/sql-reference/sql/select).

The following search uses the ILIKE keyword to search only in columns that end with the string `_target`.

Copy code

```
SELECT ipv4_source,
       ipv4_target,
       ipv6_target
  FROM ipt
  WHERE SEARCH_IP(* ILIKE '%_target', '192.0.2.146')
  ORDER BY ipv4_source;
```

```
+-------------+-----------------+---------------------+
| IPV4_SOURCE | IPV4_TARGET     | IPV6_TARGET         |
|-------------+-----------------+---------------------|
| 192.0.2.111 | 192.000.002.146 | 2001:db8:1234::5678 |
+-------------+-----------------+---------------------+
```

#### Enable FULL\_TEXT search optimization on VARCHAR columns

To [enable FULL\_TEXT search optimization](/user-guide/search-optimization/enabling#label-enable-full-text-search) for the columns in the
`ipt` table, run the following ALTER TABLE command:

Copy code

```
ALTER TABLE ipt ADD SEARCH OPTIMIZATION ON FULL_TEXT(
  ipv4_source,
  ipv4_target,
  ipv6_target,
  ANALYZER => 'ENTITY_ANALYZER');
```

Note

The columns you specify must be VARCHAR or VARIANT columns. Columns with other data types aren’t supported.

### Search for matching IP addresses in a VARIANT column

The following examples show how to use the SEARCH\_IP function to query VARIANT columns.

The following example uses the SEARCH\_IP function to search a path to a field in a VARIANT column. Create a table
named `iptv` and insert two rows:

Copy code

```
CREATE OR REPLACE TABLE iptv(ip1 VARIANT);
INSERT INTO iptv(ip1)
  SELECT PARSE_JSON(' { "ipv1": "203.0.113.5", "ipv2": "203.0.113.5" } ');
INSERT INTO iptv(ip1)
  SELECT PARSE_JSON(' { "ipv1": "192.0.2.146", "ipv2": "203.0.113.5" } ');
```

Run the following search queries. The first query searches the `ipv1` field only. The
second searches `ipv1` and `ipv2`.

Copy code

```
SELECT * FROM iptv
  WHERE SEARCH_IP((ip1:"ipv1"), '203.0.113.5');
```

```
+--------------------------+
| IP1                      |
|--------------------------|
| {                        |
|   "ipv1": "203.0.113.5", |
|   "ipv2": "203.0.113.5"  |
| }                        |
+--------------------------+
```

Copy code

```
SELECT * FROM iptv
  WHERE SEARCH_IP((ip1:"ipv1",ip1:"ipv2"), '203.0.113.5');
```

```
+--------------------------+
| IP1                      |
|--------------------------|
| {                        |
|   "ipv1": "203.0.113.5", |
|   "ipv2": "203.0.113.5"  |
| }                        |
| {                        |
|   "ipv1": "192.0.2.146", |
|   "ipv2": "203.0.113.5"  |
| }                        |
+--------------------------+
```

To [enable FULL\_TEXT search optimization](/user-guide/search-optimization/enabling#label-enable-full-text-search) for this `ip1` VARIANT
column and its fields, run the following ALTER TABLE command:

Copy code

```
ALTER TABLE iptv ADD SEARCH OPTIMIZATION ON FULL_TEXT(
  ip1:"ipv1",
  ip1:"ipv2",
  ANALYZER => 'ENTITY_ANALYZER');
```

Note

The columns you specify must be VARCHAR or VARIANT columns. Columns with other data types aren’t supported.

### Search for matching IP addresses in long strings of text

Create a table named `ipt_log` and insert rows:

Copy code

```
CREATE OR REPLACE TABLE ipt_log(id INT, ip_request_log VARCHAR(200));
INSERT INTO ipt_log VALUES(1, 'Connection from IP address 192.0.2.146 succeeded.');
INSERT INTO ipt_log VALUES(2, 'Connection from IP address 203.0.113.5 failed.');
INSERT INTO ipt_log VALUES(3, 'Connection from IP address 192.0.2.146 dropped.');
```

Search for log entries in the `ip_request_log` column that include the `192.0.2.146` IP address:

Copy code

```
SELECT * FROM ipt_log
  WHERE SEARCH_IP(ip_request_log, '192.0.2.146')
  ORDER BY id;
```

```
+----+---------------------------------------------------+
| ID | IP_REQUEST_LOG                                    |
|----+---------------------------------------------------|
|  1 | Connection from IP address 192.0.2.146 succeeded. |
|  3 | Connection from IP address 192.0.2.146 dropped.   |
+----+---------------------------------------------------+
```

### Examples of expected error cases

The following examples show queries that return expected syntax errors.

The following example fails because `5` isn’t a supported data type for the `search_string` argument:

Copy code

```
SELECT SEARCH_IP(ipv4_source, 5) FROM ipt;
```

```
001045 (22023): SQL compilation error:
argument needs to be a string: '1'
```

The following example fails because the `search_string` argument isn’t a valid IP address.

Copy code

```
SELECT SEARCH_IP(ipv4_source, '1925.0.2.146') FROM ipt;
```

```
0000937 (22023): SQL compilation error: error line 1 at position 30
invalid argument for function [SEARCH_IP(IPT.IPV4_SOURCE, '1925.0.2.146')] unexpected argument [1925.0.2.146] at position 1,
```

The following example fails because the `search_string` argument is an empty string.

Copy code

```
SELECT SEARCH_IP(ipv4_source, '') FROM ipt;
```

```
000937 (22023): SQL compilation error: error line 1 at position 30
invalid argument for function [SEARCH_IP(IPT.IPV4_SOURCE, '')] unexpected argument [] at position 1,
```

The following example fails because no columns with supported data types are specified for the `search_data` argument.

Copy code

```
SELECT SEARCH_IP(id, '192.0.2.146') FROM ipt;
```

```
001173 (22023): SQL compilation error: error line 1 at position 7: Expected non-empty set of columns supporting full-text search.
```

The following example succeeds because a column with a supported data type is specified for the `search_data`
argument. The function ignores the `id` column because it isn’t a supported data type:

Copy code

```
SELECT SEARCH_IP((id, ipv4_source), '192.0.2.146') FROM ipt;
```

```
+---------------------------------------------+
| SEARCH_IP((ID, IPV4_SOURCE), '192.0.2.146') |
|---------------------------------------------|
| True                                        |
| False                                       |
+---------------------------------------------+
```
