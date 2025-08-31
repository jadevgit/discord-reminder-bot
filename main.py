"""
 ____        _ _              ____        _   
| __ )  ___ | | |_ ___  _ __ | __ )  ___ | |_ 
|  _ \ / _ \| | __/ _ \| '_ \|  _ \ / _ \| __|
| |_) | (_) | | || (_) | | | | |_) | (_) | |_ 
|____/ \___/|_|\__\___/|_| |_|____/ \___/ \__|
          Made by jadevgit                                      
"""


import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('API_KEY')


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)
        print("Slash commands synced to guild.")

        if not advertisement_post_reminder.is_running():
            advertisement_post_reminder.start()
        if not monday_post.is_running():
            monday_post.start()




intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1105867814058860544)
TIMEOZNE = ZoneInfo("Europe/London")

last_posted_date = None


class FeedbackSubmitModal(discord.ui.Modal, title="Submit feedback"):
    feedbackChannel = 1406011545527517348
    tOn_title = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label = "Title",
        required=True,
        placeholder="Enter the title of your feedback"
    )

    feedbackDesc = discord.ui.TextInput(
        style=discord.TextStyle.long,
        required= True,
        label="Feedback description",
        placeholder= "Enter text here"
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(self.feedbackChannel)

        embed = discord.Embed(
            title="New Feedback",
            description=self.feedbackDesc.value,  
            color=discord.Color.blurple()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)

        await channel.send(embed=embed)
        await interaction.response.send_message(f"Thank you, {interaction.user.display_name}!", ephemeral=True)



@client.tree.command(name="feedback",description="Use this command to send feedback to this server's staff!",guild=GUILD_ID)
async def feedback(interaction: discord.Interaction):
    feedback_modal = FeedbackSubmitModal()
    feedback_modal.user = interaction.user
    await interaction.response.send_modal(feedback_modal)

@tasks.loop(hours=2) # i think this is the cooldown since thats the slowmode for the official houses channel in the main TRD server
async def advertisement_post_reminder():
    channel = client.get_channel(1406277791074357329)
    reminderEmbed = discord.Embed(
        title="Remember to advertise the house",
        description="Make sure to send a post in https://discord.com/channels/967560626874503219/1375345100560793730!",
        color=discord.Color.dark_red()
    )
    await channel.send(embed=reminderEmbed)
    await channel.send(f"<@&1406213667560755232>")


@tasks.loop(hours=6)
async def monday_post():
    global last_posted_date
    now = datetime.now(tz=TIMEOZNE)
    if now.weekday() == 0:
        if last_posted_date != now.date():
            channel = client.get_channel(1406277763924627658)
            if channel:
                activitycheck = discord.Embed(
                    title= f"Activity Check for W/C {now.strftime('%m/%d/%y')}",
                    description= "Attention @everyone! Report your activity by reacting below!",
                    color = discord.Color.dark_red()
                
                )
                activitycheck.set_author(
                    name= "Ser Bot of House Bolton",
                    icon_url="https://static.wikia.nocookie.net/gameofthronesfanon/images/f/f3/Roose_Bolton_by_GibiLynx.jpg/revision/latest?cb=20200729022120"
                )
                activitycheck.set_footer(text=f"Property of PlagueNovuh all rights reserved | {now.year()} ")
                
                msg = await channel.send(embed=activitycheck)

                reaction_emoji= "<:emoji_1:1401690667364913243>"
                await msg.add_reaction(reaction_emoji)
                

                last_posted_date = now.date()


@monday_post.before_loop
async def before_monday_post():
    await client.wait_until_ready()


@advertisement_post_reminder.before_loop
async def before_advertisement():
    await client.wait_until_ready()





client.run(api_key)


