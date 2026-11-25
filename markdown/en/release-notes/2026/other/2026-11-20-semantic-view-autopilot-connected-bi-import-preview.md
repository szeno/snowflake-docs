# Nov 20, 2026: Semantic View Autopilot import from Horizon Catalog connectors (*Preview*)

Semantic View Autopilot can create a semantic view directly from a model that a Horizon Catalog connector ingests. You
don’t need to export or upload a file: Autopilot reads the model’s tables, relationships, measures, and calculated
fields from Horizon Catalog and converts them into a semantic view. Connectors for Tableau and Power BI are supported.

You can start an import in the following ways:

- In Semantic View Autopilot, select your BI tool, and then select a model from your connectors.
- On the **Metadata connections** list in Horizon Catalog, select **Import with Cortex** for a connector.
- On the page for a model in Horizon Catalog, or on its node in a lineage graph, select **Create semantic view**.

This feature is in preview and is available to all accounts in AWS deployments.

For more information, see
[Create a semantic view from a Horizon Catalog connector](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-connected-bi).
