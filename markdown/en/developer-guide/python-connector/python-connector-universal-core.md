# Snowflake Connector for Python built on the Universal Core

Preview Feature

This feature is in public preview. Inputs and behavior may change between releases.

The Snowflake Connector for Python 5.x is built on the Universal Core. This is the next version of the connector you already use, not a new product.

The Universal Core (`sf_core`) is a shared Rust library that implements the networking, authentication, result-set fetching, and stage-transfer logic that every Snowflake driver needs. Each driver wraps that core in a thin, language-specific layer that exposes the interface its ecosystem expects; the Rust layer is not visible to application code.

Snowflake previously maintained a separate implementation of this logic in each driver, so a security fix or protocol change had to be applied separately to every one. Because the core is shared, a change to it reaches every driver built on it in that driver’s next release.

Starting with this version, the connector (the `snowflake-connector-python` package) is built on the Universal Core instead of being a pure-Python implementation. It is distributed as versions 5.x and later of the existing `snowflake-connector-python` package and targets the same interface as the pure-Python connector (versions 3.x and 4.x): the same connection parameters, the same `Connection` and `Cursor` API, and the same Python Enhancement Proposal (PEP) 249 behavior carry over, except where this page notes differences. See [Connecting to Snowflake using the Python connector](/developer-guide/python-connector/python-connector-connect) and [Using the Python connector](/developer-guide/python-connector/python-connector-example) for the existing documentation, which applies equally to this version.

Because the core is shared across drivers, this version aligns the connector’s behavior for things like array binding, retry logic, and cloud storage transfers with other Snowflake drivers. A small number of API and behavior differences result from that convergence.

This version is in public preview. Validate it against a non-production account. Preview versions are not covered by the client support policy described in [Client versions & support policy](/release-notes/requirements), and the recommended and minimum supported versions listed there refer to the generally available drivers.

For the terms that apply to preview features, see [Preview features](/release-notes/preview-features).

This page covers:

