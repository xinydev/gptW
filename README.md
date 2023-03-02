# GPT Wrapper (gptW)

The ChatGPT command-line wrapper simplifies the execution of predetermined tasks through ChatGPT.

## Installation

```shell
pip install --upgrade gptw
ww --key sk-..... # set your OpenAI API key
```

## Usage

### List all available commands

```shell
ww --list

cmd | meaning                        | example
e   | Translate into English         | ww e 你好
c   | Translate into Chinese         | ww c how r u
p   | Polish sentence                | ww p hwo are you
a   | Just ask ChatGPT directly      | ww a who are you
d   | Polish document                | ww d -f README.md
r   | Code Review                    | ww r -f gptw/gptw.py
```

### Use commands

Translate to English

```shell
ww e "今天天气怎么样"
How's the weather today?
```

Translate to Chinese

```shell
ww c "who are you? "
你是谁？(Nǐ shì shéi?)
```

Ask ChatGPT directly

```shell
ww a "who are you? "
I am an AI language model created by OpenAI.
```

Polish a document

```shell
ww d -f README.md
```

Even review your code

```shell
ww r -f gptw/gptw.py

As an AI language model, I cannot run the code provided, but I can provide some feedback based on the code structure and syntax.

1. The code seems to be well-organized and follows PEP 8 guidelines for Python code.

2. The argparse module is used to parse command-line arguments, which is a good practice for command-line applications.

3. The logging module is used to provide debug output, which is helpful for troubleshooting issues.

4. The code reads and writes to files, which can be a potential security risk if not handled properly. It is recommended to use secure file handling practices, such as validating user input and using file permissions.

5. The code uses the OpenAI API to generate responses, which is a powerful tool for natural language processing. However, it is important to ensure that the API key is kept secure and not exposed in the code or in any output.

6. The code could benefit from more comments and documentation to explain the purpose and functionality of each function and variable.

7. The code could also benefit from more error handling and validation of user input to prevent unexpected behavior or crashes.

Overall, the code seems to be well-written and organized, but could benefit from some additional security measures and error handling.
```

## Add your own commands

There is a config file located in "gptw/config.json". Add your command and then open a new PR.

```json
{
    "version": "v1.0.0",
    "cmds": {
        "e": {
            "prompt": "Please translate the following text into English, and polish it to make it sound more natural and in line with native speaker conventions. Please refrain from providing any additional output beyond the translated text",
            "_comment": "Translate into English"
        },
        "c": {
            "prompt": "Please translate the following text into Chinese, and polish it to make it sound more natural and in line with native speaker conventions. Please refrain from providing any additional output beyond the translated text",
            "_comment": "Translate into Chinese"
        },
        "p": {
            "prompt": "Please polish my following sentence, correct grammar errors and make it sound more natural. Output language according to the original language",
            "_comment": "Polish sentence"
        },
        "a": {
            "prompt": "",
            "_comment": "Just ask ChatGPT directly"
        },
        "d": {
            "prompt": "Polish the document below, correct grammar errors, and make the document more complete",
            "_comment": "Polish document"
        }
    }
}
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
