# FAQ

## Does CoCo Desktop require WSL on Windows?

No. CoCo Desktop **does not require WSL**. WSL is entirely optional:

- On Windows, the agent’s terminal and shell tools use **PowerShell** by default, not WSL.
- The app probes for WSL only to offer it as an *additional* terminal profile. If WSL is installed, CoCo can list your WSL distributions as optional terminal profiles. If WSL isn’t installed, the app uses PowerShell and works normally.
- CoCo never blocks startup on WSL and never prompts you to install or upgrade it.

If you see a prompt to install or update WSL (“Windows Subsystem for Linux must be updated”),
it’s coming from something else on the machine, not from CoCo. It’s safe to dismiss for the
purpose of running CoCo Desktop.

## Why do I get “Not a valid Python interpreter”?

If selecting a Python interpreter (including one from a virtual environment) returns “Not a valid
Python interpreter,” the cause is usually the language server, not your Python installation.
Switch the Python language server to Jedi:

1. Open **Settings** (gear icon or `Cmd/Ctrl+,`).
2. Search for `python.languageServer`.
3. Set it to **Jedi**.
4. Run **Developer: Reload Window** from the Command Palette.

Jedi is the supported and default Python language server for CoCo Desktop. If the
interpreter is still rejected after switching to Jedi and reloading, report it as a bug.

## Does Snowflake use my prompts or conversations to train models?

CoCo Desktop is a Snowflake AI Feature. Per Snowflake’s AI features data-privacy principle,
**Snowflake never uses your Customer Data to train models made available to our customer base**.

How your inputs and outputs are classified and the terms that govern them are set out in the legal
notices for Snowflake AI Features. For the full, current terms, see
[Snowflake AI features](/guides-overview-ai-features) and the legal notices on the
[CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop) page.
