# Remote Development with the Snowflake Extension for Visual Studio Code

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Remote Development lets you create a Snowflake-backed development environment, connect to it over [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh), and run Python notebooks, SQL, scripts, terminals, and Git on Snowflake-managed compute. The environment is backed by Snowflake Notebook and includes Python, Jupyter, and Snowflake libraries.

You can use these capabilities in **Visual Studio Code** or **Cursor**. Both are built on the same Visual Studio Code extension model, so you install and run the Snowflake Extension for Visual Studio Code the same way in each of them.

To use Remote Development, install version 1.38 or later of the Snowflake Extension for Visual Studio Code and make sure your account meets the requirements in [Prerequisites](#prerequisites).

## Prerequisites

Before you start, make sure you have:

| Requirement | Details |
| --- | --- |
| Snowflake Extension for Visual Studio Code | Install version 1.38 or later of the Snowflake extension from the Visual Studio Code Marketplace, or from the extensions UI in Cursor. Persistent storage and Git require version 1.39 or later. |
| Editor version | Use the latest version of Visual Studio Code or Cursor for the best Jupyter kernel picker experience. |
| Remote - SSH extension | Install `ms-vscode-remote.remote-ssh` from the Visual Studio Code Marketplace. |
| Account parameter | The `ENABLE_NOTEBOOK_SERVICE_REMOTE_VS_CODE_ACCESS` account parameter must be enabled. It’s enabled by default, and an account administrator can disable it. |
| Snowflake privileges | Your role must be able to create and run notebook services: the `USAGE` privilege on the target compute pool, and the compute pool must allow the `NOTEBOOK` workload type (the `ALLOWED_SPCS_WORKLOAD_TYPES` parameter). Your role must also be able to use any external access integrations or secrets you select for the service. |
| Local SSH tools | The extension uses your local OpenSSH client and `nc` (netcat). `nc` is preinstalled on macOS and many Linux distributions. On Windows, install a netcat-compatible executable named `nc` and make sure it’s on your `PATH`. |

Expand

Show lessSee more

## Enable and manage access

Remote Development is enabled by default through the `ENABLE_NOTEBOOK_SERVICE_REMOTE_VS_CODE_ACCESS` account parameter. An account administrator can disable it for the account by setting the parameter to `false`.

When Remote Development is enabled, notebooks in your account can reach the following endpoints through the external access integration that the feature uses:

- `update.code.visualstudio.com:443`
- `vscode.download.prss.microsoft.com:443`
- `marketplace.visualstudio.com:443`
- `*.gallerycdn.vsassets.io:443`
- `download.visualstudio.microsoft.com:443`
- `marketplace.cursorapi.com:443`
- `cursor-cdn.com:443`
- `downloads.cursor.com:443`
- `anysphere-binaries.s3.us-east-1.amazonaws.com:443`
- `sfc-repo.snowflakecomputing.com:443`
- `ai.snowflake.com:443`

To turn Remote Development on or off for your own user, open your user settings JSON (**Preferences: Open User Settings (JSON)** from the Command Palette) and set the value:

Copy code

```
{
  "snowflake.remoteDevelopment.enabled": false
}
```

Set the value to `false` to hide the **Remote Environments** panel for your user, or `true` to show it.

## Supported editors

Remote Development works in two Snowflake-supported editors that share the Visual Studio Code extension model:

- **Visual Studio Code**: Install the Snowflake Extension for Visual Studio Code from the Visual Studio Code Marketplace.
- **Cursor**: Install the Snowflake Extension for Visual Studio Code from the extensions UI the same way you install other compatible extensions. In Cursor, switch to **editor mode** to follow the instructions in this topic.

## Create a remote environment

1. In the **Remote Environments** panel, select **Create Remote Development Environment**.
2. Enter a **Service name**. Use a Snowflake-compatible identifier and choose a name that doesn’t conflict with an existing local SSH host alias.
3. Select one or more **Workspaces** to associate with the remote service. During SSH setup, you’re prompted separately to mount workspaces into the running environment.
4. Optional: select **External access integrations** if your notebooks need outbound network access, for example to install packages from PyPI or to reach your Git provider’s host.
5. Optional: select **Secrets** to make Snowflake secrets available inside the remote environment, for example a Git credential. Selecting secrets works much like selecting external access integrations.
6. Optional: expand **Service settings** and adjust the compute and runtime settings, including **Enable persistent storage**.
7. Select **Create**.

The service appears in the **Remote Environments** panel. Creation can take a few minutes while Snowflake provisions the service and starts the container.

### Service settings

| Setting | Description |
| --- | --- |
| Compute type | Select CPU or GPU. GPU requires an available GPU compute pool. |
| Python version | Select the Python version for the remote environment. |
| Runtime version | Select the Snowflake Container Runtime version, when runtime choices are available for your account. |
| Compute pool | Select an available compute pool. If no pools are listed, enter a compute pool name manually. |
| Idle timeout | Select how long the service can remain idle before Snowflake suspends it. The default is 24 hours. |
| Enable persistent storage | Mounts a persistent drive at `/mnt/pd0` in the service. You can set this only when you create a service, and you can’t change it afterward. |

Expand

Show lessSee more

**Enable persistent storage** requires version 1.39 or later of the Snowflake Extension for Visual Studio Code. For details, see [Use persistent storage and Git in a remote environment](#label-remote-dev-persistent-storage).

**Python version** and **Runtime version** appear only when Snowflake Container Runtimes are available for your account.

## Manage remote environments

The **Remote Environments** panel lists your remote development services and refreshes every 30 seconds while the panel is visible. You can also refresh it manually.

| Status | Meaning |
| --- | --- |
| RUNNING | The service is active and can accept Remote - SSH connections. |
| SUSPENDED | The service is stopped and can be resumed. |
| PENDING | Snowflake is creating or starting the service. |
| SUSPENDING | Snowflake is stopping the service. |
| FAILED | The service failed. Open the details panel to view the error. |
| UNKNOWN | The extension couldn’t map the service status. Refresh the panel or open details. |

Expand

Show lessSee more

Use the inline actions next to each service in the panel to manage it:

| Action | Available when | Description |
| --- | --- | --- |
| Resume | Service is SUSPENDED | Starts the service again. |
| Stop | Service is RUNNING | Suspends the service. |
| Delete | Any service status | Permanently deletes the service. |
| Info | Any service status | Opens service details, including status, compute pool, runtime, endpoints, timestamps, and error messages. |
| Manage workspaces on remote | Any service status | Changes the workspace selection for the service so you can add or remove workspaces. See [Select multiple workspaces](#select-multiple-workspaces). |
| Setup SSH | Service is RUNNING and no proxy is active | Starts the local SSH proxy and opens the remote environment in a new editor window. |
| Stop Proxy | A proxy is active for the service | Stops the local SSH proxy and removes the generated SSH config entry. |

Expand

Show lessSee more

Suspending a service stops the running remote environment but keeps the service definition so you can resume it later. Compute pool billing and auto-suspend behavior depend on your Snowflake compute pool configuration.

Deleting a service is permanent. The extension also stops any active local proxy for that service.

## Connect to a remote environment

1. In the **Remote Environments** panel, find a service with status **RUNNING**.
2. Select **Setup SSH**.
3. When prompted, choose one or more workspaces to mount, or press Escape to skip mounting.
4. Your editor opens a new window connected to the remote environment at `/root`.

You don’t need to create SSH keys or configure port forwarding manually.

If you have many workspaces, there can be a short pause between selecting **Setup SSH** and seeing the workspace picker while the extension prepares the list. The extension doesn’t show progress during this step, so wait a moment for the picker to appear before selecting **Setup SSH** again.

### Select multiple workspaces

You can associate more than one workspace with a remote environment.

- When you create a service or run **Setup SSH**, the workspace picker supports multiple selection. Choose all the workspaces you want to mount.
- To change the selection for an existing service, use **Manage workspaces on remote** in the **Remote Environments** panel. You can add workspaces to, or remove them from, the service.
- In the **Explorer** view of the remote window, your mounted workspaces appear under **Workspaces**, already included in the current editor workspace.

Each mounted workspace is linked under:

`/root/workspaces/<workspace_name>`

If you press Escape at the picker, the extension skips mounting and continues opening the remote window. You can still use the remote environment, but workspace files aren’t linked under `/root/workspaces`.

If workspace mounting fails, the extension shows a warning and still opens the remote environment. You can retry **Setup SSH** later after confirming that your role has access to the workspace.

### First connection

The first connection can take a few minutes because your editor installs extensions on the remote host. If the Extensions view shows **Reload Required** or **Reload Window**, reload the remote window before opening notebooks.

If the remote window opens before the Python or Jupyter extension finishes installing, wait for installation to finish and reload the window.

### Optional reading: how the SSH connection works

You can skip this section if you only need the standard connection workflow.

When you connect, the extension:

1. Starts a local proxy on `127.0.0.1` that forwards SSH traffic to Snowflake over a secure WebSocket connection.
2. Writes a generated `Host <service-name>` entry to your user SSH config file (for example `~/.ssh/config` on macOS and Linux).
3. Installs required extensions on the remote host.
4. Configures the remote Python and Jupyter settings.
5. Opens the remote folder `/root` in a new editor window.

The generated SSH host entry uses the remote service name. If your SSH config already contains a `Host` entry with the same name, the extension replaces that entry. Choose service names that don’t collide with SSH hosts you manage manually.

The local proxy uses the Snowflake session token that’s active when you connect. The proxy doesn’t refresh session tokens automatically. If the remote connection becomes unresponsive after a long session, stop the proxy, sign in again if needed, and run **Setup SSH** again.

## Work with notebooks

After the remote window opens, create or open a Jupyter notebook:

1. Run **Create: New Jupyter Notebook** from the Command Palette, or create a file ending in `.ipynb`.
2. In the action bar of the notebook, select **Snowflake: Start Notebook Kernel**.
3. In the kernel picker, select **Snowflake Kernel (Python + SQL)**.

This is the same kernel that Snowflake Notebooks use in Snowflake Workspaces. Python and SQL cells run exactly the way they do when you run a notebook in the Snowsight Workspaces UI. Run Python cells and SQL cells in the same notebook without switching kernels.

Run a test Python cell:

Copy code

```
from snowflake.snowpark.context import get_active_session

session = get_active_session()
print(session.sql("SELECT CURRENT_VERSION()").collect())
```

If you mounted workspaces during SSH setup, their files are available under:

`/root/workspaces/<workspace_name>`

Use mounted workspaces for files you want to keep across remote sessions. If you enabled persistent storage for the service, you can also use `/mnt/pd0`. Don’t rely on files stored only in local container paths such as `/root` or `/tmp` to persist after service lifecycle changes.

## Use persistent storage and Git in a remote environment

Persistent storage is optional. To use it, expand **Service settings** and select **Enable persistent storage** when you [create the remote environment](#create-a-remote-environment). This mounts a persistent drive backed by [Snowpark Container Services block storage volumes](/developer-guide/snowpark-container-services/block-storage-volume) at:

`/mnt/pd0`

Files stored there survive suspend and resume, which is useful for large package installs or cloning Git repositories.

This Git workflow is independent of the [Git integration in Snowflake](/developer-guide/git/git-overview) that connects Snowflake to a Git repository. Here, you use standard Git against the persistent storage drive inside the remote environment.

Important

Persistent storage requires version 1.39 or later of the Snowflake Extension for Visual Studio Code. You can select **Enable persistent storage** only when you create a service, and you can’t change it afterward. If an existing service doesn’t have persistent storage, create a new service with the option selected.

### Clone and work with a repository

Before you can clone from a remote repository, the service needs outbound network access to your Git provider’s host (for example, `github.com`) through an external access integration.

1. In the remote window, open a terminal, or use your preferred Git extension.
2. Change to the persistent storage drive and clone your repository:

   Copy code

   ```
   cd /mnt/pd0
   git clone https://github.com/<owner>/<repo>.git
   ```
3. In the editor, run **Add Folder to Workspace** and select the cloned repository folder under `/mnt/pd0`.

Your editor’s built-in Source Control features now track changes for the repository, so you can stage, commit, and push from the Source Control view as you do for a local repository.

If the repository is public and doesn’t require authentication, you don’t need the credential setup in the next section.

### Authenticate to a private repository

To work with a private repository without storing your credentials in plain text on the persistent storage drive, store the credential in a Snowflake secret and let Git read it from the mounted secret at runtime.

1. Create a personal access token with your Git provider. For GitHub, create a classic token at `https://github.com/settings/tokens` and add the `repo` scope for private repositories.
2. Create a Snowflake secret that holds the credential:

   Copy code

   ```
   CREATE OR REPLACE SECRET my_db.my_schema.git_pat
     TYPE = PASSWORD
     USERNAME = '<git_username>'
     PASSWORD = '<git_access_token>';
   ```
3. When you [create the remote service](#create-a-remote-environment), select the secret in the **Secrets** field so it’s mounted into the environment.
4. In the remote environment, clone the repository onto the persistent storage drive, passing the credential helper for this command only. Snowflake mounts the secret under `/secrets/`, using the secret’s username and password values:

   Copy code

   ```
   cd /mnt/pd0
   git -c credential.helper='!f() { echo "username=$(cat /secrets/<prefix>/<mount_name>/git_pat/username)"; echo "password=$(cat /secrets/<prefix>/<mount_name>/git_pat/password)"; }; f' \
     clone https://github.com/<owner>/<repo>.git
   ```

   Replace the path with the mount path for your secret. Confirm the exact path by listing the contents of `/secrets/` in the remote terminal.
5. Set the credential helper for the cloned repository so that later fetches and pushes reuse it:

   Copy code

   ```
   cd /mnt/pd0/<repo>
   git config --local credential.helper \
     '!f() { echo "username=$(cat /secrets/<prefix>/<mount_name>/git_pat/username)";
             echo "password=$(cat /secrets/<prefix>/<mount_name>/git_pat/password)"; }; f'
   ```

Important

Use repository-local configuration (`git config --local`) rather than global configuration (`git config --global`). Global Git configuration is stored outside `/mnt/pd0`, so it’s lost when the service suspends and resumes. Repository-local configuration lives in the repository on the persistent storage drive, so it persists.

Because Git reads the credential from the mounted secret at runtime, your token isn’t written to the persistent storage drive.

## Use Cortex Code in a remote environment

You can use [Cortex Code](/user-guide/cortex-code/cortex-code) in a remote environment through the Cortex Code support in the Snowflake Extension for Visual Studio Code. For details, see [Cortex Code in your code editor](/user-guide/cortex-code/cortex-code-in-your-editor).

## Disconnect

To end your editor session, close the remote window.

To stop the local SSH tunnel, return to the local editor window and select **Stop Proxy** for the service. This closes the local proxy and removes the generated `Host <service-name>` entry from your SSH config.

If you stop or delete a service, the extension also stops any active local proxy for that service.

## Troubleshooting

### Remote Environments panel is not visible

| Possible cause | Resolution |
| --- | --- |
| Feature disabled for the account | The `ENABLE_NOTEBOOK_SERVICE_REMOTE_VS_CODE_ACCESS` account parameter is enabled by default. Ask an account administrator to confirm it hasn’t been disabled. |
| Disabled for your user | Set `snowflake.remoteDevelopment.enabled` to `true` in your user settings JSON, then reload your editor window. |
| Extension is outdated | Update to version 1.38 or later of the Snowflake Extension for Visual Studio Code, then reload your editor window. |
| You aren’t signed in | Sign in to Snowflake from the Snowflake extension. |

Expand

Show lessSee more

### Panel is visible but empty

You might not have any remote services yet. Select **Create Remote Development Environment** to create one.

If you expect to see existing services, refresh the panel and confirm that you’re signed in with the expected role and account.

### Create fails

| Possible cause | Resolution |
| --- | --- |
| Service name already exists | Choose a different service name, or use the panel actions to resume, stop, or delete the existing service. |
| Invalid compute pool | Select a listed compute pool or confirm the manually entered compute pool name. |
| Missing privileges | Ask your Snowflake administrator to grant access to the compute pool, workspace, external access integration, or secret. |
| GPU selected without GPU capacity | Select CPU or choose an available GPU compute pool. |

Expand

Show lessSee more

### SSH connection fails

| Possible cause | Resolution |
| --- | --- |
| Service is not running | Resume the service first. If the status is PENDING, wait and refresh the panel. |
| `nc` is not installed | Install netcat and make sure `nc` is on your local `PATH`. |
| Local proxy stopped | Select **Setup SSH** again. |
| Network blocks WebSocket traffic | Allow outbound `wss://` connections to your Snowflake account endpoint. |
| Corporate proxy blocks WebSocket | Configure your network to allow WebSocket upgrade traffic to Snowflake, or bypass the proxy for Snowflake hosts. |
| Snowflake session expired | Select **Stop Proxy**, sign in again if needed, and run **Setup SSH** again. |
| Existing SSH host alias conflicts | Rename the remote service or update your local SSH config to avoid a `Host <service-name>` collision. |

Expand

Show lessSee more

### Workspace picker is slow to appear

If you have many workspaces, the extension can take a moment to prepare the picker after you select **Setup SSH** or create a service. The extension doesn’t show progress during this step. Wait for the picker to appear rather than selecting the action again.

### Notebook kernel doesn’t appear

| Possible cause | Resolution |
| --- | --- |
| Remote extensions are still installing | Wait for the Snowflake, Python, and Jupyter extensions to finish installing, then reload the remote window. |
| Kernel isn’t started | In the notebook action bar, select **Snowflake: Start Notebook Kernel**, then choose **Snowflake Kernel (Python + SQL)**. |
| Editor window needs reload | Run **Developer: Reload Window** in the remote window. |
| Remote extension is outdated | Make sure the Snowflake extension in the remote session is version 1.38.0 or later, then reload the remote window. |

Expand

Show lessSee more

### Persistent storage isn’t available

Persistent storage is optional and can be enabled only when you create a service. If `/mnt/pd0` doesn’t exist in the remote environment, either the service was created without **Enable persistent storage** selected, or the extension was older than version 1.39 when you created the service. Update the extension to version 1.39 or later and create a new service with the option selected.

### Terminal file listings are slow

Mounted workspaces use a remote filesystem. Commands that read many file attributes can be slower than on a local disk. The extension adds an interactive shell alias that disables colorized `ls` output because color detection can trigger extra metadata calls.

### Service is stuck in PENDING or FAILED

If a service remains PENDING for several minutes, the compute pool might still be provisioning or might not have available capacity. Refresh the panel and check the service details.

If a service is FAILED, open the **Info** panel and review the error message. Common causes include invalid compute pools, missing privileges, unavailable runtime images, quota limits, or insufficient compute capacity.

## Best practices

Use shorter idle timeouts for temporary development sessions to reduce unnecessary compute usage.

Select external access integrations only when your workload needs outbound network access.

Mount a workspace when you need files to persist across sessions or be shared with other Snowflake notebook workflows.

Enable persistent storage when you plan to clone Git repositories or install large packages. Decide before you create the service, because you can’t add it later.

Store Git credentials in a Snowflake secret rather than on the persistent storage drive.

Stop the proxy when you’re done using the remote window so stale SSH entries and local proxy processes don’t remain active.

Reconnect after long breaks. If the Snowflake session used by the local proxy expires, stop the proxy and run **Setup SSH** again.

## FAQ

**Do I need to manage SSH keys?**  
No. The extension manages the SSH connection through a local proxy and Snowflake authentication.

**Can I open a terminal on the remote environment?**  
Yes. In the remote window, use **Terminal: Create New Terminal**.

**Can I run SQL cells in notebooks?**  
Yes. Select the **Snowflake Kernel (Python + SQL)** kernel. It’s the same kernel that Snowflake Notebooks use in Workspaces, so Python and SQL cells run the same way they do in the Snowsight Workspaces UI.

**Can I use Git in the remote environment?**  
Yes, if you selected **Enable persistent storage** when you created the service, which requires extension version 1.39 or later. Clone your repository under `/mnt/pd0`, add the folder to your editor workspace, and use your editor’s Source Control features. See [Use persistent storage and Git in a remote environment](#label-remote-dev-persistent-storage).

**Can I use Cortex Code in the remote environment?**  
Yes, in Visual Studio Code and Cursor. See [Use Cortex Code in a remote environment](#use-cortex-code-in-a-remote-environment).

**Can multiple users share one remote service?**  
Yes, if each user has the required Snowflake privileges to access the notebook service. Remote Development uses SSH access and the Snowflake notebook service privilege model, so multiple authorized users can connect to and operate on the same service in parallel.

**What packages are installed?**  
The selected Snowflake Container Runtime determines the base Python version and preinstalled packages. For runtime details, see [Snowflake Container Runtime for ML](/developer-guide/snowflake-ml/container-runtime-ml).

**Can I install additional packages?**  
Yes, if the environment has outbound network access through an external access integration or another approved package source.
