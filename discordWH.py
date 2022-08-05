from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv() #Check Environment Variables in .env file
webhook_url= os.getenv('WEBHOOK')

webhook = DiscordWebhook(url=webhook_url) #Discord WebHook URL

def sendMessage(tokens, available, vaults):
    embed=DiscordEmbed(title=f"Space available for the {vaults[tokens]['title']} !", url=vaults[tokens]['website'], color=vaults[tokens]['color'])
    embed.set_thumbnail(url=vaults[tokens]['logo'])
    embed.add_embed_field(name=f":farmer: The {vaults[tokens]['title']} vault has some space available :farmer:", value=f"There is {available/10**vaults[tokens]['decimals']:,.2f} {tokens} available to be deposited in the {vaults[tokens]['title']}!", inline=False)
    embed.set_footer(text=f"-- Powered by hal.xyz")
    webhook.add_embed(embed)
    response = webhook.execute(remove_embeds=True)
    print("discord sent!")
    sleep(5)
