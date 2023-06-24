import discord,json,os,random
from discord.ext import commands

with open("config.json") as file:
    info = json.load(file)
    token = info["token"]
    prefix = info["prefix"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("\n\n\n")
    print("Bot Running !")
    print("--------------")

##COMMANDE POUR AFFICHER LES STOCKS RESTANT
@bot.command()
async def stock(ctx):
    stockmenu = discord.Embed(title="Compte en stock",description="", color = discord.Color.blue())
    stockmenu.set_image(url="https://media.discordapp.net/attachments/999694798896246785/1034779111001968701/20221022_231401.gif")
    for filename in os.listdir("Accounts"):
        with open("Accounts/"+filename) as f:
            ammount = len(f.read().splitlines())
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt","")
            stockmenu.description += f"**{name}** : `{ammount}`\n"
    await ctx.reply(embed=stockmenu)

##COMMANDE POUR AJOUTER DU STOCK
## -addstock service
## compte1
## compte2

@bot.command()
async def addstock(ctx, name, *, account):
    fourni = discord.utils.get(ctx.guild.roles, name="Fournisseur")##Avoir le rôle Fournisseur pour pouvoir faire la commande
    if fourni in ctx.author.roles:
        name = name.lower()+".txt"
        if name not in os.listdir("Accounts"):
            em_compte = discord.Embed(title="Ce type de service n'existe pas", color = discord.Color.blue())
            em_compte.add_field(name="Pour voir les service disponible : ", value = f"<#1087135567248101397>") ##Pour la value changer les chiffres de <#1087135567248101397> et y mettre l'id du salon affichant les service dispo
            em_compte.set_image(url="https://cdn.discordapp.com/attachments/1088552391118426132/1097986781116370955/MOSHED-2020-2-20-22-48-16.gif") ##image embed
            await ctx.reply(embed=em_compte)
        else:
            i = 0
            message_content = ctx.message.content.split('\n', 1)[1]
            num_lines = len(message_content.split('\n'))
            with open("Accounts/"+name, "a") as file:
                file.write(f"{account}\n")
                i = i + 1
            name2 = name.replace(".txt", "")
            em_restock = discord.Embed(title = f"Restock de {name2} pour les VIP", color = discord.Color.blue())
            em_restock.add_field(name = f"{num_lines} comptes {name2} restock par {ctx.author}", value = "`=stock` pour plus d'info")
            em_restock.set_image(url="https://media.discordapp.net/attachments/999694798896246785/1034779111001968701/20221022_231401.gif")##image embed
            channel=bot.get_channel(1087135852796334101) ## changer par l'id du salon où envoyer les restock
            await channel.send("<@&1090720995238756474>") ## changer les chiffres par l'id du rôle à ping quand y a un restock
            await channel.send(embed=em_restock)
            await ctx.send("Compte ajouté dans le stock")
    else:
        await ctx.send("Vous n'êtes pas fournisseur")


@bot.command()
async def gen(ctx, name=None):
        if ctx.channel.id == 1092874946209923294: ## après == mettre l'id du salon où dois être utilisé le gen
                    if name == None:
                        e_compte = discord.Embed(title="Spécifiez le type de compte !", color = discord.Color.blue())
                        e_compte.add_field(name="Pour voir les service disponible : ", value = f"`{prefix}stock`")
                        e_compte.set_image(url="https://cdn.discordapp.com/attachments/1088552391118426132/1097986781116370955/MOSHED-2020-2-20-22-48-16.gif")##image embed
                        await ctx.reply(embed=e_compte)
                    else:
                        name = name.lower()+".txt"
                        if name not in os.listdir("Accounts"):
                            em_compte = discord.Embed(title="Ce type de service n'existe pas", color = discord.Color.blue())
                            em_compte.add_field(name="Pour voir les service disponible : ", value = f"<#1087135567248101397>")
                            em_compte.set_image(url="https://cdn.discordapp.com/attachments/1088552391118426132/1097986781116370955/MOSHED-2020-2-20-22-48-16.gif")##image embed
                            await ctx.reply(embed=em_compte)
                        else:
                            with open("Accounts/"+name) as file:
                                lines = file.read().splitlines()
                            if len(lines) == 0:
                                em_stock = discord.Embed(title = "Aucun stock disponible pour ce service", color = discord.Color.blue())
                                em_stock.add_field(name = "Merci d'attendre le restock", value = "_ _")
                                em_stock.set_image(url="https://cdn.discordapp.com/attachments/1088552391118426132/1097986781116370955/MOSHED-2020-2-20-22-48-16.gif")##image embed
                                await ctx.reply(embed=em_stock)
                            if len(lines) > 0:
                                with open("Accounts/"+name) as file:
                                    account = random.choice(lines)
                                try:
                                    name2 = name.replace(".txt", "")
                                    em_mp = discord.Embed(title="Compte généré", color = discord.Color.blue())
                                    em_mp.add_field(name="Service : ", value = f"`{name2}`", inline = False)
                                    em_mp.add_field(name=" compte : ", value = f"`{str(account)}`")
                                    em_mp.set_image(url="https://media.discordapp.net/attachments/999694798896246785/1034779111001968701/20221022_231401.gif")##image embed
                                    await ctx.author.send(embed=em_mp)
                                    await ctx.author.send("**Donnez votre avis sur le serveur dans** <#1087135482028236931>") ## changer les chiffres dans <#64654646> pour mettre le salon où laisser un avis
                                    await ctx.author.send(":warning: *LES CODES SONT ALÉATOIRE ET NE FONCTIONNE PAS OBLIGATOIREMENT* :warning:")
                                    await ctx.author.send(f"{str(account)}")
                                except:
                                    em_error = discord.Embed(title = "Echec de l'envoie en dm !", color = discord.Color.blue())
                                    em_error.add_field(name = "Veuillez dévérouiller vos dms", value = "_ _")
                                    em_error.set_image(url = "https://cdn.discordapp.com/attachments/1088552391118426132/1097986781116370955/MOSHED-2020-2-20-22-48-16.gif")##image embed
                                    await ctx.reply(embed=em_error)
                                else:
                                    em_reply = discord.Embed(title="**Compte généré avec succès !**", color = discord.Color.blue())
                                    em_reply.add_field(name=" *Regarde tes mp !*", value = "_ _")
                                    em_reply.set_image(url="https://media.discordapp.net/attachments/999694798896246785/1034779111001968701/20221022_231401.gif")##image embed
                                    em_reply.set_footer(text=f"{ctx.author} | {ctx.author.id}")
                                    await ctx.reply(embed=em_reply)
                                    with open("Accounts/"+name,"w") as file:
                                        file.write("")
                                    with open("Accounts/"+name,"a") as file:
                                        for line in lines:
                                            if line != account:
                                                file.write(line+"\n")
        else:
            em = discord.Embed(title="Erreur de la commande", color = discord.Color.blue())
            em.add_field(name = "Veuillez utiliser la commande dans le salon suivant :", value = "<#1092874946209923294>", inline = False)
            em.add_field(name = "Et vérifier le nom de service avec la commande :", value = f"`{prefix}stock`")
            em.set_image(url="https://cdn.discordapp.com/attachments/1088552391118426132/1097986781116370955/MOSHED-2020-2-20-22-48-16.gif")##image embed
            await ctx.reply(embed=em)

bot.run(token)