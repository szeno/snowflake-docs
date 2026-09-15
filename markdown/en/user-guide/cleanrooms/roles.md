# Collaborator roles in Collaboration Data Clean Rooms

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview of collaboration roles

Collaborators have one or more of the following *collaboration roles* in a clean room collaboration scenario. In this case,
a *collaboration role* is a set of capabilities, not an [RBAC role](/user-guide/cleanrooms/manage-access):

- **Owner:** The owner defines, creates, and owns the collaboration, and defines which collaborators are invited and their collaboration
  roles. An owner isn’t automatically an analysis runner or a data provider, and doesn’t have any elevated run privileges. The owner’s
  main abilities are to create the clean room, assign collaboration roles, determine who can share data with whom, and tear down the
  clean room. A collaboration can have only one owner.
- **Data provider:** Provides data offerings, such as tables and views, to a collaboration, and specifies which analysis runners can
  use them. That is, account A is a data provider to accounts B and C, as specified in the collaboration specification.
- **Analysis runner:** Runs permitted templates on permitted data offerings, as specified by the collaboration specification.
  An analysis runner isn’t a data provider to themselves by default, unless specified in the collaboration specification.

One collaborator can have multiple collaboration roles in a collaboration, and multiple collaborators can have the same collaboration
role (except for the owner collaboration role, which is assigned to only one user). For example, the owner of a collaboration can
also be a data provider and an analysis runner.

The owner specifies the initial collaborators and their collaboration roles when they create the collaboration. After the collaboration is
created, the owner can request to add or remove collaborators and change collaborator roles by calling
[EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a
[preview feature](/release-notes/preview-features)); these changes take effect only after the affected collaborators approve them. For
example, the owner can request to add a new analysis runner, add a data provider for an existing analysis runner, or update a data provider
to an analysis runner. The owner collaboration role itself can’t be changed or transferred to another collaborator.

In addition, collaborators can link or remove [resources](/user-guide/cleanrooms/resources) after a collaboration is created.

## See your role

Call `GET_STATUS` to see your roles in a collaboration in the ROLES column:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);
```

If you want to see more details about your roles, for example, if you’re a data
provider and want to see whom you can share data with, you must examine the spec.
Here is how to see the collaboration spec in a single call after you have joined a collaboration:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS() ->>
  SELECT "COLLABORATION_SPEC" FROM $1
    WHERE "SOURCE_NAME" = $collaboration_name;
```

## Example

The following example shows a very basic collaboration that defines collaboration roles, but doesn’t include any resources.
You can create a collaboration with or without resources, and add or remove them later.

Copy code

```
api_version: 2.0.0
spec_type: collaboration
name: basic_collaboration
owner: alice
collaborator_identifier_aliases:
  alice: corp1.acct123
  bob: corp2.acctxyz
analysis_runners:
  alice:
    data_providers:
      alice:
        data_offerings: []
      bob:
        data_offerings: []
  bob:
    data_providers:
      alice:
        data_offerings: []
```

The previous collaboration defines the following collaborators and collaboration roles:

- `alice` is the collaboration owner, an analysis runner, and a data provider for `bob` and herself. `alice` is the alias
  defined in the collaboration for account `corp1.acct123`.
- `bob` is an analysis runner, and a data provider for `alice` but *not* for himself. `bob` is the alias defined in the
  collaboration for account `corp2.acctxyz`.

After the collaboration is created, the owner can request to add or remove collaborators and change collaboration roles by calling [EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a [preview feature](/release-notes/preview-features)), subject to approval from the affected collaborators.

Data providers can link data offerings after a collaboration is created. Any collaborator can request to add templates after a collaboration
is created. The following example shows how you can use the Collaboration API to link resources into the previous collaboration after
it’s created:

Copy code

```
api_version: 2.0.0
spec_type: collaboration
name: basic_collaboration
owner: alice
collaborator_identifier_aliases:
  alice: corp1.acct123
  bob: corp2.acctxyz
analysis_runners:
  alice:
    data_providers:
      alice:
        data_offerings:
        - id: alice_data_1
        - id: alice_data_2
      bob:
        data_offerings:
        - id: bob_data_1
    templates:
    - id: template1  # Alice can run template1 using alice_data_1, alice_data_2, or bob_data_1.
  bob:
    data_providers:
      alice:
        data_offerings:
        - id: alice_data_1
    templates:
    - id: template2  # Bob can run template2 using data from alice_data_1, provided by alice.
```

The modified collaboration now supports the following resources and capabilities:

- `alice` can run analyses using `template1` with data from `alice_data_1`, `alice_data_2`, and `bob_data_1`.
- `bob` can run `template2` using data from `alice_data_1`.
