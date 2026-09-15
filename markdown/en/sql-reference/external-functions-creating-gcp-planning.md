# Planning an external function for GCP

This topic helps you prepare to create an external function for GCP (Google Cloud Platform) using the Google Cloud Console
user interface.

## Prerequisites

These instructions assume that you are an experienced Google Cloud Console user.

To create an external function for GCP, you must have the following:

- A Google Cloud project ID.
- The correct services enabled for your Google Cloud Project. For detailed requirements, see the
  [Quickstart for Deploying an API/API Gateway using gcloud](https://cloud.google.com/api-gateway/docs/quickstart).

## Create a worksheet to track required information

As you complete the tasks to create an external function in the Google Cloud Console, you are required to enter specific values
(for example, Cloud Function Trigger URL) during each step in the process. Often, the values you enter are required in subsequent steps.

To facilitate recording/tracking this information, we’ve provided a worksheet with fields for each of the required values:

Copy code

```
================================================================================
=================== Tracking Worksheet: Google Cloud Console ===================
================================================================================

****** Step 1: Cloud Function (Remote Service) Info ****************************

Cloud Function Trigger URL: ____________________________________________________

****** Step 2: API Config File Info ********************************************

Path Suffix: ___________________________________________________________________
Configuration File Name: _______________________________________________________

****** Step 2: API Gateway (Proxy Service) Info ********************************

Managed Service Identifier: ____________________________________________________
Gateway Base URL: _____________________________________________________________

****** Steps 3-4: API Integration & External Function Info *********************

API Integration Name: __________________________________________________________
API_GCP_SERVICE_ACCOUNT: _______________________________________________________

External Function Name: ________________________________________________________

****** Step 5: Security Info ***************************************************

Security Definition Name: ______________________________________________________
```

## Next step

[Step 1: Create the remote service (Google Cloud Function) in the console](/sql-reference/external-functions-creating-gcp-ui-remote-service)
