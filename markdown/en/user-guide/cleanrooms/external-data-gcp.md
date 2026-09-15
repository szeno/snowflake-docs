# Snowflake Data Clean Room: External data from Google Cloud Platform

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

Note

Snowflake Data Clean Rooms do not currently support data subject consent management. Customers are responsible for ensuring they have
obtained all necessary rights and consents to use the data linked in their clean rooms. Customers must also ensure compliance with all
applicable laws and regulations when using Data Clean Rooms, including in connection with third-party connectors.

Data analyzed in a [Snowflake Data Clean Room](/user-guide/cleanrooms/overview) can be native to Snowflake, reside externally
in cloud provider storage, or both. A *connector* allows collaborators to access external data from a cloud provider from within the clean
room.

The external data connector uses [Snowflake external tables](/user-guide/tables-external-intro) to make data
available. Be aware that there is an increased security risk associated with linking external tables in a clean room. As a result,
the provider must explicitly allow the use of external tables in the clean room before
consumers can use a connector to include external data. If the provider uses the external data connector, the consumer is warned that
external tables are being used so they can decide whether to install the clean room.

This topic describes how to use a connector so clean room analysts can access external data from a Google Cloud Platform bucket.

Important

Third-party connectors are not offered by Snowflake and may be subject to additional terms. These integrations are made available for
your convenience, but you are responsible for any content sent to or received from the integrations.

Customers are responsible for obtaining any necessary consents in connection with their use of Snowflake Data Clean Rooms. Please ensure
that you are complying with applicable laws and regulations when using Snowflake Data Clean Rooms, including in connection with
third-party connectors for activation purposes.

## Prerequisites

To use the connector for external data:

- The provider must explicitly [allow the use of external tables in the clean room](/user-guide/cleanrooms/register-data).
- Files must be in parquet format.

## Connect to a Google Cloud Platform bucket

Allowing clean room collaborators to access data from Google Cloud Platform (GCP) storage consists of the following steps:

1. In GCP, [obtain the URL of the GCP bucket](#label-cleanroom-external-data-gcp-url).
2. In the clean room environment, [create the connector](#label-cleanroom-external-data-gcp-connector).
3. In GCP, [grant permissions to the connector](#label-cleanroom-external-data-gcp-permissions).
4. In the clean room environment, [authenticate the connector with GCP](#label-cleanroom-external-data-gcp-authenticate).

The following sections discuss these steps in more detail.

### Obtain the URL of the GCP bucket

The clean room connector needs the URL of the GCP storage bucket in order to access the data. Before creating the connector, you must:

1. Sign in to Google Cloud Platform Console as a project editor.
2. From the Console dashboard, select **Cloud Storage** » **Browser**.
3. Select the bucket that contains the data you want to access from the clean room, and navigate to the location of that data. The bucket
   cannot be empty.
4. Select the copy icon to copy the URL of the storage bucket and save it for the next task.

### Create the connector and copy the service account identifier

You are now ready to create the connector in the clean room environment. Once you have created the connector, you need to copy details about
its service account so it can be associated with the bucket in GCP. To create the connector in your clean room environment:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Connectors**, then expand the **Google Cloud** section.
3. In the **Storage bucket URL** field, enter the URL that you copied from GCP, then replace `https://` with `gcs://` in the URL.
4. Select **Create**. The clean room generates a service account that it uses to access GCP.
5. Use the Copy icon to copy the identifier of the service account, and save it for the next task.

### Grant permissions to the connector

Clean rooms need permission to access external data in the GCP bucket. Granting these permissions consists of creating a dedicated GCP role
for the connector’s service account, then adding the service account as a principal of the GCP bucket.

To create the dedicated GCP role for the connector’s service account:

1. Sign in to the Google Cloud Platform Console as a project editor.
2. From the Console dashboard, select **IAM & admin** » **Roles**.
3. Select **Create Role**.
4. Enter a name and description for the role.
5. Select **Add Permissions**, then add the following permissions:

> - `storage.buckets.get`
> - `storage.objects.list`
> - `storage.objects.get`

Now that you have created a dedicated role, you are ready to associate the connector’s service account as a principal of the GCP bucket.
To associate the service account:

1. Sign in to Google Cloud Platform Console as a project editor.
2. From the Console dashboard, select **Cloud Storage** » **Browser**.
3. Select the bucket that contains the external data.
4. Select **Show Info Panel**. The information panel slides open.
   [![Show the info panel of a Google Cloud Platform bucket](/static/images/cleanrooms/gcp-bucket-show-info-panel.png)](/static/images/cleanrooms/gcp-bucket-show-info-panel.png)
5. Select **Add Principals**.
6. In the **New Principals** text box, paste the service account identifier that you copied from the clean room.
7. From the **Select a role** drop-down list, select the dedicated role you created for the service account.

### Authenticate the connector

You are now ready to authenticate the connector to make sure it can access the GCP bucket. To authenticate the connector:

1. In the left navigation of the clean room, select **Connectors** and expand the **Google Cloud** section. If you are signed out of the
   clean room, see [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. Select the GCP bucket you are connecting to, and select **Authenticate**.

## Remove access to external data on GCP

To remove access to a GCP bucket from a clean room environment:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Connectors**, then expand the **Google Cloud** section.
3. Find the GCP bucket that is currently connected, and select the trash can icon.
