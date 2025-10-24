import discord
from discord.ext import commands


class HelpCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_text = """
        **Comando:** -help
        **Parâmetros:** 
        - `comando` (str, opcional): Nome do comando específico para ver detalhes
        
        **Descrição:** Exibe a lista de todos os comandos disponíveis ou informações detalhadas sobre um comando específico.
        
        **Uso:** 
        - `-help` (lista todos os comandos)
        - `-help <nome_comando>` (mostra ajuda detalhada do comando)
        
        **Exemplo:** 
        - `-help`
        - `-help jokenpo`
        - `-help clear`
        """

    @commands.command()
    async def help(self, ctx, comando: str = None):
        if comando is None:
            # Exibir lista de todos os comandos
            embed = discord.Embed(
                title="📚 Lista de Comandos Disponíveis",
                description="Use `-help <comando>` para ver informações detalhadas sobre um comando específico.",
                color=discord.Color.blue()
            )
            
            # Organizar comandos por categoria
            categorias = {
                'moderacao': {'emoji': '🛡️', 'comandos': []},
                'utilitarios': {'emoji': '🔧', 'comandos': []},
                'misc': {'emoji': '🎮', 'comandos': []},
                'outros': {'emoji': '⚙️', 'comandos': []}
            }
            
            # Coletar todos os comandos dos cogs
            for cog_name, cog in self.bot.cogs.items():
                # Pegar todos os comandos do cog
                for cmd in cog.get_commands():
                    if not cmd.hidden:  # Não mostrar comandos ocultos
                        # Determinar a categoria baseada no nome do módulo
                        module_path = cog.__module__
                        
                        if 'moderacao' in module_path:
                            categorias['moderacao']['comandos'].append(cmd.name)
                        elif 'utilitarios' in module_path:
                            categorias['utilitarios']['comandos'].append(cmd.name)
                        elif 'misc' in module_path:
                            categorias['misc']['comandos'].append(cmd.name)
                        elif 'outros' in module_path:
                            categorias['outros']['comandos'].append(cmd.name)
            
            # Adicionar campos ao embed por categoria
            nomes_categorias = {
                'moderacao': 'Moderação',
                'utilitarios': 'Utilitários',
                'misc': 'Diversão',
                'outros': 'Outros'
            }
            
            for cat_key, cat_data in categorias.items():
                if cat_data['comandos']:
                    comandos_formatados = ', '.join([f"`{cmd}`" for cmd in sorted(cat_data['comandos'])])
                    embed.add_field(
                        name=f"{cat_data['emoji']} {nomes_categorias[cat_key]}",
                        value=comandos_formatados,
                        inline=False
                    )
            
            embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await ctx.send(embed=embed)
            
        else:
            # Exibir ajuda específica de um comando
            comando_encontrado = None
            cog_encontrado = None
            
            # Buscar o comando em todos os cogs
            for cog_name, cog in self.bot.cogs.items():
                for cmd in cog.get_commands():
                    if cmd.name.lower() == comando.lower():
                        comando_encontrado = cmd
                        cog_encontrado = cog
                        break
                if comando_encontrado:
                    break
            
            if comando_encontrado and cog_encontrado:
                # Verificar se o cog tem help_text
                if hasattr(cog_encontrado, 'help_text'):
                    embed = discord.Embed(
                        title=f"📖 Ajuda: {comando_encontrado.name}",
                        description=cog_encontrado.help_text.strip(),
                        color=discord.Color.green()
                    )
                    embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                    await ctx.send(embed=embed)
                else:
                    # Caso não tenha help_text, mostrar mensagem básica
                    embed = discord.Embed(
                        title=f"📖 Ajuda: {comando_encontrado.name}",
                        description=f"**Uso:** `-{comando_encontrado.name}`\n\nNenhuma documentação adicional disponível.",
                        color=discord.Color.orange()
                    )
                    await ctx.send(embed=embed)
            else:
                # Comando não encontrado
                embed = discord.Embed(
                    title="❌ Comando não encontrado",
                    description=f"O comando `{comando}` não existe.\n\nUse `-help` para ver todos os comandos disponíveis.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCmd(bot))
