# Option 1: Load data with the Snowpipe REST API

This topic describes how to call the public REST endpoints to load data and retrieve load history reports. The instructions assume you have completed the setup instructions in
[Data loading preparation using the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs).

## Load data

Loading takes place in two steps:

Step 1:
:   Stage your data files:

    - Internal stage: Use the [PUT](/sql-reference/sql/put) command to stage your files.
    - External stage: Use the client tools provided by the cloud provider to copy your files to the stage location (Amazon S3, Google Cloud Storage, or Microsoft Azure).

Step 2:
:   Submit a request to the [insertFiles](/user-guide/data-load-snowpipe-rest-apis#label-rest-api-insertfiles) REST endpoint to load the staged data files.

    For your convenience, sample Java and Python programs that illustrate how to submit a REST endpoint are provided in this topic.

### Sample program for the Java SDK

Copy code

```
import net.snowflake.ingest.SimpleIngestManager;
import net.snowflake.ingest.connection.HistoryRangeResponse;
import net.snowflake.ingest.connection.HistoryResponse;
import org.bouncycastle.asn1.pkcs.PrivateKeyInfo;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.openssl.PEMParser;
import org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter;
import org.bouncycastle.openssl.jcajce.JceOpenSSLPKCS8DecryptorProviderBuilder;
import org.bouncycastle.operator.InputDecryptorProvider;
import org.bouncycastle.operator.OperatorCreationException;
import org.bouncycastle.pkcs.PKCS8EncryptedPrivateKeyInfo;
import org.bouncycastle.pkcs.PKCSException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.security.PrivateKey;
import java.security.Security;
import java.time.Instant;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class SDKTest
{
  // Path to the private key file that you generated earlier.
  private static final String PRIVATE_KEY_FILE = "/<path>/rsa_key.p8";

  public static class PrivateKeyReader
  {
    // If you generated an encrypted private key, implement this method to return
    // the passphrase for decrypting your private key.
    private static String getPrivateKeyPassphrase() {
      return "<private_key_passphrase>";
    }

    public static PrivateKey get(String filename)
            throws Exception
    {
      PrivateKeyInfo privateKeyInfo = null;
      Security.addProvider(new BouncyCastleProvider());
      // Read an object from the private key file.
      PEMParser pemParser = new PEMParser(new FileReader(Paths.get(filename).toFile()));
      Object pemObject = pemParser.readObject();
      if (pemObject instanceof PKCS8EncryptedPrivateKeyInfo) {
        // Handle the case where the private key is encrypted.
        PKCS8EncryptedPrivateKeyInfo encryptedPrivateKeyInfo = (PKCS8EncryptedPrivateKeyInfo) pemObject;
        String passphrase = getPrivateKeyPassphrase();
        InputDecryptorProvider pkcs8Prov = new JceOpenSSLPKCS8DecryptorProviderBuilder().build(passphrase.toCharArray());
        privateKeyInfo = encryptedPrivateKeyInfo.decryptPrivateKeyInfo(pkcs8Prov);
      } else if (pemObject instanceof PrivateKeyInfo) {
        // Handle the case where the private key is unencrypted.
        privateKeyInfo = (PrivateKeyInfo) pemObject;
      }
      pemParser.close();
      JcaPEMKeyConverter converter = new JcaPEMKeyConverter().setProvider(BouncyCastleProvider.PROVIDER_NAME);
      return converter.getPrivateKey(privateKeyInfo);
    }
  }

  private static HistoryResponse waitForFilesHistory(SimpleIngestManager manager,
                                                     Set<String> files)
          throws Exception
  {
    ExecutorService service = Executors.newSingleThreadExecutor();

    class GetHistory implements
            Callable<HistoryResponse>
    {
      private Set<String> filesWatchList;
      GetHistory(Set<String> files)
      {
        this.filesWatchList = files;
      }
      String beginMark = null;

      public HistoryResponse call()
              throws Exception
      {
        HistoryResponse filesHistory = null;
        while (true)
        {
          Thread.sleep(500);
          HistoryResponse response = manager.getHistory(null, null, beginMark);
          if (response.getNextBeginMark() != null)
          {
            beginMark = response.getNextBeginMark();
          }
          if (response != null && response.files != null)
          {
            for (HistoryResponse.FileEntry entry : response.files)
            {
              //if we have a complete file that we've
              // loaded with the same name..
              String filename = entry.getPath();
              if (entry.getPath() != null && entry.isComplete() &&
                      filesWatchList.contains(filename))
              {
                if (filesHistory == null)
                {
                  filesHistory = new HistoryResponse();
                  filesHistory.setPipe(response.getPipe());
                }
                filesHistory.files.add(entry);
                filesWatchList.remove(filename);
                //we can return true!
                if (filesWatchList.isEmpty()) {
                  return filesHistory;
                }
              }
            }
          }
        }
      }
    }

    GetHistory historyCaller = new GetHistory(files);
    //fork off waiting for a load to the service
    Future<HistoryResponse> result = service.submit(historyCaller);

    HistoryResponse response = result.get(2, TimeUnit.MINUTES);
    return response;
  }

  public static void main(String[] args)
  {
    final String host = "<account_identifier>.snowflakecomputing.com";
    final String user = "<user_login_name>";
    final String pipe = "<db_name>.<schema_name>.<pipe_name>";
    try
    {
      final long oneHourMillis = 1000 * 3600L;
      String startTime = Instant
              .ofEpochMilli(System.currentTimeMillis() - 4 * oneHourMillis).toString();
      final PrivateKey privateKey = PrivateKeyReader.get(PRIVATE_KEY_FILE);
      SimpleIngestManager manager = new SimpleIngestManager(host.split("\.")[0], user, pipe, privateKey, "https", host, 443);
      List<StagedFileWrapper> files = new ArrayList<>();
      // Add the paths and sizes the files that you want to load.
      // Use paths that are relative to the stage where the files are located
      // (the stage that is specified in the pipe definition)..
      files.add(new StagedFileWrapper("<path>/<filename>", <file_size_in_bytes> /* file size is optional but recommended, pass null when it is not available */));
      files.add(new StagedFileWrapper("<path>/<filename>", <file_size_in_bytes> /* file size is optional but recommended, pass null when it is not available */));
      ...
      manager.ingestFiles(files, null);
      HistoryResponse history = waitForFilesHistory(manager, files);
      System.out.println("Received history response: " + history.toString());
      String endTime = Instant
              .ofEpochMilli(System.currentTimeMillis()).toString();

      HistoryRangeResponse historyRangeResponse =
              manager.getHistoryRange(null,
                                      startTime,
                                      endTime);
      System.out.println("Received history range response: " +
                                 historyRangeResponse.toString());

    }
    catch (Exception e)
    {
      e.printStackTrace();
    }

  }
}
```

This example uses the [Bouncy Castle Crypto APIs](https://www.bouncycastle.org/java.html). In order to compile and run this
example, you must include the following JAR files in your classpath:

- the provider JAR file (`bcprov-jdkversions.jar`)
- the PKIX / CMS / EAC / PKCS / OCSP / TSP / OPENSSL JAR file (`bcpkix-jdkversions.jar`)

where `versions` specifies the versions of the JDK that the JAR file supports.

Before you compile the sample code, replace the following placeholder values:

> `PRIVATE_KEY_FILE = "/<path>/rsa_key.p8"`
> :   Specify the local path to the private key file you created in [Use key pair authentication & key rotation](/user-guide/data-load-snowpipe-rest-gs#label-configuring-rsa-authentication-keys) (in [Data loading preparation using the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs)).
>
> `return "<private_key_passphrase>"` in `getPrivateKeyPassphrase()`
> :   If you generated an encrypted key, implement the `getPrivateKeyPassphrase()` method to return the passphrase for decrypting that key.
>
> `host = "<account_identifier>.snowflakecomputing.com"`
> :   Specify your host information in the form of a URL.
>
>     The preferred format of the account identifier is as follows:
>
>     `organization_name-account_name`
>     :   Names of your Snowflake organization and account. For details, see [Format 1 (preferred): Account name in your organization](/user-guide/admin-account-identifier#label-account-name).
>
>     Alternatively, specify your *account locator*, along with the [region](/user-guide/intro-regions) and [cloud platform](/user-guide/intro-cloud-platforms) where the account is hosted, if required. For details, see [Format 2: Account locator in a region](/user-guide/admin-account-identifier#label-account-locator).
>
> `user = "<user_login_name>"`
> :   Specify your Snowflake login name.
>
> `pipe = "<db_name>.<schema_name>.<pipe_name>"`
> :   Specify the fully-qualified name of the pipe to use to load the data.
>
> `files.add("<path>/<filename>", <file_size_in_bytes>)`
> :   Specify the path to your files to load in the file objects list.
>
>     Optionally specify the size of each file, in bytes, to avoid delays when Snowpipe calculates the operations required to load the data.
>
>     The path you specify must be relative to the stage where the files are located. Include the complete name for each file, including the file extension. For example, a CSV file that is gzip-compressed might have the extension `.csv.gz`.

### Sample program for the Python SDK

Copy code

```
from logging import getLogger
from snowflake.ingest import SimpleIngestManager
from snowflake.ingest import StagedFile
from snowflake.ingest.utils.uris import DEFAULT_SCHEME
from datetime import timedelta
from requests import HTTPError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.primitives.serialization import NoEncryption
import time
import datetime
import os
import logging

logging.basicConfig(
        filename='/tmp/ingest.log',
        level=logging.DEBUG)
logger = getLogger(__name__)

# If you generated an encrypted private key, implement this method to return
# the passphrase for decrypting your private key.
def get_private_key_passphrase():
  return '<private_key_passphrase>'

with open("/<private_key_path>/rsa_key.p8", 'rb') as pem_in:
  pemlines = pem_in.read()
  private_key_obj = load_pem_private_key(pemlines,
  get_private_key_passphrase().encode(),
  default_backend())

private_key_text = private_key_obj.private_bytes(
  Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode('utf-8')
# Assume the public key has been registered in Snowflake:
# private key in PEM format

ingest_manager = SimpleIngestManager(account='<account_identifier>',
                                     host='<account_identifier>.snowflakecomputing.com',
                                     user='<user_login_name>',
                                     pipe='<db_name>.<schema_name>.<pipe_name>',
                                     private_key=private_key_text)
# List of files, but wrapped into a class
staged_file_list = [
  StagedFile('<path>/<filename>', <file_size_in_bytes>),  # file size is optional but recommended, pass None if not available
  StagedFile('<path>/<filename>', <file_size_in_bytes>),  # file size is optional but recommended, pass None if not available
  ...
  ]

try:
    resp = ingest_manager.ingest_files(staged_file_list)
except HTTPError as e:
    # HTTP error, may need to retry
    logger.error(e)
    exit(1)

# This means Snowflake has received file and will start loading
assert(resp['responseCode'] == 'SUCCESS')

# Needs to wait for a while to get result in history
while True:
    history_resp = ingest_manager.get_history()

    if len(history_resp['files']) > 0:
        print('Ingest Report:\n')
        print(history_resp)
        break
    else:
        # wait for 20 seconds
        time.sleep(20)

    hour = timedelta(hours=1)
    date = datetime.datetime.utcnow() - hour
    history_range_resp = ingest_manager.get_history_range(date.isoformat() + 'Z')

    print('\nHistory scan report: \n')
    print(history_range_resp)
```

Before you execute the sample code, replace the following placeholder values:

> `<private_key_path>`
> :   Specify the local path to the private key file you created in [Use key pair authentication & key rotation](/user-guide/data-load-snowpipe-rest-gs#label-configuring-rsa-authentication-keys) (in [Data loading preparation using the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs)).
>
> `return "<private_key_passphrase>"` in `get_private_key_passphrase()`
> :   If you generated an encrypted key, implement the `get_private_key_passphrase()` function to return the passphrase for decrypting that key.
>
> `account='<account_identifier>'`
> :   Specify the unique identifier for your account (provided by Snowflake). See the `host` description.
>
> `host='<account_identifier>.snowflakecomputing.com'`
> :   Specify the unique hostname for your Snowflake account.
>
>     The preferred format of the account identifier is as follows:
>
>     `organization_name-account_name`
>     :   Names of your Snowflake organization and account. For details, see [Format 1 (preferred): Account name in your organization](/user-guide/admin-account-identifier#label-account-name).
>
>     Alternatively, specify your *account locator*, along with the [region](/user-guide/intro-regions) and [cloud platform](/user-guide/intro-cloud-platforms) where the account is hosted, if required. For details, see [Format 2: Account locator in a region](/user-guide/admin-account-identifier#label-account-locator).
>
> `user='<user_login_name>'`
> :   Specify your Snowflake login name.
>
> `pipe='<db_name>.<schema_name>.<pipe_name>'`
> :   Specify the fully-qualified name of the pipe to use to load the data.
>
> `file_list=['<path>/<filename>', '<path>/<filename>']` | `staged_file_list=[StagedFile('<path>/<filename>', <file_size_in_bytes>), StagedFile('<path>/<filename>', <file_size_in_bytes>)]`
> :   Specify the path to your files to load in the file objects list.
>
>     The path you specify must be relative to the stage where the files are located. Include the complete name for each file, including the file extension. For example, a CSV file that is gzip-compressed might have the extension `.csv.gz`.
>
>     Optionally specify the size of each file, in bytes, to avoid delays when Snowpipe calculates the operations required to load the data.

## View the load history

Snowflake provides [REST endpoints](/user-guide/data-load-snowpipe-rest-apis) and an [Snowflake Information Schema](/sql-reference/info-schema) table function for viewing your load history:

- REST endpoints:

  - [insertReport](/user-guide/data-load-snowpipe-rest-apis#label-rest-api-insertreport)
  - [loadHistoryScan](/user-guide/data-load-snowpipe-rest-apis#label-rest-api-loadhistoryscan)
- Information Schema table function:

  - [COPY\_HISTORY](/sql-reference/functions/copy_history)
- Account Usage view:

  - [COPY\_HISTORY](/sql-reference/account-usage/copy_history)

Note that querying either the Information Schema table function or Account Usage view, unlike calling the REST endpoints, requires a running warehouse.

## Delete staged files

Delete the staged files after you successfully load the data and no longer require the files. For instructions, see
[Deleting staged files after Snowpipe loads the data](/user-guide/data-load-snowpipe-manage#label-snowpipe-delete-data-files).
