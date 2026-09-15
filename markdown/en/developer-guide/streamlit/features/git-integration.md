# Sync Streamlit in Snowflake apps with a Git repository

To use version control with your Streamlit apps, you can sync your app with a branch in a Git repository.

You must have already set up your Snowflake account to be connected to a Git repository and have created
a branch in that repository to use with your app. See [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

Note

For Streamlit apps created using the [ROOT\_LOCATION parameter](/sql-reference/sql/create-streamlit), Git integration is not supported.

## Create a Streamlit in Snowflake app from a file in a Git repository

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Next to **+ Streamlit**, open the drop-down menu and select **Create from repository**.
4. For **File location in repository**, select the repository and branch in the repository that contain the Streamlit app file, then select
   the specific `.py` file. For details on connecting Snowflake to your Git repository, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).
5. For **App location**, select a database and schema to contain the Streamlit app. You can’t change these after you create the app.
6. For **Query warehouse** and **App warehouse**, select a warehouse.
7. Select **Create** to create a Streamlit app from the `.py` file in your Git repository.

## Connect an existing Streamlit in Snowflake app with a Git repository

Note

To connect a Streamlit app to a Git repository, you must use a role with the following privileges at a minimum:

- OWNERSHIP or READ on the Git repository
- USAGE on the schema that contains the Git repository

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**, and then open or create a Streamlit app.
3. In the **Files** tab, next to the database object explorer, select **Connect Git Repository**.
4. For **File location in repository**, select the repository and the branch in the repository that you want to sync with the Streamlit app.
5. Select **Select Folder**.
6. When the prompt to commit your app to the Git repository appears, complete the commit steps outlined in [Push changes to a branch in a Git repository](#label-snowsight-streamlit-git-push-changes).

After connecting your Streamlit app with a Git repository, you can select the branch name and open the repository details in Snowflake or Github.

## Push changes to a branch in a Git repository

If a Streamlit app is connected to a branch in a Git repository, after you make changes to the app you can push
your changes to the branch.

Note

You must use a role with the OWNERSHIP or WRITE privilege on the Git repository to push your changes.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**, and then open a Streamlit app.
3. Make any relevant changes to the Streamlit app.
4. Select **Push to Git**.
5. In the **Push to Git** dialog that appears, you can review the username and email address that are used to commit the changes
   to the specified branch and repository. If you need to update the username and email address, expand the **Credentials** section and
   update the **Author name** and **Author email**.
6. For **Commit message**, enter a message to include with your commit.
7. Expand the **Credentials** section to configure credentials. Enter your personal access token for the Git repository in the
   **Personal access token** field. This access token comes from the remote Git provider, such as GitHub.

   - This token is required to authenticate to the Git repository.
   - The token must have read and write access to the content of the repository for the commit to work.
   - Once entered, the token will be saved for future commits. You can update it during any future commits.
8. Select **Push**.

A confirmation message states that your changes were pushed successfully to your branch.

## Sync a Streamlit in Snowflake app with a remote branch in a Git repository

After you connect your app to a branch in a Git repository, you can sync any changes in the remote branch with your Streamlit app.

To sync a Streamlit app with a remote branch in a Git repository:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**, and then open or create a Streamlit app.
3. On the **Files** tab in the database object explorer, select **Pull**.

Snowflake fetches any changes present on the remote repository branch and merges the contents with those changes.

### Merge conflicts

Snowflake attempts to resolve merge conflicts that occur during a sync. If there are merge conflicts that Snowflake
isn’t able to resolve, you’ll receive a message to discard or commit your changes to a new branch. When they
are committed to a new branch, use your Git provider to manually merge your changes from the new branch to the original
branch. Then you should pull the latest updates into your Streamlit app.
