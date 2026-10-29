# Bring-your-own model for AI\_EMBED

Preview Feature — Open

Available to all accounts where Snowpark Container Services model inference is supported, with no additional edition restrictions.

[AI\_EMBED](/sql-reference/functions/ai_embed) supports running inference against a user-deployed model inference service on SPCS along with Snowflake’s Cortex models. To use this feature, the `model` argument needs to point to an SPCS model inference service that hosts a [Sentence Transformer](/developer-guide/snowflake-ml/model-registry/built-in-models/sentence-transformer) model.

Important

This feature supports text input only. FILE input (image embeddings) and [PROMPT](/sql-reference/functions/prompt) input aren’t supported. See [Limitations](#limitations).

## Prerequisites

Before you can use this feature, log a [Sentence Transformer](/developer-guide/snowflake-ml/model-registry/built-in-models/sentence-transformer) model, then deploy it as an SPCS model inference service using the [Snowsight UI](/developer-guide/snowflake-ml/model-registry/snowsight-ui#deploy-user-models) or the [Python API](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api#deploy-a-model-for-online-inference).

For more examples on creating SPCS inference services, see [Example workflows](/developer-guide/snowflake-ml/inference/real-time-inference-examples).

## Syntax

The function accepts the same arguments as the standard [AI\_EMBED](/sql-reference/functions/ai_embed) function. The only change is that the `model` argument is an SPCS service name instead of the name of a Cortex embedding model.

Copy code

```
AI_EMBED( <model> , <input> )
```

## Arguments

`model`
:   Name of an SPCS model inference service which hosts a [Sentence Transformer](/developer-guide/snowflake-ml/model-registry/built-in-models/sentence-transformer) model.

`input`
:   A string to generate an embedding from. FILE input is not supported. See [Limitations](#limitations).

## Returns

An embedding vector of type VECTOR derived from the input text.

## Examples

The examples in this section use a SQL variable for the service name:

Copy code

```
SET service_name = '<db>.<schema>.<service>';
```

You can confirm the service exists with the following command:

Copy code

```
DESC SERVICE IDENTIFIER($service_name);
```

### Single embedding

Copy code

```
SELECT AI_EMBED($service_name, 'hello world');
```

### Embeddings from a table column

Copy code

```
CREATE OR REPLACE TABLE documents (id INT, content VARCHAR);
INSERT INTO documents VALUES
  (1, 'Snowflake is a cloud data platform.'),
  (2, 'Embeddings represent text as vectors.'),
  (3, 'AI_EMBED generates vector embeddings.');

SELECT
  id,
  content,
  AI_EMBED($service_name, content) AS embedding
FROM documents
ORDER BY id;
```

## Limitations

The following AI\_EMBED inputs are not yet supported when the function points to an SPCS service.

### FILE input

Image embedding via FILE input is not supported. The SPCS path only accepts text input.

Copy code

```
-- Image input is not supported.
SELECT AI_EMBED(
  $service_name,
  TO_FILE('@my_images', 'cat.png')
);
```

### PROMPT input

[PROMPT](/sql-reference/functions/prompt) inputs are rejected to avoid handling multimodal inputs, which are not supported yet on the SPCS path. As a result, even PROMPT() templates that contain only text arguments are rejected.

Copy code

```
-- PROMPT() input is not supported.
SELECT AI_EMBED(
  $service_name,
  PROMPT('Embed: {0}', 'hello world')
);
```

## Access control requirements

The user must have the USAGE privilege on the SPCS service and on its inference function.

## Legal notices

Refer to [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql#legal-notices).
