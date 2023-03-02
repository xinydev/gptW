import argparse
import json
import logging
import sys

import openai

import gptw


def args_init():
    parser = argparse.ArgumentParser(
        description="\n".join(
            [
                "The ChatGPT command-line wrapper simplifies the execution of predetermined tasks through ChatGPT",
                "usage:",
                "",
                'ww e "今天天气怎么样"  # translate to English',
                'ww c "who are you?"  # translate to Chinese',
                "ww --list  # get all available commands",
            ]
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "cmd", help="cmd, run `ww --list` to get all available cmd", nargs="?", type=str
    )
    parser.add_argument(
        "text",
        help="text",
        type=str,
        nargs="*",
    )
    parser.add_argument("-k", "--key", dest="key", help="set api key")
    parser.add_argument("-f", "--file", dest="file", help="read from file")
    parser.add_argument(
        "-l",
        "--list",
        dest="list",
        action="store_true",
        default=False,
        help="list all available sub cmds",
    )

    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="enable debug output",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + gptw.__version__,
    )
    try:
        return parser.parse_args()
    except Exception:
        sys.exit(0)


def init_logging(debug: bool):
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


key_file = "/tmp/gptw-key.txt"


def set_apikey(key):
    with open(key_file, "w") as f:
        f.write(key)


def get_apikey():
    with open(key_file) as f:
        openai.api_key = f.readline().strip()


cfg_file = "gptw/config.json"


def get_configs():
    with open(cfg_file) as f:
        return json.load(f)["cmds"]


def ask_gpt(text):
    logging.debug(f"!!!ask:{text}")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
        temperature=0.2,
    )
    return str(completion.choices[0].message.content).strip()


def ask_gpt_with(pre, text):
    return ask_gpt(f'{pre}\n"{text}"')


def main():
    args = args_init()
    init_logging(args.debug)

    if args.key:
        logging.debug("key mode")
        set_apikey(args.key)
        exit(0)

    configs = get_configs()
    logging.debug(f"configs:{configs}")

    if args.list:
        print(f'{"cmd":<{3}} | {"meaning":<{30}} | {"example"}')
        for cfg in configs:
            print(
                f"{cfg: <{3}} | {configs[cfg]['_comment']:<{30}} | {configs[cfg]['example']}"
            )
        exit(0)

    try:
        get_apikey()
    except Exception:
        print("please run `ww --key sk-...` to set you OpenAI key first")
        exit(0)

    text = " ".join(args.text)
    if args.file:
        with open(args.file) as f:
            text = "\n".join(f.readlines())
    if not text:
        print("Please enter some content")
        exit(0)

    if not args.cmd or args.cmd not in configs:
        print("need a command")
        exit(0)

    logging.debug(f"cmd:{args.cmd},text:{text}")
    print(ask_gpt_with(configs[args.cmd]["prompt"], text))
