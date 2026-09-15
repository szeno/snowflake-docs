# Tutorial 3: Add a CKE to Snowflake CoWork

## Step-by-step instructions

It’s easy to add a Cortex Knowledge Extension to Snowflake CoWork. Once you have a CKE in your account, you can add it to Snowflake CoWork by adding the CKE to an Agent in Snowsight.

Important

Before you get started, make sure Snowflake CoWork has access to the CKE:

Copy code

```
-- Grant Snowflake CoWork the right access to the CKE so it can be added as an agent
grant imported privileges on database <CKE_DATABASE_NAME> to role <SNOWFLAKE_INTELLIGENCE_ROLE>;
```

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. In the **Agents** screen, select **Create Agent** and give the Agent a name.

   ![A screenshot of the Create Agent page in Snowsight.](/static/images/cortex-knowledge-extensions/cke-create-agent.png)
4. On the **Tools** tab, click **Search documents and unstructured** to open the **Add tool: Cortex Search** dialog.
5. Select the Database that has the CKE, and select the Search Service for the CKE.
6. Give the CKE a display name and a description.
7. Click **Add**.

   ![A screenshot of how to add a search service to an agent.](/static/images/cortex-knowledge-extensions/cke-add-search-service.png)
8. Navigate to **Snowflake CoWork** on the left side.
9. Select the drop down under the textbox to select the new Agent with your CKE tied to it.

![A screenshot showing a chat box created from the agent.](/static/images/cortex-knowledge-extensions/cke-agent-chat-box.png)

10. Ask a question with the selected Agent and see the cited answers with links back to the source content via the CKE.

![A screenshot showing responses in a chat box created from the agent.](/static/images/cortex-knowledge-extensions/cke-agent-chat-response.png)
