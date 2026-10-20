# Sharing Streamlit in Snowflake apps

Feature — Generally Available

Not supported in government regions.

This topic covers how to share Streamlit in Snowflake apps with roles and individual users, and the URLs for sharing apps
with or without the Snowsight interface.

To render an app inside an external web page rather than share a link to it, see
[Embedding Streamlit in Snowflake apps in external pages](/developer-guide/streamlit/features/embedding/overview).

## App URLs

Each Streamlit in Snowflake app has two URLs: app-builder URLs that show the Snowsight elements and
app-viewer URLs that hide them. This allows you to share view-only links with business users.

By default, sharing an app using the app-viewer URL lets end users change the URL to access other parts of Snowflake.
To enforce restricted access to only app-viewer URLs, an administrator must configure the ALLOWED\_INTERFACES user
property. For more information, see [Limit a user’s access to only Streamlit in Snowflake](/developer-guide/streamlit/object-management/security#label-limit-access-streamlit-only).

An administrator can also configure app-viewer URLs to redirect to your organization’s identity provider (IdP).
For more information, see [Essential security setup](/developer-guide/streamlit/object-management/security#label-streamlit-essential-security-setup).

### App-builder URLs

When you view an app from its app-builder URL, an object toolbar appears at the top of the app. The left side of the toolbar displays the
app’s name. The right side of the toolbar displays the app’s status. Additionally, if you have the necessary privileges to edit
the app, the toolbar contains an **Edit** button. If you have the necessary permission to share the app with other roles and users, the
toolbar contains a **Share** button.

If you select any app from the Streamlit Apps page in Snowsight, a new tab opens to its app-builder URL. This URL has the following
format:

Copy code

```
https://app.snowflake.com/<organization_name>/<account_name>/#/streamlit-apps/<app_database>.<app_schema>.<app_name>
```

### App-viewer URLs

When you view an app from its app-viewer URL, the app is displayed without any part of the Snowsight interface.
To enforce restricted access to only app-viewer URLs, an administrator must configure the ALLOWED\_INTERFACES user
property. For more information, see [Limit a user’s access to only Streamlit in Snowflake](/developer-guide/streamlit/object-management/security#label-limit-access-streamlit-only).

The app-viewer URL has the following format:

Copy code

```
https://app.snowflake.com/streamlit/<organization_name>/<account_name>/#/apps/<url_id>
```

Your app’s `url_id` is returned by DESCRIBE STREAMLIT.

## Share a Streamlit app

You can share an app with a role, or directly with a user through
[user-based access control (UBAC)](/user-guide/security-access-control-overview).

There are two sharing permission levels for Streamlit in Snowflake apps:

- **View and share**: If a user visits the app-builder URL, they can view the app and share it with other roles and users.
  This level grants USAGE WITH GRANT OPTION.
- **View only**: If a user visits the app-builder URL, they can only view the app. They can’t share it.

All roles and users with USAGE on the app can access the app-viewer URL, regardless of the sharing option.

To share a Streamlit app, do the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app you want to share.
4. Select **Share**.

   The **Share Streamlit app** window opens.
5. In the **Grant to a role or person** field, begin typing a role name or a username.
6. Select the role or user.

   The role or user appears in the sharing list.
7. In the drop-down list on the right of the role or user, select a sharing permission level.
8. If a warning icon appears next to a user, see [Grant USAGE on the database and schema](#label-streamlit-sharing-users-location-usage).
9. To copy your app’s URL, select **Copy link**.

   - To copy the app-builder URL, select **For app builders** from the dropdown list.
   - To copy the app-viewer URL, select **For app viewers** from the dropdown list.

   You can then send this URL through email or text.
10. Select **Done**. Your changes apply when you select **Done**.

## Share an app with a user

Privileges granted directly to a user take effect only when the user has all secondary roles enabled. For more
information, see [Granting privileges to a user](/user-guide/security-access-control-configure#label-security-grant-privileges-to-a-user).

To share an app with a user by using SQL:

Copy code

```
GRANT USAGE ON DATABASE streamlit_db TO USER jane_doe;
GRANT USAGE ON SCHEMA streamlit_db.streamlit_schema TO USER jane_doe;
GRANT USAGE ON STREAMLIT streamlit_db.streamlit_schema.streamlit_app TO USER jane_doe;
```

For **View and share**, add WITH GRANT OPTION to the grant on the app.

### Grant USAGE on the database and schema

A user also needs USAGE on the app’s database and schema. If they don’t have it, a warning icon appears next to their
name. Hover over it and select **Grant USAGE**. This grant applies immediately, not on **Done**. Revoking the user’s
access to the app later doesn’t revoke USAGE on the database and schema.

**Grant USAGE** appears only if your role can make the grant. The icon checks only direct grants, so a user who has
USAGE through a role can open the app without it.

### Notifications

Sharing an app with a user in the **Share Streamlit app** window notifies them in Snowsight, and by email if
their [email address is verified](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address). Grants made with SQL or Snowflake CLI don’t send
a notification.

### Stop sharing an app with a user

In the **Share Streamlit app** window, select the trash icon next to the user, and then select **Done**. This revokes
USAGE on the app but not on the database and schema. To keep the user’s access but stop them from sharing the app,
change them to **View only**.
