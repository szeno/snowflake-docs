# External network access in Streamlit in Snowflake

This topic describes how to create secure access to network locations external to Snowflake.

## External network access in Streamlit in Snowflake

You can create secure access to specific network locations external to Snowflake, and you can use that access from within the
Streamlit app code. You can enable access through an external access integration.

To enable a Streamlit app to use an external access integration (EAI), you can run the [CREATE STREAMLIT](/sql-reference/sql/create-streamlit)
or [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) command and set the EXTERNAL\_ACCESS\_INTEGRATIONS parameter to include that EAI.

With an EAI, you can use Python libraries that access external locations, such as `requests` or `urllib`,
and use third-party libraries that require access to a network location.

For more information, see [External network access overview](/developer-guide/external-network-access/external-network-access-overview).

### Example: Access the OpenAI API

The following example shows how to create an EAI for an outbound request to the OpenAI API:

1. To create a network rule that represents the external network’s location and restrictions for access, use the [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule)
   command:

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE network_rules
     MODE = EGRESS
     TYPE = HOST_PORT
     VALUE_LIST = ('api.openai.com');
   ```

   For more information, see [Creating a network rule to represent the external network location](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-network-rule).
2. To create a secret that represents credentials required to authenticate with the external network location, use the
   [CREATE SECRET](/sql-reference/sql/create-secret) command:

   Copy code

   ```
   CREATE OR REPLACE SECRET openai_key
     TYPE = GENERIC_STRING
     SECRET_STRING = '<any_string>';
   ```

   For more information, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret).
3. To create an EAI, run the [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration) command, setting ALLOWED\_NETWORK\_RULES
   to the network rule you created and ALLOWED\_AUTHENTICATION\_SECRETS to the secret you created:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION openai_access_int
     ALLOWED_NETWORK_RULES = (network_rules)
     ALLOWED_AUTHENTICATION_SECRETS = (openai_key)
     ENABLED = TRUE;
   ```
4. To grant the required privileges to use the SECRET and INTEGRATION objects for external access to the Streamlit app creator, use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)
   command:

   Copy code

   ```
   GRANT READ ON SECRET openai_key TO ROLE streamlit_app_creator_role;
   GRANT USAGE ON INTEGRATION openai_access_int TO ROLE streamlit_app_creator_role;
   ```
5. To enable the Streamlit app to use the integration, run the [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) command, setting the
   EXTERNAL\_ACCESS\_INTEGRATIONS property to the integration:

   Copy code

   ```
   USE ROLE streamlit_app_creator_role;

   ALTER STREAMLIT streamlit_db.streamlit_schema.streamlit_app
     SET EXTERNAL_ACCESS_INTEGRATIONS = (openai_access_int)
     SECRETS = ('my_openai_key' = streamlit_db.streamlit_schema.openai_key);
   ```

   Note

   You can also set up a new Streamlit object to use an external access integration by specifying the EXTERNAL\_ACCESS\_INTEGRATIONS parameter
   when you run the [CREATE STREAMLIT](/sql-reference/sql/create-streamlit) command:

   Copy code

   ```
   CREATE STREAMLIT streamlit_db.streamlit_schema.streamlit_app
     ROOT_LOCATION = '<stage_path_and_root_directory>'
     MAIN_FILE = '<path_to_main_file_in_root_directory>'
     EXTERNAL_ACCESS_INTEGRATIONS = (openai_access_int)
     SECRETS = ('my_openai_key' = streamlit_db.streamlit_schema.openai_key);
   ```
6. In your Streamlit app code, call the external API:

   Copy code

   ```
   from openai import OpenAI
   import streamlit as st
   import _snowflake

   st.title(":speech_balloon: Simple chat app using an external LLM")
   st.write("This app shows how to call an external LLM to build a simple chat application.")

   # Use the _snowflake library to access secrets
   secret = _snowflake.get_generic_secret_string('my_openai_key')
   client = OpenAI(api_key=secret)

   # ...
   # code to use API
   # ...
   ```
