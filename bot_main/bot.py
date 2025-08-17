from discord.ext import commands
import discord
import os
import tokenB as tk

token = tk.token

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all(), case_insensitive=True, strip_after_prefix=True)

# Leitura de Comandos na pasta 'comandos'

async def ler_cmds():
    '''
    Leitura de comandos do diretório especificado
    '''
    for arquivo in os.listdir('comandos'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f'comandos.{arquivo[:-3]}')



@bot.event
async def on_ready():
    print(f'Logado com sucesso como {bot.user}')
    await ler_cmds()


bot.run(token)
