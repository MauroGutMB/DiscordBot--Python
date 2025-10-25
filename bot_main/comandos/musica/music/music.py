import discord
from discord.ext import commands
import asyncio
import yt_dlp
import random
from collections import deque


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}  # Dicionário para armazenar filas por servidor
        self.now_playing = {}  # Música atual por servidor
        
        # Configurações do yt-dlp
        self.ytdl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0',
        }
        
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_format_options)
        
        self.help_text = """
        **Comandos de Música:** 
        
        **-play <URL>** - Adiciona música à fila e toca
        **-connect** - Conecta o bot ao seu canal de voz
        **-disconnect** - Desconecta o bot do canal de voz
        **-pause** - Pausa a música atual
        **-skip** - Pula para a próxima música
        **-shuffle** - Embaralha a fila de músicas
        **-queue** - Mostra a fila de músicas
        **-np** - Mostra a música tocando atualmente
        
        **Descrição:** Sistema completo de reprodução de músicas do YouTube e Spotify.
        """

    def get_queue(self, guild_id):
        """Obtém ou cria uma fila para o servidor"""
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()
        return self.queues[guild_id]

    async def extract_info(self, url):
        """Extrai informações da música do YouTube/Spotify"""
        loop = asyncio.get_event_loop()
        
        try:
            data = await loop.run_in_executor(
                None, 
                lambda: self.ytdl.extract_info(url, download=False)
            )
            
            if data is None:
                return None
            
            # Se for playlist, pegar apenas a primeira
            if 'entries' in data:
                # Se for playlist do Spotify, converter cada música
                if 'spotify' in url.lower():
                    entries = []
                    for entry in data['entries']:
                        if entry:
                            entries.append({
                                'title': entry.get('title', 'Desconhecido'),
                                'url': entry.get('url'),
                                'webpage_url': entry.get('webpage_url', url),
                                'duration': entry.get('duration', 0),
                                'thumbnail': entry.get('thumbnail')
                            })
                    return entries
                else:
                    data = data['entries'][0]
            
            return [{
                'title': data.get('title', 'Desconhecido'),
                'url': data.get('url'),
                'webpage_url': data.get('webpage_url', url),
                'duration': data.get('duration', 0),
                'thumbnail': data.get('thumbnail')
            }]
            
        except Exception as e:
            print(f"Erro ao extrair informações: {e}")
            return None

    def play_next(self, guild_id, ctx):
        """Toca a próxima música da fila"""
        queue = self.get_queue(guild_id)
        
        if len(queue) > 0:
            next_song = queue.popleft()
            self.now_playing[guild_id] = next_song
            
            try:
                source = discord.FFmpegPCMAudio(next_song['url'], **self.ffmpeg_options)
                
                ctx.voice_client.play(
                    source,
                    after=lambda e: self.play_next(guild_id, ctx) if e is None else print(f"Erro no player: {e}")
                )
                
                # Enviar embed da música tocando
                embed = discord.Embed(
                    title="🎵 Tocando Agora",
                    description=f"**{next_song['title']}**",
                    color=discord.Color.green()
                )
                
                if next_song.get('thumbnail'):
                    embed.set_thumbnail(url=next_song['thumbnail'])
                
                if next_song.get('duration'):
                    minutes, seconds = divmod(next_song['duration'], 60)
                    embed.add_field(name="⏱️ Duração", value=f"{int(minutes)}:{int(seconds):02d}")
                
                if next_song.get('webpage_url'):
                    embed.add_field(name="🔗 Link", value=f"[Clique aqui]({next_song['webpage_url']})")
                
                asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.bot.loop)
                
            except Exception as e:
                print(f"Erro ao reproduzir: {e}")
                self.play_next(guild_id, ctx)
        else:
            self.now_playing[guild_id] = None

    @commands.command()
    async def play(self, ctx, *, url: str = None):
        """Toca uma música do YouTube ou Spotify"""
        
        # Se não forneceu URL, mostrar instruções
        if url is None:
            embed = discord.Embed(
                title="❌ URL não fornecida",
                description="Você precisa fornecer um link do YouTube ou Spotify!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📖 Como usar",
                value="**Uso:** `-play <URL>`\n\n**Exemplos:**\n`-play https://youtube.com/watch?v=...`\n`-play https://open.spotify.com/track/...`",
                inline=False
            )
            embed.set_footer(text="💡 Dica: Você precisa estar em um canal de voz!")
            return await ctx.send(embed=embed)
        
        # Verificar se o usuário está em canal de voz
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você precisa estar em um canal de voz para usar este comando!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        # Conectar ao canal se não estiver conectado
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        
        # Mostrar que está processando
        processing_embed = discord.Embed(
            title="⏳ Processando...",
            description="Buscando informações da música...",
            color=discord.Color.blue()
        )
        processing_msg = await ctx.send(embed=processing_embed)
        
        try:
            songs = await self.extract_info(url)
            
            if not songs:
                embed = discord.Embed(
                    title="❌ Erro",
                    description="Não foi possível encontrar a música. Verifique se o link está correto.",
                    color=discord.Color.red()
                )
                return await processing_msg.edit(embed=embed)
            
            guild_id = ctx.guild.id
            queue = self.get_queue(guild_id)
            
            # Adicionar músicas à fila
            for song in songs:
                queue.append(song)
            
            # Criar embed de confirmação
            if len(songs) == 1:
                embed = discord.Embed(
                    title="✅ Adicionado à fila",
                    description=f"**{songs[0]['title']}**",
                    color=discord.Color.green()
                )
                
                if songs[0].get('thumbnail'):
                    embed.set_thumbnail(url=songs[0]['thumbnail'])
                
                if songs[0].get('duration'):
                    minutes, seconds = divmod(songs[0]['duration'], 60)
                    embed.add_field(name="⏱️ Duração", value=f"{int(minutes)}:{int(seconds):02d}")
                
                embed.add_field(name="📊 Posição na fila", value=f"#{len(queue)}")
            else:
                embed = discord.Embed(
                    title="✅ Playlist adicionada",
                    description=f"**{len(songs)}** músicas adicionadas à fila!",
                    color=discord.Color.green()
                )
            
            embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await processing_msg.edit(embed=embed)
            
            # Se não está tocando nada, começar a tocar
            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                self.play_next(guild_id, ctx)
                
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao processar a música:\n```{str(e)}```",
                color=discord.Color.red()
            )
            await processing_msg.edit(embed=embed)

    @commands.command()
    async def connect(self, ctx):
        """Conecta o bot ao canal de voz do usuário"""
        
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você precisa estar em um canal de voz!",
                color=discord.Color.red()
            )
            embed.set_footer(text="💡 Entre em um canal de voz e tente novamente")
            return await ctx.send(embed=embed)
        
        if ctx.voice_client:
            embed = discord.Embed(
                title="⚠️ Aviso",
                description="Já estou conectado a um canal de voz!",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed)
        
        channel = ctx.author.voice.channel
        await channel.connect()
        
        embed = discord.Embed(
            title="✅ Conectado",
            description=f"Conectado ao canal **{channel.name}**!",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Use -play <URL> para tocar músicas")
        await ctx.send(embed=embed)

    @commands.command()
    async def disconnect(self, ctx):
        """Desconecta o bot do canal de voz"""
        
        if not ctx.voice_client:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não estou conectado a nenhum canal de voz!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        guild_id = ctx.guild.id
        
        # Limpar fila
        if guild_id in self.queues:
            self.queues[guild_id].clear()
        if guild_id in self.now_playing:
            del self.now_playing[guild_id]
        
        await ctx.voice_client.disconnect()
        
        embed = discord.Embed(
            title="👋 Desconectado",
            description="Desconectado do canal de voz e fila limpa!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        """Pausa a música atual"""
        
        if not ctx.voice_client:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não estou conectado a nenhum canal de voz!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = discord.Embed(
                title="⏸️ Pausado",
                description="Música pausada!",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Use -play para retomar")
            await ctx.send(embed=embed)
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = discord.Embed(
                title="▶️ Retomado",
                description="Música retomada!",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description="Nenhuma música está tocando!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        """Pula para a próxima música"""
        
        if not ctx.voice_client:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não estou conectado a nenhum canal de voz!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        if not ctx.voice_client.is_playing():
            embed = discord.Embed(
                title="❌ Erro",
                description="Nenhuma música está tocando!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        ctx.voice_client.stop()
        
        embed = discord.Embed(
            title="⏭️ Pulado",
            description="Música pulada!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def shuffle(self, ctx):
        """Embaralha a fila de músicas"""
        
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if len(queue) == 0:
            embed = discord.Embed(
                title="❌ Erro",
                description="A fila está vazia!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        # Converter deque para lista, embaralhar e converter de volta
        queue_list = list(queue)
        random.shuffle(queue_list)
        self.queues[guild_id] = deque(queue_list)
        
        embed = discord.Embed(
            title="🔀 Embaralhado",
            description=f"Fila embaralhada! **{len(queue_list)}** músicas reorganizadas.",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        """Mostra a fila de músicas"""
        
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        embed = discord.Embed(
            title="🎵 Fila de Músicas",
            color=discord.Color.blue()
        )
        
        # Música tocando atualmente
        if guild_id in self.now_playing and self.now_playing[guild_id]:
            current = self.now_playing[guild_id]
            embed.add_field(
                name="▶️ Tocando Agora",
                value=f"**{current['title']}**",
                inline=False
            )
        
        # Próximas músicas
        if len(queue) > 0:
            queue_text = ""
            for i, song in enumerate(list(queue)[:10], 1):
                duration = ""
                if song.get('duration'):
                    minutes, seconds = divmod(song['duration'], 60)
                    duration = f" `[{int(minutes)}:{int(seconds):02d}]`"
                queue_text += f"`{i}.` {song['title']}{duration}\n"
            
            embed.add_field(
                name=f"📋 Próximas ({len(queue)} na fila)",
                value=queue_text,
                inline=False
            )
            
            if len(queue) > 10:
                embed.set_footer(text=f"E mais {len(queue) - 10} músicas...")
        else:
            if guild_id not in self.now_playing or not self.now_playing[guild_id]:
                embed.description = "📭 A fila está vazia!\n\nUse `-play <URL>` para adicionar músicas."
        
        await ctx.send(embed=embed)

    @commands.command(name='np')
    async def nowplaying(self, ctx):
        """Mostra a música tocando atualmente"""
        
        guild_id = ctx.guild.id
        
        if guild_id not in self.now_playing or not self.now_playing[guild_id]:
            embed = discord.Embed(
                title="❌ Nenhuma música tocando",
                description="Use `-play <URL>` para tocar uma música!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        song = self.now_playing[guild_id]
        
        embed = discord.Embed(
            title="🎵 Tocando Agora",
            description=f"**{song['title']}**",
            color=discord.Color.purple()
        )
        
        if song.get('thumbnail'):
            embed.set_thumbnail(url=song['thumbnail'])
        
        if song.get('duration'):
            minutes, seconds = divmod(song['duration'], 60)
            embed.add_field(name="⏱️ Duração", value=f"{int(minutes)}:{int(seconds):02d}")
        
        if song.get('webpage_url'):
            embed.add_field(name="🔗 Link", value=f"[Clique aqui]({song['webpage_url']})")
        
        queue = self.get_queue(guild_id)
        if len(queue) > 0:
            embed.add_field(name="📊 Próximas na fila", value=f"{len(queue)} músicas", inline=False)
        
        embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
