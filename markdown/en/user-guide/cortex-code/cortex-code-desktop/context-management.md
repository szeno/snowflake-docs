# Context management

Every conversation has a **context window** — the amount of text the model can consider at
once, including your messages, the agent’s replies, tool results, and any instructions or
files in scope. CoCo Desktop gives you visibility into how that window is being used and tools
to keep it clear so long conversations stay responsive.

## See the token breakdown

The **context ring** in the bottom-right of the composer (the message input) fills up as the
conversation consumes the context window, so you can see at a glance how much room is left.
Hover the ring to open the **Context window** popover, which shows the tokens used out of the
total, the percentage used, and an estimated breakdown of what’s taking up space.

Note

The breakdown is an estimate, and the ring’s usage is clamped to 100%, so it won’t report
impossible values even during large tool runs.

## Compact a conversation

When a conversation grows long, run **`/compact`** from the chat input to summarize the
history and free up context. Compacting replaces the earlier turns the model carries with a
concise summary, so the agent keeps the thread of what you were doing without re-reading
everything — and the full conversation stays visible to you on screen.

Use `/compact` when a session is getting long but you want to keep going in the same
conversation rather than starting a new one.

## Automatic token savings

CoCo also reduces token use on its own — for example, by loading your most-used tools up
front and discovering the rest on demand, offloading large tool results to disk instead of
your context, and sending only the new part of the conversation each turn. These behaviors
are automatic and require no configuration.
