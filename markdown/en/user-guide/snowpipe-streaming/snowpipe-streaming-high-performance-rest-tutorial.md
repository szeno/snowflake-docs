# Tutorial: Get started with Named Channels using the REST API

Note

Where possible, use the Snowpipe Streaming SDK instead of the REST API to benefit from automatic batching and simpler integration. Use direct REST when an SDK isn’t suitable for your environment.

This guide shows you how to stream data into Snowflake using the [Snowpipe Streaming REST API](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-api) and a JSON Web Token (JWT) generated with SnowSQL. It covers Named Channel REST ingestion for ordered, exactly-once workloads.

For the Elastic Channel REST path (simpler, recommended for most new applications), see [Tutorial: Get started with Elastic Channels (REST)](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-rest-getting-started).

## Prerequisites

Before you begin, ensure you have the following items:

**Snowflake User and Objects:**

A Snowflake user that is configured for key-pair authentication. Register your public key by using the following SQL command:

Copy code

```
ALTER USER MY_USER SET RSA_PUBLIC_KEY='<your-public-key>';
```

A Snowflake database, schema, and a target table for streaming ingestion. You can create them by using the following SQL commands and replacing placeholders like `MY_DATABASE`, `MY_SCHEMA`, `MY_TABLE` with the names that you want:

Copy code

```
-- Create Database and Schema
CREATE OR REPLACE DATABASE MY_DATABASE;
CREATE OR REPLACE SCHEMA MY_SCHEMA;

-- Create Target Table
CREATE OR REPLACE TABLE MY_TABLE (
    id NUMBER,
    c1 NUMBER,
    ts STRING
);
```

**ACCOUNT\_IDENTIFIER:**

We suggest that you use Format 1 for the ACCOUNT\_IDENTIFIER, which uses the account name within your organization; for example, `myorg-account123`. For more information on the format, see [Account identifiers](/user-guide/admin-account-identifier).

**Installed tools:**

- `curl`: For making HTTP requests.
- `jq`: For parsing JSON responses.
- `SnowSQL`: For running commands, Snowflake’s command-line client.

**Generated JWT:**

Generate your JWT by using SnowSQL:

Copy code

```
snowsql --private-key-path rsa_key.p8 --generate-jwt \
  -a <ACCOUNT_IDENTIFIER> \
  -u MY_USER
```

Caution

Store your JWT securely. Avoid exposing it in logs or scripts.

## Prerequisites and setup

The following steps configure the environment variables, ingest host, and sample rows required for Named Channel REST ingestion.

### Step 1: Set environment variables

Set up the necessary environment variables for your Snowflake account and the streaming operation. Note that the `PIPE` variable targets the default streaming pipe associated with your table.

Copy code

```
# Paste the JWT token obtained from SnowSQL
export JWT_TOKEN="PASTE_YOUR_JWT_TOKEN_HERE"

# Configure your Snowflake account and resources:
export ACCOUNT="<ACCOUNT_IDENTIFIER>" # For example, ab12345
export USER="MY_USER"
export DB="MY_DATABASE"
export SCHEMA="MY_SCHEMA"
export TABLE="MY_TABLE"

# Replace ACCOUNT with your Account URL Host to form the control plane host:
export CONTROL_HOST="${ACCOUNT}.snowflakecomputing.com"
```

### Step 2: Discover and configure the ingest host

Snowpipe Streaming REST uses two hostnames: the Snowflake account endpoint (`CONTROL_HOST`) and an account-specific ingest endpoint (`INGEST_HOST`) returned by `GET /v2/streaming/hostname`.

If you use AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect, set `CONTROL_HOST` to the hostname from the `privatelink-account-url` value returned by [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config). Don’t include `https://` or a trailing slash.

Important

If your Snowflake account name contains underscores (e.g., MY\_ACCOUNT), a known issue can cause an internal error when calling the ingestion service.

You must replace all underscores with dashes in the INGEST\_HOST before generating the scoped token. This converted format (with dashes) must be used for all subsequent REST API calls, including the generation of the scoped token itself.

For example, if the hostname returned is `my_account.region.ingest.snowflakecomputing.com`, you must change it to `my-account.region.ingest.snowflakecomputing.com` for all subsequent REST API calls.

The ingest host is the endpoint for streaming data. Discover the ingest host by using your JWT:

Copy code

```
export INGEST_HOST=$(curl -sS -X GET \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT" \
  "https://${CONTROL_HOST}/v2/streaming/hostname")

echo "Ingest Host: $INGEST_HOST"
```

#### Configure private DNS for the ingest host

If you use private connectivity, the returned ingest hostname must also resolve through your Snowflake private endpoint. The ingest hostname is separate from the Snowflake account hostname and might not appear in [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) or [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink).

Create a private DNS record for the exact normalized `INGEST_HOST` value and route it to the same existing Snowflake private endpoint used by your account hostname:

- On AWS, create a [Route 53 private hosted-zone](/user-guide/admin-security-privatelink) `CNAME` (or an appropriate alias) that targets the existing Snowflake VPC endpoint regional DNS name.
- On [Azure](/user-guide/privatelink-azure), resolve the ingest hostname to the existing Snowflake private endpoint IP address by using your private DNS configuration.
- On [Google Cloud](/user-guide/private-service-connect-google), resolve the ingest hostname to the existing Private Service Connect endpoint.

