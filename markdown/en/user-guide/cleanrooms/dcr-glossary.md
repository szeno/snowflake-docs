# Glossary of Snowflake Data Clean Room terms

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Get to know these terms as they are used in Snowflake Data Clean Rooms. Some terms are used differently here than
in the rest of Snowflake.

Activate / activation
:   Exporting the results table of a query out of the clean room, either to a collaborator or to a third party. If
    allowed by the other party and the clean room settings, you can export query results to your own account or to an
    approved third-party partner, such as Google Ads or Meta Ads Manager.

Analysis runner
:   A [collaboration role](/user-guide/cleanrooms/roles) that allows a collaborator to run templates and view
    results in a collaboration. An analysis runner can use data offerings shared with them by data providers.

Code spec
:   A registered package of one or more custom Python functions or procedures that can be called by a template. Code
    specs are defined using a YAML code specification and registered by calling `REGISTRY.REGISTER_CODE_SPEC`. A
    template references a code spec by its ID, and the template calls functions using the syntax
    `cleanroom.code_spec_name$function_name`.

Collaboration
:   A secure multi-party data sharing environment. A collaboration is defined by a YAML specification that lists the
    collaborators, their collaboration roles, and all resources (templates, data offerings, and so on) available in the
    collaboration. The collaboration owner creates the collaboration by calling INITIALIZE, and other collaborators
    join by calling JOIN.

Collaboration owner
:   A [collaboration role](/user-guide/cleanrooms/roles) assigned to the collaborator who creates a
    collaboration by calling INITIALIZE. The owner defines the collaboration spec, including the list of
    collaborators, their roles, and the initial set of resources. Owners can’t act as analysis runners or
    data providers by default unless the collaboration specification grants them those roles explicitly.

Collaboration role
:   A role that describes the set of actions that a user can perform in a given collaboration. One user can have many
    collaboration roles in a collaboration. Roles include owner, data provider, and analysis runner. Not the same as an
    RBAC role. Learn more about roles at [Collaborator roles in Collaboration Data Clean Rooms](/user-guide/cleanrooms/roles).

Collaborator
:   Any participant in a collaboration. Each collaborator is identified by an alias and has one or more collaboration
    roles (owner, data provider, analysis runner).

