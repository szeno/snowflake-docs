# Artifacts in Snowflake CoWork

Snowflake CoWork delivers rich, interactive charts and tables as part of its responses. When you find an insight worth keeping, you can save it as an **artifact**: a persistent, live reference to that chart or table. An artifact preserves the underlying query and visualization specification so you can revisit it later, refresh it against current data, and share it with a teammate who sees the same artifact filtered through their own data permissions.

The same underlying infrastructure also powers **shared conversations**, a standalone capability that lets you share a full conversation as a static snapshot. Shared conversations reuse artifact storage and access controls, but they don’t refresh, and their lifecycle is tied to the source conversation. See [Artifact types](#label-artifact-types) for the differences.

## Artifact types

Snowflake CoWork supports two types of artifacts. Each type has different refresh and deletion behavior.

| Type | Description | Data refresh | Persistence |
| --- | --- | --- | --- |
| **Chart or table** | A single chart or table you save from an agent response. | Live reference. Re-runs the original SQL query under the viewer’s credentials. | Persists until you explicitly delete it. |
| **Shared conversation** | A snapshot of a full conversation you share with another user through a link. | Snapshot. The conversation is captured at share time and doesn’t refresh. | Tied to the source conversation. See [Artifact lifecycle](#label-artifact-lifecycle). |

Expand

Show lessSee more

Note

In the rest of this page, “artifact” refers to a chart or table artifact, the live-reference type. Where behavior differs for shared conversations, this page calls them out by name.

## Interactive tables and charts

When you ask Snowflake CoWork a question, the agent generates a response that may include a chart, a table, or both. Charts and tables are interactive, so you can sort, filter, search, and resize directly without asking a new question. In explorer mode, charts and tables are synced so that interactions in one update the other.

Note

Queries default to rolling time windows (for example, “last 30 days” always means the most recent 30 days). If you need a fixed time period, ask with explicit dates such as “show me data from November 15 through November 22.”

## Save chart and table artifacts

When a chart or table contains an insight you want to keep, select **Save** to create an artifact. The artifact preserves the underlying query, the visualization specification, and a cached snapshot so the artifact loads instantly when viewed later. The snapshot is created and refreshed by running the artifact’s query with the credentials of the viewer.

## Manage artifacts

The artifacts hub is the central place to manage your artifacts. It contains the following tabs:

- **Saved**: All artifacts you’ve saved.
- **Shared with me**: Artifacts shared with you through a link.

The hub displays cached snapshots as tile previews for fast loading. You can select a tile to expand the artifact, see additional context, and start a follow-up conversation. You can also search for saved artifacts by name within the artifacts hub.

Chart and table artifacts auto-refresh when you view them more than 12 hours after your last view. You can also refresh manually at any time. The refresh re-runs the original SQL query with your current credentials and updates both the data and the snapshot. Shared conversations don’t refresh; they remain at the snapshot captured when they were shared.

You can ask follow-up questions on any saved artifact. Each follow-up starts a new conversation thread that includes the artifact’s visualization spec, data snapshot, and a summary of the original conversation context. The original conversation stays private and unchanged.

## Share artifacts

You can share an artifact by copying a link and sending it through any communication channel. When you share, you create a link to an artifact object, not a copy. Any account user with the link can open the shared artifact, as long as they have access to the underlying data.

You can share two kinds of artifacts:

- **Charts and tables:** Share a link to a single saved artifact. The recipient runs the underlying query with their own credentials.
- **Conversations:** Share a snapshot of a full conversation. The snapshot reflects the data and visualization at the time of sharing and doesn’t refresh.

When a recipient opens a shared chart or table:

- The artifact runs the SQL query using the recipient’s credentials, respecting their role-based access controls (RBAC), row-level security, and column masking.
- The artifact appears in the recipient’s **Shared with me** tab in the artifacts hub.
- The recipient can explore the artifact, ask follow-up questions, and return to it later.

Note

Recipients can re-share artifacts they have access to. Recipients can also save a shared artifact to their own **Saved** tab.

### Follow-up conversations about shared artifacts

Recipients can ask follow-up questions using the same agent that created the artifact, if they have access to that agent. If they don’t have agent access, Snowflake CoWork displays a warning that follow-up questions may not be available or may produce degraded results with a different agent.

Follow-up conversations are private to the person asking. No information flows back to the original sharer.

### Revoking access

You can unshare an artifact at any time. Unsharing invalidates the link immediately and no one can open it afterward.

### Disabling sharing for the account

Account admins can disable sharing of artifacts and chats for the entire account. In Snowsight, open the Snowflake CoWork settings and, under **Data controls**, turn off **Sharing artifacts and chats**.

When sharing is disabled:

- Existing shared links stop working immediately. Recipients see a “not found” message.
- Users can’t create new shared links from the artifact or conversation menus.
- Saved artifacts in each user’s **Saved** tab are unaffected. Users keep private access to their own artifacts.

Re-enabling **Sharing artifacts and chats** doesn’t restore previously shared links. Users have to create new links.

Note

The **Sharing artifacts and chats** control is account-wide. There is no role-level or per-user override.

## Security and access control

Artifacts follow a caller’s-rights model. Every data interaction validates the current user’s permissions at runtime.

The following security behaviors apply:

- **Saved artifacts are user-scoped:** Saved artifacts are private to each user. Other users can only see artifacts that are explicitly shared.
- **RBAC is enforced:** Every refresh and share runs the query under the viewer’s current role and credentials. Two users with different roles may see different results from the same artifact.
- **Ownership is persistent:** Artifacts are tied to the user, not to a specific role or agent. If you lose access to the originating agent, you keep the artifact and can still refresh it as long as you have access to the underlying data.

## Data deletion and privacy

Artifacts don’t store a shared copy of source data. Each viewer has their own cached snapshot, generated under their own credentials and visible only to them. The underlying artifact is a query against the source tables, not a stored result set:

- **Chart and table artifacts** store the SQL query and visualization specification, not the result set. Each refresh re-executes the query against the source tables under the viewer’s roles.
- **Shared conversation artifacts** capture the conversation as a snapshot at share time. They are deleted when the source conversation is deleted. See [Artifact lifecycle](#label-artifact-lifecycle).

When data is deleted from a source table, that data no longer appears in chart or table artifacts the next time they are refreshed.

## Artifact lifecycle

### Deleting artifacts

| Action | Effect |
| --- | --- |
| You delete a saved chart or table artifact | The artifact is permanently removed from your **Saved** tab. |
| You delete a conversation that was shared | All shared-conversation artifacts derived from that conversation are deleted, whether the deletion is explicit or driven by retention. Anyone with the shared link sees a “not found” message. Conversation threads that start from a shared conversation artifact will also be deleted. |
| You unshare an artifact | The link is invalidated immediately. The underlying artifact remains in your **Saved** tab unless you also delete it. Conversation threads that start from a shared conversation artifact will also become inaccessible when the access to the shared conversation is revoked. |

Expand

Show lessSee more

Saved chart and table artifacts persist until you explicitly delete them.

### Access changes

The following table describes what happens when access conditions change but the artifact isn’t deleted.

| Condition | Effect |
| --- | --- |
| You lose agent access | You can still view and refresh the artifact. Follow-up questions with the original agent aren’t available. |
| You lose data access | The last cached snapshot remains visible, but refresh isn’t available. |
| The agent is deleted or modified | The artifact and its saved query are unaffected. Follow-up questions use the current agent definition, if available. |

Expand

Show lessSee more

When an agent is no longer available, Snowflake CoWork displays a warning.

## Known limitations

- **Single artifacts only:** Currently, you can save and share an individual tile per artifact. Collections of multiple tiles aren’t supported.
- **No user-level sharing permissions:** Currently, all sharing (chart and table artifacts and shared conversations alike) is link-based and public within the account. You can’t restrict a shared link to specific users.
- **No folders or labels:** Currently, artifacts can’t be organized into groups, folders, or labeled for categorization.
- **Chart editor only available for some chart types:** The manual chart editor UI is only available for bar, line, pie, and scatter charts. For artifacts containing other chart types, ask Snowflake CoWork to make changes to the chart.
