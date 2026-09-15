# Parsing documents with AI\_PARSE\_DOCUMENT

Regional Availability

Available natively to accounts in [select regions](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).
Available through [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to accounts in all regions.

AI\_PARSE\_DOCUMENT is a Cortex AI function that extracts **text, data, layout elements, and images** from documents,
enabling end-to-end, multimodal document processing pipelines at enterprise scale.

The function processes documents stored on internal or external stages, preserving reading order and structural
elements such as tables and headers. It can be combined with other Cortex AI functions to build advanced workflows
for extraction, classification, enrichment, and analysis.

AI\_PARSE\_DOCUMENT supports a wide range of use cases, including:

- **Data enrichment:** Extract text and images to add visual and contextual signals for deeper insights
- **Multimodal RAG:** Combine text and images to improve retrieval-augmented generation (RAG) quality
- **Image understanding:** Use extracted images with AI\_EXTRACT or AI\_COMPLETE for automatic tagging and analysis
- **Knowledge base creation:** Build richer repositories that include both structured text and visual content
- **Compliance and audit workflows:** Extract and analyze elements such as charts, signatures, and embedded visuals

AI\_PARSE\_DOCUMENT orchestrates advanced AI models for document understanding and layout analysis, enabling
high-fidelity processing of complex, multi-page documents.

## Processing modes

The AI\_PARSE\_DOCUMENT function offers two modes for processing documents:

- **LAYOUT** mode is the preferred choice for most use cases, especially for complex documents. It is optimized for
  extracting structured content such as tables, headers, and layout relationships, and is required for image
  extraction.
- **Image extraction (LAYOUT mode):** Extract embedded images alongside text and layout by setting
  `'extract_images': true`, enabling multimodal workflows such as RAG, image analysis, and compliance use cases.
  There is no additional cost for using this parameter.
- **OCR** mode is recommended for fast, high-quality text extraction from scanned or text-heavy documents such as
  contracts, insurance claims, and manuals.

For each mode, use the `page_split` option to split multi-page documents into separate pages in the response.
You can also use the `page_filter` option to process only specified pages. If using `page_filter`,
`page_split` is implied, and you do not need to set it explicitly.

AI\_PARSE\_DOCUMENT is horizontally scalable, enabling efficient batch processing of multiple documents simultaneously.
Documents can be processed directly from object storage to avoid unnecessary data movement.

AI\_PARSE\_DOCUMENT supports documents on stages that use client-side or server-side encryption, including in accounts that
use PrivateLink or other [network policies](/user-guide/network-policies) that restrict public network access to stages.

## Examples

### Simple layout example

This example uses AI\_PARSE\_DOCUMENT’s LAYOUT mode to process a two-column research paper. The `page_split` parameter
is set to TRUE in order to separate the document into pages in the response. AI\_PARSE\_DOCUMENT returns the content in Markdown
format. The following shows rendered Markdown for one of the processed pages (page index 4 in the JSON output) next to
the original page. The raw Markdown is shown in the JSON response following the images.

| Page from the original document | Extracted Markdown rendered as HTML |
| --- | --- |
| A page from a scientific paper as it appears in a PDF document | The same page as it appears when the Markdown returned by AI_PARSE_DOCUMENT is rendered (as in a browser) |

Expand

Show lessSee more

Tip

To view either of these images at a more legible size, select it by clicking or tapping.

The following is the SQL command to process the original document:

Copy code

```
SELECT AI_PARSE_DOCUMENT (
    TO_FILE('@docs.doc_stage','research-paper-example.pdf'),
    {'mode': 'LAYOUT' , 'page_split': true}) AS research_paper_example;
```

The response from AI\_PARSE\_DOCUMENT is a JSON object containing metadata and text from the pages of the document, like
the following. Some page objects have been omitted for brevity.

```
{
  "metadata": {
    "pageCount": 19
  },
  "pages": [
    {
      "content": "# SwiftKV: Fast Prefill-Optimized Inference with Knowledge-Preserving Model Transformation \n\nAurick Qiao
      Zhewei Yao Samyam Rajbhandari Yuxiong He<br />Snowflake AI Research<br />San Mateo, CA, United States<br />Correspondence:
      aurick.qiao@ snowflake.com\n\n\n#### Abstract\n\nLLM inference for enterprise applications, such as summarization, RAG,
      and code-generation, typically observe much longer prompt than generations, leading to high prefill cost and response
      latency. We present SwiftKV, a novel model transformation and distillation procedure targeted at reducing the prefill
      compute (in FLOPs) of prompt tokens while preserving high generation quality. First, SwiftKV prefills later layers' KV
      cache using an earlier layer's output, allowing prompt tokens to skip those later layers. Second, SwiftKV employs a
      lightweight knowledge-preserving distillation procedure that can adapt existing LLMs with minimal accuracy impact. Third,
      SwiftKV can naturally incorporate KV cache compression to improve inference performance in low-memory scenarios. Our
      comprehensive experiments show that SwiftKV can effectively reduce prefill computation by $25-50 \\%$ across several LLM
      families while incurring minimum quality degradation. In the end-to-end inference serving, SwiftKV realizes up to $2
      \\times$ higher aggregate throughput and $60 \\%$ lower time per output token. It can achieve a staggering 560 TFlops/GPU
      of normalized inference throughput, which translates to 16 K tokens/s for Llama-3.1-70B. SwiftKV is open-sourced at
      https://github . com/snowflakedb/arctictraining.\n\n\n## 1 Introduction\n\nLarge Language Models (LLMs) are now an
      integral enabler of enterprise applications and offerings, including code and data co-pilots (Chen et al., 2021; Pourreza
      and Rafiei, 2024), retrieval augmented generation (RAG) (Lewis et al., 2020; Lin et al., 2024), summarization (Pu et al.,
      2023; Zhang et al., 2024), and agentic workflows (Wang et al., 2024; Schick et al., 2023). However, the cost and speed of
      inference determine their practicality, and improving the throughput and latency of LLM inference has become increasingly
      important.\n\nWhile prior works, such as model pruning (Ma et al., 2023; Sreenivas et al., 2024), KV cache compression
      (Hooper et al., 2024; Shazeer, 2019; Ainslie et al., 2023b; Chang et al., 2024), and sparse attention (Zhao et al., 2024;
      Jiang et al., 2024), have been developed to accelerate LLM inference, they typically significantly degrade the model
      quality or work best in niche scenarios, such as lowmemory environments or extremely long contexts requests (e.g. $>100
      \\mathrm{~K}$ tokens). On the other hand, production deployments are often compute-bound rather than memory-bound, and
      such long-context requests are rare amongst diverse enterprise use cases (e.g. those observed at Snowflake).\n\nIn this
      paper, we take a different approach to improving LLM inference based on the key observation that typical enterprise
      workloads process more input tokens than output tokens. For example, tasks like code completion, text-to-SQL,
      summarization, and RAG each submit long prompts but produce fewer output tokens (a 10:1 ratio with average prompt length
      between 500 and 1000 is observed in our production). In these scenarios, inference throughput and latency are often
      dominated by the cost of prompt processing (i.e. prefill), and reducing this cost is key to improving their performance.
      \n\nBased on this observation, we designed SwiftKV, which improves throughput and latency by reducing the prefill
      computation for prompt tokens. SwiftKV (Fig. 1) consists of three key components:\n\nModel transformation. SwiftKV rewires
      an existing LLM so that the prefill stage during inference can skip a number of later transformer layers, and their KV
      cache are computed by the last unskipped layer. This is motivated by the observation that the hidden states of later
      layers do not change significantly (see Sec. 3.2 and (Liu et al., 2024b)). With SwiftKV, prefill compute is reduced by
      approximately the number of layers skipped.\n\nOptionally, for low-memory scenarios, we",
      "index": 0
    },
    ...
    {
      "content": "Efficient Distillation. Since only a few $\\mathbf{W}_{Q K V}$ parameters need training, we can keep just a
      single copy of the original model weights in memory that are frozen during training, and add an extra trainable copy of
      the $\\mathbf{W}_{Q K V}$ parameters for layers $>l$ initialized using the original model (See Fig. 1).\n\nDuring
      training, we create two modes for the later layers $>l$, one with original frozen parameters using original architecture,
      and another with the SwiftKV re-wiring using new QKV projections i.e.,\n\n$$\n\\begin{aligned}\n& \\mathbf{y}_{\\text
      {teacher }}=\\mathbf{M}(\\mathbf{x}, \\text { SwiftKV }=\\text { False }) \\\\\n& \\mathbf{y}_{\\text {student }}=\\mathbf
      {M}(\\mathbf{x}, \\text { SwiftKV }=\\text { True })\n\\end{aligned}\n$$\n\nwhere $\\mathbf{y}$ is the final logits,
      $\\mathbf{M}$ is the model, and $\\mathbf{x}$ is the input. Afterwards, we apply the standard distillation loss (Hinton et
      al., 2015) on the outputs. After the distillation, the original KV projection layers $>l$ are discarded during inference.
      \n\nThis method allows us to distill Llama-3.1-8BInstruct on 680 M tokens of data in 3 hours using 8 H100 GPUs, and
      Llama-3.1-70B-Instruct in 5 hours using 32 H100 GPUs across 4 nodes. In contrast, many prune-and-distill (Sreenivas et
      al., 2024) and layer-skipping (Elhoushi et al., 2024) methods require much larger datasets (e.g. 10-100B tokens) and incur
      greater accuracy gaps than SwiftKV.\n\n### 3.5 Optimized Implementation for Inference\n\nLLM serving systems can be
      complex and incorporate many simultaneous optimizations at multiple layers of the stack, such as PagedAttention (Kwon et
      al., 2023), Speculative Decoding (Leviathan et al., 2023), SplitFuse (Holmes et al., 2024; Agrawal et al., 2024), and
      more. A benefit of SwiftKV is that it makes minimal changes to the model architecture, so it can be integrated into
      existing serving systems without implementing new kernels (e.g. for custom attention operations or sparse computation) or
      novel inference procedures.\n\nImplementation in vLLM and SGLang. To show that the theoretical compute reductions of
      SwiftKV translates to real-world savings, we integrated it with vLLM (Kwon et al., 2023) and SGLang (Zheng et al., 2024).
      Our implementation is compatible with chunked prefill (Holmes et al., 2024; Agrawal et al., 2024), which mixes chunks of
      prefill tokens and decode tokens in each minibatch. During each forward pass, after completing layer $l$, the KV-cache for
      the remaining layers ( $>l$ ) are immediately computed, and only the decode tokens are propagated through the rest of the
      model layers.\n\n## 4 Main Results\n\nWe evaluated SwiftKV in terms of model accuracy (Sec. 4.1) compared to the original
      model and several baselines, and end-to-end inference performance (Sec. 4.2) in a real serving system.\n\nDistillation
      datasets. Our dataset is a mixture of Ultrachat (Ding et al., 2023), SlimOrca (Lian et al., 2023), and OpenHermes-2.5
      (Teknium, 2023), totaling roughly 680M Llama-3.1 tokens. For more details, please see Appendix A.1.\n\nSwiftKV Notation.
      For prefill computation, we report the approximate reduction as $(L-l) / L$ due to SwiftKV, and for KV cache, we report
      the exact memory reduction due to AcrossKV. For example, SwiftKV $(l=L / 2)$ and 4-way AcrossKV is reported as $50 \\%$
      prefill compute reduction and $37.5 \\% \\mathrm{KV}$ cache memory reduction.\n\n### 4.1 Model Quality Impact of
      SwiftKV\n\nTable 2 shows the quality results of all models we evaluated, including Llama-3.1-Instruct, Qwen2.
      5-14B-Instruct, Mistral-Small, and Deepseek-V2. Of these models, we note that the Llama models span two orders of
      magnitude in size (3B to 405B), Llama-3.1-405B-Instruct uses FP8 (W8A16) quantization, and Deepseek-V2-Lite-Chat is a
      mixture-of-experts model that implements a novel latent attention mechanism (DeepSeek-AI et al., 2024).\n\nWe also compare
      with three baselines: (1) FFN-SkipLLM (Jaiswal et al., 2024), a training-free method for skipping FFN layers (no attention
      layers are skipped) based on hidden state similarity, (2) Llama-3.1-Nemotron-51B-Instruct (Sreenivas et al., 2024), which
      is pruned and distilled from Llama-3.1-70B-Instruct using neural architecture search on 40B tokens, and (3) DarwinLM-8.4B
      (Tang et al., 2025), which is pruned and distilled from Qwen2.5-14B-Instruct using 10B tokens.\n\nSwiftKV. For Llama,
      Mistral, and Deepseek, we find the accuracy degradation for $25 \\%$ SwiftKV is less than $0.5 \\%$ from the original
      models (averaged across tasks). Additionally, the accuracy gap is within $1-2 \\%$ even at $40-50 \\%$ SwiftKV. Beyond $50
      \\%$ SwiftKV, model quality drops quickly. For example, Llama-3.1-8B-Instruct incurs a 7\\% accuracy gap at $62.5 \\%$
      SwiftKV. We find that Qwen suffers larger degradations, at $1.1 \\%$ for $25 \\%$ SwiftKV and $7.4 \\%$ for $50 \\%$
      SwiftKV, which may be due to Qwen models having lower simularity between layer at 50-75\\% depth (Fig. 2). Even still,
      SwiftKV",
      "index": 4
    },
    ...
  ]
}
```

### Table structure extraction example

This example demonstrates extracting structural layout, including a table, from a 10-K filing. The following shows the
rendered results for one of the processed pages (page index 28 in the JSON output).

| Page from the original document | Extracted Markdown rendered as HTML |
| --- | --- |
| A page from an SEC 10-K filing as it appears in a PDF document | The same page as it appears when the Markdown returned by AI_PARSE_DOCUMENT is rendered (as in a browser) |

Expand

Show lessSee more

Tip

To view either of these images at a more legible size, select it by clicking or tapping.

The following is the SQL command to process the original document:

Copy code

```
SELECT AI_PARSE_DOCUMENT (
    TO_FILE('@docs.doc_stage','10K-example.pdf'),
    {'mode': 'LAYOUT', 'page_split': true}) AS sec_10k_example;
```

The response from AI\_PARSE\_DOCUMENT is a JSON object containing metadata and text from the pages of the document, like
the following. The results for all but the page previously shown have been omitted for brevity.

```
{
  "metadata": {
    "pageCount": 53
  },
  "pages": [
    {
      "content": ...
      "index": 0
    },
    ....
    {
      "content": "# Key Operational and Business Metrics \n\nIn addition to the measures presented in our interim condensed
      consolidated financial statements, we use the following key operational and business metrics to evaluate our business,
      measure our performance, develop financial forecasts, and make strategic decisions.\n\n|  | Three Months Ended March 31, |  |
      \n| :--: | :--: | :--: |\n|  | 2025 | 2024 |\n| Ending Paid Connected Fitness Subscriptions ${ }^{(1)}$ | 2,880,176 | $3,051,
      451$ |\n| Average Net Monthly Paid Connected Fitness Subscription Churn ${ }^{(1)}$ | $1.2 \\%$ | $1.2 \\%$ |\n| Ending Paid
      App Subscriptions ${ }^{(1)}$ | 572,775 | 675,190 |\n| Average Monthly Paid App Subscription Churn ${ }^{(1)}$ | $8.1 \\%$ |
      $9.0 \\%$ |\n| Subscription Gross Profit (in millions) | \\$ 288.8 | \\$ 298.1 |\n| Subscription Contribution (in millions) $
      { }^{(2)}$ | \\$ 304.9 | \\$ 316.4 |\n| Subscription Gross Margin | $69.0 \\%$ | $68.1 \\%$ |\n| Subscription Contribution
      Margin ${ }^{(2)}$ | $72.9 \\%$ | $72.3 \\%$ |\n| Net loss (in millions) | \\$ $(47.7)$ | \\$ $(167.3)$ |\n| Adjusted EBITDA
      (in millions) ${ }^{(3)}$ | \\$ 89.4 | \\$ 5.8 |\n| Net cash provided by operating activities (in millions) | \\$ 96.7 | \\$
      11.6 |\n| Free Cash Flow (in millions) ${ }^{(4)}$ | \\$ 94.7 | \\$ 8.6 |\n\n[^0]\n## Ending Paid Connected Fitness
      Subscriptions\n\nEnding Paid Connected Fitness Subscriptions includes all Connected Fitness Subscriptions for which we are
      currently receiving payment (a successful credit card billing or prepaid subscription credit or waiver). We do not include
      paused Connected Fitness Subscriptions in our Ending Paid Connected Fitness Subscription count.\n\n## Average Net Monthly
      Paid Connected Fitness Subscription Churn\n\nTo align with the definition of Ending Paid Connected Fitness Subscriptions
      above, our quarterly Average Net Monthly Paid Connected Fitness Subscription Churn is calculated as follows: Paid Connected
      Fitness Subscriber \"churn count\" in the quarter, divided by the average number of beginning Paid Connected Fitness
      Subscribers each month, divided by three months. \"Churn count\" is defined as quarterly Connected Fitness Subscription
      churn events minus Connected Fitness Subscription unpause events minus Connected Fitness Subscription reactivations.\n\nWe
      refer to any cancellation or pausing of a subscription for our All-Access Membership as a churn event. Because we do not
      receive payment for paused Connected Fitness Subscriptions, a paused Connected Fitness Subscription is treated as a churn
      event at the time the pause goes into effect, which is the start of the next billing cycle. An unpause event occurs when a
      pause period elapses without a cancellation and the Connected Fitness Subscription resumes, and is therefore counted as a
      reduction in our churn count in that period. Our churn count is shown net of reactivations and our new quarterly Average Net
      Monthly Paid Connected Fitness Subscription Churn metric averages the monthly Connected Fitness churn percentage across the
      three months of the reported quarter.\n\n## Ending Paid App Subscriptions\n\nEnding Paid App Subscriptions include all App
      One, App+, and Strength+ subscriptions for which we are currently receiving payment.\n\n## Average Monthly Paid App
      Subscription Churn\n\nWhen a Subscriber to App One, App+, or Strength+ cancels their membership (a churn event) and
      resubscribes in a subsequent period, the resubscription is considered a new subscription (rather than a reactivation that is
      counted as a reduction in our churn count). Average Paid App Subscription Churn is calculated as follows: Paid App
      Subscription cancellations in the quarter, divided by the average number of beginning Paid App Subscriptions each month,
      divided by three months.\n\n\n[^0]:    (1) Beginning January 1, 2025, the Company migrated its subscription data model for
      reporting Ending Paid Connected Fitness Subscriptions, Average Net Monthly Paid Connected Fitness Subscription Churn, Ending
      Paid App Subscriptions, and Average Monthly Paid App Subscription Churn to a new data model that provides greater visibility
      to changes to a subscription's payment status when they occur. The new model gives the Company more precise and timely data
      on subscription pause and churn behavior. Prior period information has been revised to conform with current period
      presentation. The impact of this change in the model on Ending Paid Connected Fitness Subscriptions, Average Net Monthly
      Paid Connected Fitness Subscription Churn, Ending Paid App Subscriptions and Average Monthly Paid App Subscription Churn for
      the three months ended March 31, 2025 and 2024 is immaterial.\n    (2) Please see the section titled \"Non-GAAP Financial
      Measures—Subscription Contribution and Subscription Contribution Margin\" for a reconciliation of Subscription Gross Profit
      to Subscription Contribution and an explanation of why we consider Subscription Contribution and Subscription Contribution
      Margin to be helpful measures for investors.\n    (3) Please see the section titled \"Non-GAAP Financial Measures—Adjusted
      EBITDA\" for a reconciliation of Net loss to Adjusted EBITDA and an explanation of why we consider Adjusted EBITDA to be a
      helpful measure for investors.\n    (4) Please see the section titled \"Non-GAAP Financial Measures-Free Cash Flow\" for a
      reconciliation of net cash provided by (used in) operating activities to Free Cash Flow and an explanation of why we
      consider Free Cash Flow to be a helpful measure for investors.",
      "index": 28
    },
    ...
    {
      "content": "# CERTIFICATION OF PRINCIPAL FINANCIAL OFFICER PURSUANT TO 18 U.S.C. SECTION 1350, AS ADOPTED PURSUANT TO
      SECTION 906 OF THE SARBANES-OXLEY ACT OF 2002 \n\nI, Elizabeth F Coddington, Chief Financial Officer of Peloton Interactive,
      Inc. (the \"Company\"), do hereby certify, pursuant to 18 U.S.C. Section 1350, as adopted pursuant to Section 906 of the
      Sarbanes-Oxley Act of 2002, that to the best of my knowledge:\n\n1. the Quarterly Report on Form 10-Q of the Company for the
      fiscal quarter ended March 31, 2025 (the \"Report\") fully complies with the requirements of Section 13(a) or 15(d) of the
      Securities Exchange Act of 1934, as amended; and\n2. the information contained in the Report fairly presents, in all
      material respects, the financial condition, and results of operations of the Company.\n\nDate: May 8, 2025\n\nBy: /s/
      Elizabeth F Coddington\nElizabeth F Coddington\nChief Financial Officer\n(Principal Financial Officer)",
      "index": 52
    }
  ]
}
```

### Slide deck example

This example demonstrates extracting structural layout from a presentation. Below we show the rendered results for one of the processed slides (page index 17 in the JSON output).

| Slide from the original document | Extracted Markdown rendered as HTML |
| --- | --- |
| A slide from a presentation as it appears in a PowerPoint deck | The same slide as it appears when the Markdown returned by AI_PARSE_DOCUMENT is rendered (as in a browser) |

Expand

Show lessSee more

Tip

To view either of these images at a more legible size, select it by clicking or tapping.

The following is the SQL command to process the original document:

Copy code

```
SELECT AI_PARSE_DOCUMENT (TO_FILE('@docs.doc_stage','presentation.pptx'),
    {'mode': 'LAYOUT' , 'page_split': true}) as presentation_output;
```

The response from AI\_PARSE\_DOCUMENT is a JSON object containing metadata and the text from the slides of the presentation,
like the following. The results for some slides have been omitted for brevity.

```
{
  "metadata": {
    "pageCount": 38
  },
  "pages": [
    {
      "content": "![img-0.jpeg](img-0.jpeg)\n\n# **SNOWFLAKE INVESTOR PRESENTATION**\n\nFirst Quarter Fiscal 2026\n\n© 2026 Snowflake Inc. All Rights Reserved",
      "index": 0
    },
    ...
    {
      "content": "# Our Consumption Model \n\n## Revenue Recognition Consumption\n\nSnowflake recognizes the substantial majority of its revenue as customers consume the platform\n\nPro: Enables faster growth\nPro: Aligned with customer value\nPro: Aligned with usage-based costs\nConsider: Revenue is variable based on customers' usage\n\n## Pricing Model Consumption\n\nThe platform is priced based on consumption of compute, storage, and data transfer resources\n\nPro: Customers don't pay for shelfware\n\nConsider: Performance improvements inherently reduce customer cost\n\n## Billings Terms Typically Upfront\n\nSnowflake typically bills customers annually in advance for their capacity contracts\n\nSome customers consume on-demand and/or are billed in-arrears\n\nPro: Bookings represent contractual minimum\n\nPro: Variable consumption creates upside for renewal cycle\n\nConsider: Payment terms are evolving",
      "index": 17
    },
    ...
    {
      "content": "![img-23.jpeg](img-23.jpeg)\n\n# PRODUCT REVENUE\n\n## $996.8M + 26% YoY Growth\n\n## NET REVENUE RETENTION RATE\n\n## $124%\n\n## TOTAL CUSTOMERS\n\n## $1M+ CUSTOMERS\n\n## $0.5 + 27% YoY Growth\n\nCustomers with Trailing 12-Month Product Revenue Greater than $1M\n\n## FORBES GLOBAL 2000 CUSTOMERS\n\n## $754 + 4% YoY Growth\n\n## SNOWFLAKE MARKETPLACE LISTINGS\n\n## AI/ML ADOPTION\n\n## 5,200+ Accounts using Snowflake AI/ML\n\n## SNOWFLAKE AI DATA CLOUD\n\n### Unified Platform and Connected Ecosystem\n\n- **Data Engineering**\n- **Analytics**\n- **AI**\n- **Applications & Collaboration**\n\n### Fully Managed | Cross-Cloud | Interoperable | Secure | Governed\n\n1. For the three months ended April 30, 2025.\n2. As of April 30, 2025. Please see our Q1FY26 earnings press release for definitions of net revenue retention rate, customers with trailing 12-month product revenue greater than $1 million (which definition includes a description of our total customer count), and Forbes Global 2000 customers.\n3. As of April 30, 2025. Each live dataset, package of datasets, or data service published by a data provider as a single product offering on Snowflake Marketplace is counted as a unique listing. A listing may be available in one or more regions where Snowflake Marketplace is available.\n4. Adoption is based on capacity and on-demand accounts using Snowflake AI/ML features on a weekly basis via our internal classification. We take the average of the last 4 weeks of the quarter ended April 30, 2025.",
      "index": 36
    },
    {
      "content": "# THANK YOU\n\n![img-24.jpeg](img-24.jpeg)",
      "index": 37
    }
  ]
}
```

### Multilingual document example

This example showcases AI\_PARSE\_DOCUMENT’s multilingual capabilities by extracting structural layout from a German
article. AI\_PARSE\_DOCUMENT preserves the reading order of the main text even when images and pull quotes are present.

| Page from the original document | Extracted Markdown rendered as HTML |
| --- | --- |
| A slide from a presentation as it appears in a PowerPoint deck | The same slide as it appears when the Markdown returned by AI_PARSE_DOCUMENT is rendered (as in a browser) |

Expand

Show lessSee more

Tip

To view either of these images at a more legible size, select it by clicking or tapping.

The following is the SQL command to process the original document. Since the document has a single page,
you do not need page splitting for this example.

Copy code

```
SELECT AI_PARSE_DOCUMENT (TO_FILE('@docs.doc_stage','german_example.pdf'),
    {'mode': 'LAYOUT'}) AS german_article;
```

The response from AI\_PARSE\_DOCUMENT is a JSON object containing metadata and the text from the document,
like the following.

```
{
  "metadata": {
    "pageCount": 1
  },
  "content": "![img-0.jpeg](img-0.jpeg)\n\nSchulen haben es verdient, gute Orte zu sein. Hier sollen wir Wissen und Fähigkeiten
  erlernen, die uns durch das Leben tragen. Hier verbringen viele einen Großteil ihres Tages, und das in einer Lebensphase, in
  der sich Zeit beinahe grenzenlos und eine Doppelstunde wie ein halbes Leben anfühlen kann.\n\nOb es die Freundin ist, ohne die
  man auf dem Schulhof verloren wäre. Der Lehrer, mit dem man nicht klarkommt, den man aber trotzdem jeden Tag aushalten muss.
  Die Klassenfahrt, auf der man zum ersten Mal das Meer sieht und knutscht. In Schulen entstehen Erfahrungen, Beziehungen und
  Erinnerungen, die uns ein ganzes Leben prägen.\n\nDie Erwartungen an Schulen sind dementsprechend hoch. Trotzdem werden sie
  von der Gesellschaft schnell vergessen und von der Politik hinten angestellt. Seit Jahrzehnten kriegt das deutsche Schulsystem
  verheerende Zeugnisse.\n\nNoch immer entscheiden Bildungsgrad und Kontostand der Eltern darüber, welchen Schulabschluss Kinder
  und Jugendliche machen. Noch immer funktioniert es vielerorts nur auf dem Papier, dass alle gut zusammen lernen. Im Alltag
  fehlen dann die Lehrkräfte und Mittel, um zum Beispiel einen geflüchteten Jugendlichen oder einen mit ADHS so zu unterstützen,
  dass alle möglichst gleichberechtigt in einem Klassenraum sitzen. Auch die gesellschaftliche Einsicht, dass alle
  Schulabschlüsse ihren Wert haben und gebraucht werden, muss erst wieder zurückgewonnen werden.\n\nJetzt aber hoch mit
  euch!\nDass Schule so irre früh anfangen muss, ist kein Gesetz. Und auch gar nicht ratsam: Jugendliche haben einen anderen
  Biorhythmus und brauchen mehr Schlaf als Erwachsene. Ein Schulbeginn gegen 9 oder 10 Uhr wäre für die meisten besser, da ist
  sich die Forschung einig\n\nAn Schulen tritt die Realität sehr schnell ein. Während sich die Gesellschaft noch fragt, wie mit
  künstlicher Intelligenz umzugehen ist, nutzen sie Lehrkräfte, Schülerinnen und Schüler längst für ihre Zwecke. Während über
  Jahre diskutiert wurde, ob Deutschland ein Einwanderungsland sei, war es das an Schulen längst. Und während andere Themen den
  Klimawandel in der Öffentlichkeit verdrängen, sind es besonders Schülerinnen und Schüler, die laut auf das drängendste Problem
  unserer Zeit hinweisen. Die Herausforderungen und Fragen, die sich an Schulen stellen, betreffen uns alle. Schule ist Zukunft.
  \n\nSchulleitungen, Lehrkräfte, pädagogisches Personal und alle, die sich sonst noch um das Gelingen des Schulalltags kümmern,
  stellen sich dem jeden Tag aufs Neue. Sie versuchen, Schule trotz vieler Probleme und fehlender Wertschätzung zu gestalten,
  sie versuchen, den Schülerinnen und Schülern zu vermitteln, dass es auf sie ankommt. Damit sie selbst an sich glauben. Sie
  haben es verdient.",
}
```

Snowflake Cortex can produce a translation to any supported language (English, language code `'en'`, in this case) as follows:

Copy code

```
AI_TRANSLATE(ger_example, '', 'en') from german_article;
```

The translation is as follows:

```
"Schools deserve to be good places. Here, we are supposed to learn knowledge and skills that will carry us through life. Many
spend a large part of their day here, and this is during a phase of life when time can seem almost endless and a double period
can feel like half a lifetime.

Whether it's the friend you would be lost without in the schoolyard. The teacher you can't get along with, but still have to
endure every day. The class trip where you see the sea for the first time and make out. In schools, experiences,
relationships, and memories are created that shape us for a lifetime.

The expectations for schools are correspondingly high. Nevertheless, they are quickly forgotten by society and pushed to the
back by politics. For decades, the German school system has been receiving devastating reports.

Even now, the level of education and the financial status of the parents still determine which school certificate children and
young people receive. It still only works on paper that everyone learns well together. In everyday life, the teachers and
resources are lacking to support, for example, a refugee youth or a student with ADHD so that they can sit in a classroom on
an equal footing. The societal insight that all school certificates have value and are needed also needs to be regained.

Now, let's get going!

The fact that school has to start so early is not a law. And it's not advisable either: teenagers have a different biological
rhythm and need more sleep than adults. A start time of 9 or 10 o'clock would be better for most, research agrees.

Reality sets in very quickly at schools. While society is still wondering how to deal with artificial intelligence, teachers,
students, and pupils are already being used for their purposes. While it was debated for years whether Germany is an
immigration country, it has been one in schools for a long time. And while other topics are pushing climate change out of the
public eye, it is especially students who are loudly pointing out the most pressing problem of our time. The challenges and
questions that schools face affect us all. School is the future.

School administrations, teachers, educational staff, and all those who take care of the success of everyday school life face
this every day. They try to shape school despite many problems and lack of appreciation, they try to convey to the students
that it's up to them. So that they believe in themselves. They deserve it."
```

### Using OCR mode

OCR mode extracts text from scanned documents, such as screenshots or PDFs containing images of text.
It does not preserve layout.

Copy code

```
SELECT AI_PARSE_DOCUMENT(
  TO_FILE( '@docs.doc_stage', 'document_1.pdf' ),
  { 'mode': 'OCR' } ) AS OCR;
```

Output:

```
{
  "content": "content of the document"
}
```

### Process only certain pages of a document

This example demonstrates using the `page_filter` option to extract specific pages from a document, specifically
the first page of a 55-page research paper. Keep in mind that page indexes start at 0 and ranges are inclusive of
the start value but exclusive of the end value. For example, `start: 0, end: 1` returns only the first page (index 0).

Copy code

```
SELECT AI_PARSE_DOCUMENT(
  TO_FILE('@my_documents', 'ResearchArticle.pdf'),
  {'mode': 'LAYOUT', 'page_filter': [{'start': 0, 'end': 1}]} );
```

Result:

```
{
  "metadata": {
    "pageCount": 55
  },
  "pages": [
    {
      "content": "# The Critical Role of Strength Training in Lifelong Health: Evidence-Based
      Benefits and Implementation Strategies \n\n\n#### Abstract\n\nBackground: Strength training
      has emerged as one of the most powerful interventions for promoting health across the
      lifespan. This comprehensive review examines the extensive evidence supporting strength
      training's role in preventing chronic disease, maintaining functional independence, and
      enhancing quality of life.\n\nMethods: We conducted a systematic review of peer-reviewed
      literature published between 2018-2024, analyzing 127 studies involving over 45,000
      participants across various populations.\n\nResults: Regular resistance exercise provides
      cardiovascular benefits ( $15-20 \\%$ reduction in heart disease risk), metabolic improvements
      ( $12-18 \\%$ better insulin sensitivity), cognitive enhancements ( $25 \\%$ slower
      cognitive decline), and psychological well-being improvements. Strength training increases
      bone mineral density by $1-3 \\%$ annually and reduces fall risk by up to $40 \\%$ in older
      adults.\n\nConclusions: Current guidelines recommend at least two sessions per week targeting
      all major muscle groups. Implementation of strength training programs should be considered a
      public health priority given the substantial evidence for disease prevention and health
      promotion.\n\n\nKeywords: resistance training, muscle strength, bone density, chronic
      disease prevention, healthy aging, exercise prescription\n\n## Introduction\n\nThe human
      musculoskeletal system is designed for regular mechanical loading and progressive challenge.
      Throughout evolutionary history, our ancestors engaged in strength-demanding activities
      essential for survival, maintaining robust muscle mass and bone density well into advanced age.
      However, the modern sedentary lifestyle has created an unprecedented mismatch between our
      biological needs and daily activities, contributing to rising rates of sarcopenia,
      osteoporosis, and metabolic dysfunction.\n\nStrength training, also known as resistance
      training or weight training, represents a targeted intervention that can address many
      contemporary health challenges. Unlike aerobic exercise alone, resistance training provides
      unique physiological adaptations that are essential for long-term health and functional
      independence. The World Health Organization now recognizes strength training as a fundamental
      component of physical activity guidelines for all adults.\n\nKey Statistics: Only 31\\% of
      adults meet strength training recommendations, despite evidence showing $20-30 \\%$ reductions
      in all-cause mortality among regular participants.\n\n## Physiological Mechanisms and
      Adaptations\n\n## Musculoskeletal Benefits\n\nStrength training stimulates muscle protein
      synthesis through mechanistic target of rapamycin (mTOR) pathway activation, leading to
      increased muscle fiber size and improved neuromuscular coordination. Research demonstrates
      that adults can increase muscle mass by $2-4 \\%$ per month during initial training phases,
      with continued improvements possible throughout life.\n\nBone tissue responds to mechanical
      loading through osteoblast activation and increased bone formation. Weight-bearing resistance
      exercises create piezoelectric effects that stimulate osteocyte networks, resulting in
      improved bone mineral density and reduced fracture risk. Studies show 1-3\\% annual",
      "index": 0
    }
  ]
}
```

### Classify multiple documents

To classify multiple documents, first create a table of the files by retrieving the document locations from a
directory, converting these locations to FILE objects.

Copy code

```
CREATE TABLE documents_table AS
  (SELECT TO_FILE('@my_documents', RELATIVE_PATH)
    AS docs FROM DIRECTORY(@my_documents));
```

Then apply AI\_PARSE\_DOCUMENT to each document in the table and process the results, for example by passing them
to AI\_CLASSIFY to categorize the documents by type. This is an efficient approach to batch document analysis in a
document collection.

Copy code

```
WITH single_page_extraction as (
  SELECT
  TO_VARCHAR (AI_PARSE_DOCUMENT(docs, {'mode': 'LAYOUT',
    'page_filter': [{'start': 0, 'end': 1}]} )) AS first_page FROM documents_table)
SELECT AI_CLASSIFY(
  first_page,
  ['health', 'fitness','economics', 'science', 'psychology' ,'sociology','statistics', 'finance', 'Artificial Intelligence', 'Analytics'],
  {'output_mode': 'multi'} ) as article_classification
FROM single_page_extraction;
```

The query returns classification labels for each document.

```
{ "labels": [ "health", "psychology", "science" ] }
{ "labels": [ "fitness", "health", "science" ] }
{ "labels": [ "Analytics", "Artificial Intelligence" ] }
{ "labels": [ "finance", "Analytics" ] }

..

{ "labels": [ "finance" ] }
{ "labels": [ "Artificial Intelligence", "science" ] }
{ "labels": [ "Artificial Intelligence", "science" ] }
{ "labels": [ "fitness", "health", "science" ] }
```

### Extract and describe images

AI\_PARSE\_DOCUMENT can extract images embedded in documents alongside text and layout, enabling high-fidelity, multimodal
document processing workflows.

To extract images from a document, set the `'mode'` option to `'LAYOUT'` (image extraction requires LAYOUT mode) and
set the `'extract_images'` option to TRUE. AI\_PARSE\_DOCUMENT returns an array, `images`, in the JSON output. Each
element of `images` contains a field, `image_base64`, with the extracted image data encoded as a base64 string.
Image OBJECT\_CONSTRUCT also contains fields for a unique ID and image bounding boxes.

Copy code

```
SELECT AI_PARSE_DOCUMENT(
    TO_FILE('@my_stage', 'my_document.pdf'),
    {'mode': 'LAYOUT', 'extract_images': true})
AS layout_with_images;
```

After extracting image data, you can decode the images using BASE64\_DECODE\_BINARY and pass them directly to AI\_EXTRACT
to process or describe the image contents. The following example generates a description for the first extracted image
after converting it to binary from base64. (AI\_EXTRACT requires binary input.) The query uses a regular expression to
strip the metadata (schema and format) from the base64 string.

Copy code

```
SELECT AI_EXTRACT(
file_data => BASE64_DECODE_BINARY(
    REGEXP_REPLACE(
    (
        SELECT (
            AI_PARSE_DOCUMENT(
                TO_FILE('@image_docs', 'my_document.pdf'),
                {'mode': 'LAYOUT', 'extract_images': true}
            ):images[0]['image_base64']
            )::STRING
        ),
    '^data:image/[^;]+;base64,', '')
    ),
responseFormat => {'Image Name': 'Describe the image'}
);
```

Alternatively, you can store extracted images in a Snowflake stage for reuse, auditing, or additional processing with
other Cortex AI functions, such as multimodal AI\_COMPLETE. (AI\_COMPLETE does not currently support direct image input.)
The following example creates and uses a Python stored procedure to decode base64 image data from AI\_PARSE\_DOCUMENT and
upload the resulting image files to a specified stage.

Copy code

```
CREATE OR REPLACE PROCEDURE SAVE_EXTRACTED_IMAGES(r VARIANT)
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('pillow', 'snowflake-snowpark-python')
HANDLER = 'run'
AS
$$
import base64
import io
import os
import tempfile
from PIL import Image

def process_parse_document_result(data: dict) -> tuple[str, str, str]:
    images = data["images"]
    for image in images:
        id = image["id"]
        data, image_base64 = image["image_base64"].split(";", 1)
        extension = data.split("/")[1]
        base64 = image_base64.split(",")[1]
        yield id, extension, base64

def decode_base64(encoded_image: str) -> bytes:
    return base64.b64decode(encoded_image)

def run(session, r):
    destination_path = r["DESTINATION_PATH"]
    parse_document_result = r["PARSE_DOCUMENT_RESULT"]

    if not destination_path:
        return ["Error: destination_path parameter is required"]
    if not destination_path.startswith("@"):
        return ["Error: destination_path must start with @ (e.g. @output_stage/path"]
    if destination_path == "@":
        return ["Error: destination_path must include a stage name after @"]

    # Clean the result directory
    session.sql(f"RM destination_path")

    uploaded_files = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for image_id, extension, encoded_image in process_parse_document_result(parse_document_result):
            image_bytes = decode_base64(encoded_image)
            image: Image = Image.open(io.BytesIO(image_bytes))

            image_path = os.path.join(temp_dir, image_id)
            image.save(image_path)

            session.file.put(
                image_path, destination_path, auto_compress=False, overwrite=True
            )
            uploaded_files.append(f"{destination_path}/{image_id}")

            os.remove(image_path)
    return uploaded_files
$$;
```

After creating the SAVE\_EXTRACTED\_IMAGES procedure, you can call it to extract images from a document and store them in
a stage, as shown in the following code snippet:

Copy code

```
CALL SAVE_EXTRACTED_IMAGES(
(
SELECT OBJECT_CONSTRUCT(*)
FROM ( SELECT
    '@image_docs/output' as destination_path,
    AI_PARSE_DOCUMENT(
    TO_FILE('@image_docs/my_document.pdf'),
    {'mode': 'LAYOUT', 'extract_images': true}
    ) as parse_document_result
) LIMIT 1
));
```

The output of this query is a list of file paths for the images stored in the specified stage, such as:

```
image_docs/output/img-0.jpeg
image_docs/output/img-1.jpeg
image_docs/output/img-10.jpeg
image_docs/output/img-11.jpeg
image_docs/output/img-12.jpeg
image_docs/output/img-13.jpeg
```

Now you can process the stored images using other Cortex AI functions, such as AI\_COMPLETE for multimodal analysis or
generation.

Copy code

```
SELECT AI_COMPLETE(
    'pixtral-large',
    'Describe the image in 10 words.',
    TO_FILE('@image_docs/output/img-0.jpeg')
);
```

Response:

```
The image shows central bank policy rates for various countries from 2000 to 2025.
```

Note

Image extraction has the following limitations:

- No more than 50 images can be extracted from a single document. Additional images are ignored.
- Images smaller than 4x4 pixels are not extracted.

Extracting images does not incur additional costs. Billing for AI\_PARSE\_DOCUMENT is based on the number of pages
processed; a single image file is considered a page.

## Input requirements

AI\_PARSE\_DOCUMENT is optimized for both digital-born and scanned documents. The following table lists the limitations and
requirements of input documents:

|  |  |
| --- | --- |
| Maximum file size | 100 MB |
| Maximum pages per document | 2,000 |
| Maximum page resolution | - 10000 x 10000 pixels - 33.3 x 33.3 inches (at 300 DPI) - 2400 x 2400 pts (at 300 DPI) |
| Supported file type | PDF, PPTX, DOCX, JPEG, JPG, PNG, TIFF, TIF, HTML, TXT |
| Stage encryption | Client-side or server-side encryption |
| Font size | 8 points or larger for best results |

Expand

Show lessSee more

## Supported document features and limitations

|  |  |
| --- | --- |
| Page orientation | AI\_PARSE\_DOCUMENT automatically detects page orientation. |
| Page splitting | AI\_PARSE\_DOCUMENT can split multi-page documents into individual pages and parse each separately. The output is split per page. |
| Page filtering | AI\_PARSE\_DOCUMENT can process some of the pages in a document, instead of all of them, by specifying page ranges. This is useful when you know what pages the information you’re looking for is on. |
| Characters | AI\_PARSE\_DOCUMENT detects the following characters:   - a-z - A-Z - 0-9 - À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô   Õ Ö Ø Ù Ú Û Ü Ý Þ ß à á â ã ä å æ ç è é ê   ë ì í î ï ð ñ ò ó ô õ ö ÷ ø ù ú û ü ý þ ÿ   Ą ą Ć ć Č č Đ đ Ę ę ı Ł ł Ń ń ō Œ œ Ś ś Š   š Ÿ Ź ź Ż ż Ž ž ʒ β δ ε з Ṡ - ! “ # $ % & ‘ ( ) \* + , - . / : ; < = > ?   @ [ ] ^ \_ ` { | } ~ ¡ ¢ £ ¥ § © ª « ­ ® ¯   ° ± ² ³ ´ µ ¶ · º » ¿ ‘ † ‡ • ‣ ⁋ ₣ ₤ ₦   ₩ € ₭ ₹ ™ ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↰ ↱ ↲ ↳ ↴   ↵ |
| Images | AI\_PARSE\_DOCUMENT can extract embedded images from documents (up to 50 images per document) in addition to generating markup for them. See [Extract and describe images](#label-parse-document-extract-images) for details. |
| Structured elements | AI\_PARSE\_DOCUMENT automatically detects and extracts tables and forms. |
| Fonts | AI\_PARSE\_DOCUMENT recognizes text in most serif and sans-serif fonts, but may have difficulty with decorative or script fonts. The function also recognizes handwriting. |

Expand

Show lessSee more

### Supported languages

AI\_PARSE\_DOCUMENT is trained for the following languages in both OCR and LAYOUT modes:

- Chinese
- English
- French
- German
- Hindi
- Italian
- Norwegian
- Polish
- Portuguese
- Romanian
- Russian
- Spanish
- Swedish
- Turkish
- Ukrainian

## Regional availability

Support for AI\_PARSE\_DOCUMENT is available to accounts in the following Snowflake regions:

| AWS | Azure | Google Cloud Platform |
| --- | --- | --- |
| US West 2 (Oregon) | East US 2 (Virginia) | US Central 1 (Iowa) |
| US East (Ohio) | West US 2 (Washington) | Middle East Central 2 (Dammam) |
| US East 1 (N. Virginia) | Europe (Netherlands) |  |
| Europe (Ireland) |  |  |
| Europe Central 1 (Frankfurt) |  |  |
| Europe West 2 (London) |  |  |
| Asia Pacific (Sydney) |  |  |
| Asia Pacific (Tokyo) |  |  |

Expand

Show lessSee more

AI\_PARSE\_DOCUMENT has cross-region support in other Snowflake regions. For information on enabling Cortex AI cross-region support, see [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

## Access control requirements

To use the AI\_PARSE\_DOCUMENT function, a user with the ACCOUNTADMIN role must grant the SNOWFLAKE.CORTEX\_USER database role to the user who
will call the function. See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) topic for details.

## Cost considerations

The Cortex AI\_PARSE\_DOCUMENT function incurs compute costs based on the number of pages per document processed. The following describes how pages are counted for different file formats:

- For paged file formats (PDF, DOCX), each page in the document is billed as a page.
- For image file formats (JPEG, JPG, TIF, TIFF, PNG), each individual image file is billed as a page.
- For HTML and TXT files, each chunk of 3,000 characters is billed as a page, including the last chunk, which may be less than 3,000 characters.

Snowflake recommends executing queries that call the Cortex AI\_PARSE\_DOCUMENT function in a smaller warehouse (no larger
than MEDIUM). Larger warehouses do not increase performance.

## Error conditions

Snowflake Cortex AI\_PARSE\_DOCUMENT can produce the following error
messages:

| Message | Explanation |
| --- | --- |
| `Document contains language that is not supported.` | Input document contains unsupported language. |
| `The provided file format {file_extension} isn't supported. Supported formats: .['.docx', '.pptx', '.pdf'].` | The document is in unsupported format. |
| `The provided file format .bin isn't supported. Supported formats: ['.docx', '.pptx', '.pdf']. Ensure the file is stored with server-side encryption.` | The file format is not supported and understood as a binary file. |
| `Maximum number of 2000 pages exceeded. The document has {actual_pages} pages.` | The document exceeds the 2,000-page limit. |
| `Page size in pixels exceeds 10000x10000. The page size is {actual_px} pixels.` | Image input or a converted document page is larger than the supported dimensions. |
| `Page size in inches exceeds 50x50 (3600x3600 pt). The page size is {actual_in} inches ({actual_pt} pt).` | Page is larger than the supported dimensions. |
| `Maximum file size of 104857600 bytes exceeded. The file size is {actual_size} bytes.` | The document is larger than 100 MB. |
| `Provided file cannot be found.` | The file does not exist. |
| `Provided file cannot be accessed.` | The file can’t be accessed due to insufficient privileges. |
| `The Parse Document function did not respond in the allowed time.` | Timeout occurred. |
| `Internal error.` | System error occurred. Wait and try again. |

Expand

Show lessSee more

## Legal notices

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
