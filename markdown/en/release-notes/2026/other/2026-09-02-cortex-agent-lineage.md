# Sep 02, 2026: Data lineage for Cortex Agents

You can now use data lineage to see which data a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) can reach
through the tools declared in its specification. A semantic view that a Cortex Analyst tool references, and a Cortex
Search service that a Cortex Search tool references, both appear upstream of the agent. Because a semantic view is
itself downstream of the tables it references, you can trace the whole path from a table, through the semantic view, to
the agent that consumes it.

Snowflake records these relationships when you create an agent or commit a new version, so an agent whose most recent
version was committed before this change doesn’t appear in lineage until you commit a new version.

For more information about using data lineage, see [Data Lineage](/user-guide/ui-snowsight-lineage).
