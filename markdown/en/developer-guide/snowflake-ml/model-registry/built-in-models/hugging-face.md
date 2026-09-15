# Hugging Face pipeline

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Snowflake Model Registry supports any Hugging Face model defined as a
[transformer](https://huggingface.co/docs/transformers/index) that can be loaded with the [transformers.Pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.pipeline) method.

Use one of the following methods to log a Hugging Face model to the Model Registry:

1. Import and deploy a model from Hugging Face using Snowsight. See [Import and deploy models from an external service](/developer-guide/snowflake-ml/model-registry/snowsight-ui#label-model-import-external) for instructions.
2. Create a :class:`snowflake.ml.model.models.huggingface.TransformersPipeline` instance and call `~snowflake.ml.registry.Registry.log_model`:

   Copy code

   ```
   # reg: snowflake.ml.registry.Registry

   from snowflake.ml.model.models import huggingface

   model = huggingface.TransformersPipeline(
    task="text-classification",
    model="ProsusAI/finbert",
    # compute_pool_for_log=... # Optional
   )

   mv = reg.log_model(model, model_name='finbert', version_name='v5')
   ```

   Important

   - If you don’t specify a `compute_pool_for_log` argument, the model is logged using the default CPU compute pool.
   - If you specify a `compute_pool_for_log` argument, the model is logged using the specified compute pool.
   - If you specify `compute_pool_for_log` argument as None, the model files are downloaded locally and then uploaded to the model registry. This requires [huggingface-hub](https://pypi.org/project/huggingface-hub/) to be installed.
3. Load the model from Hugging Face in memory and log it to Model Registry:

   Copy code

   ```
   # reg: snowflake.ml.registry.Registry

   lm_hf_model = transformers.pipeline(
    task="text-generation",
    model="bigscience/bloom-560m",
    token="...",  # Put your HuggingFace token here.
    return_full_text=False,
    max_new_tokens=100,
   )

   lmv = reg.log_model(lm_hf_model, model_name='bloom', version_name='v560m')
   ```

If you are using Snowflake Notebooks, in order to download the weights of the model, you need to have an external access integration attached to your notebook. This integration is required to allow egress to the following hosts:

- `huggingface.co`
- `hub-ci.huggingface.co`
- `cdn-lfs-us-1.hf.co`
- `cdn-lfs-eu-1.hf.co`
- `cdn-lfs.hf.co`
- `transfer.xethub.hf.co`
- `cas-server.xethub.hf.co`
- `cas-bridge.xethub.hf.c`

Note

This list of hosts are only those required for accessing Hugging Face, and may change at any time. Your model may require artifacts from other sources, which should be added to the network rule as allowed for egress.

The following example creates a new external access integration `huggingface_network_rule` for use with a Notebook:

Copy code

```
CREATE NETWORK RULE huggingface_network_rule
TYPE = HOST_PORT
VALUE_LIST = (
    'huggingface.co',
    'hub-ci.huggingface.co',
    'cdn-lfs-us-1.hf.co',
    'cdn-lfs-eu-1.hf.co',
    'cdn-lfs.hf.co',
    'transfer.xethub.hf.co',
    'cas-server.xethub.hf.co',
    'cas-bridge.xethub.hf.co'
)
MODE = EGRESS
COMMENT = 'Network Rule for Hugging Face external access';

CREATE EXTERNAL ACCESS INTEGRATION huggingface_access_integration
ALLOWED_NETWORK_RULES = (huggingface_network_rule)
ENABLED = true;
```

See [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access) for more information.

Once your external access integration is created, attach it to your Notebook and have access to the Hugging Face model repository to download the weights and configurations of the model. See [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access) for more information.

## Model Registry API

When calling `log_model`, the `options` dictionary supports the following keys:

| Option key | Description | Type |
| --- | --- | --- |
| `target_methods` | A list of methods available on the model object. Hugging Face models use the object’s `__call__` method by default, if it exists. | `list[str]` |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with a GPU. If set to `None`, the model can’t be deployed to a platform with a GPU. Defaults to `12.4`. | `Optional[str]` |

Expand

Show lessSee more

The model registry infers the `signatures` argument if the pipeline contains a task from the following list:

- [fill-mask](#label-hugging-face-fill-mask-signature)
- question-answering ([single output](#label-hugging-face-question-single-signature), [multiple outputs](#label-hugging-face-question-multi-signature))
- [summarization](#label-hugging-face-summarize-signature)
- [table-question-answering](#label-hugging-face-table-question-signature)
- [text2text-generation](#label-hugging-face-text-to-text-signature)
- text-classification ([single output](#label-hugging-face-text-classify-single-signature), [multiple outputs](#label-hugging-face-text-classify-multi-signature))
- sentiment-analysis ([single output](#label-hugging-face-text-classify-single-signature), [multiple outputs](#label-hugging-face-text-classify-multi-signature))
- [text-generation](#label-hugging-face-text-gen-signature) ([with OpenAI-compatible settings](#label-hugging-face-text-gen-openai-signature))
- [token-classification](#label-hugging-face-ner-signature)
- [ner](#label-hugging-face-ner-signature)
- [translation](#label-hugging-face-translaton-gen-signature)
- [translation\_xx\_to\_yy](#label-hugging-face-translaton-gen-signature), where `xx` and `yy` are two-letter country codes defined in [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes#Current_ISO_3166_country_codes)
- [zero-shot-classification](#label-hugging-face-zero-shot-classify-signature)

Note

Task names are case-sensitive.

The `sample_input_data` argument to `log_model` is ignored for Hugging Face models. Specify the `signatures` argument
when logging a Hugging Face model that is not in the preceding list so that the registry knows the signatures of the target
methods.

To see the inferred signature, call the `~snowflake.ml.model.ModelVersion.show_functions` method. This signature gives you the required types and column names for model function input, as well as the format of its output. The following example shows the signature for the model `bigscience/bloom-560m` with a task of `text-generation`:

```
{'name': '__CALL__',
  'target_method': '__call__',
  'signature': ModelSignature(
                      inputs=[
                          FeatureSpec(dtype=DataType.STRING, name='inputs')
                      ],
                      outputs=[
                          FeatureSpec(dtype=DataType.STRING, name='outputs')
                      ]
                  )}]
```

The following example shows how to invoke a model using the previous signature:

Copy code

```
# model: snowflake.ml.model.ModelVersion

import pandas as pd

remote_prediction = model.run(pd.DataFrame(["Hello, how are you?"], columns=["inputs"]))
```

## Usage notes

- Many Hugging Face models are large and don’t fit in a standard warehouse. Use a Snowpark-optimized warehouse or choose
  a smaller version of the model. For example, an alternative to the `Llama-2-70b-chat-hf` model is `Llama-2-7b-chat-hf`.
- Snowflake warehouses do not have GPUs. Use only CPU-optimized Hugging Face models.
- Some Hugging Face transformers return an array of dictionaries per input row. The model registry converts this array of dictionaries to a
  string containing a JSON representation of the array. For example, multi-output Question Answering output looks similar to this:

  ```
  '[{"score": 0.61094731092453, "start": 139, "end": 178, "answer": "learn more about the world of athletics"},
  {"score": 0.17750297486782074, "start": 139, "end": 180, "answer": "learn more about the world of athletics.\""}]'
  ```

## Example

Copy code

```
# Prepare model

import transformers
import pandas as pd

finbert_model = transformers.pipeline(
    task="text-classification",
    model="ProsusAI/finbert",
    top_k=2,
)

# Log the model
mv = registry.log_model(
    finbert_model,
    model_name="finbert",
    version_name="v1",
)

# Use the model
mv.run(pd.DataFrame(
        [
            ["I have a problem with my Snowflake that needs to be resolved asap!!", ""],
            ["I would like to have udon for today's dinner.", ""],
        ]
    )
)
```

Result:

```
0  [{"label": "negative", "score": 0.8106237053871155}, {"label": "neutral", "score": 0.16587384045124054}]
1  [{"label": "neutral", "score": 0.9263970851898193}, {"label": "positive", "score": 0.05286872014403343}]
```

## Inferred signatures for Hugging Face pipelines

This section describes the inferred signatures for supported Hugging Face pipelines, including a description and example of the required inputs and expected outputs. All inputs and outputs are Snowpark DataFrames.

### Fill-mask pipeline

A pipeline whose task is “[fill-mask](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.FillMaskPipeline)”
has the following inputs and outputs.

#### Inputs

- `inputs`: A string where there is a mask to fill.

Example:

```
--------------------------------------------------
|"inputs"                                        |
--------------------------------------------------
|LynYuu is the [MASK] of the Grand Duchy of Yu.  |
--------------------------------------------------
```

#### Outputs

- `outputs`: A string that contains a JSON representation of a list of objects, each of which may contain keys such
  as `score`, `token`, `token_str`, or `sequence`. For details, see
  [FillMaskPipeline](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.FillMaskPipeline).

Example:

```
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|"outputs"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|[{"score": 0.9066258072853088, "token": 3007, "token_str": "capital", "sequence": "lynyuu is the capital of the grand duchy of yu."}, {"score": 0.08162177354097366, "token": 2835, "token_str": "seat", "sequence": "lynyuu is the seat of the grand duchy of yu."}, {"score": 0.0012052370002493262, "token": 4075, "token_str": "headquarters", "sequence": "lynyuu is the headquarters of the grand duchy of yu."}, {"score": 0.0006560495239682496, "token": 2171, "token_str": "name", "sequence": "lynyuu is the name of the grand duchy of yu."}, {"score": 0.0005427763098850846, "token": 3200, "token_str"...  |
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="fill-mask",
    model="google-bert/bert-base-uncased",
)

mv = registry.log_model(
    model=model,
    model_name="GOOGLE_BERT_BASE_UNCASED",
)

input_df = pd.DataFrame([{"text": "LynYuu is the [MASK] of the Grand Duchy of Yu."}])
mv.run(
    input_df,
    # function_name="__call__", # Optional
)
```

### Token classification

A pipeline whose task is “ner” or
[token-classification](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TokenClassificationPipeline)
has the following inputs and outputs.

#### Inputs

- `inputs`: A string that contains the tokens to be classified.

Example:

```
------------------------------------------------
|"inputs"                                      |
------------------------------------------------
|My name is Izumi and I live in Tokyo, Japan.  |
------------------------------------------------
```

#### Outputs

- `outputs`: A string that contains a JSON representation of a list of result objects, each of which may contain keys such
  as `entity`, `score`, `index`, `word`, `name`, `start`, or `end`. For details, see
  [TokenClassificationPipeline](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TokenClassificationPipeline).

Example:

```
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|"outputs"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|[{"entity": "PRON", "score": 0.9994392991065979, "index": 1, "word": "my", "start": 0, "end": 2}, {"entity": "NOUN", "score": 0.9968984127044678, "index": 2, "word": "name", "start": 3, "end": 7}, {"entity": "AUX", "score": 0.9937735199928284, "index": 3, "word": "is", "start": 8, "end": 10}, {"entity": "PROPN", "score": 0.9928083419799805, "index": 4, "word": "i", "start": 11, "end": 12}, {"entity": "PROPN", "score": 0.997334361076355, "index": 5, "word": "##zumi", "start": 12, "end": 16}, {"entity": "CCONJ", "score": 0.999173104763031, "index": 6, "word": "and", "start": 17, "end": 20}, {...  |
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="token-classification",
    model="dslim/bert-base-NER",
)

mv = registry.log_model(
    model=model,
    model_name="BERT_BASE_NER",
)

mv.run(
    pd.DataFrame([{"inputs": "My name is Izumi and I live in Tokyo, Japan."}]),
    # function_name="__call__", # Optional
)
```

### Question answering (single output)

A pipeline whose task is “[question-answering](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.QuestionAnsweringPipeline)”,
where `top_k` is either unset or set to 1, has the following inputs and outputs.

#### Inputs

- `question`: A string that contains the question to answer.
- `context`: A string that may contain the answer.

Example:

```
-----------------------------------------------------------------------------------
|"question"                  |"context"                                           |
-----------------------------------------------------------------------------------
|What did Doris want to do?  |Doris is a cheerful mermaid from the ocean dept...  |
-----------------------------------------------------------------------------------
```

#### Outputs

- `score`: Floating-point confidence score from 0.0 to 1.0.
- `start`: Integer index of the first token of the answer in the context.
- `end`: Integer index of the last token of the answer in the original context.
- `answer`: A string that contains the found answer.

Example:

```
--------------------------------------------------------------------------------
|"score"           |"start"  |"end"  |"answer"                                 |
--------------------------------------------------------------------------------
|0.61094731092453  |139      |178    |learn more about the world of athletics  |
--------------------------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="question-answering",
    model="deepset/roberta-base-squad2",
)

QA_input = {
    "question": "Why is model conversion important?",
    "context": "The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.",
}

mv = registry.log_model(
    model=model,
    model_name="ROBERTA_BASE_SQUAD2",
)

mv.run(
    pd.DataFrame.from_records([QA_input]),
    # function_name="__call__", # Optional
)
```

### Question answering (multiple outputs)

A pipeline whose task is “[question-answering](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.QuestionAnsweringPipeline)”,
where `top_k` is set and is larger than 1, has the following inputs and outputs.

#### Inputs

- `question`: A string that contains the question to answer.
- `context`: A string that may contain the answer.

Example:

```
-----------------------------------------------------------------------------------
|"question"                  |"context"                                           |
-----------------------------------------------------------------------------------
|What did Doris want to do?  |Doris is a cheerful mermaid from the ocean dept...  |
-----------------------------------------------------------------------------------
```

#### Outputs

- `outputs`: A string that contains a JSON representation of a list of result objects, each of which may contain keys such
  as `score`, `start`, `end`, or `answer`.

Example:

```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|"outputs"                                                                                                                                                                                                                                                                                                                                        |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|[{"score": 0.61094731092453, "start": 139, "end": 178, "answer": "learn more about the world of athletics"}, {"score": 0.17750297486782074, "start": 139, "end": 180, "answer": "learn more about the world of athletics.\""}, {"score": 0.06438097357749939, "start": 138, "end": 178, "answer": "\"learn more about the world of athletics"}]  |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="question-answering",
    model="deepset/roberta-base-squad2",
    top_k=3,
)

QA_input = {
    "question": "Why is model conversion important?",
    "context": "The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.",
}

mv = registry.log_model(
    model=model,
    model_name="ROBERTA_BASE_SQUAD2",
)

mv.run(
    pd.DataFrame.from_records([QA_input]),
    # function_name="__call__", # Optional
)
```

### Summarization

A pipeline whose task is “[summarization](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.SummarizationPipeline)”,
where `return_tensors` is False or unset, has the following inputs and outputs.

#### Inputs

- `documents`: A string that contains text to summarize.

Example:

```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|"documents"                                                                                                                                                                                               |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|Neuro-sama is a chatbot styled after a female VTuber that hosts live streams on the Twitch channel "vedal987". Her speech and personality are generated by an artificial intelligence (AI) system  wh...  |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### Outputs

- `summary_text`: A string that contains the generated summary, or, if `num_return_sequences` is greater than 1,
  a string that contains a JSON representation of a list of results, each of which is a dictionary that contains fields, including `summary_text`.

Example:

```
---------------------------------------------------------------------------------
|"summary_text"                                                                 |
---------------------------------------------------------------------------------
| Neuro-sama is a chatbot styled after a female VTuber that hosts live streams  |
---------------------------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="summarization",
    model="facebook/bart-large-cnn",
)

text = "The transformers library is a great library for natural language processing which provides a unified interface for many different models and tasks."

mv = registry.log_model(
    model=model,
    model_name="BART_LARGE_CNN",
)

mv.run(
    pd.DataFrame.from_records([{"documents": text}]),
    # function_name="__call__", # Optional
)
```

### Table question answering

A pipeline whose task is
“[table-question-answering](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TableQuestionAnsweringPipeline)”
has the following inputs and outputs.

#### Inputs

- `query`: A string that contains the question to be answered.
- `table`: A string that contains a JSON-serialized dictionary in the form `{column -> [values]}` representing the table
  that may contain an answer.

Example:

```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|"query"                                  |"table"                                                                                                                                                                                                                                                   |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|Which channel has the most subscribers?  |{"Channel": ["A.I.Channel", "Kaguya Luna", "Mirai Akari", "Siro"], "Subscribers": ["3,020,000", "872,000", "694,000", "660,000"], "Videos": ["1,200", "113", "639", "1,300"], "Created At": ["Jun 30 2016", "Dec 4 2017", "Feb 28 2014", "Jun 23 2017"]}  |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### Outputs

- `answer`: A string that contains a possible answer.
- `coordinates`: A list of integers that represent the coordinates of the cells where the answer was located.
- `cells`: A list of strings that contain the content of the cells where the answer was located.
- `aggregator`: A string that contains the name of the aggregator used.

Example:

```
----------------------------------------------------------------
|"answer"     |"coordinates"  |"cells"          |"aggregator"  |
----------------------------------------------------------------
|A.I.Channel  |[              |[                |NONE          |
|             |  [            |  "A.I.Channel"  |              |
|             |    0,         |]                |              |
|             |    0          |                 |              |
|             |  ]            |                 |              |
|             |]              |                 |              |
----------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd
import json

model = transformers.pipeline(
    task="table-question-answering",
    model="microsoft/tapex-base-finetuned-wikisql",
)

data = {
    "year": [1896, 1900, 1904, 2004, 2008, 2012],
    "city": ["athens", "paris", "st. louis", "athens", "beijing", "london"],
}
query = "What is the city of the year 2004?"

mv = registry.log_model(
    model=model,
    model_name="TAPEX_BASE_FINETUNED_WIKISQL",
)

mv.run(
    pd.DataFrame.from_records([{"query": query, "table": json.dumps(data)}]),
    # function_name="__call__", # Optional
)
```

### Text classification (single output)

A pipeline whose task is
“[text-classification](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TextClassificationPipeline)” or “sentiment-analysis”,
where `top_k` is not set or is None,
has the following inputs and outputs.

#### Inputs

- `text`: A string to classify.
- `text_pair`: A string to classify along with `text`, and which is used with models that compute text similarity. Leave empty if the model does not use it.

Example:

```
----------------------------------
|"text"       |"text_pair"       |
----------------------------------
|I like you.  |I love you, too.  |
----------------------------------
```

#### Outputs

- `label`: A string that represents the classification label of the text.
- `score`: A floating-point confidence score from 0.0 to 1.0.

Example:

```
--------------------------------
|"label"  |"score"             |
--------------------------------
|LABEL_0  |0.9760091304779053  |
--------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
)

text = "I'm happy today!"

mv = registry.log_model(
    model=model,
    model_name="TWITTER_ROBERTA_BASE_SENTIMENT_LATEST",
)

mv.run(
    pd.DataFrame.from_records([{"text": text}]),
    # function_name="__call__", # Optional
)
```

### Text classification (multiple output)

A pipeline whose task is
“[text-classification](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TextClassificationPipeline)” or “sentiment-analysis”,
where `top_k` is set to a number,
has the following inputs and outputs.

Note

A text classification task is considered multiple-output if `top_k` is set to any number, even if that number is 1.
To get a [single output](#label-hugging-face-text-classify-single-signature), use a `top_k` value of None.

#### Inputs

- `text`: A string to classify.
- `text_pair`: A string to classify along with `text`, which is used with models that compute text similarity. Leave empty if the model does not use it.

Example:

```
--------------------------------------------------------------------
|"text"                                              |"text_pair"  |
--------------------------------------------------------------------
|I am wondering if I should have udon or rice fo...  |             |
--------------------------------------------------------------------
```

#### Outputs

- `outputs`: A string that contains a JSON representation of a list of results, each of which contains fields that include `label` and `score`.

Example:

```
--------------------------------------------------------
|"outputs"                                             |
--------------------------------------------------------
|[{"label": "NEGATIVE", "score": 0.9987024068832397}]  |
--------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    top_k=3,
)

text = "I'm happy today!"

mv = registry.log_model(
    model=model,
    model_name="TWITTER_ROBERTA_BASE_SENTIMENT_LATEST",
)

mv.run(
    pd.DataFrame.from_records([{"text": text}]),
    # function_name="__call__", # Optional
)
```

### Text-to-text generation

A pipeline whose task is
“[text2text-generation](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.Text2TextGenerationPipeline)”,
where `return_tensors` is False or unset,
has the following inputs and outputs.

#### Inputs

- `inputs`: A string that contains a prompt.

Example:

```
--------------------------------------------------------------------------------
|"inputs"                                                                      |
--------------------------------------------------------------------------------
|A descendant of the Lost City of Atlantis, who swam to Earth while saying, "  |
--------------------------------------------------------------------------------
```

#### Outputs

- generated\_text : A string that contains the generated text if `num_return_sequences` is 1, or if num\_return\_sequences is
  greater than 1, a string representation
  of a JSON list of result dictionaries that contain fields including `generated_text` .

Example:

```
----------------------------------------------------------------
|"generated_text"                                              |
----------------------------------------------------------------
|, said that he was a descendant of the Lost City of Atlantis  |
----------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="text2text-generation",
    model="google-t5/t5-small",
)

text = "Tell me a joke."

mv = registry.log_model(
    model=model,
    model_name="T5_SMALL",
)

mv.run(
    pd.DataFrame.from_records([{"inputs": text}]),
    # function_name="__call__", # Optional
)
```

Note

Text-to-text generation pipelines where `return_tensors` is True are not supported.

### Translation generation

A pipeline whose task is
“[translation](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TranslationPipeline)”,
where `return_tensors` is False or unset,
has the following inputs and outputs.

Note

Translation generation pipelines where `return_tensors` is True are not supported.

#### Inputs

- `inputs`: A string that contains text to translate.

Example:

```
------------------------------------------------------------------------------------------------------
|"inputs"                                                                                            |
------------------------------------------------------------------------------------------------------
|Snowflake's Data Cloud is powered by an advanced data platform provided as a self-managed service.  |
------------------------------------------------------------------------------------------------------
```

#### Outputs

- `translation_text`: A string that represents generated translation if `num_return_sequences` is 1, or a string
  representation of a JSON list of result dictionaries, each containing fields that include `translation_text`.

Example:

```
---------------------------------------------------------------------------------------------------------------------------------
|"translation_text"                                                                                                             |
---------------------------------------------------------------------------------------------------------------------------------
|Le Cloud de données de Snowflake est alimenté par une plate-forme de données avancée fournie sous forme de service autogérés.  |
---------------------------------------------------------------------------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="translation",
    model="deepvk/kazRush-kk-ru",
)

text = "Иттерді кім шығарды?"

mv = registry.log_model(
    model=model,
    model_name="KAZRUSH_KK_RU",
)

mv.run(
    pd.DataFrame.from_records([{"inputs": text}]),
    # function_name="__call__", # Optional
)
```

### Zero-shot classification

A pipeline whose task is
“[zero-shot-classification](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.ZeroShotClassificationPipeline)”
has the following inputs and outputs.

#### Inputs

- `sequences`: A string that contains the text to be classified.
- `candidate_labels`: A list of strings that contain the labels to be applied to the text.

Example:

```
-----------------------------------------------------------------------------------------
|"sequences"                                                       |"candidate_labels"  |
-----------------------------------------------------------------------------------------
|I have a problem with Snowflake that needs to be resolved asap!!  |[                   |
|                                                                  |  "urgent",         |
|                                                                  |  "not urgent"      |
|                                                                  |]                   |
|I have a problem with Snowflake that needs to be resolved asap!!  |[                   |
|                                                                  |  "English",        |
|                                                                  |  "Japanese"        |
|                                                                  |]                   |
-----------------------------------------------------------------------------------------
```

#### Outputs

- `sequence`: The input string.
- `labels`: A list of strings that represent the labels that were applied.
- `scores`: A list of floating-point confidence scores for each label.

Example:

```
--------------------------------------------------------------------------------------------------------------
|"sequence"                                                        |"labels"        |"scores"                |
--------------------------------------------------------------------------------------------------------------
|I have a problem with Snowflake that needs to be resolved asap!!  |[               |[                       |
|                                                                  |  "urgent",     |  0.9952737092971802,   |
|                                                                  |  "not urgent"  |  0.004726255778223276  |
|                                                                  |]               |]                       |
|I have a problem with Snowflake that needs to be resolved asap!!  |[               |[                       |
|                                                                  |  "Japanese",   |  0.5790848135948181,   |
|                                                                  |  "English"     |  0.42091524600982666   |
|                                                                  |]               |]                       |
--------------------------------------------------------------------------------------------------------------
```

### Text generation

A pipeline whose task is
“[text-generation](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TextGenerationPipeline)”,
where `return_tensors` is False or unset,
has the following inputs and outputs.

Note

Text generation pipelines where `return_tensors` is True are not supported.

#### Inputs

- `inputs`: A string that contains a prompt.

Example:

```
--------------------------------------------------------------------------------
|"inputs"                                                                      |
--------------------------------------------------------------------------------
|A descendant of the Lost City of Atlantis, who swam to Earth while saying, "  |
--------------------------------------------------------------------------------
```

#### Outputs

- `outputs`: A string that contains a JSON representation of a list of result objects, each of which contains fields that include `generated_text`.

Example:

```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|"outputs"                                                                                                                                                                                                 |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|[{"generated_text": "A descendant of the Lost City of Atlantis, who swam to Earth while saying, \"For my life, I don't know if I'm gonna land upon Earth.\"\n\nIn \"The Misfits\", in a flashback, wh...  |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd

model = transformers.pipeline(
    task="text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
)

mv = registry.log_model(
    model=model,
    model_name="TINYLLAMA",
)

text = "A descendant of the Lost City of Atlantis, who swam to Earth while saying,"
mv.run(
    pd.DataFrame.from_records([{"inputs": text}]),
    # function_name="__call__", # Optional
)
```

### Text generation (OpenAI-compatible)

A pipeline whose task is
“[text-generation](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TextGenerationPipeline)”,
where `return_tensors` is False or unset,
has the following inputs and outputs.

By providing the `snowflake.ml.model.openai_signatures.OPENAI_CHAT_SIGNATURE` signature, while logging the model, the model will be compatible with the OpenAI API. This allows the users to pass *openai.client.ChatCompletion* style requests to the model.

Note

Text generation pipelines where `return_tensors` is True are not supported.

#### Inputs

- `messages`: A list of dictionaries that contain the messages to be sent to the model.
- `max_completion_tokens`: The maximum number of tokens to generate.
- `temperature`: The temperature to use for the generation.
- `stop`: The stop sequence to use for the generation.
- `n`: The number of generations to produce.
- `stream`: Whether to stream the generation.
- `top_p`: The top p value to use for the generation.
- `frequency_penalty`: The frequency penalty to use for the generation.
- `presence_penalty`: The presence penalty to use for the generation.

Example:

```
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| messages                                                                                                                                                                                          |   max_completion_tokens |   temperature | stop   |   n | stream   |   top_p |   frequency_penalty |  presence_penalty |
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| [{'role': 'system', 'content': 'Complete the sentence.'}, {'role': 'user', 'content': [{'type': 'text', 'text': 'A descendant of the Lost City of Atlantis, who swam to Earth while saying, '}]}] |                     250 |           0.9 |        |   3 | False    |       1 |                 0.1 |               0.2 |
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### Outputs

- `outputs`: A string that contains a JSON representation of a list of result objects, each of which contains fields that include `generated_text`.

Example:

```
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| id           | object          |     created | model                                      | choices                                                                                                                                      |  usage                                                               |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| chatcmpl-... | chat.completion | 1.76912e+09 | /shared/model/model/models/TINYLLAMA/model | [{'finish_reason': 'stop', 'index': 0, 'logprobs': None, 'message': {'content': 'The descendant is not actually ...', 'role': 'assistant'}}] | {'completion_tokens': 399, 'prompt_tokens': 52, 'total_tokens': 451} |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### Code Example

Copy code

```
import transformers
import pandas as pd
from snowflake.ml.model import openai_signatures

model = transformers.pipeline(
    task="text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
)

mv = registry.log_model(
    model=model,
    model_name="TINYLLAMA",
    signatures=openai_signatures.OPENAI_CHAT_SIGNATURE,
)

# create a pd.DataFrame with openai.client.chat.completion arguments
x_df = pd.DataFrame.from_records(
    [
        {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "Complete the sentence.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "A descendant of the Lost City of Atlantis, who swam to Earth while saying, ",
                        }
                    ],
                },
            ],
            "max_completion_tokens": 250,
            "temperature": 0.9,
            "stop": None,
            "n": 3,
            "stream": False,
            "top_p": 1.0,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.2,
        }
    ],
)

# OpenAI Chat Completion compatible output
output_df = mv.run(X=x_df)
```
