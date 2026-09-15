# Troubleshoot Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic describes the steps to troubleshoot the Openflow components.

## Openflow BYOC troubleshooting

### BYOC custom ingress troubleshooting

For help with BYOC custom ingress, see [Custom ingress troubleshooting](/user-guide/data-integration/openflow/setup-openflow-byoc-custom-ingress#label-openflow-byoc-custom-ingress-troubleshooting).

### General BYOC troubleshooting

If any part of a deployment, connector, or runtime is causing problems,
you can use a built-in tool to generate a diagnostic bundle. This bundle
includes the information necessary to keep your Openflow BYOC deployment
secure while allowing the [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) team to
troubleshoot the issue. To share the diagnostic bundle with [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support), attach it to your support case.

1. From the AWS Console UI for EC2, right-click on the **openflow-agent-{deployment-key}** instance with your Deployment Key.
2. In the context menu, click the **Connect** button.
3. Switch from **EC2 Instance Connect** to **Connect using EC2 Instance Connect Endpoint**. Leave the default **EC2 Instance Connect Endpoint** in place.
4. Click the **Connect** button. A new browser tab or window will appear with a command-line interface.
5. Run `./diagnostics.sh` from this browser-based CLI. Follow a few simple prompts to confirm that you want to create the bundle, and then optionally create a shareable link. The diagnostic utility will upload the file to an S3 bucket created for the Deployment using the Deployment Key. For example, `s3://byoc-tf-state-{deployment-key}/diagnostics/openflow_20250131123456.tar.gz`

With the pre-signed URL, you can safely share temporary access to the
diagnostic bundle with the Snowflake team for up to 1 hour. Your S3 bucket and all of its
contents remain private.
