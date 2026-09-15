# Nov 07, 2025: AI\_REDACT function (*Preview*)

The AI\_REDACT function is now available in preview. This managed function detects and redacts personally identifiable
information (PII) from unstructured text data using a large language model (LLM). AI\_REDACT automatically recognizes
various categories of PII (name, address, and so on, including subcategories such as first or last name) and replaces
them with placeholder values.

For example, passing the following string to AI\_REDACT:

> “John Smith’s email is [jsmith@example.com](mailto:jsmith@example.com) and he lives in San Francisco.”

Results in the following output:

> “[NAME]’s email is [EMAIL] and he lives in [ADDRESS].”

For more information, see [Detect and redact personally identifiable information (PII)](/user-guide/snowflake-cortex/redact-pii) and [AI\_REDACT](/sql-reference/functions/ai_redact).
