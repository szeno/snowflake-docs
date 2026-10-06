# Agentic Marketplace Discovery

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Snowflake Marketplace **Discover** page in Snowsight offers two ways to find products: use **Agentic discovery** to describe your needs to CoCo in natural language and get matching listings, or switch to **Marketplace search** to search for providers or listings directly. In Agentic discovery, you can ask CoCo to compare products and, from the conversation, install listings, start trials, or initiate sales requests for products on the public Snowflake Marketplace.

CoCo is also available throughout Snowsight. You can continue the conversation you started on the Marketplace Discover page as you work elsewhere in Snowsight to evaluate, try, and implement the products you find. Natural language Marketplace discovery with CoCo elsewhere in Snowsight is generally available; see [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight). This topic covers the Discover-page experience and its listing actions, which are available in public preview.

This feature applies to the public Snowflake Marketplace only. It doesn’t apply to the Internal Marketplace.

## Prerequisites

To use CoCo for Marketplace search and listing actions, you need the following:

- Access to CoCo in Snowsight. Your role must have the `SNOWFLAKE.COPILOT_USER` database role and either the `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.CORTEX_AGENT_USER` database role. See [Access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).
- A Snowflake account that can access the Snowflake Marketplace. See [Use listings as a consumer](/collaboration/consumer-becoming).

To install a listing or start a trial, your role must also have the privileges required for those consumer actions (for example, CREATE DATABASE and IMPORT SHARE). See [Access and install listings as a consumer](/collaboration/consumer-listings-access) and [Explore listings](/collaboration/consumer-listings-exploring).

## What you can do

From CoCo on the Snowflake Marketplace Discover page, you can do the following for public Snowflake Marketplace listings:

| Action | Description |
| --- | --- |
| Search | Describe the problem, data product, app, or use case you need in natural language. CoCo returns matching Snowflake Marketplace listings, often grouped by category. |
| Get recommendations | Ask CoCo to recommend the best fit for your use case |
| Dive deeper | Ask CoCo for detailed information about a specific listing including examples of how it fits your use case and how it could enrich data already in your account. |
| Compare and refine | Ask CoCo to compare listings (for example, coverage, granularity, or refresh cadence), open listing details, or recommend the best fit for your use case. |
| Install | Install a free or accessible listing into your account from an in-chat **Get this listing** form. |
| Start a trial | Start a trial for a paid or limited trial listing so you can evaluate the product before you purchase or request full access. |
| Initiate a sales request | Start a sales request when a listing requires you to contact the provider to purchase or obtain the product (for example, a sales-led offer). |
| Initiate a request for a private listing | Start an acquisition request for a private listing |

Expand

Show lessSee more

CoCo uses the same consumer agreements and access rules as the Snowflake Marketplace UI. When CoCo presents an install, trial, or sales request form, complete the required acknowledgments and configuration before you continue.

## Find listings with Agentic discovery

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace**.
3. On the **Discover** tab, select **Agentic discovery** to use CoCo. To search for providers or listings directly instead, switch to **Marketplace search**. You can toggle between the two at any time.
4. In **Agentic discovery**, use the prompt field (**Let’s solve a problem**) to describe what you’re working on.

   You can also select a suggested prompt under the field, such as **Find data & apps**, **Connect my systems**, **Build with AI**, or **Get tailored recommendations**.
5. Review the CoCo response. Matching listings appear as cards that can include the listing title, provider, short description, and labels such as **Free to try**, **Paid**, **Secure share**, or **Native App**.
6. Optionally select **Tell me more** on a listing card, or ask follow-up questions in the CoCo conversation to refine results, compare options, or get more detail.

Example prompts:

- “Find weather data for North America.”
- “Show me listings related to credit card transactions.”
- “Find Native Apps that help with Salesforce data.”
- “Find Marketplace datasets for healthcare and life sciences.”

For more ways to discover listings with CoCo elsewhere in Snowsight, see [Example prompts](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-example-prompts). The `marketplace-search` and `get-marketplace-listing-details` skills are also described in [marketplace-search](/user-guide/cortex-code/bundled-skills#label-bundled-skill-marketplace-search).

## Install, trial, or request a listing with CoCo

After CoCo surfaces a listing that fits your need, install it, start a trial, or initiate a sales request from the same chat:

1. On the listing card, select **Tell me more**.
2. In the chat, review the listing details CoCo provides, then follow the install, trial, or sales request flow that appears.
3. When CoCo shows a **Get this listing** form, complete the required steps:
   - Select the agreement and privacy acknowledgments for the listing.
   - Review or change the suggested **Database name** if a database will be created from the listing.
   - Select **Install listing** (or the equivalent action for a trial or sales request).
4. If install or trial succeeds, open the resulting database or app and continue with your usual consumer workflow. See [Access and install listings as a consumer](/collaboration/consumer-listings-access).

## Limitations

- Available only for the public Snowflake Marketplace, not the Internal Marketplace.
- Available in public preview.
- Listing actions succeed only when your role has the privileges required for that action and the listing supports the action (for example, a trial must be offered on the listing).
- Billing, payment setup, and capacity drawdown rules for paid listings still apply. See [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying).
