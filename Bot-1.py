import discord
import aiohttp

# Définir le token Discord et la clé API Fortnite directement dans le fichier
DISCORD_TOKEN = "MTM2ODk1NjY1OTAxOTI4ODYzOA.GZ-WJb.oUzyva-LZtNseQsZ5FitgemtOTlo2yvkG9p_NI"  # Remplace par ton vrai token Discord
API_KEY = "dbfd6501-50e2-4ffd-9709-ce06cb391a62"  # Remplace par ta vraie clé API Fortnite

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "!ping":
        await message.channel.send("Pong !")

    if message.content.startswith("!stats"):
        parts = message.content.split()
        if len(parts) != 2:
            await message.channel.send("Utilisation : `!stats pseudo`")
            return

        pseudo = parts[1]
        await message.channel.send(f"Recherche des stats de **{pseudo}**...")

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": API_KEY}  # Utilisation de la clé API Fortnite
            async with session.get(f"https://fortnite-api.com/v2/stats/br/v2?name={pseudo}", headers=headers) as resp:
                if resp.status != 200:
                    await message.channel.send("Joueur non trouvé ou erreur avec l’API.")
                    return
                data = await resp.json()
                stats = data["data"]["stats"]["all"]["overall"]
                await message.channel.send(
                    f"**Stats de {pseudo}** :\n"
                    f"- Victoires : {stats['wins']}\n"
                    f"- Kills : {stats['kills']}\n"
                    f"- K/D : {stats['kd']}\n"
                    f"- Matchs : {stats['matches']}"
                )

    if message.content.startswith("!battlepass"):
        parts = message.content.split()
        if len(parts) != 2:
            await message.channel.send("Utilisation : `!battlepass pseudo`")
            return

        pseudo = parts[1]
        await message.channel.send(f"Recherche du Battlepass de **{pseudo}**...")

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": API_KEY}  # Utilisation de la clé API Fortnite
            async with session.get(f"https://fortnite-api.com/v2/battlepass/v2?name={pseudo}", headers=headers) as resp:
                if resp.status != 200:
                    await message.channel.send("Erreur avec l'API ou joueur introuvable.")
                    return
                data = await resp.json()
                battlepass = data["data"]
                await message.channel.send(
                    f"**Battlepass de {pseudo}** :\n"
                    f"- Niveau actuel : {battlepass['level']}\n"
                    f"- Points de Battlepass : {battlepass['xp']}\n"
                    f"- Récompenses débloquées : {battlepass['rewards']}"
                )

    if message.content.startswith("!shop"):
        await message.channel.send("Récupération de la boutique Fortnite...")

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": API_KEY}  # Utilisation de la clé API Fortnite
            async with session.get("https://fortnite-api.com/v2/shop/br", headers=headers) as resp:
                if resp.status != 200:
                    await message.channel.send("Erreur avec l'API de la boutique.")
                    return
                data = await resp.json()
                shop_items = data["data"]["featured"]
                await message.channel.send("**Boutique Fortnite :**")
                for item in shop_items:
                    item_name = item["name"]
                    item_price = item["price"]
                    await message.channel.send(f"- {item_name} : {item_price} V-Bucks")

    if message.content.startswith("!annonce"):
        if message.author.guild_permissions.administrator:
            annonce = message.content[len("!annonce "):]
            await message.channel.send(f"**Annonce :** {annonce}")
        else:
            await message.channel.send("Tu n'as pas la permission d'envoyer des annonces.")

    if "fortnite" in message.content.lower():
        await message.channel.send("Fortnite c’est la vie ! ")

client.run(DISCORD_TOKEN)

