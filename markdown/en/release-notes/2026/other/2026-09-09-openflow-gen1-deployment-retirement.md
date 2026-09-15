# Sep 09, 2026: Openflow gen 1 deployment creation retired

You can no longer create new first generation (gen 1) Openflow deployments (BYOC or Snowflake).
All new deployments are second generation (gen 2), created with `CREATE OPENFLOW DEPLOYMENT` or
the Openflow UI.

Existing gen 1 deployments continue to work unchanged, and you can still create new gen 1 runtimes
on an existing gen 1 deployment. Only gen 1 **deployment** creation is affected.

For a comparison of gen 1 and gen 2, see
[Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations). Migration from gen 1 to gen 2
is available separately in Private Preview; contact your Snowflake account representative to be
included.
