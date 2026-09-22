Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_COMPLETE (Structured outputs)

AI\_COMPLETE lets you supply a JSON schema or SQL type literal that completion responses must follow, producing structured
output. Structured output reduces the need for post-processing in your AI data pipelines and enables seamless
integration with systems that require deterministic responses. AI\_COMPLETE verifies each generated token against your
structured output definition to ensure that the response conforms to your type structure.

Every model supported by AI\_COMPLETE supports structured output, but the most powerful models typically generate higher
quality responses.

## Using AI\_COMPLETE with type literals

Type literals allow you to define structured output for AI\_COMPLETE using SQL types, taking advantage of Snowflake’s
built-in mappings between SQL and JSON types. Begin your type literal with the TYPE keyword and use a SQL OBJECT as the top-level
type. The properties of your top-level object can be any SQL type with a supported mapping to JSON.

Note

Type literals are supported only for the single string text prompt version of AI\_COMPLETE. For more information, see
[AI\_COMPLETE (Single string)](/sql-reference/functions/ai_complete-single-string).

The following example uses a type literal to produce structured output for a prompt. The prompt contains both instructions to the model and the data to process. The `response_format` type literal produces the model’s response as a JSON object with a top-level `note` containing a `date`, `address`, `items_count`, and a `price` array containing prices.

Copy code

```
SELECT AI_COMPLETE(
    model => 'llama3.3-70b',
    prompt => 'Extract structured data from this customer interaction note: Customer Sarah Jones complained about the mobile app crashing during checkout. She tried to purchase 3 items: a red XL jacket ($89.99), blue running shoes ($129.50), and a fitness tracker ($199.00). The app crashed after she entered her shipping address at 123 Main St, Portland OR, 97201. She has been a premium member since January 2024.',
    response_format => TYPE OBJECT(note OBJECT(items_count NUMBER, price ARRAY(STRING), address STRING, member_date STRING)),
    show_details => TRUE
);
```

The following is a full response to this query:

```
{
  "created": 1758755328,
  "model": "llama3.3-70b",
  "structured_output": [
    {
      "raw_message": {
        "note": {
          "items_count": 3,
          "price": [
            "$89.99",
            "$129.50",
            "$199.00"
          ]
        }
      },
      "type": "json"
    }
  ],
  "usage": {
    "completion_tokens": 49,
    "prompt_tokens": 100,
    "total_tokens": 149
  }
}
```

### Type literal notes and limitations

Specifying a structured output schema as a type literal follows these rules:

- STRING and VARCHAR types are mapped to JSON strings.
- VARCHAR types aren’t guaranteed to produce output of a specific length.
- FIXED types without a scale are mapped to JSON integers. All other numeric types are mapped to JSON numbers.

Type literals have restrictions around supported types:

- The empty object OBJECT() isn’t allowed as a type literal.
- Not all SQL types have a mapping for structured output. These include, but aren’t limited, to:
  - VARIANT
  - MAP
  - [Date & time data types](/sql-reference/data-types-datetime)

The use of an unsupported data type returns an error.

## Using AI\_COMPLETE with JSON schemas

