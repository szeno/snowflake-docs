# Nov 10, 2026: AI\_EXTRACT and AI\_PARSE\_DOCUMENT now support page filtering with FL\_FILTER\_PAGES

AI\_EXTRACT and AI\_PARSE\_DOCUMENT now support selecting document pages with FL\_FILTER\_PAGES. Process the pages relevant to your task directly in SQL, without creating separate files for each document section.

Use FL\_FILTER\_PAGES as the file argument to select individual pages, multiple page ranges, or pages relative to the end of a document. For example, extract signatory details from the last three pages of a contract or parse only the summary section of a report. You can also supply page ranges from a column to select different pages for each document in a batch.

For syntax and examples, see [FL\_FILTER\_PAGES](/sql-reference/functions/fl_filter_pages).
