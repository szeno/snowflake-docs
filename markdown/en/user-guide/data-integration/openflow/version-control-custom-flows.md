# Version control for custom flows

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow supports Registry Clients, including the GitHub Registry Client, which allows you to
use a Git repository to store and version your custom flow definitions. This enables standard software
development lifecycle (SDLC) practices, such as branching, pull
requests, code review, and environment promotion.

A common workflow is:

- Maintain a `main` branch representing your production flow definitions.
- Create feature branches for new development.
- Develop and commit changes on the Openflow canvas.
- Open pull requests, review with Flow Diff, and merge.

## Prerequisites

- A GitHub repository for storing flow definitions.
- A GitHub Personal Access Token with `repository` access.
- An Openflow Runtime with access to the Openflow canvas.
- Appropriate execute-as role privileges on the runtime object.

## Step 1: Create a GitHub Registry Client

1. Create a repository in GitHub to store your flow definitions.
2. Generate a Personal Access Token (PAT) in GitHub with repository access permissions.
3. On the Openflow canvas, navigate to **Controller Settings** and create a new Registry Client.
4. Select **GitHub Registry Client** as the type.
5. Configure the Registry Client with:
   - Your GitHub repository URL.
   - The GitHub repository owner.
   - Your Personal Access Token for authentication.

## Step 2: Create and version a new flow

1. On the Openflow canvas, create a new Process Group for your flow.
2. Build your flow: add processors, configure connections, and set up your data pipeline.
3. Right-click the Process Group and select **Start Version Control**.
4. Choose the GitHub Registry Client you configured in
   [Step 1](#label-openflow-git-create-registry-client).
5. Provide a flow name and an initial commit message.

After you save, the flow definition is committed to your GitHub repository. You can verify by
checking the repository in GitHub.

## Step 3: Use branches to manage changes

### Create a development branch

In your GitHub repository, create a new branch (for example, `dev` or a feature branch
like `feature/add-new-table`).

### Import and develop on the branch

1. On the Openflow canvas, import the flow from the GitHub Registry into a new Process Group by
   dragging the **Import from Registry** icon from the toolbar to the canvas.
2. When importing, select the target branch (for example, `dev`) to work against.
3. Make your changes to the flow inside the Process Group.
4. Commit your changes in Openflow. This pushes the updated flow definition to the selected
   branch in GitHub.

### Review and merge via pull request

1. In GitHub, open a pull request from your development branch to `main`.
2. Review the changes. Use the Snowflake Flow Diff GitHub Action
   (see [Step 4](#label-openflow-git-flow-diff)) for human-readable diffs.
3. Merge the pull request after it’s approved.
4. Back on the Openflow canvas, update the `main` Process Group to pull the latest version from
   the `main` branch.

## Step 4: Set up Snowflake Flow Diff (GitHub Action)

Snowflake Flow Diff is a GitHub Action that makes flow changes human-readable by rendering
a visual diff of your pipeline changes directly in pull request conversations.

### Set up the workflow file

1. In your GitHub repository, create the file `.github/workflows/flowdiff.yml`.
2. Copy the workflow configuration from the
   [Snowflake Flow Diff repository](https://github.com/Snowflake-Labs/snowflake-flow-diff)
   (see the Usage section in the README).
3. Commit and push the workflow file.

### Review flow changes

1. When a pull request is opened, the Flow Diff action runs automatically.
2. Navigate to the **Conversations** tab on the pull request and wait for the Flow Diff
   analysis to appear.
3. The analysis shows a visual, human-readable comparison of flow changes instead of raw
   JSON diffs.

## Manage parameters across environments

Openflow uses Parameters to manage environment-specific values (for example, connection strings,
credentials, table names) across different Runtimes.

Keep the following concepts in mind:

- Parameters are grouped into a Parameter Context, which has a one-to-one mapping with a
  Process Group.
- Parameter Context inheritance allows you to define shared parameters in a parent context and
  override specific values in child contexts. This is useful for promoting flows across dev,
  staging, and production environments.
- Parameter Contexts can integrate with Secrets Managers to securely handle sensitive credentials
  without storing them in the flow definition.

## Recommended SDLC workflow

1. **Development environment**: Developers create feature branches, build or modify flows, and
   commit changes on the Openflow canvas against their feature branch.
2. **Code review**: Open a pull request in GitHub. Use Snowflake Flow Diff for readable reviews.
3. **Merge to main**: After approval, merge the pull request into the `main` branch.
4. **Promote to production**: In your production Runtime, update the Process Group to pull the
   latest version from `main`.
5. **Parameterize**: Use Parameter Contexts to handle environment-specific configuration without
   modifying the flow definition itself.
