import discord
import DiscordUtils
import humanfriendly

music_ = DiscordUtils.Music()

class Music(commands.Cog):
    """<:music:929100003178348634> Music commands"""
    def __init__(self, bot):
        self.bot = bot
        
    def now_playing_embed(self, ctx, song) -> discord.Embed:
        return discord.Embed(
            title=song.title,
            url=song.url,
            color=self.bot.color,
            description=f"""
            **Duration:** {humanfriendly.format_timespan(song.duration)}
            **Channel:** [{song.channel}]({song.channel_url})
            """
            ).set_image(url=song.thumbnail
            ).set_footer(text=f"Loop: {'✅' if song.is_looping else '❌'}", icon_url=ctx.guild.icon.url if ctx.guild.icon is not None else 'https://cdn.discordapp.com/embed/avatars/1.png'
            ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
    
    @commands.command()
    async def join(self, ctx):
        """Joins VC where you're in."""
        if not ctx.author.voice:
            return await ctx.send("You are not in a voice channel. Please join one.")
        
        if ctx.guild.me.voice and len(ctx.guild.me.voice.channel.members) > 1:
            return await ctx.send("Someone else is already using the bot.")
        
        try:
            await ctx.author.voice.channel.connect()
            await ctx.message.add_reaction('👍')
        except Exception as e:
            return await ctx.send(f"I wasn't able to connect to your voice channel.\nPlease make sure I have enough permissions.\nError: {e}")
        
    @commands.command(aliases=['dc'])
    async def leave(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("You're not in a voice channel.")
        if not ctx.guild.me.voice:
            return await ctx.send("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.send("I'm not in the same VC you're in.")
        player = music_.get_player(guild_id=ctx.guild.id)
        
        if player:
            try:
                await player.stop()
                await player.delete()
            except Exception:
                pass
            
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction('👋')
        
    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx):
        """See what's playing now."""
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("Nothing is playing rn.")
        if not ctx.voice_client.is_playing():
            return await ctx.send("No music playing rn ._.")
        song = player.now_playing()
        await ctx.send(embed=self.now_playing_embed(ctx, song))
        
    @commands.command()
    async def pause(self, ctx):
        """Pause the song."""
        if not ctx.author.voice:
            return await ctx.send("You're not in a VC.")
        if not ctx.guild.me.voice:
            return await ctx.send("I am not playing any songs ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.send("I'm not in the same VC as you.")
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I am not playing any songs ._.")
        try:
            await player.pause()
        except DiscordUtils.NotPlaying:
            return await ctx.send("I am not playing any songs ._.")
        await ctx.message.add_reaction("⏸️")
    
    @commands.command()
    async def resume(self, ctx):
        """Resume the song."""
        if not ctx.author.voice:
            return await ctx.send("You're not in a VC.")
        if not ctx.guild.me.voice:
            return await ctx.send("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.send("I'm not in the same VC as you.")
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I am not playing any songs ._.")
        try:
            await player.resume()
        except DiscordUtils.NotPlaying:
            return await ctx.send("I am not playing any songs ._.")
        await ctx.message.add_reaction("▶️")
