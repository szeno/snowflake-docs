# Tutorial 1: Providers set up and test a CKE

## Introduction

For providers, this tutorial describes how to set up and test your CKE.

### What you’ll learn

In this tutorial you’ll learn how to:

- Create Snowflake objects
- Load your data into Snowflake
- Chunk your documents
- Create the Cortex Search Service
- Verify the CKE is working correctly
- Share and test the CKE with a consumer account

### Prerequisites

The following prerequisites are required to complete this tutorial:

- You have a Snowflake account and user with a role that grants the necessary
  privileges to create a database, tables, virtual warehouse objects, Cortex Search services, and Streamlit apps.

Refer to the [Snowflake in 20 minutes](/user-guide/tutorials/snowflake-in-20minutes) for instructions to meet these requirements.

# Step 1: Create Snowflake objects

The first step is to create Snowflake objects.

Use the accountadmin role.

Copy code

```
use role accountadmin;
```

Create a warehouse named `xsmall_cke_getting_started` for creating and updating the index.

Copy code

```
create warehouse xsmall_cke_getting_started warehouse_size=xsmall;
```

Create a separate role named `cke_owner`.

Copy code

```
create role cke_owner;
grant role cke_owner to user admin;
grant usage on warehouse xsmall_cke_getting_started to role cke_owner;
```

Create and use a database named `cke_getting_started`.

Copy code

```
grant create database on account to role cke_owner;
use role cke_owner;
create database cke_getting_started;
use database cke_getting_started;
```

Create and use a schema called `articles`.

Copy code

```
create schema articles;
use schema articles;
```

# Step 2: Load your data into Snowflake

The next step is to load your data into Snowflake. Refer to [Load data into Snowflake](/guides-overview-loading-data) for more information.

The example code below stores data in a Snowflake table named `cke_simple_article` in the following format:

| Column name | Type | Description |
| --- | --- | --- |
| `DOCUMENT_ID` | `VARCHAR` | The unique identifier for the document. This is the primary key of the table. |
| `DOCUMENT_TITLE` | `VARCHAR` | The title of the document. |
| `SOURCE_URL` | `VARCHAR` | A URL linking to the source of a document. |
| `DOCUMENT_TEXT` | `VARCHAR` | The document contents, parsed as text. This is the content that will be indexed and searched. |

Expand

Show lessSee more

Note that you can include additional document metadata in your indexed dataset. In our example below, we include only `SOURCE_URL` and `DOCUMENT_ID`, but you can add more columns depending on your document source.

Create a simple table.

Copy code

```
create or replace table cke_simple_article (
    DOCUMENT_ID VARCHAR,
    DOCUMENT_TITLE VARCHAR,
    SOURCE_URL VARCHAR,
    text VARCHAR
);
```

Now insert some sample data into that table.

Copy code

