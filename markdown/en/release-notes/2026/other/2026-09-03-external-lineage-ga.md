# Sep 03, 2026: External lineage (*General availability*)

[External lineage](/user-guide/external-lineage) is now generally available and is no longer in
[Preview](/release-notes/preview-features).

External lineage extends Snowflake’s [native lineage](/user-guide/ui-snowsight-lineage) to include data sources and
destinations outside Snowflake, giving you visibility into data flows across your entire data ecosystem. It uses the
[OpenLineage](https://openlineage.io) standard: tools such as dbt and Apache Airflow send OpenLineage events to a
Snowflake REST endpoint, and Snowflake incorporates them into the lineage it already tracks.

With external lineage, you can do the following:

- Send COMPLETE OpenLineage events to the `/api/v2/lineage/external-lineage` endpoint to establish lineage, either from a
  data tool with an OpenLineage integration or by sending the request yourself. See
  [Configure your data tool](/user-guide/external-lineage#label-external-lineage-configure).
- Capture lineage between two objects outside Snowflake, so a pipeline that moves data through several external systems
  appears as a connected chain even where no Snowflake object sits between them.
- Capture lineage between individual columns using the `columnLineage` facet, in addition to lineage between objects. See
  [Payload requirements](/user-guide/external-lineage#label-external-lineage-configure-manual-payload).
- View external objects in the lineage graph in Snowsight, where they’re labeled as external nodes.
- Query external lineage with SQL. External objects appear in the output of
  [GET\_LINEAGE](/sql-reference/functions/get_lineage-snowflake-core), and you can retrieve the lineage of an external
  object by anchoring the query on it. See
  [Lineage for objects outside Snowflake](/sql-reference/functions/get_lineage-snowflake-core#label-get-lineage-external-objects).
- Remove lineage with a DELETE request to the same endpoint. See
  [Send requests to remove lineage](/user-guide/external-lineage#label-external-lineage-remove).

External lineage requires Enterprise Edition (or higher). Sending lineage requires the `INGEST LINEAGE` privilege on the
account, and removing lineage requires the `DELETE LINEAGE` privilege. See
[Grant Snowflake privileges](/user-guide/external-lineage#label-external-lineage-privilege).

For more information, see [External lineage](/user-guide/external-lineage).
