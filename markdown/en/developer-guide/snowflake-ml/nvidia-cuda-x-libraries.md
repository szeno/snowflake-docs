# CUDA-X Libraries in Snowflake ML

Use Snowflake Container Runtime’s CUDA-X integrations to seamlessly scale data transformations and ML over GPUs without changing your code. Snowflake has integrated NVIDIA’s cuML and cuDF libraries into the runtime environment. With this integration, you can use libraries such as scikit-learn, umap-learn, or hdbscan with your GPUs. You don’t have to learn new frameworks or handle complex dependencies.

You can run complex processing such as topic modeling, genomics, and pattern recognition without compromising on data sizes or algorithmic
complexity. Reducing the processing time gives you the opportunity to further iterate on your models.

The integration with the CUDA-X libraries enables the GPU-accelerated processing of large datasets in the Snowflake ML Container Runtime. The processing speed can be orders of magnitude faster than using the Container Runtime exclusively.

## NVIDIA CUDA-X Libraries for Data Science

Open-source libraries like cuML and cuDF utilize GPUs for more efficient and scalable data workflows. You can use these libraries to process
data with billions of rows and millions of dimensions. For more information about these libraries, see [NVIDIA CUDA-X Data Science](https://developer.nvidia.com/topics/ai/data-science/cuda-x-data-science-libraries).

[![](/static/images/snowflake-ml/cuda-x-libraries.png)](/static/images/snowflake-ml/cuda-x-libraries.png)

CUDA-X DS libraries combine the power of GPUs with commonly used Python libraries for data analytics, machine learning, and graph
analytics—delivering major speedups without requiring teams to rewrite their code. With CUDA-X DS, you can use the GPU speed increases, to
process datasets up to terabytes in size with a single GPU.

NVIDIA cuML can deliver the following performance improvements over CPU workflows:

- Up to 50x for scikit-learn
- Up to 60x for UMAP
- Up to 175x for HDBSCAN

## Use Cases

The integration of the CUDA-X libraries in the Snowflake ML Container Runtime uses GPUs with Scikit-learn and pandas for the following use cases:

### Large-Scale topic modeling

Topic modeling on large and feature-rich data sets requires:

- Using embedding models
- Applying dimensionality reduction at scale
- Using clustering and visualization to extract accurate and relevant topics

GPU parallelism can help you accomplish the preceding workflows more efficiently. By accelerating your processing with cuML, you can transform millions of product reviews from raw text to well-defined topic clusters that can be reduced from hours on CPU to minutes on GPU with no modifications to existing Python code. This highlights the seamless drop-in acceleration for UMAP and HDBSCAN libraries.

For more information about performing topic modeling over GPUs on Snowflake, see
<https://quickstarts.snowflake.com/guide/accelerate-topic-modeling-with-gpus-in-snowflake-ml/#0>

### Computational Genomics Workflows

Use Snowflake’s CUDA-X integrations to significantly accelerate the processing of biological sequences. You can convert DNA sequences into
feature vectors for scalable classification tasks, such as predicting gene families.

Executing pandas and scikit-learn code directly on GPUs with cuDF and cuML speeds up data loading, preprocessing, and ensemble
model training. This GPU acceleration for existing workflows, without code changes, allows researchers to prioritize biological insights and
model design over low-level GPU programming.

## Developing in Snowflake

Use the CUDA-X libraries to develop and deploy GPU-accelerated machine learning models within the Snowflake ML Container Runtime . This
section provides a step-by-step guide for integrating these tools into your Python workflows.

To get started, do the following:

1. Define your Python script in a Snowflake Notebook or an ML Job
2. Select the GPU runtime and a GPU compute pool for your Notebook or ML Job

After you’ve done the preceding steps, run the following code to configure the CUDA-X accelerators in your environment.

Copy code

```
#Install cuDF and cuML accelerators for zero code change acceleration

import cuml
cuml.accel.install()
import cudf.pandas
cudf.pandas.install()
```

Now you can run pandas operations directly over GPUs or fit the scikit-learn, umap, or hdbscan model (note that there is no code change
needed to run over GPUs). This example shows how to use `hdbscan` on large datasets:

Copy code

```
import hdbscan
from sklearn.datasets import make_blobs

# Generate some sample data with multiple clusters
data, _ = make_blobs(n_samples=500, centers=4, cluster_std=0.8, random_state=42)

# Initialize and fit HDBSCAN
# min_cluster_size: The minimum size of clusters; smaller clusters will be considered noise.
# min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=15, min_samples=5, cluster_selection_epsilon=0.5)
hdbscan_model.fit(data)
```

### Applied Use Case: Topic Modeling at Scale

Computational efficiency is crucial for large scale text analysis and topic modeling. GPUs use parallel processing to reduce processing time
from hours to minutes. This section demonstrates how to accelerate ML models on a dataset of 200,000 beauty product reviews using GPU
acceleration with CUDA-X.

You can use CUDA-X to do the following:

- Transform raw text into numerical representations (embeddings) for machine learning.
- Accelerate dimensionality reduction

To utilize the CUDA libraries, add %load\_ext cuml.accel at the beginning of your code. This reduces your processing time from hours to
minutes.

The following example code uses the `SentenceTransformer` class to create embeddings.

Copy code

```
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts, show_progress_bar=True)
```

The following example code uses HDBSCAN to reduce high-dimensional data. It retains the cluster topics.

Copy code

```
from umap import UMAP
from hdbscan import HDBSCAN
umap_model = UMAP(n_components=15, n_neighbors=15, min_dist=0.0)
hdbscan_model = HDBSCAN(min_cluster_size=100, gen_min_span_tree=True, prediction_data=True)
```

### Applied Use Case: Running complex genomics workflows

Gene family organization, which includes paralogs and orthologs, is crucial for understanding gene evolution, function, and conserved
biological processes.

With the CUDA-X libraries, you can create a classification model to predict gene families from DNA sequences. This model can accelerate
genomic annotation, identify novel gene functions, and provide insights into evolutionary pathways.

The [dataset](https://raw.githubusercontent.com/nageshsinghc4/DNA-Sequence-Machine-learning/master/human_data.txt) has a series of plain
text nucleotide sequences and their corresponding gene family class labels. The classes correspond to seven distinct human gene families.

The following code uses the **nucleotide transformer** from Hugging Face to convert the DNA sequences into vectors. The transformer
tokenizes and batches the sequences to transform each gene sequence into a 1280-feature vector.

Copy code

```
%load_ext cudf.pandas
%load_ext cuml.accel

from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

def get_dna_embeddings(sequences, classes):
    tokens_ids = tokenizer.batch_encode_plus(sequences, return_tensors="pt", padding="longest")["input_ids"].to('cuda:0')

    attention_mask = tokens_ids != tokenizer.pad_token_id
    try:
        torch_outs = model(
            tokens_ids,
            attention_mask=attention_mask,
            encoder_attention_mask=attention_mask,
            output_hidden_states=True
        )
    except:
        return []

    embeddings = torch_outs['hidden_states'][-1].detach()
    attention_mask = torch.unsqueeze(attention_mask, dim=-1)
    mean_sequence_embeddings = torch.sum(attention_mask*embeddings, axis=-2)/torch.sum(attention_mask, axis=1)
    return list(zip(mean_sequence_embeddings.numpy(), classes))

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-human-ref")
model = AutoModelForMaskedLM.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-human-ref")

# Example of obtaining embeddings (simplified)
sequences = ["ATGCCCCAACTAAATACTACCGTATGGCCCACCATAATTACCCCCA", ...]
classes = [0, ...]

genes = []
batch_size=10

emb = get_dna_embeddings(human_genes[i], human_classes[i])
genes += emb
```

You can use the following code to evaluate two ensemble classification models:

- A Random Forest Classifier
- An XGBoost classifier

Copy code

```
%load_ext cudf.pandas
%load_ext cuml.accel

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

human_dna = pd.read_table(human_url) # This would now run on GPU

genes = []
batch_size=10

human_genes = human_dna['sequence'].tolist()
human_classes = human_dna['class'].tolist()

human_genes = [human_genes[i:i + batch_size] for i in range(0, len(human_genes), batch_size)]
human_classes = [human_classes[i:i + batch_size] for i in range(0, len(human_classes), batch_size)]

# Create the embeddings
for i in tqdm(range(len(human_genes)), desc='Producing embeddings...'):
    emb = get_dna_embeddings(human_genes[i], human_classes[i])
    genes += emb

genes_df = pd.DataFrame(genes, columns=['embeddings', 'class'])
genes_df[[f'emb_{i}' for i in range(1280)]] = pd.DataFrame(genes_df['embeddings'].tolist(), index=genes_df.index) # the embeddings generated above

X, y = genes_df[[f'emb_{i}' for i in range(1280)]], genes_df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                   test_size = 0.20,
                                                   random_state=42)

classifier = RandomForestClassifier(n_estimators=200, max_depth=20, max_features=1.0, n_jobs=-1)
classifier.fit(X_train, y_train)
```

## See Also

- [Snowflake ML: End-to-End Agentic Machine Learning](/developer-guide/snowflake-ml/overview)
- [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml)
