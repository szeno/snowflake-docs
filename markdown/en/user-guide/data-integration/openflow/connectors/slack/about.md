# About Openflow Connector for Slack

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for Slack,
steps to set it up, and limitations.

The Openflow Connector for Slack connects a Slack workspace to Snowflake
in order to ingest Slack messages, reactions, file attachments, and channel
memberships (ACLs). The connector also supports the Cortex Search service and can make
ingested Slack content ready for conversational analysis for use in AI
Assistants using SQL, Python or REST APIs.

Use this connector if you’re looking to do the following:

- Pull Slack messages and metadata into Snowflake for searchable, organization-wide insights
- Ingest Slack content and make it ready for chat in your AI assistants with Snowflake Cortex

## Limitations

- The connector captures historical file attachments, reactions and messages, but only after the Slack App is added to a conversation or channel.
- If a user edits an existing message or deletes a message, the changes are captured in Snowflake at the next refresh interval.

## Workflow

1. **Slack Admin** creates a Slack App as described later, then installs
   the App in the channels or conversations they wish to ingest messages
   from. The Bot token and App token from the Slack App need to be
   provided to the Snowflake Account Admin
2. **Snowflake account admin**:

   1. Installs the connector.
   2. Specifies the required parameters for the flow template, for
      example, Bot token, App token, and database and schema names.
   3. Runs flow. The following happens when the flow is run in Openflow:
      1. The flow automatically creates a database, schema and the
         necessary tables and external access integration in Snowflake
         on behalf of the admin. It also creates a Cortex Search and
         wires up chunks and ACLs and metadata. By default, these are
         only accessible to the Snowflake account admin role
      2. Fetches specified conversations, metadata, ACLs from the Slack
         channel(s). An ACL is defined as the snapshot list of user IDs
         and emails that are members of each channel being ingested.
      3. Chunks ingested conversation messages
      4. Puts chunked conversation messages along with metadata and ACLs
         into Snowflake tables
3. **IT Developer** in customer’s organization creates bespoke Chat App
   and passes user identity which is the user’s email registered on
   Slack, as a filter when invoking Cortex Search REST API with the end
   user’s question
4. **End users** of the Chat App in the customer’s organization see
   responses from Cortex Search restricted to chunks from conversations
   they have access to in the Slack channel based on ACLs, along with a
   link to the source conversation.

### Considerations

- By default, any user with the Snowflake account admin role will be
  able to “see” the raw ingested messages and conversations and tables
  created by the flow template
- The user with the Snowflake account admin role decides who can access
  the internal stage and tables through Snowflake roles.
- The user with the Snowflake account admin role decides who can query
  the Cortex Search service through Snowflake roles.

### Next steps

[Set up the Openflow Connector for Slack](/user-guide/data-integration/openflow/connectors/slack/setup)
