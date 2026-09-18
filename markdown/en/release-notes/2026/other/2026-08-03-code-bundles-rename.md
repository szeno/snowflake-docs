# Aug 03, 2026: Notebook Project Objects are now Code Bundles

Notebook Project Objects have been renamed to **Code Bundles**. The object, its behavior, and its access model are unchanged: only the name and the corresponding SQL, CLI, and Snowsight labels are updated. Existing objects are recognized as Code Bundles automatically, with no migration required.

The `NOTEBOOK PROJECT` SQL grammar continues to work as an alias for `CODE BUNDLE`, and `EXECUTE NOTEBOOK PROJECT` is supported indefinitely, so your existing tasks and schedules keep running without changes.

For more information, see the [behavior change announcement](/release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes) and [Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).
