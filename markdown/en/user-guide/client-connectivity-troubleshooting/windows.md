# Windows troubleshooting steps

Follow these steps to identify and confirm that you have a proxy and to gather the proxy host and port numbers that you need for further troubleshooting.

1. Check the proxy settings.

   1. Open the **Settings** menu.
   2. Search for “proxy”, and select **Change proxy settings**.
2. Check the manual proxy configuration.

   1. In **Manual proxy setup**, select the `Use a proxy server` option.
      - If it is `On`, a proxy is currently in use.
      - If it is `Off`, no proxy is being used.
3. Check the automatic proxy configuration.

   1. Under **Automatic proxy setup**, look for `Use setup script`. If it is `On`, a proxy might be configured via a script.
   2. To verify, enter the script URL in your browser. If a file is downloaded, it contains the proxy information.
4. Check the proxy using the Windows `PowerShell`, as follows:

   Copy code

   ```
   $proxyAddr = (Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings').ProxyServer
   $proxyEnable = (Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings').ProxyEnable

   # Output the values
   $proxyAddr
   $proxyEnable
   ```

   For example:

   - If the `proxyAddr` is `my.pro.xy:123` and `proxyEnable` is `0`, the proxy address is `my.pro.xy:123`.
   - If `proxyEnable` is `0`, the proxy is disabled; if it is `1`, the proxy is enabled.
5. Proceed based on the proxy test results:

   - **Proxy found**: Based on these environment variables settings, you can gather the proxy host and port that you will need for [further testing](#label-connectivity-win-proxy).
   - **No proxy found**: If the test for the proxy is negative, continue with [further testing](#label-connectivity-win-noproxy).

## If you have a proxy

After identifying your proxy settings, or if you already know your proxy information, proceed to test the URL that is encountering issues. You should test all URLs in Snowflake’s allowlist thoroughly. At the very least, make sure to test the URL that is causing failures in your connector specifically.

In the Windows `Powershell`, run the following commands, making sure to update the URL in the commands to match the Snowflake URL that you are testing. Also, make sure to update your `PROXY_URL`.

Copy code

```
[Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

$proxy = New-Object System.Net.WebProxy("http://<PROXY:PORT>")
$url = "https://<URL>/"

$req = [Net.HttpWebRequest]::Create($url)
$req.Proxy = $proxy
$req.GetResponse() | Out-Null
$output = [PSCustomObject]@{
  Proxy = $proxy
  URL = $url
  'Issuer' = $req.ServicePoint.Certificate.Issuer
  'Subject' = $req.ServicePoint.Certificate.Subject
}

$output|ConvertTo-Json

Sample expected output:

{
    "Proxy": {
                  "Address": "<IP ADDRESS>"",
                  "BypassProxyOnLocal": false,
                  "BypassList": [
                                ],
                  "Credentials": null,
                  "UseDefaultCredentials": false,
                  "BypassArrayList": [
                                      ]
              },
    "URL": "https://<account>.snowflakecomputing.com"",
    "Issuer": "CN=Amazon, OU=Server CA 1B, O=Amazon, C=US",
    "Subject": "CN=*.us-east-1.snowflakecomputing.com",
    "Cert Start Date": "5/23/2022 8:00:00 PM",
    "Cert End Date": "6/22/2023 7:59:59 PM"
}
```

Observe any references to the proxy in the test results to confirm that the proxy was used during this test. If the connection is successful, examine the issuer information provided in the output.

After completing these steps, continue with [follow-up actions](/user-guide/client-connectivity-troubleshooting/followup-actions).

## If you don’t have a proxy

You should test all URLs in the Snowflake allowlist thoroughly. At the very least, make sure to specifically test the URL that is causing failures in your connector.

1. Open `Powershell`.
2. Run the following commands in `Powershell`, updating the URL in the commands to match the URL that you are testing.

   Copy code

   ```
   [Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
   $url = "https://<URL>/""
   $req = [Net.HttpWebRequest]::Create($url)
   $req.GetResponse() | Out-Null
   $output = [PSCustomObject]@{
     URL = $url
     'Issuer' = $req.ServicePoint.Certificate.Issuer
     'Subject' = $req.ServicePoint.Certificate.Subject
   }
   $output|ConvertTo-Json
   ```

   Sample successful output:

   ```
   {
    "URL": "https://<account>.snowflakecomputing.com"",
    "Issuer": "CN=Amazon, OU=Server CA 1B, O=Amazon, C=US",
    "Subject": "CN=*.us-east-1.snowflakecomputing.com"
   }
   ```

   Sample connection failure output:

   ```
   Exception calling "GetResponse" with "0" argument(s): "Unable to connect to the remote server"
   At line:4 char:1

   + $req.GetResponse() | Out-Null
   + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo     : NotSpecified: (:) [], MethodInvocationException
    + FullyQualifiedErrorId : WebException
   ```

If the connection is successful, examine the issuer information provided in the output.

After completing these steps, continue with [follow-up actions](/user-guide/client-connectivity-troubleshooting/followup-actions).
