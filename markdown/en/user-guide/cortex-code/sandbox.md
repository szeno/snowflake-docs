# CoCo CLI sandbox

CoCo CLI can run shell commands inside a sandbox to restrict filesystem access, network
access, and process capabilities. Sandboxing adds a layer of isolation so the agent cannot
accidentally modify files or access resources outside of your project.

Important

Support for this feature is experimental and may be subject to change.

Note

This page covers the local sandbox, which isolates commands but still runs them on your
machine. To run the agent’s tools in a Snowflake-managed container instead, see
[CoCo CLI cloud sandbox](/user-guide/cortex-code/cloud-sandbox).

## Platform support

The sandbox uses the operating system’s built-in isolation features to restrict commands.

| Platform | Implementation | Dependencies |
| --- | --- | --- |
| macOS | `sandbox-exec` (built-in) | `ripgrep` |
| Linux | `bubblewrap` | `bubblewrap`, `socat`, and `ripgrep` |
| Windows | Native restricted tokens | None |

Expand

Show lessSee more

### Installing dependencies

macOS:

Copy code

```
brew install ripgrep
```

Debian / Ubuntu:

Copy code

```
sudo apt-get install bubblewrap socat ripgrep
```

Fedora / RHEL:

Copy code

```
sudo dnf install bubblewrap socat ripgrep
```

## Enabling the sandbox

Use the `/sandbox` slash command in CoCo CLI:

```
/sandbox                          # Interactive selector
/sandbox runtime on               # Enable sandbox
/sandbox runtime off              # Disable sandbox
/sandbox runtime status           # Show sandbox status
/sandbox status                   # Show current sandbox status
```

You can also enable the sandbox in your settings file. Add a `sandbox` object to
`~/.snowflake/cortex/settings.json` (user-level) or `.snowflake/cortex/settings.json`
(project-level):

Copy code

```
{
  "sandbox": {
    "enabled": true
  }
}
```

