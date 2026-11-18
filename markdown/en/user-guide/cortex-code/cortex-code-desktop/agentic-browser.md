# Agentic Browser

CoCo Desktop includes a built-in browser that the agent can use to browse the web,
test your applications, and interact with pages on your behalf. Think of it as giving the agent
its own browser tab — it can read pages, click buttons, fill out forms, and report back what it finds.

[![Agentic Browser panel showing navigation controls and a rendered web page](/static/images/user-guide/cortex-code/cortex-code-desktop/agentic-browser/browser-panel.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/agentic-browser/browser-panel.png)

## What’s new in v2.0.0

CoCo Desktop v2.0.0 includes an updated Agentic Browser as part of the redesigned interface. It adds the following features to the browser in v1.25.4 and earlier:

- **Agent activity indicators**: While CoCo works in the browser, the browser shows what it’s doing, such as “CoCo is clicking”, “CoCo is reading the page”, or “CoCo is filling in a form”. Select **Stop** to end the agent’s turn.
- **Comments on the page**: Use **Comment on Page** to click an element or drag across an area, type what should change, and select **Save**. Each comment appears as a numbered pin on the page. Press **Enter** on a pin to edit it, or **Delete** to remove it. Ask CoCo to address your comments, and it reads them from the browser, including the page and element that each comment refers to, and marks the ones it has addressed as resolved.
- **Multiple tabs**: Press **⌘T** (**Ctrl+T** on Windows) to open a new browser tab. You can have up to 10 browser tabs open at once. The editor area and the Agent view browser panel each have their own limit. When the limit is reached, close a tab to open another. CoCo can also open and close tabs.
- **A home page on new tabs**: In the Agent Window, a new browser tab opens a CoCo home page with example prompts that you can run to watch the agent use the browser. To open Google on new tabs instead, disable the `agentBrowser.homePage.enabled` setting.
- **Find in page**: Press **⌘F** (**Ctrl+F** on Windows) while the browser has focus to search the page.
- **More browser commands**: The Command Palette includes **New Browser Tab**, **Find in Page**, **Zoom In**, **Zoom Out**, **Reset Zoom**, **Clear Cookies and Cache**, **Open Browser in New Window**, and **Open Browser Settings**.
- **A switch to turn the browser off**: To turn off the Agentic Browser, disable the `agentBrowser.enabled` setting. When it’s off, browser tabs and the browser panel don’t load pages, links in chat open in your external browser, and the agent’s browser tools are unavailable. To turn it back on, select **Open Browser Settings**.

These features are part of the redesigned interface. If you disable the `snowflake.consumerGradeUI.enabled` setting to return to the previous interface, the Agentic Browser has the features that it had in v1.25.4.

## Agent view vs Editor view

The browser panel is available in both IDE views:

- **Agent view**: a full-screen workspace where the agent drives the workflow. The browser appears as a built-in panel alongside chat, terminal, and file changes. Toggle with ⌘E.
- **Editor view**: the traditional code editor layout. The browser opens as a tab in the editor area or in the sidebar. The agent is still available via the chat panel.

The browser works identically in both views. Your sessions carry over when you switch, so you can toggle freely depending on whether you want the agent or your code front and center.

## Opening the browser

- **Agent view**: click the Browser tab in the right-hand panel, or ask the agent to open a URL.
- **Editor view**: use ⌘ + Shift + B, or open the Browser view from the sidebar (globe icon).
- **Command Palette**: search for “Open Agentic Browser”.

## Toolbar controls

| Button | Action |
| --- | --- |
| **← →** | Navigate back and forward in history. |
| **Reload** | Refresh the current page. |
| **URL bar** | Type a URL and press Enter to navigate. |
| **Select Element** | Pick any element on the page and attach it to the chat — great for asking “fix this button” or “why does this look wrong?” |
| **Screenshot** | Capture the current page and attach it to the chat for the agent to review visually. |
| **DevTools** | Open Chromium Developer Tools for manual inspection. |
| **Copy URL** | Copy the current page URL to clipboard. |
| **Bookmark** | Bookmark the current page for quick access. |
| **Open External** | Open the current page in your system browser. |

Expand

Show lessSee more

## What the agent can do

When the agent uses the browser, it can:

- **Navigate** — open URLs, go back/forward, manage multiple tabs.
- **Read** — understand page structure, read text content, check console logs and network activity.
- **Interact** — click buttons, fill out forms, select dropdowns, upload files, drag and drop.
- **Wait** — wait for content to load or change before proceeding.
- **Capture** — take screenshots for visual verification.

The agent understands pages structurally, not as raw pixels. This makes interactions precise
and reliable — it knows exactly which button to click or which field to fill.

## Browsers in multiple chats

In Agent view, each chat has its own browser panel, and the agent’s browser tools act on the
panel of the chat that called them. A subagent uses its parent chat’s browser panel.

The agent can click, press keys, drag, and take screenshots only in a browser panel that’s on
screen. When a chat’s browser panel isn’t shown, for example because you switched to another
chat or closed the panel, those actions fail and the agent asks you to switch to that chat and
open its browser panel. The agent can still read the page, navigate, go back and forward, and
run scripts on the page.

Because of this, only the chat that you’re viewing can interact with its browser page. If you
run several sessions that use the browser at the same time, the sessions that you aren’t viewing
stop at their next click, key press, drag, or screenshot and wait for you to switch to them. For
browser tasks such as testing an app, stay on that chat until the agent finishes, or run them
one chat at a time.

If the agent opens a page in a chat whose browser panel hasn’t opened yet, the page opens when
you return to that chat. Until then, the agent can’t read the page.

## Sharing context with the agent

### Select Element

Click **Select Element** in the toolbar, then hover over any element on the page and click it.
The element’s structure and styles are attached to your chat. Then ask the agent anything about it —
“fix this alignment”, “make this responsive”, “what font is this using?”

### Screenshot to chat

Click **Screenshot** to capture what you’re seeing and share it with the agent.
Useful for visual bug reports, design comparisons, or asking “does this look right?”

## Testing local development servers

The browser works with `localhost` URLs, making it perfect for testing local apps:

1. Start your dev server (for example, `streamlit run app.py` or `npm run dev`).
2. Ask the agent to open it and test a workflow.
3. The agent navigates your app, interacts with the UI, and reports results.

Tip

Ask “start my app and test the login flow” — the agent will run the server, open the browser, and
walk through the entire flow autonomously.

## Example workflows

### Frontend development

Run your dev server, select a broken element, and ask “why is this not aligned?”
The agent inspects the page, identifies the issue, and fixes your source code directly.

### Web research

Ask “go to the Snowflake docs and find the syntax for CREATE DYNAMIC TABLE” —
the agent navigates, searches, and brings back the answer.

### End-to-end testing

Ask “test the signup flow — fill in the form, submit, and verify the success page” —
the agent walks through your entire app flow and reports what happened.

### Visual verification

Take a screenshot and ask “does this match the Figma design?” —
the agent compares what’s rendered to your requirements.

### API debugging

Ask “what network requests happen when I click Submit?” —
the agent monitors traffic and reports back the API calls, payloads, and responses.

## Security

The agentic browser runs within CoCo Desktop’s security model:

- The agent asks for your confirmation before performing sensitive actions.
- Cross-origin interactions (different domains within iframes) require explicit approval.
- All browser activity happens locally on your machine — nothing is sent to external servers beyond normal page requests.
- The agent respects your [permission mode](/user-guide/cortex-code/cortex-code-desktop/permission-modes) settings for browser actions.
