# Browser test

For a successful connection to Snowflake, the URLs listed in the Snowflake allowlist should be accessible via the browser. To verify, you should try to access the URLs in your browser. The results of this browser test can help Snowflake understand the possible root causes of your issue.

- For the Snowflake URL, you should be able to access the login page in the browser.
- For a Stage URL, you should expect some sort of 403 error, but still succeed in connecting. See the examples below:
  - AWS stage successful connection example:

    Copy code

    ```
    <Error>
      <Code>AccessDenied</Code>
      <Message>Access Denied</Message>
      <RequestId>5CXSPXCBPY8DDQ0N</RequestId>
      <HostId>
        fQPUOjEOGM2lpG4TWXCwAGfOnuR01LHHzlm6+0rmzC3Zu7geOe4IEwNwIOLLl43Tk183XFJG5pw=
      </HostId>
    </Error>
    ```
  - Azure stage successful connection example:

    Copy code

    ```
    <Error>
      <Code>InvalidQueryParameterValue</Code>
      <Message>
        Value for one of the query parameters specified in the request URI is invalid. RequestId:1c0658d7-e01e-010c-5be8-8023af000000 Time:2022-06-15T18:44:55.1523344Z
      </Message>
      <QueryParameterName>comp</QueryParameterName>
      <QueryParameterValue/>
      <Reason/>
    </Error>
    ```
  - GCP stage successful connection example:

    Copy code

    ```
    <Error>
      <Code>AccessDenied</Code>
      <Message>Access denied.</Message>
      <Details>
        Anonymous caller does not have storage.objects.list access to the Google Cloud Storage bucket.
      </Details>
    </Error>
    ```
  - OCSP URL (`http://ocsp.snowflakecomputing.com/ocsp_response_cache.json`) successful connection example:

    You should see a progress bar for downloading the `ocsp_response_cache.json` file to the location specified in your browser.

    If the test is unsuccessful, you would see an error similar to the following:

    Copy code

    ```
    <Error>
      <Code>AccessDenied</Code>
      <Message>Access Denied</Message>
      <RequestId>YE1ZB5WN693FMJNP</RequestId>
      <HostId>hOZHtpAS4SU8/qsX5vZG/dOlWe33ttwYyCy9zrENWN7V/B38JTxdaCCyA+gePDoDUZ3VNf95Pn0=</HostId>
    </Error>
    ```

After completing these steps, continue with [follow-up actions](/user-guide/client-connectivity-troubleshooting/followup-actions).
