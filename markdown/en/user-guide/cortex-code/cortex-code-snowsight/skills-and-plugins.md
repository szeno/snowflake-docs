# Skills and Plugins

Skills extend CoCo with specialized capabilities that can be invoked by typing `/` in the message box.

## Requirements

To use skills and plugins in CoCo on Snowsight, you need:

- An active warehouse in your session. Skills execute queries and AI functions on your behalf,
  so your current warehouse handles the compute. Any warehouse size works for most skills.
- To manage skills in the Horizon Catalog (share, change access, delete), you need the
  ACCOUNTADMIN role or a role with equivalent privileges on the Catalog.

## Built-in skills

Snowflake provides built-in skills that are available from any page in Snowsight. Type `/` to see and select from the available skills. The list of built-in skills evolves as feature teams add new skills to Snowsight.

## Personal skills

You can create your own skills in a workspace to tailor CoCo to your specific workflows.

To add a personal skill, use any of the following options in the workspace:

- Upload Skill File(s)
- Upload Skill Folder(s)
- + Create Skill

Personal skills are stored in the `.snowflake/cortex/skills` directory of the workspace and can be invoked by typing `/` in the message box.

Note

Personal skills can only be accessed from the workspace where they were created. They are not available when using a different workspace or when outside of a workspace.

## Skills and plugins in Horizon Catalog

Note

The Skill Catalog is rolling out progressively. If you don’t see **Catalog >> Skills and plugins** in Snowsight or Skill Catalog entries in the `/` menu, the feature might not yet be enabled for your account. Contact your account team for availability.

Skills can be shared and discovered through the Horizon Catalog. The `+` menu and the `/` command both show Local, Built-in, and Skill Catalog skills.

To share a skill, use the `share-skill` skill, which provides a share link. To install a shared skill, paste a skill link into the message box. The `find-skill` skill helps facilitate skill discovery and invocation.

### Managing skills in the Catalog

A user with the ACCOUNTADMIN role can manage skills through the Catalog:

1. Navigate to **Catalog >> Skills and plugins** to browse and search available skills.
2. Select a skill to view its details.
3. Available management actions:
   - Change access (role or user)
   - Change owner
   - Delete
