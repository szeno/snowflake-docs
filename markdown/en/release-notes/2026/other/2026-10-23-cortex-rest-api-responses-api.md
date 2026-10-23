# Oct 23, 2026: Responses API for the Cortex REST API (*Preview*)

You can now call OpenAI models through the OpenAI-compatible Responses API, in preview. Send requests to
`/api/v2/cortex/v1/responses` on the Cortex REST API, or to `/v1/responses` on the Cortex AI Gateway, with the
OpenAI SDK or any other client that uses the Responses API.

The API doesn’t keep conversation state, so send the full conversation with each request. `previous_response_id`
and background mode aren’t supported.

For more information, see [Responses API reference](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-responses-reference)
and [Inference with Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/inference).
