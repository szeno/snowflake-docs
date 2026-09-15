# Drop an external volume by using Snowsight

Dropping an external volume removes the [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) from the account, but retains a version of the
external volume so that it can be recovered using [UNDROP EXTERNAL VOLUME](/sql-reference/sql/undrop-external-volume). For more information, see [Usage Notes for DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume#label-drop-external-volume-usage-notes).

Note

To drop an external volume by using SQL, use the [DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume) command.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has OWNERSHIP privilege on the external volume you want to drop.

   For instructions, see [Switch your primary role](/user-guide/ui-snowsight-gs#label-switching-your-active-role).
3. In the navigation menu, select **Catalog** » **External data**.
4. Select the **External volumes** tab.
5. Select the external volume you want to drop.
6. Select **…** » **Drop external volume**.
7. Select **Drop external volume** again.
