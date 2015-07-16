#!/usr/bin/env python3
import argparse
import logging
import time
from api import TelegramAPI, NumbersAPI, CatFactAPI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
boturl = 'https://api.telegram.org/bot'
commands = ['/number', '/cat']
num = NumbersAPI()
cat = CatFactAPI()


def command(command, text):
    logger.info('Parsing command {} with data: {}'.format(command, text))
    if command == '/number':
        try:
            number = int(text.split()[0])
        except ValueError:
            return "I do not recognize that as a number"
        except AttributeError:
            return "Please provide a number"
        result = num.number(number)
        return result
    elif command == '/cat':
        return cat.facts(number=1)[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--offset', '-o')
    parser.add_argument('--limit', '-l')
    parser.add_argument('--timeout', '-t')
    parser.add_argument('--wait', '-w')
    parser.add_argument('token')
    args = parser.parse_args()

    logger.info('Secret bot URL: {0}{1}/'.format(boturl, args.token))
    telegramapi = TelegramAPI(url='{0}{1}/'.format(boturl, args.token))

    offset = args.offset if args.offset else 0
    wait = args.wait if args.wait else 15
    while True:
        logger.info('Waiting {} seconds'.format(wait))
        time.sleep(wait)
        updates = telegramapi.get_updates(
            offset=offset,
            limit=args.limit,
            timeout=args.timeout)
        for update in updates:
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                if 'text' in message:
                    text = message['text'].split(maxsplit=1)
                    command_args = text[1] if len(text) == 2 else None
                    if text[0] in commands:
                        returntext = command(text[0], command_args)
                        if returntext:
                            telegramapi.send_message(chat_id, text=returntext)
            if update['update_id'] >= offset:
                offset = update['update_id'] + 1
