# AI\_COMPLETE with documents

The Cortex AI\_COMPLETE function is a general purpose AI Function that can understand data stored in PDF, Microsoft Word,
and other document file formats. You can use AI\_COMPLETE to perform a variety of document data extraction tasks, such as:

- Answer questions using data in graphs and charts.
- Finding relations between charts and document text.
- Summarizing document content in the a specific question.
- Extracting entities from documents.

An advantage of AI\_COMPLETE over other [document processing AI Functions](/user-guide/snowflake-cortex/ai-documents) is the ability to choose a
model, so you can use the best model for your specific document processing task.

## Processing documents with AI\_COMPLETE

The COMPLETE function processes documents files stored in an internal Snowflake stage or an external stage. The
completion prompt can reference a single document or multiple documents. For example, you compare the correctness of a
translation of marketing materials by providing the original and translated documents as input to the function, along
with a prompt asking the model to evaluate the translation quality.

When calling the function, you must specify the model to use and a prompt. The prompt should include instructions along
with a FILE object reference for each document you want to process. See [Examples](#examples) for sample prompts and completions, and
[AI\_COMPLETE (Prompt object)](/sql-reference/functions/ai_complete-prompt-object) for function call syntax.

### Input requirements

AI\_COMPLETE is optimized for documents both digital-born and scanned. The following table lists the limitations and
requirements of input documents:

| Supported file type | All models: .txt, .md, .pdf Claude models: .txt, .md, .pdf, .doc, .docx, .xls, .xlsx, .csv, .xhtml |
| --- | --- |
| Stage encryption | Server-side encryption |
| Data type | [FILE](/sql-reference/functions/to_file) object |

Expand

Show lessSee more

Note

Processing files from stages with AI\_COMPLETE is currently incompatible with custom network policies.

### Examples

The following examples illustrate how to use AI\_COMPLETE to process documents for three common use cases: chart Q&A,
contextualized document summarization, and technical report exploration.

## Chart Q&A example

![Title page of "Breaking the Gridlock" EU report](/static/images/cortex-functions/breaking-the-gridlock.png)

The following example uses Anthropic’s Claude Opus 4 model to analyze data represented in a chart within the context of
the document `hdr2023-24snapshoten.pdf` stored in the `@docs` stage.

Copy code

```
SELECT AI_COMPLETE(
  MODEL => 'claude-4-opus',
  PROMPT => PROMPT('Compare the distributions of HDI in each group: low HDI group, medium HDI group, high HDI group and very high HDI group visualized in {0}', TO_FILE('@docs', 'hdr2023-24snapshoten.pdf'))
);
```

Response:

```
Looking at the document, I can see Figure S.2 on page 6 which shows the recovery of HDI values since the 2020-2021
decline across different HDI groups. The visualization shows:

**Low HDI group**:
- 49% recovered
- 51% did not recover

**Medium HDI group**:
- The document doesn't provide specific recovery percentages for this group in the figure

**High HDI group**:
- The document doesn't provide specific recovery percentages for this group in the figure

**Very high HDI group**:
- 100% recovered (all OECD countries)

The document also provides additional insights about HDI distributions:

1. **Inequality trends** (Figure S.3, page 7): The inequality between very high HDI and low HDI countries has been
   increasing since 2020, reversing a long-term declining trend. The difference in HDI values between these groups
   increased from 0.38 in 2017 to 0.39 in 2020 and is projected to continue rising.

2. **Overall recovery patterns**: The text notes that "every Organisation for Economic Co-operation and Development
   country is projected to have recovered, but only about half of the Least Developed Countries are projected to have
   done so."

3. **Global HDI trajectory**: While the global HDI value is projected to reach a record high in 2023, it remains below
   its pre-2019 trend, suggesting a permanent shift in the development trajectory.

The document emphasizes the highly unequal nature of recovery across HDI groups, with countries in higher HDI
categories showing much stronger recovery rates than those in lower HDI categories.
```

## Contextualized document summarization example

![First page of EU Resolution 1008/2008](/static/images/cortex-functions/eu-resolution-1008-2008.png)

The following example uses Anthropic’s Claude Sonnet 4 model to extract the summary of a legal text with a complex
layout. The document `CELEX_32008R1008_EN_TXT.pdf` is stored inthe @docs stage; the prompt narrows the summarization
context.

Copy code

```
SELECT AI_COMPLETE(
  MODEL => 'claude-4-sonnet',
  PROMPT => PROMPT('summarize the changes from the perspective of private aviation {0}', TO_FILE('@docs', 'CELEX_32008R1008_EN_TXT.pdf'))
);
```

Response:

```
From a private aviation perspective, this EU Regulation 1008/2008 introduces several significant changes that affect
private operators and business aviation:

## Key Changes Affecting Private Aviation:

### **Operating License Requirements**
- **Stricter financial oversight**: Private operators must demonstrate they can meet financial obligations for 24
  months from start of operations, with enhanced monitoring during the first two years
- **Simplified requirements for smaller operators**: Aircraft under 10 tonnes MTOM and/or less than 20 seats need
  only demonstrate €100,000 net capital (unless operating scheduled services or exceeding €3 million turnover)

### **Aircraft Registration and Leasing**
- **Flexible registration**: Private operators can register aircraft either in their home Member State or anywhere within the Community

- **Wet lease restrictions**: Stricter limitations on wet leasing aircraft from third countries, requiring prior
  approval and justification based on:
  - Exceptional needs (up to 7 months, renewable once)
  - Seasonal capacity requirements
  - Operational difficulties when EU-registered aircraft unavailable
- **Safety equivalence**: All third-country leased aircraft must meet equivalent safety standards to EU requirements.

### **Enhanced Supervision**

- **Unified oversight**: The same Member State authority now oversees both the Air Operator Certificate (AOC) and
  operating license, improving efficiency for operators with bases in multiple countries
- **Regular assessments**: Mandatory financial reviews, particularly after two years of operation and when potential
  problems are suspected

### **Insurance Requirements**
- **Extended coverage**: Insurance requirements now explicitly include mail liability coverage in addition to
  passengers, cargo, and third parties

### **Operational Flexibility**
- **Code-sharing freedom**: Private operators can more freely enter into code-share arrangements on intra-Community
  routes and routes to third countries
- **Pricing freedom**: Complete freedom to set fares and rates for intra-Community services

### **Administrative Streamlining**
- **Consolidated regulation**: The three separate regulations are now combined into one comprehensive framework,
  simplifying compliance
- **Reduced bureaucracy**: Member States cannot require documents already provided to licensing authorities

These changes generally **liberalize** private aviation operations within the EU while **strengthening** financial
and safety oversight, creating a more integrated and competitive market for private operators.
```

## Technical report exploration

![First page of 75mm gun specification booklet](/static/images/cortex-functions/gun-75mm-specification.png)

The following example uses the Gemini 3.1 Pro model to analyze casualty data represented in the diagrams of a technical report. The document `75mm-M3-spec-booklet-MK-VI.pdf` is stored in the `@docs` stage.

Copy code

```
SELECT AI_COMPLETE(
  MODEL => 'gemini-3.1-pro',
  PROMPT => PROMPT('explain findings from figures 69-73 of {0}', TO_FILE('@docs', '75mm-M3-spec-booklet-MK-VI.pdf'))
);
```

Response:

```
Based on the provided document, specifically **page 4**, here is an explanation of the findings from Figures 69
through 73. These figures illustrate the fragmentation patterns and effectiveness of the **75-mm Shell, H.E., M48**
when fired from an M3 Gun. They visualize how dangerous the shell is to personnel (casualties) and equipment
(perforation of mild steel) at different burst heights and orientations.
```

### Supported models and limitations

All models available to Snowflake Cortex have limitations on the total number of input and output tokens, known as the
model’s *context window.* The context window size is measured in tokens. Inputs exceeding the context window limit
result in an error.

For text models, tokens generally represent approximately four characters of text; the word count corresponding to a
limit is somewhat less than the context window given in tokens. For image models, the token count per document depends
on the vision model’s architecture. Tokens within a prompt (e.g., “summarize this document:”) also contribute to the
model’s context window.

| Model | Context window (tokens) | File types | File size | Max pages | Documents per prompt |
| --- | --- | --- | --- | --- | --- |
| `gemini-3.1-pro` | 1,000,000 | .pdf, .txt, .md | 37.5MB | 3,000 | 20 |
| `gemini-3.5-flash` | 1,000,000 | .pdf, .txt, .md | 37.5MB | 1,000 | 20 |
| `claude-4-sonnet` | 200,000 | .txt, .md, .pdf, .doc, .docx, .xls, .xlsx, .csv, .xhtml | 22MB | 100 | 5 |
| `claude-4-opus` | 200,000 | .txt, .md, .pdf, .doc, .docx, .xls, .xlsx, .csv, .xhtml | 22MB | 100 | 5 |
| `claude-haiku-4-5` | 200,000 | .txt, .md, .pdf, .doc, .docx, .xls, .xlsx, .csv, .xhtml | 22MB | 100 | 5 |
| `claude-sonnet-4-5` | 200,000 | .txt, .md, .pdf, .doc, .docx, .xls, .xlsx, .csv, .xhtml | 22MB | 100 | 5 |
| `claude-opus-4-5` | 200,000 | .txt, .md, .pdf, .doc, .docx, .xls, .xlsx, .csv, .xhtml | 22MB | 100 | 5 |
| `claude-sonnet-4-6` | 1,000,000 | .txt, .md, .pdf, .doc, .docx, .xls, .xlsx, .csv, .xhtml | 22MB | 100 | 5 |

Expand

Show lessSee more

### Access control requirements

To use the AI\_COMPLETE function, a user with the ACCOUNTADMIN role must grant the SNOWFLAKE.CORTEX\_USER database role to the user who
will call the function. See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) topic for details.

