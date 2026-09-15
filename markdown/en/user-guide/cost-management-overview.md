# Managing cost in Snowflake

Approaching Snowflake cost using the cost management framework described in this topic allows you to manage costs more effectively.
Each part of the framework offers powerful features that help minimize total cost of ownership while maximizing the
economic value that Snowflake provides.

## Cost management framework

Effective Snowflake cost management is divided into three parts: visibility, control, and optimization.

![Cost Management Framework](/static/images/cost-framework.png)

### Visibility

Visibility includes understanding the different sources of cost and the ability to explore that cost in detail. Visibility also includes
attributing cost to the right entities within your organization and monitoring costs as they accumulate so you can avoid unexpected costs.

Understand:
:   Gaining visibility into your Snowflake cost begins with understanding the basic concepts of Snowflake cost, including
    the different usage types that incur cost and the factors that determine the cost of using Snowflake resources.
    [Learn More](/user-guide/cost-understanding-overall)

Explore:
:   Once you have a good understanding of how costs accumulate in Snowflake, you are ready to explore your current Snowflake costs.
    Snowsight provides pre-built dashboards that help you visualize the cost of your Snowflake usage. If you would like to gather
    more details about your Snowflake cost, you can write custom queries against the Organization Usage and Account Usage schemas, which
    contain views dedicated to usage and cost. [Learn More](/user-guide/cost-exploring-overall)

Attribute:
:   The ability to chargeback cost to different entities within your organization clarifies who is incurring costs and for what
    purpose. This visibility can inform decisions on how to implement cost-saving measures. [Learn More](/user-guide/cost-attributing)

### Control

Snowflake provides features that let you monitor credit usage, which helps you control how much is spent during a given time period.
Budgets let you control costs for both serverless features and warehouses, while resource monitors focus solely on warehouses. Snowflake also
helps you set cost controls so you don’t spend more than expected. For example, by setting limits on how long a query can run
before it’s terminated, you can avoid unexpected costs associated with runaway queries. [Learn More](/user-guide/cost-controlling)

### Optimization

Snowflake provides tools that provide insights into how you might save and help identify significant changes in daily costs so you can
investigate in order to prevent cost spikes in the future. [Learn More](/user-guide/cost-optimize).
