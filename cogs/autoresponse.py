from discord.ext import commands
import discord


class Autoresponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.autoresponse = self
        bot.logger.info("Initialised Autoresponse")

    async def can_send_message(self, last_message):
        import datetime
        difference = datetime.datetime.now() - last_message
        self.bot.logger.info("Timer total seconds debug: {time}".format(time=difference.total_seconds()))
        if difference.total_seconds() < 120:
            return False
        else:
            return True

    async def check_last_message(self, message):
        import datetime
        if message.channel.name not in self.bot.last_message.keys():
            self.bot.last_message[message.channel.name] = datetime.datetime.now()
            return True
        elif await self.can_send_message(self.bot.last_message[message.channel.name]):
            self.bot.last_message[message.channel.name] = datetime.datetime.now()
            return True
        else:
            return False

    async def auto_response_message(self, ctx, message: str = None, trigger: str = None):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.author.send(content=message.format(ctx=ctx))
        elif await self.check_last_message(message=ctx):
            self.bot.logger.info(
                "Auto-Response Triggered, Trigger: {trigger} sending to channel {ctx.channel.name} Triggering-Message: {ctx.content}".format(
                    trigger=trigger, ctx=ctx))
            await ctx.channel.send(content=message.format(ctx=ctx))
        else:
            self.bot.logger.info(
                "Auto-Response Triggered, Trigger: {trigger} sending via PM to {ctx.author.name} Triggering-Message: {ctx.content} Last Message: {last}".format(
                    trigger=trigger, ctx=ctx, last=self.bot.last_message[ctx.channel.name]))
            try:
                await ctx.author.send(content=message.format(ctx=ctx))
                await ctx.add_reaction("📬")
            except discord.errors.Forbidden:
                await ctx.add_reaction('⛔')
                self.bot.logger.info("Auto-Response Could not DM User {ctx.author} received Forbidden".format(ctx=ctx))


def setup(bot):
    bot.add_cog(Autoresponse(bot))
