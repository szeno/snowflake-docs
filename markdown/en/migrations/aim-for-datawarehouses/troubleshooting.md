# Snowflake AIM Agent for Data Warehouses - Troubleshooting

The Snowflake AIM Agent for Data Warehouses and its bundled tooling (SnowConvert, `uv`, ODBC drivers, and Python packages) are installed automatically the first time the agent runs. You don’t need to install them yourself. Use the tables below to get unblocked when setup doesn’t complete or the agent doesn’t behave as expected.

## The agent or its tooling isn’t installed

| Situation | What you’ll see | What to do |
| --- | --- | --- |
| Snowflake CoCo isn’t installed | No `cortex` command | Install the [Snowflake CoCo CLI](/user-guide/cortex-code/cortex-code-cli). The Snowflake AIM Agent for Data Warehouses is bundled with it. Confirm with `cortex --version`. |
| Skill installed, dependencies not set up yet | The first run installs tooling automatically | Let the first run finish. It installs dependencies via Homebrew (macOS/Linux) or winget (Windows). Make sure `python3` is on your `PATH`. |
| `scai` not found after install | SnowConvert CLI missing | Run the install hook `migration-plugin/hooks/install-dependencies`, or install directly: `brew install --cask snowflakedb/snowconvert-ai/snowconvert-ai`. |
| The skill doesn’t trigger mid-project | The agent stays in plain CoCo mode (can happen after context compaction) | Trigger it directly with `/migrate <your prompt>`. |
| You already have converted `.sql` files | — | Use the **midway-entry** path: import the pre-converted files and start at deployment, skipping extraction and conversion (SQL Server and Redshift). |

Expand

Show lessSee more

Advanced users can also run conversion directly with the SnowConvert AI CLI (`scai`) outside the guided skill and import the results, but the guided Snowflake AIM Agent for Data Warehouses is the recommended path.

## Common problems

| Problem | Resolution |
| --- | --- |
| **`migration-guide` skill doesn’t appear** | Ensure you’re on the latest version of Snowflake CoCo. Run `cortex --version` to confirm. |
| **Installation and update fails during setup** | Check that `python3` is available on your `PATH`. The Snowflake AIM Agent for Data Warehouses installs dependencies via Homebrew (macOS/Linux) or winget (Windows). |
| **`scai` not found after skill install** | Run the install hook manually: `migration-plugin/hooks/install-dependencies`. Or install directly: `brew install --cask snowflakedb/snowconvert-ai/snowconvert-ai`. |
| **Snowflake connection errors** | Verify your connection in `~/.snowflake/config.toml` or `~/.snowflake/connections.toml` and confirm the connection name matches what you provided during setup. |
| **Agent seems lost** | Say `"What is the current state?"`: the agent re-reads project status and resets context. |

Expand

Show lessSee more

## Support

For help with the Snowflake AIM Agent for Data Warehouses, contact [**aim-support@snowflake.com**](mailto:aim-support@snowflake.com).
