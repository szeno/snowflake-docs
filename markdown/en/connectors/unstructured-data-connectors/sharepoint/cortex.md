# Query the Cortex Search service with Snowflake Connector for SharePoint

[Preview Feature](/release-notes/preview-features) — Open

Support for this feature is available to accounts in most Snowflake regions. See [Regional availability](/connectors/unstructured-data-connectors/sharepoint/about#label-sharepoint-regional-availability) for a full list of regions.

Note

The Snowflake Connector for SharePoint is subject to the [Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Important

Thank you for your interest in the Snowflake Connector for SharePoint.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements is not guaranteed. The new solution is available as [Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/about) and
includes better performance, customizability, and enhanced deployment options.

You can use the [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) service to build chat
and search applications to chat with or query your documents in SharePoint.

After you install and configure the Snowflake Connector for SharePoint and it begins
ingesting content from Sharepoint, you can query the Cortex Search service.
For more information about using Cortex Search, see [Query a Cortex Search service](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service).

## Filter responses

To restrict responses from the Cortex Search service to documents that a specific user
has access to in SharePoint, you can specify a filter containing the user ID or email address of the user
when you query Cortex Search. For example, `filter.@contains.user_ids` or `filter.@contains.user_emails`.
The name of the Cortex Search service created by the connector is `search_service` in the schema `Cortex`.

Run the following SQL code in a SQL worksheet to query
the Cortex Search service with files ingested from your SharePoint site.

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
- `user_emailID`: Email ID of the user who you want to filter the responses for.
- `your_question`: The question that you want to get responses for.
- `number_of_results`: Maximum number of results to return in the response. The maximum value is 1000 and the default value is 10.

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    '<application_instance_name>.cortex.search_service',
      '{
        "query": "<your_question>",
         "columns": ["chunk", "web_url"],
         "filter": {"@contains": {"user_emails": "<user_emailID>"} },
         "limit": <number_of_results>
       }'
   )
)['results'] AS results
```

Here’s a complete list of values that you can enter for `columns`:

| Column name | Type | Description |
| --- | --- | --- |
| `full_name` | String | A full path to the file from the Sharepoint site documents root. Example: `folder_1/folder_2/file_name.pdf`. |
| `web_url` | String | A URL that displays an original Sharepoint file in a browser. |
| `last_modified_date_time` | String | Date and time when the item was most recently modified. |
| `chunk` | String | A piece of text from the document that matched the Cortex Search query. |
| `user_ids` | Array | An array of Microsoft 365 user IDs that have access to the document. It also includes user IDs from all the Microsoft 365 groups that are assigned to the document. To find a specific user ID, see [Get a user](https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http). |
| `user_emails` | Array | An array of Microsoft 365 user email IDs that have access to the document. It also includes user email IDs from all the Microsoft 365 groups that are assigned to the document. |

Expand

Show lessSee more

## Example: Query an AI assistant for human resources (HR) information

You can use Cortex Search to query an AI assistant for employees to chat with the latest versions of
HR information, such as onboarding, code of conduct, team processes, and organization policies.
Using response filters, you can also allow HR team members to query employee contracts while adhering to access controls configured in SharePoint.

PythonREST API

Run the following code in a [Python worksheet](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create) to query the
Cortex Search service with files ingested from SharePoint.
Ensure that you add the `snowflake.core` package to your database.

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
- `user_emailID`: Email ID of the user who you want to filter the responses for.

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.core import Root

def main(session: snowpark.Session):

   root = Root(session)

   # fetch service
   my_service = (root
     .databases["<application_instance_name>"]
     .schemas["cortex"]
     .cortex_search_services["search_service"]
   )

   # query service
   resp = my_service.search(
     query="What is my vacation carry over policy?",
     columns = ["chunk", "web_url"],
     filter = {"@contains": {"user_emails": "<user_emailID>"} },
     limit=1
   )
   return (resp.to_json())
```

Execute the following code in a command-line interface to query the Cortex Search
service with files ingested from your SharePoint.
You will need to authentication through key pair authentication and OAuth to access the
Snowflake REST APIs. For more information,
see [REST API](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service#label-cortex-search-query-syntax-rest)
and [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
- `account_url`: Your Snowflake account URL. For instructions on finding your account URL, see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).

Copy code

```
curl --location "https://<account_url>/api/v2/databases/<application_instance_name>/schemas/cortex/cortex-search-services/search_service" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer <CORTEX_SEARCH_JWT>" \
     --data '{
         "query": "What is my vacation carry over policy?",
         "columns": ["chunk", "web_url"],
         "limit": 1
     }'
```

Sample response:

```
{
  "results" : [ {
  "web_url" : "https://<domain>.sharepoint.com/sites/<site_name>/<path_to_file>",
  "chunk" : "Answer to the question asked."
  } ]
}
```

## Next steps

[Manage the Snowflake Connector for SharePoint](/connectors/unstructured-data-connectors/sharepoint/manage).
