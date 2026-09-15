# Managing Snowflake network policies with Python

You can use Python to manage Snowflake network policies, which you can use to control inbound access to the Snowflake service and internal
stage. For more information, see [Controlling network traffic with network policies](/user-guide/network-policies).

Note

[ALTER NETWORK POLICY](/sql-reference/sql/alter-network-policy) is currently not supported.

The Snowflake Python APIs represents network policies with two separate types:

- `NetworkPolicy`: Exposes a network policy’s properties such as its name, network rules, and allowed and blocked IP lists.
- `NetworkPolicyResource`: Exposes methods you can use to fetch a corresponding `NetworkPolicy` object and drop the network
  policy.

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Creating a network policy

To create a network policy, first create a `NetworkPolicy` object, and then create a `NetworkPolicyCollection` object from the
API `Root` object. Using `NetworkPolicyCollection.create`, add the new network policy to Snowflake.

Code in the following example creates a `NetworkPolicy` object that represents a network policy named `my_network_policy` with
the specified allowed and blocked network rules and IP addresses:

Copy code

```
from snowflake.core.network_policy import NetworkPolicy

my_network_policy = NetworkPolicy(
  name = 'my_network_policy',
  allowed_network_rule_list = ['allowed_network_rule1','allowed_network_rule2'],
  blocked_network_rule_list = ['blocked_network_rule1','blocked_network_rule2'],
  allowed_ip_list=['8.8.8.8'],
  blocked_ip_list=['192.100.123.0'],
)

root.network_policies.create(my_network_policy)
```

## Getting network policy details

You can get information about a network policy by calling the `NetworkPolicyResource.fetch` method, which returns a
`NetworkPolicy` object.

Code in the following example gets information about a network policy named `my_network_policy`:

Copy code

```
my_network_policy = root.network_policies["my_network_policy"].fetch()
print(my_network_policy.to_dict())
```

## Listing network policies

You can list network policies using the `NetworkPolicyCollection.iter` method, which returns a `PagedIter` iterator of
`NetworkPolicy` objects.

Code in the following example lists network policies whose name starts with `my` and prints the name of each:

Copy code

```
network_policy_iter = root.network_policies.iter(like="my%")  # returns a PagedIter[NetworkPolicy]
for network_policy_obj in network_policy_iter:
  print(network_policy_obj.name)
```

## Dropping a network policy

You can drop a network policy with a `NetworkPolicyResource` object.

Code in the following example gets the `my_network_policy` network policy resource object and then drops the network policy.

Copy code

```
my_network_policy_res = root.network_policies["my_network_policy"]
my_network_policy_res.drop()
```