Column policy
:   Specified by a collaborator to indicate which of their data columns can be projected by other collaborators. A
    clean room column policy is determined entirely within a clean room, and isn’t derived from any Snowflake policies
    that might be applied to the source table outside of the clean room.
    [Learn more about column policies.](/user-guide/cleanrooms/v1/policies#label-dcr-column-policies)

Data offering
:   A package of one or more datasets that a data provider shares with specific analysis runners in a collaboration.
    Each dataset represents one source table or view owned by the data provider. A data offering is a live view of the
    data, not a snapshot, so any changes to the source data are reflected in the collaboration. Data offerings are
    registered in a registry and then linked into a collaboration.

Data provider
:   A [collaboration role](/user-guide/cleanrooms/roles) that allows a collaborator to share data offerings with
    specific analysis runners in a collaboration. A data provider registers and links data offerings into the
    collaboration for other collaborators to use.

Dataset
:   A secure view of a single source table or view from a data provider. A data offering consists of one or more
    datasets. The data offering specification defines which columns to expose, what policies to apply, and whether the
    data can be queried by template only or also by free-form SQL for each dataset.

DCR privilege
:   A conceptual permission string used to grant access to specific Collaboration API procedures to a role. DCR
    privileges can be granted for individual objects or more general actions. DCR privileges include READ, CREATE
    COLLABORATION, and JOIN COLLABORATION. These privilege strings are passed into
    [GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE](/user-guide/cleanrooms/collaboration-api-reference#label-grant-privilege-on-object-to-role) and
    [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-grant-privilege-on-account-to-role). To learn more, see
    [Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access).

Free-form SQL
:   A mode of data access where an analysis runner can run arbitrary SQL queries directly against a data provider’s
    dataset, without using a template. The data provider enables this by setting `allowed_analyses: template_and_freeform_sql`
    in their data offering specification. Snowflake policies defined in the `freeform_sql_policies` section of the
    data offering are enforced on these queries. See [Free-form SQL queries](/user-guide/cleanrooms/free-form-sql).

Differential privacy
:   An algorithmic and mathematical system that adds protection to individual rows or entities in a dataset by adding
    noise to numerical results and requiring grouping in queries to prevent exact values from being associated with
    exact rows or entities in the data.

Join policy
:   A policy set by a clean room collaborator that specifies which of their columns can be joined on in queries
    in that clean room. A clean room join policy is entirely independent of Snowflake join policies.
    [Learn more about join policies.](/user-guide/cleanrooms/v1/policies#label-dcr-join-policies)

Linking
:   Importing a resource into a collaboration. See [Resources](/user-guide/cleanrooms/resources).

Local data offering
:   Local data offerings let standard edition accounts use their own tables in a collaboration. These offerings are not visible to any other collaborator, and template policies are not enforced. See [Run an analysis with your own data when you use Standard Edition](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-using-local-data).

Linking
:   Importing a protected view of data into a clean room. The provider and consumer can both link their own data into
    a clean room to make it available to any queries supported by that clean room. Linking a table or view means
    creating a copy (a view) of the source data within the clean room, dynamically linked to the source table or view
    outside of the clean room.

Registry
:   An account-level container that stores resources such as templates, data offerings, and code specs. You must
    register a resource in a registry before you can link it to a collaboration. Each account has a default registry
    that all users can access, and you can create custom registries to group and manage access to resources. Custom
    registries are private to the creator until access is explicitly granted to other roles. Learn more at
    [Registries](/user-guide/cleanrooms/registries).

Resource
:   A reusable component that can be registered in a registry and linked into a collaboration. Resources include
    templates, data offerings, and code specs. Each resource is defined by a YAML specification, has a name and
    version, and is registered by calling the appropriate REGISTRY procedure. Resources can be linked into a
    collaboration at creation time or added later.

SCO
:   *Secure Collaboration Orchestrator.* A Snowflake-managed account that manages a collaboration behind the scenes.
    The SCO creates an individual app package per collaboration, shares data with collaborators according to the
    collaboration definition, and enforces collaboration policies such as who can access which data using which
    templates. Costs associated with the SCO aren’t charged to users.

Secure view
:   When you link a table or view into the clean room, a secure view is created. This is an encrypted view based on
    the source table or view outside the clean room. The secure view is generally invisible to you, but might
    sometimes appear in an error message or when you are browsing the database objects using various tools, where you
    will see some name mangling of the original linked dataset. Unless directed otherwise, always refer to your data
    using the dataset name, which is identical to the linked source table or view.

Spec / specification / definition
:   A YAML document that defines a collaboration resource. Each resource type has its own specification schema,
    including collaboration specifications, data offering specifications, template specifications, analysis request
    specifications, and code specifications. Specifications are passed to API procedures such as
    INITIALIZE, REGISTER\_DATA\_OFFERING, and REGISTER\_TEMPLATE. See the
    [schema reference](/user-guide/cleanrooms/spec-reference) for details.

Template
:   Each clean room has one or more templates, which are SQL queries written in JinjaSQL, provided by collaborators.
    The template provider specifies which analysis runners can use their templates. Depending on how they are written, a
    template can either be an analysis template, which returns results immediately, or an activation template, which saves results into the
    Snowflake account of the designated collaborator.

## Legacy Provider & Consumer Clean Room Terms

The following terms are used in Legacy Provider & Consumer Clean Rooms. For current terminology, see the
definitions above.

Provider
:   A clean room creator. The provider typically shares some data and the list of permitted queries that can be run
    in that clean room, and sets high-level clean room configurations.

Consumer
:   A person or account invited to use a clean room by the clean room provider. Consumers typically import their own
    data and run one or more queries supported by that clean room. However, a clean room can be configured to allow
    consumers to propose their own query, subject to approval by the provider.

Clean rooms UI
:   Or “UI” for short. The browser-based web application you can use to manage the Snowflake Clean Room environment,
    create new clean rooms, or use clean rooms to which you have been invited. This used to be called the “web app,”
    and you might still see that terminology used in some places.
