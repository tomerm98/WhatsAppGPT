from datetime import datetime
import sys
import openai
from googletrans import Translator
from pandas import DataFrame
from whatstk import WhatsAppChat
from whatstk.utils.utils import ColnamesDf as Columns

MODEL_NAME = 'gpt-4'
SYSTEM_PROMPT = ('You are a WhatsApp conversation analyzer. '
                 'You will receive a list of messages in the format `author: content` and fulfill your instructions')

SHOULD_TRANSLATE = True  # translating the chat to english can help reduce token count
INSTRUCTIONS = 'List 5 things that were discussed in the conversation. One sentence each.'
START_TIME = datetime(2023, 1, 7)
END_TIME = datetime(2023, 1, 14)

translator = Translator()


def translate_usernames(chat: DataFrame) -> DataFrame:
    """
    Some names have multiple variations when translated to english and Google will pick one at random.
    So we translate each username only once and then update it in the entire chat.
    That way the english name of each user will stay consistent.
    """
    original_usernames = list(chat[Columns.USERNAME].unique())
    english_usernames = [t.text for t in translator.translate(original_usernames)]
    return chat.replace(dict(zip(original_usernames, english_usernames)))


def cut_chat(chat: DataFrame, start: datetime, end: datetime) -> DataFrame:
    date_column = chat[Columns.DATE]
    return chat.loc[(date_column >= start) & (date_column <= end)]


def serialize_chat(chat: DataFrame) -> str:
    messages = [
        f'{row[Columns.USERNAME]}: {row[Columns.MESSAGE]}'
        for _, row in chat.iterrows()
    ]
    return '\n'.join(messages)


def analyze_chat(serialized_chat: str, instructions: str) -> str:
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': instructions},
        {'role': 'user', 'content': serialized_chat},
    ]
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages
    )
    return response['choices'][0]['message']['content']


def run():
    path = sys.argv[1]
    print('Loading file...')
    chat = WhatsAppChat.from_source(path).df
    print(f'Chat file contains {len(chat)} messages')
    print(f'Cutting chat based on date range...')
    chat = cut_chat(chat, START_TIME, END_TIME)
    print(f'Chat now has only {len(chat)} messages in date range: {START_TIME.isoformat()} => {END_TIME.isoformat()}')

    if SHOULD_TRANSLATE:
        print('Translating usernames to English...')
        chat = translate_usernames(chat)

    usernames = ', '.join(chat[Columns.USERNAME].unique())
    print(f'Users in chat: {usernames}')

    print('Serializing chat...')
    serialized = serialize_chat(chat)

    if SHOULD_TRANSLATE:
        print('Translating messages to English...')
        serialized = translator.translate(serialized).text

    print(f'Chat analysis model: {MODEL_NAME}')
    print('Analysis instructions:')
    print(f'"{INSTRUCTIONS}"')
    print(f'Analyzing...')
    analysis = analyze_chat(serialized, INSTRUCTIONS)
    print()
    print('Result:')
    print('-----')
    print(analysis)


if __name__ == '__main__':
    run()
