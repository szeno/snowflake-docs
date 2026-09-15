# August 4, 2026: Workspace sharing in Declarative Native Apps (*Public Preview*)

Workspace sharing is now available in public preview for Declarative Native Apps. Providers can share a whole directory of
files and folders by declaring a workspace in the application package manifest. Consumers get a read-only
[workspace](/user-guide/ui-snowsight/workspaces) when they install the app, and can browse the folder structure and open the files.

Workspace sharing is also how providers share
[Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview), the
next-generation notebook experience. Include `.ipynb` files in the shared directory, and consumers can run and interact with those
notebooks in their own account without being able to modify them. Shared notebooks run with
[restricted caller’s rights](/developer-guide/restricted-callers-rights), so they can only access the objects that the app shares.

Sharing individual notebooks with `application_content.notebooks` shares
[Legacy Notebooks](/user-guide/ui-snowsight/notebooks) and is deprecated. Share notebooks in a workspace instead. For the
Legacy Notebooks removal timeline, see [Disable Legacy Notebook creations](/release-notes/bcr-bundles/un-bundled/bcr-disable-legacy-notebooks).

For more information, see:

- [Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces)
- [Access a shared workspace in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-shared-workspace)
- [Declarative Native App manifest reference](/developer-guide/declarative-sharing/manifest-reference)
