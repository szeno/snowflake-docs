# Installing the Python Connector

Important

`pip install --upgrade snowflake-connector-python` installs version 5.x. Snowpark for Python, Snowflake ML, Snowflake SQLAlchemy, and Snowflake CLI still require a connector version before 5.0. Upgrading a shared environment can make those libraries fail to install or to import. Check the pins in [Upgrade steps](/developer-guide/python-connector/python-connector-upgrade#label-python-upgrade-steps) before you upgrade.

To install the latest Python Connector for Snowflake, use:

> Copy code
>
> ```
> pip install snowflake-connector-python
> ```

Note

Pin a release before 5.0 if you need the previous connector, for example `snowflake-connector-python>=4,<5`.

You can download the package files directly from [PyPI](https://pypi.org/project/snowflake-connector-python/).

Note

Before version 5.0, the connector was published from [snowflake-connector-python](https://github.com/snowflakedb/snowflake-connector-python).

## Prerequisites

Requires Python 3.11 or later. Wheels are published for CPython 3.11, 3.12, 3.13, 3.14, and 3.14t (free-threaded CPython). Windows on ARM does not include a 3.14t wheel.

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

## Installing a FIPS-supporting version

Note

These instructions work only for version 5.0 and later.

Before you build or use a FIPS-supporting version, review [FIPS 140-3 considerations for drivers built on the Universal Core](/developer-guide/universal-core/universal-core-fips). That page describes the AWS-LC FIPS module, known deviations, behavior differences, common build requirements, verification, and SBOM responsibilities for drivers built on the Universal Core.

A FIPS-supporting version links the FIPS module into the connector. Install it from the PyPI source distribution. Prebuilt wheels are standard builds, and `pip install` uses a wheel by default. `SNOWFLAKE_FIPS` is read only while pip builds that unpacked source distribution. Building from a git checkout, including an editable install or a wheel build from that checkout, fails if the variable is set.

Pass `--no-binary` for this package so pip downloads the source distribution and builds it. The flag names the distribution, `snowflake-connector-python`, and doesn’t apply to dependencies. On Linux and macOS:

> Copy code
>
> ```
> SNOWFLAKE_FIPS=1 python -m pip install --no-binary snowflake-connector-python snowflake-connector-python
> ```

On Windows, set the variable in PowerShell, then run the same install:

> Copy code
>
> ```
> $env:SNOWFLAKE_FIPS = "1"
> python -m pip install --no-binary snowflake-connector-python snowflake-connector-python
> ```

This version doesn’t build on Windows on ARM. On Linux, the module is linked into the connector. On macOS and Windows, the install places the module’s shared libraries next to the connector.

Confirm the installed build without opening a connection:

> Copy code
>
> ```
> import snowflake.connector
>
> status = snowflake.connector.get_fips_status()
> print(status.is_fips)
> ```

The value is `True` for a FIPS-supporting version and `False` for a standard version. A true value means this process loaded that version and its TLS provider is the FIPS module. It does not mean that every cryptographic operation in the process uses that module, and it does not certify the connector.

A FIPS-supporting version needs [Rust](https://www.rust-lang.org/tools/install) 1.94.1, a C++ compiler, `curl`, `unzip`, [Go](https://go.dev/dl/) 1.25, Perl, and CMake 3. `curl` and `unzip` download the protobuf compiler. To use a compiler you already have, set `PROTOC` to the path of that `protoc` binary. CMake 4 isn’t supported.

The C++ compiler depends on the platform:

- On Linux, use GCC 13. GCC 14 and GCC 15 fail to build the module. Install `gcc-13` and `g++-13`, then set `CC=gcc-13` and `CXX=g++-13` for the install command. On Linux ARM64, also set `CFLAGS=-fno-jump-tables` and `CXXFLAGS=-fno-jump-tables`.
- On macOS, use Apple Clang. Set `CC=clang` and `CXX=clang++`.
- On Windows x64, use MSVC, Ninja, Perl, NASM, and LLVM Clang. Set `LIBCLANG_PATH` to the directory that contains `libclang.dll`. Put the MSVC directory that contains `link.exe` ahead of other `link.exe` programs on `PATH`. If you use Strawberry Perl, put `C:\Strawberry\perl\bin` on `PATH` and leave `C:\Strawberry\c\bin` off `PATH`, because its `gcc` shadows MSVC.
