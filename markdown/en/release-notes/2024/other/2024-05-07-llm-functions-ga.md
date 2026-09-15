# May 07, 2024 — Cortex LLM Functions — *General Availability*

With this release, we are pleased to announce the general availability of LLM Functions. LLM Functions gives you instant access
to industry-leading large language models (LLMs), including
[Snowflake Arctic](https://www.snowflake.com/blog/arctic-open-efficient-foundation-language-models-snowflake/),
an open enterprise-grade model developed by Snowflake.

The available functions include:

- COMPLETE: Given a prompt, returns a response that completes the prompt. This function accepts either a single prompt
  or a conversation with multiple prompts and responses.
- EXTRACT\_ANSWER: Given a question and unstructured data, returns the answer to the question if it can be found in the
  data.
- SENTIMENT: Returns a sentiment score, from -1 to 1, representing the detected positive or negative sentiment of the
  given text.
- SUMMARIZE: Summarizes the given text.
- TRANSLATE: Translates the given text from any supported language to any other.

With this GA release, Cortex LLM Functions will be made available to all accounts. For immediate access, see the
[LLM Functions required privileges section](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for instructions on adding the CORTEX\_USER role
to your user roles. Over the next two weeks (5/7/2024-5/21/2024), the CORTEX\_USER role will be added to the PUBLIC role.

For more information, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql).
