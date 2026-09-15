# ALTER NETWORK RULE

Modifies an existing network rule.

See also:
:   [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) , [DROP NETWORK RULE](/sql-reference/sql/drop-network-rule) , [DESCRIBE NETWORK RULE](/sql-reference/sql/desc-network-rule) , [SHOW NETWORK RULES](/sql-reference/sql/show-network-rules)

## Syntax

Copy code

```
ALTER NETWORK RULE [ IF EXISTS ] <name> SET
  VALUE_LIST = ( '<value>'  [ , '<value>', ... ] )
  [ COMMENT = '<string_literal>' ]

ALTER NETWORK RULE [ IF EXISTS ] <name> UNSET { VALUE_LIST | COMMENT }
```

## Parameters

`name`
:   Specifies the identifier of the network rule.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in
    double quotes are case-sensitive.

`SET ...`
:   Specifies the properties to set for the network rule:

    `VALUE_LIST = ( 'value' [, 'value', ...] )`
    :   Replaces the current network identifiers with a new list of identifiers. Using this command is not additive; previously specified
        values are removed when you set a new value list.

        Valid values in the list are determined by the type of network rule:

        > - When `TYPE = IPV4`, each value must be a valid IPv4 address or [range of addresses](/sql-reference/sql/alter-network-rule#label-alter-network-rule-usage-notes).
        > - When `TYPE = AWSVPCEID`, each value must be a valid VPCE ID. VPC IDs are not supported.
        > - When `TYPE = AZURELINKID`, each value must be a valid LinkID of an Azure [private endpoint](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview).
        >   Execute the [SYSTEM$GET\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_privatelink_authorized_endpoints) function to retrieve the LinkID associated
        >   with an account.
        > - When `TYPE = GCPPSCID`, each value must be a valid pscConnectionID of a [Google Cloud Private Service Connect (PSC) endpoint](https://docs.cloud.google.com/vpc/docs/private-service-connect#endpoints). Run the [gcloud compute forwarding-rules describe command](https://docs.cloud.google.com/memorystore/docs/cluster/multiple-vpcs-automatically-registered-psc-connection#get_the_connection_id_1) to get the pscConnectionID for each forwarding rule.
        > - When `TYPE = HOST_PORT`, each value must resolve to a valid domain. Optionally, it can also include a port or range of ports.
        >
        >   In most cases, the valid port range is 1-65535. If you do not specify a port, it defaults to 443. If an external network location supports dynamic ports, you need to specify all possible ports.
        >
        >   To allow access to all ports, define the port as 0; for example, `example.com:0`.
        >
        >   When the value resolves to a domain, you can use a single asterisk as a wildcard character. The asterisk matches only alphanumeric
        >   characters and hyphens (`-`).
        >
        >   Wildcards are supported only for a single level of subdomains, as in the following examples:
        >
        >   - `*.google.com`
        >   - `snowflake-*.google.com` and `snowflake*abc.google.com`
        >
        >   You can allow requests to all outbound endpoints by specifying `0.0.0.0` as the domain, as in the examples below.
        >   When you specify `0.0.0.0` as the domain, you may use only 443 and 80 as port values.
        >
        >   - Allow access to all endpoints at port 80
        >
        >     Copy code
        >
        >     ```
        >     value_list = ('0.0.0.0:80');
        >     ```
        >   - Allow access to all endpoints at port 443
        >
        >     Copy code
        >
        >     ```
        >     value_list = ('0.0.0.0:443');
        >     ```
        >
        >     Copy code
        >
        >     ```
        >     value_list = ('0.0.0.0');
        >     ```
        >   - Allow access to all endpoints at both port 80 and 443
        >
        >     Copy code
        >
        >     ```
        >     value_list = ('0.0.0.0:80', '0.0.0.0:443');
        >     ```
        > - When `TYPE = PRIVATE_HOST_PORT`, specify one valid domain.
        >
        >   In most cases, the valid port range is 1-65535. If you do not specify a port, it defaults to 443. If an external network location supports dynamic ports, you need to specify all possible ports.
        >
        >   To allow access to all ports, define the port as 0; for example, `example.com:0`.
        > - When `TYPE = COMPUTE_POOL`, each value must be a valid compute pool name, or `'ALL'` to match all Snowpark Container Services compute pools in the account.

    `COMMENT = 'string_literal'`
    :   Adds a comment for the first time or overwrites an existing comment.

`UNSET ...`
:   Clears properties of the network rule:

    `VALUE_LIST`
    :   Removes all network identifiers from the network rule.

    `COMMENT`
    :   Removes the comment that was associated with the network rule.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Network Rule | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When specifying IP addresses for a network rule, Snowflake supports ranges of IP addresses using [Classless Inter-Domain Routing (CIDR) notation](https://tools.ietf.org/html/rfc4632).

  For example, `192.168.1.0/24` represents all IPv4 addresses in the range of `192.168.1.0` to `192.168.1.255`.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Example

Modify a network rule that is used to allow or block traffic from a range of IPv4 addresses. Assumes that `TYPE = IPV4` for the
network rule.

Copy code

```
ALTER NETWORK RULE cloud_network SET VALUE_LIST = ('47.88.25.32/27');
```

Modify a network rule that is used to allow or block traffic over AWS PrivateLink. Assumes that `TYPE = AWS_VPCEID` for the network
rule.

Copy code

```
ALTER NETWORK RULE corporate_network SET VALUE_LIST = ('vpce-123abc3420c1931');
```

Modify a network rule that is used to allow or block traffic over Google Cloud Private Service Connect. Assumes that `TYPE = GCPPSCID`
for the network rule.

Copy code

```
ALTER NETWORK RULE corporate_network SET VALUE_LIST = ('31618973889077266');
```

Modify a network rule that is used to allow traffic to an external destination. Assumes that `TYPE = HOST_PORT` for the network
rule.

Copy code

```
ALTER NETWORK RULE external_access_rule SET VALUE_LIST = ('example.com', 'example.com:443');
```

Modify a network rule that is used to allow or block traffic from IPv6 addresses. Assumes that `TYPE = IPV6` for the network
rule.

Copy code

```
ALTER NETWORK RULE ipv6_network SET VALUE_LIST = ('2001:db8::/32', '2001:0db8:85a3::8a2e:370:7334');
```
