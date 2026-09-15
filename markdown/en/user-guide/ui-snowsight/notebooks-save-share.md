# Save and share results in notebooks

You can collaborate on data analysis with others using Snowflake Notebooks.

Each Snowflake notebook is owned by a role, so other users that are granted or inherit the owner role can open, run, and edit notebooks
owned by that role. You cannot share the notebook with other roles.

Caution

Notebooks are saved every three seconds. If other users have the notebook open and run it, you might overwrite each other’s work.

## Export your notebook as a file for sharing

To share your notebook externally, you can export it as an `.ipynb` file. The exported notebook can be shared with others who may not
use Snowflake Notebooks. They can open the notebooks with other solutions that are compatible with the `.ipynb` format.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. Open the notebook to export.
4. Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) menu, and then select **Export**.
5. Acknowledge that some commands might not be supported in other notebook tools, and select **Export**.

   A file named `notebook_app` is downloaded. You can then
   [import the exported notebook into another Snowflake account](/user-guide/ui-snowsight/notebooks-create#label-notebooks-create) or another tool that supports
   `.ipynb` files.

Note

Only the cell content — not the cell outputs — is included as part of the export.

To download a CSV file of a cell, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. Open the notebook from which you want to download data.
4. Run the cell for the data to download.
5. Hover over the table and select **Download data as .csv**.

## Collaborate in notebooks

- The role used to create the notebook owns the notebook. For details on privileges required for notebooks, see [Set up Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-setup).
- Any user with that role, or whose role inherits that role, can access, edit, run, and manage the notebook.
- To share and collaborate on a notebook with another user, that user must either have the owner role or be granted a role that
  inherits the owner role of the notebook.
- Ownership of a notebook can be transferred to a different role. For details, see [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership).

## Limitations

- You cannot share a notebook with other roles.
- Roles with only the USAGE privilege on a notebook cannot create a task to schedule that notebook. The USAGE privilege allows the notebook
  to be referenced in certain contexts (such as the [SHOW NOTEBOOKS](/sql-reference/sql/show-notebooks) command), but does not permit execution or scheduling.
