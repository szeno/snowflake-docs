# Skills and Plugins

Skills extend CoCo with specialized capabilities that can be invoked by typing `/` in the message box.

## Requirements

To use skills and plugins in CoCo on Snowsight, you need:

- An active warehouse in your session. Skills execute queries and AI functions on your behalf,
  so your current warehouse handles the compute. Any warehouse size works for most skills.
- To manage skills in AI & ML (share, change access, delete), you need the
  ACCOUNTADMIN role or a role that ACCOUNTADMIN has granted the relevant governance privileges to.
  For details, see [Delegate administration](/user-guide/cortex-code/cortex-code-skill-plugin-sharing#label-cortex-code-skill-sharing-delegate-administration).

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

## Skills and plugins in AI & ML

Note

Sharing skills and plugins is rolling out progressively. If you don’t see **AI & ML** > **Skills and plugins** in Snowsight or shared skills in the `/` menu, the feature might not yet be enabled for your account. Contact your account team for availability.

Skills can be shared and discovered through AI & ML. The `+` menu and the `/` command both show local, built-in, and shared skills.

To share a skill, use the `share-skill` skill, which provides a share link. To install a shared skill, paste a skill link into the message box. The `find-skill` skill helps facilitate skill discovery and invocation.

### Managing skills in AI & ML

A user with the ACCOUNTADMIN role, or a role that ACCOUNTADMIN has granted the relevant governance privileges to,
can manage skills through AI & ML:

1. Navigate to **AI & ML** > **Skills and plugins** to browse and search available skills.
2. Select a skill to view its details.
3. Available management actions:
   - Change access (role or user)
   - Change owner
   - Delete
