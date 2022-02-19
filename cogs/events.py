from discord.ext import commands
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')
        await self.bot.change_presence(activity=discord.Game(name=">help"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

def setup(bot):
    bot.add_cog(Events(bot))