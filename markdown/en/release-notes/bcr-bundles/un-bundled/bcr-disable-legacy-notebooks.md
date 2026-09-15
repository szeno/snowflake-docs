# Disable Legacy Notebook creations

Starting September 1, 2026, Snowflake will disable the ability to create new Legacy Notebooks. Existing Legacy
Notebooks will remain fully functional until the next behavioral change (planned for November 2026).

Customers are encouraged to start migrating from Legacy Notebooks to the new Notebooks in Workspaces experience
using the [Migration Flow](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-migrate).
With Notebooks in Workspaces, users enjoy the benefits of full Jupyter compatibility, integrated Cortex Code flows,
organizing notebooks alongside other files (`.sql`, `.py`, `.csv`, and others) in folders, streamlined Container
Runtime updates with managed CPU/GPU compute infrastructure, and easy collaboration through shared or Git-backed
workspaces. This is part of a broader effort to unify all Snowsight authoring inside of Workspaces (for example,
the [Worksheets migration to Workspaces](/release-notes/bcr-bundles/un-bundled/bcr-2117)).

## Timeline

### September 1, 2026

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

### November 2026

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

Ref: 2307
