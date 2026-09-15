# Installing Snowflake CLI

This topic explains how to install Snowflake CLI on [supported platforms](/release-notes/requirements#label-client-operating-system-support). Note that Snowflake CLI is not currently available for AIX systems.

Snowflake recommends using binary installation methods, such as package managers, to install Snowflake CLI on your system.
You can download the binary installers from the official [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).

## Requirements

To use Snowflake CLI, you need a valid Snowflake account with the privileges required for the features you intend to use.

Tip

If your Snowflake account requires MFA (multi-factor authentication), Snowflake CLI requires approval for every command. You can use MFA caching to require
authentication only once every four hours. For more information, see [Use multi-factor authentication (MFA)](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-mfa).

## Install Snowflake CLI using package managers

Select your operating system below.

macOSLinuxWindows

On macOS you can install Snowflake CLI with [Homebrew](#label-snowcli-install-homebrew) or with the [macOS package installer](#label-snowcli-install-macos-installer).

### Homebrew

Install [Homebrew](https://brew.sh/) if necessary, then choose one of the following installation methods.

#### Option 1: Homebrew core formula

The Homebrew community maintains a `snowflake-cli` formula that is updated automatically. It might not include the latest release.

1. Install Snowflake CLI:

   Copy code

   ```
   brew install snowflake-cli
   ```
2. Verify that the software was installed successfully:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
3. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

To upgrade, run:

Copy code

```
brew upgrade snowflake-cli
```

#### Option 2: Snowflake-maintained tap (recommended)

Snowflake maintains a tap that distributes a pre-built binary (cask) updated with every release. Homebrew requires you to explicitly trust third-party taps before installing casks from them.

1. Add and trust the Snowflake tap:

   Copy code

   ```
   brew tap snowflakedb/snowflake-cli
   brew trust --cask snowflakedb/snowflake-cli/snowflake-cli
   ```
2. Install Snowflake CLI:

   Copy code

   ```
   brew install --cask snowflake-cli
   ```
3. Verify that the software was installed successfully:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
4. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

To upgrade, run:

Copy code

```
brew upgrade --cask snowflake-cli
```

### macOS package installer

1. Download the Snowflake CLI installer from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).
2. Run the installer and follow the instructions.
3. To verify that the software was installed successfully, open a new terminal and run the following command:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
4. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

On Linux, Snowflake CLI is distributed as both `deb` packages (Debian, Ubuntu) and `rpm` packages (RHEL, CentOS, Fedora).

### Debian and Ubuntu (`deb`)

1. Download the Snowflake CLI `deb` package from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).
2. Install the package:

   Copy code

   ```
   sudo dpkg -i snowflake-cli-<version>.deb
   ```
3. Verify that the software was installed successfully:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
4. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

### RHEL, CentOS, and Fedora (`rpm`)

1. Download the Snowflake CLI `rpm` package from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).
2. Install the package:

   Copy code

   ```
   sudo rpm -i snowflake-cli-<version>.rpm
   ```
3. Verify that the software was installed successfully:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
4. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

On Windows, install Snowflake CLI with the package installer.

### Windows installer

1. Download the Snowflake CLI installer from the [Snowflake CLI repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).
2. Run the installer and follow the instructions.
3. To verify that the software was installed successfully, open a new terminal and run the following command:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
4. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

## Install Snowflake CLI as a Python tool

You can also install Snowflake CLI as a Python package using `uv`, `pipx`, or `pip`.

