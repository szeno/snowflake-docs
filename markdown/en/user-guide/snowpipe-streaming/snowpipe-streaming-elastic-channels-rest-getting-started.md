# Tutorial: Get started with Elastic Channels (REST API)

Note

We recommend starting with the [SDK getting-started guide](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-getting-started) to benefit from the improved throughput and simpler error handling the SDK provides. Use the REST API for lightweight workloads where the SDK is not suitable.

This tutorial shows how to stream data into Snowflake through the Snowpipe Streaming REST API using an Elastic Channel, cURL, and a JWT. The Elastic Channel REST path is the recommended starting point for new REST integrations because it does not require opening a channel or managing offset and continuation tokens.

For the Named Channel REST path (ordered, exactly-once ingestion), see [Tutorial: Get started with Snowpipe Streaming REST API](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-tutorial).

## Prerequisites

- A Snowflake user configured for key-pair authentication. Register your public key:

  Copy code

  ```
  ALTER USER MY_USER SET RSA_PUBLIC_KEY='<your-public-key>';
  ```

  For required privileges, see [Access control](/user-guide/snowpipe-streaming/snowpipe-streaming-access-control).
- A Snowflake database, schema, and target table:

  Copy code

  ```
  CREATE OR REPLACE DATABASE MY_DATABASE;
  CREATE OR REPLACE SCHEMA MY_SCHEMA;

  CREATE OR REPLACE TABLE MY_TABLE (
      id NUMBER,
      c1 NUMBER,
      ts STRING
  );
  ```
- `curl`, `jq`, and SnowSQL installed.
- Your Snowflake account identifier (Format 1: `myorg-account123`). For details, see [Account identifiers](/user-guide/admin-account-identifier).

## Step 1: Generate a JWT and set environment variables

Generate a JWT using SnowSQL:

Copy code

```
snowsql --private-key-path rsa_key.p8 --generate-jwt \
  -a <ACCOUNT_IDENTIFIER> \
  -u MY_USER
```

Caution

Store your JWT securely. Avoid exposing it in logs or shell history.

Set environment variables for the tutorial:

Copy code

```
export JWT_TOKEN="PASTE_YOUR_JWT_TOKEN_HERE"
export ACCOUNT="<ACCOUNT_IDENTIFIER>"   # for example, ab12345
export USER="MY_USER"
export DB="MY_DATABASE"
export SCHEMA="MY_SCHEMA"
export TABLE="MY_TABLE"
export CONTROL_HOST="${ACCOUNT}.snowflakecomputing.com"
```

## Step 2: Discover and configure the ingest host

Snowpipe Streaming REST uses two hostnames. The first is the Snowflake account endpoint (`CONTROL_HOST`). The second is an account-specific ingest endpoint (`INGEST_HOST`) returned by `GET /v2/streaming/hostname`.

If you use AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect, set `CONTROL_HOST` to the hostname from `privatelink-account-url` returned by [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config).

Important

If your Snowflake account name contains underscores, replace all underscores with dashes in the `INGEST_HOST` before generating the scoped token. Use the converted value (with dashes) for all subsequent API calls. For example, `my_account.region.ingest.snowflakecomputing.com` becomes `my-account.region.ingest.snowflakecomputing.com`.

Discover the ingest host:

Copy code

```
export INGEST_HOST=$(curl -sS -X GET \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT" \
  "https://${CONTROL_HOST}/v2/streaming/hostname")

echo "Ingest Host: $INGEST_HOST"
```

