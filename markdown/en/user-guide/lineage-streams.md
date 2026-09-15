# Streams on the data lineage graph

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Overview

Data lineage lets you trace how data flows between objects in your account. Streams weren’t previously shown as nodes on
the lineage graph because of the complexity of representing them. Snowflake now surfaces streams on lineage graphs,
with the limitations described in this topic.

## Streams as object nodes

On the object-level lineage graph, a stream appears as a node. Edges go into the stream node from the objects it was
created from, and edges go out of the stream node to objects created from it.

## Streams as edge properties for columns

Streams behave differently from other Snowflake objects: they don’t have columns in the same way tables and views do.
That makes column dependencies hard to capture for streams.

For that reason, Snowflake doesn’t show streams as nodes on the column lineage graph. A stream appears as an edge
property instead.

For example, consider a table `T`, a stream `S` created on `T`, and a view `V` that reads from `S`:

- On the object-level lineage graph, Snowflake shows `T` » `S` » `V`.
- On the column lineage graph, Snowflake shows `T` » `V`, with the edge labeled to indicate that stream `S` is an
  intermediate object.

The label is the stream’s fully qualified name in the `streamName` field. For example, if the stream is in database
`Db` and schema `Sc`, the edge shows `Db.Sc.S` for `streamName`.
