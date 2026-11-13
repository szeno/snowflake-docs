# Installing Snowflake CLI

Snowflake CLI is how you develop on Snowflake from the command line, from running SQL to building Snowpark, Streamlit, DCM and Native App projects. Run the [Snowflake installer](#label-snowcli-install-direct), and use [`snow upgrade`](#label-snowcli-upgrade) to move to the latest release of the same major version.

Snowflake CLI runs on all [supported platforms](/release-notes/requirements#label-client-operating-system-support).

## Install the CLI

macOSLinuxWindows

1. Run the standalone installer:

   Copy code

   ```
   curl -LsS https://sfc-repo.snowflakecomputing.com/snowflake-cli/install.sh | sh
   ```
2. In the terminal where you ran the installer, run:

   Copy code

   ```
   export PATH="$HOME/.local/share/snowflake-cli/bin:$PATH"
   ```

   The installer asks before it adds `~/.local/share/snowflake-cli/bin` to your shell profile. After you accept, open a new terminal and skip this export.
3. Check the installation:

   Copy code

   ```
   snow --version
   ```
4. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

1. Run the installer:

   Copy code

   ```
   curl -LsS https://sfc-repo.snowflakecomputing.com/snowflake-cli/install.sh | sh
   ```
2. In the terminal where you ran the installer, run:

   Copy code

   ```
   export PATH="$HOME/.local/share/snowflake-cli/bin:$PATH"
   ```

   The installer asks before it adds `~/.local/share/snowflake-cli/bin` to your shell profile. After you accept, open a new terminal and skip this export.
3. Check the installation:

   Copy code

   ```
   snow --version
   ```
4. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

1. In PowerShell, run the installer:

   Copy code

   ```
   irm https://sfc-repo.snowflakecomputing.com/snowflake-cli/install.ps1 | iex
   ```
2. Open a new terminal and check the installation:

   Copy code

   ```
   snow --version
   ```
3. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

### Upgrade an installation

`snow upgrade` updates a standalone install to the latest release of the same major version. It doesn’t install the next major version.

Copy code

```
snow upgrade
```

```
Upgraded 3.12.0 → 3.13.1.
```

Homebrew, pip, pipx, uv, and the package installers are left unchanged. The command prints the standalone installer command instead.

See [`snow upgrade`](/developer-guide/snowflake-cli/command-reference/upgrade-commands/upgrade) for `--revert` and `--dry-run`.

### Enable automatic upgrades

Add this to `config.toml`:

Copy code

```
[cli]
auto_upgrade = true
```

Automatic upgrades apply only to a standalone install. For the environment variable and other options, see [Enable automatic upgrades](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-auto-upgrade).

## Install with an OS tool

macOSLinuxWindows

Install with Homebrew or the macOS package installer.

### Homebrew

#### Homebrew formula

The community formula builds from source.

1. Install Snowflake CLI:

   Copy code

   ```
   brew install snowflake-cli
   ```
2. Upgrade later with:

   Copy code

   ```
   brew upgrade snowflake-cli
   ```

#### Snowflake tap

The Snowflake tap installs the official binary.

1. Add the tap:

   Copy code

   ```
   brew tap snowflakedb/snowflake-cli
   ```
2. Trust the cask:

   Copy code

   ```
   brew trust --cask snowflakedb/snowflake-cli/snowflake-cli
   ```
3. Install Snowflake CLI:

   Copy code

   ```
   brew install --cask snowflake-cli
   ```
4. Upgrade later with:

   Copy code

   ```
   brew upgrade --cask snowflake-cli
   ```

A Homebrew cask install works for every account on this Mac. It registers `/etc/paths.d/snowflake-cli` and doesn’t edit shell startup files.

### Install the macOS package

1. Check which package matches this Mac:

   Copy code

   ```
   uname -m
   ```

   `arm64` is Apple silicon. `x86_64` is Intel.
2. Download the package from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html). Open `darwin_arm64` or `darwin_x86_64`, then the highest version:

   ```
   darwin_arm64/<version>/snowflake-cli-<version>-darwin-arm64.pkg
   darwin_x86_64/<version>/snowflake-cli-<version>-darwin-x86_64.pkg
   ```
3. Open the `.pkg` and follow the installer.
4. Open a new terminal and check the installation:

   Copy code

   ```
   snow --version
   ```

The installer copies the application to `~/Applications` or `/Applications`. Open a new terminal after you install.

A machine-wide install in `/Applications` registers `/etc/paths.d/snowflake-cli`. It doesn’t edit shell startup files.

An install for your account adds a `PATH` entry to `~/.zprofile` for zsh, or to the first existing login profile for Bash: `~/.bash_profile`, `~/.bash_login`, or `~/.profile`. If none of those files exists, or if you use another shell, add this line to your shell configuration and open a new terminal:

Copy code

```
export PATH="$HOME/Applications/SnowflakeCLI.app/Contents/MacOS:$PATH"
```

#### Remove PATH entries from older installers

Older macOS package installers, including older Homebrew cask installs, appended `export PATH=` lines to shell startup files. Those lines can keep an outdated `snow` ahead of the current one.

1. Preview the lines the command would remove:

   Copy code

   ```
   snow helpers clean-installer-path
   ```
2. Remove them:

   Copy code

   ```
   snow helpers clean-installer-path --apply
   ```
3. Open a new terminal.

The command copies each file it changes before editing it. For details, see [snow helpers clean-installer-path](/developer-guide/snowflake-cli/command-reference/helpers-commands/clean-installer-path).

1. Check the architecture:

   Copy code

   ```
   uname -m
   ```

   `aarch64` is ARM. `x86_64` is Intel or AMD.
2. Download the package from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html). Open `linux_aarch64` or `linux_x86_64`, then the highest version:

   ```
   linux_aarch64/<version>/snowflake-cli-<version>.aarch64.deb
   linux_aarch64/<version>/snowflake-cli-<version>.aarch64.rpm
   linux_x86_64/<version>/snowflake-cli-<version>.x86_64.deb
   linux_x86_64/<version>/snowflake-cli-<version>.x86_64.rpm
   ```