If you use private connectivity, create a private DNS record for `INGEST_HOST` that routes to your existing Snowflake private endpoint. You don’t need a second Snowflake private endpoint. For details, see the [private connectivity troubleshooting](#troubleshooting) section.

Obtain a scoped token for the ingest host:

Copy code

```
export SCOPED_TOKEN=$(curl -sS -X POST "https://$CONTROL_HOST/oauth/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&scope=${INGEST_HOST}")

echo "Scoped token obtained"
```

## Step 3: Create sample rows

Create a batch of rows in newline-delimited JSON (NDJSON) format. Include a stable event identifier (`id`) in each row so that you can deduplicate downstream if the request is retried.

Copy code

```
export NOW_TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
export REQUEST_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

cat <<EOF > rows.ndjson
{"id":1,"c1":$RANDOM,"ts":"$NOW_TS"}
{"id":2,"c1":$RANDOM,"ts":"$NOW_TS"}
EOF
```

`id` is a stable event identifier for deduplication. `REQUEST_ID` is a UUID you will use to track the request, and reuse on retries of the same rowset (batch of rows).

## Step 4: Append rows to the Elastic Channel

Send the rows to the table endpoint, which is available only for Elastic Channels. On the first request, Snowflake creates or resolves the managed default pipe. Every streaming pipe includes an implicit `ELASTIC` channel; the request uses it without a separate open-channel operation.

Copy code

```
curl -sS -X POST \
  -H "Authorization: Bearer $SCOPED_TOKEN" \
  -H "Content-Type: application/x-ndjson" \
  "https://${INGEST_HOST}/v2/streaming/data/databases/$DB/schemas/$SCHEMA/tables/$TABLE/rows?requestId=${REQUEST_ID}&retryCount=0" \
  --data-binary @rows.ndjson | jq .
```

A successful HTTP 200 response is the **durable acknowledgement**: Snowflake has durably buffered the request payload. It does not mean the rows are immediately queryable.

Important

Elastic delivery is at least once. If the request returns an ambiguous response (network timeout, no response, or a server-side 5xx) and you retry, Snowflake may already have accepted the original request. Pass the **same `requestId`** on every retry of the same rowset to enable server-side correlation for support. The `retryCount` query parameter helps Snowflake identify retries: set it to `0` on the first attempt and increment it on each retry. A `retryCount` greater than `0` signals that duplicates are possible. Add a stable event identifier to your payload and reconcile or deduplicate downstream when duplicates matter.

Alternatively, you can use the pipe endpoint for a custom PIPE:

Copy code

```
export PIPE="MY_TABLE-STREAMING"

curl -sS -X POST \
  -H "Authorization: Bearer $SCOPED_TOKEN" \
  -H "Content-Type: application/x-ndjson" \
  "https://${INGEST_HOST}/v2/streaming/data/databases/$DB/schemas/$SCHEMA/pipes/$PIPE/channels/ELASTIC/rows?requestId=${REQUEST_ID}&retryCount=0" \
  --data-binary @rows.ndjson | jq .
```

Note

Direct REST clients own batching and compression, unlike SDK users whose appends are combined internally. For production REST requests, build bounded NDJSON batches and send partial batches after an elapsed-time threshold. Use ZSTD or Gzip compression: add `Content-Encoding: zstd` or `Content-Encoding: gzip` only when the payload is compressed in the matching format. Each Elastic request can contain up to 4 MB of payload data (the payload size sent over the network, after compression if used).

## Step 5: Verify the data

Allow a few seconds for Snowflake to process and materialize the data, then query the target table:

Copy code

```
SELECT * FROM MY_DATABASE.MY_SCHEMA.MY_TABLE;
```

If rows are acknowledged but not visible in the target table, check the error table:

Copy code

```
SELECT * FROM MY_DATABASE.MY_SCHEMA.MY_TABLE__ERRORS LIMIT 20;
```

For more information on error tables, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

## Step 6: Clean up (optional)

Copy code

```
rm -f rows.ndjson
unset JWT_TOKEN SCOPED_TOKEN ACCOUNT USER DB SCHEMA TABLE CONTROL_HOST INGEST_HOST NOW_TS REQUEST_ID PIPE
```

## Troubleshooting

- **HTTP 401 (Unauthorized):** Verify that your JWT is valid and not expired. Regenerate if needed.
- **HTTP 404 (Not Found):** Verify that the database, schema, and table names are correct and exist in your Snowflake account.
- **HTTP 429 (Too Many Requests):** Retry using exponential backoff with random variation in retry delays (jitter). Don’t assume a fixed reserved request rate.
- **No rows in target table after acknowledgement:** Allow time for materialization, then check the error table.

### Private connectivity troubleshooting

- **`CONTROL_HOST` doesn’t resolve:** Verify that you used `privatelink-account-url` and that the private DNS zone is linked to the application runtime.
- **`Get Hostname` succeeds but `INGEST_HOST` doesn’t resolve:** Add the returned ingest hostname to private DNS and route it through the existing Snowflake private endpoint.
- **DNS works outside the connector but fails inside it:** Test from the connector container or runtime, and restart long-running workers after DNS changes if they cache negative DNS responses.
- **TLS hostname mismatch:** Keep the returned ingest hostname as the URL hostname. Don’t connect to the raw private endpoint IP address or rewrite the TLS SNI or HTTP `Host` header.

## Next steps

- [Best practices](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices): Batching, compression, stable event IDs, and graceful shutdown.
- [Error handling](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-error-handling): Retries, duplicate risk, and request ID correlation.
- [REST API reference](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-api#elastic-channel-rest-api): Full Elastic endpoint specifications.
- [Limitations](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-limitations): Request size, delivery guarantees, and SDK version requirements.
