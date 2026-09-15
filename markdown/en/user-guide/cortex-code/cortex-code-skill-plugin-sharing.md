# Share skills and plugins

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Overview

Skill and plugin sharing lets you share, discover, and govern skills and plugins across your Snowflake
account. Instead of keeping skills local to a single user’s machine, you can publish them so that teammates,
roles, or your entire account can find and use them.

Key capabilities:

- **Sharing:** Publish a skill or plugin and receive a link you can send to colleagues.
- **Discovery:** Search for shared skills and plugins from CoCo Desktop, CoCo in Snowsight, and
  the CoCo CLI.
- **Governance:** Certify skills, control access by role, and track install and usage counts from the
  **Skills & Plugins** area under [Horizon Catalog](/user-guide/snowflake-horizon) in Snowsight.

Note

Any user can share skills and plugins that they own. Governance actions require the ACCOUNTADMIN role.

## How it works

Skills and plugins are stored as **Cortex Extension** objects in your Snowflake account. A Cortex Extension contains
the skill or plugin files and metadata such as name, description, version, and content type (Skill or
Plugin).

When you share a skill or plugin, the system returns a `snow://` URI in the format:

```
snow://skill_catalog/DB.SCHEMA.CORTEX_EXTENSION_NAME
```

To reference a specific version, append a version segment to the URI:

```
snow://skill_catalog/DB.SCHEMA.CORTEX_EXTENSION_NAME/versions/version$1
```

You can send this link through any channel (Slack, email, and so on). The recipient pastes the URI into
CoCo to install and use the skill or plugin.

Note

Cortex Extension objects are created in your personal database by default, in a `SKILL_SHARING` schema that Snowflake creates automatically for skill and plugin sharing.

Plugins appear alongside skills in the **Skills & Plugins** area under Horizon Catalog in Snowsight. Skills
and plugins follow the same sharing, discovery, and governance model.

## Share a skill or plugin

### Sharing options

Sharing is governed by two independent concepts:

- **Access (RBAC):** Determines which roles can install and use the skill or plugin.
- **Discoverability:** Determines whether the skill or plugin appears in the catalog for browsing. A discoverable skill or plugin is searchable and visible in the UI for users who have the appropriate role.

Because access and discoverability are independent, you can combine them to share in two main ways:

- **Private (not discoverable):** Send the link directly to a colleague. The skill or plugin doesn’t appear in the catalog for others to browse, and only people who have the link can access it. This is similar to an “unlisted” video: accessible to anyone with the link, but not browsable.
- **Public or role-based (discoverable):** Share to the PUBLIC role or to a specific role. The skill or plugin is discoverable in the catalog and browsable by anyone with the appropriate role, who can find it through manual search or automatic discovery.

### Sharing interfaces

The following interfaces support sharing:

| Interface | Skills | Plugins |
| --- | --- | --- |
| CoCo CLI | Yes | Yes |
| CoCo Desktop | Yes | Yes |
| CoCo in Snowsight | Yes | No |

Expand

Show lessSee more

#### CoCo CLI

Use the `/share-skill-and-plugin` skill to publish a skill or plugin:

```
> /share-skill-and-plugin my-skill
```

CoCo prompts you to choose the target role (default PUBLIC) and whether to make the skill discoverable
(default Yes). After sharing, you receive a link:

```
Skill "my-skill" shared to Snowflake connection 'my-connection'.
Share link: snow://skill_catalog/USERS.MY_SCHEMA.MY_SKILL
```

You can also share from the Skill manager by running `/skill` and selecting the share option for a specific skill.

To update a previously shared skill, re-run the same share workflow. The Cortex Extension object is updated with the
new skill files.

#### CoCo in Snowsight

Type `Share skill <skill>` in CoCo to initiate sharing of the skill.

#### CoCo Desktop

