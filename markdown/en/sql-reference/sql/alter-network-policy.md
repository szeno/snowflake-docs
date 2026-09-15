# ALTER NETWORK POLICY

Modifies the properties for an existing network policy.

Note

Only the network policy owner (that is, the role with the OWNERSHIP privilege on the network policy) or higher can alter a network policy.

See also:
:   [CREATE NETWORK POLICY](/sql-reference/sql/create-network-policy) , [DESCRIBE NETWORK POLICY](/sql-reference/sql/desc-network-policy) , [DROP NETWORK POLICY](/sql-reference/sql/drop-network-policy) , [SHOW NETWORK POLICIES](/sql-reference/sql/show-network-policies)

## Syntax

Copy code

```
ALTER NETWORK POLICY [ IF EXISTS ] <name> SET {
    [ ALLOWED_NETWORK_RULE_LIST = ( '<network_rule>' [ , '<network_rule>' , ... ] ) ]
    [ BLOCKED_NETWORK_RULE_LIST = ( '<network_rule>' [ , '<network_rule>' , ... ] ) ]
    [ ALLOWED_IP_LIST = ( [ '<ip_address>' ] [ , '<ip_address>' ... ] ) ]
    [ BLOCKED_IP_LIST = ( [ '<ip_address>' ] [ , '<ip_address>' ... ] ) ]
    [ COMMENT = '<string_literal>' ] }

ALTER NETWORK POLICY [ IF EXISTS ] <name> UNSET COMMENT

ALTER NETWORK POLICY <name> ADD { ALLOWED_NETWORK_RULE_LIST = '<network_rule>' | BLOCKED_NETWORK_RULE_LIST = '<network_rule>' }

ALTER NETWORK POLICY <name> REMOVE { ALLOWED_NETWORK_RULE_LIST = '<network_rule>' | BLOCKED_NETWORK_RULE_LIST = '<network_rule>' }

ALTER NETWORK POLICY <name>  RENAME TO <new_name>

ALTER NETWORK POLICY <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER NETWORK POLICY <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the network policy to alter. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies the parameter to set for the network policy:

    > `ALLOWED_NETWORK_RULE_LIST = ( 'network_rule' [ , 'network_rule' , ... ] )`
    > :   Specifies a list of [network rules](/user-guide/network-rules) that contain the network identifiers that are allowed access to
    >     Snowflake. There is no limit on the number of network rules in the list.
    >
    >     Replaces existing network rules in the allowed list. To add network rules without replacing existing ones, use the
    >     `ALTER NETWORK POLICY ... ADD` command.
    >
    > `BLOCKED_NETWORK_RULE_LIST = ( 'network_rule' [ , 'network_rule' , ... ] )`
    > :   Specifies a list of network rules that contain the network identifiers that are denied access to Snowflake. There is no limit on the
    >     number of network rules in the list.
    >
    >     Replaces existing network rules in the blocked list. To add network rules without replacing existing ones, use the
    >     `ALTER NETWORK POLICY ... ADD` command.
    >
    > `ALLOWED_IP_LIST = ( [ ip_address ] [ , ip_address , ... ] )`
    > :   Specifies a list of IPv4 addresses that are allowed access to your Snowflake account. This is referred to as the *allowed list*.
    >
    >     Snowflake recommends using network rules in conjunction with network policies rather than using this property. Use the
    >     `ALLOWED_NETWORK_RULE_LIST` property to specify network rules that contain IPv4 or IPv6 addresses.
    >
    >     If you are not yet using network rules, specify at least one IPv4 address or CIDR block range to allow access to your Snowflake
    >     account. Additionally, if you are not using network rules and this property is specified with an empty list, no IPv4 addresses are
    >     allowed to access your Snowflake account.
    >
    >     Note
    >
    >     The `ALLOWED_IP_LIST` parameter supports IPv4 addresses only. To allow or block IPv6 addresses, use network rules with
    >     `TYPE = IPV6` and add them to the `ALLOWED_NETWORK_RULE_LIST` or `BLOCKED_NETWORK_RULE_LIST`. IPv4 and IPv6 network
    >     rules are evaluated independently, so if your network has dual-stack (IPv4 and IPv6) traffic, create separate network rules
    >     for each address family and add both to the network policy. To enable IPv6 ingress for your account, see
    >     [IPv6 addresses](/user-guide/network-rules#label-network-rule-ipv6-addresses).
    >
    > `BLOCKED_IP_LIST = ( [ ip_address ] [ , ip_address , ... ] )`
    > :   Specifies a list of IPv4 addresses that are denied access to your Snowflake account. This is referred to as the *blocked list*.
    >     To unset this parameter, specify a different CIDR block range, a series of IPv4 addresses, or a single IPv4 address.
    >
    >     Snowflake recommends using network rules in conjunction with network policies rather than using this parameter. Use the
    >     `BLOCKED_NETWORK_RULE_LIST` property to specify network rules that contain IPv4 or IPv6 addresses.
    >
    >     To block public access, use a network rule and add the network rule to the `BLOCKED_NETWORK_RULE_LIST` property. The result is
    >     that only IP addresses that use private connectivity, such as AWS PrivateLink, can access your Snowflake account.
    >
    >     Default: No value; no IP addresses in `ALLOWED_IP_LIST` property are blocked.
    >
    > `COMMENT = 'string_literal'`
    > :   Adds a comment or overwrites an existing comment for the network policy.
    >
    > `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    > :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.
    >
    >     The tag value is always a string, and the maximum number of characters for the tag value is 256.
    >
    >     For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies the properties to unset for the network policy, which resets them to the defaults:

    > - `COMMENT`, which removes the comment, if one exists, for the network policy.
    > - `TAG tag_name [ , tag_name ... ]`