- [What’s improved](#label-python-universal-core-improvements)
- [Ecosystem compatibility](#label-python-universal-core-ecosystem)
- [Installing the release candidate](#label-python-universal-core-install)
- [Configuration differences](#label-python-universal-core-config)
- [Limitations and unsupported features](#label-python-universal-core-limitations)
- [Migrating from the previous Python driver](#label-python-universal-core-migration)
- [Behavior differences](#label-python-universal-core-behavior-differences)

## What’s improved

- **Faster data fetching:** result-set download, decompression, and decoding are handled by the Rust core rather than by Python code in the connector. The difference is largest on Arrow result sets and on large `fetchall()` calls.
- **Faster import time:** importing `snowflake.connector` does less work at module load than the pure-Python connector does, which matters most for short-lived processes such as serverless functions and command-line tools.
- **Asynchronous I/O API:** a new `snowflake.connector.aio` module exposes the same PEP 249-style `Connection` and `Cursor` objects as asyncio coroutines.

**Unified security model:** TLS, certificate revocation checking, token refresh, and OAuth flows are implemented once in the Universal Core and behave the same way across every driver built on it. A fix in any of these areas reaches all of those drivers rather than being reimplemented per language.

**Consistent cross-driver behavior:** Because networking, authentication, and stage-transfer logic live in the Universal Core, the same query, the same authentication flow, and the same error condition produce the same outcome across drivers built on it.

## Ecosystem compatibility

Most of Snowflake’s Python libraries currently declare a dependency on a connector version below 5.0.0, so they cannot be installed into the same environment as driver 5.x. The following are the requirements declared by the latest published version of each library:

| Library | Latest published version | Declared connector requirement |
| --- | --- | --- |
| Snowpark for Python (`snowflake-snowpark-python`) | 1.54.0 | `>=3.17.0,<5.0.0` |
| Snowflake CLI (`snowflake-cli`) | 3.24.1 | `==4.7.1` |
| Snowflake ML (`snowflake-ml-python`) | 1.51.0 | `>=3.17.3,<5` |
| Snowflake Python API (`snowflake-core`) | 1.13.1 | `snowflake-connector-python`, no upper bound |

Expand

Show lessSee more

Of these, only `snowflake-core` resolves against a 5.x connector, and Snowflake has not yet verified it against driver 5.x. For Snowpark, the Snowflake CLI, and Snowflake ML, continue to use the 4.x connector. Because each library sets its own requirement, check that library’s release notes for when it accepts a 5.x connector.

SnowSQL is not affected by which connector you install: it ships as a self-contained installer that bundles its own Python and connector, so you cannot substitute driver 5.x into it.

Caution

Python UDFs and stored procedures are **not yet supported** with driver 5.x. If your application deploys or relies on Python UDFs or stored procedures, stay on the 3.x/4.x driver until support is added.

## Installing the release candidate

Caution

This build of the Python driver is currently distributed as a release candidate (RC). Do not use it with production workloads. It is published under the same package name (`snowflake-connector-python`) as your current driver, so only one version can be installed in a given environment at a time. Install the RC into a separate virtual environment rather than upgrading your production environment in place.

### Prerequisites

- Python 3.11 or later. Wheels are published for CPython 3.11, 3.12, 3.13, and 3.14.

### Install the new version

Because release candidates are pre-release versions, `pip` and other installers do not install them by default. Snowflake recommends installing the RC into a dedicated virtual environment rather than upgrading your production environment in place:

> Copy code
>
> ```
> python -m venv ud-preview
> source ud-preview/bin/activate     # on Windows: ud-preview\Scripts\activate
>
> pip install --pre --upgrade snowflake-connector-python
> ```

To pin a specific release-candidate build instead of always taking the latest pre-release, specify the version explicitly:

> Copy code
>
> ```
> pip install snowflake-connector-python==5.0.0rc3
> ```

Optional extras such as `pandas` install the same way as with the current driver:

> Copy code
>
> ```
> pip install --pre --upgrade "snowflake-connector-python[pandas]"
> ```

Verify which version is active:

> Copy code
>
> ```
> import snowflake.connector
> print(snowflake.connector.__version__)
> ```

A version beginning with `5.` confirms you are running the Universal-Core-based driver rather than the pure-Python 3.x or 4.x connector.

### Installing from source

If you want to build the RC from source instead of installing from PyPI, for example to test an unreleased fix, you need a few additional prerequisites beyond a normal `pip install`, because the package compiles a Rust extension as part of the build:

- [Rust toolchain](https://www.rust-lang.org/tools/install) (stable channel), for compiling the Universal Core.
- [Git](https://git-scm.com/), to clone the source repository.
- A C compiler toolchain for your platform, for example Xcode Command Line Tools on macOS, `build-essential` on Debian/Ubuntu, or the Visual Studio Build Tools on Windows. Some of the driver’s own dependencies require it.

Then build and install the package:

> Copy code
>
> ```
> git clone https://github.com/snowflakedb/drivers.git
> cd drivers/python
>
> python -m venv ud-preview
> source ud-preview/bin/activate     # on Windows: ud-preview\Scripts\activate
>
> pip install .
> ```

The Rust core is compiled automatically as part of this `pip install` step; you do not need to invoke `cargo` yourself. Building from source takes noticeably longer than installing the prebuilt wheel from PyPI, because the Rust core is compiled locally.

## Configuration differences

Most connection parameters behave as they do in the 4.x connector. The items below are specific to this version.

### Certificate revocation checking

Drivers built on the Universal Core do not support OCSP-based certificate revocation checking. Starting with the public preview versions, revocation checking is available only through CRLs (certificate revocation lists), and it is off by default.

This aligns with the broader move away from OCSP, which has been a frequent cause of production outages and offers little real security in its default fail-open mode.

If you require revocation checking, enable CRL checking and evaluate it in a non-production environment under a realistic workload. Confirm that your network allows outbound access to the CRL distribution points named in Snowflake’s certificate chain: a driver that cannot reach a distribution point cannot complete a revocation check.

The CRL caches are controlled by `enable_crl_memory_cache` and `enable_crl_file_cache`, which replace `enable_crl_cache`.

## Limitations and unsupported features

The Universal-Core-based Python driver is not yet at full parity with the pure-Python connector. The items below are the current known behavior changes with the highest chance of affecting existing applications. This list reflects the driver’s behavior-difference catalog as of this RC and will shrink as the driver approaches general availability; re-check this page before upgrading a later RC build.

### Behavior changes worth validating before you upgrade

These are not missing features, but they change what your application should expect to observe:

- **Removed OCSP support in favor of CRLs.** The Python connector 5.x does not implement OCSP and performs revocation checking through CRLs only, off by default; 4.x performed OCSP checking by default. OCSP connection parameters are rejected rather than ignored. *(BD#58)*
- `session_token` connections now require `master_token` and are validated eagerly at `connect()` time, rather than lazily on first use.
- Cursor methods now consistently raise `InterfaceError` after a cursor or connection is closed, and `ProgrammingError` when you fetch before executing a query. The pure-Python connector raised inconsistent errors (`TypeError`, `AttributeError`, or nothing) depending on the method.
- `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` environment variables are **not** consulted unless you opt in with `use_proxy_env=True`. The pure-Python connector (3.17.0+) read them unconditionally.
- OAuth client-credential and authorization-code flows now require the token/authorization endpoint to use `https://` (loopback hosts are exempt). A plaintext `http://` endpoint is rejected at connect time instead of only logging a warning.
- S3 endpoint resolution for `cn-*` regions is delegated to the AWS SDK’s own resolver when no regional-URL flag is set. This has not yet been verified end-to-end against a live `cn-*` region stage.

Note

Several other parameters were renamed for consistency with other Snowflake drivers: `private_key_file_pwd` is now `private_key_password`, `client_request_mfa_token` is now `client_store_temporary_credential`, and `enable_stage_s3_privatelink_for_us_east_1` is now `use_s3_regional_url`. The previous names still work but emit a `DeprecationWarning`. See [Migrating from the previous Python driver](#label-python-universal-core-migration) for the full checklist.

## Migrating from the previous Python driver

Most applications require no code changes beyond upgrading the package. The steps below help you find the applications that do.

### Step 1: Install the RC in an isolated environment and run your test suite

Because the RC shares a package name with your current driver, it cannot be installed alongside it in the same environment. Install the RC into a separate virtual environment (see [Installing the release candidate](#label-python-universal-core-install)) and run your existing test suite against it, pointed at a non-production account. Run Python with deprecation warnings elevated to errors so that renamed parameters surface immediately instead of silently working. For example, if you use pytest:

> Copy code
>
> ```
> python -W error::DeprecationWarning -m pytest
> ```

Pass `-W error::DeprecationWarning` to whatever test runner or entry point you use.

Alternatively, if your project declares its dependencies in `pyproject.toml`, pin the release-candidate version there instead of installing it directly with `pip install`:

> Copy code
>
> ```
> [project]
> dependencies = [
>     "snowflake-connector-python==5.0.0rc3",
> ]
> ```

Then reinstall your project’s dependencies with your usual tool, for example `pip install --upgrade .`, `uv sync`, or `poetry lock && poetry install`, so the pinned RC is picked up.

### Step 2: Update renamed parameters

The following previous parameter names still work on the Universal Core but emit a `DeprecationWarning`. Update call sites proactively rather than relying on the alias long-term:

| Previous name | New name |
| --- | --- |
| `private_key_file_pwd` | `private_key_password` |
| `client_request_mfa_token` | `client_store_temporary_credential` |
| `client_fetch_threads` | `client_prefetch_threads` |
| `enable_stage_s3_privatelink_for_us_east_1` | `use_s3_regional_url` |
| `create_temp_table=True` (in `write_pandas`) | `table_type='temp'` |

Expand

Show lessSee more

### Step 3: Remove usage of parameters and methods that no longer have an effect or no longer exist

Unlike the renames above, these do not have a working alias and require a code change:

- Replace any use of `Connection.connect()` for re-authentication with constructing a new `Connection`.
- Replace `region` with a fully qualified `account` value or an explicit `host`.
- If you disabled CRL caching with `enable_crl_cache=False`, set `enable_crl_memory_cache=False` and `enable_crl_file_cache=False` instead.
- If you depend on `client_fetch_use_mp` (process-pool chunk fetching), there is currently no replacement; measure whether the default thread pool is sufficient for your workload.
- If your code reads `ResultBatch.session_manager` or `ResultBatch.http_config` to control HTTP behavior for chunk downloads after closing the connection, remove that code; chunk fetching is now handled internally and does not require an active-connection workaround.

### Step 4: Re-check error handling around cursors and fetches

If your code catches `TypeError` or `AttributeError` around cursor operations to detect a closed cursor or a fetch-before-execute condition, update it to catch `InterfaceError` and `ProgrammingError` respectively, which the driver now raises consistently. This aligns the driver’s error handling with the exception hierarchy defined by [PEP 249](https://peps.python.org/pep-0249/#exceptions): `InterfaceError` and `ProgrammingError` are the exceptions PEP 249 itself specifies for these conditions.

### Step 5: Re-check proxy and OAuth endpoint configuration

- If you rely on `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` environment variables being picked up automatically, set `use_proxy_env=True` on the connection.
- If you use `oauth_token_request_url` or `oauth_authorization_url` with a plaintext `http://` endpoint (other than a loopback address), switch it to `https://`.

## Behavior differences

Every behavior difference between the generally available driver and the version built on the Universal Core is catalogued in the driver source repository, as a machine-readable file listing each entry’s previous behavior, new behavior, classification, and whether it is a breaking change. Read it in full before you upgrade an application you cannot easily roll back:

- [Snowflake Connector for Python 5.x behavior-difference catalog](https://github.com/snowflakedb/drivers/blob/main/python/BehaviorDifferences.yaml)

The sections above summarize the entries most likely to affect an existing application. The catalog is the complete list.

The table below is a snapshot of that catalog as of this RC, including low-impact and non-breaking entries not called out elsewhere on this page.

| Name | Type | Breaking change | Impact |
| --- | --- | --- | --- |
| Closed cursor raises InterfaceError on all operations | bugfix | Yes | High |
| Fetching before execute raises ProgrammingError | bugfix | Yes | High |
| Connection does not expose a public connect() method | api\_incompatibility | Yes | High |
| client\_fetch\_threads deprecated; client\_fetch\_use\_mp removed | api\_incompatibility | Yes | High |
| client\_session\_keep\_alive[\_heartbeat\_frequency] setters removed | api\_incompatibility | Yes | High |
| S3 endpoint for cn-\* regions delegated to AWS SDK | unknown | Yes | High |
| oauth\_enable\_refresh\_tokens parameter has no effect | api\_incompatibility | Yes | High |
| enable\_stage\_s3\_privatelink\_for\_us\_east\_1 renamed to use\_s3\_regional\_url | api\_incompatibility | Yes | High |
| HTTP\_PROXY/HTTPS\_PROXY env vars are not consulted by default | api\_incompatibility | Yes | High |
| Azure Blob PUT does not set Content-Encoding header | bug | Yes | High |
| Header of a gzip-compressed file does not contain filename | bug | Yes | Medium |
| DEFLATE compression type option is now correctly auto-detected | bugfix | Yes | Medium |
| Empty connections.toml preserves config.toml connections | bugfix | Yes | Medium |
| Session parameter updates visible across cursors without execute | enhancement | Yes | Medium |
| region connection parameter and Connection.region property removed | api\_incompatibility | Yes | Medium |
| BROTLI compression type option is now supported | enhancement | Yes | Low |
| Private key password parameter name changed | api\_incompatibility | No | Low |
| CONFIG\_PARSER deprecated alias removed | api\_incompatibility | Yes | Low |
| Deprecated add\_subparser method and \_sub\_parsers property removed | api\_incompatibility | Yes | Low |
| ConfigManager without file\_path returns MissingConfigOptionError on option retrieval | bug | Yes | Low |
| MFA token caching parameter renamed | api\_incompatibility | No | Low |
| rest.request() validates HTTP method (internal API) | enhancement | Yes | Low |
| JSONResultBatch supports Arrow and Pandas conversion | enhancement | Yes | Low |
| write\_pandas create\_temp\_table: DeprecationWarning alias restored for Snowpark compat | api\_incompatibility | No | Low |
| ResultBatch does not expose session\_manager or http\_config | api\_incompatibility | Yes | Low |
| oauth\_credentials\_in\_body sends client\_secret\_post (body only, not body+header) | api\_incompatibility | No | Low |
| Concurrent interactive auth prompts are serialized (disable\_parallel\_user\_prompt) | enhancement | No | Low |
| executemany uses server arrayBindSupported flag to gate array binding | enhancement | No | Low |
| OAuth bad client secret surfaces IdP error slug instead of generic browser message | enhancement | Yes | Low |
| Session token authentication: eager validation and master\_token requirement | enhancement | Yes | Low |
| OAuth token/authorization endpoint URLs must use HTTPS (non-loopback http rejected) | enhancement | Yes | Low |
| Failed GET download no longer leaves an orphaned .part file | bugfix | No | Low |
| Azure SAS refresh triggers on any 403, not only token-expiry-reason matches | enhancement | No | Low |
| Terminal Azure 403 after SAS refresh is logged with outcome-tiered severity | enhancement | No | Low |
| enable\_crl\_cache removed; CRL caches controlled by independent toggles | api\_incompatibility | Yes | Low |
| file\_stream on a non-PUT statement raises ProgrammingError instead of being silently ignored | enhancement | Yes | Low |
| GCS PUT on matching content re-uploads by default (honors skip\_upload\_on\_content\_match) | bugfix | Yes | Low |

Expand

Show lessSee more
