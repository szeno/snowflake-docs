Categories:
:   [IPADDRESS functions](/sql-reference/functions-ipaddress) (Network)

# IPADDRESS\_TRUNC

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the network address of an [IPADDRESS](/sql-reference/data-types-ipaddress) value for a given
prefix length. The function keeps the leading bits of the address that the prefix length specifies and
sets the remaining host bits to zero. For example, truncating `192.168.129.255` to a prefix length of
17 returns `192.168.128.0`.

Use this function to group addresses by subnet, to mask the host bits of addresses so that they’re less
precise, and to match addresses against networks that are stored as a network address and a prefix length.

See also:

- [IPADDRESS data type](/sql-reference/data-types-ipaddress)
- [TO\_IPADDRESS](/sql-reference/functions/to_ipaddress)
- [TRY\_TO\_IPADDRESS](/sql-reference/functions/try_to_ipaddress)

## Syntax

Copy code

```
IPADDRESS_TRUNC( <ip_address> , <prefix_length> )
```

## Arguments

`ip_address`
:   An expression of type `IPADDRESS`.

`prefix_length`
:   An integer expression that specifies the number of leading bits of the address to keep:

    - For an IPv4 address, specify a value from 0 through 32.
    - For an IPv6 address, specify a value from 0 through 128.

    The prefix length doesn’t need to be a constant. For example, you can pass a column that stores a
    prefix length for each row.

## Returns

Returns a value of type [IPADDRESS](/sql-reference/data-types-ipaddress) with the same address family
as the input.

If either argument is `NULL`, the function returns `NULL`.

## Usage notes

- The valid range of the prefix length depends on the address family of each input value. If the prefix
  length is outside that range, the function raises an error rather than returning `NULL`. For
  example, a prefix length of 48 is valid for an IPv6 address but raises the following error for an
  IPv4 address:

  ```
  Invalid prefix length 48 for IPADDRESS_TRUNC; expected 0 through 32 for IPv4 or 0 through 128 for IPv6.
  ```

  If Snowflake can detect the invalid prefix length when it compiles the query, the query fails with a
  SQL compilation error instead. This happens when the prefix length is a constant outside 0 through 128,
  or when both arguments are constants. For example, `IPADDRESS_TRUNC(IPADDRESS '192.0.2.1', 33)` returns
  the following error:

  ```
  SQL compilation error: error line 1 at position 7
  invalid argument for function [IPADDRESS_TRUNC] unexpected argument [33] at position 2,
  ```
