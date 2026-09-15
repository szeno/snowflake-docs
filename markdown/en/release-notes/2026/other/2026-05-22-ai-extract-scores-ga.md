# May 22, 2026: AI\_EXTRACT extraction scores (*General availability*)

Extraction scores for the Snowflake Cortex AI\_EXTRACT function are now generally available. Key capabilities include:

- **Confidence scores for extracted values:** Pass `scores => TRUE` in an AI\_EXTRACT call to get back a `scoring`
  object alongside the standard `response` object, with a score between 0 and 1 indicating the model’s certainty
  about each extracted value.
- **Support for entities, lists, and tables:** Per-field scores are returned for entity extraction, and aggregate
  scores are returned for list and table extraction.
- **Support for fine-tuned arctic-extract models:** Extraction scores work with
  [fine-tuned](/user-guide/snowflake-cortex/arctic-extract-finetuning) arctic-extract models in addition to the
  default model.
- **Human-in-the-loop workflows:** Use scores to set thresholds and flag low-scoring extractions for human
  review, and to build fallback mechanisms for unreliable extractions.
- **No additional cost:** Requesting scores does not incur additional cost beyond the standard AI\_EXTRACT call.

For more information, see [Extraction scores](/sql-reference/functions/ai_extract#label-ai-extract-scores).
