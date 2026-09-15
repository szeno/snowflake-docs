# Oct 16, 2025: AI\_EXTRACT function (*General availability*)

The Snowflake AI\_EXTRACT function lets you extract information from text or document files using large language models.

This release adds the following features to the existing AI\_EXTRACT capabilities:

- **Table extraction support:** Extract tabular data from documents, which helps you analyze financial reports, data sheets, invoices, and other documents that contain tabular data.
- **Flexible response formats:** Define the response format using simple object schemas, arrays of questions, or JSON schemas that support both entity and table extraction.
- **Contextual guidance:** Provide context to the model using the optional `description` field; for example, to help the model localize the correct table in a document.
- **Output length:** The maximum output length for entity extraction is 512 tokens per question. For table extraction, the model returns answers that are a maximum of 4096 tokens long.

For more information, see [AI\_EXTRACT](/sql-reference/functions/ai_extract).
