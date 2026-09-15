# Cortex Agents for Microsoft Teams and Microsoft 365 Copilot

## Introduction

For most teams, accessing timely data insights means context-switching between dedicated analytics platforms and
communication tools, leading to delays and reduced productivity. Integrating an agentic AI system into Microsoft Teams
can bring the answers directly to where conversations and decisions happen, accelerating the flow of information across
your business. But building a secure, in-chat analytics solution that is both powerful and intuitive is a significant
undertaking. Fortunately, Snowflake has built one for you.

The Snowflake Cortex Agents integration for Microsoft Teams and Microsoft 365 Copilot embeds Snowflake’s conversational
AI agents into your business communication platform. Business teams and non-technical users can interact with their
Snowflake structured and unstructured data using simple, natural language to receive direct answers and visualizations without leaving
their Teams chats or the broader Microsoft 365 ecosystem. The integration is available via
[Microsoft AppSource](https://appsource.microsoft.com/en-us/product/Office365/WA200008996) for
seamless deployment.

Use the following sections to set up the integration and start using it to get value from your data.
For a Quickstart guide, see [Getting Started with Cortex Agents for Microsoft Teams and Microsoft 365 Copilot](https://quickstarts.snowflake.com/guide/getting_started_with_the_microsoft_teams_and_365_copilot_cortex_app).

Important

When you use this integration, you are directing Snowflake to send or receive data between the Snowflake Service and Microsoft services (including Microsoft Teams and Microsoft 365 Copilot). Snowflake is not responsible for the privacy, security, or integrity of data once it leaves the Snowflake Service boundary. Your use of Microsoft Teams or Microsoft 365 Copilot, and any data you process with it, is governed solely by the terms between you and Microsoft.

### Key features

- **Seamless analytics via natural language.** Delight your business decision-makers by empowering them to get insights
  themselves within the Microsoft Teams and Microsoft 365 Copilot interfaces. You can discover trends and analyze data
  without technical expertise or waiting for a custom dashboard to be built. Users can ask questions conversationally
  and receive accurate, LLM-powered answers in text, tabular, or chart form on the fly, dramatically accelerating
  data-driven decision-making.
- **Dual interfaces for comprehensive workflows.** Cortex Agents for Microsoft Teams offer two distinct interfaces to
  support different business needs. Use the standard Teams Application for dedicated, in-depth analysis within a Teams
  Bot application chat, or leverage the Microsoft 365 Copilot Agent to bring targeted Snowflake insights into your
  wider conversational workflow within the Microsoft 365 Copilot ecosystem.
- **Powered by Snowflake Cortex Agents.** This integration is powered by the Snowflake Cortex Agents API, which handles
  the complexities of generating accurate, reliable insights from your data. The agentic system intelligently interprets
  user requests and generates responses, saving your teams from having to build complex conversational AI patterns or
  manage underlying models. You can reuse the same agents you use with
  [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork), avoiding duplicate
  configuration and governance effort.
- **Enterprise-grade security and governance.** Built on Snowflake’s privacy-first foundation, the integration ensures you
  can confidently explore AI-driven use cases. This means:
  - **Your data stays within Snowflake’s governance boundary.** User prompts are sent to the Cortex Agents API, but the
    underlying data queried to generate an answer never leaves Snowflake’s secure environment. The resulting SQL query is
    executed within your Snowflake virtual warehouse.
  - **Seamless integration with Snowflake’s privacy and governance features.** The integration fully respects Snowflake’s
    role-based access control (RBAC). All queries executed on behalf of a user adhere to their established permissions,
    guaranteeing that users can only see data they are authorized to access.

## Regional availability and limitations

The Cortex Agents integration for Microsoft Teams and Microsoft 365 Copilot is available across all Snowflake public
cloud deployments. However, there are some regional considerations and current limitations you should be aware of:

### Consent for accounts outside Azure US East 2

When connecting a Snowflake account that is based in a region other than Azure US East 2, administrators are
prompted to accept a consent notification during the account setup process. This consent acknowledges that the bot backend infrastructure processes user prompts and bot responses through
a service hosted in the Azure US East 2 region.

To withdraw consent, the account must be removed by an administrator through the Teams application interface.

Consent text displayed during setup

The following is the exact consent you will be asked to accept when connecting your Snowflake account to the Teams bot:

Copy code

```
Data Processing.
Use of this integration requires an intermediate processing (but not storage) step in Snowflake's Azure East US 2 region,
regardless of the region where your Snowflake account is located.
By proceeding, you are authorizing Snowflake to process your data within Snowflake's Azure East US 2 region.

For more information on this behavior, please refer to .
```

### Private Link

Private Link configurations are not supported. You must disable Private Link to use this integration.

### Sovereign cloud regions

The integration is not available for Snowflake accounts in sovereign cloud regions.

## Set up integration

Cortex Agent’s Microsoft Teams integration allows organization administrators to connect multiple Snowflake accounts to
the Teams and Copilot workspaces in their organizations. Setting up the integration involves a few simple steps, summarized
below:

1. **Tenant-wide setup by Azure administrator.** The integration requires a one-time setup by a Microsoft Azure
   administrator to grant consent for the Snowflake application within the Microsoft Entra ID (formerly Azure Active Directory) tenant. This
   step enables secure OAuth 2.0 authentication for the integration.
2. **Snowflake security integration.** After the Azure administrator has completed the tenant-wide setup, a
   Snowflake administrator must configure a security integration for each individual Snowflake account that they wish to
   connect to the Microsoft Teams or M365 Copilot application. This step ensures that the integration can securely access
   the necessary data within each Snowflake account.
3. **Linking accounts to the bot.** Once the security integration is configured, the Snowflake administrator can link
   the Snowflake account to the Microsoft Teams or M365 Copilot bot. This step allows the bot to access the data and
   functionality of the Snowflake account, enabling users to interact with their data directly within Teams or Copilot.

### Prerequisites

Before you begin the integration process, make sure you have established the following:

- **Administrator access.** Setup requires administrative access on both Snowflake and your Microsoft tenant.
- **Snowflake administrative privileges:** Your Snowflake user must have access to the ACCOUNTADMIN or SECURITYADMIN
  role. These permissions are required to create the necessary security integration object in your Snowflake account.
- **Microsoft administrative privileges:** Your Azure user must have Global Administrator privileges (or an equivalent
  role) for your Microsoft Entra ID tenant. These privileges are required to grant the necessary tenant-wide admin
  consent for the application.
- **Microsoft tenant ID:** You need your organization’s Microsoft tenant ID to configure the Snowflake security
  integration. For more information on finding your organization’s Tenant ID, see
  [Get subscription and tenant IDs in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-portal/get-subscription-tenant-id).
- **Individual User Accounts:** Every end user must have their own Microsoft and Snowflake user accounts.
- **End-user licensing:** Users must have the appropriate Microsoft licenses to access Microsoft Teams. A Copilot license
  is also required if you plan to use the integration with Microsoft 365 Copilot.

### Step 1: Tenant-wide Entra ID configuration

To enable secure authentication for Cortex Agents, a Microsoft Azure administrator must grant consent for two
applications hosted in Snowflake’s tenant, creating a *service principal* for each application within your Entra ID tenant.
The two applications are:

- **Cortex Agents Bot OAuth Resource:** Represents the protected Snowflake API and defines the access permissions
  (scopes) for client applications.
- **Cortex Agents Bot Snowflake OAuth Client:** Represents the client application, in this case the Teams application
  back end service, that calls the Snowflake API after requesting an access token.

Instructions for granting consent for these applications are provided below. The process is very similar for both applications,
but the specific permissions and scopes differ slightly.

#### Granting consent for OAuth Resource principal

To grant consent for the Cortex Agents Bot OAuth Resource application service principal:

1. In your browser, navigate to `https://login.microsoftonline.com/<tenant-id>/adminconsent?client_id=5a840489-78db-4a42-8772-47be9d833efe`,
   where `tenant-id` is your organization’s Microsoft tenant ID.

   If you are not already signed in, you are prompted to do so.

   A **Permission requested** dialog appears, showing the permission that the application requires.
2. Select **Accept** to grant the requested permission.

#### Granting consent for OAuth Client principal

This process displays two dialogs. Each is similar to the one for the OAuth Resource principal, but the permissions requested are different.

To grant consent for the Cortex Agents Bot Snowflake OAuth Client application service principal:

1. In your browser, navigate to `https://login.microsoftonline.com/<tenant-id>/adminconsent?client_id=bfdfa2a2-bce5-4aee-ad3d-41ef70eb5086`,
   where `tenant-id` is your organization’s Microsoft tenant ID.

   A **Permissions requested (1 of 2)** dialog appears, showing one set of permissions that the application requires.
2. Select **Accept** to grant the requested permissions.

   The second permission dialog appears (**Permissions requested (2 of 2)**).
3. Select **Accept** to grant the requested permissions.

Important

You may see an error message stating that a required query string parameter was missing, like the following.

```
{
  "error": {
    "code": "ServiceError",
    "message": "Missing required query string parameter: code. Url = https://unitedstates.token.botframework.com/.auth/web/redirect?admin_consent=True&tenant=<TENANT-ID>"
  }
}
```

You can safely ignore this error. Consent was still granted successfully. To be sure, confirm the permissions were granted successfully
by following the instructions in the next section.

#### Confirming permission grants

After granting consent for both applications, you can confirm that the permissions were granted successfully by checking the
**Enterprise applications** section of the Microsoft Entra ID portal.

1. Log in to the [Microsoft Entra admin center](https://entra.microsoft.com/) if necessary.
2. Navigate to Enterprise Applications by typing “enterprise applications” in the search box, then selecting **Enterprise applications** in the results.
3. In the **All applications** list, find the two applications for which you just granted consent: Snowflake Cortex Agents Bot OAuth Resource and
   Snowflake Cortex Agents Bot OAuth Client. An easy way to do this is to search for “Snowflake Cortex Agent.”

   If both applications appear in the list, permissions have been correctly granted. If one or both applications are missing, try granting consent again.

### Step 2: Snowflake security integration

Integrating Snowflake with Microsoft Teams requires a [security integration](/sql-reference/sql/create-security-integration)
that establishes cryptographic trust between your Snowflake account and your Entra ID tenant. This process requires:

- Enabling Entra ID as an external OAuth provider in Snowflake.
- Choosing or creating at least one Cortex Agent object for the integration.
- Granting required roles and privileges so intended users can invoke the agent.

#### Enabling Entra ID as an external OAuth provider

A Snowflake security integration object represents an integration with an external OAuth provider, in this case
Microsoft Entra ID. This integration allows Snowflake to authenticate users who are logged into Microsoft Teams or
Copilot.

The following SQL statement is an annotated template for creating the integration. This command must be
executed by a role with ACCOUNTADMIN privileges. Replace the `tenant-id` placeholders with your Microsoft
Tenant ID.

Copy code

```
CREATE OR REPLACE SECURITY INTEGRATION entra_id_cortex_agents_integration
    TYPE = EXTERNAL_OAUTH
    ENABLED = TRUE
    EXTERNAL_OAUTH_TYPE = AZURE
    EXTERNAL_OAUTH_ISSUER = 'https://login.microsoftonline.com/<tenant-id>/v2.0'
    EXTERNAL_OAUTH_JWS_KEYS_URL = 'https://login.microsoftonline.com/<tenant-id>/discovery/v2.0/keys'
    EXTERNAL_OAUTH_AUDIENCE_LIST = ('5a840489-78db-4a42-8772-47be9d833efe')
    EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = ('email', 'upn')
    EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'email_address'
    EXTERNAL_OAUTH_ANY_ROLE_MODE = 'ENABLE'
```

See [CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external) for a complete reference of the parameters
available for this command.

Together, the EXTERNAL\_OAUTH\_TOKEN\_USER\_MAPPING\_CLAIM and EXTERNAL\_OAUTH\_SNOWFLAKE\_USER\_MAPPING\_ATTRIBUTE parameters
link an Entra ID identity to a Snowflake identity. For authentication to succeed, the value of the specified claim in
the JWT must exactly match the value of the specified attribute on a user object in Snowflake. The two main configurations
Snowflake recommends are:

- Mapping by User Principal Name (UPN): Set the EXTERNAL\_OAUTH\_TOKEN\_USER\_MAPPING\_CLAIM parameter to ‘upn’ and the
  EXTERNAL\_OAUTH\_SNOWFLAKE\_USER\_MAPPING\_ATTRIBUTE parameter to ‘LOGIN\_NAME’.
- Mapping by email address: Set the EXTERNAL\_OAUTH\_TOKEN\_USER\_MAPPING\_CLAIM parameter to ‘email’ and the
  EXTERNAL\_OAUTH\_SNOWFLAKE\_USER\_MAPPING\_ATTRIBUTE parameter to ‘EMAIL\_ADDRESS’.

The example statement above uses the email address mapping configuration, but also specifies UPN in the
EXTERNAL\_OAUTH\_TOKEN\_USER\_MAPPING\_CLAIM parameter, allowing you to change the mapping method by changing only the
EXTERNAL\_OAUTH\_SNOWFLAKE\_USER\_MAPPING\_ATTRIBUTE.

The example statement also enables EXTERNAL\_OAUTH\_ANY\_ROLE\_MODE, so that the user’s default role is used.

For more information on OAuth scopes, see [Scopes](/user-guide/oauth-ext-overview#label-ext-oauth-scopes).

#### User provisioning requirements

To ensure successful authentication using the mapping configuration described previously, make sure that a strict
one-to-one mapping exists between Entra ID users and Snowflake users. Designate or create a Snowflake user for every
Entra ID user who will use the integration.

Each Entra ID user must map to exactly one Snowflake user. For email mapping, the Entra ID primary email must exactly
match the Snowflake user’s EMAIL\_ADDRESS. For UPN mapping, the Entra ID UPN must exactly match the Snowflake user’s
LOGIN\_NAME.

To reduce manual administration effort, you can optionally configure automatic user provisioning and deprovisioning from
Entra ID to Snowflake. See
[Configure automatic provisioning](https://learn.microsoft.com/en-us/entra/identity/saas-apps/snowflake-provisioning-tutorial).

#### Create and configure the Cortex Agents

After you create the security integration, ensure that at least one
[Cortex Agent Object](/user-guide/snowflake-cortex/cortex-agents-rest-api) exists in your Snowflake account for the Teams or Microsoft 365
Copilot integration to use.

If you already have a working agent that you want to use, no further action is required for this step.

To create a new agent, follow the [instructions](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-create).

Note

If you already use Snowflake CoWork and have created agents for that experience,
you can reuse those agents with the Microsoft Teams and Microsoft 365 Copilot integration.
You don’t need to recreate or reconfigure them;
any changes you make to an agent (such as instructions, tools, underlying objects, or privileges)
are immediately reflected across all three interfaces.

##### Grant required privileges to users

Make sure the role under which the integration will run (each user’s default role or permitted secondary roles) has the grants described in the
[access control requirements section](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control).

### Step 3: Setting up the Teams app and connecting your Snowflake account

The final step in the integration process is to set up the Microsoft Teams application and connect it to the Snowflake
users who will use it. This requires you to complete the following tasks:

- Install the Cortex Agents app from the Teams store
- Connect your Snowflake account to the Teams application

#### Install the app from the Teams store

All users must install the Cortex Agents app from the Microsoft Teams store. To install the app, search for “Snowflake
Cortex Agents” in the Teams app store, then click **Add** to install the app.

Note

Depending on your organization’s Microsoft Teams policies, a Teams Administrator may need to approve the app before it is available to users.
See [Overview of app management and governance in Teams admin center](https://learn.microsoft.com/en-us/microsoftteams/manage-apps) for instructions.

#### Connect your Snowflake account to the Teams app

The first user to interact with the Cortex Agents app in Teams is prompted to connect their Snowflake account to the
app. This user must have the ACCOUNTADMIN or SECURITYADMIN role in Snowflake for this step to succeed.

To recap, every user’s default role in Snowflake must have the required privileges to access the agent’s objects, as
described in the [access control requirements section](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control) of the Cortex Agents
topic.

Security integrations block the main Snowflake administrative roles by default. Therefore, you cannot use administrative
roles such as ACCOUNTADMIN as the default role for the user that will set up the Teams bot. For information on this
restriction, see [BLOCKED\_ROLES\_LIST](/sql-reference/sql/create-security-integration-oauth-snowflake#label-oauth-blocked-roles-list) in the CREATE SECURITY INTEGRATION topic.

Snowflake recommends you create a dedicated, non-administrative role with the required permissions and set it as the
default for the setup user. Alternatively, use the [SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) mechanism to grant the additional permissions without
altering the user’s primary default role, as follows:

Copy code

```
GRANT ROLE <integration_specific_role> TO USER <user_name>;
ALTER USER <user_name> SET DEFAULT_SECONDARY_ROLES = ('ALL');
```

To set up the Teams bot, follow these steps:

1. Click **I’m the Snowflake administrator**, below the notice stating that an administrator needs to configure
   Snowflake for the Teams integration, to begin the process.
2. Provide your Snowflake account URL where indicated, and select **Connect Snowflake account**.

   To find your account URL, log in to Snowsight and click the account selector in the bottom left corner of the page. The
   hostname portion of the URL is displayed at the top of the menu and is in the format `your-organization-your-account`.
   The full URL is `your-organization-your-account.snowflakecomputing.com`.

   The configuration wizard verifies that the URL leads to a valid Snowflake instance and confirms that your user has
   access to it and has the required administrative privileges. If your account is in a region other than Azure US East 2,
   you are prompted to accept a consent notification during this process.

After the setup passes final validation, the Teams app is connected to your Snowflake account and the agents are ready to use.

Tip

After you have connected your Snowflake account to the Cortex Teams app, you can connect additional Snowflake accounts to the same
app by logging into the Teams app with a user that has the necessary privileges and issuing the “add new account” command in the chat.

## Using the Cortex Agents

After the integration is set up, the bot appears in the Microsoft Teams interface, allowing your users to interact with
it in a private chat. Users can ask questions in natural language, and the bot responds with answers based on Snowflake
data.

In Microsoft 365 Copilot, your users can interact with the agents in the context of their broader workflows, asking
questions and receiving answers about their Snowflake data within the Copilot interface.

### Available commands

In addition to asking natural language questions, Cortex Agent bots accept predefined commands from Microsoft Teams chat. These commands help manage accounts and agents within the Teams interface.

The following commands are available:

| Command | Description |
| --- | --- |
| `Help` | Display a list of available commands and usage instructions. |
| `Choose agent` | Switch between available Cortex Agents within the current account. Displays a list of agents you have access to. |
| `Logout` | Log out from the current account. |
| `Show configured accounts` | Display a list of all configured Snowflake accounts. |
| `Clear context` | Clear agent’s internal chat history. |
| `Starter prompts` | Explore example questions you can ask the chosen agent. |
| `Admin Panel` | Display a list of available admin commands for your Snowflake account. |
| `Add account` | Connect an additional Snowflake account to the Teams app. Requires administrative privileges on the Snowflake account. |
| `Describe account` | Display information about the current Snowflake account. Displays a list of accounts with admin privileges to describe. |
| `Remove account` | Disconnect a Snowflake account from the Teams app. Requires administrative privileges. |

Expand

Show lessSee more

Note

Commands are case-insensitive and can be entered conversationally in the Teams chat. For example, you can send `Help`
or `help` in the chat to access the help command.

### Feedback on answers (Teams only)

Users can provide qualitative feedback on the agent’s responses directly in the Microsoft Teams interface (for example,
marking an answer as helpful or not helpful and optionally adding a comment). Users can also review the feedback they
have previously submitted. For instructions, see [View feedback provided by users](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agents-view-feedback).

Note

The feedback capability is available only in Microsoft Teams and is not supported in the Microsoft 365 Copilot experience.

### Switching between accounts and agents

You can connect multiple Snowflake accounts to the integration. Each connected account can expose one or more Cortex
Agents. Once the accounts are connected, users can switch among accounts and agents in the Teams UI with a single click;
no need to re-authenticate or re-enter connection details. Switching between accounts and agents makes it easier to
compare insights across business domains (for example, sales versus marketing) while preserving each user’s security
context.

Tip

You can also switch among agents in an account conversationally (for example, by entering “Choose agent”) if
you prefer a command interaction instead of the UI.

## Security considerations

The Cortex Agents integration for Microsoft Teams is designed with security in mind, leveraging Snowflake’s existing
security features and Microsoft Entra ID’s authentication capabilities. The integration ensures that user data remains
secure and that access is controlled through Snowflake’s role-based access control (RBAC) system.

### End-to-end authentication flow

To understand the security implications of using the Cortex Agents integration for Microsoft Teams, it is important to
understand the end-to-end authentication flow. This process involves the following steps:

- **User interaction:** A user sends a message to the Snowflake Cortex Agents bot in Microsoft Teams.
- **Authentication trigger:** The bot’s back end service (the “Client” app) initiates an OAuth 2.0 flow, redirecting the
  user to the Microsoft Entra ID.
- **User authentication:** The user signs in to their Microsoft account with their corporate credentials, satisfying any
  MFA or Conditional Access policies enforced by their tenant.
- **Token issuance:** Entra ID provides a short-lived authorization code. The bot’s backend securely exchanges this code
  for a JWT access token.
- **API call to Snowflake:** The bot back end calls the Snowflake Cortex Agents API, including the access token in the
  `Authorization: Bearer` header.
- **Snowflake token validation:** The Snowflake service receives the request and validates the JWT against the policy
  defined in the Snowflake security integration object.

### Role-Based Access Control

Because it uses the Cortex Agents API under a specific user role, the Teams integration executes Cortex Agents requests
with the exact privileges of the user’s designated Snowflake role. The agent inherits all existing data governance
controls, including:

- The agent can only access databases, schemas, tables, and warehouses that the user’s role permits them to use.
- **Data masking policies:** The agent respects dynamic data masking policies, granting access only when allowed by the user’s role.
- **Row-Level access policies:** The agent enforces row-level security policies.

The agent cannot bypass any existing Snowflake security controls, and users cannot access data that they are not already
authorized to see.

### Network policies

The integration supports Snowflake [network policies](/user-guide/network-policies) by forwarding the client
IP address received from Microsoft to Snowflake for policy enforcement. Network policies allow administrators to
control inbound access to the Snowflake service by restricting connections based on IP addresses and other network
identifiers.

Important

The Cortex Agents integration for Microsoft Teams and Microsoft 365 Copilot does not create, modify, or activate any
network policies on your Snowflake account; it only respects the network policies that exist in your Snowflake
instance. Network policy configuration is entirely under the control of your Snowflake account administrators.

When a user signs in to the Cortex Agents bot, Microsoft issues a token that includes an `ipaddr` claim representing
the user’s IP address at the time of sign-in. The integration forwards this IP address to Snowflake with each request,
allowing Snowflake to enforce any network policies that rely on client IP information. Microsoft might periodically
issue additional tokens with the same IP address for the duration of the user’s session. The IP address claim in the
token is updated only when a user completely signs out and back in within the bot.

Caveats for IP-based network policies

Before you rely on network policies with this integration, understand two ways the forwarded IP address can differ
from the user’s actual client IP:

- **Microsoft might send a Microsoft-managed IP.** The Entra ID `ipaddr` claim doesn’t always contain the end user’s
  current public IP address. In some Microsoft Teams scenarios, Microsoft populates this claim with an IP address from
  Microsoft-managed infrastructure instead. The integration forwards the claim to Snowflake exactly as received and doesn’t
  rewrite it, so Snowflake can evaluate a Microsoft-managed IP rather than the user’s actual client IP. Microsoft-managed
  IPs might change, and Snowflake doesn’t control the value Microsoft assigns to the claim. Because this behavior is
  determined by Microsoft, Snowflake recommends contacting Microsoft to understand how and when the `ipaddr` claim is
  populated in your tenant.
- **The IP address doesn’t refresh during a session.** The IP address used for network policy enforcement reflects
  the user’s address at the time of Microsoft sign-in and does not update if the user changes their IP address (for
  example, by connecting to a different network or by connecting to or disconnecting from a VPN) during their session
  with the bot, unless otherwise controlled by your Microsoft tenant configuration. Snowflake continues enforcing
  network policies against the original IP address until the user explicitly signs out of the bot and signs back in.
  In Snowsight, a client IP change typically invalidates the session immediately when network policies are enabled.
  In the Microsoft Teams and Microsoft 365 Copilot integration, session persistence and IP refresh behavior are
  controlled by Microsoft.

Customers that require strict IP allowlisting should validate this behavior in their Microsoft tenant before rollout.

Integration-level network policies aren't enforced

When the integration forwards the client IP address to Snowflake, Snowflake evaluates the request against the
**user-level** or **account-level** network policy, not the network policy attached to the security integration.
As a result, a network policy that you set on the security integration doesn’t govern traffic from this integration.

To restrict access based on IP address for the Cortex Agents integration for Microsoft Teams and Microsoft 365 Copilot,
apply the network policy at the user level or the account level. For more information about the scopes at which a
network policy can be applied, see [Network policies](/user-guide/network-policies).

## Current limitations

OAuth identity provider must be Entra ID
:   The integration exclusively supports Microsoft Entra ID as the identity provider for authentication and requires a
    direct one-to-one mapping between Entra ID users and Snowflake users. Organizations that use another primary IdP
    (for example, Okta or another SAML/OIDC provider) can enable this integration by configuring standard identity
    federation between that provider and Microsoft Entra ID. In this federated model, the primary IdP handles the user’s
    sign-in, after which Entra ID issues the final token required by the integration.

Default user role reliance
:   The integration’s functionality is tied to each user’s default Snowflake role due to an architectural constraint in
    the Cortex Agents API, which determines session permissions based on the role context established during
    authentication. Therefore, the user’s default role must be granted all necessary privileges on the underlying objects
    for the agent to function correctly. While Snowflake’s [secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement)
    feature can help to broaden data access, the primary execution context is governed by the user’s default role.

Integration-level network policies aren’t enforced
:   Network policies attached to the security integration don’t govern traffic from this integration. Snowflake evaluates
    the forwarded client IP address against the user-level or account-level network policy instead. To restrict access based
    on IP address, apply the network policy at the user level or the account level.

## Troubleshooting

If you encounter issues with the Cortex Agents integration for Microsoft Teams, check the following sections for possible solutions.

### Privilege and access issues

The user’s default role must have the required privileges to access the objects used or accessed by the agent.
Error messages caused by access issues typically include the phrase “database object does not exist or not authorized.”

Troubleshooting such issues involves checking that user’s default role is set to a role that has the required privileges.

#### Default role setting

The first step in troubleshooting access issues is to check the user’s default role setting. To verify this setting,
use the DESCRIBE USER command. Check the DEFAULT\_ROLE property in the output. If the user’s default role is incorrect,
change it using the ALTER USER command.

Copy code

```
ALTER USER <user_name> SET DEFAULT_ROLE = '<correct_role>';
```

If changing the user’s primary DEFAULT\_ROLE is not feasible, you can use the Snowflake’s secondary roles mechanism. A
user can perform actions using the combined privileges of their primary and active secondary roles. This lets you
grant an additional, integration-specific role to the user without altering their primary role.

To add a secondary role for the Cortex Agents integration, use SQL commands like the following.

Copy code

```
GRANT ROLE <integration_specific_role> TO USER <user_name>;
ALTER USER <user_name> SET DEFAULT_SECONDARY_ROLES = ('ALL');
```

#### Required permissions

Make sure the role under which the integration will run (each user’s default role or permitted secondary roles) has the
grants described in the [access control requirements section](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control).

### Security integration issues

A Snowflake security integration connects the Microsoft Entra ID tenant to the Snowflake account. The issues in this
section are related to the security integration.

#### Invalid OAuth access token (error code 390303)

This error can indicate that one or more property values in the security integration are incorrect, preventing Snowflake
from validating the access token received from Entra ID. To rectify this, check the following fields in the security
integration. In particular, make sure the tenant ID is correct in the URLs.

- **EXTERNAL\_OAUTH\_ISSUER:** This must be set to the correct Entra ID issuer URL, which is in the format
  `https://login.microsoftonline.com/tenant-id/v2.0`, where `tenant-id` is your organization’s Microsoft
  tenant ID.
- **EXTERNAL\_OAUTH\_JWS\_KEYS\_URL:** This must be set to the correct JWS keys URL, which is in the format
  `https://login.microsoftonline.com/tenant-id/discovery/v2.0/keys`, where `tenant-id` is your organization’s
  Microsoft tenant ID.
- **EXTERNAL\_OAUTH\_AUDIENCE\_LIST:** This must include the correct audience for the Cortex Agents Bot OAuth Resource
  application, which is the application ID `5a840489-78db-4a42-8772-47be9d833efe`.

Update any incorrect values using the ALTER SECURITY INTEGRATION command.

#### Incorrect username or password (error code 390304)

This error message points to a mismatch between the user identifier sent by Entra ID and the corresponding user’s record
in Snowflake, usually because the Entra ID user identity does not map to exactly one Snowflake user. This can happen when the Snowflake
user does not exist, when the mapped UPN or email address is incorrect, or when the mapping resolves to multiple Snowflake
users (for example, if the mapping is performed using email address and multiple users share the same address).

The error message includes the UPN and email of the user attempting to log in. Use this information to verify the
affected user’s configuration using the DESCRIBE USER command. Make sure the user’s NAME or EMAIL property matches the
value of the same property in Entra ID for the corresponding user. When using email address mapping, each user in the
Snowflake account that will use the integration must have a unique email address.

#### Role not listed in the access token or was filtered out (error code 390317)

This error occurs when Snowflake cannot assign a role to the user based on the information in the OAuth access token.
The access token is configured with the `session:role-any` scope, which allows the user to assume any of their
assigned roles in Snowflake. However, the security integration must be explicitly configured to permit this behavior.

Use the DESCRIBE SECURITY INTEGRATION command to check the value of the EXTERNAL\_OAUTH\_ANY\_ROLE\_MODE property, then
change it to `ENABLE` or `ENABLE_FOR_LOGIN`.

Copy code

```
DESCRIBE SECURITY INTEGRATION entra_id_cortex_agents_integration;

ALTER SECURITY INTEGRATION entra_id_cortex_agents_integration
    SET EXTERNAL_OAUTH_ANY_ROLE_MODE = 'ENABLE';
```

#### Role specified in the connect string is not granted to this user (error code 390186)

This error occurs when Snowflake security integration doesn’t allow the user’s default role to use the security
integration.

To resolve this, check the following properties in the output of DESCRIBE SECURITY INTEGRATION:

- EXTERNAL\_OAUTH\_ALLOWED\_ROLES\_LIST: If the parameter is enabled, verify that it contains the user’s default role.
- EXTERNAL\_OAUTH\_BLOCKED\_ROLES\_LIST: If the parameter is enabled, verify that it does not contain the user’s default role.

### Network policy issues

If a user is blocked by a network policy when using the Cortex Agents integration for Microsoft Teams or
Microsoft 365 Copilot, try the following steps:

1. **Verify that the user’s IP address is allowlisted.** Confirm that the user’s current IP address is included in the
   user-level or account-level network policy. This integration doesn’t enforce network policies attached to the security
   integration, so verify the allowlist at the user level or the account level. A simple way to test this is to have the
   user log in to their Snowflake account directly at [Snowflake](https://app.snowflake.com/). If the user can log in
   successfully, their IP address is allowlisted.
2. **Check for IPv6 addresses.** If you encounter an IPv6 address in an error related to a
   network policy, this indicates that Microsoft is sending an IPv6 address as a claim within the authentication token.
   To allow IPv6 addresses, create a network rule with `TYPE = IPV6` and add it to your network policy. For more
   information, see [IPv6 addresses](/user-guide/network-rules#label-network-rule-ipv6-addresses).
3. **Refresh the Entra ID token.** The bot may be using a token with an outdated IP address. To force a token
   refresh, have the user type `Logout` in the chat window, then type `/login` and sign in to Microsoft again.
4. **Contact Microsoft if the IP address is managed by Microsoft.** If the blocked IP address belongs to Microsoft rather
   than the user’s network, Microsoft populated the `ipaddr` claim with a Microsoft-managed infrastructure IP. Snowflake
   forwards this claim as received and doesn’t control its value, so Snowflake recommends that you contact Microsoft to
   understand how and when the `ipaddr` claim is populated in your tenant.
