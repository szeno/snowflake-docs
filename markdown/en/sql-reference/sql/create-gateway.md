# CREATE GATEWAY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Creates a new [gateway](/developer-guide/snowpark-container-services/gateway)
in the current schema. A gateway enables traffic splitting or shadow traffic across multiple service endpoints.

See also:
:   [ALTER GATEWAY](/sql-reference/sql/alter-gateway) , [DESCRIBE GATEWAY](/sql-reference/sql/desc-gateway), [DROP GATEWAY](/sql-reference/sql/drop-gateway) , [SHOW GATEWAYS](/sql-reference/sql/show-gateways)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] GATEWAY [ IF NOT EXISTS ] <name>
  FROM SPECIFICATION <specification_text>
```

## Required parameters

`name`
:   String that specifies the identifier for the gateway; it must be unique for the schema in which the gateway is created.

`FROM SPECIFICATION`
:   Specifies the gateway specification inline. The specification defines a traffic split or shadow traffic configuration.

    For a traffic split gateway, the specification uses the following format:

    Copy code

    ```
    spec:
      type: traffic_split
      split_type: custom
      targets:
      - type: endpoint
        value: <db>.<schema>.<service>!<endpoint>
        weight: <weight>
      - type: endpoint
        value: <db>.<schema>.<service>!<endpoint>
        weight: <weight>
    ```

    For a shadow traffic gateway, the specification uses the following format:

    [Preview Feature](/release-notes/preview-features) — Open

    Shadow traffic gateways are available to all accounts.

    Copy code

    ```
    spec:
      type: shadow_traffic
      primary:
      - type: endpoint
        value: <db>.<schema>.<service>!<endpoint>
      shadow:
      - type: endpoint
        value: <db>.<schema>.<service>!<endpoint>
        weight: <weight>
    ```

## Specification parameters

`type`
:   The gateway configuration type. Supported values:

    - `traffic_split`: Routes requests among target endpoints according to their weights.
    - `shadow_traffic`: Routes all requests to one primary endpoint and mirrors a percentage of requests to one or more shadow endpoints.

`split_type`
:   For a `traffic_split` gateway, the fixed value `custom`.

    Don’t specify this parameter for a `shadow_traffic` gateway.

`targets`
:   For a `traffic_split` gateway, a list of target endpoints to route traffic to. Each target must specify:

    `type`
    :   Fixed value. Must be set to `endpoint`.

    `value`
    :   The fully qualified endpoint name in the format `db.schema.service!endpoint`. Each target endpoint must exist.

    `weight`
    :   The traffic weight for this endpoint, specified as an integer. All weights must add up to 100.

`primary`
:   For a `shadow_traffic` gateway, a list containing exactly one primary endpoint. The primary endpoint receives all requests and returns responses to clients.

    Don’t specify `weight` for the primary endpoint.

`shadow`
:   For a `shadow_traffic` gateway, a list of one or more shadow endpoints. Each shadow endpoint receives a copy of the percentage of requests specified by `weight`. Responses from shadow endpoints aren’t returned to clients.

    Each shadow target uses the same `type` and `value` fields as a traffic split target. Set `weight` to an integer from 0 through 100. Weights for multiple shadow targets don’t need to add up to 100.

Note

- Maximum number of endpoints per gateway is 5 by default.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE GATEWAY | Schema | Required to create a gateway in the schema. |
| BIND SERVICE ENDPOINT | Account | Required to bind service endpoints to the gateway. |
| USAGE | Database | Required on the database containing the gateway. |
| USAGE | Schema | Required on the schema containing the gateway. |
| USAGE | Service endpoints | Required on the target service endpoints. Grant the service role `ALL_ENDPOINTS_USAGE` to provide access. |

Expand

Show lessSee more

To grant the required privileges, use the following commands:

Copy code

```
-- Grant CREATE GATEWAY privilege in the schema
GRANT CREATE GATEWAY ON SCHEMA <schema_name> TO ROLE <role_name>;

-- Grant BIND SERVICE ENDPOINT privilege on the account
GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE <role_name>;

-- Grant USAGE on target endpoints via service role
GRANT SERVICE ROLE <db_name>.<schema_name>.<service_name>!ALL_ENDPOINTS_USAGE TO ROLE <role_name>;
```

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a gateway that splits traffic between two service endpoints:

Copy code

```
CREATE GATEWAY split_gateway
  FROM SPECIFICATION $$
spec:
  type: traffic_split
  split_type: custom
  targets:
  - type: endpoint
    value: db.schema.s2!ep1
    weight: 60
  - type: endpoint
    value: db.schema.s1!ep1
    weight: 40
$$;
```

Create or replace a gateway with a new traffic split configuration:

Copy code

```
CREATE OR REPLACE GATEWAY split_gateway
  FROM SPECIFICATION $$
spec:
  type: traffic_split
  split_type: custom
  targets:
  - type: endpoint
    value: db.schema.service1!endpoint1
    weight: 70
  - type: endpoint
    value: db.schema.service2!endpoint1
    weight: 30
$$;
```

Create a shadow traffic gateway that sends all requests to a primary endpoint and mirrors 10 percent of the requests to a shadow endpoint:

Copy code

```
CREATE GATEWAY shadow_gateway
  FROM SPECIFICATION $$
spec:
  type: shadow_traffic
  primary:
  - type: endpoint
    value: db.schema.production_service!inference
  shadow:
  - type: endpoint
    value: db.schema.challenger_service!inference
    weight: 10
$$;
```
