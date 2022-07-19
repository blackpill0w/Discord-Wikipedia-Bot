import discord
from discord.ext import commands
import wikipedia

TOKEN_FILE = 'token.txt'
TOKEN = ''
with open(TOKEN_FILE, 'r') as f:
    TOKEN = f.read().strip()

bot = commands.Bot(command_prefix='/')
last_search_suggestions = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def wikisearch(message, arg, n_res = 10):
    global last_search_suggestions
    last_search_suggestions = wikipedia.search(arg, results=n_res)
    search_results = ''
    for i, item in enumerate(last_search_suggestions):
        search_results += f'{i+1} - {item}\n'
    response = f'Search results: ```{search_results}```'
    await message.channel.send(response)

@bot.command()
async def wikidef(message, arg:str, n_sentences = 10):
    global last_search_suggestions
    response = ''
    if arg[0] == '*' and arg[1:].isdigit():
        i = int(arg[1:])
        if (i < len(last_search_suggestions)):
            print('here')
            summary = wikipedia.summary(last_search_suggestions[i], sentences=n_sentences)
            response = f'Result (from {wikipedia.page(arg).url}): ```{summary}```'
            last_search_suggestions.clear()
        else:
            response = 'Sorry, there was an error.'
    else:
        try:
            summary = wikipedia.summary(arg, sentences=n_sentences)
            response = f'Result (from {wikipedia.page(arg).url}): ```{summary}```'
            last_search_suggestions.clear()
        except wikipedia.exceptions.DisambiguationError as e:
            last_search_suggestions = e.options
            suggestions = ''
            for i, item in enumerate(last_search_suggestions):
               suggestions += f'{i+1} - {item}\n'
            response = f'''Sorry, I counldn't find what you are looking for, here are some suggestions:
            ```{suggestions}```
            '''
    await message.channel.send(response)


bot.run(TOKEN)
