# Sep 02, 2026: Data lineage for streams

You can now see [streams](/user-guide/streams-intro) on Snowflake [data lineage](/user-guide/ui-snowsight-lineage)
graphs.

On the object-level lineage graph, a stream appears as a node. Edges go into the stream from the objects it was created
from, and edges go out of the stream to objects created from it. On the column lineage graph, a stream isn’t shown as a
node. It appears as an edge property (`streamName`) on the relationship between the source and target objects.

This feature requires Enterprise Edition (or higher).

For more information, see [Streams on the data lineage graph](/user-guide/lineage-streams).
