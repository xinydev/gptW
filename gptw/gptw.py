import argparse
import json
import logging
import os
import sys
from os.path import expanduser

import gptw


def args_init():
    parser = argparse.ArgumentParser(
        description="\n".join(
            [
                "GPT Simplifies Your Daily Workflow (gptW)",
                "",
                "Usage:",
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
    parser.add_argument(
        "-c", "--config", dest="config", help="set config key and value"
    )
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
        parser.print_help()
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


CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
prompts_file = os.path.join(CURRENT_FOLDER, "prompts.json")
config_file = os.path.join(expanduser("~"), ".gptw-config.txt")


def set_config(key, value):
    cfg = {}

    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump(cfg, f)

    with open(config_file) as f:
        cfg = json.load(f)

    cfg[key] = value

    with open(config_file, "w") as f:
        json.dump(cfg, f)


CONFIG = None


def get_config(key):
    if not CONFIG:
        with open(config_file) as f:
            CFG = json.load(f)
    try:
        return CFG[key]
    except Exception:
        print("config not found, run `ww --config` to set it")
        sys.exit(1)


def get_prompts():
    with open(prompts_file) as f:
        return json.load(f)["cmds"]


def ask_gpt(token, model, text):
    import openai

    logging.debug(f"!!!ask:{text}")
    openai.api_key = token
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        temperature=0.5,
    )
    return str(completion.choices[0].message.content).strip()


def ask_poe(token, bot_name, text):
    import poe

    poe.logger.setLevel(logging.WARNING)
    client = poe.Client(token)

    for chunk in client.send_message(bot_name, text, with_chat_break=True):
        pass
    # delete the 3 latest messages, including the chat break
    client.purge_conversation(bot_name, count=3)
    return chunk["text"]


def ask_gpt_web(token, proxy, model, text):
    os.environ["CHATGPT_BASE_URL"] = proxy
    logging.debug("proxy:" + os.environ["CHATGPT_BASE_URL"])

    from revChatGPT.V1 import Chatbot

    chatbot = Chatbot(
        config={
            "access_token": token,
            "paid": True,
            "model": model,
            "collect_analytics": False,
        }
    )
    response = ""
    for data in chatbot.ask(text):
        response = data["message"]
    return response


def ask_azure_multi_pass(token, endpoint, depname, text):
    msgs = [{"role": "user", "content": text}]
    for _ in range(5):
        resp = ask_azure(token, endpoint, depname, msgs)
        msgs.append({"role": "assistant", "content": resp})
        msgs.append({"role": "user", "content": "a better one"})
        print(resp)
        print("")
    return ""


def ask_azure(token, endpoint, depname, msgs):
    import openai

    logging.debug(f"!!!ask:{msgs}")
    openai.api_key = token
    openai.api_base = endpoint
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    completion = openai.ChatCompletion.create(
        engine=depname,
        messages=msgs,
        temperature=0.5,
    )
    resp = str(completion.choices[0].message.content).strip()
    logging.debug(f"!!!resp:{resp}")
    return str(completion.choices[0].message.content).strip()


def list_commands(prompts):
    print(f'{"cmd":<{3}} | {"meaning":<{30}} | {"example"}')
    for pmt in prompts:
        print(
            f"{pmt: <{3}} | {prompts[pmt]['_comment']:<{30}} | {prompts[pmt]['example']}"
        )


def main():
    args = args_init()
    init_logging(args.debug)
    logging.debug(f"src folder: {CURRENT_FOLDER}")

    if args.config:
        logging.debug("set config")
        k, v = args.config.split("=")
        set_config(k, v)
        exit(0)

    prompts = get_prompts()
    logging.debug(f"configs:{prompts}")

    if args.list:
        list_commands(prompts)
        exit(0)

    text = " ".join(args.text)
    if args.file:
        with open(args.file) as f:
            text = "\n".join(f.readlines())
    if not text:
        print("Please enter some content")
        exit(0)

    if not args.cmd or args.cmd not in prompts:
        print("need a command")
        exit(0)

    logging.debug(f"cmd:{args.cmd},text:{text}")

    msg = f'{prompts[args.cmd]["prompt"]}\n```{text.replace("```","")}```'

    if get_config("provider") == "openai":
        logging.debug("use openai")
        model = get_config("openai-model")
        token = get_config("openai-token")
        print(ask_gpt(token, model, msg))
    if get_config("provider") == "poe":
        logging.debug("use poe")
        token = get_config("poe-token")
        bot_name = get_config("poe-bot-name")
        print(ask_poe(token, bot_name, msg))
    if get_config("provider") == "gpt-web":
        logging.debug("use gpt-web")
        token = get_config("gpt-web-token")
        proxy = get_config("gpt-web-proxy")
        model = get_config("gpt-web-model")
        print(ask_gpt_web(token, proxy, model, msg))
    if get_config("provider") == "azure":
        logging.debug("use azure")
        token = get_config("azure-token")
        endpoint = get_config("azure-endpoint")
        depname = get_config("azure-depname")
        print(ask_azure_multi_pass(token, endpoint, depname, msg))
