# Autocapture inference logs for realtime inference

Use Auto Capture in Snowflake ML to automatically log every request and response processed by a model service. Auto Capture provides immediate visibility into the request successes, request failures, and the inputs behind unexpected predictions.

Instead of piping request or response data into a table or view, you can automatically persist inference request and response data. Instead of needing to correctly create pipelines for data ingestion and monitoring, you can use Auto Capture.

With Auto Capture, you can do the following:

- **Rapidly debug**: Analyze historical inference data to diagnose edge cases and understand model behavior.
- **Continuously improve your models**: Use real-world production data to create high-quality datasets to train new models.
- **Test**: Use the data collected from the logs for A/B testing and shadow testing.

For each inference request, Auto Capture logs the following:

- Request payload
- Response payload
- Model version identifier
- Service identifier
- Gateway routing metadata
- Request/response timestamps
- Response code (such as 200).

Note

Snowflake doesn’t capture data for the inputs and outputs using the vLLM inference engine.

This data is read-only and cannot be modified by users.

Snowflake only captures response data for successful requests. If a request fails, Snowflake doesn’t capture any data.

## Prerequisites and model version compatibility

The following sections describe the prerequisites and model version compatibility for Auto Capture.

### Access control requirements

To configure and access captured inference data, your role must have the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Model | Required to create a service with autocapture enabled and to read inference table data using the INFERENCE\_TABLE function. OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). In a managed access schema, only the schema owner (for example, the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| OWNERSHIP | Service | Required to list whether a service has autocapture enabled in the list\_service() function. OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). In a managed access schema, only the schema owner (for example, the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| USAGE | Model, Service, Version, Gateway | Required to resolve entities in the INFERENCE\_TABLE function. |

Expand

Show lessSee more

### Model version compatibility

Each model exists as a model object. The model object has its own inference table, which contains the data and metadata for each inference request. Auto Capture logs the data from the model’s inference table. Each model service has its own inference table.

If you’re creating a new model, Auto Capture is automatically enabled.

Models created before January 23, 2026, don’t support Auto Capture. You must clone the model and enable Auto Capture for its service.

Use the following command to duplicate an existing model:

Copy code

```
CREATE [ OR REPLACE ] MODEL [ IF NOT EXISTS ] <name> [ WITH VERSION <version_name> ]
FROM MODEL <source_model_name> [ VERSION <source_version_or_alias_name> ]
```

The model created with the preceding command has an empty inference table. For information about enabling autocapture, see [Activate Auto Capture](#label-autocapture-activate).

You can also create a model version from an existing model version. For more information, see [Variant Syntax](/sql-reference/sql/create-model#label-create-model-variant-syntax).

After duplicating the model, you can enable autocapture by following the steps in [Activate Auto Capture](#label-autocapture-activate).

## Activate Auto Capture

After you’ve created a new model or cloned an existing model, enable Auto Capture for the model service using the Python SDK. For more information about the model service, see [Deploy models for real-time inference (REST API)](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api).

Use the following Python code to enable Auto Capture:

Copy code

```
mv.create_service(
    service_name="my_service",
    service_compute_pool="my_compute_pool",
    autocapture=True
)
```

The `mv` variable is the model version object. You defined it when you logged the model to the model registry.

The default value for autocapture is `False`. Make sure you’re enabling autocapture for a model that you’ve created after January 23, 2026 and logged to the model registry. Otherwise, the service creation fails because the model doesn’t have an inference table.

Important

The autocapture setting is immutable. You can’t enable or disable auto-capture on an existing model service. You must recreate the service to change this configuration. If you recreate the service, the endpoint changes unless you use a stable endpoint or gateway.

## Query inference data

To access your logs, use the INFERENCE\_TABLE function. This function returns inference logs for a model and supports filtering by version, service, and gateway. Only model owners are able to see the data when they have USAGE privileges on the gateway and service.

### Basic example

The following example demonstrates how to retrieve all inference logs for a model using the INFERENCE\_TABLE function. This query returns all captured request and response data for every inference request processed by the model’s services.

Copy code

```
-- Fetch all inference logs for a specific model
SELECT * FROM TABLE(INFERENCE_TABLE('my_model'));
```

### Advanced filtering example

You can filter by specific versions, services, or gateways directly within the INFERENCE\_TABLE() function:

Copy code

```
SELECT * FROM TABLE(
  INFERENCE_TABLE(
    'MY_MODEL',
    MODEL_VERSION => 'V1',
    SERVICE => 'MY_PREDICTION_SERVICE',
    GATEWAY => 'MY_GATEWAY'
  )
);
```

Important

The service, version, and gateway arguments must exist at the time of the query. If created a new service, version, or gateway with the same name as one that had existed previously, the query only produces data from the current version.

You can use the following predicate clause to filter by function name:

Copy code

```
WHERE RECORD_ATTRIBUTES:"snow.model_serving.function.name" = 'predict'
```

Note

For best performance, filter for a time range on the TIMESTAMP column.

### Passing supplemental metadata with extra\_columns

When autocapture is enabled, pass supplemental metadata (such as record IDs or primary keys) using a top-level `extra_columns` list in the REST request body. This field is supported only with the `dataframe_split` and `dataframe_records` payload formats.

List column names in `extra_columns` and include the corresponding values in each row of the dataframe payload. These columns are not sent to the model but are captured in the inference log under `snow.model_serving.request.extra_columns.<column>` in `RECORD_ATTRIBUTES`.

Example request body:

Copy code

```
payload = {
    "dataframe_records": [
        {"feature_a": 1.0, "request_id": "abc-123"}
    ],
    "extra_columns": ["request_id"]
}
```

Query captured extra columns:

Copy code

```
SELECT
  RECORD_ATTRIBUTES:"snow.model_serving.request.extra_columns.request_id"::VARCHAR AS request_id
FROM TABLE(INFERENCE_TABLE('my_model'));
```

For full payload examples and guidelines, see [Stable Endpoints & API Reference](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference).

### Querying historical data for deleted entities

The inference data is retained after you delete a service, version, or gateway. You can still query this historical data so long as the model still exists.

The following example returns all inference logs for a model:

Copy code

```
SELECT *
FROM TABLE(
  INFERENCE_TABLE('my_model')
);
```

The following example filters inference logs by model version:

Copy code

```
SELECT *
FROM TABLE(
  INFERENCE_TABLE(
    'my_model',
    MODEL_VERSION => 'v1'
  )
);
```

The following example filters inference logs by version and service:

Copy code

```
SELECT *
FROM TABLE(
  INFERENCE_TABLE(
    'my_model',
    MODEL_VERSION => 'v1',
    SERVICE => 'my_service'
  )
);
```

The following example filters inference logs by version and gateway:

Copy code

```
SELECT *
FROM TABLE(
  INFERENCE_TABLE(
    'my_model',
    MODEL_VERSION => 'v1',
    GATEWAY => 'my_gateway'
  )
);
```

## Data schema and metadata

Snowflake only captures response data for successful requests. If a request fails, Snowflake doesn’t capture any data.

The following are the record attributes that are captured:

| Field | Description |
| --- | --- |
| `snow.model_serving.request.data.<column>` | The input features sent to the model. |
| `snow.model_serving.request.extra_columns.<column>` | Supplemental metadata from the REST `extra_columns` field. Only captured for `dataframe_split` and `dataframe_records` requests. |
| `snow.model_serving.response.data.<column>` | The inference output returned by the model. |
| `snow.model_serving.request.timestamp` | When the request hit the inference service. |
| `snow.model_serving.response.code` | HTTP status (such as 200 for success and 5xx for errors). |
| `snow.model_serving.truncation_policy` | Indicates if data exceeded size limits (NONE or TRUNCATED\_DEFAULT). For more information, see [Data truncation logic](#label-autocapture-truncation). |
| `snow.model_serving.last_hop_id` | Reflects the last gateway id from where the request landed to the inference service. |
| `snow.model_serving.hop_ids` | Reflects the list of gateway ids, depicting the path of traversal. Currently limited to only one gateway. |

Expand

Show lessSee more

## Data truncation logic

To maintain system performance, there’s a 1 MB limit for each inference event. If the request and response reaches the limit, Snowflake applies a multi-stage truncation process to preserve as much utility as possible.

The following table shows the truncation process:

| Stage | Trigger | Action taken |
| --- | --- | --- |
| 1: Soft Reduction | > 700 KB | Raw bytes removed; Strings > 2 KB truncated; JSON objects replaced with a `TRUNCATED` status. |
| 2: Aggressive | > 900 KB | All strings further truncated to 256 bytes. |
| 3: Removal | > 900 KB\* | If still over limit, the payload is dropped and replaced with a minimal metadata skeleton. |

Expand

Show lessSee more

\*Stage 3 occurs if metadata alone exceeds the threshold after content reduction.

## Limits

Keep in mind the following limitations and considerations when using auto capture:

- **LLM Support**: Auto capture isn’t supported for Large Language Models (LLMs).
- **Throughput**: Auto capture is designed for a system throughput of approximately 300-400 requests per second (or 10MB/s) per service.
- **Replication**: You can’t replicate inference tables. Replicated models will have no inference tables in the target account.
- **Retention**: Inference data persists even if the Service or Gateway is deleted.
- **Warning**: Deleting the Model object will permanently delete all associated inference data.
- **Ground Truth**: To perform drift analysis, pass join keys in `extra_columns` on REST requests and join the INFERENCE\_TABLE output to a ground truth table on those captured values.
- **Consumer Accounts**: Consumer accounts can’t create a service with autocapture enabled for shared models with inference tables.
- **Performance**: Autocapture is designed to not add latency to inference requests. However, it may drop some captures during periods of extremely high request volume.

## Schema

As part of this feature, the following values are added to the respective columns.

### RESOURCE\_ATTRIBUTES

The following table describes the resource attribute schema fields:

| Field | Description |
| --- | --- |
| `snow.model.version.id` | Unique identifier for the model version. |
| `snow.model.version.name` | Name of the model version. |

Expand

Show lessSee more

### RECORD\_ATTRIBUTES

The following table describes the record attribute schema fields:

| Field | Description |
| --- | --- |
| `snow.model_serving.function.name` | Name of the model function that was called. |
| `snow.model_serving.last_hop_id` | The ID of the last gateway that processed the request. |
| `snow.model_serving.hop_ids` | List of gateway IDs that processed the request. |
| `snow.model_serving.request.data.<column>` | Input fields where `<column>` represents specific input field names. |
| `snow.model_serving.request.extra_columns.<column>` | Supplemental metadata from the REST `extra_columns` field. Only captured for `dataframe_split` and `dataframe_records` requests. |
| `snow.model_serving.request.timestamp` | Timestamp of when the request was captured by the inference service. |
| `snow.model_serving.response.data.<column>` | Response data where `<column>` contains the inference response fields. |
| `snow.model_serving.response.timestamp` | Timestamp of when the response was captured by the service. |
| `snow.model_serving.response.code` | Response code from the inference service (for example, 200, 5xx). |
| `snow.model_serving.truncation_policy` | Indicates whether data was truncated. Values are `NONE` or `TRUNCATED_DEFAULT`. |

Expand

Show lessSee more
