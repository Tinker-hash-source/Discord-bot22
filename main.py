import discord
from discord.ext import commands
from discord.ui import Button, View
import os

# Для Render берем из переменных окружения
TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = int(os.environ.get('APPLICATIONS_CHANNEL_ID', 0))

# Настройка интентов
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # ОБЯЗАТЕЛЬНО!

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} запущен на Render!')
    print(f'📊 Серверов: {len(bot.guilds)}')
    await bot.change_presence(activity=discord.Game(name="/заявка"))

# Класс для кнопок (упрощенный)
class ApplicationView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id
    
    @discord.ui.button(label="✅ Принять", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: Button):
        user = interaction.guild.get_member(self.user_id)
        if user:
            # Даем роль
            role = discord.utils.get(interaction.guild.roles, name="Участник")
            if role:
                await user.add_roles(role)
            
            embed = discord.Embed(
                title="✅ ЗАЯВКА ПРИНЯТА",
                description=f"Пользователь: {user.mention}",
                color=discord.Color.green()
            )
            await interaction.message.edit(embed=embed, view=None)
            await interaction.response.send_message("✅ Принято!", ephemeral=True)
    
    @discord.ui.button(label="❌ Отклонить", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: Button):
        user = interaction.guild.get_member(self.user_id)
        if user:
            embed = discord.Embed(
                title="❌ ЗАЯВКА ОТКЛОНЕНА",
                description=f"Пользователь: {user.name}",
                color=discord.Color.red()
            )
            await interaction.message.edit(embed=embed, view=None)
            await interaction.response.send_message("❌ Отклонено!", ephemeral=True)

# Команда /заявка
@bot.tree.command(name="заявка", description="Подать заявку")
async def application(interaction: discord.Interaction):
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        embed = discord.Embed(
            title="📝 НОВАЯ ЗАЯВКА",
            description=f"**Пользователь:** {interaction.user.mention}",
            color=discord.Color.blue()
        )
        
        view = ApplicationView(interaction.user.id)
        await channel.send(embed=embed, view=view)
        
        await interaction.response.send_message(
            "✅ Заявка отправлена!",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ Канал не найден",
            ephemeral=True
        )

# Тестовая команда
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Понг! {round(bot.latency * 1000)}мс")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Токен не найден!")