The default permission mode is `"regular"`. To use auto-allow mode, set `"mode": "autoAllow"`
explicitly. See [Permission modes](#label-cortex-code-sandbox-permission-modes).

## Permission modes

The sandbox has two permission modes that control how commands are approved:

| Mode | Setting value | Behavior |
| --- | --- | --- |
| Auto-allow | `"autoAllow"` | Commands that can be sandboxed run automatically without prompting. Commands that cannot be sandboxed (for example, those requiring network access to non-allowed domains) fall back to the normal permission flow. |
| Regular | `"regular"` | All commands prompt for approval, even when running inside the sandbox. |

Expand

Show lessSee more

Set the mode with the `/sandbox` command or in settings:

```
/sandbox mode auto                # Set auto-allow mode
/sandbox mode regular             # Set regular mode
```

## Filesystem restrictions

The sandbox controls which paths commands can read from and write to.

### Default behavior

- **Working directory**: Always allowed for read and write.
- **Skills directory** (`~/.snowflake/cortex/skills`): Allowed.
- **Context directory** (`~/.snowflake/cortex/.ctx`): Allowed when `ctxAvailable` is enabled.

### Protected paths (always denied for write)

The following paths are always protected, regardless of your configuration:

- Shell configuration files: `~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, `~/.zprofile`,
  `~/.profile`, `~/.bash_login`, `~/.bash_logout`
- Git hooks: `~/.git/hooks`, `.git/hooks`
- SSH configuration: `~/.ssh/authorized_keys`, `~/.ssh/config`
- Managed settings directories and files: `/Library/Application Support/Cortex/` (macOS),
  `/etc/cortex/` (Linux), `%ProgramData%\Cortex\` (Windows)

### Custom filesystem rules

Configure filesystem access in settings:

Copy code

```
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowRead": [],
      "denyRead": ["/private/secrets"],
      "allowWrite": ["/tmp", "~/projects"],
      "denyWrite": ["/etc", "/var"]
    }
  }
}
```

| Setting | Default | Description |
| --- | --- | --- |
| `allowRead` | `[]` (allow all) | Paths the sandbox can read. An empty array means all paths are allowed (except those in `denyRead`). |
| `denyRead` | `[]` | Paths the sandbox cannot read. Takes precedence over `allowRead`. |
| `allowWrite` | `[]` (working directory only) | Paths the sandbox can write to. |
| `denyWrite` | `[]` | Paths the sandbox cannot write to. Takes precedence over `allowWrite`. |

Expand

Show lessSee more

Important

Deny rules always take precedence over allow rules. If a path matches both `allowWrite`
and `denyWrite`, the path is denied.

## Network restrictions

The sandbox can restrict which domains commands can access over the network.

Copy code

```
{
  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "deniedDomains": ["*.internal.company.com"],
      "allowLocalBinding": false
    }
  }
}
```

| Setting | Default | Description |
| --- | --- | --- |
| `allowedDomains` | `[]` (allow all) | Domains the sandbox can access. An empty array means all domains are allowed (except those in `deniedDomains`). Supports wildcards (`*.example.com`). |
| `deniedDomains` | `[]` | Domains the sandbox cannot access. Takes precedence over `allowedDomains`. Supports wildcards. |
| `allowLocalBinding` | `false` | Whether sandboxed commands can bind to local ports. |

Expand

Show lessSee more

## Unsandboxed command fallback

Some commands may not be compatible with the sandbox. The `allowUnsandboxedCommands` setting
controls what happens when a command cannot run inside the sandbox.

| Setting | Behavior |
| --- | --- |
| `true` (default) | The agent can request to run the command on the host. You are prompted to approve. |
| `false` | Commands must run inside the sandbox or be listed in `excludedCommands`. If neither applies, the command fails. |

Expand

Show lessSee more

### Excluded commands

You can specify commands that should always run on the host, outside the sandbox:

Copy code

```
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": true,
    "excludedCommands": ["docker", "kubectl"]
  }
}
```

Excluded commands bypass the sandbox and follow the normal permission flow.

## Settings reference

The complete `sandbox` settings object:

Copy code

```
{
  "sandbox": {
    "enabled": false,
    "mode": "regular",
    "allowUnsandboxedCommands": true,
    "excludedCommands": [],
    "permissions": {
      "allow": [],
      "deny": []
    },
    "network": {
      "allowedDomains": [],
      "deniedDomains": [],
      "allowLocalBinding": false
    },
    "filesystem": {
      "allowRead": [],
      "denyRead": [],
      "allowWrite": [],
      "denyWrite": []
    },
    "ctxAvailable": true
  }
}
```

| Setting | Default | Description |
| --- | --- | --- |
| `enabled` | `false` | Enable or disable the sandbox. |
| `mode` | `"regular"` | Permission mode: `"regular"` or `"autoAllow"`. |
| `allowUnsandboxedCommands` | `true` | Allow fallback to host execution when a command cannot be sandboxed. |
| `excludedCommands` | `[]` | Commands that always run on the host, outside the sandbox. |
| `permissions.allow` | `[]` | High-level permission allow rules. Supports patterns like `WebFetch(domain:example.com)`, `Edit(path)`, `Read(path)`, `Bash(command)`. |
| `permissions.deny` | `[]` | High-level permission deny rules. Same pattern syntax as `permissions.allow`. Takes precedence over allow rules. |
| `network.allowedDomains` | `[]` | Network domain allowlist (empty = allow all). Supports wildcards. |
| `network.deniedDomains` | `[]` | Network domain denylist. Takes precedence over allowlist. |
| `network.allowLocalBinding` | `false` | Allow sandboxed commands to bind to local ports. |
| `filesystem.allowRead` | `[]` | Read allowlist (empty = allow all except deny). |
| `filesystem.denyRead` | `[]` | Read denylist. Takes precedence. |
| `filesystem.allowWrite` | `[]` | Write allowlist. |
| `filesystem.denyWrite` | `[]` | Write denylist. Takes precedence. |
| `ctxAvailable` | `true` | Allow sandbox access to the context directory (`~/.snowflake/cortex/.ctx`), used for storing conversation context and session data. |

Expand

Show lessSee more

### Configuration scopes

Sandbox settings follow the same precedence as other CoCo settings:

1. **Project-level** (highest priority): `.snowflake/cortex/settings.json`
2. **User-level**: `~/.snowflake/cortex/settings.json`
3. **Managed/enforced**: Administrators can enforce sandbox policy via the managed settings file.
   See [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings#label-cortex-code-managed-settings).
