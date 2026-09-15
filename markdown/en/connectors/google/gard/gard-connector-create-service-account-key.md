# Configuring service account authentication for Google Cloud Platform (GCP)

## Prerequisites

An application that authenticates to Google using a service account must provide a service account key file with correct roles set.

To provide the service account key file, you must create a Google Cloud Platform (GCP) project first. Refer to the GCP documentation to learn how to create a GCP project.

## Creating a service account key

The following procedure describes how to create a service account:

1. To open the service account creator, select **APIs & Services** » **Credentials** in your GCP project.
2. Select **Create credentials** » **Service account**.
3. In the **Service account details** form type in a service account name of your choice.
4. In the **Grant this service account access to project** section you need to grant this service account at least the following set of roles: BigQuery Data Viewer, BigQuery Read Session User and BigQuery Job User.
5. After creating a service account find it on the list in the **Credentials** section and press on its name in order to manage the service account.
6. Select **Keys** » **Add key** » **Create a new key**.
7. In the key type selection view choose the recommended JSON type and press **Create** in order to save the service account key, which will be needed during the connector configuration.

## Setting up access to multiple GCP projects

You may have multiple Google Analytics properties exported to separate GCP projects. To ingest data for all of them with a single Snowflake Connector for Google Analytics Raw Data instance, you will need to allow access for the service account to each of the GCP projects.

The following procedure describes how to allow access for the previously created service account to an additional GCP project.

1. Note the Email value of the service account you created earlier.
2. In the selected GCP project, go to the **IAM & Admin** » **IAM** section.
3. Above the list of principals, select **Grant Access**.
4. In the **New principals** form type the Email of your service account.
5. In the **Select a role** form choose all the following roles: BigQuery Data Viewer, BigQuery Read Session User and BigQuery Job User.
6. Press **Save** and confirm that the service account’s Email appears in the list of principals.
