# CoCo CLI keyboard shortcuts

Master CoCo CLI with these keyboard shortcuts for efficient navigation.

## Input shortcuts

| Shortcut | Action |
| --- | --- |
| Enter | Submit message |
| Ctrl-J | Insert newline (multiline input) |
| Ctrl/Cmd-V | Paste from clipboard |
| Ctrl-C | Cancel/interrupt (double-tap to exit) |
| Esc | Cancel the current action or dismiss the active overlay (context-dependent) |
| Ctrl-K | Kill line (delete from cursor to end of line) |
| Ctrl-Y | Yank (paste killed text) |
| Ctrl-A | Move to line start |
| Ctrl-E | Move to line end |
| Ctrl-B | Move cursor left |
| Ctrl-F | Move cursor right |
| Ctrl-D | Delete character under cursor |

Expand

Show lessSee more

## View shortcuts

| Shortcut | Action |
| --- | --- |
| Ctrl-T | Open table viewer (cycle forward through cached SQL query results) |
| Ctrl-O | Cycle display mode: compact → expanded → transcript |
| Alt-T | Open or close the fullscreen todo viewer |
| Alt-G | Open fullscreen web search results view |
| Ctrl-S | Open or close the background agent (subagent) picker |
| Ctrl-B | If a bash tool call is running, move it to the background; otherwise go back one level |
| ? | Toggle help overlay (only when the input line is empty) |

Expand

Show lessSee more

## Mode shortcuts

| Shortcut | Action |
| --- | --- |
| Ctrl-P | Toggle plan mode |
| Ctrl-G | Toggle team mode |
| Shift-Tab | Cycle permission level (confirm actions ↔ bypass safeguards) |

Expand

Show lessSee more

Plan mode (Ctrl-P) and team mode (Ctrl-G) are independent toggles. They are not steps in the Shift-Tab permission-level cycle.

## History navigation

| Shortcut | Action |
| --- | --- |
| Ctrl-R | Open history search; press again for the next older match |
| Ctrl-S | While history search is open, go to the previous (newer) match |
| Ctrl-G | Cancel history search |
| Esc | Cancel history search |
| Up / Down | Navigate history (when at top/bottom of input) |
| Option-Up | Previous history entry |
| Option-Down | Next history entry |

Expand

Show lessSee more

Ctrl-S and Ctrl-G are context-dependent: outside of history search, Ctrl-S opens the background agent picker and Ctrl-G toggles team mode.

### Table viewer shortcuts

Additional shortcuts for the table viewer (Ctrl-T):

| Shortcut | Action |
| --- | --- |
| Tab | Cycle to next table |
| Shift-Tab | Cycle to previous table |
| c | Copy query to clipboard |

Expand

Show lessSee more

## Auto-complete triggers

Typing one of the trigger characters below begins auto-completion for commands, file paths, skills, or Snowflake tables.

| Trigger | Action |
| --- | --- |
| / | Slash command completion |
| @ | File path completion |
| $ | Skill completion |
| # | Snowflake table completion |
| Tab | Accept suggestion |
| Up / Down | Navigate suggestions |

Expand

Show lessSee more

## Display modes

Press Ctrl-O to cycle through Compact, Expanded, and Transcript display modes for tool execution details.

Compact mode (Default)
:   - Minimal tool execution display
    - Shows summary of operations

Expanded mode
:   - Full tool execution details
    - Complete input/output display

Transcript mode
:   - Full scrollable conversation transcript

## Quick reference card

```
┌──────────────────────────────────────────────────────────┐
│                  CORTEX CODE SHORTCUTS                   │
├──────────────────────────────────────────────────────────┤
│  INPUT                  │  VIEW                          │
│  Enter      Submit      │  Ctrl-T    Table viewer        │
│  Ctrl-J     Newline     │  Ctrl-O    Cycle display mode   │
│  Ctrl-C     Cancel      │  Alt-T     Todo viewer          │
│  Ctrl-R     History     │  Alt-G     Web search results   │
│  Esc        Cancel      │  Ctrl-S    Subagent picker      │
│                         │  ?         Help overlay        │
├─────────────────────────┼────────────────────────────────┤
│  NAVIGATION             │  AUTOCOMPLETE                  │
│  Up/k       Up          │  /         Commands            │
│  Down/j     Down        │  @         Files               │
│  g          Top         │  $         Skills              │
│  G          Bottom      │  #         Tables              │
│  q/Esc      Exit        │  Tab       Accept              │
├─────────────────────────┴────────────────────────────────┤
│  Shift-Tab  Cycle permission level (confirm ↔ bypass)     │
│  Ctrl-P     Toggle plan mode   Ctrl-G  Toggle team mode   │
└──────────────────────────────────────────────────────────┘
```

## Tips

- **Use Ctrl-O often**: Switch between compact, expanded, and transcript display modes based on what you need to see.
- **Master Ctrl-R**: History search is powerful for repeating complex prompts.
- **Vim-style navigation**: The h/j/k/l keys work everywhere for cursor movement.
- **Double-tap patterns**: For example, Ctrl-C Ctrl-C exits.
