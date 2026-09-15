# Overview of Snowflake Data Clean Rooms

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

This topic provides a high-level guide to the components that make up a collaboration, and outlines the basic steps in creating or using a Snowflake Data Clean Room collaboration.

## Requirements

- You must be [updated to the latest version of Snowflake Data Clean Rooms](/user-guide/cleanrooms/managing-updates#label-dcr-updating-cleanrooms-environment-main).
- You need access to the Data Clean Rooms Collaboration API to see or manage collaborations. For more information, see [Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access).
- Data Providers must use Snowflake Enterprise Edition. Owners and Analysis runners can use Standard Edition.
- If you use Snowflake Standard Edition, you cannot share data through a data clean room with policy enforcement. However, you can access data offerings from other collaborators, or [use your own data](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-using-local-data) without applying policies or sharing the data.
- To [activate results](/user-guide/cleanrooms/activation) to another Snowflake account, you must use Snowflake Enterprise Edition.
- Trial accounts don’t support Snowflake Data Clean Rooms.

## Roles and resources in a collaboration

To understand how to use a collaboration, you must first understand collaboration roles and collaboration resources.

### Collaboration roles

The following roles are available in a collaboration. These roles define the high-level capabilities of the collaborator.

- **Owner:** The owner defines, creates, and owns the collaboration, and defines which collaborators are invited and their collaboration
  roles. An owner isn’t automatically an analysis runner or a data provider, and doesn’t have any elevated run privileges. The owner’s
  main abilities are to create the clean room, assign collaboration roles, determine who can share data with whom, and tear down the
  clean room. A collaboration can have only one owner.
- **Data provider:** Provides data offerings, such as tables and views, to a collaboration, and specifies which analysis runners can
  use them. That is, account A is a data provider to accounts B and C, as specified in the collaboration specification.
- **Analysis runner:** Runs permitted templates on permitted data offerings, as specified by the collaboration specification.

These roles are designated in the collaboration specification that is used to create the collaboration.

A collaborator can be assigned multiple collaboration roles, and (except for the owner role) a collaboration role can be assigned to
multiple collaborators.

Learn more

- [Learn more about roles](/user-guide/cleanrooms/roles)

### Collaboration resources

A collaboration contains resources, including data offerings, templates, and code specs. All resources, and the collaboration itself, are defined by YAML specifications.

Collaborations support the following types of resources:

- **Template:** A JinjaSQL query that analysis runners can execute in the collaboration. Depending on the type of template, results can
  either be delivered directly, or *activated* (saved) to the Snowflake account of a designated collaborator. Analysis runners can pass
  values into a template at run time to replace template variables used for column names, WHERE clauses, and other query elements.
- **Data offering:** A package of one or more tables shared by a data provider with specific analysis runners. A data offering is a live
  view of the source data, not a snapshot, and its specification controls which columns are exposed and what policies apply.
- **Code spec:** A set of custom Python functions or procedures that can be called by a template. Code specs let you extend template
  capabilities with user-defined logic such as machine learning models or custom transformations.

Learn more

- [Collaboration resources](/user-guide/cleanrooms/resources)
- [Collaboration resource schemas](/user-guide/cleanrooms/spec-reference)
- [Design custom templates](/user-guide/cleanrooms/custom-templates)
- [Code specs](/user-guide/cleanrooms/resources-code-specs)

### Example clean room specification

Here is the YAML specification for a basic clean room that involves two participants, `alice` (an alias for account `corp1.acct123`),
and `bob` (an alias for account `corp2.acctxyz`). The specification assigns roles to each user and links two data offerings into the
collaboration.

Copy code

```
api_version: 2.0.0
spec_type: collaboration
name: basic_collaboration
owner: alice                # alice is the collaboration owner.
collaborator_identifier_aliases:
  alice: corp1.acct123
  bob: corp2.acctxyz
analysis_runners:
  alice:                    # alice is also an analysis runner.
    data_providers:
      alice:                # alice provides data to herself.
        data_offerings:     # alice provides these data offerings.
        - id: alice_data_1
        - id: alice_data_2
      bob:                  # bob provides data to alice.
        data_offerings:     # bob provides this data to alice.
        - id: bob_data_1
    templates:              # alice can use this template with any data she can access.
    - id: template1
  bob:                      # bob is an analysis runner
    data_providers:         # bob can use data from the following data providers.
      alice:
        data_offerings:     # alice provides the following data to bob.
        - id: alice_data_1
    templates:              # bob can use this template with any data he can access.
    - id: template2
```

This simple collaboration includes the following resources and collaboration roles:

- `alice` is the collaboration owner, an analysis runner, and a data provider for herself and `bob`.
- `bob` is an analysis runner, and a data provider for `alice`, but *not* for himself.
- `alice` can run `template1`, `bob` can run `template2`.

Other things to note about this collaboration:

- Both `alice` and `bob` can add new templates, and share them with any other collaborators.
- Any data provider can add or remove data offerings in their data offerings list, even after the collaboration is created.
- The owner can request to add or remove collaborators and change collaborator roles after the collaboration is created by calling [EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a [preview feature](/release-notes/preview-features)); these changes require approval from the affected collaborators. For example, the owner could later request to make `bob` a data provider to himself.

## Basic clean room collaboration workflow

Here is a simple clean room collaboration scenario:

1. The collaboration owner optionally registers any templates or data offerings that they want to appear in the initial configuration of
   the collaboration.
2. The owner optionally asks any intended collaborators to register any templates or data offerings that they want to appear in the initial
   configuration of the collaboration. Collaborators then give the resource IDs of any items that they registered.
3. The owner then creates a collaboration. The collaboration specification defines the collaborators, their roles, and any resources that
   should be available in the initial state of the collaboration.

   - If the collaboration includes collaborators in other cloud hosting regions, they must
     [enable Cross-Cloud Auto-Fulfillment on their account](/user-guide/cleanrooms/laf#label-dcr-collab-enabling-laf) before they can review and join the
     collaboration.
   - When the collaboration is created, it will become visible and joinable by all collaborators in the collaboration spec.
4. Collaborators review and join the collaboration.
5. Collaborators can then optionally [link resources into the collaboration](#label-dcr-collaboration-add-resources),
   as appropriate for their roles. Data providers can link data offerings to their analysis runners; any role can request to add a
   template and share it with any other collaborator.
6. Analysis runners can then run any templates shared with them in the collaboration, using any data offerings shared with them in the
   collaboration. The analysis runner bears the cost of the analysis. Templates can either return query results in the response or
   [activate results to the caller or another collaborator](/user-guide/cleanrooms/activation#label-dcr-collaboration-activating-results).
7. The owner can later request to add or remove collaborators and change collaborator roles by calling [EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a [preview feature](/release-notes/preview-features)), subject to approval from the affected collaborators.

Learn more

- [See how to implement a basic two-party collaboration, with end-to-end code.](/user-guide/cleanrooms/tutorials/collaboration-basic-api-tutorial)
- See additional examples in the **Use cases** section of the Data Clean Rooms documentation.

### Creating a collaboration

Any Snowflake Data Clean Rooms user with appropriate privileges can create a clean room. A clean room is defined using a YAML specification
that determines all the collaborators and their relative roles in the collaboration, as well as any resources present in the initial
configuration of the collaboration. (The resource owners must join before the resources can be used.) Resources can be added or removed
after the collaboration is created. The owner can also request to add or remove collaborators and change collaborator roles after the
collaboration is created by calling [EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a
[preview feature](/release-notes/preview-features)); these changes require approval from the affected collaborators.

Collaborations aren’t versioned: a collaboration can change with the addition or removal of resources, but those changes aren’t tracked.

Learn more

- [Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access)
- [Collaboration specification](/user-guide/cleanrooms/spec-collaboration)

### Adding resources to a collaboration

A collaboration can access resources, including templates, data offerings, and code specs. To use a resource in a collaboration, you must
first *register* it with the collaboration clean rooms environment, then *link* it into a specific collaboration:

- *Registration* is an account-level action; it packages and copies the resource into the clean rooms environment, and returns an ID that
  is used to reference that resource. A resource is registered in a registry, either the default registry for your account, or a custom
  registry that someone in your account created. The default registry is available to any collaborator in the account with READ REGISTRY
  privileges; a custom registry can be access-controlled by the registry creator.
- *Linking* shares a registered resource with a specific collaboration. More specifically, it shares a registered resource with a specific
  set of collaborators in a specific collaboration. You can link a resource either by adding it to the collaboration specification used to
  create a collaboration, or you can call the appropriate Collaboration API procedure to link the resource into a collaboration.

Resources can be added to a collaboration at creation time or after a collaboration is created.

Unlike collaborations, resources are versioned. Newer versions of a resource don’t overwrite older versions. If you want to replace a
resource with a newer version, you must also update the collaboration to remove the old version (if you choose) and add the new version.

The account that registers a resource must be a collaborator, and must join the collaboration before any resources they registered can be
available in the collaboration.

Learn more

- [Learn more about registries.](/user-guide/cleanrooms/registries)
- [Learn more about adding resources to your collaboration.](/user-guide/cleanrooms/resources)

### Joining a collaboration

A collaboration is visible to all collaborators listed in the collaboration specification. All collaborators, including the owner, must join
the collaboration. All collaborators except for the owner must review the collaboration before they can join. Reviewing a collaboration
exposes the collaboration specification to the invited party. After reviewing the collaboration, the invitee can then join the
collaboration. You must join a collaboration before any resources that you provide to a collaboration become usable.

You can see your join status (invited, joining, joined) by calling GET\_STATUS on the collaboration. Most collaboration mutation actions,
such as linking a resource, joining a collaboration, or activating results, are either asynchronous, or might take some time to propagate
to other collaborators, so you should call the appropriate procedure to see the state of the change.

### Running an analysis

Collaborators listed as analysis runners in a collaboration can run queries on any data offerings available to them in the collaboration.

Collaborations support the following types of analyses:

- Templated analysis queries: An analysis runner can run any templates assigned to them in the collaboration, and see results synchronously.
- Activation analyses: If the data offering, collaboration, and template allow it, the analysis runner can *activate* (save) results to a
  designated collaborator’s Snowflake account.
- Free-form SQL analyses: If the collaboration and data offering allow it, analysis runners can run SQL queries directly against a data
  offering’s data. See [Free-form SQL queries](/user-guide/cleanrooms/free-form-sql).

Learn more

- [Activating query results](/user-guide/cleanrooms/activation)
- [Free-form SQL queries](/user-guide/cleanrooms/free-form-sql)

### Editing a collaboration

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The collaboration owner can request to edit an existing collaboration in place, instead of tearing it down and recreating it. To edit a
collaboration, the owner submits an updated version of the collaboration specification in the
[EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) procedure. EDIT can add or remove
collaborators, change collaborator roles, share or remove already-registered templates, and link or unlink already-linked data offerings for
analysis runners. Edits are applied as a single update request that all affected collaborators must approve before the changes take effect.

Learn more

- [EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference)

### Leave or delete a collaboration

You can leave a collaboration at any time, although the collaboration owner can’t leave a collaboration, and instead deletes the
collaboration for everyone.

- Non-owners leave a collaboration by calling LEAVE. Any data offerings they have provided will be removed from the
  collaboration. You can’t rejoin a collaboration after leaving it.
- Collaboration owners can’t leave a collaboration: ownership can’t be transferred. A collaboration owner can drop a collaboration for all
  collaborators by calling TEARDOWN.

Leaving or deleting a collaboration is asynchronous. You must call GET\_STATUS to monitor the status, and call LEAVE or TEARDOWN again when GET\_STATUS shows the status as LOCAL\_DROP\_PENDING.

Deleting a collaboration doesn’t affect the registration status of any resources linked into the collaboration. Those resources can
continue to be used or linked into new collaborations.
