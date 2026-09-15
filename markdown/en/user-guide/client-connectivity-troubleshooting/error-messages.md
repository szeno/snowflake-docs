# Error messages

Client connectivity error messages can signal various underlying causes located in the network path between a host and a Snowflake endpoint, including any possible proxies, security appliances, load balancers, DNS servers, and so on. You can find common error messages and their potential causes and resolutions for the following clients:

# JDBC errors

|  |  |
| --- | --- |
| JDBC error 1 | **Error(s)**  ``` Cannot connect: connection refused: Java::NetSnowflakeClientJdbc::SnowflakeSQLException: JDBC driver encountered communication error. Message: Exception encountered for HTTP request: Connection reset. ```  **Root cause**: This error has various underlying causes, located in the network path between the host you’re trying to connect from, and the Snowflake endpoint, including any possible proxies, security appliances, load balancers and such.  **Resolution scenario**: label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 2 | **Error(s)**  ``` JDBC driver encountered communication error. Message: Exception encountered for HTTP request:  sun.security.validator.ValidatorException: No trusted certificate found.  OR  javax.net.ssl.SSLHandshakeException: No trusted certificate found  OR  'SSL peer certificate or SSH remote key was not OK' ```  **Root cause**: The issue is likely caused by a proxy or security appliance performing an SSL inspection.  On rare occasions, usually with older installations of Java, the same symptom can also occur when there’s no SSL inspection but the cloud provider changed one of the intermediary certificate authorities to another (well-known) authority, which is not yet present in the truststore.  **Resolution scenario**: label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 3 | **Error(s)**  ``` JDBC driver encountered a communication error. Message: Exception encountered for an HTTP request: Network is unreachable (Connect Failed) ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 4 | **Error(s)**  ``` JDBC driver encountered communication error. Message: Exception encountered for HTTP request: <SERVICE_ENDPOINT>: nodename nor servname provided, or not known. ```  **Root cause**: See label-client\_connectivity\_dns\_issues.  **Resolution scenario**: label-client\_connectivity\_dns\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 5 | **Error(s)**  ``` WARNING!!! Using fail-open to connect. Driver is connecting to an HTTPS endpoint without OCSP based Certificate Revocation checking as it could not obtain a valid OCSP Response to use from the CA OCSP responder. Details: {"cacheEnabled":true,"ocspReqBase64":null,"ocspMode":"FAIL_OPEN","sfcPeerHost":"<SERVICE_ENDPOINT>","ocspResponderURL":null,"cacheHit":true,"eventType":"OCSPValidationError","certId":"<OBFUSCATED>"} ```  **Root cause**: See label-client\_connectivity\_ocsp\_issues.  **Resolution scenario**: label-client\_connectivity\_ocsp\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 6 | **Error(s)**  ``` JDBC driver internal error: Max retry reached for the download of #chunk0 (Total chunks:<x>) retry=<y>, error=net.snowflake.client.jdbc.SnowflakeSQLException: JDBC driver encountered communication error. Message: Error encountered when downloading a result chunk: ```  **Root cause**: See label-client\_connectivity\_large\_result\_issues.  **Resolution scenario**: label-client\_connectivity\_large\_result\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 7 | **Error(s)**  ``` JDBC driver encountered communication error. Message: Exception encountered for HTTP request: Failed to find the root CA ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 8 | **Error(s)**  ``` net.snowflake.client.jdbc.internal.apache.http.impl.execchain.RetryExec execute INFO: I/O exception (java.net.SocketException) caught when processing request to {s}->https://[<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>]:443: Broken pipe (Write failed) ```  **Root cause**:  The client driver tried to send data over a connection (pipe) which it believes to be up, which particular connection is already closed down on the remote end, just the client driver was not aware of this.   - a simple(r) scenario for this error is when there is an idle timeout configured on a proxy or security appliance between the client driver and Snowflake, which when expires, terminates the connection without notifying the parties - oftentimes, troubleshooting the true underlying root cause of what exactly, and why is tearing down the connections between the client driver and Snowflake can be a complex endeavor where details are out of scope for this documentation   **Resolution scenario**:  You can configure a TTL inside the JDBC driver which will gracefully close the connections from the client side sooner than they would be torn down by a remote idle timeout; preventing the issue. Setting is available from JDBC driver version 3.12.17; and from 3.13.30 there’s a default (1 minute) already configured.  For more information, see [Troubleshooting](/developer-guide/jdbc/jdbc-using#label-jdbc-connection-reset-error). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 9 | **Error(s)**  ``` JDBC driver encountered communication error. Message: Exception encountered for HTTP request: Remote host terminated the handshake ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 10 | **Error(s)**  ``` net.snowflake.client.jdbc.SnowflakeSQLLoggedException: JDBC driver encountered IO error. Message: Encountered exception during upload: null. ```  **Root cause**: The client driver has issues accessing the cloud storage associated with your Snowflake account, during an upload operation. This is caused by a misconfiguration on a proxy / security appliance sitting on the network path between the client driver and the cloud storage.  **Resolution scenario**: Although the direction of the traffic is the opposite, see label-client\_connectivity\_large\_result\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 11 | **Error(s)**  ``` JDBC driver encountered communication error. Message: Exception encountered for HTTP request: Certificate for [<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>] doesn't match any of the subject alternative names: [*.us-west-2.snowflakecomputing.com, *.us-west-2.aws.snowflakecomputing.com, *.global.snowflakecomputing.com, *.snowflakecomputing.com, *.prod1.us-west-2.aws.snowflakecomputing.com, *.prod2.us-west-2.aws.snowflakecomputing.com]. ```  **Root cause**: What this error message means: The client driver is trying to connect to a Snowflake account (or cloud storage) located in AWS US WEST, which is also the default cloud region. The connection is not successful, because the certificate seen by the client driver is not a match for the hostname in the request.  Most likely causes include:   - If your Snowflake account is not in AWS US WEST: most common issue is a misconfiguration in the account part in the JDBC driver connection string. - If your Snowflake account is indeed in AWS US WEST: likely cause could be a proxy / security appliance performing SSL inspection.   **Resolution scenario**:   - For the first cause, please either use the regionless notation in the account field of the configuration, such as myorg-test, myorg-prod, etc. Alternatively, if you want to use the locator notation, make sure to use the correct one as indicated in the [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config) documentation. For example, an account in AWS EU Frankfurt would be `xy12345.eu-central-1`. - For the second cause, see label-client\_connectivity\_large\_result\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| JDBC error 12 | Error(s)  ``` I/O exception (net.snowflake.client.jdbc.internal.apache.http.NoHttpResponseException) caught when processing request to {s}->https://[<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>].snowflakecomputing.com:443: The target server failed to respond ```  **Root cause**:  The client driver did not receive a timely response to the request sent to the remote endpoint.  Most likely causes include:   - If the issue is persistent, it is likely an actual connectivity problem. - If the issue is intermittent and specifically; if NoHttpResponseException happens very quickly (milliseconds) after the request has been sent, this error indicates that the TCP session between the client driver and the server is down, just the driver did not know about it. This latter often happens if an intermediary proxy/load balancer tears down the session between the client and the server, without letting any of the parties know.   **Resolution scenario**:   - For persistent errors and where the NoHttpResponseException happens after a longer wait following the request, please follow the [Troubleshooting steps](troubleshooting-steps). - For occasions where this exception is intermittent and is thrown very quickly after the client driver sends the request, between versions 3.12.17 and 3.13.30 you have a configuration option net.snowflake.jdbc.ttl to ensure idle connections are closed and thus prevent the intermediary node (such as `loadbalancer`) tearing it down unexpectedly, without telling the clients on the other ends. For more information, see [Troubleshooting](/developer-guide/jdbc/jdbc-using#label-jdbc-connection-reset-error).   From JDBC driver version 3.13.30 and onwards; you still have this configuration option but usually it’s not necessary to change it, as it now has a default value of 1 minute idle timeout (60 seconds).  In both scenarios, the JDBC driver should automatically retry sending the failed request per its retry strategy, without needing any user intervention. |

