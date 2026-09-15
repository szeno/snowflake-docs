Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# PARSE\_IP

Returns a JSON object consisting of all the components from a valid INET (Internet Protocol) or CIDR (Classless Internet Domain Routing) IPv4 or IPv6 string.

## Syntax

Copy code

```
PARSE_IP(<expr>, '<type>' [, <permissive>])
```

## Arguments

**Required:**

`expr`
:   A string expression.

`type`
:   A string that identifies the type of IP address. Supports either `INET` or `CIDR`; the value is
    case-insensitive.

**Optional:**

`permissive`
:   Flag that determines how parse errors are handled:

    - If set to 0, parse errors cause the function to fail.
    - If set to 1, parse errors result in an object with the `error`
      field set to the respective error message (and no other fields set).

    Default value is 0.

## Returns

[OBJECT](/sql-reference/data-types-semistructured#label-data-type-object).

## Usage notes

- The function parses an IP address and returns a JSON object.

  The following elements are always returned:

  `family`
  :   Numeric value. `4` (IPv4) or `6` (IPv6).

  `ip_type`
  :   String value. `inet` or `cidr` from the input.

  `host`
  :   String value. Host address from the input expression.

  `ip_fields`
  :   Array of 4 numeric fields, each a value between 0 and 4,294,967,295 (2^32 - 1), inclusive. The bit values from
      this array are mapped to the raw bits in the host address.

      - IPv4 addresses: Displays only the rightmost 32 bits of the host address.
      - IPv6 addresses: Displays each of the 32-bit fields that map to the raw 128-bit host address from left to right.

  If a subnet mask is input, the results include `network_prefix_length`, a numeric value that identifies the length of the subnet mask.

  The following elements are returned for IPv4 addresses:

  `ipv4`
  :   Numeric IP address that matches the first field in `ip_fields`.

  `ipv4_range_start`
  :   Numeric start address of the network, displayed when a subnet mask is included in the input.

  `ipv4_range_end`
  :   Numeric end address of the network, displayed when a subnet mask is included in the input.

  The following elements are returned for IPv6 addresses:

  `hex_ipv6`
  :   IP address expressed as a fully padded, fixed-size hexadecimal value.

  `hex_ipv6_range_start`
  :   Fully padded fixed-size hexadecimal start address of the network, displayed when a subnet mask is included in the input.

  `hex_ipv6_range_end`
  :   Fully padded fixed-size hexadecimal end address of the network, displayed when a subnet mask is included in the input.

  The `snowflake$type` element is reserved for internal Snowflake usage.
- For IP address range calculations or subnet mask searches, query the individual JSON elements directly. See the examples, below.
- When inputting a subnet mask, Snowflake recommends storing the function output in a VARIANT column and querying against the generated elements for better performance. See the examples.

## Examples

> Copy code
>
> ```
> SELECT column1, PARSE_IP(column1, 'INET') FROM VALUES('192.168.242.188/24'), ('192.168.243.189/24');
> --------------------+-----------------------------------+
>  COLUMN1            | PARSE_IP(COLUMN1, 'INET')         |
> --------------------+-----------------------------------|
>  192.168.242.188/24 | {                                 |
>                     |   "family": 4,                    |
>                     |   "host": "192.168.242.188",      |
>                     |   "ip_fields": [                  |
>                     |     3232297660,                   |
>                     |     0,                            |
>                     |     0,                            |
>                     |     0                             |
>                     |   ],                              |
>                     |   "ip_type": "inet",              |
>                     |   "ipv4": 3232297660,             |
>                     |   "ipv4_range_end": 3232297727,   |
>                     |   "ipv4_range_start": 3232297472, |
>                     |   "netmask_prefix_length": 24,    |
>                     |   "snowflake$type": "ip_address"  |
>                     | }                                 |
>  192.168.243.189/24 | {                                 |
>                     |   "family": 4,                    |
>                     |   "host": "192.168.243.189",      |
>                     |   "ip_fields": [                  |
>                     |     3232297917,                   |
>                     |     0,                            |
>                     |     0,                            |
>                     |     0                             |
>                     |   ],                              |
>                     |   "ip_type": "inet",              |
>                     |   "ipv4": 3232297917,             |
>                     |   "ipv4_range_end": 3232297983,   |
>                     |   "ipv4_range_start": 3232297728, |
>                     |   "netmask_prefix_length": 24,    |
>                     |   "snowflake$type": "ip_address"  |
>                     | }                                 |
> --------------------+-----------------------------------+
> ```
>
> Copy code
>
> ```
> SELECT PARSE_IP('fe80::20c:29ff:fe2c:429/64', 'INET');
>
> ----------------------------------------------------------------+
>   PARSE_IP('FE80::20C:29FF:FE2C:429/64', 'INET')                |
> ----------------------------------------------------------------|
>   {                                                             |
>     "family": 6,                                                |
>     "hex_ipv6": "FE80000000000000020C29FFFE2C0429",             |
>     "hex_ipv6_range_end": "FE80000000000000FFFFFFFFFFFFFFFF",   |
>     "hex_ipv6_range_start": "FE800000000000000000000000000000", |
>     "host": "fe80::20c:29ff:fe2c:429",                          |
>     "ip_fields": [                                              |
>       4269801472,                                               |
>       0,                                                        |
>       34351615,                                                 |
>       4264297513                                                |
>     ],                                                          |
>     "ip_type": "inet",                                          |
>     "netmask_prefix_length": 64,                                |
>     "snowflake$type": "ip_address"                              |
>   }                                                             |
> ----------------------------------------------------------------+
> ```
>
> Copy code
>
> ```
> WITH
> lookup AS (
>   SELECT column1 AS tag, PARSE_IP(column2, 'INET') AS obj FROM VALUES('San Francisco', '192.168.242.0/24'), ('New York', '192.168.243.0/24')
> ),
> entries AS (
>   SELECT PARSE_IP(column1, 'INET') AS ipv4 FROM VALUES('192.168.242.188/24'), ('192.168.243.189/24')
> )
> SELECT lookup.tag, entries.ipv4:host, entries.ipv4
> FROM lookup, entries
> WHERE lookup.tag = 'San Francisco'
> AND entries.IPv4:ipv4 BETWEEN lookup.obj:ipv4_range_start AND lookup.obj:ipv4_range_end;
>
> ---------------+-------------------+-----------------------------------+
>  TAG           | ENTRIES.IPV4:HOST | IPV4                              |
> ---------------+-------------------+-----------------------------------|
>  San Francisco | "192.168.242.188" | {                                 |
>                |                   |   "family": 4,                    |
>                |                   |   "host": "192.168.242.188",      |
>                |                   |   "ip_fields": [                  |
>                |                   |     3232297660,                   |
>                |                   |     0,                            |
>                |                   |     0,                            |
>                |                   |     0                             |
>                |                   |   ],                              |
>                |                   |   "ip_type": "inet",              |
>                |                   |   "ipv4": 3232297660,             |
>                |                   |   "ipv4_range_end": 3232297727,   |
>                |                   |   "ipv4_range_start": 3232297472, |
>                |                   |   "netmask_prefix_length": 24,    |
>                |                   |   "snowflake$type": "ip_address"  |
>                |                   | }                                 |
> ---------------+-------------------+-----------------------------------+
> ```
>
> Copy code
>
> ```
> CREATE OR REPLACE TABLE ipv6_lookup (tag String, obj VARIANT);
>
> -----------------------------------------+
>  status                                  |
> -----------------------------------------|
>  Table IPV6_LOOKUP successfully created. |
> -----------------------------------------+
>
> INSERT INTO ipv6_lookup
>     SELECT column1 AS tag, parse_ip(column2, 'INET') AS obj
>     FROM VALUES('west', 'fe80:12:20c:29ff::/64'), ('east', 'fe80:12:1:29ff::/64');
>
> -------------------------+
>  number of rows inserted |
> -------------------------|
>                        2 |
> -------------------------+
>
> CREATE OR REPLACE TABLE ipv6_entries (obj VARIANT);
> ------------------------------------------+
>  status                                   |
> ------------------------------------------|
>  Table IPV6_ENTRIES successfully created. |
> ------------------------------------------+
>
> INSERT INTO ipv6_entries
>     SELECT parse_ip(column1, 'INET') as obj
>     FROM VALUES
>         ('fe80:12:20c:29ff:fe2c:430:370:2/64'),
>         ('fe80:12:20c:29ff:fe2c:430:370:00F0/64'),
>         ('fe80:12:20c:29ff:fe2c:430:370:0F00/64'),
>         ('fe80:12:20c:29ff:fe2c:430:370:F000/64'),
>         ('fe80:12:20c:29ff:fe2c:430:370:FFFF/64'),
>         ('fe80:12:1:29ff:fe2c:430:370:FFFF/64'),
>         ('fe80:12:1:29ff:fe2c:430:370:F000/64'),
>         ('fe80:12:1:29ff:fe2c:430:370:0F00/64'),
>         ('fe80:12:1:29ff:fe2c:430:370:00F0/64'),
>         ('fe80:12:1:29ff:fe2c:430:370:2/64');
>
> -------------------------+
>  number of rows inserted |
> -------------------------|
>                       10 |
> -------------------------+
>
> SELECT lookup.tag, entries.obj:host
>     FROM ipv6_lookup AS lookup, ipv6_entries AS entries
>     WHERE lookup.tag = 'east'
>     AND entries.obj:hex_ipv6 BETWEEN lookup.obj:hex_ipv6_range_start AND lookup.obj:hex_ipv6_range_end;
>
> ------+------------------------------------+
>  TAG  | ENTRIES.OBJ:HOST                   |
> ------+------------------------------------|
>  east | "fe80:12:1:29ff:fe2c:430:370:FFFF" |
>  east | "fe80:12:1:29ff:fe2c:430:370:F000" |
>  east | "fe80:12:1:29ff:fe2c:430:370:0F00" |
>  east | "fe80:12:1:29ff:fe2c:430:370:00F0" |
>  east | "fe80:12:1:29ff:fe2c:430:370:2"    |
> ------+------------------------------------+
> ```
