Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view

This Account Usage view provides a historical record of pipeline errors, enabling users to monitor performance trends. This view displays key metrics such as processed data volume, error rates, and latency.

You can use this Account Usage view to query the error history for a specific pipe or channel.

Note

The SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view only applies to [Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ACCOUNT\_ID | NUMBER | The ID of the Snowflake account. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the rowset channel history was created. |
| CHANNEL\_ID | NUMBER | The internal, system-generated ID of the Snowpipe Streaming channel. |
| CHANNEL\_NAME | VARCHAR | The user-defined name of the Snowpipe Streaming channel. |
| PIPE\_ID | NUMBER | The internal ID of the Snowpipe object associated with this Snowpipe Streaming channel. |
| END\_OFFSET | VARCHAR | The last offset token processed and included in this specific channel history record. |
| TABLE\_ID | NUMBER | The internal ID of the target table for this Snowpipe Streaming channel. |
| TABLE\_NAME | VARCHAR | The name of the target table for this Snowpipe Streaming channel. |
| TABLE\_SCHEMA\_ID | NUMBER | The internal ID of the schema containing the target table. |
| TABLE\_SCHEMA\_NAME | VARCHAR | The name of the schema containing the target table. |
| TABLE\_DATABASE\_ID | NUMBER | The internal ID of the database containing the target table. |
| TABLE\_DATABASE\_NAME | VARCHAR | The name of the database containing the target table. |
| PIPE\_NAME | VARCHAR | “The name of the Snowpipe object associated with the current Snowpipe Streaming channel history entry. |
|  |  |  |
| Named pipes: The value is the user-defined name of the Snowpipe object associated with the channel. |  |  |
|  |  |  |
| Default pipe: The value is automatically derived from the target table name; for example, MY\_TABLE-STREAMING.” |  |  |
| PIPE\_SCHEMA\_ID | NUMBER | “The internal identifier for the schema associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the internal ID of the schema that contains the user-defined Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the internal ID of the schema that contains the target table.” |  |  |
| PIPE\_SCHEMA\_NAME | VARCHAR | “The name of the schema associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the user-defined name of the schema that contains the Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the name of the schema that contains the target table.” |  |  |
| PIPE\_DATABASE\_ID | NUMBER | “The internal identifier for the database associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the internal ID of the database that contains the user-defined Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the internal ID of the database that contains the target table.” |  |  |
| PIPE\_DATABASE\_NAME | VARCHAR | “The name of the database associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the user-defined name of the database that contains the Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the name of the database that contains the target table.” |  |  |
| LAST\_ERROR\_OFFSET\_UPPER\_BOUND | VARCHAR | The upper bound of the offset token range of the last rowset that encountered errors during this historical period. |
| LAST\_ERROR\_MESSAGE | VARCHAR | The last error message encountered while writing data to the channel. This column displays a redacted error message when an error is encountered. |
| SNOWFLAKE\_PROCESSING\_LATENCY\_MS | NUMBER | The average latency, in milliseconds, observed by the Snowflake service in processing rowsets for this channel during this historical period. |
| ROWS\_INSERTED | NUMBER | The total number of rows successfully inserted through this channel during this historical period. |
| ROWS\_PARSED | NUMBER | The total number of rows parsed (processed) by the channel during this historical period. |
| ROW\_ERROR\_COUNT | NUMBER | The total number of rows that encountered errors and were not inserted through this channel during this historical period. |

Expand

Show lessSee more

## Usage notes

- The Snowpipe Streaming high-performance architecture only supports ON\_ERROR=CONTINUE. Other ON\_ERROR options are not supported.