All Python-tool installation methods require [Python](https://python.org) version 3.10 or later.

uvpipxpip

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager. The `uv tool` subcommand installs Python packages into isolated environments and exposes their executables on your `PATH`, so it doesn’t modify your current Python environment.

To install Snowflake CLI using `uv`, you must have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

1. Run the following shell command:

   Copy code

   ```
   uv tool install snowflake-cli
   ```
2. To verify that the software was installed successfully, run the following command:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
3. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

To upgrade an existing installation, run:

Copy code

```
uv tool upgrade snowflake-cli
```

[pipx](https://github.com/pypa/pipx) installs and runs Python packages in isolated virtual environments, so it doesn’t modify your current Python environment.

To install Snowflake CLI using `pipx`, you must have [pipx](https://github.com/pypa/pipx) installed.

1. Run the following shell command:

   Copy code

   ```
   pipx install snowflake-cli
   ```
2. To verify that the software was installed successfully, run the following command:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
3. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

Note

This method modifies the Python environment where you install Snowflake CLI. Consider [`uv`](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-uv) or [`pipx`](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-pipx) instead to avoid dependency conflicts.

1. Run the following shell command:

   Copy code

   ```
   pip install snowflake-cli
   ```
2. To verify that the software was installed successfully, run the following command:

   Copy code

   ```
   snow --help
   ```

   ```
   Usage: snow [OPTIONS] COMMAND [ARGS]...

   Snowflake CLI tool for developers.

   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --version                           Shows version of the Snowflake CLI                                                                   │
   │ --info                              Shows information about the Snowflake CLI                                                            │
   │ --config-file                 FILE  Specifies Snowflake CLI configuration file that should be used [default: None]                       │
   │ --install-completion                Install completion for the current shell.                                                            │
   │ --show-completion                   Show completion for the current shell, to copy it or customize the installation.                     │
   │ --help                -h            Show this message and exit.                                                                          │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ app          Manages a Snowflake Native App                                                                                              │
   │ connection   Manages connections to Snowflake.                                                                                           │
   │ cortex       Provides access to Snowflake Cortex.                                                                                        │
   │ git          Manages git repositories in Snowflake.                                                                                      │
   │ notebook     Manages notebooks in Snowflake.                                                                                             │
   │ object       Manages Snowflake objects like warehouses and stages                                                                        │
   │ snowpark     Manages procedures and functions.                                                                                           │
   │ spcs         Manages Snowpark Container Services compute pools, services, image registries, and image repositories.                      │
   │ sql          Executes Snowflake query.                                                                                                   │
   │ stage        Manages stages.                                                                                                             │
   │ streamlit    Manages a Streamlit app in Snowflake.                                                                                       │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
3. [Configure the Snowflake connection](/developer-guide/snowflake-cli/connecting/connect).

## Install Snowflake CLI in FIPS-compliant environments

You can use a Docker image to install Snowflake CLI in an environment that is compliant with FIPS (Federal Information Processing Standards).

### Prerequisites

Before installing Snowflake CLI in a FIPS-compliant environment, ensure that you meet the following prerequisites:

- **FIPS-compliant Python**: Python must be preinstalled, built, and configured for FIPS compliance. This typically means Python is linked against a FIPS-enabled OpenSSL library.
- **FIPS-enabled OpenSSL**: The system’s OpenSSL libraries must be FIPS-compliant and available to Python at runtime.
- **Build tools**: Standard build tools (such as a C compiler and Python development headers) must be available, as dependencies will be built from source.
- **Network Access**: The environment must allow access to PyPI or your internal package index for downloading source distributions.

### Install Snowflake CLI in a FIPS-compliant Dockerfile

To install Snowflake CLI in a FIPS-compliant environment, follow these steps:

1. Create a Python virtual environment in the container, as shown in the following example:

   Copy code

   ```
   python -m venv .venv
   ```
2. Activate the Python virtual environment in the container, as shown in the following example:

   Copy code

   ```
   source ~/.venv/bin/activate
   ```
3. Upgrade `pip` and `setuptools` in the container, as shown in the following example:

   Copy code

   ```
   pip install -U setuptools pip
   ```
4. Install the cryptography, Python connector, and Snowflake CLI dependencies from source in the container, as shown in the following example. Note that all dependencies must be installed from source to ensure they are built against your FIPS-compliant libraries.

   Copy code

   ```
   pip install cryptography==44.0.3 --no-binary cryptography
   pip install -U snowflake-connector-python[secure-local-storage] --no-binary snowflake-connector-python[secure-local-storage]
   pip install -U snowflake-cli --no-binary snowflake-cli
   ```

   The `--no-binary` option forces installation from source, ensuring that the builds use FIPS-ready libraries.

### Validate the Docker image

To confirm that your Python environment uses a FIPS-enabled OpenSSL library, enter the following command in the running container:

Copy code

```
python -c "import ssl; print(ssl.OPENSSL_VERSION)"
```

After installing Snowflake CLI and validating the Docker image, you can use Snowflake CLI in the container.

Copy code

```
snow <your-command>
```

where <*your-command*> is any valid Snowflake CLI command, such as `snow --help`.

## Install command auto-completion functionality

Snowflake CLI supports tab completion for `bash`, `zsh`, `fish`, and PowerShell. The completion command auto-detects your current shell.

1. Run the following command:

   Copy code

   ```
   snow --install-completion
   ```

   The output reports the shell that completion was installed for, along with where the completion script was written. For example, in `zsh`:

   ```
   zsh completion installed in <user home>/.zfunc/_snow
   Completion will take effect once you restart the terminal
   ```
2. To apply the change, restart your shell or source your shell profile. For example:

   Copy code

   ```
   source ~/.zshrc
   ```

Note

If `snow --install-completion` doesn’t modify your shell profile (for example, in environments with non-standard shell setups), you can install completion manually:

1. Run `snow --show-completion` to print the completion script for your current shell.
2. Append the printed script to your shell profile (`.bashrc`, `.zshrc`, `.config/fish/config.fish`, or your PowerShell profile).
3. Restart your shell, or source the profile.
