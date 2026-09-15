# Aug 10, 2026: AI\_MULTI\_EMBED support for large video files in semantic video search (*General availability*)

Snowflake Cortex AI\_MULTI\_EMBED is now generally available for semantic video search with support
for large video files up to 6 GB using the TwelveLabs Marengo Embed 3.0 model, enabling
organizations to index and search production-grade video content directly in Snowflake. This makes
it easier to retrieve relevant scenes, quotes, actions, and brands from large video libraries using
multimodal embeddings instead of relying only on filenames, tags, or manual review.

Key use cases include:

- **Brand suitability and contextual advertising:** Evaluate whether video segments align with brand
  guidelines, safety thresholds, or campaign requirements, and match ads or promotions to relevant
  scenes, topics, or moments.
- **Scene analysis and retrieval:** Search large video libraries for relevant scenes, actions, and
  visual concepts, and analyze how scenes evolve across content.
- **Spoken-moment discovery:** Find quotes, dialogue, and transcript-aligned moments across
  long-form video content.
- **Brand and product search:** Identify where brands or products appear or are mentioned across
  media collections.
- **Content indexing at scale:** Build richer media indexes for recommendation, moderation,
  analytics, and downstream AI applications.

For video inputs, AI\_MULTI\_EMBED uses the `twelvelabs-marengo-embed-3-0` model to generate
embeddings across visual, audio, and transcription signals. As part of a broader workflow, teams can
use these embeddings and derived labels to power downstream ML models, combine video-derived signals
with subscriber or other first-party data, and enable agents to reason over multimodal context and
provide recommendations, all within Snowflake’s governed platform.

For more information, see [AI\_MULTI\_EMBED](/sql-reference/functions/ai_multi_embed) and
[Cortex AI Functions: Multimodal](/user-guide/snowflake-cortex/ai-multimodal).
