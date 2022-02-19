from discord.ext import commands
import discord
import os
import requests
import subprocess
import random

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title = "MetadataBot"
        )
        embed.add_field(name="prefix:", value=">", inline=False)
        embed.add_field(name="`>`help", value="Will show this message", inline=False)
        embed.add_field(name="`>`extractmetadata", value="Will extract metadata from uploaded image", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def extractmetadata(self, ctx, *, image_link: str = None):
        random_filename = ''.join(str(random.randint(0,9)) for _ in range (15))
        if len(ctx.message.attachments) == 0:
            if image_link == None:
                embed = discord.Embed(
                    title = "Error !",
                    description="Please provide a link or upload an image !"
                )
                await ctx.send(embed=embed)
            else:
                try:
                    url = requests.get(image_link).content
                    with open(''.join(random_filename), 'wb') as f:
                        f.write(url)
                    message = f'''```\n{subprocess.check_output(f"exiftool {random_filename}", shell=True, universal_newlines=True)}\n```'''
                    if len(message) > 4000:
                        hastebin_lnk = requests.post("https://www.toptal.com/developers/hastebin/documents", data=message.encode('utf-8'))
                        await ctx.send(f"Metadata is too big for Discord ! Click on the link to see it <https://www.toptal.com/developers/hastebin/{hastebin_lnk.json()['key']}>")
                    else:
                        await ctx.send(message)
                except Exception as e:
                    embed = discord.Embed(
                        title = "Error !",
                        description=f'''```
{e}```'''
                    )
                    await ctx.send(embed=embed)


            os.remove(random_filename)
        else:
            url = requests.get(ctx.message.attachments[0].url).content
            with open(f"{random_filename}", 'wb') as f:
                f.write(url)
            message = f'''```
{subprocess.check_output(f"exiftool {random_filename}", shell=True, universal_newlines=True)}```'''
            if len(message) > 4000:
                hastebin_lnk = requests.post("https://www.toptal.com/developers/hastebin/documents", data=message.encode('utf-8'))
                await ctx.send(f"Metadata is too big for Discord ! Click on the link to see it <https://www.toptal.com/developers/hastebin/{hastebin_lnk.json()['key']}>")
            else:
                await ctx.send(message)

            os.remove(random_filename)

def setup(bot):
    bot.add_cog(Commands(bot))