For more control over structured output, use a [JSON schema](https://json-schema.org/) as the value for
`response_format`. The supplied JSON schema defines the structure, data types, and constraints that the generated text
must conform to, including required fields.

For simple tasks, you don’t need to specify any details of the output format, or even instruct the model to “respond in
JSON.” For more complex tasks, prompting the model to respond in JSON can improve accuracy; see
[Optimizing JSON adherence accuracy](#label-complete-structured-output-optimizing-adherence).

The following illustrates the syntax of an AI\_COMPLETE function call that uses a JSON schema to specify the structured
output format. The schema defines a top-level object, `properties`, with a `property_name` property of type string;
this field is required in the response.

Copy code

```
AI_COMPLETE(
    ...
    response_format => {
        'type': 'json',
        'schema': {
            'type': 'object',
            'properties': {
                'property_name': {
                    'type': 'string'
                },
                ...
            },
            'required': ['property_name', ...]
        }
    }
)
```

Important

For OpenAI (GPT) models, the following requirements apply:

- [additionalProperties](https://json-schema.org/understanding-json-schema/reference/object#additionalproperties) field must be set to
  `false` in every node of the schema.
- The [required](https://json-schema.org/understanding-json-schema/reference/object#required) field must be included and contain the names of
  every property in the schema.

Other models do not require these fields, but you might include them anyway so you don’t need a different schema for OpenAI models.

## SQL examples

The following example is a more complete demonstration of using AI\_COMPLETE with a single string input.

Copy code

```
SELECT AI_COMPLETE(
    model => 'mistral-large2',
    prompt => 'Return the customer sentiment for the following review: New kid on the block, this pizza joint! The pie arrived neither in a flash nor a snail\'s pace, but the taste? Divine! Like a symphony of Italian flavors, it was a party in my mouth. But alas, the party was a tad pricey for my humble abode\'s standards. A mixed bag, I\'d say!',
    response_format => {
            'type':'json',
            'schema':{'type' : 'object','properties' : {'sentiment_categories':{'type': 'object','properties':
            {'food_quality' : {'type' : 'string'},'food_taste': {'type':'string'}, 'wait_time': {'type':'string'}, 'food_cost': {'type':'string'}},'required':['food_quality','food_taste' ,'wait_time','food_cost']}}}

    }
);
```

Response:

```
{
    "sentiment_categories":
    {
        "food_cost": "negative",
        "food_quality": "positive",
        "food_taste": "positive",
        "wait_time": "neutral"
    }
}
```

The following example demonstrates how to use the `response_format` argument to specify a JSON schema for the response and using the
`show_details` argument to return inference metadata.

Copy code

```
SELECT AI_COMPLETE(
    model => 'mistral-large2',
    prompt => 'Return the customer sentiment for the following review: New kid on the block, this pizza joint! The pie arrived neither in a flash nor a snail\'s pace, but the taste? Divine! Like a symphony of Italian flavors, it was a party in my mouth. But alas, the party was a tad pricey for my humble abode\'s standards. A mixed bag, I\'d say!',
    response_format => {
            'type':'json',
            'schema':{'type' : 'object','properties' : {'sentiment_categories':{'type': 'object','properties':
            {'food_quality' : {'type' : 'string'},'food_taste': {'type':'string'}, 'wait_time': {'type':'string'}, 'food_cost': {'type':'string'}},'required':['food_quality','food_taste' ,'wait_time','food_cost']}}}

    },
    show_details => TRUE
);
```

Response:

```
{
    "created": 1738683744,
    "model": "mistral-large2",
    "structured_output": [
        {
        "raw_message": {
            "sentiment_categories":
            {
                "food_cost": "negative",
                "food_quality": "positive",
                "food_taste": "positive",
                "wait_time": "neutral"
            }
        },
        "type": "json"
        }
    ],
    "usage": {
        "completion_tokens": 60,
        "prompt_tokens": 94,
        "total_tokens": 154
    }
}
```

## Python example

Note

Structured output is supported in `snowflake-ml-python` version 1.8.0 and later.

The following example demonstrates how to use the `response_format` argument to specify a JSON schema for the response.

Copy code

```
from snowflake.cortex import complete, CompleteOptions

response_format = {
    "type": "json",
    "schema": {
        "type": "object",
        "properties": {
            "people": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "number"},
                    },
                    "required": ["name", "age"],
                },
            }
        },
        "required": ["people"],
    },
}
prompt = [{
    "role": "user",
    "content": "Please prepare me a data set of 5 ppl and their age",
}]

options = CompleteOptions(
        max_tokens=4096,
        temperature=0.7,
        top_p=1,
        guardrails=False,
        response_format=response_format
    )

result = complete(
model="claude-sonnet-4-6",
prompt=prompt,
session={session_object}, # session created via connector
stream=True,
options=options,
)

output = "".join(result)
print(output)
```

Response:

```
{"people": [{"name":"John Smith","age":32},{"name":"Sarah Johnson","age":28},
{"name":"Michael Chen","age":45},{"name":"Emily Davis","age":19},{"name":"Robert Wilson","age":56}]}
```

### Pydantic example

Pydantic is a data validation and settings management library for Python. This example uses Pydantic to define a schema
for the response format. The code performs these steps:

1. Uses Pydantic to define a schema
2. Converts the Pydantic model to a JSON schema using the `model_json_schema` method
3. Passes the JSON schema to the `complete` function as the `response_format` argument

Note

This example is meant to be run in a Snowsight Python worksheet, which already has a connection to Snowflake. To run
it in a different environment, you might need to [establish a connection to Snowflake](/developer-guide/python-connector/python-connector-connect)
using the Snowflake Connector for Python.

Copy code

```
from pydantic import BaseModel, Field
import json
from snowflake.cortex import complete, CompleteOptions
from snowflake.snowpark.context import get_active_session

class Person(BaseModel):
    age: int = Field(description="Person age")
    name: str = Field(description="Person name")

class People(BaseModel):
    people: list[Person] = Field(description="People list")

ppl = People.model_json_schema()
'''
This is the ppl object, keep in mind there's a '$defs' key used

{'$defs': {'Person': {'properties': {'age': {'description': 'Person age', 'title': 'Age', 'type': 'integer'}, 'name': {'description': 'Person name', 'title': 'Name', 'type': 'string'}}, 'required': ['age', 'name'], 'title': 'Person', 'type': 'object'}}, 'properties': {'people': {'description': 'People list', 'items': {'$ref': '#/$defs/Person'}, 'title': 'People', 'type': 'array'}}, 'required': ['people'], 'title': 'People', 'type': 'object'}

'''

response_format_pydantic={
    "type": "json",
    "schema": ppl,
}
prompt=[{"role": "user", "content": "Please prepare me a data set of 5 ppl and their age"}]
options_pydantic = CompleteOptions(  # random params
        max_tokens=4096,
        temperature=0.7,
        top_p=1,
        guardrails=False,
        response_format=response_format_pydantic
    )
model_name = "claude-sonnet-4-6"

session = get_active_session()
try:
    result_pydantic = complete(
        model=model_name,
        prompt=prompt,
        session=session,
        stream=True,
        options=options_pydantic,
    )
except Exception as err:
    result_pydantic = (chunk for chunk in err.response.text) # making sure it's generator, similar to the valid response

output_pydantic = "".join(result_pydantic)
print(output_pydantic)
```

Response:

```
{"people": [{"name":"John Smith","age":32},{"name":"Sarah Johnson","age":45},
{"name":"Mike Chen","age":28},{"name":"Emma Wilson","age":19},{"name":"Robert Brown","age":56}]}
```

## REST API example

You can use the [Snowflake Cortex LLM REST API](/user-guide/snowflake-cortex/cortex-rest-api) to invoke
COMPLETE with the LLM of your choice. Below is an example supplying a schema using the Cortex LLM REST API:

Copy code

```
curl --location --request POST 'https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete'
--header 'Authorization: Bearer <jwt>' \
--header 'Accept: application/json, text/event-stream' \
--header 'Content-Type: application/json' \
--data-raw '{
    "model": "claude-sonnet-4-6",
    "messages": [{
        "role": "user",
        "content": "Order a pizza for a hungry space traveler heading to the planet Zorgon. Make sure to include a special instruction to avoid any intergalactic allergens."
    }],
    "max_tokens": 1000,
    "response_format": {
            "type": "json",
            "schema":
            {
                "type": "object",
                "properties":
                {
                    "crust":
                    {
                        "type": "string",
                        "enum":
                        [
                            "thin",
                            "thick",
                            "gluten-free",
                            "Rigellian fungus-based"
                        ]
                    },
                    "toppings":
                    {
                        "type": "array",
                        "items":
                        {
                            "type": "string",
                            "enum":
                            [
                                "Gnorchian sausage",
                                "Andromedian mushrooms",
                                "Quasar cheese"
                            ]
                        }
                    },
                    "delivery_planet":
                    {
                        "type": "string"
                    },
                    "special_instructions":
                    {
                        "type": "string"
                    }
                },
                "required":
                [
                    "crust",
                    "toppings",
                    "delivery_planet"
                ]
            }
        }
    }'
```

Response:

```
data: {"id":"4d62e41a-d2d7-4568-871a-48de1463ed2a","model":"claude-sonnet-4-6","choices":[{"delta":{"content":"{\"crust\":","content_list":[{"type":"text","text":"{\"crust\":"}]}}],"usage":{}}

data: {"id":"4d62e41a-d2d7-4568-871a-48de1463ed2a","model":"claude-sonnet-4-6","choices":[{"delta":{"content":" \"thin\"","content_list":[{"type":"text","text":" \"thin\""}]}}],"usage":{}}

data: {"id":"4d62e41a-d2d7-4568-871a-48de1463ed2a","model":"claude-sonnet-4-6","choices":[{"delta":{"content":", \"topping","content_list":[{"type":"text","text":", \"topping"}]}}],"usage":{}}

data: {"id":"4d62e41a-d2d7-4568-871a-48de1463ed2a","model":"claude-sonnet-4-6","choices":[{"delta":{"content":"s\": [\"Quasar","content_list":[{"type":"text","text":"s\": [\"Quasar"}]}}],"usage":{}}
```

## Create a JSON schema definition

To get the best accuracy from COMPLETE Structured Outputs, follow these guidelines:

- **Use the “required” field** in the schema to specify required fields. COMPLETE raises an error if a required
  field cannot be extracted.

  In the following example, the schema directs COMPLETE to find people mentioned in the document. The `people` field
  is marked as required to make sure people are identified.

  Copy code

  ```
  {
   'type': 'object',
   'properties': {
       'dataset_name': {
           'type': 'string'
       },
       'created_at': {
           'type': 'string'
       },
       'people': {
           'type': 'array',
           'items': {
               'type': 'object',
               'properties': {
                   'name': {
                       'type': 'string'
                   },
                   'age': {
                       'type': 'number'
                   },
                   'isAdult': {
                       'type': 'boolean'
                   }
               }
           }
       }
   },
   'required': [
       'dataset_name',
       'created_at',
       'people'
   ]
  }
  ```

  Response:

  ```
  {
   "dataset_name": "name",
   "created_at": "date",
   "people": [
       {
           "name": "Andrew",
           "isAdult": true
       }
   ]
  }
  ```
- **Provide detailed descriptions** of the fields to be extracted so that the model can more accurately identify them. For
  example, the following schema includes a description of each of the fields of `people`: `name`, `age`, and `isAdult`.

  Copy code

  ```
  {
   'type': 'object',
   'properties': {
       'dataset_name': {
           'type': 'string'
       },
       'created_at': {
           'type': 'string'
       },
       'people': {
           'type': 'array',
           'items': {
               'type': 'object',
               'properties': {
                   'name': {
                       'type': 'string',
                       'description': 'name should be between 9 to 10 characters'
                   },
                   'age': {
                       'type': 'number',
                       'description': 'Should be a value between 0 and 200'
                   },
                   'isAdult': {
                       'type': 'boolean',
                       'description': 'Persons is older than 18'
                   }
               }
           }
       }
   }
  }
  ```

### Using a JSON reference

Schema references solve practical problems when using Cortex COMPLETE Structured Outputs. With references, represented
by `$ref`, you can define common objects like addresses or prices once, then reuse them throughout the
schema. This way, when you need to update validation logic or add a field, you can change it in one place instead of in
multiple locations.

Using references reduces coding effort, reduces bugs from inconsistent implementations, and makes code reviews simpler. Referenced components
create cleaner hierarchies that better represent entity relationships in your data model. As projects grow more complex,
this modular approach helps you manage technical debt while maintaining schema integrity.

Third-party libraries such as Pydantic support the reference mechanism natively in Python, simplifying schema usage in
your code.

The following guidelines apply to the use of references in JSON schema:

- **Scope limitation:** The `$ref` mechanism is limited to the user’s schema only; external schema references (such as HTTP URLs) are not supported.
- **Definition placement:** Object definitions should be placed at the top level of the schema, specifically under the definitions or `$defs` key.
- **Enforcement:** While the JSON Schema specification recommends using the `$defs` key for definitions, Snowflake’s
  validation mechanism strictly enforces this structure. This is an example of a valid `$defs` object:

Copy code

```
{
    '$defs': {
        'person':{'type':'object','properties':{'name' : {'type' : 'string'},'age': {'type':'number'}}, 'required':['name','age']}},
    'type': 'object',
    'properties': {'title':{'type':'string'},'people':{'type':'array','items':{'$ref':'#/$defs/person'}}}
}
```

#### Example using JSON reference

This SQL example demonstrates the use of references in a JSON schema.

Copy code

```
select ai_complete(
    model => 'claude-sonnet-4-6',
    prompt => 'Extract structured data from this customer interaction note: Customer Sarah Jones complained about the mobile app crashing during checkout. She tried to purchase 3 items: a red XL jacket ($89.99), blue running shoes ($129.50), and a fitness tracker ($199.00). The app crashed after she entered her shipping address at 123 Main St, Portland OR, 97201. She has been a premium member since January 2024.',
    'response_format' => {
            'type': 'json',
            'schema': {
'type': 'object',
'$defs': {
    'price': {
        'type': 'object',
        'properties': {
            'amount': {'type': 'number'},
            'currency': {'type': 'string'}
        },
        'required': ['amount']
    },
    'address': {
        'type': 'object',
        'properties': {
            'street': {'type': 'string'},
            'city': {'type': 'string'},
            'state': {'type': 'string'},
            'zip': {'type': 'string'},
            'country': {'type': 'string'}
        },
        'required': ['street', 'city', 'state']
    },
    'product': {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'category': {'type': 'string'},
            'color': {'type': 'string'},
            'size': {'type': 'string'},
            'price': {'$ref': '#/$defs/price'}
        },
        'required': ['name', 'price']
    }
},
'properties': {
    'customer': {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'membership': {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'since': {'type': 'string'}
                }
            },
            'shipping_address': {'$ref': '#/$defs/address'}
        },
        'required': ['name']
    },
    'issue': {
        'type': 'object',
        'properties': {
            'type': {'type': 'string'},
            'platform': {'type': 'string'},
            'stage': {'type': 'string'},
            'severity': {'type': 'string', 'enum': ['low', 'medium', 'high', 'critical']}
        },
        'required': ['type', 'platform']
    },
    'cart': {
        'type': 'object',
        'properties': {
            'items': {
                'type': 'array',
                'items': {'$ref': '#/$defs/product'}
            },
            'total': {'$ref': '#/$defs/price'},
            'item_count': {'type': 'integer'}
        }
    },
    'recommended_actions': {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'department': {'type': 'string'},
                'action': {'type': 'string'},
                'priority': {'type': 'string', 'enum': ['low', 'medium', 'high', 'urgent']}
            }
        }
    }
},
'required': ['customer', 'issue','cart']
}
        }
    }
);
```

Response:

```
{
  "created": 1747313083,
  "model": "claude-sonnet-4-6",
  "structured_output": [
    {
      "raw_message": {
        "cart": {
          "item_count": 3,
          "items": [
            {
              "color": "red",
              "name": "jacket",
              "price": {
                "amount": 89.99,
                "currency": "USD"
              },
              "size": "XL"
            },
            {
              "color": "blue",
              "name": "running shoes",
              "price": {
                "amount": 129.5,
                "currency": "USD"
              }
            },
            {
              "name": "fitness tracker",
              "price": {
                "amount": 199,
                "currency": "USD"
              }
            }
          ],
          "total": {
            "amount": 418.49,
            "currency": "USD"
          }
        },
        "customer": {
          "membership": {
            "since": "2024-01",
            "type": "premium"
          },
          "name": "Sarah Jones",
          "shipping_address": {
            "city": "Portland",
            "state": "OR",
            "street": "123 Main St",
            "zip": "97201"
          }
        },
        "issue": {
          "platform": "mobile",
          "severity": "high",
          "stage": "checkout",
          "type": "app_crash"
        }
      },
      "type": "json"
    }
  ],
  "usage": {
    "completion_tokens": 57,
    "prompt_tokens": 945,
    "total_tokens": 1002
  }
}
```

## Optimizing JSON adherence accuracy

COMPLETE Structured Outputs does not usually require a prompt; it already understands that its response should conform
to the schema you specify. However, task complexity can significantly influence the ability of LLMs to follow a JSON
response format. The more complex the task, the more you can improve the accuracy of results by specifying a prompt.

- **Simple tasks** such as text classification, entity extraction, paraphrasing, and summarization tasks that don’t
  require complex reasoning generally do not require additional prompting. For smaller models of lower intelligence,
  just using Structured Outputs significantly improves JSON adherence accuracy, as it ignores any text the model
  provides unrelated to the supplied schema.
- **Medium-complexity tasks** include any simple task in which the model is asked for additional reasoning, such as
  providing its rationale for a classification decision. For these use cases, we recommend adding “Respond in JSON” in
  the prompt to optimize performance.
- **Complex reasoning tasks** prompt models to perform more open-ended ambiguous tasks, such as assessing and scoring
  the quality of a call based on the relevance, professionalism, and faithfulness of answers. For these use cases, we
  recommend using the most powerful models like Anthropic’s `claude-sonnet-4-6` or Mistral AI’s `mistral-large2` and
  adding “Respond in JSON”, and details about the schema you want to generate in the prompt.

For the most consistent results, set the `temperature` option to 0 when you call COMPLETE, regardless of the task or
model.

Tip

To handle possible errors raised by a model, use [TRY\_COMPLETE](/sql-reference/functions/try_complete-snowflake-cortex) rather than COMPLETE.

## Cost considerations

Cortex COMPLETE Structured Outputs incurs compute cost based on the number of tokens processed, but does not incur
additional compute cost for the overhead of verifying each token against the supplied JSON schema. However, the number
of tokens processed (and billed) increases with schema complexity. In general, the larger and more complex the supplied
schema is, the more input and output tokens are consumed. Highly-structured responses with deep nesting (e.g.,
hierarchical data) consume a larger number of tokens than simpler schemas.

## Limitations

- You cannot use spaces in the keys of the schema.
- The characters allowed for property names are letters, digits, hyphen, underscore. Names may be a maximum of 64 characters long.
- You cannot address external schemas using `$ref` or `$dynamicRef`.

The following constraint keywords are not supported. The use of an unsupported constraint keyword results in an error.

| Type | Keywords |
| --- | --- |
| integer | `multipleOf` |
| number | `multipleOf`, `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum` |
| string | `minLength`, `maxLength`, `format` |
| array | `uniqueItems`, `contains`, `minContains`, `maxContains`, `minItems`, `maxItems` |
| object | `patternProperties`, `minProperties`, `maxProperties`, `propertyNames` |

Expand

Show lessSee more

These limitations might be addressed in future releases.

## Error conditions

| Situation | Example message | HTTP status code |
| --- | --- | --- |
| Request validation failed. The query was cancelled as the model wouldn’t be able to generate a valid response. This can be caused by a malformed request. | `please provide a type for the response format object`, `please provide a schema for the response format object` | 400 |
| Input schema validation failed. The query was cancelled as the model wouldn’t be able to generate a valid response. This can be caused by missing required properties in request payload or using unsupported json schema features such as constraints, or inappropriate use of $ref mechanism (for example, reaching outside of the schema | `input schema validation error: <reason>` with one of the reasons below:   - `/properties/city additional properties are not allowed` - `/properties/arrondissement regexp pattern ^[a-zA-Z0-9_-]{1,64}$ mismatch on string` - `/properties/province/type sting should be one of [\"object\", \"array\", \"string\", \"number\", \"integer\", \"boolean\", \"null\"]` - `Invalid ref #/http://example.com/custom-email-validator.json#. Please define a valid object in #/$defs/ section` | 400 |
| Model output validation failed. The model could not generate a response that matched the schema. | `json mode output validation error: <reason>` with one of the reasons below:   - `An error occurred while unmarshalling the model output. Model returned invalid JSON that cannot be parsed due to: unexpected end of JSON input` | 422 |

Expand

Show lessSee more
