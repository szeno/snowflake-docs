# IPADDRESS data type

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The IPADDRESS data type stores IPv4 and IPv6 addresses as a native 128-bit value. Use it instead of
storing addresses as VARCHAR or BINARY when you want Snowflake to validate the address, compare
values in numeric order, and return a canonical text form.

A value of the IPADDRESS type is a single host address. The type doesn’t store a prefix length,
CIDR range, or network mask. To work with an address range, either store its first and last address
and compare against that range, or store its network address and prefix length and match with
[IPADDRESS\_TRUNC](/sql-reference/functions/ipaddress_trunc). For more information, see [Filter and join on address ranges](#label-ipaddress-type-ranges).

The following considerations apply to the IPADDRESS data type:

- Each value occupies 16 bytes. IPv4 and IPv6 addresses share the same 128-bit storage.
- Comparison operators, `BETWEEN`, `ORDER BY`, `MIN`, and `MAX` use the numeric order of the
  128-bit address, not the order of its text form.
- Snowflake stores the address, not the text you supplied. Two spellings of the same IPv6 address
  are the same value, and querying the column returns the canonical form.
- The ANSI literal form `IPADDRESS '<address>'` is supported as input.
- IPADDRESS is natively supported in [VARIANT](/sql-reference/data-types-semistructured): `TYPEOF`
  reports `IPADDRESS`, and casting the value back to IPADDRESS returns the canonical address.
- When you load data with [COPY INTO <table>](/sql-reference/sql/copy-into-table) or Snowpipe, the
  column in the source file holds the address as text. Snowflake validates each value as it’s
  loaded and canonicalizes it. An invalid address fails the load by default. To skip the offending
  rows and load the rest, set the `ON_ERROR` copy option.

## Specify an IPADDRESS data type

- To specify an IPADDRESS type, use the following syntax:

  Copy code

  ```
  <column_name> IPADDRESS
  ```

  Where:

  - `column_name` is the name of a column in a table.

## Accepted input and canonical output

Snowflake parses IPADDRESS strings strictly:

- IPv4 dotted-decimal addresses, such as `192.0.2.1`.
- IPv6 addresses, including compressed forms, such as `2001:db8::1`.

The following forms aren’t valid IPADDRESS values:

- CIDR prefixes, such as `192.0.2.0/24`.
- Bracketed IPv6 literals, such as `[2001:db8::1]`.
- Zone identifiers, such as `fe80::1%eth0`.
- DNS hostnames.
- Octal or other non-decimal IPv4 encodings.

When Snowflake displays an IPADDRESS value, it uses a canonical text form:

- IPv4 addresses use dotted decimal, such as `192.0.2.1`.
- IPv6 addresses follow [RFC 5952](https://datatracker.ietf.org/doc/html/rfc5952): lowercase hexadecimal,
  compressed zeros, and no extra leading zeros in a group. For example, the input
  `2001:0db8:0000:0000:0000:0000:0000:0001` is stored and displayed as `2001:db8::1`.

## Filter and join on address ranges

Because IPADDRESS values compare in numeric address order, a subnet or CIDR block is a contiguous
range. Express membership in a range with `BETWEEN` and the first and last address of the range:

Copy code

```
SELECT COUNT(*)
  FROM ipaddr_events
  WHERE src_ip BETWEEN TO_IPADDRESS('10.0.0.0') AND TO_IPADDRESS('10.255.255.255');
```

The same predicate works as a join condition, so you can enrich addresses from a reference table
that stores one row per range:

Copy code

```
SELECT e.event_id, c.vendor
  FROM ipaddr_events AS e
  LEFT OUTER JOIN ipaddr_cidrs AS c
    ON e.src_ip BETWEEN c.start_ip AND c.end_ip;
```

If your reference table stores each network as a network address and a prefix length instead, use
[IPADDRESS\_TRUNC](/sql-reference/functions/ipaddress_trunc) to clear the host bits of the address and compare the
result with the network address:

Copy code

```
SELECT e.event_id, n.owner
  FROM ipaddr_events AS e
  LEFT OUTER JOIN ipaddr_networks AS n
    ON IPADDRESS_TRUNC(
         e.src_ip,
         IFF(e.src_ip BETWEEN IPADDRESS '0.0.0.0' AND IPADDRESS '255.255.255.255',
             LEAST(n.prefix_len, 32),
             n.prefix_len)) = n.network;
```

The prefix length that `IPADDRESS_TRUNC` accepts depends on the address family: 0 through 32 for an
IPv4 address, and 0 through 128 for an IPv6 address. A prefix length above 32 for an IPv4 address
raises an error rather than returning `NULL`. Because `ipaddr_events` contains both IPv4 and IPv6
addresses, the preceding query uses [IFF](/sql-reference/functions/iff) and [LEAST](/sql-reference/functions/least)
to cap the prefix length at 32 for IPv4 addresses. For more information, see
[Join to a table of networks](/sql-reference/functions/ipaddress_trunc#label-ipaddress-trunc-join-networks) and [Handle tables that contain both IPv4 and IPv6 addresses](/sql-reference/functions/ipaddress_trunc#label-ipaddress-trunc-mixed-families).

To test membership in a set of individual addresses rather than a range, use `IN`:

Copy code

```
SELECT COUNT(*)
  FROM ipaddr_events
  WHERE src_ip IN (SELECT ip FROM ipaddr_allowlist);
```

To compare against a range with `BETWEEN`, store the first and last address of each range, or compute
them when you populate the reference table. For more information, see [Limitations for the IPADDRESS data type](#label-ipaddress-type-limitations). To break an address-with-prefix string such as
`192.0.2.0/24` into its parts, you can use [PARSE\_IP](/sql-reference/functions/parse_ip), which returns an object
rather than an IPADDRESS value.

## Convert to and from IPADDRESS

You can convert between VARCHAR and IPADDRESS with [TO\_IPADDRESS](/sql-reference/functions/to_ipaddress),
[TRY\_TO\_IPADDRESS](/sql-reference/functions/try_to_ipaddress), [CAST](/sql-reference/functions/cast), or the `::`
operator. Invalid text raises an error for `TO_IPADDRESS` and `CAST`, and returns `NULL` for `TRY_TO_IPADDRESS`.

You can convert an IPADDRESS value to text with `TO_VARCHAR` or `::VARCHAR`. The result is the
canonical address string.

## Limitations for the IPADDRESS data type

The following limitations apply to the IPADDRESS data type:

- Apache Iceberg™ tables don’t support IPADDRESS as a column type.
- The semi-structured aggregate functions `ARRAY_AGG`, `ARRAY_UNIQUE_AGG`, and `OBJECT_AGG` don’t
  accept IPADDRESS values. To aggregate addresses, cast them to VARCHAR first.
- The IPADDRESS data type isn’t supported in stored procedures or user-defined functions (UDFs) written in a
  language other than SQL, such as Python, Java, JavaScript, or Scala.
- The IPADDRESS data type isn’t supported in Snowpark.
- Snowflake doesn’t support CIDR literals or a CIDR data type, and no function returns the last address of a
  range as an IPADDRESS value. [PARSE\_IP](/sql-reference/functions/parse_ip) returns the start and end of a range, but
  in an OBJECT rather than as IPADDRESS values. To group or match addresses by network, use
  [IPADDRESS\_TRUNC](/sql-reference/functions/ipaddress_trunc). To filter on an arbitrary range, use `BETWEEN`, as
  described in [Filter and join on address ranges](#label-ipaddress-type-ranges).

## Examples for the IPADDRESS data type

The following examples show how to store and query IPADDRESS values:

- [Find the addresses in a subnet](#label-ipaddress-example-subnet)
- [Insert an IPADDRESS value into a table](#label-ipaddress-example-inserting)
- [Use an ANSI literal](#label-ipaddress-example-ansi-literal)
- [Compare and aggregate IPADDRESS values](#label-ipaddress-example-minmax)

For examples that group addresses by subnet, mask the host bits of addresses, and join to a table of networks, see
[IPADDRESS\_TRUNC](/sql-reference/functions/ipaddress_trunc).

### Find the addresses in a subnet

This example filters events to the addresses in the `10.0.0.0/8` block by comparing against the
first and last address of that block.

1. Create a table of events and insert addresses from inside and outside the block:

   Copy code

   ```
   CREATE OR REPLACE TABLE ipaddr_events (event_id NUMBER, src_ip IPADDRESS);

   INSERT INTO ipaddr_events VALUES
     (1, '10.0.0.7'),
     (2, '10.255.255.254'),
     (3, '192.0.2.1'),
     (4, '2001:db8::1');
   ```
2. Select the events whose source address falls in the block:

   Copy code

   ```
   SELECT event_id, src_ip
     FROM ipaddr_events
     WHERE src_ip BETWEEN TO_IPADDRESS('10.0.0.0') AND TO_IPADDRESS('10.255.255.255')
     ORDER BY src_ip;
   ```

   ```
   +----------+----------------+
   | EVENT_ID | SRC_IP         |
   |----------+----------------|
   |        1 | 10.0.0.7       |
   |        2 | 10.255.255.254 |
   +----------+----------------+
   ```

### Insert an IPADDRESS value into a table

- Create a table with a column of IPADDRESS type and insert IPv4 and IPv6 values:

  Copy code

  ```
  CREATE TABLE sample_ipaddress_table(ip_col IPADDRESS);

  INSERT INTO sample_ipaddress_table VALUES
    ('192.0.2.1'),
    ('2001:db8::1');
  ```
- Query the table:

  Copy code

  ```
  SELECT ip_col FROM sample_ipaddress_table ORDER BY ip_col;
  ```

  ```
  +-------------+
  | IP_COL      |
  |-------------|
  | 192.0.2.1   |
  | 2001:db8::1 |
  +-------------+
  ```

### Use an ANSI literal

- Specify an IPADDRESS literal without a separate `CAST`:

  Copy code

  ```
  SELECT IPADDRESS '2001:db8::1' AS ip;
  ```

  ```
  +-------------+
  | IP          |
  |-------------|
  | 2001:db8::1 |
  +-------------+
  ```

### Compare and aggregate IPADDRESS values

- `MIN` and `MAX` follow numeric address order:

  Copy code

  ```
  SELECT MIN(ip_col), MAX(ip_col) FROM sample_ipaddress_table;
  ```

  ```
  +-------------+-------------+
  | MIN(IP_COL) | MAX(IP_COL) |
  |-------------+-------------|
  | 192.0.2.1   | 2001:db8::1 |
  +-------------+-------------+
  ```
