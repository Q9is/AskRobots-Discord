import openai
import discord
import pprint
import os
import aiohttp
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_KEY")
token = os.environ.get("DISCORD_TOKEN")
engine = os.environ.get("OPENAI_ENGINE", "text-davinci-002")

intents = discord.Intents.default()
pp = pprint.PrettyPrinter(indent=4)
bot = discord.Client(intents=intents)

# Dictionary to store chat history by channel
chat_histories = {}


# Asynchronous function to call the OpenAI API
async def call_openai_api(channel_id, message, api_model):
    # Get the chat history for the channel or set up a new history
    history = chat_histories.get(channel_id, [{"role": "system", "content": "You are a helpful assistant."}])

    # Add the user's message to the history
    history.append({"role": "user", "content": message.content})

    # Calculate the token count of the chat history and remove messages if the count is over the specified limit
    token_limit = 8000 if api_model == "gpt-4" else 4000
    token_count = sum(len(tokenizer(text["content"]).input_ids) for text in history)
    while token_count > token_limit:
        removed_message = history.pop(0)
        token_count -= len(tokenizer(removed_message["content"]).input_ids)

    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": api_model,
        "messages": history,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers) as response:
            result = await response.json()
            print("Result:", result)  # Add the print statement here
            if "error" in result:
                print("Error from OpenAI API:", result["error"])
                assistant_message = "An error occurred while processing your request. Please try again."
            else:
                assistant_message = result["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": assistant_message})
            chat_histories[channel_id] = history
            return assistant_message


@bot.event
async def on_ready():
    """
    Print a message to the console when the bot is ready.
    :return:
    """
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('Pong!')

    if message.content.startswith('$chat4'):
        prompt = message.content[6:]
        # Call OpenAI text completion API using GPT-4
        try:
            response = await call_openai_api(message.channel.id, message, "gpt-4")
        except openai.error.RateLimitError as error:
            response = "Open API rate limit exceeded."
            return
        chunk_size = 2000
        for i in range(0, len(response), chunk_size):
            await message.channel.send(response[i:i+chunk_size])
        pp.pprint(response)

    elif message.content.startswith('$chat'):
        prompt = message.content[5:]
        # Call OpenAI text completion API using GPT-3.5 Turbo
        try:
            response = await call_openai_api(message.channel.id, message, "gpt-3.5-turbo")
        except openai.error.RateLimitError as error:
            response = "Open API rate limit exceeded."
            return
        chunk_size = 2000
        for i in range(0, len(response), chunk_size):
            await message.channel.send(response[i:i+chunk_size])
        pp.pprint(response)

    if message.author == bot.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send('commands:\n$chat\n$chat4\n$help')


bot.run(token, reconnect=True)
