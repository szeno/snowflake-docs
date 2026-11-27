# About Openflow Connector for Slack

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

This topic describes the basic concepts of the Openflow Connector for Slack,
its variants, and limitations.

The Openflow Connector for Slack connects a Slack workspace to Snowflake
to ingest Slack messages, reactions, file attachments, and channel
memberships (ACLs). The connector also supports the Cortex Search service and can make
ingested Slack content ready for conversational analysis for use in AI
Assistants using SQL, Python, or REST APIs.

Use this connector if you’re looking to do the following:

- Pull Slack messages and metadata into Snowflake for searchable, organization-wide insights
- Ingest Slack content and make it ready for chat in your AI assistants with Snowflake Cortex

## Variants of the Openflow Connector for Slack

The Openflow Connector for Slack contains two variants, which differ in whether ingested content is indexed into Cortex Search. Choose the variant that meets your requirements before you set up the connector.

|  |  |
| --- | --- |
| Variant | Description |
| [Ingest Slack content only](/user-guide/data-integration/openflow/connectors/slack/setup#label-slack-use-case-1-ingest-slack-content-only) | Ingests Slack messages, reactions, file attachments, and channel memberships (ACLs) into Snowflake tables for custom analysis, without Cortex Search processing. |
| [Ingest Slack content and enable Cortex](/user-guide/data-integration/openflow/connectors/slack/setup#label-slack-use-case-2-ingest-slack-content-and-enable-cortex) | Ingests the same content, then chunks messages and creates a Cortex Search service with channel membership ACLs for conversational analysis in AI assistants. |

Expand

Show lessSee more

## Workflow

1. **Slack admin** creates a Slack App as described later, then installs
   the App in the channels or conversations they intend to ingest messages
   from. The Bot token and App token from the Slack App need to be
   provided to the Snowflake account admin.
2. **Snowflake account admin**:

   1. Installs the connector.
   2. Specifies the required parameters for the flow template, for
      example, Bot token, App token, and database and schema names.
   3. Runs flow. The following happens when the flow is run in Openflow:
      1. The flow automatically creates a database, schema and the
         necessary tables and external access integration in Snowflake
         on behalf of the admin. If you use the Ingest Slack content and enable
         Cortex variant, it also creates a Cortex Search service and wires up
         chunks, ACLs, and metadata. By default, these are
         only accessible to the Snowflake account admin role.
      2. Fetches specified conversations, metadata, ACLs from the Slack
         channel(s). An ACL is defined as the snapshot list of user IDs
         and emails that are members of each channel being ingested.
      3. Chunks ingested conversation messages.
      4. Puts chunked conversation messages along with metadata and ACLs
         into Snowflake tables.
3. **IT Developer** in customer’s organization creates bespoke Chat App
   and passes user identity which is the user’s email registered on
   Slack, as a filter when invoking Cortex Search REST API with the end
   user’s question.
4. **End users** of the Chat App in the customer’s organization see
   responses from Cortex Search restricted to chunks from conversations
   they have access to in the Slack channel based on ACLs, along with a
   link to the source conversation.

## Considerations

- By default, any user with the Snowflake account admin role can
  “see” the raw ingested messages and conversations and tables
  created by the flow template.
- The user with the Snowflake account admin role decides who can access
  the internal stage and tables through Snowflake roles.
- The user with the Snowflake account admin role decides who can query
  the Cortex Search service through Snowflake roles.

## Limitations

- The connector captures historical file attachments, reactions, and messages, but only after the Slack App is added to a conversation or channel.
- If a user edits an existing message or deletes a message, the changes are captured in Snowflake at the next refresh interval.

## Next steps

[Set up the Openflow Connector for Slack](/user-guide/data-integration/openflow/connectors/slack/setup)
