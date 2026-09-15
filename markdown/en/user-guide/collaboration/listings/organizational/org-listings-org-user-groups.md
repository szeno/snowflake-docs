# Use organization user groups with organizational listings

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Providers can use [organization user groups](/user-guide/organization-users#label-org-users-groups) to assign consumers to organizational listings. For example, an organization account can create a marketing organization user group, and then providers can assign specific consumers to organization listings that are specific to the marketing team. With this functionality, the provider no longer needs to assign individual consumers to specific organizational listings. To identify the organization user group to associate for an organizational listing, the provider modifies the following fields in the listing manifest:

Copy code

```
organization_targets:
  access:
    - account: <account_name>
    - organization_user_group: <organization_user_group_1>
    - organization_user_group: <organization_user_group_2>
    - account: <account_name>
      roles: [<roles_list>]
```

To create an organizational listing programmatically, select the **SQL** tab in [Create an organizational listing](/user-guide/collaboration/listings/organizational/org-listing-create).

For more information about the listing manifest, see [Listing manifest reference](/progaccess/listing-manifest-reference).

To allow consumers to access their assigned organizational listings, the consumers must import the organization user group.

Note

You can make an organizational listing discoverable or accessible to an organization user group. Making an organizational listing discoverable or accessible to all accounts makes it discoverable or accessible to the organization user group as well. For this reason, you don’t need to add the organization user group to the listing manifest when making a listing discoverable or accessible to all accounts.
