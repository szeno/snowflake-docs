# Cloud Agents

Cloud Agents is a capability in CoCo (Snowsight) that provides a cloud-based compute environment for each session. CoCo runs inside an isolated container, unlocking a broader set of capabilities that were previously only available in the CoCo CLI.

Note

Cloud Agents is available at no additional cost. Pricing may be introduced in a future release.

## What’s enabled

### Web search

CoCo can search the web as part of answering your questions or completing tasks.

To test: ask CoCo to “search the web for [topic]” and it will use a live web search as part of its response.

### Shell command execution

CoCo can run arbitrary shell commands inside the sandboxed container. This enables tasks like running shell scripts, installing packages, executing CLI tools, and performing system operations that are not possible in the standard browser-based experience.

### Python script execution

Full Python execution is available inside the container runtime. CoCo can run Python files, install dependencies, and execute multi-step scripts as part of agentic workflows.

## How to use it

Open CoCo in Snowsight as you normally would. Each session runs in the Cloud Agents sandbox automatically, so shell commands, Python execution, and web search are available without additional configuration.

## Security and isolation

Cloud Agents runs in an isolated container managed by Snowflake.

- **No change to existing grants.** Cloud Agents does not modify any of your Snowflake RBAC settings or open up additional SQL access.
- **Isolated execution.** Each session runs in its own container.
- **Outbound network is restricted, not disabled.** HTTPS egress is limited to a fixed allowlist of package managers and related build tooling. For the full list, see [Allowed package manager egress](#label-cloud-agents-allowed-package-manager-egress). Hosts outside that allowlist are not reachable from the sandbox. [External access integrations](/developer-guide/external-network-access/external-network-access-overview) are not currently supported for Cloud Agents.

### Allowed package manager egress

By default, the Cloud Agents sandbox can reach the following package managers and related hosts over HTTPS so you can install dependencies and build tooling inside the container. Access to these hosts is read-only (GET and HEAD only), so package installs and downloads work, but publish and other write operations are blocked:

| Ecosystem | What’s allowed |
| --- | --- |
| Python | PyPI |
| JavaScript | npm, Yarn, and the Node.js distribution server |
| Ruby | RubyGems and RVM |
| Rust | crates.io and rustup |
| Go | The Go module proxy, checksum database, and related Go hosts |
| JVM | Maven, Gradle, Kotlin, and Spring |
| Other language registries | Packagist, NuGet, Pub, Hex, CPAN, Hackage, CocoaPods, and Swift |
| OS packages | Debian, Ubuntu, and Alpine package mirrors |

Expand

Show lessSee more

Anything outside Snowflake and this allowlist, including arbitrary websites or private registries, isn’t reachable from the sandbox.

## Disable non-Snowflake egress (account administrators)

By default, Cloud Agents allows HTTPS egress to the package manager allowlist. Account administrators can block all non-Snowflake egress from the sandbox for the entire account by setting the [COCO\_CLOUD\_AGENTS\_NON\_SNOWFLAKE\_EGRESS\_DISABLED](/sql-reference/parameters#label-coco-cloud-agents-non-snowflake-egress-disabled) account parameter to `TRUE`:

Copy code

```
ALTER ACCOUNT SET COCO_CLOUD_AGENTS_NON_SNOWFLAKE_EGRESS_DISABLED = TRUE;
```

Only ACCOUNTADMIN can change this parameter. The default is `FALSE` (non-Snowflake egress to the package manager allowlist is allowed). When set to `TRUE`, the sandbox cannot reach hosts outside Snowflake, including package registries.

## Current scope

This release focuses on three capabilities: web search, shell command execution, and Python script execution.

Not yet included:

- Multi-agent (parallel agent) execution
- Persistent filesystem across sessions (session-scoped today)
- Full CLI tool parity (grep, glob, and other tools are being validated)

## Availability

- Generally available in all commercial regions on AWS, Azure, and Google Cloud.
- Not available in government, FedRAMP, DoD, VPS, or China deployments.
