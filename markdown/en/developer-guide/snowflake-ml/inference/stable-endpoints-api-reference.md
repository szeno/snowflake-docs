# Stable Endpoints & API Reference

This page provides the technical specifications for consuming your inference services externally and using the Snowflake Gateway to manage production model upgrades and high availability.

## Stable Endpoints with Snowflake Gateway

The standard SPCS ingress system has a tight coupling between a service and its hostname; when a service is recreated, the associated hostname is lost. The Snowflake Gateway resolves this by providing a permanent hostname allocated at creation that does not change for the lifetime of the gateway object.

### Key Capabilities

**Stable URL:** Maintain one permanent URL while pointing the gateway to different underlying services as your models evolve. Changes are typically reflected within one minute.

**Traffic Splitting:** Route requests to multiple endpoints based on assigned percentages, facilitating blue-green or canary deployments.

**Shadow Traffic:** Send production requests to a primary endpoint and mirror a percentage of them to challenger endpoints without returning challenger responses to clients.

[Preview Feature](/release-notes/preview-features) — Open

Shadow traffic gateways are available to all accounts.

**Automatic Failover:** Automatically redirect traffic from an unavailable or non-operational endpoint to other healthy targets.

### Gateway Failover Behavior

The gateway respects the relative percentage of specified healthy endpoints and will automatically trigger a failover if:

- A service is suspended (and auto\_resume is false) or its compute pool is suspended (until it comes back up).
- A service fails its readiness probe or is dropped entirely.
- The gateway owner loses USAGE or OWNERSHIP privileges on a target service endpoint.

Note

Traffic is never failed over to an endpoint with a 0% split or a shadow endpoint with a `weight` of 0. A target must have at least 1% traffic to be considered for failover.

## Managing Model Upgrades

### 1. Creating and Altering a Gateway

You can define how traffic is distributed between model versions using a YAML-based specification within a SQL command.

Copy code

```
-- Create a gateway to split traffic between V1 (90%) and V2 (10%)
CREATE OR REPLACE GATEWAY my_model_gateway
  FROM SPECIFICATION $$
    spec:
      type: traffic_split
      split_type: custom
      targets:
        - type: endpoint
          value: my_db.my_schema.model_v1_service!inference
          weight: 90
        - type: endpoint
          value: my_db.my_schema.model_v2_service!inference
          weight: 10
  $$;

-- Change the gateway to split traffic differently V1 (60%) and V2 (40%)
ALTER GATEWAY split_gateway
FROM SPECIFICATION $$
spec:
type: traffic_split
split_type: custom
targets:
- type: endpoint
value: my_db.my_schema.model_v1_service!inference
weight: 60
- type: endpoint
value: my_db.my_schema.model_v2_service!inference
weight: 40
$$;
```

**Rules for traffic split specifications:** `type` must be `traffic_split`, `split_type` must be `custom`, and all target weights must sum to exactly 100. By default, a gateway can route to a maximum of 5 endpoints.

To evaluate a challenger without using its responses in production, use a `shadow_traffic` gateway. The primary endpoint receives every request. Each shadow endpoint receives a copy of the percentage of requests specified by its `weight`.

Copy code

```
CREATE OR REPLACE GATEWAY my_model_shadow_gateway
  FROM SPECIFICATION $$
spec:
  type: shadow_traffic
  primary:
  - type: endpoint
    value: my_db.my_schema.model_v1_service!inference
  shadow:
  - type: endpoint
    value: my_db.my_schema.model_v2_service!inference
    weight: 10
$$;
```

**Rules for shadow traffic specifications:** `type` must be `shadow_traffic`. Specify exactly one primary endpoint with no `weight`, and at least one shadow endpoint with a `weight` from 0 through 100. Shadow weights don’t need to add up to 100.

### 2. Handling Schema Evolution

When a new model version (V2) requires different input features than V1, follow this strategy to avoid request disruptions:

