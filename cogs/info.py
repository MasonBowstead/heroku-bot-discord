import discord
from discord.ext import commands
from .utils import Pyson, checks

member_info = Pyson('./cogs/data/member_info')


class Info:

    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @commands.command()
    async def add_info(self, ctx, member: discord.Member, *, information: str):
        ': Add information for a member.'
        if member:
            slot = {str(member.id): information}
            member_info.data.update(slot)
            member_info.save
            await ctx.author.send(f'Info added for {member.mention}')
        else:
            await ctx.author.send('Please mention a member to add info.')
        await ctx.message.delete()

    @commands.command()
    async def info(self, ctx, member: discord.Member=None):
        ': Check info about a member.'
        if not member:
            member = ctx.author
        info = member_info.data.get(str(member.id))
        if info:
            embed = discord.Embed(title=f'Application for {member.name}', description=info, color=discord.Color.blue())
            await ctx.author.send(embed=embed)
        else:
            await ctx.author.send(f'No info available for {member.mention}')

    @checks.is_admin()
    @commands.command(name='remove')
    async def _remove(self, ctx, member: discord.Member):
        ': Remove info for a player'
        if member:
            id = str(member.id)
            if id in member_info.data:
                del member_info.data[id]
                member_info.save
                await ctx.author.send(f'Info removed for {member.mention}')
            else:
                await ctx.author.send(f'No info available for {member.mention}')
        else:
            await ctx.author.send('Please mention a member to remove info.')


def setup(bot):
    bot.add_cog(Info(bot))
