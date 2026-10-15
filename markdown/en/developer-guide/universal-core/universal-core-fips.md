# FIPS 140-3 considerations for drivers built on the Universal Core

Drivers built on the [Universal Core](/developer-guide/universal-core/universal-core) can be built so that the core performs most of
its security-relevant cryptography with the FIPS module of [AWS-LC](https://github.com/aws/aws-lc), the open source cryptographic
library from AWS that the core uses, instead of the library’s standard build. On this page, a
*FIPS build* means a driver whose Universal Core was built with the `fips` build option. Use this page if your organization applies
Federal Information Processing Standard (FIPS) 140-3 requirements to the software that connects to Snowflake.

Important

Drivers built on the Universal Core aren’t FIPS 140-3 validated, and Snowflake doesn’t claim that any build of them, including a
FIPS build, is FIPS compliant. A FIPS build uses a version of the AWS-LC FIPS module that isn’t covered by a Cryptographic Module
Validation Program (CMVP) certificate, and some operations run outside the module. You’re responsible for determining whether a
build meets your requirements.

This page covers:

- [Drivers this page applies to](#label-universal-core-fips-scope)
- [Cryptographic module](#label-universal-core-fips-module)
- [Why AWS-LC FIPS 3.6.0 instead of 3.1.0](#label-universal-core-fips-module-version)
- [Known deviations](#label-universal-core-fips-deviations)
- [Behavior differences in a FIPS build](#label-universal-core-fips-behavior)
- [Check that your application loaded a FIPS build](#label-universal-core-fips-status)
- [Software bills of materials (SBOMs)](#label-universal-core-fips-sbom)
- [Build from source with the FIPS module](#label-universal-core-fips-build)
- [Build with a different AWS-LC FIPS module](#label-universal-core-fips-other-module)
- [Recommendations](#label-universal-core-fips-recommendations)

## Drivers this page applies to

This page applies only to drivers built on the Universal Core. For the FIPS options of drivers that aren’t built on it, such as
the `snowflake-jdbc-fips` JAR file of the JDBC driver, see that driver’s documentation.

A FIPS build isn’t the default. A driver that supports one delivers it in one of the following ways:

- **An artifact that Snowflake builds:** The FIPS build is a separate artifact that Snowflake builds and publishes next to the
  standard build.
- **A build from source:** You build the driver from its public source code with the `fips` build option turned on.

Each driver’s documentation states whether that driver supports a FIPS build and which of these ways applies. The way that you
obtain a FIPS build also determines who provides its software bill of materials (SBOM). For more information, see
[Software bills of materials (SBOMs)](#label-universal-core-fips-sbom).

## Cryptographic module

The `fips` build option, which is the `fips` Cargo feature of the `sf_core` crate, links version 3.6.0 of the AWS-LC FIPS module
(AWS-LC FIPS 3.6.0) into the driver. The module comes from the `aws-lc-fips-sys` crate, which the core pins to exactly version
0.13.17, so a dependency update can’t change the module without an edit to the core’s source. A test in the core checks that the
linked module reports the version `AWS-LC FIPS 3.6.0` and that it runs in FIPS mode. Without the `fips` option, the core uses the
standard (non-FIPS) build of AWS-LC.

Whether a driver uses the FIPS module is decided when the driver is built. No connection parameter turns a standard build into a
FIPS build.

In a FIPS build, the core performs the following operations with the AWS-LC FIPS module:

- **TLS:** Securing connections to Snowflake and to cloud storage, including verifying certificate chains.
- **Certificate revocation checking:** Downloading certificate revocation lists (CRLs) over HTTPS and verifying their signatures.
- **Key pair authentication:** Decrypting encrypted private keys (PBKDF2 and AES) and signing JSON Web Tokens (JWTs) with RSA.
- **Client-side encryption for stage file transfers:** Encrypting file contents with AES-CBC, wrapping file keys, computing file
  digests, and generating random keys and initialization vectors.
- **OAuth:** Generating random values for PKCE, the `state` parameter, and DPoP proofs; computing the PKCE code challenge; and
  signing DPoP proofs with ECDSA on the P-256 curve.
- **Workload identity federation on AWS:** Signing the attestation request with HMAC-SHA-256.

The Universal Core doesn’t use OpenSSL or the `ring` library for cryptography in the code that it ships. A driver’s packaging can
bring other cryptographic libraries into your application’s process; that driver’s documentation lists them.

## Why AWS-LC FIPS 3.6.0 instead of 3.1.0

CMVP certificates cover AWS-LC FIPS 3.1.0:
[certificate #5314](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5314) for the static module
and [certificate #5298](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5298) for the dynamic
module. Both are FIPS 140-3 certificates. Their Security Policies list Amazon Linux 2023 on two specific hardware platforms as the
only tested operational environments, and the certificates apply when the module is installed, initialized, and configured as
specified in Section 11.1 of its Security Policy. That section names the exact source archive to build the module from and doesn’t
allow changes to it.

Snowflake chose AWS-LC FIPS 3.6.0 instead, because the `aws-lc-fips-sys` release that carries AWS-LC FIPS 3.1.0 (version 0.13.11)
is affected by two vulnerabilities that later module versions fix:

- [CVE-2026-3337 (RUSTSEC-2026-0043)](https://rustsec.org/advisories/RUSTSEC-2026-0043.html): A timing side channel in AES-CCM
  tag verification. Fixed in AWS-LC FIPS 3.2.0 (`aws-lc-fips-sys` 0.13.12).
- [CVE-2026-4428 (RUSTSEC-2026-0042)](https://rustsec.org/advisories/RUSTSEC-2026-0042.html): A logic error in CRL
  distribution-point checks that can let a revoked certificate pass revocation checking when partitioned CRLs are used. Fixed in
  AWS-LC FIPS 3.3.0 (`aws-lc-fips-sys` 0.13.13).

Applying these fixes to AWS-LC FIPS 3.1.0 would change the module’s source, so the result would no longer be the module that the
certificates cover. Even without changes, a 3.1.0 module that runs outside the tested operational environments, such as on another
Linux distribution, macOS, or Windows, is a port that the CMVP makes no statement about. Downgrading to 3.1.0 therefore wouldn’t
give drivers built on the Universal Core a module that the certificates cover, and it would reintroduce both vulnerabilities.

As a result, no CMVP certificate covers the module in a FIPS build, and Snowflake doesn’t claim that one does. To check the current
validation status of AWS-LC modules, search the CMVP
[validated modules](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search) and
[modules in process](https://csrc.nist.gov/projects/cryptographic-module-validation-program/modules-in-process/modules-in-process-list)
lists.

## Known deviations

In a FIPS build, the following operations run outside the AWS-LC FIPS module or use a construction that isn’t approved for FIPS
140-3.

### File-key wrapping with AES-ECB

When the `PUT` command uses client-side encryption, the driver encrypts each file with a random file key, using AES-CBC, and wraps
the file key with the stage’s master key, using AES in ECB mode. The `GET` command reverses both steps. All of these operations run
inside the module, but raw AES-ECB isn’t an approved key-wrapping construction, such as AES-KW or AES-KWP. Running it inside the
module doesn’t make it one.

The Snowflake stage service and other Snowflake drivers use the same wrapping format. A driver that switched to an approved
key-wrapping construction on its own couldn’t read or write the files that other clients use, so changing the format requires a
coordinated change to the stage protocol.

Named internal stages that use server-side encryption only, which you create with `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')`, avoid
this deviation. The driver doesn’t encrypt files on the client for those stages, so it doesn’t wrap a file key. Before you choose
server-side encryption only, review its tradeoffs in
[Internal stage parameters](/sql-reference/sql/create-stage#label-create-stage-internalstageparams). For example, you can’t change
a stage’s encryption type after you create it.

### Request signing for stages in Amazon S3

For stages in Amazon S3, the driver transfers files with the AWS SDK for Rust. The SDK signs each request with AWS Signature
Version 4 (SigV4), and it computes the HMAC-SHA-256 for that signature with a Rust implementation (RustCrypto) instead of the
module. This applies to every `PUT` and `GET` command for an account hosted on AWS, because the internal stages of those accounts
are stored in Amazon S3. The driver doesn’t replace the SDK’s signer.

The driver’s own signing, such as the attestation request for workload identity federation on AWS, uses the module. Moving the
SDK’s signer into the module depends on a change proposed in the SDK
([smithy-lang/smithy-rs#4874](https://github.com/smithy-lang/smithy-rs/pull/4874)) and on an SDK release that the driver can
adopt.

### Integrity checksums

The driver computes an MD5 checksum (Content-MD5) when it uploads files to stages in Microsoft Azure, and some checksums that the
AWS SDK computes for requests to Amazon S3 use MD5 or SHA-1. These checksums detect accidental data corruption. They aren’t used for
authentication or encryption, and they’re computed outside the module.

## Behavior differences in a FIPS build

A FIPS build behaves like a standard build of the same driver, except for the following differences:

- **Certificate verification can’t be turned off:** Connection settings that turn off TLS certificate verification are rejected
  with an error. In the Universal Core, these settings are `verify_certificates=false` and `tls_skip_verify=true`. Each driver
  might expose them under different names.
- **TLS uses FIPS-approved cipher suites only:** The driver negotiates TLS 1.2 or TLS 1.3 and offers only the cipher suites that
  the TLS library allows in FIPS mode.
- **Some encrypted private keys are rejected:** For key pair authentication, a FIPS build rejects the following keys:

  - PKCS#8 private keys encrypted with Triple DES (3DES-CBC).
  - Private keys in the traditional encrypted PEM format, which have a `Proc-Type: 4,ENCRYPTED` header. Decrypting them requires
    an MD5-based key derivation.

  A FIPS build accepts PKCS#8 private keys encrypted with AES. The command for an encrypted key in
  [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth) produces a key that a FIPS build accepts.

To convert a rejected key, re-encrypt it with AES-256-CBC:

Copy code

```
openssl pkcs8 -topk8 -v2 aes-256-cbc -in old_rsa_key.pem -out rsa_key.p8
```

The command prompts for the current passphrase and for a new one. If your OpenSSL installation runs in FIPS mode, it might not be
able to decrypt the old key; run the conversion where the old key’s algorithms are available.

## Check that your application loaded a FIPS build

Drivers built on the Universal Core that support a FIPS build provide a status call that reports whether the running process
loaded a FIPS build. The call is available in both builds, and it doesn’t open a connection or use the network:

- `is_fips` is true when the driver was built with the `fips` option and its TLS provider runs in FIPS mode.
- `is_fips` is false in a standard build. It’s also false in a FIPS build whose TLS provider didn’t start in FIPS mode.

A true value means that your process loaded the AWS-LC FIPS module and that the module runs in FIPS mode. It doesn’t mean that the
driver or your build is FIPS 140-3 validated, so don’t read it as a compliance claim. It also doesn’t confirm a CMVP certificate or
a module version, and the [known deviations](#label-universal-core-fips-deviations) still apply.

Make the status call once when your application starts, before it opens a connection, and stop if `is_fips` is false. That way,
a deployment that loads the standard build by mistake fails at startup instead of running without the module. Each driver’s
documentation gives the exact call for its language.

## Software bills of materials (SBOMs)

An SBOM describes one specific binary. Who provides the SBOM for a FIPS build depends on how you obtained it:

- **An artifact that Snowflake builds:** Snowflake publishes an SBOM for the artifact, and the driver’s documentation says where
  to find it. That SBOM describes only that artifact, on the platforms that Snowflake publishes it for.
- **A build from source:** Snowflake doesn’t publish an SBOM for a binary that it didn’t build. You generate the SBOM and keep it
  with the binary. This applies whenever you build a driver yourself, including a driver that Snowflake also publishes as an
  artifact, for example when you build it for a platform that Snowflake doesn’t publish. An SBOM that Snowflake publishes, or that
  Snowflake’s CI produces, doesn’t describe your binary.

To generate an SBOM for the native library of a build from source, use
[cargo-cyclonedx](https://github.com/CycloneDX/cyclonedx-rust-cargo) with the same features, target, and lockfile as your build:

Copy code

```
cargo install cargo-cyclonedx --version 0.5.9 --locked
cargo cyclonedx --format json --spec-version 1.5 --all --features fips \
  --manifest-path <native_crate_dir>/Cargo.toml
```

The command writes the SBOM next to the crate’s `Cargo.toml` and names it after the crate. If you cross-compile, also pass
`--target` with your target triple. Don’t use `--all-features`, which describes a different set of features from the one that you
built. An SBOM of the native library doesn’t describe the rest of the driver package, such as the dependencies of a Python
package; the driver’s documentation describes how to generate that SBOM.

An SBOM generated from the Cargo dependency graph lists `aws-lc-fips-sys` and also the standard `aws-lc-sys` crate. With
the version of the TLS library (rustls) that the core uses, the `fips` option still adds `aws-lc-sys` to the dependency graph, so
Cargo compiles both crates. The `aws-lc-sys` entry shows that the crate is part of the dependency graph, not that the binary links
it. To check which module a binary uses, use the [status call](#label-universal-core-fips-status) and the
[linkage check](#label-universal-core-fips-verify).

## Build from source with the FIPS module

If a driver’s FIPS build is a build from source, or you want to build one yourself, build the driver’s native library with the
`fips` option. The driver’s documentation describes how its packaging passes that option to the core, for example through an
installer setting or an environment variable. This section describes what the core’s build requires for any driver.

When you build from source, you’re responsible for the toolchain and build host, the resulting binary, its
[SBOM](#label-universal-core-fips-sbom), any signature, and any claim about FIPS 140-3 that you make for it. A build that you
produce doesn’t inherit anything that Snowflake states about its own artifacts.

### Source

Build from the source of a released driver version in the [Snowflake driver source repository](https://github.com/snowflakedb/drivers),
and use the lockfile (`Cargo.lock`) of that version. The lockfile pins every dependency, including the `aws-lc-fips-sys` crate and
the module that it contains.

### Build toolchain

The AWS-LC FIPS module has stricter toolchain requirements than the rest of the driver. The toolchains that Snowflake’s CI uses to
build and test FIPS builds are a working recipe, not a certified environment. For the exact versions, see the
[setup-fips-build-env](https://github.com/snowflakedb/drivers/blob/main/.github/actions/setup-fips-build-env/action.yml) action in
the driver source repository.

The following table lists the toolchains that Snowflake’s CI uses for each platform:

| Platform | Requirements | Notes |
| --- | --- | --- |
| Linux x64 | GCC 13, CMake 3, Make, Go, and Perl | Set `CC=gcc-13` and `CXX=g++-13`. GCC 14 and GCC 15 fail to build the module, and CMake 4 isn’t supported. |
| Linux ARM64 | Same as Linux x64 | Also set `CFLAGS=-fno-jump-tables` and `CXXFLAGS=-fno-jump-tables`. The build tooling of AWS-LC FIPS 3.6.0 can’t process the jump tables that GCC generates on this platform. |
| macOS (x64 and ARM64) | Apple Clang, CMake 3, Go, and Perl | None |
| Windows x64 | MSVC, CMake 3, Ninja, Go, Perl, NASM, and Clang | Set `LIBCLANG_PATH` to the directory that contains `libclang.dll`. If you use Strawberry Perl, keep its `c\bin` directory off `PATH`. |
| Windows ARM64 | Not supported | The module doesn’t build for this platform. |

Expand

Show lessSee more

All platforms also need a Rust toolchain at least as new as the `rust-version` value in `sf_core/Cargo.toml`.

### Build command

Run the following commands from the root of the driver source repository. Replace `<native_crate>` with the Cargo package that
produces the driver’s native library:

Copy code

```
export AWS_LC_FIPS_SYS_USE_SYSTEM=0
cargo build --locked --release --package <native_crate> --features fips
```

On Windows, set the environment variable with `$env:AWS_LC_FIPS_SYS_USE_SYSTEM = "0"` in PowerShell.

In these commands:

- `--features fips` is required. Without it, the build links the standard AWS-LC library.
- `--locked` makes the build fail instead of updating dependencies, so the pinned module version stays in place.
- `--all-features` isn’t a substitute for `--features fips`, because it also turns on features that are meant for testing.
- `AWS_LC_FIPS_SYS_USE_SYSTEM=0` makes the build compile the module from the source in the pinned crate. Without it, the build can
  link an AWS-LC FIPS installation that it finds through the `OPENSSL_DIR`, `OPENSSL_INCLUDE_DIR`, and `OPENSSL_LIB_DIR`
  environment variables or through pkg-config.

### Deploy the module with the driver

On Linux, the build links the module statically into the driver’s native library. On macOS and Windows, the module is built as
shared libraries whose names contain `aws_lc_fips_0_13_17`, such as `libaws_lc_fips_0_13_17_crypto.dylib` on macOS and
`aws_lc_fips_0_13_17_crypto.dll` on Windows. Deploy them with the driver’s native library, and make sure that the dynamic loader
finds that copy rather than another AWS-LC library on the system. The driver’s packaging might do this for you.

### Verify the build

1. Run the core’s FIPS tests in the same environment as your build, with `AWS_LC_FIPS_SYS_USE_SYSTEM=0` still set. The tests
   check that the linked module reports `AWS-LC FIPS 3.6.0`, that it runs in FIPS mode, and that the TLS configuration offers
   only FIPS-approved cipher suites:

   Copy code

   ```
   cargo test --locked --lib --package sf_core --no-default-features --features fips,protobuf -- tls::fips_tests
   ```

   The tests compile test-only dependencies that need OpenSSL development files. Those dependencies aren’t part of the driver
   that you deploy. On Windows, add the directory that contains the module’s DLLs to `PATH` before you run the tests.
2. Load your build in a test application and confirm that the [status call](#label-universal-core-fips-status) reports
   `is_fips` as true.
3. Check which cryptographic libraries your native library links. The driver source repository includes a script,
   `ci/fips/check_linked_crypto.py`, that fails if a native library doesn’t link the pinned FIPS module, or if it links the
   standard AWS-LC library, `ring`, or OpenSSL. The script requires Python 3.11 or later and a library built with its symbols
   kept:

   Copy code

   ```
   CARGO_PROFILE_RELEASE_STRIP=false cargo build --locked --release --package <native_crate> --features fips
   python3 ci/fips/check_linked_crypto.py <path_to_native_library>
   ```

   On Windows, the script also needs the linker map from the library’s final link. Build the library with
   `cargo rustc --locked --release --lib --package <native_crate> --features fips -- -C "link-arg=/MAP:<map_path>"`, and then run
   the script with `--linker-map <map_path>`.

   The script checks native linkage only. It doesn’t detect cryptography that runs outside the module in Rust code, such as the
   [known deviations](#label-universal-core-fips-deviations), and it doesn’t establish CMVP validation.
4. Generate the [SBOM](#label-universal-core-fips-sbom) for the binary that you deploy, and keep it with that binary.

## Build with a different AWS-LC FIPS module

If your requirements call for an AWS-LC FIPS module other than the one that the core pins, you can build the core with it in one
of the following ways. Snowflake doesn’t test builds that use a different module and doesn’t make any claim about them.
Either way, the result is a build from source: you generate its SBOM, and it doesn’t inherit anything that Snowflake states about
its own builds.

### Change the pinned crate version

The core selects the module through its pin on the `aws-lc-fips-sys` crate, and each release of that crate carries one module
version. To use another version:

1. In `sf_core/Cargo.toml`, change the `aws-lc-fips-sys` version from `=0.13.17` to the release that carries the module that you
   want.
2. In `sf_core/src/tls/mod.rs`, change `EXPECTED_FIPS_MODULE_VERSION` to the version string that the module reports, so that the
   core’s FIPS tests check your module.
3. Update the lockfile to that release:

   Copy code

   ```
   cargo update --package aws-lc-fips-sys --precise <crate_version>
   ```
4. Build and verify as described in [Build from source with the FIPS module](#label-universal-core-fips-build).

Keep the following limits in mind:

- The core limits the `aws-lc-rs` crate to versions earlier than 1.18. Versions 1.18 and later use AWS-LC FIPS 4.x, and newer
  versions of rustls require them, so moving to a 4.x module also means lifting that limit. Snowflake hasn’t evaluated that
  change.
- The crate builds the module with its own build configuration, which differs from the procedure in Section 11.1 of a module’s
  Security Policy. Pinning the release that carries AWS-LC FIPS 3.1.0 (`aws-lc-fips-sys` 0.13.11) doesn’t by itself give you a
  module that certificate #5314 or #5298 covers, and it reintroduces the
  [vulnerabilities that later versions fix](#label-universal-core-fips-module-version).

### Link an AWS-LC FIPS module that you built

The `aws-lc-fips-sys` crate can link an AWS-LC FIPS installation that you built and installed yourself, instead of building the
module from its bundled source. Choose this approach if you need to control exactly how the module is built, for example to follow
the Section 11.1 procedure of a module’s Security Policy on an operational environment that its certificate lists.

1. Build and install AWS-LC with FIPS turned on (`-DFIPS=1`). The installation needs `include/openssl/base.h` and a `lib` or
   `lib64` directory that contains `libcrypto`. The crate requires FIPS module version 3 or later.
2. Provide Rust bindings that match the installation’s `BORINGSSL_PREFIX` setting. If your AWS-LC version supports it, build
   AWS-LC with `-DGENERATE_RUST_BINDINGS=ON`. Otherwise, generate the bindings separately and set
   `AWS_LC_FIPS_SYS_SYSTEM_BINDINGS` to the path of the bindings file.
3. Set `AWS_LC_FIPS_SYS_SYSTEM_DIR` to the installation prefix, and build as described in [Build from source with the FIPS module](#label-universal-core-fips-build).
   Don’t set `AWS_LC_FIPS_SYS_USE_SYSTEM=0` for this build, because the build fails when both variables are set. The build also
   fails if the prefix doesn’t contain a usable FIPS installation of AWS-LC.
4. On macOS and Windows, where the module is a shared library, make sure that the dynamic loader finds your installation at
   runtime, for example through an rpath or a library search path.
5. Change `EXPECTED_FIPS_MODULE_VERSION` in `sf_core/src/tls/mod.rs` to the version string that your module reports, and then
   verify the build. The linkage-check script expects the symbol prefix of the bundled module, so adapt it to your installation.

For all the options that the crate supports, see the
[`aws-lc-fips-sys` 0.13.17 documentation](https://crates.io/crates/aws-lc-fips-sys/0.13.17).

## Recommendations

To get the most out of a FIPS build:

- Check the [status call](#label-universal-core-fips-status) when your application starts, and stop if `is_fips` is false.
- Keep certificate verification turned on in every environment, so that a configuration that works with a standard build also
  works with a FIPS build.
- Use private keys that are encrypted with AES-256-CBC for key pair authentication, and convert keys in the formats that a FIPS
  build rejects.
- Decide how to handle each [known deviation](#label-universal-core-fips-deviations). If your requirements don’t allow file-key
  wrapping with AES-ECB, use named internal stages with `SNOWFLAKE_SSE` encryption. If they don’t allow SigV4 signing outside the
  module, don’t run `PUT` and `GET` commands against stages in Amazon S3 from a FIPS build.
- Review the other cryptographic libraries that the driver’s packaging brings into your application’s process. The driver’s
  documentation lists them.
- Keep the SBOM that matches each binary that you deploy: the SBOM that Snowflake publishes with its artifact, or the SBOM that
  you generate for your own build.
- Track the CMVP status of AWS-LC modules, and check this page again when you upgrade the driver. A driver release can change the
  pinned module or remove a deviation.