1. **Superset Update:** Update your client application to send all the features required by both V1 and V2. Snowflake model serving implicitly ignores unnecessary features.
2. **Gradual Split:** Deploy V2 and use ALTER GATEWAY to slowly shift traffic percentages from V1 to V2.
3. **Client Cleanup:** Once 100% of traffic is routed to V2, update the client to remove the now-obsolete V1 features.

Important

Gateway routing with superset features is currently supported in dataframe\_records format; support for dataframe\_split is coming soon.

### 3. HTTP endpoint

Every gateway object comes with its endpoint name, which can be found by using following query:

Copy code

```
DESC GATEWAY split_gateway ->> select "ingress_url" as endpoint from $1
```

The endpoint of the gateway will be https://<endpoint>/. To call any particular methods to the model via gateway, use the method name as path to the URL (eg https://<endpoint>/<method-name> ). In a URL, underscores (\_) in the method name are replaced by dashes (-) in the URL. For example, the service name predict\_prob is changed to predict-proba in the URL.

For private link users, use privatelink\_ingress\_url instead of ingress\_url.

## Authorization & Security

### Accessing the Endpoint

**Authentication:** Using Programmatic Access Tokens (PAT) in the header is the simplest: `Authorization: Snowflake Token="your_pat_token"`. Gateway supports all the protocols Service Endpoint supports.

**The 404 Behavior:** For security, Snowflake returns a 404 Not Found for all authorization failures (e.g., incorrect token or lack of network route). There is currently no way to distinguish authentication errors from invalid URLs.

### Required Privileges

To manage or use a Gateway, the owner role requires:

- **Gateway Management:** CREATE GATEWAY in the schema and USAGE, MODIFY, or OWNERSHIP on the gateway object.
- **Endpoint Usage:** USAGE on the database, schema, and target service endpoints (specifically the ALL\_ENDPOINTS\_USAGE service role on the deployed service).
- **Public Access:** BIND SERVICE ENDPOINT on the account to expose the gateway to the public internet.

## Request & Response Protocols

Gateway supports the same data format as described in the Real-time inference page.

### Passing Supplemental Metadata

In some scenarios, you may need to pass supplemental data (such as record IDs or primary keys) that are not part of the model’s input signature but are required for downstream logging or joining with ground-truth labels. To handle this, Snowflake supports an optional extra\_columns top-level field.

When autocapture is enabled on the model service, values from declared extra columns are logged in the inference table under `snow.model_serving.request.extra_columns.<column>`. See [Autocapture inference logs](/developer-guide/snowflake-ml/inference/auto-capture-inference-logs).

#### Example

With dataframe\_split you include extra\_columns as a top-level field alongside the DataFrame payload:

Copy code

```
payload = {
    "dataframe_split": {
        "index": [0, 1],
        "columns": [
            "customer_id",
            "age",
            "monthly_spend",
            "primary_key",
        ],
        "data": [
            [101, 32, 85.5, "001"],
            [102, 45, 120.0, "002"],
        ]
    },
    "extra_columns": ["primary_key"]
}
```

or with dataframe\_records:

Copy code

```
payload = {
    "dataframe_records": [
        {
            "customer_id": 101,
            "age": 32,
            "monthly_spend": 85.5,
            "primary_key": "001",
        },
        {
            "customer_id": 102,
            "age": 45,
            "monthly_spend": 120.0,
            "primary_key": "002",
        },
    ],
    "extra_columns": ["primary_key"]
}
```

#### Guidelines for extra\_columns

**Optional:** You can omit extra\_columns entirely if you do not need it.

**No collisions:** The column names listed in extra\_columns must not collide with the columns that your model method expects as inputs. Keep model inputs and extra columns conceptually separate.

**Payload size limit:** The entire request payload (including extra\_columns and all data rows) is limited to 1 MB. If you exceed this limit:

- Reduce the batch size (fewer rows per request), or
- Remove or shorten extra columns that are not strictly necessary.
