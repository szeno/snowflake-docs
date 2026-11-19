# Nov 18, 2026: AI\_EXTRACT citations (*Preview*)

Snowflake Cortex AI\_EXTRACT now supports citations that connect extracted values to supporting content in source documents and text. This addition makes it easier to verify extraction results, review information in context, and build applications that display source evidence alongside extracted fields.

Key capabilities include:

- **Document citations:** Identify supporting content using page numbers and bounding boxes, enabling applications to highlight the relevant regions in source documents.
- **Text citations:** Locate supporting passages using start and end offsets in the input text, enabling applications to display the source text associated with an extracted value.
- **Citations with extraction scores:** Request citations alongside extraction scores to help prioritize results for review and inspect the supporting source content.
- **Integration with existing SQL workflows:** Enable citations by setting `citation => TRUE` in an AI\_EXTRACT call. Citations are returned in a `citations` object alongside the extracted values, with no separate function call required.

For more information, see [Extract information with citations](/user-guide/snowflake-cortex/document-extraction#label-ai-extract-extract-with-citations) in the AI\_EXTRACT user guide and [Citations](/sql-reference/functions/ai_extract#label-ai-extract-citations) in the AI\_EXTRACT SQL reference.
