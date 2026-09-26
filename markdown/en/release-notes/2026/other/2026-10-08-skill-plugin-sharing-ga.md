# Oct 8, 2026: Skill and plugin sharing in CoCo (*General availability*)

Skill and plugin sharing in CoCo is now generally available and is no longer in [Preview](/release-notes/preview-features).

Instead of keeping skills and plugins local to a single user’s machine, you can publish them as Cortex Extension objects so that teammates, specific roles, or your entire account can find and install them.

This release adds the following capabilities:

- **Security scanning**: Skills and plugins are scanned for security issues when they’re shared. Sharing returns the link immediately while the scan runs in the background, and a skill or plugin that fails the scan can’t be installed by anyone else. An administrator can override a false positive. The scanner accepts up to 50 files per skill or plugin, 2 MiB for any single file, and 10 MiB in total.
- **Delegated administration**: Catalog governance no longer requires ACCOUNTADMIN. Each governance action is backed by its own privilege, so you can create a catalog administrator role and grant it only what it needs. ACCOUNTADMIN retains full authority.
- **Categories**: Group skills and plugins into account-specific categories so people can narrow the catalog instead of scanning one long list. Snowflake suggests a category at publish time, and administrators maintain the list of available categories.
- **Editable descriptions**: Every shared skill and plugin carries a human-readable description, generated when you share and editable by the owner without publishing a new version.
- **Bulk import**: A built-in skill shares every skill and plugin it finds in a local directory, creating a Cortex Extension for each one. Point it at a cloned Git repository to bring a team’s whole collection into Snowflake in one pass.

The following capabilities were already available in preview:

- **Sharing**: Publish from the CoCo CLI, CoCo Desktop, or CoCo in Snowsight and get a `snow://` link to send to colleagues. Access and discoverability are controlled independently, so you can share privately by link or publish to a role for browsing.
- **Discovery**: Find shared skills and plugins through automatic in-context discovery, manual search in CoCo, or the **Skills and plugins** page under **AI & ML** in Snowsight.
- **Versioning**: Each upload creates a new version. A link without a version resolves to the version Snowflake selects for use, preferring the newest certified version with an eligible scan status.
- **Certification and telemetry**: Certify individual versions, and review install and usage counts over the last 28 days for each shared skill and plugin.

For more information, see [Share skills and plugins](/user-guide/cortex-code/cortex-code-skill-plugin-sharing).
