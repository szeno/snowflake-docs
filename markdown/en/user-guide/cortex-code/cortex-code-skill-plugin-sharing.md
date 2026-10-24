# Share skills and plugins

## Overview

Skill and plugin sharing lets you share, discover, and govern skills and plugins across your Snowflake
account. Instead of keeping skills local to a single user’s machine, you can publish them so that teammates,
roles, or your entire account can find and use them.

Key capabilities:

- **Sharing:** Publish a skill or plugin and receive a link you can send to colleagues.
- **Discovery:** Search for shared skills and plugins from CoCo Desktop, CoCo in Snowsight, and
  the CoCo CLI.
- **Security scanning:** Every shared skill and plugin is scanned for security issues before anyone else can
  install it.
- **Governance:** Certify skills, control access by role, organize the catalog into categories, and track
  install and usage counts from the **Skills and plugins** page under **AI & ML** in Snowsight.

Note

Any user can share skills and plugins that they own. Governance actions require either the ACCOUNTADMIN role or
a role that ACCOUNTADMIN has granted the relevant governance privileges to. For details, see
[Delegate administration](#label-cortex-code-skill-sharing-delegate-administration).

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

`snow://skill_catalog/` and `snow://cortex_extension/` are interchangeable prefixes for the same object, so a link in
either form works wherever a URI is accepted.

Note

Cortex Extension objects are created in your personal database by default, in a `SKILL_SHARING` schema that Snowflake creates automatically for skill and plugin sharing.

Plugins appear alongside skills on the **Skills and plugins** page under **AI & ML** in Snowsight. Skills
and plugins follow the same sharing, discovery, and governance model.

## Share a skill or plugin

### Sharing options

Sharing is governed by two independent concepts:

- **Access (RBAC):** Determines which roles can install and use the skill or plugin.
- **Discoverability:** Determines whether the skill or plugin appears in the catalog for browsing. A discoverable skill or plugin is searchable and visible in the UI for users who have the appropriate role.

Because access and discoverability are independent, you can combine them to share in two main ways:

- **Private (not discoverable):** Send the link directly to a colleague. The skill or plugin doesn’t appear in the catalog for others to browse, and only people who have the link can access it. This is similar to an “unlisted” video: accessible to anyone with the link, but not browsable.
- **Public or role-based (discoverable):** Share to the PUBLIC role or to a specific role. The skill or plugin is discoverable in the catalog and browsable by anyone with the appropriate role, who can find it through manual search or automatic discovery.

### Descriptions

Every shared skill and plugin carries a short, human-readable description that tells people what it does. When you
share through CoCo, Snowflake analyzes the contents and generates a one to two sentence summary, which you can edit
before or after publishing. Generating the description is part of the CoCo share workflow, so creating a Cortex
Extension directly with SQL doesn’t produce one.

This description is separate from the front matter in the skill’s `SKILL.md` file or the plugin’s manifest. Front
matter is written for CoCo and agents, so it’s optimized for matching a task to a skill rather than for someone
browsing the catalog. The description is what people read in the catalog.

The description applies to the object rather than to a single version, much like a README in a repository. Owners
can update it at any time without publishing a new version. The per-version front matter continues to come from the
skill or plugin files themselves.

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
information, see [Publish a skill](/user-guide/cortex-code/cortex-code-desktop/skills#publish-a-skill-to-the-skills-catalog)
and [Publish a plugin](/user-guide/cortex-code/cortex-code-desktop/plugins#publish-a-plugin-to-the-catalog).

## Import skills and plugins in bulk

Use `/bulk-share-skills-and-plugins` to share a collection of local skills and plugins with your Snowflake account.
The skill scans a directory, lets you review which items to publish, and creates or updates a Cortex Extension for
each approved item instead of requiring you to share each one by hand.

To import from a Git repository, clone the repository to your machine first. Then invoke the skill in the CoCo CLI or
CoCo Desktop with the path to your local clone, not the Git repository URL. For example, enter the following prompt in
CoCo, replacing the path with your clone’s location:

```
/bulk-share-skills-and-plugins Scan /path/to/team-skills recursively and help me share the skills and plugins with my Snowflake account.
```

Any local directory works, whether or not it’s a Git repository. CoCo must be able to read that directory.

The skill guides you through the following steps:

1. Choose whether to scan only the directory’s immediate children or scan recursively, and choose the audience for
   newly shared items.
2. Review the discovered inventory before anything is published. You can exclude individual items or subdirectories,
   or keep only skills or only plugins.
3. Confirm the inventory to publish the selected items. The skill reports a `snow://` share link for each successful
   item and a reason for each failure or skipped item.

A recursive scan treats each outermost skill or plugin as one artifact. For example, skills contained within a plugin
aren’t also published as separate skills.

To refresh the collection after changes in Git, update your local clone and run the skill again. Existing skills and
plugins receive content updates while keeping their current audience and catalog visibility. Newly discovered items
are shared with the audience you choose for that run. If an existing extension has the same name but a different type
(skill versus plugin), the item is skipped rather than overwritten. Items removed from the directory aren’t
unshared automatically.

Imported skills and plugins behave like any other shared skill or plugin. Security scanning, categories, certification,
and access control all apply in the same way.

## Security scanning

Skills and plugins are scanned for security issues when they’re shared. Because a skill or plugin can instruct an
agent to read files, run commands, and reach external services, scanning reduces the risk that a shared skill
exfiltrates data or takes destructive action in your account.

Scanning depends on client support, so upgrade the CoCo CLI and CoCo Desktop to their latest versions before you rely
on it.

Skills shared during the preview aren't scanned

Scanning applies from the point it became available, and Snowflake doesn’t scan existing content retroactively. A skill
or plugin you shared during the preview therefore has no scan result.

An unscanned skill or plugin stays available: people can still install and use it. Version selection treats unscanned
the same way it treats a passed scan, so a skill shared during the preview keeps serving normally. Unscanned isn’t the
same state as failed or pending, which do block installation.

To get a scan result, share the skill or plugin again. That publishes a new version and triggers a scan on it.

### What happens when you share

Sharing doesn’t wait for the scan to finish. You get the `snow://` link immediately and can send it to colleagues
right away, while the scan runs in the background.

The scan result then determines whether anyone else can install the skill or plugin:

- **Passed:** The skill or plugin can be installed. If it’s discoverable and the person holds a role that has
  access, it also appears in the catalog.
- **Failed or still pending:** The skill or plugin can’t be installed. It doesn’t appear in the catalog, and anyone
  who has the link is told that it isn’t available.

Your own copy isn’t affected. A failed scan stops other people from installing the skill or plugin, but doesn’t stop
you from using it locally. However, it is best practice to not run a skill or plugin that has failed a scan and
Snowflake advises against doing so.

### Scan limits

The scanner accepts a skill or plugin up to the following limits:

| Limit | Value |
| --- | --- |
| Files per skill or plugin | 100 |
| Size of any single file | 2 MiB |
| Total size of all files | 10 MiB |

Expand

Show lessSee more

A skill or plugin that exceeds any of these limits can’t be scanned, which means other people can’t install it.

### Scan failures

A failed scan reports what it found. To review the findings, check the scan status as described in
[Review scan status](#label-cortex-code-skill-sharing-review-scan-status). To resolve a failure, fix the reported issue
in the skill or plugin and share it again. Sharing again creates a new version and triggers a new scan. If you believe a
finding is a false positive, ask an administrator to override the scan status. For details, see
[Override a security scan](#label-cortex-code-skill-sharing-override-scan).

### Review scan status

Administrators can review the scan status and the detailed findings for any shared skill or plugin from the
**Skills and plugins** page in Snowsight.

`SHOW` and `DESCRIBE` also report which version is actually being served, and why, in three columns that any
authorized user can read:

| Column | Meaning |
| --- | --- |
| `effective_version` | The committed version Snowflake selects for use, preferring the newest certified version with an eligible scan status. |
| `action_required` | `TRUE` when `effective_version` is behind the latest committed version. |
| `action_required_reason` | Why the latest version wasn’t selected: `NONE`, `LATEST_VERSION_SCAN_NOT_PASSED`, or `LATEST_VERSION_NOT_CERTIFIED`. |

Expand

Show lessSee more

These columns are how you tell a healthy skill from one that’s quietly serving an older version. If `action_required`
is `TRUE` with a reason of `LATEST_VERSION_SCAN_NOT_PASSED`, the newest version you published failed or hasn’t cleared
its scan, and people are getting the last eligible version instead.

### Consent for cross-regional transfer of skills

Scanning runs automatically for all skills and plugins when you publish to the Skills Catalog. You don’t request it,
and there’s nothing to enable. By publishing a skill or plugin, you consent and agree that the skill or plugin may move
across regions for scanning purposes as identified below.

When publishing a skill or plugin, you automatically share the code with Snowflake for scanning. The following table
maps the security scanning regions to the corresponding provider regions:

| Cloud provider | Provider region | Scanning region |
| --- | --- | --- |
| AWS | US West (Oregon) | US West (Oregon) |
| AWS | US East (Ohio) | US East (Ohio) |
| AWS | US East (N. Virginia) | US East (N. Virginia) |
| AWS | Canada (Central) | Canada (Central) |
| AWS | South America (São Paulo) | South America (São Paulo) |
| AWS | EU (Ireland) | EU (Ireland) |
| AWS | Europe (London) | Europe (London) |
| AWS | EU (Paris) | EU (Paris) |
| AWS | EU (Frankfurt) | EU (Frankfurt) |
| AWS | EU (Zurich) | EU (Zurich) |
| AWS | EU (Stockholm) | EU (Stockholm) |
| AWS | Asia Pacific (Tokyo) | Asia Pacific (Tokyo) |
| AWS | Asia Pacific (Osaka) | Asia Pacific (Osaka) |
| AWS | Asia Pacific (Seoul) | Asia Pacific (Seoul) |
| AWS | Asia Pacific (Mumbai) | Asia Pacific (Mumbai) |
| AWS | Asia Pacific (Singapore) | Asia Pacific (Singapore) |
| AWS | Asia Pacific (Sydney) | Asia Pacific (Sydney) |
| AWS | Asia Pacific (Jakarta) | Asia Pacific (Jakarta) |
| Azure | - West US 2 (Washington) - Central US (Iowa) - South Central US (Texas) - East US 2 (Virginia) - Canada Central (Toronto) | Azure East US 2 (Virginia) |
| Azure | - UK South (London) - North Europe (Ireland) - West Europe (Netherlands) - Switzerland North (Zurich) - UAE North (Dubai) | Azure West Europe (Netherlands) |
| Azure | - Central India (Pune) - Japan East (Tokyo) - Southeast Asia (Singapore) - Australia East (New South Wales) | Azure Australia East (New South Wales) |
| GCP | - US Central1 (Iowa) - US East4 (N. Virginia) - Europe West2 (London) - Europe West4 (Netherlands) | AWS US West (Oregon) |

Expand

Show lessSee more

## Use a shared skill or plugin

### Install a shared skill or plugin

To install a shared skill or plugin, paste the link into CoCo:

- **CoCo CLI:** Paste the link directly into the chat. CoCo resolves the Cortex Extension object,
  downloads the files, and makes the skill or plugin available locally.
- **CoCo in Snowsight:** Paste a skill link in the CoCo chat pane. Plugins aren’t supported in CoCo in Snowsight.
- **CoCo Desktop:** Paste the link to install the skill or plugin. You can also [import a shared plugin](/user-guide/cortex-code/cortex-code-desktop/plugins#import-a-plugin-from-the-catalog).

If a skill or plugin with the same name is already installed, you receive a message indicating it already exists.

### Use a shared skill in Snowflake CoWork

Note

Snowflake CoWork has no catalog browse surface. You can’t search the catalog or install from it there, and a shared
skill reaches Snowflake CoWork only when it’s been added to a Cortex Agent.

The two products differ in who chooses the skills. In CoCo, you find a skill and add it to your own environment. In
Snowflake CoWork, the agent carries the skills: whoever configures the agent references a Cortex Extension in its
specification, and everyone who uses that agent gets those skills automatically. Individual users don’t browse, search,
or add skills to a conversation.

Referencing an extension rather than listing each skill has two consequences worth knowing:

- Snowflake expands the reference into the extension’s member skills when a request runs, so an agent that references
  a plugin picks up every skill the plugin bundles.
- Publishing a new version updates every agent that references the extension, unless the reference pins a version. For
  details, see [Cortex Extensions](/user-guide/snowflake-cortex/cortex-agents-skills#cortex-extensions).

Access still comes from the extension object, so a user needs the `READ` privilege on it.

Note

Sharing an agent that references a skill isn’t supported yet. Only agents whose tools are semantic views, Cortex Search
Services, or functions can be shared with another account, so adding a Cortex Extension to an agent makes that agent
unshareable for now. For details, see [Share Cortex agents](/user-guide/snowflake-cortex/cortex-agents-sharing).

For how to write the reference, including the version field and how naming conflicts resolve, see
[Cortex Extensions](/user-guide/snowflake-cortex/cortex-agents-skills#cortex-extensions).

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

- **Snowsight:** Browse the list of skills and plugins accessible to you from **AI & ML** > **Skills and plugins**.
  Certified skills display a **Certified** badge.
- **CoCo in Snowsight:** The `+` menu and `/` command display local, built-in, and shared skills. Plugins aren’t supported in CoCo in Snowsight, even though the **AI & ML** > **Skills and plugins** catalog lists both skills and plugins.
- **CoCo Desktop:** The `+` menu and `/` command display local, built-in, and shared skills and plugins.

Browsing and searching the catalog is a CoCo and Snowsight capability. Snowflake CoWork has no catalog
browse surface. For details, see
[Use a shared skill in Snowflake CoWork](#label-cortex-code-skill-sharing-cowork).

## Categories

Categories group related skills and plugins so people can narrow the catalog to the area they care about instead of
scanning one long list. Categories are specific to your account, so you can name them after the teams, domains, or
workflows your organization actually uses.

### How categories work

Categories work as follows:

- The catalog uses a single, flat layer of categories. Categories don’t nest.
- A skill or plugin belongs to one category at a time.
- The category applies to the skill or plugin as a whole, not to an individual version.
- Anything that hasn’t been categorized shows a dash (`-`) instead of a category name.
- Categories are account-wide, so a skill carries the same category wherever it appears.

When you share a skill or plugin, Snowflake suggests a category from the list your administrator maintains, choosing
the closest fit. You can accept the suggestion or pick a different category, and an administrator can recategorize it
later.

### Manage categories

Administrators maintain the list of categories that people can choose from, adding categories as new areas emerge and
renaming or removing ones that no longer fit.

Internally, a category is a tag on the Cortex Extension object, and the list of available categories is that
tag’s set of allowed values. Administrators can delegate the ability to maintain the list to another role. For
details, see [Delegate administration](#label-cortex-code-skill-sharing-delegate-administration).

Don't make the category tag multi-value

A skill or plugin belongs to one category at a time, and the category tag isn’t designed to hold more than one value.
Setting `MULTI_VALUE` on it can’t be undone: Snowflake doesn’t support setting it back to `FALSE`, because there’s no
way to rewrite the tag mappings once an object carries more than one category. The catalog can’t parse the resulting
data shape, and recovering means asking Snowflake to recreate the tag and redo every mapping. Don’t run the following:

Copy code

```
-- DO NOT RUN
ALTER TAG SNOWFLAKE.TAGS.CORTEX_EXTENSION_CATEGORIES
  SET MULTI_VALUE = TRUE;
```

## Versioning

Skills and plugins support versioning:

- The first version of a shared skill or plugin is version 1.
- The owner (a role that holds OWNERSHIP on the Cortex Extension object) can upload a new version at any time by
  re-running the share workflow. Each upload creates a new version.
- When browsing the catalog, users see the latest version, or the latest certified version if one exists.
  Administrators and owners can see all versions.

How a `snow://` URI resolves to a version depends on whether the URI includes a version:

- If the URI includes a version, that specific version is retrieved.
- If the URI doesn’t include a version, it resolves to the version Snowflake selects for use, preferring the newest
  certified version with an eligible scan status.

Because selection accounts for scan status, publishing a version that doesn’t clear its scan doesn’t take the skill
out of service: people keep getting the last eligible version. To see which version is being served and why, check the
`effective_version`, `action_required`, and `action_required_reason` columns described in
[Review scan status](#label-cortex-code-skill-sharing-review-scan-status).

## Governance

An administrator can browse all shared skills and plugins, certify them, change their access and visibility,
categorize them, override a security scan, reassign ownership, view usage telemetry, and delete them.

Administrators perform these actions from the **Skills and plugins** page under **AI & ML** in Snowsight.

ACCOUNTADMIN holds full authority over every governance action, but governance doesn’t have to stay there. For details,
see [Delegate administration](#label-cortex-code-skill-sharing-delegate-administration).

### How governance works

Shared skills and plugins are stored as Cortex Extension objects, which are created in the owner’s personal database
by default. When an administrator performs a governance action, such as certifying a skill or changing its access,
Snowflake copies the object to a dedicated database. The first time you perform a governance action, you’re prompted
to choose the database where governed skills and plugins are stored.

This model copies the object out of the owner’s personal database so that it can be centrally governed, while leaving
the owner’s original skill or plugin in place.

### Delegate administration

A role you create can manage skills and plugins without activating ACCOUNTADMIN. That arrangement is delegated
administration.

There’s no single administrator privilege for shared skills and plugins. Because they’re stored as Cortex Extensions,
you grant the individual privileges and application roles for the actions the role should perform, which also means
you can grant only some of them: a security team can clear false-positive scan findings without also being able to
change who can install every skill in the account.

Enable inherited grants first

Two of these grants use the `INHERITED` keyword: `INHERITED MANAGE GRANTS` and `INHERITED WRITE`. The keyword requires
that [inherited grants](/user-guide/inherited-grants-intro) be enabled for your account. Set the following with
ACCOUNTADMIN:

Copy code

```
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'ENABLED';
```

The same parameter also enables [container-level `MANAGE GRANTS`](/user-guide/container-manage-grants-intro). Without
it, `GRANT INHERITED ...` is rejected and a delegated role can’t manage access or discoverability.

#### Choose the actions

Grant only the actions the role should perform:

| Action | Required grants |
| --- | --- |
| Grant or revoke skill access | `INHERITED MANAGE GRANTS ON ALL CORTEX EXTENSIONS` |
| View metadata for every skill and plugin | `MONITOR CORTEX EXTENSIONS` |
| Override a security scan or read findings for any skill | `MANAGE CORTEX EXTENSION SECURITY SCAN` and `MONITOR CORTEX EXTENSIONS` |
| Manage category values and update existing assignments | `SNOWFLAKE.OOB_TAG_ADMIN` and `APPLY TAG ON ACCOUNT` |
| Set any skill’s category | `APPLY TAG ON ACCOUNT` |
| Certify a skill | `SNOWFLAKE.OOB_TAG_ADMIN`, `SNOWFLAKE.CORE_VIEWER`, and `APPLY TAG ON ACCOUNT` |
| Change discoverability | `INHERITED WRITE ON ALL CORTEX EXTENSIONS` |
| Change owner or delete | `MANAGE GRANTS ON ACCOUNT` |

Expand

Show lessSee more

#### Grants that reach beyond shared skills and plugins

Three of these grants aren’t limited to skills and plugins. Weigh them before granting:

| Grant | Why it’s needed | How broad it is |
| --- | --- | --- |
| `SNOWFLAKE.OOB_TAG_ADMIN` | Change the allowed category values, and set certification status. | The role can modify and apply most Snowflake-provided tags. |
| `APPLY TAG ON ACCOUNT` | Categorize and certify skills and plugins owned by other roles. Renaming or deleting a category also updates its existing assignments. | The role can apply tags to any object in the account, not just Cortex Extensions. |
| `MANAGE GRANTS ON ACCOUNT` | Change an extension’s owner, and take ownership before deleting it. Without this grant, the role can’t delete an extension it doesn’t own. | The role can grant or revoke access and transfer ownership for any object in the account. |

Expand

Show lessSee more

The other grants are limited to Cortex Extensions or to the tags that carry their category and certification status.

For what each Cortex Extension privilege allows on its own, see
[Cortex Extension privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-cortex-extension).

#### Set up the role

The following example creates a role that can perform every action. Leave out any grant whose action the role
shouldn’t perform:

Copy code

```
USE ROLE ACCOUNTADMIN;

-- Allow grants to cover current and future Cortex Extensions in this account
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'ENABLED';

-- Create the delegated administrator role
CREATE ROLE IF NOT EXISTS skill_catalog_admin;
GRANT ROLE skill_catalog_admin TO USER <user_name>;

-- Grant or revoke skill access
GRANT INHERITED MANAGE GRANTS ON ALL CORTEX EXTENSIONS IN ACCOUNT TO ROLE skill_catalog_admin;

-- View metadata for every skill and plugin in the account
GRANT MONITOR CORTEX EXTENSIONS ON ACCOUNT TO ROLE skill_catalog_admin;

-- Override security scans and read findings
GRANT MANAGE CORTEX EXTENSION SECURITY SCAN ON ACCOUNT TO ROLE skill_catalog_admin;

-- Manage category values, update assignments, and set any skill's category and
-- certification status
GRANT APPLICATION ROLE SNOWFLAKE.OOB_TAG_ADMIN TO ROLE skill_catalog_admin;
GRANT DATABASE ROLE SNOWFLAKE.CORE_VIEWER TO ROLE skill_catalog_admin;
GRANT APPLY TAG ON ACCOUNT TO ROLE skill_catalog_admin;

-- Change discoverability
GRANT INHERITED WRITE ON ALL CORTEX EXTENSIONS IN ACCOUNT TO ROLE skill_catalog_admin;

-- Change owner or delete
-- Caution: this grant is very powerful. See the warning that follows.
GRANT MANAGE GRANTS ON ACCOUNT TO ROLE skill_catalog_admin;
```

MANAGE GRANTS ON ACCOUNT is a very powerful grant

`MANAGE GRANTS ON ACCOUNT` lets the role grant or revoke any privilege on any object in the account, and transfer
ownership of any object. It reaches far beyond skills and plugins, so grant it deliberately and only to a role you
trust at that level.

Include it only if the role genuinely needs to reassign ownership or delete skills and plugins it doesn’t own. If it
doesn’t, leave this grant out: every other action in the preceding table works without it.

Keep the following in mind when you delegate:

- **Account scope is deliberate.** The two `INHERITED` grants use `IN ACCOUNT` because shared skills and plugins are
  created in their owner’s personal database by default. An account-scope inherited grant is what lets a delegated role
  reach objects there. It also covers every database created later, so review
  [Account scope reaches every database](/user-guide/inherited-grants-intro#label-inherited-grants-intro-account-scope)
  before granting.
- **Inherited grants have no per-object exceptions.** You can’t exempt one skill from an inherited grant by revoking
  the privilege on it, and the attempt fails silently. Scope the grant to what should apply uniformly.
- **Grant these with SQL.** The **Skills and plugins** page doesn’t grant or revoke these privileges. Use SQL, as in the
  preceding example, then the delegated role can perform its actions from the page.
- **Some actions need more than one grant.** Overriding a security scan needs `MANAGE CORTEX EXTENSION SECURITY SCAN`
  together with `MONITOR CORTEX EXTENSIONS`. Managing category values needs `SNOWFLAKE.OOB_TAG_ADMIN` together with
  `APPLY TAG ON ACCOUNT`. Certifying needs both of those plus `SNOWFLAKE.CORE_VIEWER`, which lets the role reference the
  certification tag. `MONITOR CORTEX EXTENSIONS` on its own is what lets a role see metadata for every skill and plugin.
- **File access depends on the grants.** Neither directly granted nor inherited `WRITE` includes `READ`.
  `MANAGE GRANTS ON ACCOUNT` lets an administrator grant `READ` to their own role, but doesn’t itself provide file-read
  access. The preceding example also grants `MONITOR CORTEX EXTENSIONS`, which permits reading extension files when
  the account’s file-read support for this privilege is enabled, as it is by default. The full example can therefore
  satisfy the skill-file read check without a separate `READ` grant. This doesn’t grant permissions to the data or
  other resources that a skill accesses when it runs.
- **ACCOUNTADMIN keeps its access.** Delegating opens an action to another role. It doesn’t remove it from
  ACCOUNTADMIN or restrict any existing access.

### Certify a skill or plugin

Certify a skill or plugin to mark it as an officially verified version for your account. Certified skills and plugins
display a **Certified** badge.

Certification is tied to a version, so you can certify versions of the same skill or plugin independently. When an end
user browses the catalog, they see the latest certified version if one exists, and the latest version otherwise. An
administrator can see all versions.

Certification status is recorded with the `SNOWFLAKE.CORE.CERTIFICATION_STATUS`
[Snowflake-provided tag](/user-guide/object-tagging/snowflake-provided-tags), set to `'CERTIFIED'` on the version being
certified.

### Change access and visibility

Access and discoverability are governed independently:

- **Access (RBAC):** Change which roles can install and use a shared skill or plugin.
- **Visibility:** Change whether a skill or plugin is discoverable in the catalog.

### Override a security scan

When a scan flags a skill or plugin that an administrator has determined is safe, the administrator can override the
scan status to make it installable again. Overriding is the supported way to clear a false positive, so owners don’t
have to work around a finding by republishing unchanged content.

Before overriding, an administrator can review the underlying findings, and can clear the override later if the
decision changes. Overriding and reading findings require `MANAGE CORTEX EXTENSION SECURITY SCAN` on the account
together with `MONITOR CORTEX EXTENSIONS`, which ACCOUNTADMIN can grant to a security team’s role. For details, see
[Delegate administration](#label-cortex-code-skill-sharing-delegate-administration).

### Reassign ownership or delete

- **Change owner:** Reassign ownership of a shared skill or plugin.
- **Delete:** Remove a skill or plugin from the catalog.

Deleting a skill or plugin that the acting role doesn’t own means taking ownership of it first, so both actions need
`MANAGE GRANTS` on the account. That privilege isn’t limited to Cortex Extensions. For details, see
[Delegate administration](#label-cortex-code-skill-sharing-delegate-administration).

### Telemetry

For each shared skill or plugin, the **Skills and plugins** page shows the install count and usage count over the last
28 days, aggregated across all clients.

Usage is only counted while a user runs the shared copy unmodified. If someone edits an installed skill or plugin
locally, their copy stops reporting usage, so its counts understate how much the skill is actually being used. To keep
telemetry for a variant, share it as its own skill or plugin instead of editing an installed one.

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

-- Certify a specific version of a skill or plugin
ALTER CORTEX EXTENSION new_db.new_schema.new_ext VERSION VERSION$1
  SET TAG SNOWFLAKE.CORE.CERTIFICATION_STATUS = 'CERTIFIED';

-- Drop an old extension
DROP CORTEX EXTENSION old_db.old_schema.old_ext;
```

To delegate governance actions to a role other than ACCOUNTADMIN, see
[Delegate administration](#label-cortex-code-skill-sharing-delegate-administration).

## Limitations

- Sharing only works within the same Snowflake account. Cross-account sharing isn’t supported.
- Skills and plugins created locally (in your workspace or on your machine) don’t appear in the catalog until
  explicitly shared.
- Exporting skills or plugins to storage outside Snowflake isn’t supported.
- A skill or plugin must fall within the security scanner’s file count and size limits to be shared with others. For
  details, see [Scan limits](#label-cortex-code-skill-sharing-scan-limits).
- Snowflake CoWork has no catalog browse surface. A shared skill reaches Snowflake CoWork only when it’s been added
  to a Cortex Agent. For details, see
  [Use a shared skill in Snowflake CoWork](#label-cortex-code-skill-sharing-cowork).
- Usage telemetry stops for an installed skill or plugin that someone edits locally. For details, see
  [Telemetry](#label-cortex-code-skill-sharing-telemetry).

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
