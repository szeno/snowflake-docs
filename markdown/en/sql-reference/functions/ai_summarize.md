Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_SUMMARIZE

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

AI\_SUMMARIZE is a managed Cortex AI function for summarizing text and multimodal content. It accepts either a
TEXT input or a FILE reference to an image or document and returns a concise summary as TEXT. AI\_SUMMARIZE
automatically identifies key themes, facts, and relationships in the input, making it easy to summarize
long-form text, images, and complex documents with a single function. The function supports multilingual
content, although summary quality can vary by language.

## Syntax

For TEXT input:

Copy code

```
AI_SUMMARIZE( '<text>' [ , return_error_details => { TRUE | FALSE } ] )
```

For FILE input:

Copy code

```
AI_SUMMARIZE( TO_FILE( '<stage>' , '<file_path>' ) [ , return_error_details => { TRUE | FALSE } ] )
```

## Arguments

**Required (one of):**

`text`
:   A string containing the text from which a summary should be generated.

`file`
:   A FILE object representing the stage reference to the file from which a summary should be generated.

**Optional:**

`return_error_details`
:   A boolean that reports row-level failures when set to `TRUE`. For more information, see
    [BCR 2184](/release-notes/bcr-bundles/2026_02/bcr-2184).

## Returns

Returns a string summary of the input.

## Usage notes

- **Short inputs:** AI\_SUMMARIZE returns the original input when the input is 110 characters or fewer, and when
  a generated summary would be longer than the source. All tokens processed are billed.
- **Summarizing across rows:** Use [AI\_AGG](/sql-reference/functions/ai_agg) rather than combining rows with LISTAGG
  before calling AI\_SUMMARIZE.
