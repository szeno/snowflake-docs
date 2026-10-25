# Model availability for Snowflake Cortex AI

Snowflake offers a wide range of models across different regions and products. The two sections below outline:

- [Product availability](#label-cortex-model-availability-by-product): which products support each model, and at what release stage. A model can be GA in one product and in preview in another.
- [Regional availability](#label-cortex-model-availability-by-region): which clouds and regions each model runs in.

Checking availability programmatically

Run `SHOW CORTEX BASE MODELS IN SCHEMA SNOWFLAKE.MODELS` to see the models your current role can use, including their release stage and cross-region scopes. See [SHOW CORTEX BASE MODELS](/sql-reference/sql/show-cortex-base-models).

✔ GA. \* Public preview. \*\* Private preview, available only to accounts that Snowflake has enabled. Legacy: only accounts that already used the model can keep calling it. Preview models aren’t suitable for production workloads. A blank cell means the model isn’t available there.

† Azure US FedRAMP High Plus accounts reach these models through cross-region inference, with processing on AWS in the United States. See [US FedRAMP High and DoD gov regions](/user-guide/snowflake-cortex/cross-region-inference#label-cortex-cross-region-fedramp-dod).

## Product availability

Jump to a provider: [Alibaba](#label-cortex-model-availability-product-alibaba) | [Anthropic](#label-cortex-model-availability-product-anthropic) | [DeepSeek](#label-cortex-model-availability-product-deepseek) | [Google](#label-cortex-model-availability-product-google) | [Meta](#label-cortex-model-availability-product-meta) | [Microsoft](#label-cortex-model-availability-product-microsoft) | [Mistral AI](#label-cortex-model-availability-product-mistral) | [Moonshot AI](#label-cortex-model-availability-product-moonshot) | [NVIDIA](#label-cortex-model-availability-product-nvidia) | [OpenAI](#label-cortex-model-availability-product-openai) | [Snowflake](#label-cortex-model-availability-product-snowflake) | [Voyage AI](#label-cortex-model-availability-product-voyage) | [xAI](#label-cortex-model-availability-product-xai) | [Z.ai](#label-cortex-model-availability-product-zai)

### Alibaba

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `qwen3-next-80b-a3b` | ✔ |  |  |  |  |
| `qwen3-vl-235b-a22b` | ✔ |  |  |  |  |
| `qwen3-32b` | ✔ |  |  |  |  |

Expand

Show lessSee more

### Anthropic

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `claude-opus-5-5` | \* | \* | \* |  | \* |
| `claude-sonnet-5-5` | \* | \* | \* |  | \* |
| `claude-haiku-5-5` |  | \* | \* |  | \* |
| `claude-fable-5-1` | \*\* | \*\* | \*\* |  | \*\* |
| `claude-fable-5` | \*\* | \*\* | \*\* |  | \*\* |
| `claude-opus-5` | ✔ | ✔ | ✔ |  | ✔ |
| `claude-sonnet-5` | ✔ | ✔ | ✔ |  | ✔ |
| `claude-opus-4-8` | ✔ | ✔ | ✔ |  | ✔ |
| `claude-opus-4-7` | ✔ | ✔ | ✔ |  | ✔ |
| `claude-opus-4-6` | ✔ | ✔ | ✔ |  | ✔ |
| `claude-sonnet-4-6` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `claude-opus-4-5` | ✔ | ✔ | ✔ |  | ✔ |
| `claude-sonnet-4-5` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `claude-haiku-4-5` | ✔ | ✔ | ✔ |  | ✔ |

Expand

Show lessSee more

### DeepSeek

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `deepseek-v4-flash` |  | \*\* |  |  |  |

Expand

Show lessSee more

### Google

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `gemini-4-argon` | \* |  | \* |  | \* |
| `gemini-3.1-pro` | \* |  | \* |  |  |
| `gemini-3.8-flash` | ✔ |  | ✔ |  | ✔ |
| `gemini-3.7-flash` | \* |  | \* |  | \* |
| `gemini-3.5-flash` | ✔ |  | ✔ |  |  |
| `gemini-3.1-flash-lite` | ✔ |  |  |  |  |

Expand

Show lessSee more

### Meta

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `llama4-maverick` | Legacy | Legacy |  |  |  |
| `llama3.3-70b` | ✔ |  |  |  |  |
| `llama3.1-70b` | Legacy | Legacy |  |  |  |
| `llama3.1-8b` | ✔ | ✔ |  |  |  |

Expand

Show lessSee more

### Microsoft

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `multilingual-e5-large` | ✔ |  |  |  |  |
| `e5-base-v2` | ✔ |  |  |  |  |

Expand

Show lessSee more

### Mistral AI

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `mistral-large2` | Legacy | Legacy |  |  |  |
| `mistral-large3` | \* |  |  |  |  |
| `mixtral-8x7b` | Legacy |  |  |  |  |
| `mistral-7b` | Legacy | Legacy |  |  |  |

Expand

Show lessSee more

### Moonshot AI

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `kimi-k3` | \* | \* | \* |  | \* |

Expand

Show lessSee more

### NVIDIA

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `nv-embed-qa-4` | ✔ |  |  |  |  |

Expand

Show lessSee more

### OpenAI

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `openai-gpt-6.1-sol` | \*\* | \* | \* |  | \* |
| `openai-gpt-6-astra` | \*\* | ✔ | \*\* |  | \*\* |
| `openai-gpt-6-sol` | \*\* | \* | \* |  |  |
| `openai-gpt-6-luna` | \*\* | \* | \* |  |  |
| `openai-gpt-5.6-sol` | \*\* | ✔ | \*\* |  | \*\* |
| `openai-gpt-5.6-terra` | \*\* | ✔ | \*\* |  | \*\* |
| `openai-gpt-5.6-luna` | \*\* | ✔ | \*\* |  | \*\* |
| `openai-gpt-5.5` | \*\* | \*\* | \*\* |  | \*\* |
| `openai-gpt-5.4` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `openai-gpt-5.4-mini` | ✔ |  |  |  |  |
| `openai-gpt-5.4-nano` | ✔ |  |  |  |  |
| `openai-gpt-5.2` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `openai-gpt-5.1` | ✔ | ✔ | ✔ |  |  |
| `openai-gpt-5` | ✔ | ✔ | ✔ |  |  |
| `openai-gpt-5-mini` | ✔ | ✔ | ✔ |  |  |
| `openai-gpt-5-nano` | ✔ | ✔ |  |  |  |
| `openai-gpt-4.1` | Legacy | Legacy | Legacy |  |  |

Expand

Show lessSee more

### Snowflake

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo | Cortex Search |
| --- | --- | --- | --- | --- | --- | --- |
| `snowflake-decision-fast` | \*\* | \*\* |  |  |  |  |
| `snowflake-arctic-embed-l-v2.0-8k` | ✔ |  |  |  |  | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ |  |  |  |  | ✔ |
| `snowflake-arctic-embed-m-v1.5` | ✔ |  |  |  |  | ✔ |
| `snowflake-arctic-embed-m` | ✔ |  |  |  |  |  |

Expand

Show lessSee more

### Voyage AI

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo | Cortex Search |
| --- | --- | --- | --- | --- | --- | --- |
| `voyage-multilingual-2` | ✔ |  |  |  |  | ✔ |

Expand

Show lessSee more

### xAI

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `grok-4.7` | \* | \* | \* |  | \* |
| `grok-4.6` | \* | \* | \* |  | \* |

Expand

Show lessSee more

### Z.ai

| Model | AI Functions | Cortex Inference | Cortex Agents / CoWork | Agent Evaluations | CoCo |
| --- | --- | --- | --- | --- | --- |
| `glm-5.3` | \* | \* | \* |  |  |

Expand

Show lessSee more

## Regional availability

Most models are reached through [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference), which depends on your `CORTEX_ENABLED_CROSS_REGION` setting rather than your account’s region. Some models also run natively in specific regions.

Jump to a provider: [Alibaba](#label-cortex-model-availability-region-alibaba) | [Anthropic](#label-cortex-model-availability-region-anthropic) | [DeepSeek](#label-cortex-model-availability-region-deepseek) | [Google](#label-cortex-model-availability-region-google) | [Meta](#label-cortex-model-availability-region-meta) | [Microsoft](#label-cortex-model-availability-region-microsoft) | [Mistral AI](#label-cortex-model-availability-region-mistral) | [Moonshot AI](#label-cortex-model-availability-region-moonshot) | [NVIDIA](#label-cortex-model-availability-region-nvidia) | [OpenAI](#label-cortex-model-availability-region-openai) | [Snowflake](#label-cortex-model-availability-region-snowflake) | [Voyage AI](#label-cortex-model-availability-region-voyage) | [xAI](#label-cortex-model-availability-region-xai) | [Z.ai](#label-cortex-model-availability-region-zai)

### Alibaba

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `qwen3-next-80b-a3b` | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ |  |  |  |  |  |  |
| `qwen3-vl-235b-a22b` | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ |  |  |  |  |  |  |
| `qwen3-32b` | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ |  |  |  |  |  |  |

Expand

Show lessSee more

### Anthropic

Cross-regionEurope

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-opus-5-5` | \* | \* | \* |  |  |  | \* | \* | \* | \* |  |  |  |  |  |
| `claude-sonnet-5-5` | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `claude-haiku-5-5` | \* | \* | \* |  |  |  | \* | \* | \* | \* |  |  |  |  |  |
| `claude-fable-5-1` | \*\* | \*\* | \*\* |  |  |  |  |  |  |  |  |  |  |  |  |
| `claude-fable-5` | \*\* | \*\* | \*\* |  |  |  |  |  |  |  |  |  |  |  |  |
| `claude-opus-5` | ✔ | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  |  |  |  |
| `claude-sonnet-5` | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| `claude-opus-4-8` | ✔ | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  |  |  |  |
| `claude-opus-4-7` | ✔ | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  |  |  |  |
| `claude-opus-4-6` | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ |  | ✔ |  |  |  |  |  |
| `claude-sonnet-4-6` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |
| `claude-opus-4-5` | ✔ | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  |  |  |  |
| `claude-sonnet-4-5` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  | ✔ |  |  |
| `claude-haiku-4-5` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in European regions, without cross-region inference.

| Model | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS Europe West 2 (London) | Azure West Europe (Netherlands) |
| --- | --- | --- | --- | --- |
| `claude-opus-4-6` |  |  | ✔ |  |
| `claude-sonnet-4-6` |  |  | ✔ |  |

Expand

Show lessSee more

### DeepSeek

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `deepseek-v4-flash` | \*\* |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

Expand

Show lessSee more

### Google

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `gemini-4-argon` | \* |  |  |  |  |  |  |  |  |  |  |  |  |  | \* |
| `gemini-3.1-pro` | \* |  |  |  |  |  |  |  |  |  |  |  |  |  | \* |
| `gemini-3.8-flash` | ✔ |  |  |  |  |  |  |  |  |  |  |  |  |  | ✔ |
| `gemini-3.7-flash` | \* |  |  |  |  |  |  |  |  |  |  |  |  |  | \* |
| `gemini-3.5-flash` | ✔ |  |  |  |  |  |  |  |  |  |  |  |  |  | ✔ |
| `gemini-3.1-flash-lite` | ✔ |  |  |  |  |  |  |  |  |  |  |  |  |  | ✔ |

Expand

Show lessSee more

### Meta

Cross-regionNorth AmericaEuropeAsia-Pacific

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `llama4-maverick` | Legacy | Legacy | Legacy |  |  |  |  |  |  |  |  |  |  |  |  |
| `llama3.3-70b` | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ | ✔ |  | ✔ |  | ✔ |  |
| `llama3.1-70b` | Legacy | Legacy | Legacy | Legacy |  |  | Legacy | Legacy | Legacy | Legacy | Legacy | Legacy |  | Legacy |  |
| `llama3.1-8b` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ |  |

Expand

Show lessSee more

These models run natively in North American regions, without cross-region inference.

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `llama4-maverick` | Legacy |  |  |  |  |  |  |  |  |
| `llama3.3-70b` | ✔ |  |  |  |  |  |  |  |  |
| `llama3-70b` | Legacy | Legacy |  | Legacy |  |  |  |  |  |
| `llama3-8b` | Legacy | Legacy |  | Legacy |  |  |  |  |  |
| `llama3.1-70b` | Legacy | Legacy | Legacy | Legacy |  |  |  |  |  |
| `llama3.1-8b` | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in European regions, without cross-region inference.

| Model | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS Europe West 2 (London) | Azure West Europe (Netherlands) |
| --- | --- | --- | --- | --- |
| `llama3-70b` | Legacy |  |  | Legacy |
| `llama3-8b` | Legacy |  |  | Legacy |
| `llama3.1-70b` | Legacy | Legacy |  | Legacy |
| `llama3.1-8b` | ✔ | ✔ |  | ✔ |

Expand

Show lessSee more

These models run natively in Asia-Pacific regions, without cross-region inference.

| Model | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) |
| --- | --- | --- |
| `llama3-70b` |  | Legacy |
| `llama3-8b` | Legacy | Legacy |
| `llama3.1-70b` | Legacy | Legacy |
| `llama3.1-8b` | ✔ | ✔ |

Expand

Show lessSee more

### Microsoft

Cross-regionNorth AmericaSouth AmericaEuropeAsia-Pacific

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `multilingual-e5-large` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ |
| `e5-base-v2` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ |  |

Expand

Show lessSee more

These models run natively in North American regions, without cross-region inference.

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | AWS US East 2 (Ohio) | AWS CA Central 1 (Central) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) | Azure West US 2 (Washington) | Google Cloud US Central 1 (Iowa) | Google Cloud US East 4 (N. Virginia) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `multilingual-e5-large` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ | ✔ | ✔ |
| `e5-base-v2` | ✔ | ✔ | ✔ |  |  | ✔ |  |  |  |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in South American regions, without cross-region inference.

| Model | AWS SA East 1 (São Paulo) |
| --- | --- |
| `multilingual-e5-large` | ✔ |

Expand

Show lessSee more

These models run natively in European regions, without cross-region inference.

| Model | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS Europe West 2 (London) | AWS Europe North 1 (Stockholm) | Azure West Europe (Netherlands) | Azure UK South (London) | Azure North Europe (Ireland) | Azure Switzerland North (Zürich) | Google Cloud Europe West 2 (London) | Google Cloud Europe West 4 (Netherlands) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `multilingual-e5-large` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `e5-base-v2` | ✔ |  |  |  | ✔ |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in Asia-Pacific regions, without cross-region inference.

| Model | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) | AWS AP South 1 (Mumbai) | AWS AP Southeast 3 (Jakarta) | Azure Central India (Pune) | Azure Japan East (Tokyo, Saitama) | Azure Southeast Asia (Singapore) | Azure Australia East (New South Wales) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `multilingual-e5-large` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `e5-base-v2` | ✔ | ✔ |  |  |  |  |  |  |

Expand

Show lessSee more

### Mistral AI

Cross-regionNorth AmericaEuropeAsia-Pacific

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `mistral-large2` | Legacy | Legacy | Legacy | Legacy |  |  | Legacy | Legacy | Legacy | Legacy | Legacy | Legacy |  | Legacy |  |
| `mistral-large3` | \* | \* | \* |  |  |  |  | \* | \* |  |  |  |  |  |  |
| `mixtral-8x7b` | Legacy | Legacy | Legacy | Legacy |  |  | Legacy | Legacy | Legacy | Legacy | Legacy | Legacy |  | Legacy |  |
| `mistral-7b` | Legacy | Legacy |  | Legacy |  |  |  | Legacy | Legacy | Legacy |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in North American regions, without cross-region inference.

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `mistral-large2` | Legacy | Legacy | Legacy | Legacy |  |  |  |  |  |
| `mixtral-8x7b` | Legacy | Legacy | Legacy | Legacy |  |  |  |  |  |
| `mistral-7b` | Legacy | Legacy | Legacy | Legacy |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in European regions, without cross-region inference.

| Model | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS Europe West 2 (London) | Azure West Europe (Netherlands) |
| --- | --- | --- | --- | --- |
| `mistral-large2` | Legacy | Legacy |  | Legacy |
| `mixtral-8x7b` | Legacy | Legacy |  | Legacy |
| `mistral-7b` | Legacy | Legacy |  | Legacy |

Expand

Show lessSee more

These models run natively in Asia-Pacific regions, without cross-region inference.

| Model | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) |
| --- | --- | --- |
| `mistral-large2` | Legacy | Legacy |
| `mixtral-8x7b` | Legacy | Legacy |
| `mistral-7b` | Legacy | Legacy |

Expand

Show lessSee more

### Moonshot AI

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kimi-k3` | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |  |

Expand

Show lessSee more

### NVIDIA

Cross-regionNorth America

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `nv-embed-qa-4` | ✔ | ✔ | ✔ |  |  |  |  |  |  |  |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in North American regions, without cross-region inference.

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `nv-embed-qa-4` | ✔ |  |  |  |  |  |  |  |  |

Expand

Show lessSee more

### OpenAI

Cross-regionNorth America

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openai-gpt-6.1-sol` | \* | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |
| `openai-gpt-6-astra` | ✔ | ✔ | ✔ |  |  |  |  |  |  |  |  |  |  |  |  |
| `openai-gpt-6-sol` | \* | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |
| `openai-gpt-6-luna` | \* | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |
| `openai-gpt-5.6-sol` | ✔ | ✔ | ✔ |  |  |  |  |  |  |  |  |  |  |  |  |
| `openai-gpt-5.6-terra` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |  |  |  |  |
| `openai-gpt-5.6-luna` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |  |  |  |  |
| `openai-gpt-5.5` | \*\* |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `openai-gpt-5.4` | ✔ |  |  | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ | ✔ | ✔ |  |
| `openai-gpt-5.4-mini` | ✔ |  |  |  |  |  |  |  |  |  | ✔ | ✔ |  | ✔ |  |
| `openai-gpt-5.4-nano` | ✔ |  |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |  |
| `openai-gpt-5.2` | ✔ |  |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |  |
| `openai-gpt-5.1` | ✔ |  |  |  |  |  |  |  |  |  | ✔ | ✔ |  | ✔ |  |
| `openai-gpt-5` | ✔ |  |  |  |  |  |  |  |  |  | ✔ | ✔ |  | ✔ |  |
| `openai-gpt-5-mini` | ✔ |  |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |  |
| `openai-gpt-5-nano` | ✔ |  |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |  |
| `openai-gpt-4.1` | Legacy |  |  |  |  |  |  |  |  |  | Legacy | Legacy |  |  |  |

Expand

Show lessSee more

These models run natively in North American regions, without cross-region inference.

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openai-gpt-4.1` |  |  |  | Legacy |  |  |  |  |  |

Expand

Show lessSee more

### Snowflake

Cross-regionNorth AmericaSouth AmericaEuropeAsia-Pacific

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `snowflake-decision-fast` | \*\* |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `snowflake-arctic-embed-l-v2.0-8k` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ |
| `snowflake-arctic-embed-m-v1.5` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ |
| `snowflake-arctic-embed-m` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ |

Expand

Show lessSee more

These models run natively in North American regions, without cross-region inference.

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | AWS US East 2 (Ohio) | AWS CA Central 1 (Central) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) | Azure West US 2 (Washington) | Google Cloud US Central 1 (Iowa) | Google Cloud US East 4 (N. Virginia) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `snowflake-arctic-embed-l-v2.0-8k` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m-v1.5` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  |  |  | ✔ | ✔ | ✔ | ✔ |

Expand

Show lessSee more

These models run natively in South American regions, without cross-region inference.

| Model | AWS SA East 1 (São Paulo) |
| --- | --- |
| `snowflake-arctic-embed-l-v2.0-8k` | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ |
| `snowflake-arctic-embed-m-v1.5` | ✔ |
| `snowflake-arctic-embed-m` | ✔ |

Expand

Show lessSee more

These models run natively in European regions, without cross-region inference.

| Model | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS Europe West 2 (London) | AWS Europe North 1 (Stockholm) | Azure West Europe (Netherlands) | Azure UK South (London) | Azure North Europe (Ireland) | Azure Switzerland North (Zürich) | Google Cloud Europe West 2 (London) | Google Cloud Europe West 4 (Netherlands) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `snowflake-arctic-embed-l-v2.0-8k` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m-v1.5` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

Expand

Show lessSee more

These models run natively in Asia-Pacific regions, without cross-region inference.

| Model | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) | AWS AP South 1 (Mumbai) | AWS AP Southeast 3 (Jakarta) | Azure Central India (Pune) | Azure Japan East (Tokyo, Saitama) | Azure Southeast Asia (Singapore) | Azure Australia East (New South Wales) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `snowflake-arctic-embed-l-v2.0-8k` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m-v1.5` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

Expand

Show lessSee more

### Voyage AI

Cross-regionNorth AmericaEuropeAsia-Pacific

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `voyage-multilingual-2` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  | ✔ |  |

Expand

Show lessSee more

These models run natively in North American regions, without cross-region inference.

| Model | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS US East (Commercial Gov - N. Virginia) | Azure East US 2 (Virginia) | Azure East US (Virginia) | Azure West US (Washington) | Azure West US 3 (Arizona) | Azure North Central US (Illinois) | Azure South Central US (Texas) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `voyage-multilingual-2` | ✔ | ✔ | ✔ | ✔ |  |  |  |  |  |

Expand

Show lessSee more

These models run natively in European regions, without cross-region inference.

| Model | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS Europe West 2 (London) | Azure West Europe (Netherlands) |
| --- | --- | --- | --- | --- |
| `voyage-multilingual-2` | ✔ | ✔ |  | ✔ |

Expand

Show lessSee more

These models run natively in Asia-Pacific regions, without cross-region inference.

| Model | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) |
| --- | --- | --- |
| `voyage-multilingual-2` | ✔ | ✔ |

Expand

Show lessSee more

### xAI

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `grok-4.7` | \* | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |
| `grok-4.6` | \* | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |

Expand

Show lessSee more

### Z.ai

| Model | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS JP (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region)† | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `glm-5.3` | \* | \* | \* |  |  |  |  |  |  |  |  |  |  |  |  |

Expand

Show lessSee more
