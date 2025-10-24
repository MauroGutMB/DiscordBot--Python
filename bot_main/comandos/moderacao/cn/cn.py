import discord
from discord.ext import commands

class ChangeNickCmd(commands.Cog):      
    def __init__(self, bot):
        self.bot = bot
        self.help_text = """
        **Comando:** -cn
        **Parâmetros:** 
        - `@membro` (opcional): Menção do membro para alterar o nick
        - `apelido` (str): Novo apelido desejado
        
        **Descrição:** Altera o apelido de um membro no servidor. Se nenhum membro for mencionado, altera seu próprio apelido.
        
        **Uso:** 
        - `-cn <novo_apelido>` (altera seu próprio nick)
        - `-cn @membro <novo_apelido>` (altera o nick de outro membro)
        
        **Exemplo:** 
        - `-cn NovoNome`
        - `-cn @Usuario AppelidoLegal`
        """

    @commands.command()
    async def cn(self, ctx, *, args=None):
        if args is None:
            return await ctx.send("Você precisa fornecer um apelido!")

        args = args.split(" ")
        membro = None

        if ctx.message.mentions:  
            membro = ctx.message.mentions[0]  
            nickname = " ".join(args[1:])  
        else:
            membro = ctx.author 
            nickname = " ".join(args)

        if not nickname:
            return await ctx.send("Você precisa fornecer um apelido válido!")

        try:
            await membro.edit(nick=nickname)
            await ctx.send(f'{ctx.author.mention} alterou o nick de {membro.mention} para "{nickname}".')
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para alterar este apelido.")
        except discord.HTTPException:
            await ctx.send("Ocorreu um erro ao tentar alterar o apelido.")
        
        


async def setup(bot):
     await bot.add_cog(ChangeNickCmd(bot))