- **Regional differences:** Supported modalities, context windows, file sizes, and page limits vary by region.
  See [Limitations](#limitations) for details.
- **Row-level errors:** Use `return_error_details => TRUE` when you want error details for individual rows.

## Examples

### Summarize text

AI\_SUMMARIZE condenses long-form text while retaining the key points and overall meaning.

In this example, a detailed product review is summarized into the product’s main strengths, comfort issues, and
the customer’s overall recommendation.

Copy code

```
SELECT AI_SUMMARIZE('These high-end luxury shoes are designed to make a statement. Crafted from premium leather with precise stitching, polished details, and a sleek silhouette, they immediately look expensive and exclusive. The craftsmanship is impressive, and their sophisticated appearance makes them an excellent match for formal outfits, tailored suits, and upscale events.

However, comfort is where these shoes fall dramatically short. The leather is extremely stiff, particularly when new, and the structured design gives the foot very little freedom to move naturally. The narrow toe box can create uncomfortable pressure around the toes, while the rigid heel may cause rubbing after only a short period of walking.

Despite their premium price, cushioning is surprisingly limited. The sole feels hard underfoot, meaning extended periods of standing or walking can quickly become tiring. After several hours, wearers may experience soreness around the heel and ball of the foot. Breaking them in can improve the experience slightly, but they are unlikely to ever feel like genuinely comfortable everyday footwear.

Ultimately, these shoes prioritize appearance, craftsmanship, and exclusivity over practicality. They look exceptional and can elevate an expensive outfit, but wearing them for an entire day could be a challenge. They are best suited to formal dinners, ceremonies, luxury events, or other occasions where minimal walking is required.

For buyers who value comfort above everything else, these shoes are difficult to recommend. For those willing to sacrifice comfort for an elegant design and prestigious appearance, however, they certainly deliver the desired luxury aesthetic.');
```

Response:

```
High-end luxury leather shoes with precise stitching, polished details, and a sleek silhouette; excellent
craftsmanship and a sophisticated, exclusive appearance suited to formal outfits, tailored suits, and upscale
events.

Major drawback: poor comfort. Extremely stiff leather (especially new), structured design limits natural foot
movement, narrow toe box causes pressure, and a rigid heel can rub. Limited cushioning and a hard sole make
standing or walking for long periods tiring; soreness at heel and ball of foot after several hours. Breaking
in helps slightly but they're unlikely to be comfortable for everyday wear.

Conclusion: prioritize appearance, craftsmanship, and exclusivity over practicality. Best for formal
occasions with minimal walking; not recommended for buyers who prioritize comfort.
```

### Summarize file content

The AI\_SUMMARIZE function generates concise summaries of image and document files stored in an internal
Snowflake stage or an external stage.

#### Image example

The following example uses AI\_SUMMARIZE to generate a summary of a Snowflake cartoon illustrating a document
processing workflow.

![Cartoon illustrating a Snowflake AI Parse Document workflow](/static/images/snowflake-cortex/ai_summarize/cartoon.jpg)

Copy code

```
SELECT AI_SUMMARIZE(TO_FILE('@my_docs', 'cartoon_image.jpeg')) AS image_summary;
```

Response:

```
Based on the provided comic strip, here is a summary of the workflow and key features of **Snowflake AI
Parse Document**, the document intelligence engine:

### **1. The Problem**
* Users face a "data mess" consisting of unorganized mountains of unstructured documents, including
  contracts, invoices, and notes.

### **2. The Solution: Snowflake AI Parse Document**
* This document intelligence engine processes unstructured documents (such as old contracts and forms)
  through three core capabilities:
  * **OCR (Optical Character Recognition):** Converts text from scanned documents and images.
  * **Layout:** Analyzes the visual structure and formatting of the documents.
  * **Extraction:** Extracts key structured fields, such as `[DATE]`, `[PARTIES]`, and `[LIABILITY CLAUSE]`.

### **3. Data Structuring and Integration**
* **`DOC_TABLE`:** Extracted data is organized into a structured table containing columns for `ID`,
  `DOC_TYPE`, `DATE_EXTRACTED`, and `CONTENT`.
* **Joining with Other Structured Data:** This newly structured document data can be joined with existing
  structured databases.

### **4. Search and Retrieval Process**
* **`DOC_CHUNKS`:** Documents are broken down into smaller text segments, mapped by `ID`, `CHUNK_ID`, and
  `CHUNK_TEXT`.
* **Cortex Search:** These chunks are fed into "Cortex Search," enabling a data search and retrieval
  process.
* **Natural Language Querying:** Users can query the system using natural language (for example, asking a
  chatbot, "Contracts from 2023 about rental?") to retrieve precise, relevant information from the
  processed documents.
```

#### Document example

The following example demonstrates how AI\_SUMMARIZE can distill a 27-page financial report with complex
layouts and detailed analysis into a concise summary.

![Cover of the Vanguard economic and market outlook for 2026 report](/static/images/snowflake-cortex/ai_summarize/vanguard-report-cover.png)

Copy code

```
SELECT AI_SUMMARIZE(TO_FILE('@my_docs', 'vanguard-economic-and-market-outlook-for-2026-ai-exuberance-eur-en-pro.pdf')) AS doc_summary;
```

Response:

```
Here is a summary of the Vanguard Economic and Market Outlook for 2026, preserving key figures, dates,
relationships, and regional forecasts for downstream factual question answering:

### **Core Theme: AI Exuberance**
* **Economic Upside vs. Stock Market Downside:** Rapid AI adoption is driving a structural shift and a
  capital-deepening cycle. However, high earnings expectations and "creative destruction" present
  downside risks and increased volatility for tech-heavy US growth stocks.
* **Investment Cycle Stage:** The current AI investment cycle is in its early stages (estimated at
  30%–40% of past historical peaks). AI scalers (for example, Amazon, Alphabet, Tesla, Apple, Oracle,
  Microsoft, Nvidia, Meta) have committed **$2.1 trillion** in capital investments through 2027, backed
  by an estimated **$2.4 trillion** in retained cash flow and existing cash.

---

### **Vanguard's 2026 Economic Forecasts (As of Dec 10, 2025)**

| Country/Region    | 2026 GDP Growth | 2026 Core Inflation | 2026 Unemployment Rate | Year-End Policy Rate | Key Risk to View                                     |
| :---------------- | :-------------: | :-----------------: | :--------------------: | :------------------: | :--------------------------------------------------- |
| **United States** |      2.25%      |         2.6%        |          4.2%          |         3.5%         | AI optimism collapses; investment buildout stalls    |
| **Euro Area**     |       1.2%      |         1.8%        |          6.3%          |         2.0%         | Inflation materially undershoots the 2% target       |
| **China**         |       4.5%      |         1.0%        |          5.1%          |         1.2%         | Technology innovation and investment accelerate      |

---

### **Regional Economic Outlooks**

* **United States:**
  * **Growth & Capital Spending:** Driven by strong capital expenditures. AI spending is projected to add
    **$450 billion** over the next year, supporting **7%** growth in overall non-residential investment.
    There is a **60% chance** of the US achieving **3% real GDP growth** in the coming years if AI acts as
    a true general-purpose technology (GPT).
  * **Labor Market:** Job creation slowed from ~150,000/month to 30,000/month, largely due to immigration
    and demographic trends (accounting for 70% of the slowdown). Employers need to add ~60,000 jobs/month
    to keep unemployment steady.
  * **Monetary Policy:** Sticky inflation and solid growth will limit the Federal Reserve's rate cuts,
    keeping the policy rate near the estimated neutral rate of **3.5%**. Only one rate cut is expected in
    the first half of 2026.
* **Euro Area:**
  * **Growth Dynamics:** A soft landing is underway. Growth of **1.2%** in 2026 will be shaped by opposing
    forces: a **0.3 percentage point (ppt)** drag from higher US tariffs (effective tariff rate up 15 ppts)
    offset by looser fiscal policy (Germany's infrastructure package boosting Euro area GDP by 0.2 ppts,
    and increased EU defense spending adding another 0.2 ppts).
  * **AI Lag:** Europe lags in AI infrastructure, with tech-sector capital commitments of **$250 billion to
    $300 billion** over the next two years (compared to over $2 trillion in the US).
* **United Kingdom:**
  * **Growth & Inflation:** GDP growth is forecast at **1%** in 2026. Headline inflation is expected to
    drop from 3.8% (end of 2025) to **2.2%** by the end of 2026, allowing the Bank of England to lower the
    bank rate to **3.25%**.
* **China:**
  * **Growth & Headwinds:** GDP growth is expected to slow to **4.5%** in 2026 due to export frontloading
    payback and weak domestic demand. Trend growth is projected to fall to **4.2%** over the coming decade.
  * **Demographics:** Chinese AI productivity gains face severe demographic headwinds, with the working-age
    population projected to shrink by **30% over the next 25 years**.
* **Japan:**
  * **Growth & Policy:** Real GDP growth is forecast at **1%** in 2026, supported by wage growth and tax
    cuts. The Bank of Japan (BoJ) is expected to continue policy normalization, gradually raising its
    policy rate to **1%** by the end of 2026.

---

### **Market and Portfolio Outlook (5-to-10-Year Horizon)**

Vanguard's preferred asset classes, ranked by the strongest risk-return profiles over the next 5 to 10
years, are:

1. **High-Quality Fixed Income:** High-quality bonds offer compelling real returns (projected at around
   **3%** over the coming decade, exceeding the past decade's returns by ~2%) due to higher neutral rates.
   They also provide a hedge (25%–30% probability) if AI-driven productivity fails to materialize.
2. **US Value-Orientated Equities:** Projected 10-year annualized return of roughly **7%** (in EUR). These
   sectors (industrials, financials, consumer segments) are better positioned to capture the long-term
   efficiency gains of AI diffusion at more attractive valuations.
3. **Non-US Developed-Market Equities:** Projected 10-year annualized return of roughly **6.5%** (in EUR).

* **US Growth/Tech Equities Outlook:** Vanguard maintains a guarded outlook on tech-heavy US growth stocks.
  The 10-year annualized return projection for US equities overall is muted at **4% to 5%** (in EUR)
  / **4.3%–5.3%** (in EUR), largely driven by high valuations (the CAPE ratio was ~37 as of November 19,
  2025, in the top 10% of historical valuations since 1988).
```

### Summarize a library of files

1. **Create a multimodal table for your files.** Create a table of file references so you can work with your
   staged files using SQL.

   Copy code

   ```
   CREATE TABLE doc_files AS
     (SELECT TO_FILE('@DEMO_DOCS', RELATIVE_PATH) AS doc FROM DIRECTORY(@DEMO_DOCS));
   ```
2. **Query file metadata with SQL.** Use file functions to inspect metadata such as file name, content type,
   size, stage, and last modified date.

   Copy code

   ```
   SELECT
     FL_GET_RELATIVE_PATH(doc) AS file_name,
     FL_GET_CONTENT_TYPE(doc)  AS content_type,
     FL_GET_ETAG(doc)          AS etag,
     FL_GET_LAST_MODIFIED(doc) AS last_modified,
     FL_GET_SIZE(doc)          AS size,
     FL_GET_STAGE(doc)         AS stage
   FROM doc_files;
   ```
3. **Summarize every file with a single query.** Use AI\_SUMMARIZE to generate a summary for each document,
   without having to reference files individually.

   Copy code

   ```
   -- Returns a summary for every document without needing to explicitly name each doc.
   SELECT AI_SUMMARIZE(doc) AS doc_summary FROM doc_files;
   ```

## Limitations

| Availability | Context Window – Text Inputs | Context Window – Files | Image Support | Document Support |
| --- | --- | --- | --- | --- |
| `ANY_REGION` | 272K | 1M | JPG/JPEG, PNG, WEBP, GIF · 100 MB | PDF, TXT, MD · 37.5 MB · 1,000 pages TXT, MD, PDF, DOC/DOCX, XLS/XLSX, CSV, XHTML · 4.5 MB · 100 pages |
| `AWS_GLOBAL` | 128K | 200K | JPG, PNG, WEBP, GIF · 3.75 MB | TXT, MD, PDF, DOC/DOCX, XLS/XLSX, CSV, XHTML · 4.5 MB · 100 pages |
| `AZURE_GLOBAL` | 272K | 400K | JPG/JPEG, PNG, GIF, WEBP · 10 MB | N/A |
| `GCP_GLOBAL` | 1M | 1M | JPG/JPEG, PNG, WEBP, GIF · 100 MB | PDF, TXT, MD · 37.5 MB · 1,000 pages |

Expand

Show lessSee more

## Legal

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
