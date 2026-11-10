# Models and regional availability for Cortex AI Functions

Snowflake Cortex AI Functions support a range of language and embedding models with varying capabilities and
context-window sizes. Use this reference to choose a model for your workload, check its input and output limits,
confirm which regions a function runs in, and understand
[legacy and end-of-life access](#label-cortex-model-lifecycle).

Per-model availability is on the Model availability page

This page does not list availability for individual models. To look up a specific model name, see
[Model availability](/user-guide/snowflake-cortex/model-availability), which covers every Cortex model across all
products.

## Choosing a model

The Snowflake Cortex AI\_COMPLETE function supports models from several providers, with varying capability, latency, and
cost. To achieve the best [performance per credit](/user-guide/snowflake-cortex/aisql-cost), choose a model that’s a good
match for the content size and complexity of your task. The following sections group models by family. For each model’s
input and output limits, see [Model restrictions](#label-cortex-llm-model-restrictions).

### Large models

If you’re not sure where to start, try a large model first to establish a quality baseline, then evaluate smaller models
against it.

- **Anthropic Claude Opus** (`claude-opus-5-5`; `claude-opus-5`): Anthropic’s most capable models,
  suited for complex reasoning, coding, long-horizon agentic work, and analysis of large document collections. Both
  models have a 1,000,000-token context window and up to 128,000 output tokens.
- **Google Gemini** (`gemini-4-argon`, Public Preview): Google’s most capable Gemini model in Snowflake Cortex,
  suited for advanced reasoning and multimodal tasks, with a 1,000,000-token context window.
- **OpenAI GPT Astra** (`openai-gpt-6-astra`): OpenAI’s most capable model, suited for complex,
  demanding reasoning work.
- **OpenAI GPT Sol** (`openai-gpt-6-sol`, `openai-gpt-5.6-sol`): OpenAI’s frontier models for
  agentic coding and long-horizon tasks.

### Medium models

Medium models balance quality with lower latency and cost, and suit most production workloads.

- **Anthropic Claude Sonnet** (`claude-sonnet-5-5`; `claude-sonnet-5`): strong performance on coding,
  tool use, and agentic tasks at lower latency and cost than Claude Opus. `claude-sonnet-5` has a 1,000,000-token
  context window and up to 64,000 output tokens.
- **xAI Grok** (`grok-4.7`, Public Preview): a general-purpose model for reasoning and agentic tasks, with a
  500,000-token context window.
- **OpenAI GPT Terra** (`openai-gpt-6.1-terra`, Public Preview; `openai-gpt-5.6-terra`): balanced models for
  everyday production work, including code generation, content workflows, and structured data extraction.
  `openai-gpt-5.6-terra` has a 1,050,000-token context window and up to 128,000 output tokens.

### Small models

Small models are fast and cost-efficient, and suit high-volume tasks like classification, extraction, and summarization.

- **Anthropic Claude Haiku** (`claude-haiku-4-5`): optimized for low-latency, high-throughput workloads, with a
  200,000-token context window and up to 64,000 output tokens.
- **Google Gemini Flash** (`gemini-3.8-flash`): a fast, low-cost Gemini model for high-volume tasks, with a
  1,000,000-token context window.
- **OpenAI GPT Luna** (`openai-gpt-6-luna`, `openai-gpt-5.6-luna`): fast, low-cost models for
  repeatable work at scale, such as summarizing documents, extracting information, and answering focused questions.
  Both have a 1,050,000-token context window and up to 128,000 output tokens.
- **OpenAI GPT mini and nano** (`openai-gpt-5.4-mini`, `openai-gpt-5.4-nano`): small, fast GPT models, each with a
  400,000-token context window and up to 128,000 output tokens.

Many of these models are available only through
[cross-region inference](/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference). Check
[Model availability](/user-guide/snowflake-cortex/model-availability#label-cortex-model-availability-by-region) for your
region before you choose.

Note

Availability of `openai-gpt-5.6-luna`, `openai-gpt-5.6-sol`, `openai-gpt-5.6-terra`, and later OpenAI models can vary by account because of model provider requirements. If a request fails with the error `Due to model provider requirements, this account is not eligible for this model at this time.`, contact [Snowflake Support](/user-guide/contacting-support).

## Function availability by region

Snowflake Cortex AI functions are available in the following regions. If your region is not listed for a particular
function, use
[cross-region inference](/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference).

The tables in this section cover the functions themselves. The models that `AI_COMPLETE` and `AI_EMBED` accept have
their own regional availability, documented in
[Model availability](/user-guide/snowflake-cortex/model-availability#label-cortex-model-availability-by-region). A
function being available in your region does not mean every model it accepts is, so check both.

Note

- You can call AI\_COUNT\_TOKENS in all regions. Supported functions and models are listed in [supported functions and models](/sql-reference/functions/ai_count_tokens#label-ai-count-tokens-supported). The models themselves are available only in the regions specified in the tables below.

Cross-RegionNorth AmericaEuropeAsia-Pacific

The following functions are available in any region via
[cross-region inference](/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference).

| Function | Cross Cloud (Any Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **AI\_COMPLETE** | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| **AI\_EMBED** | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ |  |
| **AI\_CLASSIFY TEXT** | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **AI\_CLASSIFY IMAGE** | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  |  |  |
| **AI\_EXTRACT** | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |
| **AI\_FILTER TEXT** | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **AI\_FILTER IMAGE** | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  |  |  |
| **AI\_AGG** |  | ✔ |  |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **AI\_REDACT** | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ |  |
| **AI\_SENTIMENT** | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **AI\_SIMILARITY TEXT** | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ | ✔ |  |  |  |  |
| **AI\_SIMILARITY IMAGE** | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  | ✔ |  |
| **AI\_SUMMARIZE\_AGG** | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **AI\_TRANSCRIBE** | ✔ | ✔ |  |  |  | ✔ |  |  | ✔ |  |  |  |  |
| **SENTIMENT** | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **ENTITY\_SENTIMENT** | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **EXTRACT\_ANSWER** | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ |  |  |  |  |
| **SUMMARIZE** | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **TRANSLATE** | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| **AI\_TRANSLATE** | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |

Expand

Show lessSee more

The following functions are available natively in North American regions.

| Function | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **AI\_COMPLETE** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| **AI\_EMBED** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| **AI\_CLASSIFY TEXT** | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| **AI\_CLASSIFY IMAGE** | ✔ | ✔ |  |  |  |  |  |  |  |
| **AI\_EXTRACT** | ✔ | ✔ |  |  | ✔ | ✔ |  |  | ✔ |
| **AI\_FILTER TEXT** | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| **AI\_FILTER IMAGE** | ✔ | ✔ |  |  |  |  |  |  |  |
| **AI\_AGG** | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| **AI\_REDACT** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| **AI\_SIMILARITY TEXT** | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| **AI\_SIMILARITY IMAGE** | ✔ | ✔ |  |  |  |  |  |  |  |
| **AI\_SUMMARIZE\_AGG** | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| **AI\_TRANSCRIBE** | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| **SENTIMENT** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| **ENTITY\_SENTIMENT** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| **EXTRACT\_ANSWER** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| **SUMMARIZE** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| **TRANSLATE** | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |

Expand

Show lessSee more

The following functions are available natively in European regions.

| Function | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS Europe West 2 (London) | Azure West Europe (Netherlands) |
| --- | --- | --- | --- | --- |
| **AI\_COMPLETE** | ✔ | ✔ | ✔ | ✔ |
| **AI\_EMBED** | ✔ | ✔ |  | ✔ |
| **AI\_CLASSIFY TEXT** | ✔ | ✔ |  | ✔ |
| **AI\_CLASSIFY IMAGE** | ✔ |  |  |  |
| **AI\_EXTRACT** | ✔ | ✔ |  | ✔ |
| **AI\_FILTER TEXT** | ✔ | ✔ |  | ✔ |
| **AI\_FILTER IMAGE** | ✔ |  |  |  |
| **AI\_AGG** | ✔ | ✔ |  | ✔ |
| **AI\_REDACT** | ✔ | ✔ |  | ✔ |
| **AI\_SIMILARITY TEXT** | ✔ | ✔ |  | ✔ |
| **AI\_SIMILARITY IMAGE** | ✔ |  |  |  |
| **AI\_SUMMARIZE\_AGG** | ✔ | ✔ |  | ✔ |
| **AI\_TRANSCRIBE** | ✔ |  |  |  |
| **SENTIMENT** | ✔ | ✔ |  | ✔ |
| **ENTITY\_SENTIMENT** | ✔ |  |  | ✔ |
| **EXTRACT\_ANSWER** | ✔ | ✔ |  | ✔ |
| **SUMMARIZE** | ✔ | ✔ |  | ✔ |
| **TRANSLATE** | ✔ | ✔ |  | ✔ |

Expand

Show lessSee more

The following functions are available natively in Asia-Pacific regions:

| Function | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) |
| --- | --- | --- |
| **AI\_COMPLETE** | ✔ | ✔ |
| **AI\_EMBED** | ✔ | ✔ |
| **AI\_EXTRACT** | ✔ | ✔ |
| **AI\_CLASSIFY TEXT** | ✔ | ✔ |
| **AI\_CLASSIFY IMAGE** |  |  |
| **AI\_FILTER TEXT** | ✔ | ✔ |
| **AI\_FILTER IMAGE** |  |  |
| **AI\_AGG** | ✔ | ✔ |
| **AI\_SIMILARITY TEXT** | ✔ | ✔ |
| **AI\_SIMILARITY IMAGE** |  |  |
| **AI\_SUMMARIZE\_AGG** | ✔ | ✔ |
| **AI\_TRANSCRIBE** |  |  |
| **EXTRACT\_ANSWER** | ✔ | ✔ |
| **SENTIMENT** | ✔ | ✔ |
| **ENTITY\_SENTIMENT** |  | ✔ |
| **SUMMARIZE** | ✔ | ✔ |
| **TRANSLATE** | ✔ | ✔ |

Expand

Show lessSee more

† Functions are available to Azure US FedRAMP High Plus accounts through cross-region inference with processing on AWS in the United States. See [US FedRAMP High and DoD gov regions](/user-guide/snowflake-cortex/cross-region-inference#label-cortex-cross-region-fedramp-dod).

The following Snowflake Cortex AI functions are available in the following extended regions.

| Function | AWS US East 2 (Ohio) | AWS CA Central 1 (Central) | AWS SA East 1 (São Paulo) | AWS Europe West 2 (London) | AWS Europe Central 1 (Frankfurt) | AWS Europe North 1 (Stockholm) | AWS AP Northeast 1 (Tokyo) | AWS AP South 1 (Mumbai) | AWS AP Southeast 2 (Sydney) | AWS AP Southeast 3 (Jakarta) | Azure South Central US (Texas) | Azure West US 2 (Washington) | Azure UK South (London) | Azure North Europe (Ireland) | Azure Switzerland North (Zürich) | Azure Central India (Pune) | Azure Japan East (Tokyo, Saitama) | Azure Southeast Asia (Singapore) | Azure Australia East (New South Wales) | Google Cloud Europe West 2 (London) | Google Cloud Europe West 4 (Netherlands) | Google Cloud US Central 1 (Iowa) | Google Cloud US East 4 (N. Virginia) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **AI\_EMBED** | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| **AI\_EXTRACT** | ✔ | ✔ | ✔ | ✔ | ✔ | Cross-region only | ✔ | Cross-region only | ✔ | Cross-region only | ✔ | ✔ | Cross-region only | ✔ | Cross-region only | ✔ | ✔ | ✔ | ✔ | Cross-region only | Cross-region only | Cross-region only | Cross-region only |

Expand

Show lessSee more

## Model restrictions

Models used by Snowflake Cortex have limitations on size as described in the table below. Sizes are given in tokens.
According to industry estimates, tokens generally represent about four characters of text, so the number of words corresponding to a token limit is
less than the number of tokens. Inputs exceeding the context window limit result in an error. Output that exceeds the
context window limit is truncated.

The maximum size of the output that a model can produce is limited by the following:

- The model’s output token limit.
- The space available in the context window after the model consumes the input tokens.

For example, `claude-sonnet-4-6` has a context window of 1,000,000 tokens. If 100,000 tokens are used for the input, the model can generate up to 8,192 tokens. However, if 195,000 tokens are used as input, then the model can only generate up to 5,000 tokens for a total of 200,000 tokens.

Important

In the AWS AP Southeast 2 (Sydney) region:

- the context window for `llama3-8b` and `mistral-7b` is 4,096 tokens.
- the context window for `llama3.1-8b` is 16,384 tokens.
- the context window for the Snowflake managed model from the SUMMARIZE function is 4,096 tokens.

In the AWS Europe West 1 (Ireland) region:

- the context window for `llama3.1-8b` is 16,384 tokens.
- the context window for `mistral-7b` is 4,096 tokens.

| Function | Model | Context window (tokens) | Max output (tokens) |
| --- | --- | --- | --- |
| **AI\_COMPLETE** | `claude-opus-5-5` | 1,000,000 | 128,000 |
|  | `claude-opus-5` | 1,000,000 | 128,000 |
|  | `claude-sonnet-5` | 1,000,000 | 64,000 |
|  | `claude-opus-4-8` | 1,000,000 | 128,000 |
|  | `claude-opus-4-7` | 1,000,000 | 128,000 |
|  | `claude-opus-4-6` | 1,000,000 | 128,000 |
|  | `claude-sonnet-4-6` | 1,000,000 | 64,000 |
|  | `claude-opus-4-5` | 200,000 | 64,000 |
|  | `claude-sonnet-4-5` | 200,000 | 64,000 |
|  | `claude-haiku-4-5` | 200,000 | 64,000 |
|  | `openai-gpt-6-luna` | 1,050,000 | 128,000 |
|  | `openai-gpt-5.6-terra` | 1,050,000 | 128,000 |
|  | `openai-gpt-5.6-luna` | 1,050,000 | 128,000 |
|  | `openai-gpt-5.4-mini` | 400,000 | 128,000 |
|  | `openai-gpt-5.4-nano` | 400,000 | 128,000 |
|  | `openai-gpt-5.1` | 272,000 | 8,192 |
|  | `openai-gpt-5` | 272,000 | 8,192 |
|  | `openai-gpt-5-mini` | 272,000 | 8,192 |
|  | `openai-gpt-5-nano` | 272,000 | 8,192 |
|  | `openai-gpt-4.1` | 128,000 | 32,000 |
|  | `gemini-4-argon` | 1,000,000 | 32,768 |
|  | `gemini-3.8-flash` | 1,000,000 | 64,000 |
|  | `gemini-3.7-flash` | 1,000,000 | 64,000 |
|  | `gemini-3.5-flash` | 1,000,000 | 64,000 |
|  | `gemini-3.1-pro` | 1,000,000 | 64,000 |
|  | `gemini-3.1-flash-lite` | 1,000,000 | 64,000 |
|  | `grok-4.7` | 500,000 | 65,536 |
|  | `glm-5.3` | 1,000,000 | 128,000 |
|  | `qwen3-32b` | 128,000 | 8,192 |
|  | `qwen3-next-80b-a3b` | 128,000 | 8,192 |
|  | `qwen3-vl-235b-a22b` | 128,000 | 8,192 |
|  | `mistral-large3` | 256,000 | 32,768 |
|  | `mistral-large2` | 128,000 | 8,192 |
|  | `mixtral-8x7b` | 32,000 | 8,192 |
|  | `mistral-7b` | 32,000 | 8,192 |
|  | `llama4-maverick` | 128,000 | 8,192 |
|  | `llama3.3-70b` | 128,000 | 8,192 |
|  | `llama3.1-70b` | 128,000 | 8,192 |
|  | `llama3.1-8b` | 128,000 | 8,192 |
| **EMBED\_TEXT\_768** | `e5-base-v2` | 512 | n/a |
|  | `snowflake-arctic-embed-m` | 512 | n/a |
| **EMBED\_TEXT\_1024** | `nv-embed-qa-4` | 512 | n/a |
|  | `multilingual-e5-large` | 512 | n/a |
|  | `voyage-multilingual-2` | 32,000 | n/a |
| **AI\_EXTRACT** | `arctic-extract` | 128,000 | 51,200 |
| **AI\_FILTER** | Snowflake managed model | 128,000 | n/a |
| **AI\_CLASSIFY** | Snowflake managed model | 128,000 | n/a |
| **AI\_AGG** | Snowflake managed model | 128,000 per row can be used across multiple rows | 8,192 |
| **AI\_SENTIMENT** | Snowflake managed model | 2,048 | n/a |
| **AI\_SUMMARIZE\_AGG** | Snowflake managed model | 128,000 per row can be used across multiple rows | 8,192 |
| **ENTITY\_SENTIMENT** | Snowflake managed model | 2,048 | n/a |
| **EXTRACT\_ANSWER** | Snowflake managed model | 2,048 for text 64 for question | n/a |
| **SENTIMENT** | Snowflake managed model | 512 | n/a |
| **SUMMARIZE** | Snowflake managed model | 32,000 | 4,096 |
| **TRANSLATE** | Snowflake managed model | 100,000 (input only) | 100,000 |

Expand

Show lessSee more

## Model lifecycle: legacy and end-of-life

Snowflake retires Cortex models in two stages: **legacy**, then **end-of-life**. A model marked
legacy is not yet unavailable to every account. Access depends on whether your **account** already
used that model.

### Legacy

After a model’s legacy date:

- If your account used the model anywhere before the legacy date, the account can continue to use
  it in every supported application until the model’s end-of-life date. Supported applications
  include AI\_COMPLETE, CORTEX.COMPLETE, the Agents API, Cortex Inference, and Snowflake CoWork.
- If your account had not used the model anywhere before the legacy date, the account can’t start
  using it. Queries and API calls that name the model fail.

Any usage of the model in the account before the legacy date means that the account can continue
to use the model until end-of-life, including in applications that had not called that model
before.

Snowflake recommends that you migrate to a supported model before the end-of-life date, even if
your account can still call the legacy model.

### End-of-life

After a model’s end-of-life date, the model is no longer available to any account, regardless of
prior usage. Queries and API calls that name the model fail.

Use [SHOW CORTEX BASE MODELS](/sql-reference/sql/show-cortex-base-models) to see each model’s
`lifecycle_status`, `legacy_date`, and `eol_date`. Deprecation dates for specific models are
announced in unbundled behavior change releases, such as
[Cortex model deprecations for August 2026](/release-notes/bcr-bundles/un-bundled/bcr-august-model-deprecations).
