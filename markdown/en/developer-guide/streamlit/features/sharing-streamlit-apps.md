# Sharing Streamlit in Snowflake apps

Feature — Generally Available

Not supported in government regions.

This topic covers URLs for sharing Streamlit in Snowflake apps with or without the Snowsight interface.

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
the app, the toolbar contains an **Edit** button. If you have the necessary permission to share the app with other roles, the toolbar
contains a **Share** button.

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

There are two sharing permission levels for Streamlit in Snowflake apps:

- **View and share**: If a user visits the app-builder URL, they can view the app and share it with other roles.
- **View only**: If a user visits the app-builder URL, they can only view the app. They can’t share it with other roles.

All roles with necessary USAGE privileges on the app can access the app-viewer URL, regardless of the sharing option.

To share a Streamlit app, do the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app you want to share.
4. Select **Share**.

   The **Share Streamlit app** window opens.
5. To add a role to the app’s sharing list, begin typing the name of the role.
6. Select the name of the role.

   The new role appears in the list of roles.
7. In the drop-down list on the right of the role, select a sharing permission level.
8. To copy your app’s URL, select **Copy link**.

   - To copy the app-builder URL, select **For app builders** from the dropdown list.
   - To copy the app-viewer URL, select **For app viewers** from the dropdown list.

   You can then send this URL through email or text.
9. Select **Done**.
