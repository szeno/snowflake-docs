# SnowConvert AI - Migration Assistant - Model Preference

The SnowConvert AI Migration Assistant supports configurable AI model preferences with automatic fallback functionality. This feature allows you to customize which AI models are used for generating fixes and in what order they should be attempted.

## Supported Models

The Migration Assistant supports the following AI models through Snowflake Cortex AI:

| Model | Status | Description |
| --- | --- | --- |
| Claude 3.7 Sonnet | Recommended | Best quality responses, optimized for migration assistance |
| Claude 3.5 Sonnet | Stable | High quality alternative if Claude 3.7 is unavailable |
| Claude 4 Sonnet | Experimental | Improved quality over Claude 3.7 Sonnet, latest Claude model |
| Llama 3.1 70B | Experimental | Results may vary, assistant optimized for Claude models |
| Mistral Large 2 | Experimental | Results may vary, assistant optimized for Claude models |

Expand

Show lessSee more

Warning

The Migration Assistant has been primarily optimized for Claude models. While other models are supported, they may provide varying quality results compared to the Claude models.

## How to Configure Model Preferences

Open VS Code Settings

- Go to File > Preferences > Settings (or Code > Preferences > Settings on macOS)
- Or use the keyboard shortcut: `Ctrl + ,` (Windows/Linux) or `Cmd + ,` (macOS)

Navigate to the Settings

- Search for **Snowflake: Snow Convert Migration Assistant: Model Preference**
- Or navigate to Extensions > Snowflake > **Snowflake: Snow Convert Migration Assistant: Model Preference**

Configure Your Preferences

- **Add models**
  - Select any model from the dropdown list to add it to your preferences
  - The model will be added to the end of your current list
- **Remove models**
  - Click the “X” next to any model to remove it from your preferences
  - You must have at least one model configured to use the assistant
- **Reorder models**
  - You can either:
    - Remove or add models to your desired order.
    - Change the model by clicking the “pencil” icon and selecting one of the available models.
  - The first model in the list will always be attempted first

### Default Configuration

By default, the Migration Assistant comes configured with this model preference order:

1. Claude 3.7 Sonnet (recommended)
2. Claude 3.5 Sonnet (high quality alternative)
3. Llama 3.1 70B (experimental)
4. Mistral Large 2 (experimental)

## Execution Order and Fallback Mechanism

The Migration Assistant uses an intelligent fallback system that works as follows:

1. **Sequential Execution**: Models are tried in the exact order you specify in your preference list
2. **Automatic Fallback**: If the first model fails or is unavailable, the assistant automatically attempts the next model in your list
3. **Complete Cycle**: The process continues through your entire model list until one succeeds or all models have been exhausted
4. **Error Handling**: If all models fail, you’ll receive detailed error information and suggestions for each attempted model

Example Execution Flow:

Copy code

```
1. Attempt: Claude 3.7 Sonnet → Failed (model unavailable in region)
2. Attempt: Claude 3.5 Sonnet → Failed (budget exceeded)
3. Attempt: Llama 3.1 70B → Success → Response generated
```
