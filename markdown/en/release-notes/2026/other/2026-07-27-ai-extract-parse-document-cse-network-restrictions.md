# Jul 27, 2026: AI\_EXTRACT and AI\_PARSE\_DOCUMENT support for client-side encrypted stages and network-restricted accounts (*Preview*)

With this preview release, AI\_EXTRACT and AI\_PARSE\_DOCUMENT support documents stored on stages that use client-side or
server-side encryption, including in accounts that use PrivateLink or other network policies that restrict public
network access to stages.

Key capabilities include:

- **Client-side encrypted stages:** Process documents from stages that use client-side encryption, including files on
  external stages that use client-side encryption configured in Snowflake. Server-side encrypted stages are already supported.
- **Network-restricted accounts:** Use these functions in accounts that use PrivateLink or other network policies that
  restrict public network access to stages.

For more information, see the following topics:

- [AI\_EXTRACT](/sql-reference/functions/ai_extract)
- [Extracting information from documents with AI\_EXTRACT](/user-guide/snowflake-cortex/document-extraction)
- [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document)
