from discord.ext import commands


class ShutCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_text = """
        **Comando:** -shutd
        **Parâmetros:** Nenhum
        
        **Permissões:** Apenas o dono do bot
        
        **Descrição:** Desliga o bot completamente. Este comando só pode ser usado pelo proprietário do bot.
        
        **Uso:** `-shutd`
        
        **⚠️ Atenção:** Este comando desligará o bot e ele ficará offline até ser reiniciado manualmente.
        """
    
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
