# Disable Legacy Notebook creations

Important

**Updated timeline:** Based on customer feedback and regional compute availability constraints that are more
widespread than expected, Snowflake is extending the Legacy Notebooks deprecation timeline to give customers more
time to migrate. Creation of new Legacy Notebooks is now disabled on **April 30, 2027**, and full deprecation follows
on **May 31, 2027**. These dates replace the earlier ones (September 1, 2026 and November 2026).

Starting April 30, 2027, Snowflake will disable the ability to create new Legacy Notebooks. Existing Legacy
Notebooks will remain fully functional until May 31, 2027.

Note

If your account had no Legacy Notebook activity in the 60 days before November 1, 2026, you already can’t create
new Legacy Notebooks. Existing Legacy Notebooks in these accounts follow the timeline below.

Customers are encouraged to start migrating from Legacy Notebooks to the new Notebooks in Workspaces experience
using the [Migration Flow](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-migrate).
With Notebooks in Workspaces, users enjoy the benefits of full Jupyter compatibility, integrated Cortex Code flows,
organizing notebooks alongside other files (`.sql`, `.py`, `.csv`, and others) in folders, streamlined Container
Runtime updates with managed CPU/GPU compute infrastructure, and easy collaboration through shared or Git-backed
workspaces. This is part of a broader effort to unify all Snowsight authoring inside of Workspaces (for example,
the [Worksheets migration to Workspaces](/release-notes/bcr-bundles/un-bundled/bcr-2117)).

## Recommendation: Use ARM-based compute pools on AWS and Google Cloud

Notebooks in Workspaces run on Snowpark Container Services compute pools. If your account is on AWS or Google Cloud,
we recommend creating compute pools that use ARM-based instance families. ARM instances generally have more capacity
available, which helps your notebooks start reliably. To see which instance families exist in your region, run
[SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families) or see
[Snowpark Container Services: Understanding instance families](/developer-guide/snowpark-container-services/instance-families).

If your workloads depend on x86-only packages or binaries, check that they work on ARM before you switch.

## Timeline

### April 30, 2027

- New Legacy Notebooks can no longer be created. This applies to:
  - Creation paths in Snowsight.
  - The SQL command `CREATE OR REPLACE NOTEBOOK`. All scripts and pipelines that use
    `CREATE OR REPLACE NOTEBOOK` need to be modified to use
    [CREATE OR REPLACE NOTEBOOK PROJECT](/sql-reference/sql/create-notebook-project) instead.
- Users can continue to view, edit, run, and export existing Legacy Notebooks and use the
  [Migration Flow](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-migrate).
- [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) still works for existing Legacy Notebooks.
- Snowflake will provide fixes for issues within the platform that cause existing production notebooks to lose
  functionality. Changes outside of those fixes won’t be patched.

### May 31, 2027

- All Legacy Notebooks can no longer be executed or edited (both in Snowsight and through SQL).
- All scheduled notebooks, Snowflake Tasks, or custom pipelines that use EXECUTE NOTEBOOK stop working.
- Users can continue to view and open Legacy Notebook objects from the Legacy Notebooks page.
- Users can continue to use the
  [Migration Flow](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-migrate).
- Users can continue to export `.ipynb` files.

To review the key differences between Legacy and new Notebooks, start with migrations, or read the best practices,
see [Migrating legacy notebooks to Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-migrate).

Contact your account team if you have questions or migration blockers.

## See also

- [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)
- [Working with workspaces](/user-guide/ui-snowsight/workspaces-working)
- [Best practices for shared workspaces](/user-guide/ui-snowsight/workspaces-shared-best-practices)
- [Snowpark Container Services: Understanding instance families](/developer-guide/snowpark-container-services/instance-families)

Ref: 2307