You don’t need to create a second Snowflake private endpoint for the ingest hostname.

Verify DNS and TLS from the same VM, container, pod, connector worker, or on-premises runtime that sends streaming requests. Keep `INGEST_HOST` as the request hostname for TLS Server Name Indication (SNI) and HTTP routing; don’t replace it with the private endpoint IP address or disable TLS verification.

Obtain a scoped token to authorize operations on the ingest host:

Copy code

```
export SCOPED_TOKEN=$(curl -sS -X POST "https://$CONTROL_HOST/oauth/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&scope=${INGEST_HOST}")

echo "Scoped Token obtained for ingest host"
```

### Step 3: Create sample rows

Create a batch in newline-delimited JSON (NDJSON) format:

Copy code

```
export NOW_TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

cat <<EOF > rows.ndjson
{"id":1,"c1":$RANDOM,"ts":"$NOW_TS"}
EOF
```

## Open and use a Named Channel

Use a Named Channel when you require ordering or exactly-once recovery. Complete Steps 1 through 3 in [Prerequisites and setup](#named-channel-rest-setup), then set the Named Channel variables:

Copy code

```
export PIPE="MY_TABLE-STREAMING"
export CHANNEL="MY_CHANNEL"
```

### Step 4: Open the Named Channel

Copy code

```
curl -sS -X PUT \
  -H "Authorization: Bearer $SCOPED_TOKEN" \
  -H "Content-Type: application/json" \
  "https://${INGEST_HOST}/v2/streaming/databases/$DB/schemas/$SCHEMA/pipes/$PIPE/channels/$CHANNEL" \
  -d '{"offset_token":"0"}' | tee open_resp.json | jq .
```

### Step 5: Append rows with offset and continuation tokens

Use the continuation token returned by the open operation and an application-managed source offset:

Copy code

```
export CONT_TOKEN=$(jq -r '.next_continuation_token' open_resp.json)
export OFFSET_TOKEN="1"

curl -sS -X POST \
  -H "Authorization: Bearer $SCOPED_TOKEN" \
  -H "Content-Type: application/x-ndjson" \
  "https://${INGEST_HOST}/v2/streaming/data/databases/$DB/schemas/$SCHEMA/pipes/$PIPE/channels/$CHANNEL/rows?continuationToken=$CONT_TOKEN&startOffsetToken=$OFFSET_TOKEN&endOffsetToken=$OFFSET_TOKEN" \
  --data-binary @rows.ndjson | tee append_resp.json | jq .
```

Use the `next_continuation_token` from each append response in the next append request.

### Step 6: Verify committed progress

Copy code

```
curl -sS -X POST \
  -H "Authorization: Bearer $SCOPED_TOKEN" \
  -H "Content-Type: application/json" \
  "https://${INGEST_HOST}/v2/streaming/databases/$DB/schemas/$SCHEMA/pipes/$PIPE:bulk-channel-status" \
  -d "{\"channel_names\":[\"$CHANNEL\"]}" | jq ".channel_statuses.\"$CHANNEL\""
```

Wait until `last_committed_offset_token` is `1` before advancing the source offset.

### Step 7: Verify the data

After `last_committed_offset_token` advances, query the target table:

Copy code

```
SELECT * FROM MY_DATABASE.MY_SCHEMA.MY_TABLE ORDER BY id;
```

### (Optional) Step 8: Clean up

Copy code

```
rm -f rows.ndjson open_resp.json append_resp.json
unset JWT_TOKEN SCOPED_TOKEN ACCOUNT USER DB SCHEMA TABLE PIPE CHANNEL CONTROL_HOST INGEST_HOST NOW_TS CONT_TOKEN OFFSET_TOKEN
```

## Troubleshooting

- **HTTP 401 (Unauthorized):** Verify that your JWT token is valid and not expired. If needed, regenerate it.
- **HTTP 404 (Not Found):** Double-check that the database, schema, table, or pipe names are spelled correctly and exist in your Snowflake account.
- **HTTP 429 (Too Many Requests):** Retry using exponential backoff with random variation in retry delays (jitter). Don’t assume a fixed reserved request rate.
- **No Ingest Host:** Ensure your control plane host URL is correct and accessible.

### Private connectivity troubleshooting

- **`CONTROL_HOST` doesn’t resolve:** Verify that you used `privatelink-account-url` and that the private DNS zone is linked or forwarded to the application runtime.
- **`Get Hostname` succeeds but `INGEST_HOST` doesn’t resolve:** Add the returned ingest hostname to private DNS and route it through the existing Snowflake private endpoint.
- **DNS works outside the connector but fails inside it:** Test from the connector container or managed runtime, and restart long-running workers after DNS changes if they cache negative DNS responses.
- **TLS hostname mismatch:** Keep the returned ingest hostname as the URL hostname. Don’t connect to the raw private endpoint IP address or rewrite the TLS SNI or HTTP `Host` header.
