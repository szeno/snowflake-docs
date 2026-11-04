# Installing Snowflake CLI

Snowflake CLI is how you develop on Snowflake from the command line, from running SQL to building Snowpark, Streamlit, DCM and Native App projects. Run the [Snowflake installer](#label-snowcli-install-direct), and use [`snow upgrade`](#label-snowcli-upgrade) to move to the latest release of the same major version.

Snowflake CLI runs on all [supported platforms](/release-notes/requirements#label-client-operating-system-support).

## Run the Snowflake installer

macOSLinuxWindows

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

### Upgrade a standalone install

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

### Install the macOS package

1. Download the installer from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).
2. Run the installer.

1. Download the package from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).
2. Install the package.

   Debian and Ubuntu:

   Copy code

   ```
   sudo dpkg -i snowflake-cli-<version>.deb
   ```

   RHEL, CentOS, and Fedora:

   Copy code

   ```
   sudo rpm -i snowflake-cli-<version>.rpm
   ```

1. Download the installer from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).
2. Run the installer.

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
