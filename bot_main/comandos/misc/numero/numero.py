from discord.ext import commands
import random



class AdvNum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_text = """
        **Comando:** -numero
        **Parâmetros:** Nenhum
        
        **Retorno:** Resultado do jogo de adivinhação
        
        **Descrição:** Jogo de adivinhação onde você deve descobrir um número entre 1 e 100 que o bot está pensando.
        
        **Uso:** `-numero`
        
        **Como jogar:**
        1. Digite `-numero`
        2. O bot pensará em um número entre 1 e 100
        3. Envie seus palpites no chat
        4. O bot dirá se seu palpite é maior ou menor
        5. Você tem 3 chances de errar formato inválido
        6. Tempo limite de 20 segundos por resposta
        """

    @commands.command()
    async def numero(self, ctx):
        numero_advinhar = random.randint(1, 100)

        erros = 0
        tentativas = 0
        await ctx.send(f"{ctx.message.author}, Estou pensando num número entre 1 e 100, qual é o seu palpite?")
        
        while True:
            try:
                respostac = await ctx.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=20)
                resposta = respostac.content
                palpitec = "".join([n for n in resposta if n.isdigit()])

                
                check = False if palpitec == '' else True
                if check:
                    palpite = int(palpitec)

                if erros == 3:
                    await ctx.send("Tentativas excedidas.")
                    break

                if check == False:
                    await ctx.send("Você precisa inserir apenas números.")
                    erros += 1
                    continue
                    

                if palpite > 100 or palpite < 1 and check:
                    await ctx.send("Seu palpite é inválido.")
                    tentativas += 1
                
                elif palpite < numero_advinhar:
                    await ctx.send("Seu palpite é muito pequeno")
                    tentativas += 1

                elif palpite > numero_advinhar:
                    await ctx.send("Seu palpite é muito grande")
                    tentativas += 1
                    
                else:
                    await ctx.send(f"Seu palpite está correto! Eu pensei em '{numero_advinhar}'! Você acertou em {tentativas} tentativas!")

                    break
            
            except Exception as e:
                print(e)
                await ctx.send("Erro.")
                break

async def setup(bot):
     await bot.add_cog(AdvNum(bot))
