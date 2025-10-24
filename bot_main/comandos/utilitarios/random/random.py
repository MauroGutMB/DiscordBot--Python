from discord.ext import commands
import random

class RandCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx):
       valor = random.randint(1, 100)
       await ctx.send(f'Número aleatório: {valor}')

async def setup(bot):
     await bot.add_cog(RandCmd(bot))
