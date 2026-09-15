# Organization profile manifest reference

Creating organization profiles programmatically requires a manifest, written in YAML (<https://yaml.org/spec/>). Use the information provided here to learn about the parameters available in an organization profile manifest.

## Organization profile manifest

Copy code

```
#
# Organization profile manifest
#
title: <organization_profile_title>
description: <organization_profile_description>
contact: <organization_profile_contact>
approver_contact: <organization_profile_approver_contacts>
allowed_publishers:
  access:
      - account: account_name1
        roles: [<roles_list>]
      - account: account_name2
logo: <organization_profile_logo_urn>
```

## Organization profile fields

The parameters within the organization manifest allow you to create organization profiles for specific organizational listings. Required and optional fields are identified.

`title` (Required)
:   String. The organization profile title. This field represents the Provider domain. It’s shown under the Organization Listing and as a filter option under **Providers** in an Internal Marketplace.

    > Copy code
    >
    > ```
    > . . .
    > title: "Title"
    > . . .
    > ```

`description` (Required)
:   String. A description for the organization profile.

    > Copy code
    >
    > ```
    > . . .
    > description: "Description"
    > . . .
    > ```

`contact` (Required)
:   String. The email address of the organization profile owner.

    Copy code

    ```
    . . .
    contact: "contact@snowflake.com"
    . . .
    ```

`approver_contact` (Required)
:   String. The email address of the organization profile approver.

    > The following is an example of the format:
    >
    > Copy code
    >
    > ```
    > . . .
    > approver_contact: "approver_contact@snowflake.com"
    > . . .
    > ```

`allowed_publishers` (Optional)
:   The accounts that are allowed to publish the listing associated with the organization profile. You must specify the following with `allowed_publishers`:

    - `access`: A list of accounts allowed to publish the listing associated with the organization profile. To allow all accounts to publish the listing associated with the organization profile, use `all_internal_accounts: "true"`. To specify a list of roles within the current account that can access a profile, use `roles`.

      Note

      You can only assign specific roles in the current account.

    The following is an example of the format:

    Copy code

    ```
    . . .
    allowed_publishers:
      access:
        - account: "account_name1"
          roles: ['PUBLIC']
        - account: "account_name2"
    . . .
    ```

`logo` (Optional)
:   String. The URN for the organization profile icon or emoji. Use the following format to specify a logo: *logo: “urn:icon:<name>:<color>”*

    The following table lists the available icons:

    | Icon | Name | Icon | Name |
    | --- | --- | --- | --- |
    |  | ai |  | blocks |
    |  | book |  | calendar |
    |  | classification |  | code |
    |  | compute |  | dataengineering |
    |  | diamond |  | energy |
    |  | environment |  | icon\_forecasting |
    |  | gear |  | government |
    |  | healthmedicine |  | healthscience |
    |  | language |  | legal |
    |  | loudspeaker |  | machinelearning |
    |  | marketplaceinternal |  | package |
    |  | personalinfo |  | pin |
    |  | pinbuilding |  | pindata |
    |  | pinglobe |  | pinmap |
    |  | public |  | scale |
    |  | shieldlock |  | sport |
    |  | team |  | transportation |
    |  | travel |  | weather |
    |  | writinghand |  |  |

    Expand

    Show lessSee more

    Available logo colors include:

    - Default (Grey)
    - Blue
    - Violet
    - Pink
    - Orange
    - Aqua

    The following is an example of the format:

    Copy code

    ```
    . . .
    logo: "urn:icon:shieldlock:blue"
    . . .
    ```
