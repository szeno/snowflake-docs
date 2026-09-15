# Query API reference

[Preview Feature — Open](/release-notes/preview-features)

Available to all accounts.

This page is the API reference for the Feature Store Query REST endpoint. For an
overview of the online feature store and getting started instructions, see
[Serving online features](/developer-guide/snowflake-ml/feature-store/online-feature-store).

## Endpoint

`POST <query_url>/api/v1/query`

Query features from a feature view or feature group. Always reads from the online
store (latest features).

Returns HTTP 200 on full success, HTTP 207 on partial success (at least one feature
has `TIME_OUT` or `MISSING_INPUT`). Features with `MISSING_DATA` are considered
normal and don’t trigger 207.

By default, the response includes only feature values for a minimal payload. Use
`metadata_options` to control which additional metadata is included (feature names,
types, freshness, serving status).

### Limits

- Maximum 10 entities per request

### Authentication

All requests require an `Authorization` header. You can use either a
[Programmatic Access Token (PAT)](/user-guide/programmatic-access-tokens)
or [key pair authentication](/user-guide/key-pair-auth).

For details, see
[Base URL and authentication](/developer-guide/snowflake-ml/feature-store/online-feature-store#label-online-fs-rest-auth).

## Request headers

| Header | Required | Description |
| --- | --- | --- |
| `Authorization` | Yes | `Snowflake Token="<pat>"` or `Bearer <jwt>` |
| `Content-Type` | Yes | Must be `application/json`. |
| `X-Request-ID` | No | Client-generated request ID for correlation. The server generates one if not provided. |

Expand

Show lessSee more

## Request body

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Name of the feature view or feature group. |
| `version` | Yes | Version of the feature view or feature group. |
| `object_type` | Yes | `feature_view` or `feature_group`. |
| `request_rows` | Yes | Array of objects, each with an `entity` map of join key names to values. Optionally include `request_context` for on-demand features. Maximum 10 entries. |
| `features` | No | List of feature names to return. If omitted, all features are returned. Only valid for `object_type=feature_view`, not for `feature_group`. |
| `metadata_options` | No | Controls which metadata fields are included in the response. See [Metadata options](#label-query-api-metadata-options). |
| `include_diagnostics` | No | When `true`, includes a `diagnostics` object in the response with server-side timing. Default: `false`. |

Expand

Show lessSee more

### Request row format

Each entry in `request_rows` has the following structure:

| Field | Required | Description |
| --- | --- | --- |
| `entity` | Yes | Map of join key names to values. |
| `request_context` | No | Request-time context for realtime feature views (for example, `current_amount`, `transaction_time`). |

Expand

Show lessSee more

### Metadata options

All flags default to `false`. Omit `metadata_options` entirely for minimal
(features-only) responses.

| Option | Description |
| --- | --- |
| `include_names` | Include feature `name` in metadata. For feature group queries, also includes `feature_view` and `feature_view_version` provenance. |
| `include_data_types` | Include feature `data_type` in metadata (`float64`, `int64`, `string`, `boolean`, `timestamp`). |
| `include_effective_times` | Include per-feature `effective_time` (freshness timestamp). `null` if no data exists for that feature. |
| `include_serving_status` | Include a `status` array in each result with per-feature serving status: `PRESENT`, `MISSING_DATA`, `MISSING_INPUT`, `TIME_OUT`. |

Expand

Show lessSee more

## Example requests

**Simple lookup:**

Copy code

```
{
  "name": "user_transaction_features",
  "version": "v1",
  "object_type": "feature_view",
  "request_rows": [
    { "entity": { "user_id": "user_123" } }
  ]
}
```

**Batch with feature selection:**

Copy code

```
{
  "name": "user_transaction_features",
  "version": "v1",
  "object_type": "feature_view",
  "request_rows": [
    { "entity": { "user_id": "user_123" } },
    { "entity": { "user_id": "user_456" } },
    { "entity": { "user_id": "user_789" } }
  ],
  "features": ["amount_sum_1h", "txn_count_24h"]
}
```

**Feature group with request context:**

Copy code

```
{
  "name": "fraud_detection_v3",
  "version": "v2",
  "object_type": "feature_group",
  "request_rows": [
    {
      "entity": { "user_id": "user_123", "merchant_id": "store_xyz" },
      "request_context": {
        "current_amount": 150.00,
        "transaction_time": "2024-01-15T10:30:00Z"
      }
    }
  ]
}
```

**All metadata options enabled:**

Copy code

```
{
  "name": "user_transaction_features",
  "version": "v1",
  "object_type": "feature_view",
  "metadata_options": {
    "include_names": true,
    "include_data_types": true,
    "include_effective_times": true,
    "include_serving_status": true
  },
  "include_diagnostics": true,
  "request_rows": [
    { "entity": { "user_id": "user_123" } }
  ]
}
```

## Response

The query endpoint returns a JSON object with the following fields.

### Response body

| Field | Type | Description |
| --- | --- | --- |
| `request_id` | String | Request ID for correlation. |
| `status` | String | `success` (HTTP 200) when all features resolved (`PRESENT` or `MISSING_DATA`). `partial_success` (HTTP 207) when at least one feature has `TIME_OUT` or `MISSING_INPUT`. |
| `results` | Array | One result per request row, in the same order. Each result contains a `features` array of values, and optionally a `status` array. |
| `metadata` | Object | Only present when `metadata_options` requests at least one metadata field. Contains a `features` array positionally aligned with `results[].features[]`. |
| `diagnostics` | Object | Server-side timing. Only present when `include_diagnostics` is `true`. |

Expand

Show lessSee more

**Result alignment:**

- `results[i]` corresponds to `request_rows[i]` (same order).
- `results[i].features[j]` corresponds to `metadata.features[j]` (when
  metadata is requested).
- `results[i].status[j]` corresponds to `results[i].features[j]` (when
  `include_serving_status` is `true`).

### Serving status values

| Status | Description |
| --- | --- |
| `PRESENT` | Feature value was found and returned. |
| `MISSING_DATA` | No data exists for this entity/feature combination. The feature value is `null`. This is normal and doesn’t trigger HTTP 207. |
| `MISSING_INPUT` | A required `request_context` field is missing. Triggers HTTP 207. |
| `TIME_OUT` | Feature computation timed out. Triggers HTTP 207. |

Expand

Show lessSee more

## Example responses

**Minimal production response (HTTP 200):**

Copy code

```
{
  "request_id": "req_query_456",
  "status": "success",
  "results": [
    { "features": [450.00, 12, 125.50] },
    { "features": [200.00, 5, 88.00] }
  ]
}
```

**With serving status:**

Copy code

```
{
  "request_id": "req_query_456",
  "status": "success",
  "results": [
    {
      "features": [450.00, 12, 125.50],
      "status": ["PRESENT", "PRESENT", "PRESENT"]
    },
    {
      "features": [null, null, null],
      "status": ["MISSING_DATA", "MISSING_DATA", "MISSING_DATA"]
    }
  ]
}
```

**With names, types, and freshness metadata:**

Copy code

```
{
  "request_id": "req_query_456",
  "status": "success",
  "results": [
    { "features": [450.00, 12, 125.50] },
    { "features": [200.00, 5, 88.00] }
  ],
  "metadata": {
    "features": [
      {
        "name": "amount_sum_1h",
        "data_type": "float64",
        "effective_time": "2024-01-15T10:29:55Z"
      },
      {
        "name": "txn_count_24h",
        "data_type": "int64",
        "effective_time": "2024-01-15T10:29:55Z"
      },
      {
        "name": "avg_amount_7d",
        "data_type": "float64",
        "effective_time": "2024-01-15T10:29:55Z"
      }
    ]
  }
}
```

**Feature group with provenance metadata:**

Copy code

```
{
  "request_id": "req_query_789",
  "status": "success",
  "results": [
    {
      "features": [450.00, 12, null, 0.85],
      "status": ["PRESENT", "PRESENT", "MISSING_DATA", "PRESENT"]
    }
  ],
  "metadata": {
    "features": [
      {
        "name": "amount_sum_1h",
        "feature_view": "user_transaction_features",
        "feature_view_version": "v1",
        "data_type": "float64",
        "effective_time": "2024-01-15T10:29:55Z"
      },
      {
        "name": "txn_count_24h",
        "feature_view": "user_transaction_features",
        "feature_view_version": "v1",
        "data_type": "int64",
        "effective_time": "2024-01-15T10:29:55Z"
      },
      {
        "name": "merchant_fraud_rate_7d",
        "feature_view": "merchant_risk_features",
        "feature_view_version": "v2",
        "data_type": "float64",
        "effective_time": null
      },
      {
        "name": "risk_score",
        "feature_view": "realtime_risk_features",
        "feature_view_version": "v1",
        "data_type": "float64",
        "effective_time": "2024-01-15T10:30:01Z"
      }
    ]
  }
}
```

**Partial success with timeout (HTTP 207):**

Copy code

```
{
  "request_id": "req_query_timeout",
  "status": "partial_success",
  "results": [
    {
      "features": [450.00, null],
      "status": ["PRESENT", "TIME_OUT"]
    }
  ]
}
```

## HTTP status codes

| Code | Description |
| --- | --- |
| `200` | All features resolved successfully (`PRESENT` or `MISSING_DATA`). |
| `207` | Partial success. At least one feature has `TIME_OUT` or `MISSING_INPUT`. The response body has the same schema as 200, with `status: partial_success`. |
| `400` | Invalid request: missing fields, invalid `object_type`, or `features` used with `feature_group`. |
| `401` | Authentication failed. |
| `403` | Caller lacks permission on this feature store. |
| `404` | Feature view or feature group not found. |
| `429` | Rate limit exceeded. Retry after the `Retry-After` header value. |
| `500` | Infrastructure failure where a structured response can’t be produced. |
| `503` | Service temporarily unavailable. Retry with exponential backoff. |

Expand

Show lessSee more
