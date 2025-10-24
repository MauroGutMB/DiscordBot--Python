from discord.ext import commands
import discord
import os
import tokenB as tk

token = tk.token

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all(), case_insensitive=True, strip_after_prefix=True)

# Leitura de Comandos na pasta 'comandos'

async def ler_cmds():
    '''
    Leitura de comandos do diretório especificado de forma recursiva
    '''
    categorias = ['moderacao', 'utilitarios', 'misc', 'outros']
    
    for categoria in categorias:
        caminho_categoria = os.path.join('comandos', categoria)
        
        if os.path.exists(caminho_categoria) and os.path.isdir(caminho_categoria):
            for comando_dir in os.listdir(caminho_categoria):
                caminho_comando = os.path.join(caminho_categoria, comando_dir)
                
                if os.path.isdir(caminho_comando):
                    # Procura pelo arquivo .py dentro do diretório do comando
                    for arquivo in os.listdir(caminho_comando):
                        if arquivo.endswith('.py'):
                            # Carrega a extensão no formato: comandos.categoria.comando.arquivo
                            extensao = f'comandos.{categoria}.{comando_dir}.{arquivo[:-3]}'
                            try:
                                await bot.load_extension(extensao)
                                print(f'✓ Carregado: {extensao}')
                            except Exception as e:
                                print(f'✗ Erro ao carregar {extensao}: {e}')



@bot.event
async def on_ready():
    print(f'Logado com sucesso como {bot.user}')
    await ler_cmds()


bot.run(token)
