import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

registrando_users = set()

@bot.event
async def on_ready():
    print("Bot online!")

@bot.command()
async def registrar(ctx):

    # evita duplicação por usuário
    if ctx.author.id in registrando_users:
        return

    registrando_users.add(ctx.author.id)

    def check(m):
        return (
            m.author == ctx.author and
            m.channel == ctx.channel and
            not m.author.bot
        )

    try:
        # 🔹 Nome
        await ctx.send("Qual seu nome?")
        msg_nome = await bot.wait_for("message", check=check, timeout=30)
        nome = msg_nome.content.strip().replace(" ", "")

        # 🔹 ID do jogo
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
                registrando_users.remove(ctx.author.id)
                return

        # 🔹 Telefone
        await ctx.send("Qual seu número de telefone do jogo?")

        while True:
            msg_tel = await bot.wait_for("message", check=check, timeout=30)
            telefone = msg_tel.content.strip().replace(" ", "")

            if telefone.isdigit():
                break

            await ctx.send("❌ Digite apenas números (sem letras ou símbolos)")

        # 🔹 Quem recrutou
        await ctx.send("Quem recrutou você?")
        msg_recrutou = await bot.wait_for("message", check=check, timeout=30)
        recrutador = msg_recrutou.content.strip()

    except:
        await ctx.send("Tempo esgotado ❌ tenta novamente.")
        registrando_users.remove(ctx.author.id)
        return

    # 🔹 Finalização
    nome_formatado = f"{nome}#{id_user}"

    await ctx.author.edit(nick=nome_formatado)

    cargo = discord.utils.get(ctx.guild.roles, name="Membro")

    if cargo is None:
        cargo = await ctx.guild.create_role(name="Membro")

    await ctx.author.add_roles(cargo)

    await ctx.send(
        f"✅ Registro concluído!\n"
        f"Registrado como {nome_formatado} ✅\n"
        f"Telefone: {telefone}\n"
        f"Recrutado por: {recrutador}"
    )

    registrando_users.remove(ctx.author.id)

bot.run(os.getenv("TOKEN"))