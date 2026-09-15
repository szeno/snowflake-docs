# Custom sleep timer for a Streamlit app

This topic describes how to set a custom sleep timer for a Streamlit app in Streamlit in Snowflake on warehouses.

## About sleep timers for Streamlit apps

Sleep timers only apply to Streamlit apps that use warehouse runtimes. Container runtimes
are intended for long-running services and don’t support sleep timers.

The sleep timer is configured using the Streamlit app’s `config.toml` configuration file.
If your app was created with the ROOT\_LOCATION parameter, you must use SQL to PUT the configuration
file in the app’s stage location. Otherwise, you can use SQL or the Snowsight Streamlit in Snowflake editor.

## WebSocket timeout

When a viewer opens a Streamlit app, a WebSocket connection is established between the
viewer’s browser and the Streamlit server. If there is no custom sleep timer, the
app will automatically suspend after the WebSocket connection times out due to inactivity.
At the account level, the default WebSocket timeout is approximately 15 minutes. You can
change your account’s WebSocket timeout for all Streamlit apps by contacting Snowflake Support.

When you set a custom sleep timer, the timer attempts to keep an app awake until the specified
time limit is reached, and then attempts to close the connection gracefully. However, depending
on a user’s browser settings, the timing mechanism may be suspended or delayed by an
inactive browser tab. In such cases, the app is subject to the WebSocket timeout setting. Therefore,
if you set a custom sleep timer that is less than the WebSocket timeout, your app may not
automatically suspend as quickly as expected in some scenarios. For the best results, set your
WebSocket timeout to be equal to the smallest custom sleep timer used by your apps.

Additionally, any mouse movement over an app will reset both the WebSocket timeout
and the custom sleep timer.

## Set a custom sleep timer using Snowsight

If your Streamlit app is using a warehouse runtime, to reduce code warehouse costs,
you can set a custom sleep timer for a Streamlit app to auto-suspend. If your app was
created with the ROOT\_LOCATION parameter, you must use the PUT command instead of Snowsight.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**, and then select your Streamlit app.
3. In the upper-right corner, select **Edit**.
4. If `.streamlit/config.toml` doesn’t exist, in the file explorer on the left,
   select [![Plus icon](/static/images/snowsight/icons/plus-icon-blue-bg.png)](/static/images/snowsight/icons/plus-icon-blue-bg.png) » **Create new file.** Enter `.streamlit/config.toml`, and select **Create**.
5. In the file explorer on the left, navigate to `.streamlit/config.toml`.
6. In the file editor, set the value of `streamlitSleepTimeoutMinutes` in the `[snowflake.sleep]` table.

   For example, if you want the Streamlit app to auto-suspend after 8 minutes, add the following text to the `config.toml` file:

   Copy code

   ```
   [snowflake]
   [snowflake.sleep]
   streamlitSleepTimeoutMinutes = 8
   ```

## Set a custom sleep timer using the PUT command

If your Streamlit app was created with the ROOT\_LOCATION parameter, you must use
the PUT command to modify your app’s configuration file. If your Streamlit app was created with the
FROM parameter, you can use either the PUT command or Snowsight to modify your app’s
configuration file.

1. Create or modify the `config.toml` file on your local machine to set
   `streamlitSleepTimeoutMinutes` in the `[snowflake.sleep]` table.

   For example, if you want the Streamlit app to auto-suspend after 8 minutes, include the following text in your `config.toml` file:

   Copy code

   ```
   [snowflake]
   [snowflake.sleep]
   streamlitSleepTimeoutMinutes = 8
   ```
2. Upload the `config.toml` file to your app’s stage location.
   If your app was created with the ROOT\_LOCATION parameter, execute the following command:

   Copy code

   ```
   PUT file:///<path_to_your_local_directory>/config.toml @streamlit_db.streamlit_schema.streamlit_stage/.streamlit/ overwrite=true auto_compress=false;
   ```

   If your app was created with the FROM parameter, execute the following command:

   Copy code

   ```
   PUT file:///<path_to_your_local_directory>/config.toml snow://streamlit/streamlit_db.streamlit_schema.streamlit_stage/versions/live/.streamlit/ overwrite=true auto_compress=false;
   ```

For more information about working with Streamlit files, see [Create your Streamlit app](/developer-guide/streamlit/app-development/creating-your-app).

Note

You can set the `streamlitSleepTimeoutMinutes` to any value between 5 to 240 minutes.

If you do not create the configuration file to specify the timer, the default auto-suspend time is 15 minutes.
