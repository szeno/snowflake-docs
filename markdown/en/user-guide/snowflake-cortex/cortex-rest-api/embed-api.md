# Vector embedding REST API

The Cortex REST API gives you access to an endpoint for performing [vector embeddings](/user-guide/snowflake-cortex/vector-embeddings), using the [AI\_EMBED](/sql-reference/functions/ai_embed) function.

## Setting up authentication

To authenticate to the Cortex REST API, you can use the methods described in
[Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

Set the `Authorization` header to include your token (for example, a JSON web token (JWT), OAuth token, or
[programmatic access token](/user-guide/programmatic-access-tokens)).

Tip

Consider creating a dedicated user for Cortex REST API requests.

## Setting up authorization

To send a REST API request, your default role must be granted the SNOWFLAKE.CORTEX\_USER database role.
In most cases, users already have this privilege because SNOWFLAKE.CORTEX\_USER is granted to the PUBLIC
role automatically, and all roles inherit PUBLIC.

If your Snowflake administrator has revoked this grant, they must re-grant it:

Copy code

```
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE my_role;
GRANT ROLE my_role TO USER my_user;
```

Important

REST API requests use the user’s default role, so that role must have the necessary privileges. You can change
a user’s default role with [ALTER USER … SET DEFAULT\_ROLE](/sql-reference/sql/alter-user).

Copy code

```
ALTER USER my_user SET DEFAULT_ROLE=my_role
```

## Endpoint format

You can make requests to the `/api/v2/cortex/inference:embed` endpoint to create embeddings for your text. The request takes the following form:

```
POST https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:embed
```

where `account_identifier` is the [account identifier](/user-guide/admin-account-identifier) you use to access Snowsight.

## Model availability

The following table shows the EMBED function models that you can prompt using the REST API.

**EMBED function models**

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) | Azure East US 2 (Virginia) | Azure West Europe (Netherlands) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `snowflake-arctic-embed-m-v1.5` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `e5-base-v2` | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

Expand

Show lessSee more

The following table shows the number of dimensions that each model can return.

**EMBED function models**

| Model | Number of dimensions |
| --- | --- |
| `snowflake-arctic-embed-m-v1.5` | 768 |
| `snowflake-arctic-embed-m` | 768 |
| `e5-base-v2` | 768 |
| `snowflake-arctic-embed-l-v2.0` | 1024 |

Expand

Show lessSee more

## API Reference

### POST /api/v2/cortex/inference:embed

Creates an embedding for text that you specify.

Required headers

