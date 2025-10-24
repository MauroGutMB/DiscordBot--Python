from discord.ext import commands
import random

class RandCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_text = """
        **Comando:** -random
        **Parâmetros:** Nenhum
        
        **Retorno:** Um número aleatório entre 1 e 100
        
        **Descrição:** Gera e retorna um número aleatório entre 1 e 100.
        
        **Uso:** `-random`
        **Exemplo:** `-random` (retorna: "Número aleatório: 42")
        """

    @commands.command()
    async def random(self, ctx):
       valor = random.randint(1, 100)
       await ctx.send(f'Número aleatório: {valor}')

async def setup(bot):
     await bot.add_cog(RandCmd(bot))
