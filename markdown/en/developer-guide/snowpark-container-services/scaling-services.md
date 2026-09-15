# Scaling services

As your service workload grows or shrinks, you want Snowflake to automatically adjust the number of
running service instances to match demand. Scaling up ensures your service can handle increased traffic
without degradation. Scaling down reduces resource consumption and cost when demand is low. You can
also configure automatic suspension so that an idle service doesn’t consume compute pool resources.

Snowflake recommends using autoscaling policies. Policies give you fine-grained control over scaling
behavior by letting you define conditions based on metrics such as CPU utilization, memory usage, and
ingress connection rate. You can configure separate rules for scaling up, scaling down, and suspending
a service, and you can combine multiple metric conditions to match your application’s specific
workload patterns.

For simple CPU-based autoscaling with minimal configuration, you can use `MIN_INSTANCES` and `MAX_INSTANCES`.
This is described in the [CPU-based autoscaling](#label-spcs-working-with-services-multiple-services-autoscaling) section below.
Autoscaling policies take priority over CPU-based autoscaling when both are configured.

If you configure both an autoscaling policy and `AUTO_SUSPEND_SECS`, both mechanisms operate
independently. Either can trigger suspension, whichever condition is met first.

Note

Autoscaling applies only to services and not job services.

## Autoscaling using policies

These autoscaling capabilities are based on metrics: Snowflake-provided [platform metrics](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-available-platform-metrics) or [custom metrics](/developer-guide/snowpark-container-services/monitoring-services#label-monitoring-services-application-metrics) that your application (service) can emit. You configure autoscaling policies in your service specification directing Snowflake to take specific autoscaling actions. Some examples include:

- **Scale up** service instances when the average CPU core utilization exceeds 0.8 cores (that is, when the service containers keep a core busy
  more than 80% of the time).
- **Scale down** service instances if all of the following metric conditions are true:

  - The ingress requests per service instance are fewer than two requests per second.
  - The CPU core utilization is below 0.3 (that is, each service instance keeps a core busy less than 30% of the time).
- **Suspend** a service if no ingress requests are received for a five-minute period.

You can also configure similar autoscaling policies by using custom metrics that your application emits.

### Specifying autoscaling policies

You configure autoscaling policies in your [service specification](/developer-guide/snowpark-container-services/specification-reference) by adding the `spec.resourceManagement.autoScalingPolicies` field.

The general syntax for specifying autoscaling policies in your service specification is as follows:

Copy code

```
spec:
  containers:
    ...
  endpoints:
    ...
  resourceManagement:
    autoScalingPolicies:
     scaleUp:                            # optional
        anyConditions:
        - metricCondition:
            metricName: <metric-name>
            labels:                      # optional
              <key:value>
              ...
            aggregationType: [min | max | avg]
            stabilizationPeriodSecs: <# of secs>
            targetScaling:               # optional
              targetValue: <target-value>
            stepScaling:                 # optional
              adjustmentType: changeInstanceCount | exactInstanceCount | percentChangeInstanceCount  # required
              scalingSteps:              # required
              - lowerBound: <metric-value>
                upperBound: <metric-value>
                targetAdjustment: <adjustment-value>
              - ...
        - metricCondition:
            ...
     scaleDown:                          # optional
        allConditions:
        - metricCondition:
        ...
     suspend:                            # optional
        allConditions:
        - metricCondition:
        ...
    ...
```

The following list provides details from the syntax:

- `autoScalingPolicies`: You can describe a combination of `suspend`, `scaleUp`, or `scaleDown` policies, but at most one of each type of policy.

  - For the `scaleUp` policy, use `anyConditions` to specify a list of metrics conditions. Any one of these conditions must be true for
    Snowflake to apply the specified autoscaling. This applies only for `scaleUp` policies.
  - For the `scaleDown` and `suspend` policies, use `allConditions` to specify a list of metrics conditions. All these conditions
    must be true for Snowflake to apply the specified autoscaling.
- `metricCondition`: Each one of these fields describes a metric condition:

  - `metricName`: The [name of the metric](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-available-platform-metrics) to monitor.
    For example, `network.ingress.cps` platform metric monitors ingress connections per second to the service’s public endpoints.
  - `labels` (optional): In the realm of metrics (like in Prometheus or other observability systems), a *metric* represents a type of measurement;
    for example, the platform metric `network.ingress.cps` represents the ingress connections per second to a service’s public endpoints. In some
    cases you might need to filter the metric further. For example, if the service exposes multiple public endpoints and you are interested in
    connections per second to a specific endpoint. This is where *labels* are useful.

    Each label is a key-value pair. For the `network.ingress.cps` metric, you can limit checking this metrics to a specific endpoint by adding
    the following key-value pair:

    Copy code

    ```
    labels:
      snow.endpoint.name: <public-endpoint-name>
    ```

    You can specify one or more such labels. For a given metric, you can add one or more attributes from the associated
    resource\_attributes as labels. You can query the event table to find resource\_attributes that are associated with a metric. The same information is
    also provided in the [Available platform metrics](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-available-platform-metrics) table.

    Note

    When you add a label, we recommend that you query the event table and verify that the resource\_attributes associated with the
    metric include the specific label. You can also use the [Available platform metrics](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-available-platform-metrics)
    table to find a list of valid labels for each metric. If your specified label doesn’t match, you don’t get an error and the
    condition is never triggered.
  - `aggregationType`: It can be `min`, `max`, or `avg`. For more information, see [How autoscaling works](#label-autoscaling-policy-how-it-works).
  - `stabilizationPeriodSecs`: It refers to the duration in seconds that Snowflake should monitor the metrics before applying the scaling action. For example, to define a metrics
    condition to suspend the service if there are no ingress connections for a five-minute period, specify 300 seconds as the
    stabilization period.
  - Scaling options: You must specify one of the scaling options: `targetScaling` or `stepScaling`. Based on the scaling option, Snowflake decides how to interpret the observed aggregated metrics and what scaling action to take. For more information, see [How autoscaling works](#label-autoscaling-policy-how-it-works).

### How autoscaling works

Suppose you want your service to autoscale based on the `network.ingress.cps` [platform metric](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-available-platform-metrics). It refers to ingress connections per second to a service endpoint.

After you do the necessary configuration and the service is running, Snowflake periodically (currently every 30 seconds) does the following:

1. Compare current metric values against the target:

   1. Collect metric values: Snowflake polls each service instance and collects data for the specified `network.ingress.cps` metric. For example, suppose your service exposes one endpoint. If you have three instances on this service running, Snowflake collects three data points every 30 seconds: one connections-per-second value per instance.
   2. Aggregate metric values: Snowflake aggregates the collected data using the specified `aggregationType`: min, max, or avg.
   3. Compare aggregated metric values against a target: The target is defined in one of the scaling options (`targetScaling` or `stepScaling`) you define in the service specification. Snowflake stores the comparison result, which includes the determination whether the scaling is needed and recommended instance count that Snowflake derives from the aggregated metric value.
2. Review the comparison results across the `stabilizationPeriod` to determine if scaling is needed. For scaling to happen, three criteria must be met:

   1. All the periodic evaluations over the stabilization period must indicate scaling is needed.
   2. The service properties `current_instances` and `target_instances` must be equal. When the current and target instance values are not equal, Snowflake is either in the process of shutting down or actively scaling the service up or down. Autoscaling is applied only when service is not already in the process of scaling. You can check the service properties using the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) command.
   3. It must be at least 2 minutes since the last scaling action was taken on this service.

   If all preconditions for scaling are met, Snowflake will set the `target_instances` service property to the maximum recommended instance count computed within the stabilization period.

   For example, if the stabilization period is set to 300 seconds, Snowflake records 10 comparison results, one per 30 seconds interval. Snowflake then makes an autoscaling decision based on these results and the scaling option defined in the service specification. For more information, see [Scaling options](#label-autoscaling-policy-target-step-scaling).

#### Scaling options

Snowflake makes an autoscaling decision based on observed aggregated metric values and the scaling option (target scaling or step scaling) defined in the service specification. Each `metricCondition` must specify one scaling option: `metricCondition.targetScaling` or `metricCondition.stepScaling`.

##### `targetScaling`

In `targetScaling` Snowflake scales a service instance count proportional to the observed aggregated metric values relative to the target value (`targetScaling.targetValue`) in the service specification using the following scaling criteria:

- For `scaleDown` and `suspend` policies, all the observed aggregated values should be less than or equal to the specified `targetValue`.
- For `scaleUp` policies, all the observed aggregated values should be greater than or equal to the specified `targetValue`.

When the scaling criteria is met, Snowflake computes a proportional recommended target instances using the following formula and sets the `target_instances` service property:

```
recommended-instance-count = ceil( current-instance-count * aggregated-observed-metric-value / targetValue )
```

For example, suppose the following:

- The current service instance count is 3.
- In the scale-up policy the target metric value (`targetScaling.targetValue` in the specification) is 2. This is the target value against which Snowflake compares the observed aggregated metric values.
- The aggregate of the observed metric values is 4.

Then, recommended instance count is `3 * 4 / 2 = 6`. The recommended instance count is double the current instance count, because the observed metric is double the target. Snowflake records this recommended instance count for this specific period in the stabilization window.

For more examples, see [Scale-up policy examples](#label-autoscaling-policy-scale-up-autoscaling-policy-examples).

##### `stepScaling`

`stepScaling` offers flexibility by letting you specify multiple ranges (instead of a target value that you specify in target scaling) for comparing observed aggregated metric values. You can scale the service instance count by different amounts based on the range in which the observed aggregated metrics falls.

Step scaling also lets you specify the `adjustmentType` field to specify the scaling amount using one of the following values: `changeInstanceCount`, `percentChangeInstanceCount`, or `exactInstanceCount`.

Note

Step scaling is supported only for `scaleUp` and `scaleDown` auto-scaling policies. It is not applicable for `suspend` auto-scaling policies, therefore not supported.

In describing `stepScaling`, you specify the following:

- `scalingSteps`: This is a list of one or more ranges. Each range provides a lower and upper bound for the observed aggregated metric values.
- `adjustmentType`: Specifies how to interpret the specified `targetAdjustment` value. It can be `changeInstanceCount`, `percentChangeInstanceCount`, or `exactInstanceCount`. For example:

  - In the following `scaleUp` policy, the `stepScaling` sets `adjustmentType` to `changeInstanceCount` and sets `targetAdjustment` to 1. This scales the number of service instances by one.

    Copy code

    ```
    ...
    scaleUp:
      allConditions:
      - metricCondition:
    metricName: container.memory.usage
    ...
    stepScaling:
      adjustmentType: changeInstanceCount
      scalingSteps:
      - lowerBound: 20971520
        upperBound: 31457280
        targetAdjustment: 1
      - ...
    ```
  - In the following `scaleUp` policy, the `stepScaling` sets `adjustmentType` to
    `percentChangeInstanceCount` and sets `targetAdjustment` to 25 and 50 in the scaling steps.
    This scales the number of service instances by 25 percent and 50 percent respectively, depending on the range in which the observed aggregated metrics falls.

    Copy code

    ```
    ...
    scaleUp:
      anyConditions:
      - metricCondition:
    metricName: container.cpu.usage
    ...
    stepScaling:
      adjustmentType: percentChangeInstanceCount
      scalingSteps:
      - lowerBound: 0.6
        upperBound: 0.8
        targetAdjustment: 25
      - lowerBound: 0.8
        upperBound: 2
        targetAdjustment: 50
    ```
  - In the following `scaleUp` policy, the `stepScaling` sets `adjustmentType` to
    `exactInstanceCount` and sets `targetAdjustment` to 5 and 10 in the scaling steps.
    This sets the target instance count to the provided `targetAdjustment` values 5 and 10, depending on the range in which the observed aggregated metrics falls.

    Copy code

    ```
    ...
      scaleUp:
        anyConditions:
        - metricCondition:
      metricName: container.cpu.usage
      ...
      stepScaling:
        adjustmentType: exactInstanceCount
        scalingSteps:
        - lowerBound: 0.6
          upperBound: 0.8
          targetAdjustment: 5
        - lowerBound: 0.8
          upperBound: 2
          targetAdjustment: 10
    ```

  Note

  In case of `changeInstanceCount` and `percentChangeInstanceCount`, the up or down scaling depends on whether it is `scaleUp` or `scaleDown` policy.

### Suspend policy examples

Suspending services when they aren’t in use helps you reduce costs. Currently, you can suspend a service in the following ways:

- Setting the AUTO\_SUSPEND\_SECS property during [CREATE SERVICE](/sql-reference/sql/create-service)
  or [ALTER SERVICE](/sql-reference/sql/alter-service).
  This property defines the idle duration after which Snowflake automatically suspends the service. For more information, see [Suspending a service](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-suspend-service).
- Explicitly suspend the service by calling [ALTER SERVICE … SUSPEND](/sql-reference/sql/alter-service).

You can also define auto-suspend policies by using metrics. These metrics can be Snowflake-provided [platform metrics](/developer-guide/snowpark-container-services/monitoring-services#label-monitoring-services-platform-metrics)
or [custom metrics](/developer-guide/snowpark-container-services/monitoring-services#label-monitoring-services-application-metrics)
that your service emits. The following examples show auto-suspension policies that use platform metrics.

Note

- In the [CREATE SERVICE](/sql-reference/sql/create-service) command, the `AUTO_SUSPEND_SECS` property lets you specify only the
  stabilization period. If there is no activity during this period, Snowflake suspends the service. In contrast, the autoscaling policy
  offers greater flexibility; you choose a metric and a threshold to determine when to suspend the service.
- When a request is received for a suspended service, Snowflake automatically resumes the service unless auto resume is explicitly
  disabled. For more information, see [CREATE SERVICE](/sql-reference/sql/create-service).

#### Example 1: Define a suspend autoscaling policy

The following example specifies one `suspend` autoscaling policy, based on one metric condition (`network.ingress.cps`). This example directs Snowflake
to suspend a service if there are no ingress connections to the service’s public endpoints in a 5-minute (300 seconds) period:

Copy code

```
spec:
  containers:
  ...
  endpoints:
  ...
  resourceManagement:
    autoScalingPolicies:
      suspend:
        allConditions:
        - metricCondition:
            metricName: network.ingress.cps
            aggregationType: max
            stabilizationPeriodSecs: 300
            targetScaling:
              targetValue: 0.0
```

The preceding `suspend` autoscaling policy specifies one metric condition that is based on the `network.ingress.cps` platform metric. This metric
tracks the number of ingress connections per second to the service’s endpoints; these include connections both for public ingress or
connections from service functions, but not service-to-service connections.

Periodically (currently, every 30 seconds), the autoscaling policy evaluator performs the following tasks:

1. Applies the specified aggregation (`max`) to the collected metric values.
2. Compares the aggregate value with the `targetValue` and stores the comparison result (true/false). For the suspend policy, the
   aggregated value must be less than or equal to the `targetValue`.

   For the specified 300-seconds stabilization period, Snowflake will have 10 such aggregated values, assuming Snowflake samples every 30
   seconds.
3. Snowflake examines the stored comparisons, and if all comparisons in the stabilization period meet the scaling criteria (all values are true), Snowflake suspends the service.

#### Example 2: Define a suspend autoscaling policy with an optional label

The following example specifies one `suspend` autoscaling policy that is the same as example 1, with the addition of a label:

Copy code

```
spec:
  containers:
  ...
  endpoints:
  ...
  resourceManagement:
    autoScalingPolicies:
      suspend:
        allConditions:
        - metricCondition:
            metricName: network.ingress.cps
            labels:
              snow.endpoint.name: echoendpoint
            aggregationType: max
            stabilizationPeriodSecs: 300
            targetScaling:
              targetValue: 0.0
```

A label is a key:value pair. In the preceding policy, `snow.endpoint.name` is a label and its value, `echoendpoint`, identifies an endpoint
exposed by the service.

The details about how the autoscaling policy evaluator works, as explained in example 1, apply to this example, except the metric condition
applies only to the specific endpoint you provided in the label. For example, if your service has two endpoints and runs on four
instances, there are eight endpoints to poll metrics from. However, if you add a label that identifies the endpoint, the metrics policy
evaluator polls Snowpark Container Services’ metric collector every 30 seconds for the specified metric from only the four labeled
endpoints.

The following example again shows a `suspend` autoscaling policy, but uses another platform metric `container.cpu.usage`. It is a container
metric that tracks CPU core utilization by the service containers:

Copy code

```
spec:
  containers:
  ...
  endpoints:
  ...
  resourceManagement:
        autoScalingPolicies:
          suspend:
            allConditions:
            - metricCondition:
                metricName: "container.cpu.usage"
                labels:
                  "snow.service.container.name": "echo"
                aggregationType: max
                stabilizationPeriodSecs: 300
                targetScaling:
                  targetValue: 0.01
```

The details about how the autoscaling policy evaluator works, as explained in the suspend autoscaling example 1, apply to this example. Except,
the metric condition applies only to the specific container you provided in the label. For example, if your service has two containers and
runs with four instances, there are eight containers to poll metrics from. However, the label identifies a specific container. Therefore,
the metrics policy evaluator polls Snowpark Container Services metric collector for the specified metric from only the
four containers.

#### Example 3: Define a suspend autoscaling policy using multiple platform metrics

The following example specifies one `suspend` autoscaling policy with two metrics conditions. For this auto-suspend policy, both metric
conditions must be true for Snowflake to suspend the service:

Copy code

```
spec:
  containers:
  ...
  endpoints:
  ...

  resourceManagement:
    autoScalingPolicies:
      suspend:
        allConditions:
        - metricCondition:
            metricName: network.ingress.connections.active
            labels:
              snow.endpoint.name: echoendpoint
            aggregationType: max
            stabilizationPeriodSecs: 300
            targetScaling:
              targetValue: 0.0
        - metricCondition:
            metricName: container.cpu.usage
            labels:
              "snow.service.container.name": "main"
            aggregationType: max
            stabilizationPeriodSecs: 300
            targetScaling:
              targetValue: 0.2
```

The details about how the autoscaling policy evaluator works, as explained in example 1, apply to this example. For this auto-suspend policy, both metric conditions must be true for Snowflake to suspend the service.

Note

When you configure a suspension policy based on the connection to the service endpoints, you should specify both
`network.ingress.connections.active` and `network.ingress.cps` metric conditions for the following reasons:

- `network.ingress.connections.active`: Represents currently active connections.
- `network.ingress.cps`: Represents new incoming connections per second.

`metricConditions` for both of them ensure that new connections and existing connections are checked by the auto-suspension.

### Scale-down policy examples

You can automatically scale a service by setting `MIN_INSTANCES` and `MAX_INSTANCES` when you create a service. Snowflake automatically
scales up or down the service based on CPU usage. For more information, see
[Enabling autoscaling](#label-spcs-working-with-services-enabling-autoscaling). You can also use autoscaling policies in the service
specification.

Scale-down policies are specified in much the same way as is described in the previous section for suspend policies. The only change you must make is to
replace `suspend` with `scaleDown` in `autoScalingPolicies`. The main difference between scale-down and suspend policies is that a scale-down policy lets Snowflake reduce the number of service
instances only down to the `MinInstances` value specified when you create the service. For more information, see [CREATE SERVICE](/sql-reference/sql/create-service). The number of instances will never
reach zero. In contrast, a suspend policy reduces the number of running service instances all the way to zero. This difference can be
important, as it takes time to start a service, so you typically want to be more careful about when to suspend. If you scale down too much,
the existing instances can handle the extra load while the system adds more instances to your service to handle the load.

### Scale-up policy examples

Scale up increases the number of service instances. In a scale-up policy, the metric condition is true when the aggregated value is greater than or equal to the `targetValue`. Also, if
there are multiple conditions, any one can be true, in contrast to suspend and scale-down which require all metricConditions to be true.

Copy code

```
spec:
  containers:
  ...
  endpoints:
  ...
  resourceManagement:
    autoScalingPolicies:
      scaleUp:
        anyConditions:
        - metricCondition:
            metricName: container.cpu.usage
            aggregationType: avg
            stabilizationPeriodSecs: 60
            targetScaling:
              targetValue: 1.0
        - metricCondition:
            metricName: container.memory.usage
            aggregationType: min
            stabilizationPeriodSecs: 120
            targetScaling:
              targetValue: 1234567
```

The preceding `scaleUp` autoscaling policy specifies two metric conditions that are based on the `container.cpu.usage` and `container.memory.usage`
platform metrics. This metric tracks the CPU core utilization and memory usage by the service containers.

Periodically (currently, every 30 seconds), the autoscaling policy evaluator performs the following tasks:

1. Polls the Snowpark Container Services’s metric collector for the specified metrics, and then
   collects the metric values for the running service instances.
2. Applies the specified aggregation:

   - Average of the CPU utilization.
   - Minimum memory usage.
3. Compares these aggregated values with the corresponding `targetValue`, and then stores the comparison
   result (true/false). For the scale up policy, the aggregated value must be greater than or equal
   to the `targetValue`.
4. Snowflake examines the stored comparisons. If all comparisons in the stabilization period meet
   the scaling criteria, Snowflake scales up the service, meaning a new service instance is started.

Instead of specifying `targetScaling`, you can specify `stepScaling` to scale the service instance count by a different amount based on the range in which the observed aggregated metrics falls. For more information, see [Scaling options](#label-autoscaling-policy-target-step-scaling).

For example, let us replace the `targetScaling` by `stepScaling` in the first `metricCondition` of the preceding `scaleUp` policy. The revised autoscaling policy is shown:

Copy code

```
spec:
  containers:
  ...
  endpoints:
  ...
  resourceManagement:
    autoScalingPolicies:
      scaleUp:
        anyConditions:
        - metricCondition:
            metricName: container.cpu.usage
            aggregationType: avg
            stabilizationPeriodSecs: 60
            stepScaling:
              adjustmentType: percentChangeInstanceCount
              scalingSteps:
              - lowerBound: 0.6
                upperBound: 0.8
                targetAdjustment: 25
              - lowerBound: 0.8
                upperBound: 2
                targetAdjustment: 50
        - metricCondition:
            metricName: container.memory.usage
            aggregationType: min
            stabilizationPeriodSecs: 120
            targetScaling:
              targetValue: 1.0
```

In the `scaleUp` policy, for the first `metricCondition`, the `stepScaling` sets `adjustmentType` to `percentChangeInstanceCount` and sets `targetAdjustment` to 25 and 50 in the scaling steps. This scales the number of service instances by 25 percent and 50 percent respectively, depending on the range in which the observed aggregated metrics falls.

### Multiple policy examples

In a service specification, you can define multiple autoscaling policies. For example, you can add automatic suspension, scale up, and scale
down metric-based policies for the service.

In the following service specification fragment, the `resourceManagement` section defines the following two autoscaling policies:

- Scale up the service based on two metrics conditions. When any one of these conditions (`anyConditions`) is true, Snowflake scales up the
  service.

  - Metric condition 1 specifies the `container.cpu.usage` metric. Scale up the service if the average utilization of CPU cores that are used is greater
    than or equal to 1.0.
  - Metric condition 2 specifies the `container.memory.usage` metric. Scale up the service if minimum memory usage is greater than or
    equal to the `targetValue` 1234567 bytes.
- Scale down the service based on the `container.memory.usage` metric. When minimum memory usage is less than or
  equal to the `targetValue`, 345212312 bytes.

Here is the service specification:

Copy code

```
spec:
  containers:
  ...
  endpoints:
  ...
  resourceManagement:
    autoScalingPolicies:
      scaleUp:
        anyConditions:
        - metricCondition:
            metricName: container.cpu.usage
            aggregationType: avg
            stabilizationPeriodSecs: 60
            targetScaling:
              targetValue: 1.0
        - metricCondition:
            metricName: container.memory.usage
            aggregationType: min
            stabilizationPeriodSecs: 120
            targetScaling:
              targetValue: 1234567
      scaleDown:
       allConditions:
       - metricCondition:
           metricName: container.memory.usage
           containerName: main
           aggregationType: min
           stabilizationPeriodSecs: 120
           targetScaling:
             targetValue: 345212312
```

Note

In case of a conflict, where multiple autoscaling policies evaluate to true, Snowflake takes a single action by using the scale up, suspend, and
scale down in priority order. For example, if both suspend and scale down policies evaluate to true, Snowflake suspends the service.

Instead of specifying `targetScaling`, you can specify `stepScaling` to scale the service instance count by a different amount based on the range in which the observed aggregated metrics falls. For more information, see [Scaling options](#label-autoscaling-policy-target-step-scaling).

For example, let us update the `scaleDown` policy in the preceding example by replacing the `targetScaling` by `stepScaling`. The revised autoscaling policy is shown:

Copy code

```
scaleDown:
  allConditions:
  - metricCondition:
      metricName: container.memory.usage
      containerName: main
      aggregationType: min
      stabilizationPeriodSecs: 120
      stepScaling:
        adjustmentType: exactInstanceCount
        scalingSteps:
        - lowerBound: 20971520
          upperBound: 31457280
          targetAdjustment: 1
        - lowerBound: 31457280
          upperBound: 41943040
          targetAdjustment: 3
```

In the `scaleDown` policy, the `stepScaling` sets `adjustmentType` to `exactInstanceCount` and sets `targetAdjustment` to 1 and 3 in the scaling steps. This scales the number of service instances by one and three respectively, depending on the range in which the observed aggregated metrics falls.

## CPU-based autoscaling

By default, Snowflake runs one instance of the service in the specified compute pool.
To manage heavy workloads, you can run multiple service instances by setting the MIN\_INSTANCES and MAX\_INSTANCES properties, which specify the minimum number of instances of the service to start with and the maximum instances Snowflake can scale to when needed.

**Example**

Copy code

```
CREATE SERVICE echo_service
   IN COMPUTE POOL tutorial_compute_pool
   FROM @tutorial_stage
   SPECIFICATION_FILE='echo_spec.yaml'
   MIN_INSTANCES=2
   MAX_INSTANCES=4;
```

When multiple service instances are running, Snowflake automatically
provides a load balancer to distribute the incoming requests.

Snowflake does not consider the service to be READY until at least two instances are available. While the service is not ready, Snowflake blocks access to it, meaning that associated service functions or ingress requests are denied until readiness is confirmed.

In some cases, you might want Snowflake to consider the service ready (and forward incoming requests) even if fewer than the specified minimum instances are available. You can achieve this by setting the MIN\_READY\_INSTANCES property.

Consider this scenario: During maintenance or a rolling service upgrade, Snowflake might terminate one or more service instances. This could lead to fewer available instances than the specified MIN\_INSTANCES, which prevents the service from entering the READY state. In these cases, you can set MIN\_READY\_INSTANCES to a value smaller than MIN\_INSTANCES to ensure that the service can continue to accept requests.

**Example**

Copy code

```
CREATE SERVICE echo_service
   IN COMPUTE POOL tutorial_compute_pool
   FROM @tutorial_stage
   SPECIFICATION_FILE='echo_spec.yaml'
   MIN_INSTANCES=2
   MAX_INSTANCES=4
   MIN_READY_INSTANCES=1;
```

For more information, see [CREATE SERVICE](/sql-reference/sql/create-service).

### How CPU-based autoscaling works

To configure Snowflake to autoscale the number of service instances running, set the MIN\_INSTANCES and MAX\_INSTANCES parameters in the CREATE SERVICE command. You can also use ALTER SERVICE to change these values. Autoscaling occurs when the specified MAX\_INSTANCES is greater than MIN\_INSTANCES.

Snowflake starts by creating the minimum number of service instances on the specified compute pool. Snowflake then scales up or scales down the number of service instances based on an 80% CPU resource requests. Snowflake continuously monitors CPU utilization within the compute pool, aggregating the usage data from all currently running service instances.

When the aggregated CPU usage (across all service instances) surpasses 80%, Snowflake deploys an additional service instance within the compute pool. If the aggregated CPU usage falls below 80%, Snowflake scales down by removing a running service instance. Snowflake uses a five-minute stabilization window to prevent frequent scaling. The `target_instances` service property reports the target number of service instances that Snowflake is scaling towards.

Note the following scaling behaviors:

- The scaling of service instances is constrained by the MIN\_INSTANCES and MAX\_INSTANCES parameters configured for the service.
- If scaling up is necessary and the compute pool nodes lack the necessary resource capacity to start up another service instance, compute pool autoscaling can be triggered. For more information, see
  [Autoscaling of compute pool nodes](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-how-auto-scaling-works).
- If you specify the MAX\_INSTANCES and MIN\_INSTANCES parameters when creating a service but don’t specify the CPU and memory requirements for your service instance in the service specification file, no autoscaling occurs; Snowflake starts with the number of instances specified by the MIN\_INSTANCES parameter and does not autoscale.
