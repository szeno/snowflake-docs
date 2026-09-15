# Apr 30, 2026: AI\_PARSE\_DOCUMENT increased page limit to 2,000 pages

The Snowflake Cortex AI\_PARSE\_DOCUMENT function now supports processing documents of up to 2,000 pages in both LAYOUT
and OCR modes, enabling organizations to efficiently handle large, multi-page documents such as healthcare records,
insurance claims, regulatory filings, and technical manuals in a single request with reduced pre-processing and
orchestration.

Key improvements include:

- **Expanded document size support:** Process documents up to 2,000 pages, a significant increase from previous limits,
  reducing the need to split large files before processing.
- **Improved workflow efficiency:** Minimize pre-processing steps by handling large documents in a single call,
  simplifying pipelines and reducing operational overhead.
- **Consistent performance across modes:** Both LAYOUT and OCR modes now support large-scale documents, enabling
  flexibility across a wider range of use cases.

LAYOUT mode remains the preferred choice for most use cases, especially for complex documents and layout-aware
extraction, while OCR mode is optimized for fast, high-quality text extraction from scanned and text-heavy documents.

For more information, see [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document).
