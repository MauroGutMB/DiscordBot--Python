from discord.ext import commands
import random



class JokenpoCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jokenpo(self, ctx):
        escolhas = ['Pedra', 'Papel', 'Tesoura']
        await ctx.send(f'Escolha entre  {', '.join([es for es in escolhas])}')
        try:           
            msg = await self.bot.wait_for('message', check= lambda message: message.author == ctx.message.author, timeout= 10)
            jgdr_input = msg.content.capitalize().strip()
            bot_input = random.choice(escolhas)

            if jgdr_input not in escolhas:
                await ctx.send("Por favor, insira uma escolha válida")
            else: 

                regras = {
                    "Pedra":"Tesoura", "Papel":"Pedra", "Tesoura":"Papel"
                }

                await ctx.send(f'{ctx.message.author} --> {jgdr_input} \n{self.bot.user.name} --> {bot_input}' )

                match jgdr_input:
                    case _ if jgdr_input == bot_input:
                        await ctx.send("Empate!")
                    case _ if regras[f'{jgdr_input}'] == bot_input:
                        await ctx.send("Vitória!")
                    case _:
                        await ctx.send("Derrota!")

                
        except Exception as e:
            await ctx.send("Erro.")
            print(e)

async def setup(bot):
     await bot.add_cog(JokenpoCmd(bot))
