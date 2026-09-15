# Snowpark Migration Accelerator: Validation

To proceed with the validation process, follow the steps outlined below:

1. Copy the `snowpark-checkpoints-output` folder, generated during the collection process, into the validation workload.
   [![Copying collection process output into the validation workload](/static/images/migrations/sma-assets/image(581).png)](/static/images/migrations/sma-assets/image(581).png)
2. Open the validation workload in VS Code to begin the validation process.
   [![Validation Workload](/static/images/migrations/sma-assets/image(582).png)](/static/images/migrations/sma-assets/image(582).png)
3. Generate checkpoints using the `checkpoints.json` file.

   To generate checkpoints you can do one of the following actions:

   - Generate them by accepting the suggested message:

   [![Load found checkpoints message](/static/images/migrations/sma-assets/image(575).png)](/static/images/migrations/sma-assets/image(575).png)

   - Execute the “Snowflake: Load All Checkpoints” command

   [![Load All Checkpoints Command](/static/images/migrations/sma-assets/image(576).png)](/static/images/migrations/sma-assets/image(576).png)

   Once all checkpoints are loaded, your files should appear as follows:

   [![File with checkpoints](/static/images/migrations/sma-assets/image(583).png)](/static/images/migrations/sma-assets/image(583).png)
4. Run the Python file to execute the checkpoints validation process.

When running a Python file that contains validation checkpoints, the validation results will be shown in the copied “snowpark-checkpoints-output” folder as “checkpoints\_validation\_results.json”:

[![Results](/static/images/migrations/sma-assets/image(584).png)](/static/images/migrations/sma-assets/image(584).png)

The “checkpoints\_validation\_results.json” contains the unified results of the validation process.

Copy code

```
{
    "results": [
        {
            "checkpoint_name": "sample$BBVOC7$df1$1",
            "file": "sample.py",
            "line_of_code": 10,
            "result": "PASS",
            "timestamp": "2025-05-05T15:32:29.248917"
        },
        {
            "checkpoint_name": "sample$BBVOC7$df2$1",
            "file": "sample.py",
            "line_of_code": 12,
            "result": "PASS",
            "timestamp": "2025-05-05T15:32:31.137536"
        },
        {
            "checkpoint_name": "sample$BBVOC7$df3$1",
            "file": "sample.py",
            "line_of_code": 17,
            "result": "PASS",
            "timestamp": "2025-05-05T15:32:33.133002"
        }
    ]
}
```

The validation results, as seen above, will contain the comparison result between the PySpark and Snowpark DataFrames.
