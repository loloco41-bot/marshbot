import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot online!")

@bot.command()
async def registrar(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Qual seu nome?")

    try:
        msg_nome = await bot.wait_for("message", check=check, timeout=30)
        nome = msg_nome.content.strip().replace(" ", "")

        await ctx.send("Qual seu ID no jogo?")

        tentativas = 0

        while True:
            msg_id = await bot.wait_for("message", check=check, timeout=30)
            id_user = msg_id.content.strip().replace(" ", "")

            if id_user.isdigit():
                break

            tentativas += 1
            await ctx.send("Coloque seu ID correto ❌")

            if tentativas >= 3:
                await ctx.send("Muitas tentativas. Cancelado ❌")
                return

    except:
        await ctx.send("Tempo esgotado ❌ tenta novamente.")
        return

    nome_formatado = f"{nome}#{id_user}"

    await ctx.author.edit(nick=nome_formatado)

    cargo = discord.utils.get(ctx.guild.roles, name="Membro")

    if cargo is None:
        cargo = await ctx.guild.create_role(name="Membro")

    await ctx.author.add_roles(cargo)

    await ctx.send(f"Registrado como {nome_formatado} ✅")

import os
bot.run(os.getenv("TOKEN"))