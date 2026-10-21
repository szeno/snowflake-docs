# Chart and Thread artifacts in Snowflake CoWork

In Snowflake CoWork, you can save charts and tables from responses to revisit an analysis, or share a conversation as a snapshot. For the common object model, ownership, sharing privileges, and SQL administration, see [Snowflake Artifacts](/user-guide/snowflake-artifacts).

## Artifact types

These workflows use two artifact types:

- **Chart artifacts** contain a saved chart or table and support query-backed analysis.
- **Thread artifacts** contain saved conversations and don’t run SQL or refresh.

## Save and explore charts and tables

When you ask Snowflake CoWork a question, its response can include a chart, a table, or both. You can sort, filter, search, and resize the results without asking a new question. In explorer mode, charts and tables are synchronized so that interactions in one update the other.

To save a chart or table, select **Save** on the result. The saved artifact preserves the underlying query, visualization specification, and a cached snapshot generated with the viewer’s credentials.

Queries can use rolling time windows. For example, “last 30 days” refers to the most recent 30 days when the query runs. To keep a fixed reporting period, specify dates in your question.

## Find and refresh saved artifacts

Use the artifacts hub to find your saved and shared content:

- **Saved**: Artifacts you’ve saved.
- **Shared with me**: Artifacts you’ve opened through a shared link.

Search for a saved artifact by name, or select its preview tile to open it and see additional context. The preview uses a cached snapshot.

Chart and table artifacts automatically refresh when you view them more than 12 hours after your last view. You can also refresh manually. A refresh reruns the original SQL query with your current credentials and updates the data and cached snapshot. Thread artifacts don’t refresh.

Each viewer’s chart or table snapshot is generated under that viewer’s credentials. Refresh respects [role-based access control](/user-guide/security-access-control-overview), [row access policies](/user-guide/security-row-intro), and [masking policies](/user-guide/security-column-ddm-intro), so viewers can see different results from the same artifact.

## Ask follow-up questions

You can ask follow-up questions about a saved chart or table. Each follow-up starts a new conversation with the visualization specification, data snapshot, and a summary of the original conversation context. It doesn’t change the original conversation.

For a shared artifact, you can use the original agent if you have [access to it](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents). Otherwise, Snowflake CoWork displays a warning that follow-up questions might be unavailable or produce different results with another agent. Follow-up conversations are private to the person asking; their content isn’t sent back to the original sharer.

## Share a conversation as a Thread artifact

A shared conversation captures a snapshot of the conversation, including its text and visualizations, at the time of sharing. It doesn’t rerun the original queries or refresh when source data changes.

Use the conversation’s sharing control to create a shared snapshot and send its link to recipients who have access. A recipient sees saved content rather than results recalculated with the recipient’s data privileges.

Important

Review the conversation for sensitive content before sharing. A recipient with access to the Thread artifact can view its saved content even without access to the original source data.

## Share and revoke access

For a saved chart or table, sharing provides a link to the artifact rather than creating a separate copy. Recipients need access to the artifact and, to run its query, access to its source data. They can explore the artifact, save it to their **Saved** tab, and ask follow-up questions when agent access permits.

Possessing a link doesn’t replace the applicable access checks. Permission to view an artifact doesn’t by itself establish permission to grant or revoke access. For artifact privileges and the type-specific `MANAGE ACCESS` requirements, see [Sharing privileges](/user-guide/snowflake-artifacts#label-snowflake-artifacts-sharing-privileges).

### Disabling sharing for the account

An administrator can turn off **Sharing artifacts and chats** for the account. This blocks new sharing and non-owner access to shared artifacts, even with existing grants. For configuration and the relationship to artifact privileges, see [Control sharing for the account](/user-guide/snowflake-artifacts#label-snowflake-artifacts-control-sharing).

## Lifecycle and access changes

Saved charts and tables persist independently of the source conversation until explicitly deleted. Shared conversations have a different lifecycle because they are tied to the source conversation.

### Deletion and revocation

- Deleting a source conversation, explicitly or through retention, deletes its shared-conversation artifacts. Their links return “not found”. Conversations started from those shared snapshots are also deleted.
- Revoking access to a shared conversation makes conversations started from that snapshot inaccessible.
- Deleting a saved chart or table removes that artifact. For ownership requirements and recovery limitations, see [Deletion](/user-guide/snowflake-artifacts#label-snowflake-artifacts-deletion).

### Access changes

- Losing access to the original agent doesn’t remove a saved chart or table. You can still refresh it if you retain artifact and source-data access, but follow-up questions with that agent aren’t available.
- Losing source-data access prevents refresh; the last cached snapshot remains visible.
- Deleting or modifying the original agent doesn’t change the saved query. Follow-up questions use the current agent definition, if available.

When source data is deleted, it no longer appears in a chart or table after the next successful refresh. A Thread artifact remains a saved snapshot; source-table changes don’t rewrite it. For the distinction between query-backed and saved content, see [Artifacts and source data](/user-guide/snowflake-artifacts#label-snowflake-artifacts-source-data).

## Limitations

- A saved chart or table artifact represents an individual result tile, not a collection of tiles.
- The Snowflake CoWork workflow described here doesn’t provide folders or labels for organizing saved artifacts.
- The manual chart editor supports bar, line, pie, and scatter charts. For other chart types, ask Snowflake CoWork to change the chart. For agent-level chart preferences, see [Chart customization](/user-guide/snowflake-cortex/snowflake-cowork/chart-customization).

## Related topics

- [Snowflake Artifacts](/user-guide/snowflake-artifacts).
- [Create and share a dashboard or HTML report](/user-guide/snowflake-artifacts-create-share).
- [Document generation in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/document-generation).