```
INSERT INTO cke_simple_article (DOCUMENT_ID, DOCUMENT_TITLE, SOURCE_URL, TEXT)
VALUES
    ('DOC_001', 'Sample Article 1', 'https://example.com/article1', 'This is some sample text for the first article.'),
    ('DOC_002', 'Sample Article 2', 'https://example.com/article2', 'Another sample text entry for the second article.'),
    ('DOC_003', 'Sample Article 3', 'https://example.com/article3', 'Yet another piece of text for the third article.');

INSERT INTO cke_simple_article (
    DOCUMENT_ID,
    DOCUMENT_TITLE,
    SOURCE_URL,
    text
)
VALUES (
    'DOC-GREEN-001',
    'The Grand Opening of Greenfield Biosphere',
    'https://www.example.com/news/greenfield-biosphere',
    'Greenfield Biosphere, nestled in the heart of a once-industrial landscape, opened its doors to the public today amid great fanfare and curiosity. This ambitious environmental initiative, spanning over 120 acres of reclaimed land, has been designed to house thousands of diverse plant species and animals under one vast, transparent dome. Over the past decade, teams of botanists, engineers, and conservationists collaborated intensively to restore the soil quality, implement renewable energy solutions, and establish sustainable water sources. Their efforts have resulted in an oasis that stands as a testament to nature''s resilience and humanity''s unwavering determination to coexist with it.

    Upon entering the biosphere, visitors pass through a series of controlled airlocks that maintain precise temperature and humidity levels, ensuring the delicate balance required for each habitat. The moment they step inside, a multitude of colors and scents envelops them. Towering palm trees sway gently, nurtured by a carefully engineered irrigation system that recycles water across various sections of the dome. Exotic butterflies flutter past patches of vibrant orchids, while small reptiles scurry along the edge of meandering pathways. Every detail, from lighting angles to seed selection, has been meticulously planned to promote biodiversity in a space that once lay barren.

    Local officials and environmental organizations herald this project as a bold step toward reversing ecological decline. The region had suffered decades of industrial pollution, leaving the soil depleted and wildlife populations on the brink of collapse. Public interest soared once the Greenfield Biosphere project was announced, prompting unprecedented fundraising campaigns and private investments. Citizens volunteered their time to plant seedlings, build composting facilities, and educate children on the importance of ecological stewardship. Now, as thousands explore the dome on opening day, excitement mingles with a sense of responsibility, fueling hope that this initiative can serve as a catalyst for broader restoration efforts.

    Beyond merely a tourist attraction, the Greenfield Biosphere plays a crucial role in scientific research. Biologists and ecologists from universities around the globe have established research stations within the dome to study plant migration, cross-pollination, and microclimates. Through advanced sensor networks, they collect data on everything from soil moisture levels to carbon sequestration rates, aiming to develop cutting-edge conservation strategies. Already, preliminary findings suggest that certain flora species exhibit faster growth rates under partial shade, which could help inform future reforestation projects. This research extends to aquatic ecosystems as well, with scientists closely monitoring newly formed ponds and streams for indicators of ecosystem health.

    During the grand opening ceremony, Mayor Allison Pierce praised the community for its unwavering dedication to the biosphere''s development. She emphasized how interagency cooperation and community outreach were pivotal in transforming a polluted wasteland into a verdant sanctuary. In her address, she remarked on the significance of involving local youth, who contributed to the design through art projects and educational workshops. According to Mayor Pierce, the next phase of the project will include expanding the biosphere''s capacity for endangered species breeding programs. This could cement the region''s reputation as a global leader in ecological preservation and innovation.

    For many, the real highlight of the day was the unveiling of the arboretum wing, a temperature-controlled section featuring ancient tree species that have long faced threats from illegal logging and habitat loss. Towering redwoods, thought to be too large to grow under a dome, stand proudly after years of careful nurturing. Visitors stood in awe as the directors revealed that these trees'' root systems, painstakingly preserved and transplanted, are now thriving in custom-engineered soil mixtures. A sense of reverence filled the air, with many attendees describing the experience as spiritual. The seed of hope planted in the community has visibly taken root.

    The venture''s economic impact is another key talking point. Local shops and restaurants anticipate an influx of tourists, and hotels report reservations scheduled months in advance. Construction of new eco-lodges in the surrounding areas is already underway, promising a blend of comfortable accommodations with sustainable building practices. The city council has also approved additional funding to improve roads and public transportation to accommodate the expected rise in visitor numbers. Environmental advocates caution, however, that increased foot traffic could inadvertently strain the biosphere''s delicate ecosystems, calling for balanced planning and continued emphasis on conservation education.

    Inside the administrative office, a dedicated operations team monitors real-time data feeds, adjusting temperature, humidity, and nutrient levels to meet each species'' unique needs. Modular solar panels installed around the dome generate sufficient electricity to power the entire facility, showcasing how renewable energy can be integrated seamlessly with large-scale infrastructure. Outside, an innovative wastewater treatment plant recycles greywater for irrigation, minimizing resource consumption. The architects behind the biosphere believe these sustainable technologies can be replicated in other communities looking to rehabilitate degraded land, turning once-polluted sites into living laboratories for environmental stewardship.

    While the facility is only in its first phase, future expansions are already on the drawing board. There are plans to introduce a marine habitat zone featuring coral reef tanks that highlight threats to underwater ecosystems. Specially designed walkways will give visitors a close-up view of these aquatic wonders without disturbing the delicate organisms within. Meanwhile, education programs will be expanded to local schools, offering field trips where students can learn about biodiversity, climate change, and sustainable technologies. The hope is that exposure to this living exhibit will inspire the next generation of environmental scientists, engineers, and policymakers.

    As dusk settled over the glass dome, a soft, multi-colored illumination replaced the natural daylight, casting enchanting shadows across the tropical foliage. Families strolled slowly along the paths, pausing to read plaques about the origins of each plant or to marvel at the occasional flutter of nocturnal pollinators. Meanwhile, a gentle hum of conversation reverberated in the background, carrying sentiments of astonishment and gratitude. The first day at Greenfield Biosphere ended with a collective realization that, with mindful planning, community collaboration, and respect for nature''s inherent wisdom, it is indeed possible to transform a scarred landscape into a flourishing haven for life and innovation.'
);
```

# Step 3. Chunk your documents

Before creating a Cortex Search Service, we need to ensure that each “chunk” of indexed text is no more than approximately 375 words of text. To do this, we can apply a chunking algorithm via a Snowpark UDF that imports LangChain. First, we create a chunking UDF. Then, we apply that UDF to the `cke_simple_article` table and store the chunks in a `cke_simple_article_chunks` table. And finally, we verify that the chunks were created.

