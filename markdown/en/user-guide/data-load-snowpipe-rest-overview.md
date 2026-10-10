# Load data with the Snowpipe REST API

With the Snowpipe REST API, your application tells a pipe which staged files to load. Your application stages the files, and then sends their paths in an HTTPS request to the pipe’s `insertFiles` endpoint. Snowpipe queues the files and loads them into the target table with the pipe’s `COPY INTO` statement, on Snowflake-managed compute. You don’t need a warehouse, a session, or event notifications from your cloud storage service.

You can call the REST API from any language or tool that can send HTTPS requests and either sign a JSON Web Token (JWT) for key pair authentication or get a token for workload identity federation. Snowflake also provides the Snowflake Ingest SDKs for Java and Python, which build the requests and generate the JWT for you.

For example, the following request asks the `orders_pipe` pipe to load one file from its stage. The `JWT` variable holds a token that authenticates the request, as described in [Authentication and access control](#label-snowpipe-rest-authentication):

Copy code

```
curl --request POST \
  "https://myorg-myaccount.snowflakecomputing.com/v1/data/pipes/MYDB.MYSCHEMA.ORDERS_PIPE/insertFiles?requestId=$(uuidgen)" \
  --header "Authorization: Bearer ${JWT}" \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  --data '{"files": [{"path": "2026/10/03/orders_0001.json.gz"}]}'
```

A `200` response means that Snowpipe queued the file. It doesn’t mean that the file loaded. To find out whether the file loaded, call the `insertReport` endpoint or query the copy history, as described in [Check load results](#label-snowpipe-rest-check-results).

## Choose between the REST API and automated loading

Snowpipe learns about new files in one of two ways: from event notifications that your cloud storage service sends (automated loading), or from calls that your application makes to the REST API. [Automated loading](/user-guide/data-load-snowpipe-auto) doesn’t require you to write or run any code, so it’s usually the better choice when your files land in Amazon S3, Google Cloud Storage, or Microsoft Azure storage and you can configure event notifications for the storage location.

The REST API is a better fit when:

- **Your storage can’t send event notifications to Snowflake.** For example, your files are in [S3-compatible storage](/user-guide/data-load-s3-compatible-storage), or you can’t change the notification settings of the bucket.
- **Your files are in an internal stage.** [Automated loading from internal stages](/sql-reference/sql/create-pipe#optional-parameters) is in preview and is available only for accounts hosted on AWS. With the REST API, you can load from named internal stages and table stages on any cloud platform.
- **Your application decides when files are ready.** For example, your application writes each file in several steps, or validates a batch of files first. With the REST API, Snowpipe loads only the files that your application submits, when it submits them. With automated loading, Snowpipe loads each file as soon as the storage service reports it.

If your application produces rows or events rather than files, use [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) instead. It loads rows directly, without staging files, and with lower latency.

The following table compares the two ways to start Snowpipe loads:

| Characteristic | Automated loading | Snowpipe REST API |
| --- | --- | --- |
| How Snowpipe learns about new files | Your cloud storage service sends an event notification when a file arrives | Your application calls the `insertFiles` endpoint with a list of files |
| Supported stages | External stages on Amazon S3, Google Cloud Storage, and Microsoft Azure; [internal stages in preview](/sql-reference/sql/create-pipe#optional-parameters), on AWS only | Named internal stages, table stages, and external stages, including S3-compatible storage |
| What you set up | Event notifications in your cloud provider and, for Google Cloud Storage and Microsoft Azure, a notification integration | A Snowflake user with key pair authentication or workload identity federation, and an application that stages files, calls the API, and checks the results |
| Pipe definition | `AUTO_INGEST = TRUE` | No extra properties; `AUTO_INGEST` defaults to `FALSE` |

Expand

Show lessSee more

## REST API workflow

When your application uses the REST API, a file goes through the following steps:

1. **Your application stages the file.** For an internal stage, it uploads the file with the [PUT](/sql-reference/sql/put) command. For an external stage, it writes the file with your cloud provider’s tools or APIs.
2. **Your application submits the file.** It sends the file’s path to the pipe’s `insertFiles` endpoint. The path is relative to the location in the pipe’s `COPY INTO` statement. If that statement names only the stage, the path is relative to the root of the stage, which is the stage URL for an external stage. If the statement includes a path, such as `@orders_stage/2026/`, the path in the request is relative to `2026/`. Snowflake authenticates the request, checks the privileges of the user’s default role, and adds the file to the pipe’s ingest queue. Snowpipe skips any path that the pipe already received in the last 14 days, and any path that doesn’t match the pipe’s `PATTERN` copy option.
3. **Snowpipe loads the file.** Snowflake-managed compute runs the pipe’s `COPY INTO` statement on the queued files and commits the rows to the target table. Snowpipe is designed to load a file within about a minute after it receives the request, but large files and complex transformations take longer, and Snowflake doesn’t guarantee load latency.
4. **Your application checks the result.** It calls the `insertReport` or `loadHistoryScan` endpoint, or queries the copy history with SQL. If the pipe has [error notifications](/user-guide/data-load-snowpipe-errors) enabled, Snowpipe also sends your cloud messaging service a message that lists the files that failed to load.

Snowflake bills the loads that your application starts with the REST API in the same way as loads that start from event notifications. For more information, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing).

## Endpoints

The Snowpipe REST API has three endpoints. Each endpoint URL has the following form:

```
https://<account_identifier>.snowflakecomputing.com/v1/data/pipes/<pipe_name>/<endpoint>
```

Where:

- `<account_identifier>` is your [account identifier](/user-guide/admin-account-identifier), preferably in the `organization_name-account_name` format.
- `<pipe_name>` is the fully qualified name of the pipe, in the form `database.schema.pipe`. Snowflake resolves the name with the same rules as SQL identifiers: unquoted parts aren’t case-sensitive, so `mydb.myschema.orders_pipe` and `MYDB.MYSCHEMA.ORDERS_PIPE` identify the same pipe. If part of the name was created in double quotes, enclose that part in double quotes in the URL, encoded as `%22`.

To call any endpoint, the calling role needs the `USAGE` privilege on the database and schema that contain the pipe, in addition to the privilege in the following table:

| Endpoint | Method | What it does | Required privilege |
| --- | --- | --- | --- |
| [insertFiles](/user-guide/data-load-snowpipe-rest-apis#label-rest-api-insertfiles) | `POST` | Adds up to 5,000 staged files to the pipe’s ingest queue. | `OPERATE` on the pipe |
| [insertReport](/user-guide/data-load-snowpipe-rest-apis#label-rest-api-insertreport) | `GET` | Returns the files that the pipe loaded or failed to load in the last 10 minutes. | `MONITOR` on the pipe, or `MONITOR EXECUTION` on the account |
| [loadHistoryScan](/user-guide/data-load-snowpipe-rest-apis#label-rest-api-loadhistoryscan) | `GET` | Returns the files that the pipe loaded or failed to load in a time range that you specify. | `MONITOR` on the pipe, or `MONITOR EXECUTION` on the account |

Expand

Show lessSee more

For the parameters, request bodies, and response fields of each endpoint, see [Snowpipe REST API reference](/user-guide/data-load-snowpipe-rest-apis).

## Authentication and access control

The REST API doesn’t use sessions, so every request authenticates on its own. The usual method is key pair authentication. Your application signs a JWT with the private key of a Snowflake user, and sends the token in the `Authorization: Bearer <jwt>` header. The user must have the matching public key assigned. To generate a key pair and assign the public key to a user, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

You can generate the JWT with the Snowflake CLI [`snow connection generate-jwt`](/developer-guide/snowflake-cli/command-reference/connection-commands/generate-jwt) command, with a JWT library in your application, or with the Snowflake Ingest SDK for Java or Python, which also renews the token for you. The token uses the same claims as a key pair token for the SQL API. For the claims, and for examples in Python, Java, and Node.js, see [Using key-pair authentication](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair). A JWT is valid for at most one hour after its issue time, even if its expiration time is later, so generate a new one before the current one expires.

You can also authenticate with [workload identity federation](/user-guide/workload-identity-federation). Send the token in the `Authorization: Bearer WIF.<provider>.<token>` header. Snowflake recognizes the token type from the `WIF.` prefix, so you don’t need the `X-Snowflake-Authorization-Token-Type` header. To get a token, see [Using workload identity federation](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-wif).

Keep the following in mind when you set up access:

- **Requests run with the user’s default role.** You can’t choose a role in the request. If the user doesn’t have a default role, requests run with the `PUBLIC` role. Set the user’s `DEFAULT_ROLE` property to a role that has the [required privileges](#label-snowpipe-rest-endpoints).
- **Each application should use a dedicated user and role.** Snowflake recommends that each application use its own [service user](/user-guide/admin-user-management#label-user-management-types) (`TYPE = SERVICE`), with a role that has only the privileges that the application needs. This setup follows the principle of least privilege.
- **The pipe owner needs the load privileges.** Snowpipe loads the files with the privileges of the role that owns the pipe, so that role needs privileges on the stage and the target table. The role that calls the REST API doesn’t. For the privileges that a pipe owner needs, see the **Own a pipe** column in [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control).

For an example that creates a role, grants it the privileges to call the REST API, and creates a service user with that role as its default role, see [Grant access privileges](/user-guide/data-load-snowpipe-rest-gs#label-snowpipe-rest-endpoints-access-control).

## Example: Load a file with curl

The following example loads one file with curl, and then checks the result. It assumes that you already have the following objects:

- An external stage named `mydb.myschema.orders_stage`, with the URL `s3://mybucket/orders/`.
- A pipe named `mydb.myschema.orders_pipe` that loads JSON files from the stage. Because the pipe loads from the stage without a path, each file path in the request is relative to the stage URL.
- A service user named `snowpipe_loader_svc` with a key pair, and a default role that has the `OPERATE` and `MONITOR` privileges on the pipe and the `USAGE` privilege on its database and schema.

For instructions on how to create these objects, see [Set up the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs).

1. Stage the file. The following command copies a file to the stage location with the AWS CLI:

   Copy code

   ```
   aws s3 cp orders_0001.json.gz s3://mybucket/orders/2026/10/03/orders_0001.json.gz
   ```

   If your pipe loads from an internal stage, upload the file with the `PUT` command instead.
2. Generate a JWT for the user. The following command prompts for the passphrase of the private key, unless you set the `PRIVATE_KEY_PASSPHRASE` environment variable:

   Copy code

   ```
   JWT=$(snow connection generate-jwt \
     --account myorg-myaccount \
     --user SNOWPIPE_LOADER_SVC \
     --private-key-file ~/keys/snowpipe_rsa_key.p8)
   ```
3. Submit the file to the `insertFiles` endpoint. The path is relative to the stage URL:

   Copy code

   ```
   curl --request POST \
     "https://myorg-myaccount.snowflakecomputing.com/v1/data/pipes/MYDB.MYSCHEMA.ORDERS_PIPE/insertFiles?requestId=$(uuidgen)" \
     --header "Authorization: Bearer ${JWT}" \
     --header "Content-Type: application/json" \
     --header "Accept: application/json" \
     --data '{"files": [{"path": "2026/10/03/orders_0001.json.gz", "size": 52428800}]}'
   ```

   Add `showSkippedFiles=true` to the URL when you want the response to list paths that the pipe already received and therefore skipped.

   The response confirms that Snowpipe queued the file:

   Copy code

   ```
   {
     "requestId": "8C0A6C3E-1F4B-4D5E-9A7B-2F6D1E3C4B5A",
     "responseCode": "SUCCESS"
   }
   ```
4. After a minute or two, call the `insertReport` endpoint to check the result:

   Copy code

   ```
   curl --request GET \
     "https://myorg-myaccount.snowflakecomputing.com/v1/data/pipes/MYDB.MYSCHEMA.ORDERS_PIPE/insertReport?requestId=$(uuidgen)" \
     --header "Authorization: Bearer ${JWT}" \
     --header "Accept: application/json"
   ```

   The `status` field shows that the file loaded:

   Copy code

   ```
   {
     "pipe": "MYDB.MYSCHEMA.ORDERS_PIPE",
     "completeResult": true,
     "nextBeginMark": "1_0",
     "files": [
       {
         "path": "2026/10/03/orders_0001.json.gz",
         "stageLocation": "s3://mybucket/orders/",
         "fileSize": 52428800,
         "timeReceived": "2026-10-03T17:42:10.112Z",
         "lastInsertTime": "2026-10-03T17:42:41.583Z",
         "rowsInserted": 184213,
         "rowsParsed": 184213,
         "errorsSeen": 0,
         "errorLimit": 1,
         "complete": true,
         "status": "LOADED"
       }
     ]
   }
   ```

   If the file isn’t in the report yet, Snowpipe hasn’t finished loading it. Call the endpoint again, and pass the `nextBeginMark` value from the previous response as the `beginMark` parameter.

## Check load results

The REST API and SQL give you several ways to find out whether your files loaded. In the reports from the REST API, each file has one of the following statuses: `LOADED`, `LOAD_IN_PROGRESS`, `PARTIALLY_LOADED`, or `LOAD_FAILED`. The copy history shows the same statuses as `Loaded`, `Load in progress`, `Partially loaded`, and `Load failed`. The following table compares the options:

| Option | History available | Requires a warehouse | Use it to |
| --- | --- | --- | --- |
| `insertReport` endpoint | The last 10 minutes, up to the 10,000 most recent files | No | Poll for the results of files that you just submitted |
| `loadHistoryScan` endpoint | A time range that you specify within the last 14 days, up to 10,000 files for each call | No | Look up the results for a period that `insertReport` no longer covers |
| [COPY\_HISTORY](/sql-reference/functions/copy_history) table function | The last 14 days | Yes | Investigate failed files with SQL, including the first error in each file |
| [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) | The last 365 days, usually with a latency of up to 2 hours, but up to 2 days for a table with few recent loads | Yes | Audit loads over a longer period |

Expand

Show lessSee more

Keep the following in mind when you use the report endpoints:

- **Poll `insertReport` often enough.** The endpoint keeps only the last 10 minutes of results, so call it every few minutes, and pass the `nextBeginMark` value from each response as the `beginMark` parameter of the next call. If the `completeResult` field is `false`, you missed some results; call `loadHistoryScan` for the time range that you missed.
- **Use narrow time ranges with `loadHistoryScan`.** The endpoint is rate limited. Request only the time range that you need; for example, read the last 10 minutes every 8 minutes, rather than the last 24 hours every minute.

To investigate failed files with SQL, query the [COPY\_HISTORY](/sql-reference/functions/copy_history) table function. For example, the following query returns the files that the pipe processed in the last hour, with the first error in each file that failed:

Copy code

```
SELECT file_name, status, row_count, first_error_message, last_load_time
  FROM TABLE(mydb.INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'mydb.myschema.orders',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP()),
    PIPE_NAME => 'MYDB.MYSCHEMA.ORDERS_PIPE'))
  ORDER BY last_load_time DESC;
```

To find out about failed files without polling, set up [error notifications](/user-guide/data-load-snowpipe-errors#label-snowpipe-errors-set-up) for the pipe.

## Handle errors and retries

Design your application to retry requests that fail with a timeout, a `429` status, or a `5xx` status. Retrying doesn’t help if a request contains more than 5,000 files or has a body that Snowflake can’t parse, so correct those requests first, as described in the table later in this section. Retrying is safe: Snowpipe skips any path that the pipe already received in the last 14 days, so it doesn’t load a resubmitted file twice. Wait longer before each retry; for example, use exponential backoff.

For the same reason, submitting a file again doesn’t reload it, even if you corrected the file. To load the corrected file, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).

For the parameters and response fields of each endpoint, see [Snowpipe REST API reference](/user-guide/data-load-snowpipe-rest-apis). The following table summarizes the HTTP status codes and what to do about each one:

| Status | Meaning | What to do |
| --- | --- | --- |
| `200` | The request succeeded. For `insertFiles`, Snowpipe queued the files. It skipped any file that the pipe already received or that doesn’t match the pipe’s `PATTERN` copy option. | For `insertFiles`, check the results later with a report endpoint. |
| `400` | The request is invalid. For example, the request has no files, a file path is longer than 1,024 bytes, a required parameter is missing or invalid, or the pipe is a clone that’s in the `STOPPED_CLONED` state. | Correct the request before you send it again. For a cloned pipe, check its `COPY INTO` statement before you resume it, as described in [Pipe execution states](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-execution-states). |
| `401` | The token is invalid or expired. | Generate a new token. For key pair authentication, check that the account and user in the token are uppercase, and that the public key fingerprint matches the key that’s assigned to the user. For workload identity federation, check that the token comes from the provider and identity in the user’s `WORKLOAD_IDENTITY` property. |
| `403` | The user’s default role has privileges on the pipe, but not the privilege that the endpoint requires. | Grant the [required privilege](#label-snowpipe-rest-endpoints) to the role. |
| `404` | The pipe doesn’t exist, or the user’s default role has no privileges on the pipe or on the database and schema that contain it. | Check the fully qualified pipe name in the URL, and the privileges of the user’s default role. |
| `415` | The `Content-Type` header of an `insertFiles` request isn’t `application/json` or `text/plain`. | Set the `Content-Type` header to `application/json`. |
| `429` | Snowflake limited the rate of requests or of submitted files, or the request contains more than 5,000 files. | If the request contains more than 5,000 files, split it into requests of up to 5,000 files. Otherwise, retry with exponential backoff. |
| `500` | An internal error occurred, or Snowflake couldn’t parse the request body. | Check that the request body is valid, and then retry with exponential backoff. |

Expand

Show lessSee more

A `200` response from `insertFiles` doesn’t mean that the files loaded. Files might still fail to load, such as when a file has a data error or is missing from the stage. To find out why a file failed, check its status and first error in a report endpoint or in the copy history. For more information, see [Files don’t load with the REST API](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-rest-api).

## Best practices and limitations

The following sections describe practices that make your application efficient and reliable, and the limits to plan for.

### Best practices

- **Submit files only after they’re complete.** If your application submits a file before it finishes writing the file, Snowpipe might load part of the file or fail to find it. After Snowpipe receives a path, it ignores later submissions of the same path for 14 days.
- **Send several files in each request.** One request can contain up to 5,000 files. Sending many files in one request is less likely to reach rate limits than sending a separate request for each file.
- **Include each file’s size.** When you know the size of a file in bytes, include it in the `size` field of the request. Snowpipe uses the size to plan the load.
- **Send a request ID.** Add a unique `requestId` parameter, such as a UUID, to each request so that you can trace the request in logs and with [Snowflake Support](/user-guide/contacting-support).
- **Reuse tokens.** Use the same JWT for multiple requests, and generate a new one a few minutes before it expires, rather than generating a token for each request.
- **Size files for throughput.** Aim for compressed files of roughly 100 to 250 MB. For more information, see [Snowpipe and file sizing](/user-guide/data-load-considerations-prepare#label-snowpipe-file-size).
- **Protect and rotate the private key.** Store the private key in a secrets manager, not in your code. To rotate keys without downtime, assign a second public key to the user before you retire the first one. For more information, see [Configuring key-pair rotation](/user-guide/key-pair-auth#label-key-pair-rotation).

### Limitations

- An `insertFiles` request can contain up to 5,000 files, and each file path can be up to 1,024 bytes long when encoded as UTF-8.
- The `insertReport` endpoint keeps the 10,000 most recent results for up to 10 minutes.
- The `loadHistoryScan` endpoint returns load history from the last 14 days only, up to 10,000 files for each call. Snowflake limits how often you can call it.
- Each request authenticates with a bearer token. A key pair JWT is valid for at most one hour.
- Requests always run with the user’s default role.
- Snowpipe doesn’t load files from user stages or temporary stages.

## Next steps

- To create the stage, pipe, user, and role that the REST API needs, see [Set up the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs).
- To call the REST API with the Snowflake Ingest SDK for Java or Python, see [the SDK examples](/user-guide/data-load-snowpipe-rest-load).
- To call the REST API from an AWS Lambda function when files arrive in Amazon S3, see [Call the Snowpipe REST API from AWS Lambda](/user-guide/data-load-snowpipe-rest-lambda).
- To read the details of each endpoint, see [Snowpipe REST API reference](/user-guide/data-load-snowpipe-rest-apis).
- To get notified when files fail to load, see [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors).
- To pause, resume, or recreate a pipe, see [Manage Snowpipe](/user-guide/data-load-snowpipe-manage).
