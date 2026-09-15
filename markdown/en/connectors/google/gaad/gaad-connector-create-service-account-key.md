# Configure service account authentication for Google Cloud

## Prerequisites

To provide the service account file, you must first create a Google Cloud project. For information about creating Google Cloud projects, see the Google Cloud documentation.

## Create a service account key

1. To open the service account creator, in your Google Cloud project, select **APIs & Services** » **Credentials**.
2. Select **Create credentials** » **service account**.
3. In the **Service account details** enter any service account name you choose.
4. To create the service account, select **Done**.
5. To manage the new service account, in the **Credentials** section, select the service account name.
6. Select **Keys** » **Add key** » **Create a new key**.
7. To save the service account key file, in the key type selection view, select the recommended JSON type, and then select **Create**.

   This file is needed during the connector configuration.

## Formatting the service account key

The service account key you downloaded in the previous procedure can be used to automatically complete the form when configuring the connector, using the drag-and-drop functionality in the configuration wizard.

If the private key is entered manually, it must be properly formatted first.

Example service account key in JSON format:

> Copy code
>
> ```
> {
>   "type": "service_account",
>   "project_id": "your-project-id0809",
>   "private_key_id": "7a7df777f88...f7f7s8d7f7s",
>   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADC9ON1OA4JjRidj\n/7O5Ioq+L2112946/CsXsfiHFwIQQedWt\nQ75sl7M5lHTsVQtIdtBcGJXvk5/7CHOmtkn6w\n2dRoyCWv2bknmogZIy3fssMolwVaZ15cmsuB0\nwTI81dojSVwrzPshiYY9lfugdVZ2uiFcw4haWo8o\nUhg2tHOWyveoFN2RF03kUfdnEfhAAmXKZai\nWkd49r+jAgMBAAECggEAIP/5TIE9LJ4QAZcXG2sEQl7GldrQho0nuAOVkEtzQsuP\ndmgbFYU39qinuLc83GF/Ghr3PdswzQTKeKCvZZXhQ4FpYk9VhyQr6iTKv6bBD8du\nMrF2LKknax1eCFG81o0A+zOvo\npMrJl/9EOOVJKnifhH7kdS/JRqHXEzQUGkpOWSs6ep7MGN4+vLv+GlZqIIgEGwmW\nJN/72+5bLiaL9T7If1+/T/sa\n-----END PRIVATE KEY-----\n",
>   "client_email": "testclientemail.gserviceaccount.com",
>   "client_id": "2345345634546456",
>   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
>   "token_uri": "https://oauth2.googleapis.com/token",
>   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
>   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/you-project.....",
>   "universe_domain": "googleapis.com"
> }
> ```

For the private key, only the text between **-----BEGIN PRIVATE KEY-----** and **-----END PRIVATE KEY-----** is relevant.

To transform a private key to the format acceptable by the connector, follow this procedure:

1. In a text editor, open the key downloaded in the previous procedure.
2. Copy the content of the **private\_key** field.
3. Delete both the -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY----- markers.
4. Delete all \n (newline) characters from the file. A key usually contains at least 10 occurrences.
5. Save the file for later use.

After edits, your key should resemble this code:

> Copy code
>
> ```
> MIIEvgIBADC9ON1OA4JjRidj/7O5Ioq+L2112946/CsXsfiHFwIQQedWtQ75sl7M5lHTsVQtIdtBcGJXvk5/7CHOmtkn6w2dRoyCWv2bknmogZIy3fssMolwVaZ15cmsuB0wTI81dojSVwrzPshiYY9lfugdVZ2uiFcw4haWo8oUhg2tHOWyveoFN2RF03kUfdnEfhAAmXKZaiWkd49r+jAgMBAAECggEAIP/5TIE9LJ4QAZcXG2sEQl7GldrQho0nuAOVkEtzQsuPdmgbFYU39qinuLc83GF/Ghr3PdswzQTKeKCvZZXhQ4FpYk9VhyQr6iTKv6bBD8duMrF2LKknax1eCFG81o0A+zOvopMrJl/9EOOVJKnifhH7kdS/JRqHXEzQUGkpOWSs6ep7MGN4+vLv+GlZqIIgEGwmWJN/72+5bLiaL9T7If1+/T/sa
> ```

## Grant the service account access to Google Analytics

The service account requires access to all Google Analytics properties that the connector will use.

1. In the Google Analytics console, choose a property that will be used by the connector.
2. Select the **Property access management** tab.
3. Add the service account email as a **Viewer**.
4. Repeat this process for all properties that will be used in the connector.
