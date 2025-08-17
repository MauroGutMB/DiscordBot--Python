import discord
from discord.ext import commands

class ChangeNickCmd(commands.Cog):      
    def __init__(self, bot):
        self.bot = bot


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