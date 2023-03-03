# GPT simplify your daily Workflow (gptW)

gptW has eliminated the cumbersome process of entering a series of pre-commands before using ChatGPT for ease of use.

## Example

### Translate

You can simply use the "ww" command without having to first instruct ChatGPT that the following task is a translation

Translate to English

```shell
$ ww e "今天天气怎么样"

How's the weather today?
```

Translate to Chinese

```shell
$ ww c "who are you? "

你是谁？(Nǐ shì shéi?)
```

### Polish the document

Polish a document, supporting files as input.

```shell
ww d -f README.md
```

### Code Review

```shell
$ ww r -f gptw/gptw.py

As an AI language model, I cannot run the code provided, but I can provide some feedback based on the code structure and syntax.

1. The code seems to be well-organized and follows PEP 8 guidelines for Python code.

2. The argparse module is used to parse command-line arguments, which is a good practice for command-line applications.

...

Overall, the code seems to be well-written and organized, but could benefit from some additional security measures and error handling.
```

### Ask

Ask ChatGPT directly

```shell
$ ww a "who are you? "

I am an AI language model created by OpenAI.
```

### Add your own custom command

Prepare to execute the command for chatGPT work and modify the gptw/config.json file
Then create a pull request, or you can also write the command you want to add in an issue

gtpw/config.json:

```json
{
    "version": "v1.0.0",
    "cmds": {
        "e": {
            "prompt": "Please translate the following text into English, and polish it to make it sound more natural and in line with native speaker conventions. Please refrain from providing any additional output beyond the translated text",
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
```

## Installation

```shell
pip install --upgrade gptw
ww --key sk-..... # set your OpenAI API key
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
