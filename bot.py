import discord
from discord.ext import commands

TOKEN = ""
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

PACKAGES = {
    "vip": {"name": "VIP Rank", "price": 499, "emoji": "👑", "desc": "VIP perks", "features": ["VIP Prefix", "5 Homes", "/fly", "VIP Kit"]},
    "celestial": {"name": "Celestial Rank", "price": 1499, "emoji": "🌙", "desc": "+850 Coins + Perks", "features": ["Celestial Prefix", "6 Homes", "/sit /nick /hat", "+850 Coins"]},
    "coins_1000": {"name": "1000 Coins", "price": 299, "emoji": "💰", "desc": "In-game coins", "features": ["1000 Coins", "Instant Delivery"]}
}

PAYMENTS = "💚 JazzCash: 0300-1234567\n💙 EasyPaisa: 0345-1234567"

@bot.event
async def on_ready():
    print(f'✅ {bot.user} Online!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ATRONICEMC Store"))

@bot.command(name='store')
async def store(ctx):
    embed = discord.Embed(title="🏪 ATRONICEMC STORE", description="`!buy <package>` to purchase", color=0xd32f2f)
    for k, p in PACKAGES.items():
        fts = "\n".join([f"✅ {f}" for f in p['features']])
        embed.add_field(name=f"{p['emoji']} {p['name']} - ₹{p['price']}", value=f"{p['desc']}\n{fts}\n`!buy {k}`", inline=False)
    embed.set_footer(text="ATRONICEMC")
    await ctx.send(embed=embed)

@bot.command(name='buy')
async def buy(ctx, package=None):
    if package is None or package.lower() not in PACKAGES:
        await ctx.send("❌ Use `!store` for packages\nExample: `!buy vip`"); return
    p = PACKAGES[package.lower()]
    em = discord.Embed(title=f"🛒 {p['name']}", description="React ✅ to confirm | ❌ to cancel", color=0x4caf50)
    em.add_field(name="Price", value=f"₹{p['price']}", inline=True)
    em.add_field(name="Features", value="\n".join([f"✅ {f}" for f in p['features']]), inline=False)
    msg = await ctx.send(embed=em)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')
    def check(r, u): return u == ctx.author and str(r.emoji) in ['✅','❌']
    try:
        r, u = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        if str(r.emoji) == '✅':
            dm = discord.Embed(title="💳 PAYMENT", description=f"**{p['name']}**\n**Amount: ₹{p['price']}**\n\n{PAYMENTS}", color=0xd32f2f)
            dm.add_field(name="📝 Steps", value="1. Send payment\n2. Send screenshot here\n3. Wait for delivery")
            try: await ctx.author.send(embed=dm); await ctx.send("✅ Check DM!", delete_after=10)
            except: await ctx.send(f"❌ Enable DM!\n{PAYMENTS}\nAmount: ₹{p['price']}", delete_after=30)
        else: await ctx.send("❌ Cancelled!", delete_after=10)
    except: await ctx.send("⏰ Timeout!", delete_after=10)

@bot.command(name='pay')
async def pay(ctx):
    await ctx.send(f"**💳 Payment Methods**\n{PAYMENTS}")

@bot.command(name='helpme')
async def h(ctx):
    await ctx.send("**!store** - Packages\n**!buy vip/celestial/coins_1000** - Buy\n**!pay** - Payment info")

bot.run(TOKEN)
