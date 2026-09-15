# Step 1: Create the remote service (Google Cloud Function) in the console

This topic provides detailed instructions for creating a Google Cloud Function for use as the remote service for your external function.

## Previous step

[Planning an external function for GCP](/sql-reference/external-functions-creating-gcp-planning)

## Create the Google Cloud Function

Create the function by following Google’s
[instructions to create a Cloud Function](https://cloud.google.com/functions/docs/quickstart-console).

If you are creating the function using the sample Python-language function provided by Snowflake, then choose **Python Quickstart**;
otherwise, choose the appropriate QuickStart based on the language you are using.

As you follow Google’s instructions, make sure to do the following:

1. Specify that the trigger for the function is HTTP.
2. Copy the trigger **URL** to the `Cloud Function Trigger URL` field in your tracking worksheet.
3. In the **Authentication** section, select **Require authentication**.

   The GCP instructions say to select **Allow unauthenticated invocations**. That is acceptable for sample
   functions, including the sample function provided by Snowflake, but most production systems should require authentication.
4. If **Require HTTPS** is not already enabled, then enable it.
5. Click **Save**.
6. Select an appropriate **Runtime**. If you are creating the sample Python function supplied by Snowflake,
   then choose the Python 3.7 runtime.

   Important

   Select the **Runtime** value before you paste in the code.
7. Replace the default code with either the Snowflake sample code or your own custom code. The Snowflake sample code is provided in
   [Sample synchronous Google Cloud Function](#label-external-function-sample-synchronous-google-cloud-function) (in this topic).
8. Make sure that the **Entry point** matches the name of the function (in this case, `echo`).

## Test the Google Cloud Function

After you finish creating the Google Cloud Function, use the **Testing** tab in the console to call the function to make sure that
it works as expected.

For the sample Python function provided by Snowflake, use the following test data (replace any default
data in the **Testing** tab with the data below):

> Copy code
>
> ```
> { "data":
>   [
>     [ 0, 43, "page" ],
>     [ 1, 42, "life, the universe, and everything" ]
>   ]
> }
> ```

The execution results should be similar to:

> Copy code
>
> ```
> {"data":
>   [
>     [0, [43, "page"] ],
>     [1, [42, "life, the universe, and everything"] ]
>   ]
> }
> ```

The results might be displayed in a different format from the example shown above.

If the test succeeded, you now have a Google Cloud Function that you can use as the remote service for your external function.

## Sample synchronous Google Cloud Function

This sample code combines the input parameter values into a single list (array) and returns that list as a single
value of SQL type VARIANT. The code is written in Python 3.7.

This function accepts and returns data in the same format (JSON) that Snowflake sends and reads.

> Copy code
>
> ```
> import json
>
> HTTP_SUCCESS = 200
> HTTP_FAILURE = 400
>
> def echo(request):
>     try:
>         # The list of rows to return.
>         return_value = []
>
>         payload = request.get_json()
>         rows = payload["data"]
>
>         # For each input row
>         for row in rows:
>             # Include the row number.
>             row_number = row[0]
>             # Combine the value(s) in the row into a Python list that will be treated as an SQL VARIANT.
>             row_value = row[1:]
>             row_to_return = [row_number, row_value]
>             return_value.append(row_to_return)
>
>         json_compatible_string_to_return = json.dumps( { "data" : return_value } )
>         return (json_compatible_string_to_return, HTTP_SUCCESS)
>
>     except:
>         return(request.data, HTTP_FAILURE)
> ```

For more information about data formats, see [Remote Service Input and Output Data Formats](/sql-reference/external-functions-data-format#label-external-functions-data-format) .

## Next step

[Step 2: Create the proxy service (Google Cloud API Gateway) in the console](/sql-reference/external-functions-creating-gcp-ui-proxy-service)
