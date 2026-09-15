# Resources

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview of collaboration resources

Collaborators can add various resources to a Snowflake Data Clean Room collaboration. Resources include templates, data offerings, and code specs.

Resources are available only to the collaborators designated by a collaboration specification.

Resources support versioning; however, creating a new resource with a new version doesn’t remove the previous version from the collaboration. Resources are uniquely named by combining the user-provided name and version (and alias, for data offerings).

Adding a resource to a collaboration is a two-part process:

1. **Register the resource in the account.** This makes it available to be linked into multiple collaborations. Resources are registered in either the default registry for the account, or in a custom registry. Learn more about [Registries](/user-guide/cleanrooms/registries).
2. **Link the resource into a specific collaboration.** After a resource is linked, it can be seen and used by the designated collaborators
   in the collaboration. You must have read access to the registry and update privilege on the collaboration to be able to link a resource from that registry into the collaboration.

Important

If you share data with users in other cloud hosting regions, the sharer must [enable Cross-Cloud Auto-Fulfillment on their account](/user-guide/cleanrooms/laf#label-dcr-collab-enabling-laf).

You can link the following resource types into a collaboration:

- [Templates](/user-guide/cleanrooms/resources-templates)
- [Data offerings](/user-guide/cleanrooms/resources-data-offerings)
- [Code specs](/user-guide/cleanrooms/resources-code-specs)

Use [registries](/user-guide/cleanrooms/registries) to group and manage access to your resources, and [naming paths](/user-guide/cleanrooms/resources-data-offerings#label-dcr-organizing-data-offerings) to organize your data offerings.
