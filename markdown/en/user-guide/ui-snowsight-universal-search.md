# Search for objects with Universal Search

With Universal Search, you can find objects in your account, data products available to you in the Snowflake Marketplace,
relevant Snowflake Documentation topics, and relevant Snowflake Community Knowledge Base articles, all from the [Snowsight home page](/user-guide/ui-snowsight-homepage).

Universal Search understands your query and information about your database objects and can find objects with names that differ from
your search terms. Even if you misspell or type only part of your search term, you can still see useful results.

When you use Universal Search, you can use natural language to describe what you’re looking for. For example, you can use keyword search
terms, like “opportunities” or “sales opportunities”, or use more conversational natural language search terms, like
“sales opportunities that are likely to close” or “which opportunities came from partner referrals”.

![](/static/images/screens/ui-snowsight-universal-search-results.png)

For example, if you search for “zip codes”, Universal Search returns results such as listings on the Snowflake Marketplace that mention postal
code data and a table with the column name `postal_code`.

To make it easier to find the right data for your project, object metadata such as names, comments, and tags for objects and columns
are searched. Universal Search searches only the object metadata, not the contents of your database objects.

## Search for objects in Snowsight

When you search for objects in Snowsight, the results displayed are based on the privileges of your currently active role and any
secondary roles.

To search, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Enter search terms in the home page search window.

   If you’re not on the home page, select **Search** and then enter search terms.
3. Press the **return** or **enter** key to execute the search.

   Results are displayed in categories. If a category isn’t displayed, there are no results for that category or your currently active role
   doesn’t have access to those results.
4. Select a search result to view details. For a database object, you can select **Open in Worksheets** to query the object in a worksheet.

To get or purchase listings offered on the Snowflake Marketplace that appear in the results, you must have agreed to the Snowflake Provider
and Consumer Terms. See
[Legal requirements for providers and consumers of listings](/collaboration/collaboration-listings-legal).

## Supported object types

Universal Search returns results for:

- Tables & views (including standard, Apache Iceberg™, dynamic, and hybrid)
- Workspace files
- Legacy worksheets & dashboards
- Legacy notebooks
- Streamlits
- Semantic views
- Agents
- ML models
- Streams, tasks, pipes, and stages
- Installed applications
- Application packages
- Databases & schemas
- User-defined functions (UDFs) & stored procedures
- Feature views
- Data products in the Snowflake Marketplace
- Data products in your Internal Marketplace
- Documentation pages on <https://docs.snowflake.com> and <https://other-docs.snowflake.com>
- Knowledge Base articles on <https://community.snowflake.com/>

## Limitations and considerations

- Universal Search is optimized for search terms in English.
- Indexed workspace file contents are encrypted at rest, but not yet [Tri-Secret Secure](/user-guide/security-encryption-tss)-compatible.
  You can use the [`ENABLE_WORKSPACE_FILE_CONTENT_SEARCH`](/sql-reference/parameters#enable_workspace_file_content_search) parameter to control
  whether to index workspace file content.
- New objects can take up to a few hours after they are created to appear in search results. Existing objects that are dropped and recreated,
  such as by scheduled tasks or automated pipelines, can disappear from search results for up to a few hours until the recreated objects are
  indexed.
