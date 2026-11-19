# Multi-agent orchestration with a CoWork profile: Design guidance

[Preview Feature](/release-notes/preview-features) — Open

This page covers features in preview: Snowflake CoWork profiles and the `agent_router` tool.

Part of the [Multi-agent orchestration with a CoWork profile](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration) recipe.

How to set up Snowflake CoWork profiles and their agents so they stay accurate, fast, and affordable as you grow. Each rule on this page comes from Snowflake’s evaluations of profiles with up to 1,000 subagents. A *subagent* is an agent that a profile routes questions to, called a specialist agent in the recipe. A *flat profile* answers with tools attached directly to it; a *profile with subagents* routes questions to subagents.

## Summary

- Start with one profile and attach tools to it directly. It is the cheapest and fastest setup while the tool list is small.
- Add subagents for ownership, reuse, or scale, not for accuracy. Routing does not make answers better or worse; it adds one extra agent run.
- Keep data that is used together in the same agent. Answers that need two agents’ data are noticeably less reliable.
- Instructions matter more than structure. Good instructions improved accuracy in every setup, most on ambiguous questions.
- Size is not a quality problem. Accuracy held up to 1,000 subagents; cost grows with how many tools a single agent carries.

## How a profile works

- A profile is an agent. It can answer with its own tools or hand the question to subagents through the `agent_router` tool.
- When routing, the profile sees only each subagent’s name, display name, and description. It does not see the subagent’s instructions or tools.
- A subagent sees only its own tools and instructions, not the rest of the profile.
- This visibility model drives cost. An agent re-reads all of its tool definitions on every step, while a profile reads only one short entry per subagent.

## Choosing a setup

### Pattern A: A flat profile (start here)

- **Fits:** one team with a small set of data, or a team just starting.
- **Why:** no routing step, so no routing mistakes, and the lowest latency and cost while the tool list is small.
- **Watch:** cost rises with every tool you add, because each step re-reads all of them. Past a few dozen semantic views, a profile with subagents becomes cheaper, and a flat profile stops working entirely once its tools no longer fit in the model’s context (around a thousand semantic views).
- **Move to pattern B when:** the profile grows past a few dozen semantic views, or a domain needs its own owner.

### Pattern B: One profile with domain subagents

- **Fits:** several teams own their own data (for example, sales, finance, and operations), and all users get the same experience.
- **Setup:** the profile keeps shared tools (connectors, charting, web search); each domain team owns a subagent with its data and tools. One subagent can be linked into several profiles.
- **Cost:** routing adds an extra agent run per question, a few seconds and some credits. With hundreds of tools, a profile with subagents is two to three times cheaper than a flat profile.

### Pattern C: Several profiles by persona

- **Fits:** groups of users who need different agents, instructions, or governance, for example a sales profile owned by sales operations.
- **Setup:** one profile per persona, with each user mapped to exactly one profile. Subagents can be shared across profiles.
- **Not for data access alone.** Use grants on agents and data instead of creating a profile per access level. The [recipe](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration) shows how one profile serves several personas.

### Principles for splitting into agents

- Split along domain or ownership boundaries, not one agent per semantic view.
- Keep data that is used together in one agent. When the profile has to combine two agents’ answers, joins become less reliable, and combined metrics (for example, campaign-attributed revenue) are usually wrong.
- Avoid overlapping agents. If two agents can answer the same question, merge them, or state in each description what it covers and what it does not.

## Instructions

- **Make them specific to your data.** Say which semantic view answers which topic, give default definitions (what revenue means), and say how to handle ambiguous names and questions that span domains.
- **Put each rule where the decision is made.** Routing rules belong in the profile’s instructions and in subagent descriptions; tool-choice rules belong in that subagent’s instructions.
- **Give every subagent its own instructions.** The profile can’t pass its rules down to a subagent.
- **Label look-alike tools.** Look-alike tools and development or test copies of the same data are safe with good instructions and clear descriptions. Without them, the agent picks the wrong source noticeably more often.

## Scale and cost

[![Chart: credits per question for a flat profile and a profile with subagents, from 8 to 2,189 semantic views. The flat profile is cheaper below about 30 views; above that, the profile with subagents is cheaper, and the flat profile fails at about 1,100 views.](/static/images/cortex-ai-cookbook/multi-agent-orchestration/diagrams/flat-vs-routed-cost.png)](/static/images/cortex-ai-cookbook/multi-agent-orchestration/diagrams/flat-vs-routed-cost.png)

**What one semantic view costs.** On a flat profile, each semantic view is one Cortex Analyst tool definition of about 3,500 characters (about 1,500 tokens), and the agent re-reads every definition on every step. Most of that is the fixed tool definition, so a small semantic view and a large one cost about the same; the view’s custom instructions and verified queries are added on top. In Snowflake’s evaluations, a flat profile with 30 semantic views sent about 88,000 tokens on its first model call and about 360,000 input tokens per question. On a profile with subagents, each subagent adds about 530 tokens, read once per routing decision, and each subagent re-reads only its own few views.

- **Quality does not drop with more subagents.** Accuracy and routing held from 8 up to 1,000 subagents, and agents were not distracted by irrelevant ones.
- **Adding subagents is cheap; piling tools on one agent is not.** Going from 8 to 100 subagents added little cost, while one agent with hundreds of tools cost several times more than the same tools spread across agents.
- **Keep every agent to a focused set of tools.** This applies to subagents too: a subagent with hundreds of tools has the same cost problem as a flat profile.
- **Keep descriptions short and specific.** Every routing decision reads them, and on Gemini models the combined routing text has a hard size limit.

## Before you roll out

Before you roll out, confirm the following:

- Each agent’s description says what it covers and what it does not.
- No unlabeled copies of the same data or agent in one profile.
- Instructions name the right semantic view for each topic and define key terms.
- Every subagent has its own instructions.
- Data that is queried together lives in the same agent.
- You have tested with questions that reflect your real traffic, including ambiguous and cross-domain ones. The recipe’s [routing evaluation](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration#the-routing-evaluation) is a starting point.