Users must also have READ access to the stage and file being processed.

### Cost considerations

Cost is determined by the total number of [tokens processed](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations), not by file
size. When documents are uploaded, textual content is extracted and converted into tokens; visual page segments (images)
are also transformed into tokens. Billing is based on the sum of input tokens (text plus images that the model reads)
and output tokens (text the model generates).

Actual token counts vary based on the underlying architecture of a model, as well as the document composition and
structure. Content such as dense tables, spreadsheets, structured data, code, repeated headers and footers, or
OCR-derived text may increase token volume. Conversely, image-heavy or slide-based documents with minimal extractable
text may result in lower token counts.

Note

The AI\_COUNT\_TOKENS function does not currently support document inputs in multimodal models.

### Choosing a model

The [MMLongBench-Doc](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ae0e43289bffea0c1fa34633fc608e92-Abstract-Datasets_and_Benchmarks_Track.html)
benchmark is used for evaluating model capabilities in multimodal and long context comprehension, including cross page information retrieval.

| Model | MMLongBench-Doc score |
| --- | --- |
| claude-3-7-sonnet | 52.8% |
| claude-4-sonnet | 50.2% |
| claude-4-opus | 53.0% |
| claude-haiku-4-5 | 48.9% |
| claude-sonnet-4-5 | 61.4% |
| claude-opus-4-5 | 63.8% |
| claude-sonnet-4-6 | 62.3% |
| gemini-3.1-pro | 60.5% |

