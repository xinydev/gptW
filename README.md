# GPT Simplify Your Daily Workflow (gptW)

No longer is it necessary to manually input prompts and interact with ChatGPT.

With the GPTW tool, prompt operations are fully automated! Simplify your daily workflow.

## Example

### Translate

You can simply use the "ww" command without having to first instruct ChatGPT that the following task is a translation.

Translate to English:

```shell
$ ww e "今天天气怎么样"
How's the weather today?
```

Translate to Chinese:

```shell
$ ww c "who are you? "
你是谁？(Nǐ shì shéi?)
```

### Polish the Document

Polish a document with files as input.

```shell
ww d -f README.md
```

### Code Review

```shell
$ ww r -f gptw/gptw.py
As an AI language model, I cannot run the code provided, but I can provide some feedback based on the code structure and syntax.

1. The code appears to be well-organized and follows the PEP 8 guidelines for Python code.

2. The argparse module is used to parse command-line arguments, which is a good practice for command-line applications.

...

Overall, the code seems to be well-written and organized, but could benefit from some additional security measures and error handling.
```

### Ask

Ask ChatGPT directly:

```shell
$ ww a "who are you? "
I am an AI language model created by OpenAI.
```

### Add Your Custom Prompt

Prepare your prompt and modify the gptw/config.json file following the existing format. Then, submit a PR or directly raise an issue to explain the command you want to add.

gtpw/config.json:

```json
{
    "version": "v1.0.0",
    "cmds": {
        ## cmd to use
        "e": {
            ## replace with your prompt
            "prompt": "Please translate the following text into English, and polish it to make it sound more natural and in line with native speaker conventions. Please refrain from providing any additional output beyond the translated text",
            ## A simple explanation of what this prompt is used for
            "_comment": "Translate into English"
        },
        ...
    }
}
```

Currently, the following workflows are supported. You can run "ww -l" to obtain the available workflows.

```shell
$ ww --list
cmd | meaning                        | example
e   | Translate into English         | ww e 你好
c   | Translate into Chinese         | ww c how r u
p   | Polish sentence                | ww p hwo are you
a   | Just ask ChatGPT directly      | ww a who are you
d   | Polish document                | ww d -f README.md
r   | Code Review                    | ww r -f gptw/gptw.py
dic | Dictionary                     | ww dic dictionary
```

## Installation

```shell
pip install --upgrade gptw
```

### OpenAI Config

```shell
ww --config provider=openai
ww --config openai-model=gpt-3.5-turbo
ww --config openai-token={YOUR_TOKEN}
```

### POE Config

```shell
ww --config provider=poe
ww --config poe-bot-name=chinchilla
ww --config poe-token={YOUR_TOKEN}
```

Bot names:

{'capybara': 'Sage', 'beaver': 'GPT-4', 'a2_2': 'Claude+', 'a2': 'Claude', 'chinchilla': 'ChatGPT', 'nutria': 'Dragonfly'}

### ChatGPT website

```shell
ww -c provider=gpt-web
ww -c gpt-web-model=gpt-4
ww -c gpt-web-token=  # https://chat.openai.com/api/auth/session copy the access_token session
ww -c gpt-web-proxy=  # https://github.com/acheong08/ChatGPT-Proxy-V4
```

### Azure OpenAI

```shell
ww -c provider=azure
ww -c azure-token={YOUR_TOKEN}
ww -c azure-endpoint
ww -c azure-depnam=
```

## Uninstall

```shell
pip uninstall gptw
```

## Development

```shell
pip install tox
make test
```
