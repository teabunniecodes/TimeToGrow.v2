import twitchio
from twitchio.ext import commands, routines
from datetime import timedelta


# Mysty - (ref notes in bot.py line 38) So in setup you have access to the Bot which can be used to add your Component
async def setup(bot: commands.Bot) -> None:
    await bot.add_component(MyComponent(bot))


class MyComponent(commands.Component):
    def __init__(self, bot: commands.Bot):
        # Passing args is not required...
        # We pass bot here as an example...
        self.bot = bot
        self.ticker.start()

    # We use a listener in our Component to display the messages received.
    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

    @commands.command(aliases=["hello", "howdy", "hey"])
    async def hi(self, ctx: commands.Context) -> None:
        """Simple command that says hello!

        !hi, !hello, !howdy, !hey
        """
        await ctx.reply(f"Hello {ctx.chatter.mention}!")

    @commands.group(invoke_fallback=True)
    async def socials(self, ctx: commands.Context) -> None:
        """Group command for our social links.
        4
                !socials
        """
        await ctx.send("discord.gg/..., youtube.com/..., twitch.tv/...")

    @socials.command(name="discord")
    async def socials_discord(self, ctx: commands.Context) -> None:
        """Sub command of socials that sends only our discord invite.

        !socials discord
        """
        await ctx.send("discord.gg/...")

    @commands.command(aliases=["repeat"])
    @commands.is_moderator()
    async def say(self, ctx: commands.Context, *, content: str) -> None:
        """Moderator only command which repeats back what you say.

        !say hello world, !repeat I am cool LUL
        """
        await ctx.send(content)

    @commands.Component.listener()
    async def event_stream_online(self, payload: twitchio.StreamOnline) -> None:
        # Event dispatched when a user goes live from the subscription we made above...

        # Keep in mind we are assuming this is for ourselves
        # others may not want your bot randomly sending messages...
        await payload.broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"Hi... {payload.broadcaster}! You are live!",
        )

    # @commands.Component.listener()
    # # This gives you the custom rewards id
    # async def event_custom_redemption_add(self, payload: twitchio.ChannelPointsRedemptionAdd) -> None:
    #     print(payload.reward.id)

    # TODO put the reward ids in a DB or something to keep them organized
    reward_plant_id = "99c830d9-9edc-48ea-b6c0-6f2fb783d3cb"
    reward_attack_id = "c01fab00-196d-484e-84c7-6861097a8b6e"
    reward_water_id = "c0a30f3f-de19-4643-9e80-d37b1d283547"

    # sends a message when viewer plants a plant
    @commands.reward_command(id=reward_plant_id, invoke_when=commands.RewardStatus.fulfilled)
    async def plant(self, ctx: commands.Context) -> None:
        print("plant")
        assert ctx.redemption
        await ctx.send(f"{ctx.author} redeemed {ctx.redemption.reward.title} and planted a plant!")

    @commands.reward_command(id=reward_attack_id, invoke_when=commands.RewardStatus.fulfilled)
    async def attack(self, ctx: commands.Context, *, user: twitchio.User | str) -> None:
        assert ctx.redemption
        print(type(user))
        if isinstance(user, twitchio.User):
            await ctx.send(f"{ctx.author} redeemed {ctx.redemption.reward.title} and attacked {user.mention}")
        else:
            await ctx.send(f"{ctx.author} redeemed {ctx.redemption.reward.title} and attacked {user}")

    @commands.reward_command(id=reward_water_id, invoke_when=commands.RewardStatus.fulfilled)
    async def water(self, ctx: commands.Context) -> None:
        assert ctx.redemption
        await ctx.send(f"{ctx.author} redeemed {ctx.redemption.reward.title} and watered their plant!")

    @routines.routine(delta=timedelta(seconds=10))
    async def ticker(self) -> None:
        print(self.ticker.current_iteration)