Expand

Show lessSee more

### Regional availability

See [Regional availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

### Error conditions

Snowflake Cortex AI\_COMPLETE can produce the following error messages:

| Message | Explanation |
| --- | --- |
| \_COMPLETE\_WITH\_PROMPT\_HISTORY\_LLM$V1 with remote service error: 400 ‘”invalid request parameters: unsupported document content type: application/vnd.ms-excel” | The selected file of an unsupported type (in this example, a Microsoft Excel file). Only Claude models support Excel files. |
| Request failed for external function \_COMPLETE\_WITH\_PROMPT\_HISTORY\_LLM$V1 with remote service error: 400 ‘”invalid request parameters: File data exceeds the limit of 10.00 MB for file prefix/file.pdf” | File size exceeds limit (10MB in this example). |
| Remote file [‘@docs/file.pdf](mailto:'@docs/file.pdf)’ was not found. There are several potential causes. The file might not exist. The required credentials may be missing or invalid. If you are running a copy command, please make sure files are not deleted when they are being loaded or files are not being loaded into two different tables concurrently with auto purge option. | Possibly an error in the filename. Filenames are case-sensitive. Or the file might have been deleted. |
| Error in secure object | May indicate that the stage does not exist. Check the stage name and ensure that the stage exists and is accessible. Be sure to use an at sign (@) at the beginning of the stage name. Ensure that the stage uses server-side encryption. |
| Request failed for external function COMPLETE$V6 with remote service error: 400 ‘”model “model\_name” does not support given modality” | The model provided in the request doesn’t support document or text modality. |
| Request failed for external function \_COMPLETE\_WITH\_PROMPT with remote service error: 500 ‘”internal error” | Issue with processing the request on the server side. It could be the case that the file is corrupted or truncated. |

Expand

Show lessSee more

### Legal notices

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
