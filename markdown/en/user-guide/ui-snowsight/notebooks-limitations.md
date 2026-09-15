# Limitations with Legacy Snowflake Notebooks

This topic describes unsupported features and limitations of Snowflake Notebooks.

- Only one executable `ipynb` file is permitted within each notebook.
- Streamlit components and widgets, such as slider values, do not retain their state if you refresh the browser window, open the notebook
  in a new tab, or close and reopen the current tab.
- For datasets over 1,000 points, Plotly defaults to `webgl` rendering, which is not recommended for security reasons. Snowflake recommends
  that you set the render mode to SVG, however it can cause some performance degradation.
- When you create a notebook from a repository, only the selected notebook is executable. Any other notebooks in the
  repository can be selected and edited, but they are not executable.
- Notebooks cannot be created or executed by [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).
- Renaming a notebook or moving it to a different database/schema will invalidate the notebook URL.
- Snowflake Notebooks are hosted in a third-party domain to provide increased security. In Safari, you must enable third-party cookies to
  allow reconnection to a running notebook after losing a connection. To enable this setting, in Safari select
  **Settings** » **Privacy**, and then clear the **Prevent cross-site tracking** checkbox.