Run the example below to chunk the articles into parts for the Cortex Search Service. This process can take several minutes to complete.

Copy code

```
CREATE OR REPLACE FUNCTION text_chunker(text STRING)
    RETURNS TABLE (chunk VARCHAR)
    LANGUAGE PYTHON
    RUNTIME_VERSION = '3.9'
    HANDLER = 'text_chunker'
    PACKAGES = ('snowflake-snowpark-python', 'langchain')
    AS
$$
from snowflake.snowpark.types import StringType, StructField, StructType
from langchain.text_splitter import RecursiveCharacterTextSplitter
from snowflake.snowpark.files import SnowflakeFile
import logging
import pandas as pd

class text_chunker:

    def process(self, text: str):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 2000,  # Adjust this as needed
            chunk_overlap = 300,  # Overlap to keep chunks contextual
            length_function = len
        )

        chunks = text_splitter.split_text(text)
        df = pd.DataFrame(chunks, columns=['chunk'])

        yield from df.itertuples(index=False, name=None)
$$;
```

Run the example below to split the documents into chunks for indexing.

Copy code

```
CREATE OR REPLACE TABLE cke_simple_article_chunks AS
    SELECT
        c.DOCUMENT_ID,
        c.DOCUMENT_TITLE,
        c.SOURCE_URL,
        t.chunk
    FROM cke_simple_article AS c, TABLE(text_chunker(CONCAT(c.DOCUMENT_TITLE, '\n', c.TEXT))) AS t;
```

Run the following to verify that the chunks were created.

Copy code

```
select * from cke_simple_article_chunks;
```

# Step 4. Create the Cortex Search Service

Now configure a Cortex Search Service named `cke_simple_cortex_search_service` to run on warehouse
`xsmall_cke_getting_started` and reference the chunked document table `cke_simple_article_chunks`. Note that this step can
take considerable time to complete, depending on the size of the database.

Copy code

```
CREATE OR REPLACE CORTEX SEARCH SERVICE cke_simple_cortex_search_service
  ON chunk
  ATTRIBUTES document_title
  WAREHOUSE = xsmall_cke_getting_started
  TARGET_LAG = '1 hour'
  AS (
    SELECT
        chunk,
        document_title,
        source_url
      FROM cke_simple_article_chunks
  );
```

# Step 5. Test the CKE

To verify the CKE is working correctly you can issue a simple query to the Cortex Search Service. This will verify that the service has correctly indexed your documents and that relevant documents come back from queries. This query should return the first chunk of the article “The Greenfield Biosphere” with a link to the source URL.

Copy code

```
select snowflake.cortex.search_preview(
 'cke_getting_started.articles.cke_simple_cortex_search_service',
 '{ "query": "whats happening with the greenfield biosphere?", "columns": ["chunk","document_title","source_url"] }');
```

# Step 6: Share the CKE privately for testing

After the Cortex Search Service has been created and is correctly responding to queries, you can share it. This shared Cortex Search Service is the Cortex Knowledge Extension. In this step, you’ll create a [private listing](/collaboration/provider-listings-creating-publishing#label-listings-create) and share it with another account for testing. Then you’ll test the listing in the consumer account that you shared the CKE with.

## Create the share

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listing** in the upper-right corner and select **Specified Consumers**.
4. Provide a title for the listing, and then click **Next**.
5. Click **+ Select** for **What’s in the listing?**.
6. Select **CKE\_GETTING\_STARTED**.
7. Expand **ARTICLES**.
8. Expand **Cortex Search Service**.
9. Select **CKE\_SIMPLE\_CORTEX\_SEARCH\_SERVICE**, and then select **Done**.
10. Enter a description for the listing.
11. Under **Add consumer accounts**, add the Snowflake account that you want to share and test the Cortex Knowledge Extension with. Note that must be in the same region as the provider, and you must have access to this account.

## Test the share in a consumer account

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) using the consumer account that you shared the CKE with above.
2. in the navigation menu, select **Data sharing** » **Internal sharing**.
3. Here, you should see the **CKE\_GETTING\_STARTED** listing that you shared above. Select **Get**.
4. Open a new worksheet and run the SQL command below to verify that the account has access to the shared data.

   > Copy code
   >
   > ```
   > select
   >   snowflake.cortex.search_preview(
   > 'CKE_GETTING_STARTED_GUIDE__FAKE_ARTICLES.ARTICLES.CKE_SIMPLE_CORTEX_SEARCH_SERVICE',
   > '{ "query": "whats happening with the biosphere?", "columns": ["chunk","document_title"] }'
   >   );
   > ```
   >
   > Note
   >
   > If you specified name other than **CKE\_GETTING\_STARTED** in the **Get** dialog, you’ll need to change that in the snippet above.

At this point, you have a functional Cortex Knowledge Extension!
