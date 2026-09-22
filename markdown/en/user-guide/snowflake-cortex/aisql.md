# Snowflake Cortex AI Functions (including LLM functions)

Regional Availability

Available to accounts in [select regions](/user-guide/snowflake-cortex/aisql-regional-availability).

Some individual Cortex AI Functions are [Preview Features](/release-notes/preview-features). Check
the status of each function before using it in production. Functions not marked as preview features are generally
available (GA) and can be used in production.

Use Cortex AI Functions in Snowflake to run unstructured analytics on text and images with industry-leading LLMs from OpenAI, Anthropic, Meta, Mistral AI, and DeepSeek.
AI Functions support use cases such as:

- Extracting entities to enrich metadata and streamline validation
- Aggregating insights across customer tickets
- Filtering and classifying content by natural language
- Sentiment and aspect-based analysis for service improvement
- Translating and localizing multilingual content
- Parsing documents for analytics and RAG pipelines

All the LLMs that Snowflake provides access to via our Snowflake AI Features are deployed within the Snowflake Service perimeter.

## Available functions

Snowflake Cortex features are provided as SQL functions and are also available [in Python](/user-guide/snowflake-cortex/aisql-programmatic-use).
To call any of these functions, your role needs the USE AI FUNCTIONS account-level privilege and one of the
CORTEX\_USER or AI\_FUNCTIONS\_USER database roles. For details, see
[Privileges and model access for Cortex AI Functions](/user-guide/snowflake-cortex/aisql-privileges-and-access).

Cortex AI Functions can be grouped into the following categories:

- [Cortex AI functions](#label-cortex-llm-ai-function)
- [Helper functions](#label-cortex-llm-helper-functions)

### Cortex AI functions

These task-specific functions are purpose-built managed functions that automate routine tasks, like simple summaries and
quick translations, that don’t require any customization.

- [AI\_COMPLETE](/sql-reference/functions/ai_complete): Generates a completion for a given text string or image using a selected LLM. Use this function for most generative AI tasks.
- [AI\_CLASSIFY](/sql-reference/functions/ai_classify): Classifies text or images into user-defined categories.
- [AI\_FILTER](/sql-reference/functions/ai_filter): Returns True or False for a given text or image input, allowing you to filter results in *SELECT*, *WHERE*, or *JOIN … ON* clauses.
- [AI\_AGG](/sql-reference/functions/ai_agg): Aggregates a text column and returns insights across multiple rows based on a user-defined prompt. This function isn’t subject to context window limitations.
- [AI\_EMBED](/sql-reference/functions/ai_embed): Generates an embedding vector for a text or image input, which can be used for similarity search, clustering, and classification tasks.
- [AI\_MULTI\_EMBED](/sql-reference/functions/ai_multi_embed): Creates multimodal embeddings from text, images, audio, or video, returning one or more vectors with segment metadata for semantic search across modalities.
- [AI\_EXTRACT](/sql-reference/functions/ai_extract): Extracts information from an input string or file, for example, text, images, and documents. Supports multiple languages.
- [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment): Extracts sentiment from text.
- [AI\_SUMMARIZE](/sql-reference/functions/ai_summarize): Automatically summarizes text, images, and documents, identifying key themes, facts, and relationships across multimodal content.
- [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg): Aggregates a text column and returns a summary across multiple rows. This function isn’t subject to context window limitations.
- [AI\_SIMILARITY](/sql-reference/functions/ai_similarity): Calculates the embedding similarity between two inputs.
- [AI\_TRANSCRIBE](/sql-reference/functions/ai_transcribe): Transcribes audio and video files stored in a stage, extracting text, timestamps, and speaker information.
- [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document): Extracts text (using OCR mode) or text with layout information
  (using LAYOUT mode) from documents in an internal or external stage. Can also extract images found in a document.
- [AI\_REDACT](/sql-reference/functions/ai_redact): Redact personally identifiable information (PII) from text.
- [AI\_TRANSLATE](/sql-reference/functions/ai_translate): Translates text between supported languages.

### Helper functions

Helper functions are purpose-built managed functions that reduce cases of failures when running other Cortex AI Functions, for example by
getting the count of tokens in an input prompt to ensure the call doesn’t exceed a model limit.

- [TO\_FILE](/sql-reference/functions/to_file): Creates a reference to a file in an internal or external stage for use with
  AI\_COMPLETE and other functions that accept files.
- [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens): Given an input text, returns the token count based on the model or Cortex
  function specified.
- [PROMPT](/sql-reference/functions/prompt): Helps you build prompt objects for use with AI\_COMPLETE and other functions.

## Performance considerations

Cortex AI Functions are optimized for throughput. We recommend using these functions to process numerous inputs such as text from large SQL tables. Batch processing is typically better suited for AI Functions. For more interactive use cases where latency is important, use the REST API. These are available for simple inference (Complete API), embedding (Embed API) and agentic applications (Agents API).

## Legal notices

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
