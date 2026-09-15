# MacOS and Linux troubleshooting steps

Follow these steps to identify and confirm that you have a proxy and to gather the proxy host and port numbers that you need for further troubleshooting.

1. Open a new `Terminal` window.
2. Execute the following command to retrieve proxy configuration details specific to your network. Replace `example.com` with the actual hostname you want to test.

   Copy code

   ```
   networksetup -getsecurewebproxy "$(networksetup -listnetworkserviceorder | grep $(route get example.com | grep interface | awk -F: '{print $2}') | awk -FPort: '{print $2}' | awk -F, '{print $1}' | sed 's/^ //g')"
   ```

   Sample output with a proxy configuration

   ```
   Enabled: Yes
   Server: 192.168.21.12
   Port: 3128
   Authenticated Proxy Enabled: 1
   ```

   Sample output without a proxy configuration

   ```
   Enabled: No
   Server:
   Port: 0
   Authenticated Proxy Enabled: 0
   ```
3. Additionally, you can test common environment variables used for proxy settings with the following command:

   Copy code

   ```
   env | grep -i proxy
   ```

   The command returns output similar to the following:

   ```
   http_proxy=http://my.pro.xy:123
   HTTP_PROXY=http://my.pro.xy:123
   HTTPS_PROXY=http://my.pro.xy:123
   https_proxy=http://my.pro.xy:123
   NO_PROXY=localhost,.example.com,.amazonaws.com
   ```

   - **Proxy found**: Based on these environment variables settings, you can gather the proxy host and port that you will need for [further testing](#label-connectivity-mac-proxy).
   - **No proxy found**: If the output is empty, you likely have no environment variables set for a proxy configuration, which needs [further testing](#label-connectivity-mac-noproxy).
   - The `NO_PROXY` defines the hosts that a client can use to connect directly without going through the proxy server.

## If you have a proxy

You can identify the specific URL that is experiencing connectivity issues. While it is beneficial to test all URLs listed in the Snowflake allowlist, you might want to focus on the URL that is directly causing issues in your setup.

Copy code

```
export http_proxy=http://<PROXY_HOST:PROXY_PORT> && export HTTP_PROXY=$http_proxy && export HTTPS_PROXY=$http_proxy && export https_proxy=$http_proxy

curl -v https://URL 2>&1 | tee | grep "Trying\|Connected\|Establish\|CONNECT\|subject\|issuer\|HTTP\|curl"
```

Alternatively, you can pass the proxy settings directly into `curl` (without setting the environment variables first), as shown:

- Unauthenticated proxy

  Copy code

  ```
  curl --proxy “<PROTOCOL>://<HOST>:<PORT>” ..rest of the arguments..
  ```
- Authenticated proxy

  Copy code

  ```
  curl --proxy “<PROTOCOL>://<HOST>:<PORT>” --proxy-user user:pass ..rest of the arguments..
  ```

In the `Terminal`, run the following commands. Update the command with the URL that is causing issues. Replace `<URL>` with the problematic URL. Additionally, replace `<PROXY_URL>` with your proxy information.

Copy code

```
export http_proxy=http://<PROXY_URL> && export HTTP_PROXY=$http_proxy && export HTTPS_PROXY=$http_proxy && export https_proxy=$http_proxy

curl -v https://<URL> 2>&1 | tee | grep "Trying\|Connected\|Establish\|CONNECT\|subject\|issuer\|HTTP\|curl"
```

These commands configure your environment to use the proxy for HTTP and HTTPS requests and attempt to connect to the specified Snowflake URL. It also outputs detailed information about the connection attempt, including any successful connections or errors encountered.

Successful connection example output:

```
➜  curl -v https://<account>.snowflakecomputing.com 2>&1 | tee | grep "Trying\|Connected\|Establish\|CONNECT\|subject\|issuer\|HTTP\|curl"
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying <IP ADDRESS>...
* Connected to <IP ADDRESS> (<IP ADDRESS>) port <PORT> (#0)
* Establish HTTP proxy tunnel to <account>.snowflakecomputing.com:443
> CONNECT <account>.snowflakecomputing.com:443 HTTP/1.1
> User-Agent: curl/7.79.1
< HTTP/1.1 200 Connection established
* Proxy replied 200 to CONNECT request
* CONNECT phase completed!
*  subject: CN=*.us-east-1.snowflakecomputing.com
*  subjectAltName: host "<account>.snowflakecomputing.com" matched cert's "*.us-east-1.snowflakecomputing.com"
*  issuer: C=US; O=Amazon; OU=Server CA 1B; CN=Amazon
> GET / HTTP/1.1
> User-Agent: curl/7.79.1
< HTTP/1.1 302 Found
```

Output analysis:

- “Connected to…” indicates a successful connection to the proxy (<IP ADDRESS>) and the establishment of an HTTP tunnel to Snowflake.
- HTTP status codes like `HTTP/1.1 200 Connection established` followed by `HTTP/1.1 302 Found` suggests a successful to the login page.

After completing these steps, continue with [follow-up actions](/user-guide/client-connectivity-troubleshooting/followup-actions).

## If you don’t have a proxy

In the `Terminal`, run the following command, making sure to update the URL in the commands to match the Snowflake URL that you are testing.

Copy code

```
curl -v https://<URL> 2>&1 | tee | grep "Trying\|Connected\|Establish\|CONNECT\|subject\|issuer\|HTTP\|curl"
```

Successful connection example output:

```
➜  curl -v https://<account>.snowflakecomputing.com 2>&1 | tee | grep "Trying\|Connected\|Establish\|CONNECT\|subject\|issuer\|HTTP\|curl"

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 52.22.29.117:443...
* Connected to <account>.snowflakecomputing.com (52.22.29.117) port 443 (#0)
*  subject: CN=*.us-east-1.snowflakecomputing.com
*  subjectAltName: host "<account>.snowflakecomputing.com" matched cert's "*.us-east-1.snowflakecomputing.com"
*  issuer: C=US; O=Amazon; OU=Server CA 1B; CN=Amazon
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0> GET / HTTP/1.1
< HTTP/1.1 302 Found
```

This output demonstrates a successful connection, indicating that your system can reach and communicate with the Snowflake server.

Connection failure example:

```
➜  curl -v https://<account>.snowflakecomputing.com 2>&1 | tee | grep "Trying\|Connected\|Establish\|CONNECT\|subject\|issuer\|HTTP\|curl"
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 52.22.29.117:443...
*   Trying 3.222.247.13:443...
*   Trying 54.81.51.170:443...
curl: (7) Failed to connect to <account>.us-east-1.snowflakecomputing.com port 443 after 3139 ms: Connection refused
```

After completing these steps, continue with [follow-up actions](/user-guide/client-connectivity-troubleshooting/followup-actions).
