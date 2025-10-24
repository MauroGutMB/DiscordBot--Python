from discord.ext import commands

class TesteCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_text = """
        **Comando:** -teste
        **Parâmetros:** 
        - `argumento` (str, opcional): Argumento de teste
        
        **Retorno:** Mensagem de teste com o argumento fornecido
        
        **Descrição:** Comando de teste para verificar se o bot está respondendo. A mensagem original é deletada.
        
        **Uso:** 
        - `-teste` (sem argumento)
        - `-teste <argumento>` (com argumento)
        
        **Exemplo:** 
        - `-teste` (retorna: "teste --> ")
        - `-teste ola` (retorna: "teste --> ola")
        """

    @commands.command()
    async def teste(self, ctx, a=""):
       await ctx.message.delete() 
       await ctx.send(f'teste --> {a}')
       

async def setup(bot):
     await bot.add_cog(TesteCmd(bot))