[Preview Feature](/release-notes/preview-features) — Open

The `ADD` and `REMOVE` commands are in preview, and are available to all accounts on AWS.

`ADD { ALLOWED_NETWORK_RULE_LIST = 'network_rule' | BLOCKED_NETWORK_RULE_LIST = 'network_rule' }`
:   Adds a network rule to the allowed or blocked list of the network policy without removing existing ones.

`REMOVE { ALLOWED_NETWORK_RULE_LIST = 'network_rule' | BLOCKED_NETWORK_RULE_LIST = 'network_rule' }`
:   Removes a network rule from the allowed or blocked list of the network policy.

`RENAME TO ...`
:   Specifies a new name for the existing network policy.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Network policy | Modifying a network policy requires a role with the OWNERSHIP privilege on the network policy. |

Expand

Show lessSee more

For general information about roles and privilege grants for performing SQL actions on securable objects, see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A user whose IP address is on the ALLOWED LIST and who attempts to alter a network policy by removing their entire IP CDIR range sees the
  following message:

  ```
  Changes cannot be applied to the network policy RULE_BASED_POLICY because
  current IP address/token x.xx.xxx.xxx is not allowed in it.
  ```

  This design helps prevent the currently logged-in user from being accidentally blocked or locked out from their Snowflake account.
- Don’t modify a network policy to have empty `ALLOWED_IP_LIST` and `BLOCKED_IP_LIST` properties. Use network rules in
  conjunction with the network policy to manage access to your Snowflake account.
- The `SET` action for the allowed/blocked lists is not additive (that is, it removes all IP addresses in the existing lists
  for the network policy and replaces them with the specified lists).

  As a result, to make additions to the existing lists, you must specify the new IP addresses and replicate the existing lists.
- Each `ip_address` can cover a range of addresses using Classless Inter-Domain Routing (CIDR) notation:

  `ip_address[/optional_prefix_length]`

  For example:

  `192.168.1.0/24`
- When a network policy includes values for both `ALLOWED_IP_LIST` and `BLOCKED_IP_LIST`, Snowflake applies the blocked list
  first.
- Do not add `0.0.0.0/0` to `BLOCKED_IP_LIST`. Because Snowflake applies the blocked list first, this would block your own
  access. Additionally, in order to block all IP addresses except a select list, you only need to add IP addresses to `ALLOWED_IP_LIST`.
  Snowflake automatically blocks all IP addresses not included in the allowed list.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Example

For example, use ALTER NETWORK POLICY to change a network policy named `allow_access_policy` that allows network traffic defined by
`allow_access_rule` to also block network traffic defined by `block_access_rule`, consistent with the network rules defined in
[IP ranges](/user-guide/network-policies#label-ip-ranges). First, show the current policy:

Copy code

```
DESC NETWORK POLICY allow_access_policy;
```

```
+---------------------------+-------------------+
| name                      | value             |
|---------------------------+-------------------|
| ALLOWED_NETWORK_RULE_LIST | allow_access_rule |
+---------------------------+-------------------+
```

Next, change `allow_access_policy` to also use `block_access_rule`, and then show the updated policy:

Copy code

```
ALTER NETWORK POLICY IF EXISTS allow_access_policy SET
  BLOCKED_NETWORK_RULE_LIST = ('block_access_rule');
DESC NETWORK POLICY allow_access_policy;
```

```
+---------------------------+-------------------+
| name                      | value             |
|---------------------------+-------------------|
| ALLOWED_NETWORK_RULE_LIST | ALLOW_ACCESS_RULE |
| BLOCKED_NETWORK_RULE_LIST | BLOCK_ACCESS_RULE |
+---------------------------+-------------------+
```

Next, rename the updated policy to describe use of both rules:

Copy code

```
ALTER NETWORK POLICY allow_access_policy RENAME TO limit_access_policy;
```

Then, add a comment which describes that `limit_access_policy` is defined by network rules:

Copy code

```
ALTER NETWORK POLICY limit_access_policy SET COMMENT = 'No_Lists_See_Rules';
SHOW NETWORK POLICIES;
```

Output from SHOW NETWORK POLICIES includes the updated policy name, and comment included in the changed (altered) network policy.

```
+-------------------------------+---------------------+--------------------+----------------------------+----------------------------+----------------------------------+----------------------------------+
| created on                    | name                | comment            | entries_in_allowed_ip_list | entries_in_blocked_ip_list | entries_in_allowed_network_rules | entries_in_blocked_network_rules |
|-------------------------------+------------------------------------------|----------------------------|----------------------------|----------------------------------|----------------------------------|
|...                            |                     |                    |                            |                            |                                  |                                  |
|-------------------------------+------------------------------------------|----------------------------|----------------------------|----------------------------------|----------------------------------|
| 2024-12-04 10:33:19.853 -0800 | LIMIT_ACCESS_POLICY | NO_LISTS_SEE_RULES |                           0|                           0|                                 1|                                 1|
|-------------------------------+------------------------------------------|----------------------------|----------------------------|----------------------------------|----------------------------------|
|...                            |                     |                    |                            |                            |                                  |                                  |
+-------------------------------+---------------------+--------------------+----------------------------+----------------------------+----------------------------------+----------------------------------+
```
