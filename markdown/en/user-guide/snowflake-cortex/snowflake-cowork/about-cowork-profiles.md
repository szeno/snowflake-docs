# About profiles in Snowflake CoWork

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

A profile defines what Snowflake CoWork looks like for one group of users. It names the agents that
group can reach, the instructions that decide which agent answers, and the skills and connectors
available in the conversation.

Profiles usually follow job function. Your sales team gets a profile built around sales agents, your
finance team gets one built around finance agents, and each group sees a product shaped for its own
work. Administrators configure profiles for groups of users, rather than creating a profile for
every agent or task. Most users should have access to exactly one profile.

Users do not choose an agent. When someone asks a question, the profile routes it to the agent best
suited to answer.

## What a profile contains

- **Agents.** The set of agents the profile can route to. You can add any agent in the account, not
  only agents already used in Snowflake CoWork.
- **Instructions.** General instructions that apply to every answer, and routing instructions that
  tell the profile which agent handles which kind of question.
- **Skills and connectors.** The skills and MCP servers the profile itself can use. Agents the
  profile routes to carry their own. For more information, see
  [Where capabilities come from](#label-cowork-profiles-capabilities).

## How users experience a profile

With access to one profile, users do not need to choose a profile before asking a question. They open
Snowflake CoWork, ask a question, and get an answer from whichever agent fits. Access to multiple
profiles is an exception, such as an administrator who manages profiles for several groups.

Users who have access to more than one profile pick one from the account menu. One profile is active
at a time, and the active profile appears under the user’s name so users can tell which one they are
in. Switching profiles changes which agents answer. It does not end the conversation.

You control who sees which profile by granting USAGE on it. A user with access to a single profile
sees no picker.

## Two ways to organize profiles

Most accounts need one profile. Start there.

**One profile for everyone.** A single profile, granted to every user, that routes across a trusted
handful of agents. This suits accounts where one team curates the whole Snowflake CoWork
experience. You can have hundreds of agents in the account while the profile routes to only the ten
that work well for everybody.

**One profile per function.** Separate profiles for sales, finance, legal, and everyone else, each
owned by a lead from that function. This suits accounts where functional leads want to own their
team’s experience end to end. It costs more to maintain, because each profile carries its own agent
list and routing instructions.

You can start with one profile and add more later. Adding a profile does not change the profiles you
already have.

## Example: Profiles for four groups

Consider an organization with four profiles, each owned by the corresponding functional lead or a
central administrator. Users have access to the profile for their job function:

- Go-to-market (GTM) for sales and marketing staff.
- Finance for finance staff.
- Legal for legal staff.
- General for everyone outside those three groups.

In this example, General is a working profile for the remaining users, not an empty profile that
everyone must open before requesting access to another profile. A user in GTM has access to GTM
rather than both GTM and General. An administrator who manages both profiles can have access to both.

The groups are distinct, but their agent lists can overlap. For example, GTM and General both
include an HR agent, a sales agent, and a product analytics agent. Users can ask HR questions from
their usual profile without switching to a separate HR profile.

Routing instructions can favor different agents for the same question. For “What is
happening with this customer?”, GTM’s instructions prefer the sales agent for account activity and
sales opportunities. General’s instructions prefer the product analytics agent for product usage.
The profiles share agents, but each profile describes which agent to prefer for an overlapping topic.

Each profile can also have its own connectors and preinstalled skills. In this example, GTM has a
customer relationship management MCP connector and a sales preparation skill. General has a project
management MCP connector and a project status skill. These are capabilities configured on the
profiles themselves. Agents shared between profiles retain their own capabilities, as described in
[Where capabilities come from](#label-cowork-profiles-capabilities).

Including an agent in several profiles does not give every user access to that agent. Access still
depends on the user’s role-based access control (RBAC) grants. Profile owners choose the experience
for each group, while the existing grants determine which agents each user can use.

## Who owns what

Splitting ownership lets a function change its own profile without waiting on a central team.

- The **Snowflake CoWork administrator** owns the Snowflake CoWork object, decides which profiles
  exist, and grants users access to them.
- A **profile owner** owns the contents of one profile: its agents, instructions, skills, and
  connectors. Profile owners cannot grant access to their own profile.
- An **account administrator** creates the roles that back profile ownership and access.

A common pattern is one role per profile for owners and one for users, with the user role populated
from an identity provider group through SCIM. Because a user’s group memberships decide which
profiles they see, adding someone to a team in your identity provider is enough to give them the
right profile.

## What a profile controls

A profile controls routing. It does not change data access.

- **Routing.** Questions route only to agents in the profile. Tagging an agent with `@` works only
  for agents the profile contains.
- **Privileges.** A profile does not grant or revoke access to data. Users reach the agents behind a
  profile under the grants those agents already carry, and Snowflake CoWork runs every query as the
  user who asked, so row access and masking policies continue to apply.
- **Direct links.** A link to a specific agent still opens that agent, which lets you test an agent
  before adding it to a profile.

Because a profile controls routing rather than access, you do not need a separate profile to keep an
agent away from part of a team. An engineering profile can contain an agent that only managers have
privileges on, and engineers who lack those privileges never see it.

When another team must own a specialist’s data or instructions, and grants must decide which
specialist each user reaches, see
[Multi-agent orchestration with a CoWork profile](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration).

## Where capabilities come from

A capability is anything an agent can do beyond answering from its own knowledge: web search, code
execution, a skill, or an MCP server. A profile carries capabilities, and so does every agent the
profile routes to. You configure the two separately, and neither one edits the other.

The difference shows when the two disagree. An agent that has web search keeps web search even when
the profile routing to it does not have web search. Turning a capability off on a profile turns it
off for the profile and leaves the agents untouched. Skills and MCP servers work the same way, so a
skill on an agent stays on that agent whether or not the profile lists it.

A profile is therefore not a way to take a capability away. To stop an agent from using web search,
turn web search off on that agent. To keep that agent’s capabilities out of one group’s experience,
stop routing to the agent from that group’s profile.

Whichever agent answers is the agent whose capabilities run. When a profile answers a question
itself, it uses the profile’s capabilities. When a profile routes the question, the agent that
receives it uses its own. A capability that only one agent holds is reachable only when routing
reaches that agent, which is another reason to give each agent a description that says what it is
for.

Web search and code execution also have an account-level setting, and the account setting wins over
both layers. If an administrator turns web search off for the account, no profile and no agent can
use it, whichever configuration they carry. You also cannot add it to a profile while it is off, and
the profile editor shows the option turned off. An agent configured before the setting changed still
lists web search in its own configuration, so check the account setting first when a capability does
not behave the way the configuration suggests. For more information, see
[Manage web search](/user-guide/snowflake-cortex/cortex-agents-manage#label-cortex-agents-web-search).

## Plan your profiles

A few constraints are worth knowing before you design a set of profiles.

**Profiles should divide your users cleanly.** A user who holds roles mapping to several profiles
gets a picker rather than a single answer. Choose a boundary where most people land in exactly one
group. Function works for some organizations and reporting line for others.

**You cannot express “everyone except one group”.** Snowflake privileges grant access rather than
withhold it, so there is no way to say “everyone but sales”. Instead, grant each profile to the
roles that should have it and use a general profile as the fallback for everyone else. When you add
a profile for one function, remove that function’s users from the general profile.

**Overlapping topics need routing instructions.** Several profiles can share an agent. When two
agents within a profile answer similar questions, their descriptions and the profile’s routing
instructions need to distinguish when to use each agent. The
[four-group example](#label-cowork-profiles-job-function-example) shows how different profiles can
prefer different agents for the same question.

## Profiles and the Snowflake CoWork object

The Snowflake CoWork object holds the list of profiles available in your account. Attaching a
profile to the object makes it selectable by users you granted access to. For more information about
the object, see [User access and settings for agents](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents).

A profile is stored as an agent that carries routing configuration, so the SQL commands that create
and change profiles are agent commands. An agent with an `agent_router` tool that you attach to the
Snowflake CoWork object is a profile. An agent without one is a regular agent that a profile can
route to. CoWork Admin creates profiles in
the `SNOWFLAKE_INTELLIGENCE.PROFILES` schema. If your organization does not allow that database, you
can create a profile with SQL in a database and schema you already have. For more information, see
[Create a profile in your own database and schema](/user-guide/snowflake-cortex/snowflake-cowork/set-up-cowork-profile-routing#label-cowork-profiles-custom-location).
Because a profile is an agent, your applications can also call it directly. See
[Call a Snowflake CoWork profile from the Cortex Agents API](/user-guide/snowflake-cortex/snowflake-cowork/call-cowork-profile-from-api).

If your account has agents but no profile, your users pick an agent themselves and nothing routes
yet. Other accounts route every question through a single account-wide agent named Main Agent.
Either way, see
[Set up profile routing in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/set-up-cowork-profile-routing) to start routing through a profile.

## Evaluate a profile

A profile is a Cortex Agent configured with the
[`agent_router`](/user-guide/snowflake-cortex/cortex-agents-router) tool, which inspects each
user question and routes it to the appropriate subagent in the profile (or answers directly using
the profile’s own [capabilities](#label-cowork-profiles-capabilities)). Because routing questions to
the right subagent is a profile’s primary responsibility, evaluating `agent_router` is central to
verifying that your profile’s routing instructions and subagent descriptions work as intended.

Because a profile is a Cortex Agent, you can evaluate it using
[Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations). You can use
system and custom metrics such as answer correctness and logical consistency to measure overall
response quality and reasoning, and use the tool metrics to evaluate routing behavior through
`agent_router`:

- **Tool selection accuracy (TSA).** Measures whether the profile invokes `agent_router` when a
  question should be routed to a subagent.
- **Tool execution accuracy (TEA).** Measures whether `agent_router` routes the question to the
  expected subagent (`subagent_name`).

For instructions on creating a ground truth evaluation dataset (`ground_truth_invocations`), along
with details on how TSA and TEA are graded, see
[Dataset format](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-agent-evaluation-dataset-format)
and
[Tool selection and execution metrics ground truth](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-cortex-agent-evaluation-tool-metrics).
For details on the `agent_router` tool specification and inputs, see
[Route questions between agents with the agent router](/user-guide/snowflake-cortex/cortex-agents-router) and
[Cortex Agents tools](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agents-tools).
