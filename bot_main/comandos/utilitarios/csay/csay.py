from discord.ext import commands


class ChannelSayCmd(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
        self.help_text = """
        **Comando:** -csay
        **Parâmetros:** 
        - `#canal` ou `id_canal` (opcional): Canal de destino
        - `mensagem` (str): Mensagem a ser enviada
        
        **Descrição:** Faz o bot enviar uma mensagem em um canal específico ou no canal atual. A mensagem original do usuário é deletada.
        
        **Uso:** 
        - `-csay <mensagem>` (envia no canal atual)
        - `-csay #canal <mensagem>` (envia no canal mencionado)
        - `-csay <id_canal> <mensagem>` (envia no canal pelo ID)
        
        **Exemplo:** 
        - `-csay Olá, mundo!`
        - `-csay #geral Bem-vindos!`
        - `-csay 123456789012345678 Mensagem`
        """
        

    @commands.command()
    async def csay(self, ctx, *, args=None):
        args = args.split(' ')
        id_canal = ctx.channel.id
        print(f'{ctx.author} - {id_canal}')

        if ctx.message.raw_channel_mentions:
            canal = ctx.message.raw_channel_mentions[0]
            canal = await self.bot.fetch_channel(int(canal))
            args = ' '.join(args[1:])
            await ctx.message.delete()
            await canal.send(f'{args}')

        elif len(args[0]) == 19 and args[0].isdigit():
            canal = args[0]
            canal = await self.bot.fetch_channel(int(canal))
            args = ' '.join(args[1:])
            await ctx.message.delete()
            await canal.send(f'{args}')
        
        else:
            args = ' '.join(args)
            await ctx.message.delete()
            await ctx.send(f'{args}')

async def setup(bot):
    await bot.add_cog(ChannelSayCmd(bot))
