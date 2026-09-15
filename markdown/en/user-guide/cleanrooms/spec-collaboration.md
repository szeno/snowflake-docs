# Collaboration specification

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Defines the high-level collaboration, which is visible to all collaborators. The specification defines which analysis runners are invited, and for each analysis runner, which
data and templates they can access and run. Any templates or data offerings that are listed here must be registered before they’re included
in the collaboration specification.

The owner submits this specification by calling INITIALIZE.

After a collaboration is created, the owner can request to edit it in place by submitting an updated version of this specification by calling
[EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a
[preview feature](/release-notes/preview-features)).

**Schema:**

Copy code

```
api_version: 2.0.0              # Required: Must be "2.0.0"
spec_type: collaboration        # Required: Must be "collaboration"
name: <collaboration_name>      # Required: Unique name (max 75 chars)
description: <collaboration_description>  # Optional: Description (max 1,000 chars)
owner: <owner_alias>            # Required: Alias of owner

collaborator_identifier_aliases:  # Required: Map aliases to account identifiers
  <alias_1>: <account_identifier_1>  # One or more alias mappings...

analysis_runners:               # Required: Who can run analyses
  <analysis_runner_alias>:      # One or more analysis runner definitions...
    data_providers:             # Required: Data providers for this runner
      <provider_alias>:         # One or more provider definitions...
        data_offerings:         # Required: List of offerings (can be empty [])
          - id: <data_offering_id>  # Zero or more data offering IDs...
    templates:                  # Optional: Templates this runner can use
      - id: <template_id>       # One or more template IDs...
    activation_destinations:    # Optional: Where results can be sent
      snowflake_collaborators:  # Optional: Collaborators who can receive results
        - <collaborator_alias>  # One or more collaborator aliases...
```

`api_version`
:   The version of the Collaboration API used. Must be `2.0.0`.

`spec_type`
:   Specification type identifier. Must be `collaboration`.

`name: collaboration_name`
:   User-friendly name for this collaboration. Must be unique in the creator’s account and follow
    [Snowflake identifier rules](/sql-reference/identifiers-syntax) (maximum 75 characters).

`description: collaboration_description` (*Optional*)
:   A human-readable description of the collaboration (maximum 1,000 characters), for collaborators to read.

`owner: owner_alias`
:   Alias of the collaboration owner, as defined in `collaborator_identifier_aliases`.

`collaborator_identifier_aliases`
:   A mapping of collaborator aliases to their [Data Sharing Account Identifiers](/user-guide/admin-account-identifier#label-account-name-data-sharing). Only users listed
    here can participate in the collaboration. Use the aliases defined here to refer to all collaborators, rather than using their data
    sharing account identifier directly. Must be unique in this collaboration and follow [Snowflake identifier rules](/sql-reference/identifiers-syntax) (maximum 25 characters).

`analysis_runners`
:   Describes who can run an analysis in this collaboration. Each analysis runner is keyed by a unique alias. You must allow at least one
    account to run an analysis in this collaboration.

    `<analysis_runner_alias>`
    :   Alias of account that can run an analysis in this collaboration. Alias is defined in the `collaborator_identifier_aliases` list.

    `data_providers`
    :   Data providers whose data this analysis runner can access. Each provider is keyed by the alias that is defined in
        `collaborator_identifier_aliases`.

        `data_offerings`
        :   A list of data offerings from this data provider that the analysis runner can access, or an empty array `[]` as a placeholder so
            that data offerings can be added later. Each data offering is referenced by its ID, generated when the data provider calls
            REGISTER\_DATA\_OFFERING.

    `templates` (*Optional*)
    :   The templates that can be used by this analysis runner. Each template is referenced by its ID. You can omit this in the initial spec,
        and still share templates with this analysis runner after the collaboration is created.

    `activation_destinations` (*Optional*)
    :   Defines activation settings for the analysis results.

        `snowflake_collaborators` (*Optional*)
        :   List of collaborators who can receive activated analysis results. Use the alias from the `collaborator_identifier_aliases` list in
            this spec. All collaborators listed here must have the permissions described in [Implementing activation](/user-guide/cleanrooms/activation#label-dcr-collaboration-activating-results).

## Examples

Copy code

```
api_version: 2.0.0
spec_type: collaboration
name: my_sample_collaboration
owner: Owner
collaborator_identifier_aliases:
  Owner: ENG.OWNER
  AnalysisRunner_1: ENG.CONSUMER_1
  DataProvider_1: ENG.PROVIDER_1
  DataProvider_2: ENG.PROVIDER_2
  AnalysisRunner_2: ENG.PROVIDER_3
analysis_runners:
  AnalysisRunner_1:
    data_providers:
      DataProvider_1:
        data_offerings:
        - id: DCR_PREPROD_CI_PROVIDER_ANY_NAME_ZUDFTMULHQ_iuDfn_v0
      DataProvider_2:
        data_offerings: []
    templates:
    - id: test_sca_three_party_template_JOaVG_v0
  AnalysisRunner_2:
    data_providers:
      DataProvider_2:
        data_offerings: []
    templates:
    - id: test_sca_three_party_template_JOaVG_v0
```
