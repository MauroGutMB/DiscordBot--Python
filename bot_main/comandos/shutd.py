from discord.ext import commands


class ShutCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden = True)
    @commands.is_owner()
    async def shutd(self, ctx):
        await ctx.send("Desligando.")
        await self.bot.close()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Você não tem permissão para usar esse comando.")


async def setup(bot):
     await bot.add_cog(ShutCmd(bot))