Share skills or plugins from the skill manager. Select the share option to publish and get the share link. For more
information, see [Publish a skill to the Skills Catalog](/user-guide/cortex-code/cortex-code-desktop/skills#publish-a-skill-to-the-skills-catalog)
and [Publish a plugin to the catalog](/user-guide/cortex-code/cortex-code-desktop/plugins#publish-a-plugin-to-the-catalog).

## Use a shared skill or plugin

### Install a shared skill or plugin

To install a shared skill or plugin, paste the link into CoCo:

- **CoCo CLI:** Paste the link directly into the chat. CoCo resolves the Cortex Extension object,
  downloads the files, and makes the skill or plugin available locally.
- **CoCo in Snowsight:** Paste the link in the CoCo chat pane.
- **CoCo Desktop:** Paste the link to install the skill or plugin. You can also add plugins from the [Plugins Catalog](/user-guide/cortex-code/cortex-code-desktop/plugins#import-a-plugin-from-the-catalog).

If a skill or plugin with the same name is already installed, you receive a message indicating it already exists.

### Update an installed skill or plugin

In the CoCo CLI, update installed skills and plugins to their latest shared versions:

- To update a skill, run `cortex skill update <skill-uri>`, where `<skill-uri>` is the skill’s `snow://` share link.
- To update a particular plugin, run `cortex plugin update <plugin-name>`.
- To update all installed plugins, run `cortex plugin update`.

## Discover skills and plugins

### Automatic discovery

CoCo can automatically find relevant skills and plugins while you work, searching the catalog for items related to
the current task and suggesting them in context. In the CoCo CLI and CoCo Desktop, use the `/find-skill-and-plugin`
skill. In CoCo in Snowsight, use `/find-skill`, which finds skills only (plugins aren’t supported there).

### Manual search

- **Snowsight:** Browse the list of skills and plugins accessible to you from **Catalog** > **Skills & Plugins**
  in Snowsight. Certified skills display a **Certified** badge.
- **CoCo in Snowsight:** The `+` menu and `/` command display Local, Built-in, and Skill Catalog skills and
  plugins.
- **CoCo Desktop:** The `+` menu and `/` command display Local, Built-in, and Skill Catalog skills and
  plugins.

## Versioning

Skills and plugins support versioning:

- The first version of a shared skill or plugin is version 1.
- The owner (a role that holds OWNERSHIP on the Cortex Extension object) can upload a new version at any time by
  re-running the share workflow. Each upload creates a new version.
- When browsing the catalog, users see the latest version, or the latest certified version if one exists.
  Administrators and owners can see all versions.

How a `snow://` URI resolves to a version depends on whether the URI includes a version:

- If the URI doesn’t include a version, it resolves to the latest certified version if one exists, and the latest available version otherwise.
- If the URI includes a version, that specific version is retrieved.

## Governance

Skills and plugins shared in your account are governed by users with the ACCOUNTADMIN role. An administrator can
browse all shared skills and plugins, certify them, change their access and visibility, reassign ownership, view
usage telemetry, and delete them.

Administrators perform these actions from the **Skills & Plugins** page in Snowsight under Horizon Catalog.

### How governance works

Shared skills and plugins are stored as Cortex Extension objects, which are created in the owner’s personal database
by default. When an administrator performs a governance action, such as certifying a skill or changing its access,
Snowflake copies the object to a dedicated database. The first time you perform a governance action, you’re prompted
to choose the database where governed skills and plugins are stored.

This model copies the object out of the owner’s personal database so that it can be centrally governed, while leaving
the owner’s original skill or plugin in place.

### Certify a skill or plugin

Certify a skill or plugin to mark it as an officially verified version for your account. Certified skills and plugins
display a **Certified** badge.

Certification is tied to a version, so you can certify versions of the same skill or plugin independently. When an end
user browses the catalog, they see the latest certified version if one exists, and the latest version otherwise. An
administrator can see all versions.

### Change access and visibility

Access and discoverability are governed independently:

- **Access (RBAC):** Change which roles can install and use a shared skill or plugin.
- **Visibility:** Change whether a skill or plugin is discoverable in the catalog.

### Reassign ownership or delete

- **Change owner:** Reassign ownership of a shared skill or plugin.
- **Delete:** Remove a skill or plugin from the catalog.

### Telemetry

For each shared skill or plugin, the **Skills & Plugins** page shows the install count and usage count over the last
28 days, aggregated across all clients.

## CORTEX EXTENSION SQL examples

You can manage Cortex Extension objects directly with SQL, as an alternative to the CoCo and
Snowsight workflows. The following examples show common operations:

Copy code

```
-- Create a Cortex Extension from an existing one
-- Note: CLONE isn't supported yet; use this pattern instead
CREATE CORTEX EXTENSION new_db.new_schema.new_ext
  FROM 'snow://skill_catalog/old_db.old_schema.old_ext';

-- Set RBAC
GRANT READ ON CORTEX EXTENSION new_db.new_schema.new_ext TO ROLE PUBLIC;

-- Certify a specific version of a skill or plugin (requires the ACCOUNTADMIN role)
ALTER CORTEX EXTENSION new_db.new_schema.new_ext VERSION VERSION$1
  SET TAG snowflake.core.certification_status = 'CERTIFIED';

-- Drop an old extension
DROP CORTEX EXTENSION old_db.old_schema.old_ext;
```

## Limitations

- Sharing only works within the same Snowflake account. Cross-account sharing isn’t supported.
- Security scanning on skills and plugins isn’t available yet.
- Skills and plugins created locally (in your workspace or on your machine) don’t appear in the catalog until
  explicitly shared.
- Exporting skills or plugins to storage outside Snowflake isn’t supported.

## Legal notices

Where your configuration of Cortex Code uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
