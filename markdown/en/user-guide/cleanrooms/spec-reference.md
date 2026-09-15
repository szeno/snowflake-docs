# Data Clean Rooms Schema Reference

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

This topic describes the specification schema for all collaboration resources. Specifications are shown in YAML format.

Specifications have a schema version field `api_version`. Use the API version number shown here; support for earlier schema versions
isn’t guaranteed.

**Current DCR Collaboration API version:** 2.0.0

## Resource specifications

- [Collaboration specification](/user-guide/cleanrooms/spec-collaboration): Defines the high-level collaboration, including which
  analysis runners are invited, and for each runner, which data and templates they can access.
- [Data offering specification](/user-guide/cleanrooms/spec-data-offering): Defines a set of tables that a data provider shares with
  analysis runners, including sharing rules, policies, column formats, and analysis types.
- [Template specification](/user-guide/cleanrooms/spec-template): Defines a single template in a collaboration, including
  parameters, code specs, and the JinjaSQL template content.
- [Analysis specification](/user-guide/cleanrooms/spec-analysis): Specifies the information that analysis runners need to
  run an analysis, including which template, tables, and variable values to use.
- [Code specification](/user-guide/cleanrooms/spec-code-spec): Defines one or more code functions or procedures
  that can be called by a template.