- If a column contains both IPv4 and IPv6 addresses, choose the prefix length for each address family
  separately. Put the choice in the `prefix_length` argument, for example with [IFF](/sql-reference/functions/iff),
  so that each row receives a prefix length that’s valid for its own family. To test whether a value is an
  IPv4 address, compare it with the IPv4 range:

  Copy code

  ```
  ip_col BETWEEN IPADDRESS '0.0.0.0' AND IPADDRESS '255.255.255.255'
  ```

  For an example, see [Handle tables that contain both IPv4 and IPv6 addresses](#label-ipaddress-trunc-mixed-families).
- A prefix length of 32 for an IPv4 address, or 128 for an IPv6 address, returns the input unchanged.
  A prefix length of 0 returns `0.0.0.0` for an IPv4 address and `::` for an IPv6 address.
- The function returns a single `IPADDRESS` value, the network address, not a CIDR range. The result
  doesn’t record the prefix length. For other limitations, see [Limitations for the IPADDRESS data type](/sql-reference/data-types-ipaddress#label-ipaddress-type-limitations).

## Examples

The examples in this section use the following table:

Copy code

```
CREATE OR REPLACE TABLE ipaddress_trunc_events (event_id NUMBER, src_ip IPADDRESS);

INSERT INTO ipaddress_trunc_events VALUES
  (1, '192.0.2.1'),
  (2, '192.0.2.77'),
  (3, '198.51.100.23'),
  (4, '2001:db8:abcd:1234::1'),
  (5, '2001:db8:abcd:9876:5:4:3:2'),
  (6, '2001:db8:ffff::1');
```

This section contains the following examples:

- [Return the network address of an IPv4 address and an IPv6 address](#label-ipaddress-trunc-basic)
- [Group addresses by subnet](#label-ipaddress-trunc-group-by-subnet)
- [Mask the host bits of addresses](#label-ipaddress-trunc-mask-host-bits)
- [Join to a table of networks](#label-ipaddress-trunc-join-networks)
- [Handle tables that contain both IPv4 and IPv6 addresses](#label-ipaddress-trunc-mixed-families)

### Return the network address of an IPv4 address and an IPv6 address

The following example truncates an IPv4 address to a prefix length of 17 and an IPv6 address to a prefix
length of 49:

Copy code

```
SELECT IPADDRESS_TRUNC(IPADDRESS '192.168.129.255', 17) AS ipv4_network,
       IPADDRESS_TRUNC(IPADDRESS '2001:db8:abcd:1234::1', 49) AS ipv6_network;
```

```
+---------------+-----------------+
| IPV4_NETWORK  | IPV6_NETWORK    |
|---------------+-----------------|
| 192.168.128.0 | 2001:db8:abcd:: |
+---------------+-----------------+
```

### Group addresses by subnet

The following example counts events for each IPv4 `/24` subnet and each IPv6 `/48` subnet:

Copy code

```
SELECT IPADDRESS_TRUNC(
         src_ip,
         IFF(src_ip BETWEEN IPADDRESS '0.0.0.0' AND IPADDRESS '255.255.255.255', 24, 48)) AS subnet,
       COUNT(*) AS events
  FROM ipaddress_trunc_events
  GROUP BY subnet
  ORDER BY subnet;
```

```
+-----------------+--------+
| SUBNET          | EVENTS |
|-----------------+--------|
| 192.0.2.0       |      2 |
| 198.51.100.0    |      1 |
| 2001:db8:abcd:: |      2 |
| 2001:db8:ffff:: |      1 |
+-----------------+--------+
```

### Mask the host bits of addresses

The following example sets the host bits of each address to zero, keeping the IPv4 `/24` network and the
IPv6 `/48` network:

Copy code

```
SELECT event_id,
       src_ip,
       IPADDRESS_TRUNC(
         src_ip,
         IFF(src_ip BETWEEN IPADDRESS '0.0.0.0' AND IPADDRESS '255.255.255.255', 24, 48)) AS masked_ip
  FROM ipaddress_trunc_events
  ORDER BY event_id;
```

```
+----------+----------------------------+-----------------+
| EVENT_ID | SRC_IP                     | MASKED_IP       |
|----------+----------------------------+-----------------|
|        1 | 192.0.2.1                  | 192.0.2.0       |
|        2 | 192.0.2.77                 | 192.0.2.0       |
|        3 | 198.51.100.23              | 198.51.100.0    |
|        4 | 2001:db8:abcd:1234::1      | 2001:db8:abcd:: |
|        5 | 2001:db8:abcd:9876:5:4:3:2 | 2001:db8:abcd:: |
|        6 | 2001:db8:ffff::1           | 2001:db8:ffff:: |
+----------+----------------------------+-----------------+
```

### Join to a table of networks

The following example matches each event to a table that stores each network as a network address and
a prefix length. The network address must have its host bits cleared, or no address matches it.

1. Create the table of networks:

   Copy code

   ```
   CREATE OR REPLACE TABLE ipaddress_trunc_networks (
     network IPADDRESS,
     prefix_len INTEGER,
     owner VARCHAR);

   INSERT INTO ipaddress_trunc_networks VALUES
     ('192.0.2.0', 24, 'Office'),
     ('198.51.100.0', 22, 'VPN'),
     ('2001:db8:abcd::', 48, 'Data center');
   ```
2. Join each event to the network that contains it. Because the table of networks contains both IPv4 and
   IPv6 networks, the join compares IPv4 events with IPv6 networks. To keep the prefix length valid for an
   IPv4 event, the query caps it at 32 with [LEAST](/sql-reference/functions/least). An IPv4 address never equals
   an IPv6 network address, so the capped comparison doesn’t produce false matches:

   Copy code

   ```
   SELECT e.event_id, e.src_ip, n.owner
     FROM ipaddress_trunc_events AS e
     LEFT OUTER JOIN ipaddress_trunc_networks AS n
       ON IPADDRESS_TRUNC(
            e.src_ip,
            IFF(e.src_ip BETWEEN IPADDRESS '0.0.0.0' AND IPADDRESS '255.255.255.255',
                LEAST(n.prefix_len, 32),
                n.prefix_len)) = n.network
     ORDER BY e.event_id;
   ```

   ```
   +----------+----------------------------+-------------+
   | EVENT_ID | SRC_IP                     | OWNER       |
   |----------+----------------------------+-------------|
   |        1 | 192.0.2.1                  | Office      |
   |        2 | 192.0.2.77                 | Office      |
   |        3 | 198.51.100.23              | VPN         |
   |        4 | 2001:db8:abcd:1234::1      | Data center |
   |        5 | 2001:db8:abcd:9876:5:4:3:2 | Data center |
   |        6 | 2001:db8:ffff::1           | NULL        |
   +----------+----------------------------+-------------+
   ```

### Handle tables that contain both IPv4 and IPv6 addresses

A single prefix length is often valid for only one address family. The following query fails because
the table contains IPv4 addresses and 48 is outside the 0 through 32 range for IPv4:

Copy code

```
SELECT IPADDRESS_TRUNC(src_ip, 48) FROM ipaddress_trunc_events;
```

```
Invalid prefix length 48 for IPADDRESS_TRUNC; expected 0 through 32 for IPv4 or 0 through 128 for IPv6.
```

To process every row, choose a valid prefix length for each row in the `prefix_length` argument, as shown
in the earlier examples:

Copy code

```
SELECT IPADDRESS_TRUNC(
         src_ip,
         IFF(src_ip BETWEEN IPADDRESS '0.0.0.0' AND IPADDRESS '255.255.255.255', 24, 48)) AS subnet
  FROM ipaddress_trunc_events;
```

This query returns the same values as the `MASKED_IP` column in [Mask the host bits of addresses](#label-ipaddress-trunc-mask-host-bits).