3. Install the package.

   Debian and Ubuntu:

   Copy code

   ```
   sudo dpkg -i snowflake-cli-<version>.aarch64.deb
   ```

   Copy code

   ```
   sudo dpkg -i snowflake-cli-<version>.x86_64.deb
   ```

   RHEL, CentOS, and Fedora:

   Copy code

   ```
   sudo rpm -i snowflake-cli-<version>.aarch64.rpm
   ```

   Copy code

   ```
   sudo rpm -i snowflake-cli-<version>.x86_64.rpm
   ```

   Use the file that matches this machine.
4. Check the installation:

   Copy code

   ```
   snow --version
   ```

1. Download the installer from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html). Open `windows_x86_64`, then the highest version:

   ```
   windows_x86_64/<version>/snowflake-cli-<version>.0-x86_64.msi
   ```

   For version 3.32.1, the file is `snowflake-cli-3.32.1.0-x86_64.msi`.
2. Run the installer.
3. Open a new terminal and check the installation:

   Copy code

   ```
   snow --version
   ```

## Install with Python

Requires [Python](https://python.org) 3.11 or later.

uvpipxpip

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Install Snowflake CLI:

   Copy code

   ```
   uv tool install snowflake-cli
   ```
3. Upgrade later with:

   Copy code

   ```
   uv tool upgrade snowflake-cli
   ```

1. Install [pipx](https://github.com/pypa/pipx).
2. Install Snowflake CLI:

   Copy code

   ```
   pipx install snowflake-cli
   ```

1. Activate the Python environment you want to use. `pip` installs into the current environment.
2. Install Snowflake CLI:

   Copy code

   ```
   pip install snowflake-cli
   ```

## Install for FIPS

Install Snowflake CLI from source in a container whose Python is linked against a FIPS-enabled OpenSSL. The image also needs a C compiler, Python development headers, and access to PyPI or your internal package index.

1. Create and activate a virtual environment:

   Copy code

   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install the packages from source:

   Copy code

   ```
   pip install -U setuptools pip
   pip install cryptography==44.0.3 --no-binary cryptography
   pip install -U snowflake-connector-python[secure-local-storage] --no-binary snowflake-connector-python[secure-local-storage]
   pip install -U snowflake-cli --no-binary snowflake-cli
   ```
3. Confirm the OpenSSL build:

   Copy code

   ```
   python -c "import ssl; print(ssl.OPENSSL_VERSION)"
   ```

## Enable command auto-completion

1. Install completion:

   Copy code

   ```
   snow --install-completion
   ```
2. Restart the shell. Completion is available for `bash`, `zsh`, `fish`, and PowerShell.
