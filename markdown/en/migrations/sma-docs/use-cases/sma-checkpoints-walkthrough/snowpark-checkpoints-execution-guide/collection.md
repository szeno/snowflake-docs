description:
:   This page outlines the step-by-step process for the collection procedure.

# Snowpark Migration Accelerator: Collection

To follow the collection process, please proceed with the steps outlined below:

1. Open the collection workload in VS Code to begin the process.
   [![Collection Workload](/static/images/migrations/sma-assets/image(574).png)](/static/images/migrations/sma-assets/image(574).png)
2. Generate checkpoints using the `checkpoints.json` file.

To generate checkpoints, you can perform one of the following actions:

1. Generate checkpoints by accepting the suggested message:
   [![Load found checkpoints message](/static/images/migrations/sma-assets/image(575).png)](/static/images/migrations/sma-assets/image(575).png)
2. Execute the “Snowflake: Load All Checkpoints” command:

   [![Load All Checkpoints Command](/static/images/migrations/sma-assets/image(576).png)](/static/images/migrations/sma-assets/image(576).png)

   Once all checkpoints are successfully loaded, your files should appear as shown below:

   [![File with checkpoints](/static/images/migrations/sma-assets/image(577).png)](/static/images/migrations/sma-assets/image(577).png)
3. Run the Python file to execute the checkpoints collection process.

When running a Python file that includes checkpoints, a folder named `snowpark-checkpoints-output` will be created, containing the collection results.

[![Collection results output folder](/static/images/migrations/sma-assets/image(578).png)](/static/images/migrations/sma-assets/image(578).png)

The `checkpoints_collection_results.json` file contains the consolidated results of the collection process.

Copy code

```
{
  "results": [
    {
      "timestamp": "2025-05-05 15:06:43",
      "file": "sample.py",
      "line_of_code": 57,
      "checkpoint_name": "sample$BBVOC7$df1$1",
      "result": "PASS"
    },
    {
      "timestamp": "2025-05-05 15:06:53",
      "file": "sample.py",
      "line_of_code": 57,
      "checkpoint_name": "sample$BBVOC7$df2$1",
      "result": "PASS"
    },
    {
      "timestamp": "2025-05-05 15:06:58",
      "file": "sample.py",
      "line_of_code": 57,
      "checkpoint_name": "sample$BBVOC7$df3$1",
      "result": "PASS"
    }
  ]
}
```

The `snowpark-checkpoints-output` folder should be copied into the validation workload to grant access to the collection results. For details on how to proceed with the validation process, refer to the [Validation Section](https://app.gitbook.com/o/-MB4z_O8Sl--Tfl3XVml/s/6on4bNAZUZGzMpdEum8X/~/changes/499/use-cases/sma-checkpoints-walkthrough/snowpark-checkpoints-execution-guide/validation).
