# Ingest API reference

[Preview Feature — Open](/release-notes/preview-features)

Available to all accounts.

This page is the API reference for the Feature Store Ingest REST endpoint. For an
overview of the online feature store and getting started instructions, see
[Serving online features](/developer-guide/snowflake-ml/feature-store/online-feature-store).

## Endpoint

`POST <ingest_url>/api/v1/ingest`

Ingest records to one or more stream sources in a single request. Records are
validated, then fanned out to all consuming feature views (transformation, online
write, and offline write).

Each source is processed independently. Failure in one source doesn’t affect
processing of other sources in the same request.

Writes are UPSERT-based, so it’s safe to retry failed requests.

### Limits

- Maximum 2 stream sources per request
- Maximum 10 records per stream source

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
| `records` | Yes | A map of stream source name to an array of event records. Each record must match the schema registered for that stream source. Maximum 2 sources, 10 records per source. |
| `dry_run` | No | When `true`, validates records but doesn’t write them. Default: `false`. |
| `include_diagnostics` | No | When `true`, includes a `diagnostics` object in the response with server-side timing. Default: `false`. |

Expand

Show lessSee more

**Timestamps:** All timestamp values must be in ISO 8601 format (for example,
`2024-01-15T10:30:00Z`). Timezone offsets are accepted but converted to UTC for
storage and retrieval.

### Example request

Copy code

```
{
  "records": {
    "transactions_stream": [
      {
        "timestamp": "2024-01-15T10:30:00Z",
        "user_id": "user_123",
        "amount": 150.00,
        "merchant_category": "retail"
      },
      {
        "timestamp": "2024-01-15T10:31:00Z",
        "user_id": "user_456",
        "amount": 75.50,
        "merchant_category": "grocery"
      }
    ]
  }
}
```

**Multiple stream sources in one request:**

Copy code

```
{
  "records": {
    "transactions_stream": [
      {
        "timestamp": "2024-01-15T10:30:00Z",
        "user_id": "user_123",
        "amount": 150.00
      }
    ],
    "clickstream_events": [
      {
        "timestamp": "2024-01-15T10:30:01Z",
        "session_id": "sess_abc",
        "page": "/checkout",
        "duration_ms": 3200
      }
    ]
  }
}
```

**Dry run (validate only):**

Copy code

```
{
  "dry_run": true,
  "records": {
    "transactions_stream": [
      {
        "timestamp": "2024-01-15T10:30:00Z",
        "user_id": "user_123",
        "amount": 150.00
      }
    ]
  }
}
```

## Response

The ingest endpoint returns a JSON object with the following fields.

### Response body

| Field | Type | Description |
| --- | --- | --- |
| `request_id` | String | Request ID for correlation (from `X-Request-ID` header or server-generated). |
| `status` | String | `success` (HTTP 200) when all records are accepted and all feature views succeed. `partial_success` (HTTP 207) when at least one record is rejected or at least one feature view fails. |
| `sources` | Object | Results keyed by stream source name. |
| `diagnostics` | Object | Server-side timing. Only present when `include_diagnostics` is `true`. |

Expand

Show lessSee more

Each source result contains:

| Field | Type | Description |
| --- | --- | --- |
| `records.total` | Integer | Number of records received for this source. |
| `records.failed` | Integer | Number of records that failed validation. |
| `records.errors` | Array | Details for each rejected record. Omitted when `failed` is 0. Each entry has `index` (zero-based) and `error` with `code` and `message`. |
| `feature_views.failed` | Integer | Number of feature views that failed to persist. |
| `feature_views.results` | Array | One entry per consuming feature view, each with `name`, `version`, and `status` (`success` or `failed`). |

Expand

Show lessSee more

### Record error codes

| Code | Description |
| --- | --- |
| `MISSING_REQUIRED_FIELD` | Record is missing a required field (for example, the timestamp). |
| `INVALID_FIELD_TYPE` | A field value doesn’t match the expected type. |
| `INVALID_TIMESTAMP` | Timestamp value isn’t valid ISO 8601 format. |
| `RECORD_TOO_LARGE` | The record exceeds the maximum allowed size. |

Expand

Show lessSee more

### Feature view error codes

| Code | Description |
| --- | --- |
| `NOT_FOUND` | Feature view not found. |
| `FAILED_PRECONDITION` | Feature view isn’t in a valid state for writes. |
| `UNAVAILABLE` | The store is temporarily unavailable. |
| `UDF_EXECUTION_FAILED` | The transformation function failed. |
| `WRITE_ERROR` | Write to online or offline store failed. The `store` field indicates which store (`online` or `offline`). Check `retryable` to determine whether the client should retry. |
| `INTERNAL` | An internal server error occurred. |

Expand

Show lessSee more

### Example responses

**Full success (HTTP 200):**

Copy code

```
{
  "request_id": "req_abc123",
  "status": "success",
  "sources": {
    "transactions_stream": {
      "records": {
        "total": 10,
        "failed": 0
      },
      "feature_views": {
        "failed": 0,
        "results": [
          {
            "name": "user_transaction_features",
            "version": "v1",
            "status": "success"
          }
        ]
      }
    }
  }
}
```

**Partial success with record validation errors (HTTP 207):**

Copy code

```
{
  "request_id": "req_abc123",
  "status": "partial_success",
  "sources": {
    "transactions_stream": {
      "records": {
        "total": 10,
        "failed": 2,
        "errors": [
          {
            "index": 3,
            "error": {
              "code": "MISSING_REQUIRED_FIELD",
              "message": "Record is missing required field: timestamp"
            }
          },
          {
            "index": 7,
            "error": {
              "code": "INVALID_FIELD_TYPE",
              "message": "Field 'amount': expected number, got string"
            }
          }
        ]
      },
      "feature_views": {
        "failed": 0,
        "results": [
          {
            "name": "user_transaction_features",
            "version": "v1",
            "status": "success"
          }
        ]
      }
    }
  }
}
```

**Partial success with feature view failure (HTTP 207):**

Copy code

```
{
  "request_id": "req_abc123",
  "status": "partial_success",
  "sources": {
    "transactions_stream": {
      "records": {
        "total": 10,
        "failed": 0
      },
      "feature_views": {
        "failed": 1,
        "results": [
          {
            "name": "user_transaction_features",
            "version": "v1",
            "status": "success"
          },
          {
            "name": "fraud_detection_features",
            "version": "v1",
            "status": "failed",
            "error": {
              "code": "WRITE_ERROR",
              "message": "Offline store write timed out after 30s",
              "store": "offline",
              "retryable": true
            }
          }
        ]
      }
    }
  }
}
```

## HTTP status codes

| Code | Description |
| --- | --- |
| `200` | All records accepted and all feature views succeeded. |
| `207` | Partial success. At least one record was rejected or at least one feature view failed. The response body has the same schema as 200, with `status: partial_success`. |
| `400` | Invalid request: bad JSON, missing required fields, schema mismatch, or batch limits exceeded. |
| `401` | Authentication failed. |
| `403` | Caller lacks permission on this feature store. |
| `413` | Request body exceeds maximum allowed size. |
| `429` | Rate limit exceeded. Retry after the `Retry-After` header value. |
| `500` | Infrastructure failure where a structured response can’t be produced. |
| `503` | Service temporarily unavailable. Retry with exponential backoff. |

Expand

Show lessSee more
