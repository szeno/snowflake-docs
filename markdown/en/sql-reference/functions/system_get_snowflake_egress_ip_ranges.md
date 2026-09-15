Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES

Using egress IP addresses you generate with Snowflake, you can allow ingress access from the following Snowflake features:

- External access from UDFs and procedures
- Snowpark Container Services external access and Snowflake Openflow on Snowpark Container Services
- Snowflake Git integration with IP-restricted Git servers

Returns a list of egress IP address ranges (as Classless Inter-Domain Routing (CIDR) IP addresses) that you can use to represent
Snowflake in a server’s IP allowlist.

Use this function to obtain a list of egress IP address ranges with which to allow Snowflake traffic on external servers. You
can add IP addresses from the list to the allowlist on an external server from which Snowflake makes requests.

For example, you can allow requests by user-defined functions (UDFs) deployed on Snowflake to access resources on an external server.
To do this, you add Snowflake egress IP addresses to the network firewall for your server.

Addresses in the returned list expire. You can automate refreshes from the list as described in
[Securing ingress of Snowflake requests with egress IP addresses](/user-guide/egress-ip/network-egress).

## Syntax

Copy code

```
SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES( [ <hideAnnotations> ] )
```

## Arguments

**Required:**

None.

**Optional:**

`hideAnnotations`
:   `BOOLEAN`. Available in Azure regions. When `TRUE`, the function omits the inline comments from the JSON output. When `FALSE` or omitted, Azure output includes those comments.

    Default: `FALSE`

## Returns

Returns JSON containing a list of CIDR IP addresses, effective date, and an expiration date for each address. The following example shows what the
return value looks like:

Copy code

```
SELECT SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES();
```

Copy code

```
{
  "ipv4_prefix": "153.45.151.0/24",
  "effective": "2025-06-30T23:59:59Z",
  "expires": "2026-08-30T23:59:59Z"
}
```

[Preview Feature](/release-notes/preview-features) — Open

Support for this function on Azure is in preview.

Additionally, in Azure regions you see a more detailed output:

Copy code

```
[
  {
    "ipv4_prefix": "153.45.139.0/24",
    "effective": "2026-08-19T00:00:00Z", // Allowlist this IP range before this date
    "published": "2026-07-15T14:38:56.923Z", // This IP range was published on this date, refresh allowlists if updated before this date.
    "expires": "2026-11-17T00:00:00Z",
    "usage": [
      "Network Identifier - use for Azure services such as Storage, Key Vault",
      "Stable Egress IP - use for endpoints hosted outside of Azure"
    ]
  },
  {
    "ipv4_prefix": "153.45.182.0/24",
    "effective": "2026-08-19T00:00:00Z", // Allowlist this IP range before this date
    "published": "2026-07-15T14:38:56.923Z", // This IP range was published on this date, refresh allowlists if updated before this date.
    "expires": "2026-11-17T00:00:00Z",
    "usage": [
      "Network Identifier - use for Azure services such as Storage, Key Vault"
    ]
  }
]
```

To hide inline comments, pass `TRUE` for the optional `hideAnnotations` argument:

Copy code

```
SELECT SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES(TRUE);
```

Copy code

```
[
  {
    "ipv4_prefix": "153.45.139.0/24",
    "effective": "2026-08-19T00:00:00Z",
    "published": "2026-07-15T14:38:56.923Z",
    "expires": "2026-11-17T00:00:00Z",
    "usage": [
      "Network Identifier - use for Azure services such as Storage, Key Vault",
      "Stable Egress IP - use for endpoints hosted outside of Azure"
    ]
  },
  {
    "ipv4_prefix": "153.45.182.0/24",
    "effective": "2026-08-19T00:00:00Z",
    "published": "2026-07-15T14:38:56.923Z",
    "expires": "2026-11-17T00:00:00Z",
    "usage": [
      "Network Identifier - use for Azure services such as Storage, Key Vault"
    ]
  }
]
```

On Azure, the output includes the standard `ipv4_prefix`, `effective`, and `expires` fields. The output also includes two additional fields:

- `published`: The date when Snowflake published this IP range. Refresh your allowlist if you last updated it before this date.
- `usage`: Describes how Snowflake uses the range. Values can include network identifiers for Azure services such as Storage and Key Vault, and stable egress IPs for endpoints hosted outside of Azure.

## Usage notes

Keep in mind the following about the returned list of CIDR IP address ranges:

- Each IP address expires. The returned list includes both the IP address and its expiration date and time. To allow continued access
  from Snowflake, automate refreshing your allowlist with addresses that have not yet expired.

  For more information, see [Securing ingress of Snowflake requests with egress IP addresses](/user-guide/egress-ip/network-egress).
- Addresses are scoped to the region of your Snowflake deployment. Addresses for one region differ from those for another region.
- Addresses are shared among Snowflake accounts in the region. In other words, they’re not unique to a Snowflake account.
- If an address has a `published` date after your last firewall update, update your allowlist with that address before its
  `effective` date.
