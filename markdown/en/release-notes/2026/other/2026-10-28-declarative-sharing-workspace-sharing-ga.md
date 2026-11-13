# Oct 28, 2026: Workspace sharing in Declarative Shares (*General availability*)

Workspace sharing in Declarative Shares is now generally available and is no longer in
[Preview](/release-notes/preview-features).

With workspace sharing, providers can share a directory of files and folders, including
[Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview),
documentation, images, and sample data, by declaring a workspace in the application package
manifest. Consumers receive a read-only [workspace](/user-guide/ui-snowsight/workspaces) when they
install the app, and can browse the folder structure and run shared notebooks in their own account
with [restricted caller’s rights](/developer-guide/restricted-callers-rights).

For more information, see:

- [Share a workspace in a Declarative Share](/developer-guide/declarative-sharing/workspaces)
- [Access a shared workspace in a Declarative Share](/developer-guide/declarative-sharing/consumer/access-shared-workspace)
- [Editing notebooks in a Declarative Share](/developer-guide/declarative-sharing/live-editing)
- [Declarative Share manifest reference](/developer-guide/declarative-sharing/manifest-reference)
