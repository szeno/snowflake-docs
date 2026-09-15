description:
:   Using checkpoints feature within SMA.

# Snowpark Migration Accelerator: SMA Checkpoints walkthrough

The Snowpark Migration Accelerator provides the SMA-Checkpoints feature, this feature goal is to be used within the checkpoints feature of the Snowflake Extension. SMA Checkpoints can be either enabled or disabled in order to generate a file named checkpoints.json which can be used by the extension to insert the checkpoints in the corresponding location based on the analysis made by the SMA.

[![SMA-Checkpoints Workflow](/static/images/migrations/sma-assets/image(585).png)](/static/images/migrations/sma-assets/image(585).png)

## Feature limitations

1. Dbx notebooks are not supported by checkpoints.

## Known Issues

1. Jupyter notebooks checkpoints are being generated in wrong locations, it is possible that those checkpoints do not work as expected.
2. Entry points by imports are not being identified.

**Note:** This guide is closely related to the Snowpark Checkpoints framework. For more information, see [Snowpark Checkpoints](/developer-guide/snowpark/python/snowpark-checkpoints-library).
