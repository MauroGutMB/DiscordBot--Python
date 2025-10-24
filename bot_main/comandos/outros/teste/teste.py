from discord.ext import commands

class TesteCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def teste(self, ctx, a=""):
       await ctx.message.delete() 
       await ctx.send(f'teste --> {a}')
       

async def setup(bot):
     await bot.add_cog(TesteCmd(bot))