`Authorization: Bearer token`.
:   Authorization for the request. `token` is a JSON web token (JWT), OAuth token, or
    [programmatic access token](/user-guide/programmatic-access-tokens)). For details, see
    [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

`Content-Type: application/json`
:   Specifies that the body of the request is in JSON format.

`Accept: application/json`
:   Specifies that the response contains JSON.

#### Optional headers

`X-Snowflake-Authorization-Token-Type: type`
:   Defines the type of authorization token.

    If you omit the `X-Snowflake-Authorization-Token-Type` header, Snowflake determines the token type by examining the token.

    Even though this header is optional, you can choose to specify this header. You can set the header to one of the following values:

    - `KEYPAIR_JWT` (for key-pair authentication)
    - `OAUTH` (for OAuth)
    - `PROGRAMMATIC_ACCESS_TOKEN` (for [programmatic access tokens](/user-guide/programmatic-access-tokens))

#### Required JSON arguments

| Argument | Type | Description |
| --- | --- | --- |
| `text` | array | A list of text strings for which you’re generating embeddings. The list can contain up to 1280 strings, each of which can be up to 4096 characters long. |
| `model` | string | The model that you’re using to create the embeddings. |

Expand

Show lessSee more

#### Status codes

The Snowflake Cortex LLM REST API uses the following HTTP status codes to indicate successful completion or various error
conditions.

200 `OK`
:   Request completed successfully. The body of the response contains the output of the model.

400 `invalid options object`
:   The optional arguments have invalid values.

400 `unknown model model_name`
:   The specified model does not exist.

400 `schema validation failed`
:   Errors related to incorrect response schema structure. Correct the schema and try again.

400 `max tokens of count exceeded`
:   The request exceeded the maximum number of tokens supported by the model (see [Model restrictions](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-model-restrictions)).

400 `all requests were throttled by remote service`
:   The request has been throttled due to a high level of usage. Try again later.

402 `budget exceeded`
:   The model consumption budget was exceeded.

403 `Not Authorized`
:   Account not enabled for REST API, or the default role for the calling user does not have the `snowflake.cortex_user` database role.

429 `too many requests`
:   The request was rejected because the usage quota has been exceeded. Please try your request later.

503 `embed timed out`
:   The request took too long.

## CURL request example

The following example uses `curl` to make an EMBED request to the `e5-base-v2` model.
Replace `token` and `account_identifier` with the appropriate values in this command.

Copy code

```
curl --location "<account_url>/api/v2/cortex/inference:embed" \
--header 'X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer <token>" \
--data '{
"text": ["foo", "bar"],
"model": "e5-base-v2"
}'
```

### Output

The following is the output of the request, with the contents of the embedding array truncated:

```
{
  "object" : "list",
  "data" : [ {
    "object" : "embedding",
    "embedding" : [ [ -0.02102863, 0.0051381723, -0.0071509206, -0.032512695, 0.056507032, ... ] ],
    "index" : 0
  }, {
    "object" : "embedding",
    "embedding" : [ [ -0.03859099, -0.0025452692, 0.002827513, -0.023107057, 0.039019972, ... ] ],
    "index" : 1
  } ],
  "model" : "e5-base-v2",
  "usage" : {
    "total_tokens" : 6
  }
}
```

Each embedding has an index that corresponds to the text string in a list in the request. The index is 0-based, so the first text string in the list has an index of 0, the second text string has an index of 1, and so on.

In the preceding example, “foo” corresponds to the 0 index and “bar” corresponds to the 1 index. The embedding for “foo” is the first element in the list of embeddings, and the embedding for “bar” is the second element in the list of embeddings.

## Python request example

The following example uses the Python API to make an EMBED request to the `e5-base-v2` model.
Replace `token` and `account_identifier` with the appropriate values in this command.

Copy code

```
from snowflake.core import Root
from snowflake.snowpark.context import get_active_session

def embed_service():
    # Initialize Snowflake session and root
    session = get_active_session()
    root = Root(session)

    # Send embed_request request and process response
    response = root.cortex_embed_service.embed("e5-base-v2", ['foo', 'bar'])
    print(response)

if __name__ == "__main__":
    embed_service()
```

### Output

The following is the output of the request, with the contents of the embedding array truncated:

```
{
  "object" : "list",
  "data" : [ {
    "object" : "embedding",
    "embedding" : [ [ -0.02102863, 0.0051381723, -0.0071509206, -0.032512695, 0.056507032, ... ] ],
    "index" : 0
  }, {
    "object" : "embedding",
    "embedding" : [ [ -0.03859099, -0.0025452692, 0.002827513, -0.023107057, 0.039019972, ... ] ],
    "index" : 1
  } ],
  "model" : "e5-base-v2",
  "usage" : {
    "total_tokens" : 6
  }
}
```

Each embedding has an index that corresponds to the text string in a list in the request. The index is 0-based, so the first text string in the list has an index of 0, the second text string has an index of 1, and so on.

In the preceding example, “foo” corresponds to the 0 index and “bar” corresponds to the 1 index. The embedding for “foo” is the first element in the list of embeddings, and the embedding for “bar” is the second element in the list of embeddings.

## Usage quotas

The following table shows the usage quotas for the EMBED function.

**EMBED function quotas**

| Model | Tokens Processed per Minute (TPM) | Requests per Minute (RPM) | Max output (tokens) |
| --- | --- | --- | --- |
| `snowflake-arctic-embed-m-v1.5` | 400,000 | 200 | 4,096 |
| `snowflake-arctic-embed-m` | 400,000 | 200 | 4,096 |
| `e5-base-v2` | 400,000 | 200 | 4,096 |
| `nv-embed-qa-4` | 400,000 | 200 | 4,096 |
| `multilingual-e5-large` | 400,000 | 200 | 4,096 |
| `voyage-multilingual-2` | 400,000 | 200 | 4,096 |

Expand

Show lessSee more