Expand

Show lessSee more

# ODBC errors

|  |  |
| --- | --- |
| ODBC error 1 | **Error(s)**  ``` 'OLE DB or ODBC error: [DataSource.Error] ERROR [HY000] [Snowflake][Snowflake] (25) Result download worker error: Worker error: [Snowflake][Snowflake] (4) REST request for URL <>.... :  CURLerror (curl_easy_perform() failed) - code=60 msg='SSL peer certificate or SSH remote key was not OK' osCode=9 osMsg='Bad file descriptor'. . '.* ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 2 | **Error(s)**  ``` Error: nanodbc/nanodbc.cpp:1135: 01S00: [Snowflake][Snowflake] (4) REST request for URL *** failed: CURLerror (curl_easy_perform() failed) - code=60 msg='SSL peer certificate or SSH remote key was not OK'. ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 3 | **Error(s)**  ``` 'SSL peer certificate or SSH remote key was not OK' ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 4 | **Error(s)**  ``` SSL certificate problem: self signed certificate in certificate chain. Please check for SSL interception proxy in your network. ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 5 | **Error(s)**  ``` CURLerror (curl _easy_perform failed) - code=35 msg='SSL connect error' osCode=10054 osMsg='Unknown error'. ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 6 | **Error(s)**  ``` 'Empty reply from server' (CURLerror (curl_easy_perform() failed) - code=52 msg='Server returned nothing (no header..) ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 7 | **Error(s)**  ``` ERROR 5052 Simba::ODBC::Connection::SQLDriverConnectW: [Snowflake][Snowflake] (4) REST request for URL https://[<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>]:443/session/v1/login-request?requestId=<OBFUSCATED>&request_guid=<OBFUSCATED>&databaseName=<OBFUSCATED>&schemaName=<OBFUSCATED>&warehouse=<OBFUSCATED>failed: CURLerror (curl_easy_perform() failed) - code=35 msg='SSL connect error'. ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 8 | **Error(s)**  ``` ERROR 710 Simba::ODBC::Statement::SQLFetchScroll: [Snowflake][Snowflake] (25) Result download worker error: Worker error: [Snowflake][Snowflake] (4) REST request for URL https://<STAGE>/<OBFUSCATED>/results/<OBFUSCATED>_0/main/data_0_0_1?x-amz-server-side-encryption-customer-algorithm=<OBFUSCATED>&response-content-encoding=gzip&AWSAccessKeyId=<OBFUSCATED>&Expires=<OBFUSCATED>&Signature=<OBFUSCATED> failed: CURLerror (curl_easy_perform() failed) - code=52 msg='Server returned nothing (no headers, no data)'. ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 9 | **Error(s)**  ``` [Snowflake][Snowflake] (6) Assertion failure: error_in_response_json ```  **Root cause**: There are multiple factors that can lead to this error.  **Resolution scenario**: Try [Common connectivity issues and resolutions](common-issues) and perform the [Troubleshooting steps](troubleshooting-steps). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 10 | **Error(s)**  ``` WARN 9594 sf::RestRequest::httpPerform: Got CURL(0000015547C0CC10) error: Failed to connect to <PROXY_HOST> port 80: Timed out when fetching data from https://[<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>]:443/session/v1/login-request?requestId=<OBFUSCATED>&request_guid=<OBFUSCATED>. Status code: 11, curl error code: 28 ```  **Root cause**:  The client driver was unable to perform the login operation for the given user, due to the request timing out. (curl error code 28 = CURLE\_OPERATION\_TIMEDOUT).  This is likely due to misconfiguration on one or more devices (proxy / security appliance) on the network path between the client driver and Snowflake.  **Resolution scenario**:  Please follow the [Troubleshooting steps](troubleshooting-steps) and work with your sysadmin/network admin to ensure all Snowflake endpoints are reachable from the host you’re running the client driver from. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 11 | **Error(s)**  ``` ERROR [HY000] [Microsoft][Snowflake] (4) REST request for URL https://[<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>]:443/session/v1/login-request?requestId=<OBFUSCATED>&request_guid=<OBFUSCATED> failed: CURLerror (curl_easy_perform() failed) - code=6 msg='Couldn't resolve host name'. ```  **Root cause**: See label-client\_connectivity\_dns\_issues.  **Resolution scenario**: See label-client\_connectivity\_dns\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 12 | **Error(s)**  ``` ERROR [HY000] [Snowflake][Snowflake] (4) REST request for URL https://[<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>]:443/session/v1/login-request?requestId=<OBFUSCATED>&request_guid=<OBFUSCATED> failed: CURLerror (curl_easy_perform() failed) - code=5 msg='Couldn't resolve proxy name' osCode=9 osMsg='Bad file descriptor'. ```  **Root cause**: See label-client\_connectivity\_dns\_issues.  **Resolution scenario**: See label-client\_connectivity\_dns\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| ODBC error 13 | **Error(s)**  ``` [Snowflake][Snowflake] (25) Result download worker error: Worker error: [Snowflake][Snowflake] (4) REST request for URL https://<STAGE>/results/<OBFUSCATED>_02Fmain2Fdata_0_0_8?sv=<OBFUSCATED>&spr=https&se=<OBFUSCATED>&sr=b&sp=r&sig=<OBFUSCATED>&rsce=gzip failed: CURLerror (curl_easy_perform() failed) - code=42 msg='Operation was aborted by an application callback'. ```  **Root cause**: See label-client\_connectivity\_large\_result\_issues.  **Resolution scenario**: See label-client\_connectivity\_large\_result\_issues. |

Expand

Show lessSee more

# Snowflake Connector for Python and SnowSQL errors

|  |  |
| --- | --- |
| Python error 1 | **Error(s)**  ``` SSL validation failed for https://<STAGE>/?accelerate [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:852) ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Python error 2 | **Error(s)**  ``` SSLError: HTTPSConnectionPool(host='<STAGE>', port=443): Max retries exceeded with url: /<OBFUSCATED>/results/<OBFUSCATED>_0/main/data_0_0_1?x-amz-server-side-encryption-customer-algorithm=<OBFUSCATED>&response-content-encoding=gzip&AWSAccessKeyId=<OBFUSCATED>&Expires=<OBFUSCATED>&Signature=<OBFUSCATED> (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')])"))) ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Python error 3 | **Error(s)**  ``` (Caused by ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 407 Request rejected by proxy'))) ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Python error 4 | **Error(s)**  ``` 250001 (n/a): Could not connect to Snowflake backend after 0 attempt(s).Aborting ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Python error 5 | **Error(s)**  ``` snowflake.connector.network.RetryRequest: HTTP 403: Forbidden ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Python error 6 | **Error(s)**  ``` 250003 (n/a): Failed to get the response. Hanging? method: post, url: https://[<SNOWFLAKE_DEPLOYMENT>|<SNOWFLAKE_DEPLOYMENT_REGIONLESS>|<CLIENT_FAILOVER>]:443/session/authenticator-request?request_guid=<OBFUSCATED> ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Python error 7 | **Error(s)**  ``` Retrying (Retry(total=0, connect=None, read=None, redirect=None)) after connection broken by 'ProtocolError('Connection aborted.', RemoteDisconnected ('Remote end closed connection without response'))' ```  **Root cause**:  What this error message means: The client driver was able to connect to the remote end and sent a HTTP request to it, but when attempting to read the response, no data was read from it, indicating that something on the remote end closed the connection.  The most likely cause is a persistent RemoteDisconnected error, which suggests misconfiguration on one or more proxy/security appliances between the client driver and the Snowflake endpoint.  **Resolution scenario**: Please follow the [Troubleshooting steps](troubleshooting-steps) and make sure all Snowflake endpoints are allowed on any intermediary proxy or security appliances you might have. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Python error 8 | **Error(s)**  ``` HTTPSConnectionPool(host='<STAGE>', port=443): Max retries exceeded with url: /<OBFUSCATED>/results/<OBFUSCATED>_0/main/data_0_0_1?x-amz-server-side-encryption-customer-algorithm=<OBFUSCATED>&response-content-encoding=gzip&X-Amz-Algorithm=<OBFUSCATED>&X-Amz-Date=<OBFUSCATED>&X-Amz-SignedHeaders=<OBFUSCATED>&X-Amz-Expires=<OBFUSCATED>&X-Amz-Credential=<OBFUSCATED>&X-Amz-Signature=<OBFUSCATED> (Caused by SSLError(SSLError("bad handshake: SysCallError(-1, 'Unexpected EOF')"))) ```  **Root cause**: See label-client\_connectivity\_ssl\_issues.  **Resolution scenario**: See label-client\_connectivity\_ssl\_issues. |

Expand

Show lessSee more

If the resolution steps do not resolve the issue, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) for further assistance.
