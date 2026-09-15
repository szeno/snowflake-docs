# Run the Snowpipe Streaming SDK in Snowpark Container Services

Beginning with SDK version 1.5.0, you can run the Snowpipe Streaming SDK inside [Snowpark Container Services (SPCS)](/developer-guide/snowpark-container-services/overview). The SDK authenticates by using the workload-identity token that the SPCS runtime mounts into your container, so you don’t store private keys, OAuth client secrets, or PATs in the container image.

This support applies to the Java, Python, and Node.js SDKs.

## Prerequisites

- A Snowflake account with Snowpark Container Services available. For setup details, see [Common setup](/developer-guide/snowpark-container-services/common-setup).
- A target table, role, and PIPE object in your Snowflake account. For setup details, see [Tutorial: Get started with Snowpipe Streaming high-performance architecture SDK](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-getting-started).
- Snowpipe Streaming SDK version 1.5.0 or later for the language you use.

## Authenticate with the SPCS workload-identity token

When the SDK runs inside an SPCS service, the SPCS runtime makes a short-lived workload-identity bearer token available at `/snowflake/session/token`. The platform rotates this token automatically. The SDK reads the token from the file, performs the standard scoped token exchange with Snowflake, and refreshes the token in the background.

To use SPCS authentication, set the following client-side properties:

| Property | Description |
| --- | --- |
| `authorization_type` | Set to `SPCS` to enable workload-identity authentication. Requires SDK version 1.5.0 or later. |
| `spcs_token_path` | File path to the SPCS workload-identity bearer token. Defaults to `/snowflake/session/token`. Override only if you have a non-standard SPCS deployment. |

Expand

Show lessSee more

The standard `url`, `account`, and `role` properties remain required. The `user`, `private_key`, and OAuth properties aren’t used when `authorization_type` is set to `SPCS`.

You can override the token path with the `SNOWFLAKE_SPCS_TOKEN_PATH` environment variable for non-standard deployments. The environment variable takes precedence over the `spcs_token_path` property.

### Example: client-side configuration

The following example shows a `profile.json` file that runs the SDK in SPCS:

Copy code

```
{
  "authorization_type": "SPCS",
  "url": "https://<account_identifier>.snowflakecomputing.com",
  "account": "XY12345",
  "role": "MY_INGEST_ROLE",
  "spcs_token_path": "/snowflake/session/token"
}
```

## Build a container image

Bundle the SDK into your container image alongside your application code. The following examples show minimal Dockerfile snippets for each language. Adapt them to your existing image and base layer.

PythonNode.js

Copy code

```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt   # includes snowpipe-streaming>=1.5.0

COPY app.py /app/
COPY profile.json /app/

ENTRYPOINT ["python", "/app/app.py"]
```

Copy code

```
FROM node:20-slim

WORKDIR /app

COPY package*.json /app/
RUN npm ci   # package.json declares snowpipe-streaming@^1.5.0

COPY index.js /app/
COPY profile.json /app/

ENTRYPOINT ["node", "/app/index.js"]
```

Push the image to your Snowflake image repository. For instructions, see [Working with an image registry and repository](/developer-guide/snowpark-container-services/working-with-registry-repository).

## Define the SPCS service

Define an SPCS service that runs the container and grants the service role permissions to ingest data into your target pipe. To make the SPCS workload-identity token available to the SDK, set `capabilities.securityContext.enableCustomCredentials` to `true` in the service specification.

Copy code

```
spec:
  containers:
    - name: streaming-app
      image: /<db>/<schema>/<repo>/streaming-app:latest
  endpoints:
    - name: app
      port: 8080
      public: false
capabilities:
  securityContext:
    enableCustomCredentials: true
```

For a full walkthrough of creating a service, granting roles, and managing the lifecycle, see [Snowpark Container Services: Working with services](/developer-guide/snowpark-container-services/working-with-services).

## Token rotation

The SPCS platform rotates the workload-identity token periodically. The SDK rereads the token file in the background; your application code doesn’t need to handle rotation explicitly. The SDK invalidates internal HTTP connections when the token is refreshed.

If the token file is removed or becomes unreadable while the SDK is running, the SDK surfaces an authentication error on the next ingest call. Treat this as a non-retryable error and recreate the client.

## Limitations

- The SDK reads its workload-identity token from the local filesystem inside the SPCS container. Authentication isn’t supported by passing a bearer token in code; use the file-based path.
- Network egress from your SPCS service to Snowflake must be permitted by your SPCS configuration. For details, see [Network egress](/developer-guide/snowpark-container-services/additional-considerations-services-jobs#egress-traffic).
