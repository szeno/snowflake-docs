# Network rules

Network rules are schema-level objects that group network identifiers into logical units.

Snowflake features that restrict network traffic can reference network rules rather than defining network identifiers directly in the
feature. A network rule does not define whether its identifiers should be allowed or blocked. The Snowflake feature that uses the network
rule specifies whether the identifiers in the rule are permitted or prohibited.

The following features use network rules to control network traffic:

- [Network policies](/user-guide/network-policies) use network rules to control inbound network traffic to the Snowflake service and
  internal stages.
- [External network access](/developer-guide/external-network-access/external-network-access-overview) uses network rules to restrict
  access to external network locations from a Snowflake UDF or procedure.

## Supported network identifiers

Administrators need to be able to restrict access based on the network identifier associated with the origin or destination of a request.
Network rules allow administrators to allow or block the following network identifiers:

Incoming requests:
:   - IPv4 addresses. Snowflake supports ranges of IP addresses using
      [Classless Inter-Domain Routing (CIDR) notation](https://tools.ietf.org/html/rfc4632). For example, `192.168.1.0/24` represents
      all IPv4 addresses in the range of `192.168.1.0` to `192.168.1.255`.
    - IPv6 addresses (AWS only). Snowflake supports full, compressed, and IPv4-embedded IPv6 address formats as defined in
      [RFC 4291](https://tools.ietf.org/html/rfc4291), including CIDR notation.
      For example, `2001:db8::/32` represents all IPv6 addresses starting with `2001:0db8:`. IPv6 network rules
      only support the `INGRESS` mode and don’t protect internal stages.
    - VPCE IDs of [AWS VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html#concepts-service-consumers) . VPC
      IDs are not supported.
    - LinkIDs of [Azure private endpoints](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview). Execute
      the [SYSTEM$GET\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_privatelink_authorized_endpoints) function to retrieve the LinkID associated with an
      account.
    - GCPPSCIDs (pscConnectionIDs) of [Google Cloud Private Service Connect (PSC) endpoints](https://docs.cloud.google.com/vpc/docs/private-service-connect#endpoints).
      Run the [gcloud compute forwarding-rules describe command](https://docs.cloud.google.com/memorystore/docs/cluster/multiple-vpcs-automatically-registered-psc-connection#get_the_connection_id_1) to get the pscConnectionID for each forwarding rule.
    - For `AWSVPCEID`, `AZURELINKID`, and `GCPPSCID` network rules in `INGRESS` mode, each value can also use tuple
      syntax to combine the private endpoint ID with one or more IPv4 addresses or CIDR ranges:
      `{private_link_id:ip_or_cidr[,ip_or_cidr, ...]}`. This syntax lets you control access for multiple subnets behind a
      private endpoint and lets you use private endpoint IDs with both public and private IPv4 addresses or CIDR ranges.

    Note

    Use PrivateLink ID and IP tuple network rules when multiple VPCs or VNets or accounts access Snowflake through a shared PrivateLink
    endpoint or transit gateway and you need to restrict which specific workloads behind that endpoint can connect (for example, particular
    VPCs, subnets, or hosts). They are especially useful when different business units share the same VPCE or PrivateLink ID, or when
    private IP ranges overlap, because Snowflake evaluates the combination of the PrivateLink ID and private IP, not the IP alone, to
    allow or block traffic. In simpler topologies, for example, a one-to-one PrivateLink-to-VPC mapping, or when IP-level filtering is
    enforced in your cloud network, standard PrivateLink- or IP-based network rules are usually sufficient, and tuples are not required.

    - Compute pool names of [Snowpark Container Services](/developer-guide/snowpark-container-services/overview) compute pools. Use `'ALL'` to
      match all SPCS compute pools in the account. For more information, see
      [Allow account access](/developer-guide/snowpark-container-services/spcs-execute-sql#allow-account-access).

Outgoing requests:
:   Domains, including a port range.

    In most cases, the valid port range is 1-65535. If you do not specify a port, it defaults to 443. If an external network location supports dynamic ports, you need to specify all possible ports.

    To allow access to all ports, define the port as 0; for example, `example.com:0`.

Each network rule contains a list of one or more network identifiers of the same type. The network rule’s `TYPE` property indicates
the type of identifiers that are included in the rule. For example, if the `TYPE` property is `IPV4`, then the network rule’s
value list must contain valid IPv4 addresses or address ranges in CIDR notation. If the `TYPE` property is `IPV6`, then the
value list must contain valid IPv6 addresses or address ranges in CIDR notation.

## Incoming vs. outgoing requests

The mode of a network rule indicates whether the Snowflake feature that uses the rule restricts incoming or outgoing requests.

### Incoming requests

[Network policies](/user-guide/network-policies) protect the Snowflake service and internal stages from incoming traffic. When a
network rule is used with a network policy, the administrator can set the mode to one of the following:

`INGRESS`
:   The behavior of the `INGRESS` mode depends on the value of the network rule’s `TYPE` property.

    - If `TYPE=IPV4`, by default the network rule controls access to the Snowflake service only.

      If the account administrator enables the [ENFORCE\_NETWORK\_RULES\_FOR\_INTERNAL\_STAGES](/sql-reference/parameters#label-enforce-network-rules-for-internal-stages) parameter, then `MODE=INGRESS` and `TYPE=IPV4` also protects an AWS internal stage.
    - If `TYPE=IPV6` (AWS only), the network rule controls access to the Snowflake service only. IPv6 network rules don’t protect
      internal stages.
    - If `TYPE=AWSVPCEID`, `TYPE=AZURELINKID`, or `TYPE=GCPPSCID`, then the network rule controls access to the Snowflake service only.

`INTERNAL_STAGE`
:   Controls access to an AWS internal stage without restricting access to the Snowflake service. Using this mode requires the following:

    - The account administrator must enable the [ENFORCE\_NETWORK\_RULES\_FOR\_INTERNAL\_STAGES](/sql-reference/parameters#label-enforce-network-rules-for-internal-stages) parameter.
    - The `TYPE` property of the network rule must be `AWSVPCEID`.
    - If you want to restrict access to an internal stage based on the VPCE ID of an interface endpoint, you must create a separate network
      rule by using the `INTERNAL_STAGE` mode.

    For accounts on Microsoft Azure, you cannot use a network rule to restrict access to the internal stage. However, you can [block all public network traffic](/user-guide/private-internal-stages-azure#label-private-internal-stage-azure-block-public) from accessing the internal stage.

`SNOWFLAKE_MANAGED_STORAGE_VOLUME`
:   Controls access to an AWS Snowflake-managed storage volume without restricting access to the Snowflake service. Using this
    mode requires the following:

    - The account administrator must enable the [ENFORCE\_NETWORK\_RULES\_FOR\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME](/sql-reference/parameters#label-enforce-network-rules-for-snowflake-managed-storage-volume) parameter.
    - The `TYPE` property of the network rule must be `AWSVPCEID`.

    For accounts on Microsoft Azure, you cannot use a network rule to restrict access to a Snowflake-managed storage volume. However, you can [block all public network traffic](/user-guide/private-managed-volumes-azure#label-private-snowflake-managed-storage-volumes-azure-block-public) from accessing the Snowflake-managed storage volume.

### Outgoing requests

Administrators can use network rules with features that control where requests can be sent. In these cases, the administrator defines the
network rule with the following mode:

`EGRESS`
:   Indicates that the network rule is used for traffic sent *from* Snowflake.

    Currently used with [external network access](/developer-guide/external-network-access/external-network-access-overview), which
    allows a UDF or procedure to send requests to an external network location.

## Creating a network rule

You need the CREATE NETWORK RULE privilege on the schema to create a network rule. By default, only the ACCOUNTADMIN and SECURITYADMIN
roles, along with the schema owner, have this privilege.

You can create a network rule using Snowsight or by executing a SQL command:

Snowsight:
:   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Governance & security** » **Network policies**, and then select the **Network Rules** tab.
    3. Select **+ Network Rule**.
    4. Enter the name of the network rule.
    5. Select the schema of the network rule. Network rules are schema-level objects.
    6. Optionally, add a descriptive comment for the network rule to help organize and maintain network rules in the schema.
    7. In the **Type** drop-down, select the [type of identifier](#label-network-rule-identifiers) being defined in the network
       rule.
    8. In the **Mode** drop-down, select the mode of the network rule. The `INGRESS` and `INTERNAL STAGE` modes indicate the
       network rule will be used with a network policy to restrict incoming requests and the `EGRESS` mode indicates the network rule
       will be used with an external access integration to restrict outgoing requests.
    9. Enter a comma-separated list of the identifiers that will be allowed or blocked when the network rule is added to a network policy. The
       identifiers in this list must all be of the type specified in the **Type** drop-down.
    10. Select **Create Network Rule**.

SQL:
:   An administrator can execute the [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) command to create a new network rule, specifying a list of
    network identifiers along with the type of those identifiers.

    For example, to use a custom role to create a network rule that can be used to allow or block traffic from a range of IP addresses:

    Copy code

    ```
    GRANT USAGE ON DATABASE securitydb TO ROLE network_admin;
    GRANT USAGE ON SCHEMA securitydb.myrules TO ROLE network_admin;
    GRANT CREATE NETWORK RULE ON SCHEMA securitydb.myrules TO ROLE network_admin;
    USE ROLE network_admin;

    CREATE NETWORK RULE cloud_network TYPE = IPV4 MODE = INGRESS VALUE_LIST = ('47.88.25.32/27');
    ```

### IPv4 addresses

When specifying IP addresses for a network rule, Snowflake supports ranges of IP addresses using [Classless Inter-Domain Routing (CIDR) notation](https://tools.ietf.org/html/rfc4632).

For example, `192.168.1.0/24` represents all IPv4 addresses in the range of `192.168.1.0` to `192.168.1.255`.

### IPv6 addresses

IPv6 network rules allow you to control ingress traffic to the Snowflake service based on IPv6 addresses. IPv6 network rules
are available on AWS deployments.

To allow IPv6 clients to connect to your account, set the
[ENABLE\_DUAL\_STACK\_LOAD\_BALANCER](/sql-reference/parameters#label-enable-dual-stack-load-balancer) account parameter to `TRUE`.
This configures dual-stack endpoints so that your account hostname resolves to both IPv4 and IPv6 addresses. After enabling
dual-stack endpoints, create IPv6 network rules to control which IPv6 addresses can access your account.

Snowflake supports the following IPv6 address formats as defined in [RFC 4291](https://tools.ietf.org/html/rfc4291):

- **Full format**: `2001:0000:130F:0000:0000:09C0:876A:130B`
- **Compressed format**: `2001::9C0:876A:130B`
- **IPv4-embedded**: `::ffff:192.0.2.1`
- **CIDR notation**: `2001:db8::/32`

IPv6 network rules only support the `INGRESS` mode and protect the Snowflake service. They don’t protect internal stages.
For dual-stack networks where clients connect over both IPv4 and IPv6, create separate network rules for each address family.

For more information, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule).

## Identifying network rules in your account

You can identify the network rules in your account using Snowsight or SQL.

Snowsight:
:   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Governance & security** » **Network policies**, and then select the **Network Rules** tab.

SQL:
:   Call the [NETWORK\_RULE\_REFERENCES](/sql-reference/functions/network_rule_references) Information Schema table function, or query the
    [NETWORK\_RULES](/sql-reference/account-usage/network_rules) or
    [NETWORK\_RULE\_REFERENCES](/sql-reference/account-usage/network_rule_references) Account Usage view.

## Modifying a network rule

You can modify the identifiers and comment of an existing network rule, but you cannot modify its type, mode, name, or schema.

To add or remove identifiers and comments from an existing network rule using Snowsight or SQL, do one of the following:

Snowsight:
:   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Governance & security** » **Network policies**, and then select the **Network Rules** tab.
    3. Find the network rule, select the **…** button, and then select **Edit**.
    4. Modify the comma-delimited list of identifiers or the comment.
    5. Select **Update Network Rule**.

SQL:
:   Execute an [ALTER NETWORK RULE](/sql-reference/sql/alter-network-rule) statement.

## Replication of network rules

Network rules are schema-level objects and are replicated with the database in which they are contained.

For information about replicating the network policies that use network rules, see [Replicating network policies](/user-guide/account-replication-security-integrations#label-account-replication-network-policy).

## Privileges and commands

| Command | Privilege | Description |
| --- | --- | --- |
| [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) | CREATE NETWORK RULE on SCHEMA | Creates a new network rule. |
| [ALTER NETWORK RULE](/sql-reference/sql/alter-network-rule) | OWNERSHIP on NETWORK RULE | Modifies an existing network rule. |
| [DROP NETWORK RULE](/sql-reference/sql/drop-network-rule) | OWNERSHIP on NETWORK RULE | Removes an existing network rule from the system. |
| [DESCRIBE NETWORK RULE](/sql-reference/sql/desc-network-rule) | OWNERSHIP on NETWORK RULE | Describes the properties of an existing network rule. |
| [SHOW NETWORK RULES](/sql-reference/sql/show-network-rules) | OWNERSHIP on NETWORK RULE or USAGE on SCHEMA | Lists all of the network rules in the system. |

Expand

Show lessSee more

## Snowflake-managed network rules

Feature — Generally Available

Not available in government regions.

Snowflake provides the SNOWFLAKE.NETWORK\_SECURITY schema that contains a suite of *built-in* network rules. Built-in network rules are one
type of Snowflake-managed network rule. Snowflake can update the NETWORK\_SECURITY schema with new, Snowflake-managed network rules. Built-in
network rules provide a secure, consistent, fast, and low-maintenance way to manage network security.

Snowflake-managed network rules align with easy-to-use Snowflake network policy and rule management features. Snowflake customers can add
Snowflake-managed rules to new or existing [network policies](/user-guide/network-policies). Snowflake continuously updates built-in
network rules without requiring regular maintenance by account administrators. For more information about adding a network rule to a network
policy, see [Modify a network policy](/user-guide/network-policies#label-modifying-network-policies).

Built-in network rules define the set of allowed IP addresses that a frequently used, third-party partner application uses to
connect with Snowflake. Snowflake automatically updates these rules to capture any changes that third-party providers make to their egress IP
addresses. For example, Snowflake manages a rule that defines the IP addresses that a Microsoft Power BI application uses to connect with
Snowflake. If Microsoft updates these addresses, Snowflake rules automatically update to reflect this change.

The following table lists current partner applications for which Snowflake maintains built-in network rules and information about the current
egress IP addresses for each partner application:

| SaaS applications | Egress IP addresses |
| --- | --- |
| dbt platform | [dbt platform IP addresses](https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses) |
| Microsoft Power BI | [Power BI IP ranges](https://www.microsoft.com/en-us/download/details.aspx?id=56519) |
| Microsoft Entra ID | [Azure IP ranges and service tags](https://www.microsoft.com/en-us/download/details.aspx?id=56519) |
| Microsoft Power Automate | [Azure IP ranges and service tags](https://www.microsoft.com/en-us/download/details.aspx?id=56519) |
| Microsoft Power Query Online | [Azure IP ranges and service tags](https://www.microsoft.com/en-us/download/details.aspx?id=56519) |
| Microsoft Azure DevOps | [Azure IP ranges and service tags](https://www.microsoft.com/en-us/download/details.aspx?id=56519) |
| Microsoft Azure Data Factory | [Azure IP ranges and service tags](https://www.microsoft.com/en-us/download/details.aspx?id=56519) |
| Qlik | [Qlik IP addresses](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Introduction/qlik-cloud-dns-ip.htm) |
| Tableau | [Tableau Cloud IP ranges](https://help.tableau.com/current/pro/desktop/en-us/publish_tableau_online_ip_authorization.htm) |
| GitHub Actions | [REST API endpoints for meta data](https://docs.github.com/en/rest/meta) |

Expand

Show lessSee more

### Working with Snowflake-managed network rules

To see the current list of Snowflake-managed network rules, run the [SHOW NETWORK RULES](/sql-reference/sql/show-network-rules) command to list the network rules in the SNOWFLAKE.NETWORK\_SECURITY schema:

Copy code

```
SHOW NETWORK RULES IN SNOWFLAKE.NETWORK_SECURITY;
```

Note

The SHOW command doesn’t explicitly expose IP addresses, only the number of IP addresses per rule.

To see your current Snowflake-managed rules, *including* IP addresses, query the [NETWORK\_RULES view](/sql-reference/account-usage/network_rules) and filter on rows where the database is SNOWFLAKE and the schema is NETWORK\_SECURITY:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.NETWORK_RULES
  WHERE DATABASE = 'SNOWFLAKE' AND SCHEMA = 'NETWORK_SECURITY';
```

The following example shows how to create or replace a network policy that references a built-in network rule:

Copy code

```
CREATE OR REPLACE NETWORK POLICY example_network_policy ALLOWED_NETWORK_RULE_LIST = (
  'SNOWFLAKE.NETWORK_SECURITY.DBT_APAC_AWS',
  'SNOWFLAKE.NETWORK_SECURITY.DBT_EMEA_AWS'
);
```

The following example shows how to add a built-in network rule to an existing network policy by using the ALTER NETWORK POLICY syntax:

Copy code

```
ALTER NETWORK POLICY example_network_policy ADD ALLOWED_NETWORK_RULE_LIST = (
  'SNOWFLAKE.NETWORK_SECURITY.DBT_APAC_AWS'
);
```

### Snowflake-managed egress network rules

Snowflake provides the following pre-defined, Snowflake-managed egress network rule:

`SNOWFLAKE.EXTERNAL_ACCESS.PYPI_RULE`

> You can use an EGRESS network rule with an external access integration to provide a connection from Snowflake to Python Package Index (PyPI).
> For example, you might want to use the network rule to allow Notebook users on Container Runtime to install `pip` packages by using
> the `pip install` command.
>
> For examples of how to use this network rule, see
> [Accessing PyPI to install packages in Snowpark Container](/developer-guide/external-network-access/external-network-access-examples#label-creating-using-external-access-integration-accessing-pypi-container)
> and [External access integrations for repository access](/developer-guide/streamlit/app-development/dependency-management#label-sis-pypi-eai-setup).

Only users with the ACCOUNTADMIN role have access to the SNOWFLAKE.EXTERNAL\_ACCESS.PYPI\_RULE.
