# May 13, 2026: AI\_CLASSIFY now supports document classification (*Public Preview*)

The Snowflake Cortex [AI\_CLASSIFY](/sql-reference/functions/ai_classify) function now accepts documents as
input, enabling organizations to automatically categorize document files like PDF, DOCX, CSV, and more using
simple SQL. This allows teams to easily streamline document intake and intelligently route content, such as
contracts, invoices, and various reports, into the right downstream workflows.

Extending classification to documents enables:

- **Reduced operational overhead** by eliminating the need for manual triaging.
- **Intelligent document routing** by seamlessly classifying documents upfront to route only relevant types
  into downstream processing. For example, sending invoices to AI\_EXTRACT and contracts to AI\_PARSE\_DOCUMENT.
- **High-quality classification at scale** by delivering accurate, consistent categorization across
  high-volume document workloads.

Supported formats: `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.html`, `.csv`, `.txt`, up to 100 pages per
document. The function signature and pricing are unchanged.

For more information, see [AI\_CLASSIFY](/sql-reference/functions/ai_classify).
