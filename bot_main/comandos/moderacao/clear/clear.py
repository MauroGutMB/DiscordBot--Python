from discord.ext import commands

class ClearCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_text = """
        **Comando:** -clear
        **Parâmetros:** 
        - `quantidade` (int): Número de mensagens a serem deletadas
        
        **Permissões:** Gerenciar Mensagens
        
        **Descrição:** Deleta uma quantidade específica de mensagens no canal atual.
        
        **Uso:** `-clear <quantidade>`
        **Exemplo:** `-clear 10` (deleta as últimas 10 mensagens)
        """

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, clear: int):
       await ctx.message.delete()
       await ctx.channel.purge(limit=clear) 

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para usar esse comando.")
       

async def setup(bot):
     await bot.add_cog(ClearCmd(bot))
