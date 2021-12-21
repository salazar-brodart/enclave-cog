import asyncio
import random
import time
import discord
from math import ceil
from discord.utils import get
from redbot.core import commands, bank, Config
from redbot.core.bot import Red
from redbot.core.commands import Context
from redbot.core.utils.mod import get_audit_reason
from redbot.core.utils.menus import close_menu, menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.chat_formatting import box, humanize_number, escape, italics
from .userprofile import UserProfile
from .enlevel import enlevel
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption

class enclave(commands.Cog):
    global answer
    answer = lambda s: s
    ANS = [
        ("Боги говорят - да, а Древние Боги говорят - ск'яхф ки'плаф ф'магг."),
        ("Это твёрдо, как мой панцирь!"),
        ("Это решительно так, мой друг и/или подруга!"),
        ("Скорее всего да, но также вполне вероятно, что нет..."),
        ("Хорошие перспективы для хорошего дела."),
        ("Знаки на воде указывают - да. Доверься им."),
        ("Я не имею никаких сомнений на этот счёт."),
        ("Да, господин и/или госпожа."),
        ("Опираясь на свой тысячелетний опыт, скажу - определённо да."),
        ("Цикл жизни бывает жесток. Вы можете положиться на него."),
        ("Хмельной туман застилает мой взор, давай попозже."),
        ("Что ты там мямлишь? Ну-ка повтори погромче!"),
        ("Настанет Время, когда ты узнаешь ответ на этот вопрос. *Злобно хохочет.*"),
        ("Нельзя сотворить здесь!"),
        ("Лучше спроси об этом Вессину."),
        ("Пополни ману и спроси ещё раз."),
        ("Даже не рассчитывай на это безобразие."),
        ("Мой ответ - нет. Но кто будет слушать старую тортолланку?!"),
        ("Боги отвечают - нет. А Древние боги отвечают - убей их всех."),
        ("Перспектива не так хороша, как мне хотелось бы."),
        ("Весьма сомнительно, учитывая твою репутацию, господин и/или госпожа."),
    ]
    MAT = [
        ("побитый"),
        ("плетёный"),
        ("прочный железный"),
        ("усиленный"),
        ("окованный мифрилом"),
        ("окованный железом"),
        ("ветхий"),
        ("тяжёлый"),
        ("изысканный бронзовый"),
        ("укреплённый стальной"),
        ("кориевый"),
        ("этерниевый"),
        ("окованный адамантитом"),
        ("титановый"),
        ("украшенный изумрудами"),
        ("серебряный"),
        ("вневременный"),
        ("заросший ракушками"),
    ]
    
    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.profiles = UserProfile()
        self.data = Config.get_conf(self, identifier=1099710897114110101)
        DiscordComponents(self.bot)

    @commands.group(name="выбрать", autohelp=False)
    async def выбрать(self, ctx: commands.GuildContext):
        pass
        
    @выбрать.command(name="класс")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def выбрать_класс(self, ctx: Context):
        author = ctx.author
        C1=discord.utils.get(ctx.guild.roles, id=685724787397361695)#war
        C2=discord.utils.get(ctx.guild.roles, id=685724790425649157)#hunt
        C3=discord.utils.get(ctx.guild.roles, id=685724791914758147)#rog
        C4=discord.utils.get(ctx.guild.roles, id=685724793567444995)#pal
        C5=discord.utils.get(ctx.guild.roles, id=685724794586398761)#dru
        C6=discord.utils.get(ctx.guild.roles, id=685724796075769889)#sham
        C7=discord.utils.get(ctx.guild.roles, id=685724798193762365)#mage
        C8=discord.utils.get(ctx.guild.roles, id=685724797266952219)#priest
        C9=discord.utils.get(ctx.guild.roles, id=685724799527551042)#lock
        C10=discord.utils.get(ctx.guild.roles, id=685724801486290947)#dk
        C11=discord.utils.get(ctx.guild.roles, id=685724800169410631)#monk
        C12=discord.utils.get(ctx.guild.roles, id=685724803105161216)#dh
        for r in C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12:
            if r in author.roles:
                return await ctx.send(f"У тебя уже есть класс - {r.name}.")
        war=self.bot.get_emoji(889833858160271370)
        hun=self.bot.get_emoji(889833963592503358)
        rog=self.bot.get_emoji(889833821942460426)
        pal=self.bot.get_emoji(889833946043514880)
        dru=self.bot.get_emoji(889833977177845790)
        sha=self.bot.get_emoji(889833872785805323)
        mag=self.bot.get_emoji(889833910631014430)
        pri=self.bot.get_emoji(889833892759089173)
        loc=self.bot.get_emoji(889833865638723615)
        dk=self.bot.get_emoji(921280885926531083)
        mon=self.bot.get_emoji(921280924782571550)
        dh=self.bot.get_emoji(921280848689528852)
        embed = discord.Embed(title=f'*{author.display_name} посещает классового тренера.*', description = "Выбери наиболее подходящий тебе класс, и приступим к обучению!\n*Разворачивает свиток.*", colour=discord.Colour.purple())
        embed.set_thumbnail(url=author.avatar_url)
        msg = await ctx.send(embed=embed, components=[Select(placeholder="Сделать выбор:", options=[SelectOption(label="Воин", value="Воин", emoji=war), SelectOption(label="Охотник", value="Охотник", emoji=hun), SelectOption(label="Разбойник", value="Разбойник", emoji=rog), SelectOption(label="Паладин", value="Паладин", emoji=pal), SelectOption(label="Друид", value="Друид", emoji=dru), SelectOption(label="Шаман", value="Шаман", emoji=sha), SelectOption(label="Маг", value="Маг", emoji=mag), SelectOption(label="Жрец", value="Жрец", emoji=pri), SelectOption(label="Чернокнижник", value="Чернокнижник", emoji=loc), SelectOption(label="Рыцарь смерти", value="Рыцарь смерти", emoji=dk), SelectOption(label="Монах", value="Монах", emoji=mon), SelectOption(label="Охотник на демонов", value="Охотник на демонов", emoji=dh)])])
        emb0 = discord.Embed(title = '*Тренер ушёл на обед.*')
        emb0.set_thumbnail(url="https://cdn.discordapp.com/emojis/620315257285509130.png")
        emb1 = discord.Embed(title='Класс: Воин.', description = "Обладает самыми мощными ударами, может входить в исступление и спровоцировать противника, ослабив его защиту.", color=0xc79c6e)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833858160271370.png")
        emb2 = discord.Embed(title='Класс: Охотник.', description = "Лучший в нанесении урона и выведении противника из строя, его питомец универсален для многих задач.", color=0xabd473)
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833963592503358.png")
        emb3 = discord.Embed(title='Класс: Разбойник.', description = "Виртуозно работает с монетами, своими и чужими, легко устраняет противников.", color=0xfff569)
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833821942460426.png")
        emb4 = discord.Embed(title='Класс: Паладин.', description = "Способен повышать свою эффективность силой Света. Обладает мощнейшими исцеляющими и очищающими заклинаниями.", color=0xf58cba)
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833946043514880.png")
        emb5 = discord.Embed(title='Класс: Друид.', description = "Универсальный класс с разнообразными возможностями. Может погружаться в Изумрудный сон.", color=0xff7d0a)
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833977177845790.png")
        emb6 = discord.Embed(title='Класс: Шаман.', description = "Класс с лучшими благотворными заклинаниями и опасными заклинаниями сглаза.", color=0x0070de)
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833872785805323.png")
        emb7 = discord.Embed(title='Класс: Маг.', description = "Мастерски владеет магией арканы, льда и пламени. Уверенно поддерживает, контролирует и сжигает оппонентов.", color=0x69ccf0)
        emb7.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833910631014430.png")
        emb8 = discord.Embed(title='Класс: Жрец.', description = "Класс, посвящающий себя служению высшим силам. Может обращаться как к Свету, так и к Тьме.", color=0xffffff)
        emb8.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833892759089173.png")
        emb9 = discord.Embed(title='Класс: Чернокнижник.', description = "Сильнейший класс в вызове катастроф локального и всеобщего масштаба, хочет он того или нет.", color=0x9482c9)
        emb9.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833865638723615.png")
        emb10 = discord.Embed(title='Класс: Рыцарь смерти.', description = "Сильный и опасный класс, может призывать силы Разложения на своих врагов и друзей.", color=0xc41f3b)
        emb10.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280885926531083.png")
        emb11 = discord.Embed(title='Класс: Монах.', description = "Класс, в совершенстве овладевший балансом между телом и духом. Способен за себя постоять и взбодрить друзей.", color=0x00ffba)
        emb11.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280924782571550.png")
        emb12 = discord.Embed(title='Класс: Охотник на демонов.', description = "Агрессивный класс, способный утопить противника в потоке своего гнева. Его врагам никто не завидует.", color=0xa330c9)
        emb12.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280848689528852.png")
        while True:
            try:
                interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await interaction.edit_origin()
            if interaction.values[0] == 'Воин':
                await msg.edit(embed=emb1, components = [[Button(style = ButtonStyle.green, label = 'Стать воином!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Охотник':
                await msg.edit(embed=emb2, components = [[Button(style = ButtonStyle.green, label = 'Стать охотником!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Разбойник':
                await msg.edit(embed=emb3, components = [[Button(style = ButtonStyle.green, label = 'Стать разбойником!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Паладин':
                await msg.edit(embed=emb4, components = [[Button(style = ButtonStyle.green, label = 'Стать паладином!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Друид':
                await msg.edit(embed=emb5, components = [[Button(style = ButtonStyle.green, label = 'Стать друидом!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Шаман':
                await msg.edit(embed=emb6, components = [[Button(style = ButtonStyle.green, label = 'Стать шаманом!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Маг':
                await msg.edit(embed=emb7, components = [[Button(style = ButtonStyle.green, label = 'Стать магом!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Жрец':
                await msg.edit(embed=emb8, components = [[Button(style = ButtonStyle.green, label = 'Стать жрецом!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Чернокнижник':
                await msg.edit(embed=emb9, components = [[Button(style = ButtonStyle.green, label = 'Стать чернокнижником!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Рыцарь смерти':
                await msg.edit(embed=emb10, components = [[Button(style = ButtonStyle.green, label = 'Стать рыцарем смерти!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Монах':
                await msg.edit(embed=emb11, components = [[Button(style = ButtonStyle.green, label = 'Стать монахом!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            elif interaction.values[0] == 'Охотник на демонов':
                await msg.edit(embed=emb12, components = [[Button(style = ButtonStyle.green, label = 'Стать охотником на демонов!'), Button(style = ButtonStyle.red, label = 'Вернуться к списку.')]])
            else:
                return
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            if responce.component.label == 'Стать воином!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} принимает решение совершенствоваться в воинском искусстве.*', color=0xc79c6e)
                emb.set_image(url="http://i.imgur.com/lFMFiku.png")
                await author.add_roles(C1)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать охотником!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} выходит на охоту.*', color=0xabd473)
                emb.set_image(url="http://i.imgur.com/sXQsrQZ.png")
                await author.add_roles(C2)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать разбойником!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} берёт кинжал и выходит на большую дорогу.*', color=0xfff569)
                emb.set_image(url="http://i.imgur.com/djdxDht.png")
                await author.add_roles(C3)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать паладином!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} становится поборником Света.*', color=0xf58cba)
                emb.set_image(url="http://i.imgur.com/ckgqohP.png")
                await author.add_roles(C4)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать друидом!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} встаёт на стражу природы.*', color=0xff7d0a)
                emb.set_image(url="http://i.imgur.com/l9O6VDX.png")
                await author.add_roles(C5)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать шаманом!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} наполняется силой стихий и мудростью предков.*', color=0x0070de)
                emb.set_image(url="http://i.imgur.com/rRwA2Sn.png")
                await author.add_roles(C6)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать магом!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} получает диплом мага.*', color=0x69ccf0)
                emb.set_image(url="http://i.imgur.com/73HwEut.png")
                await author.add_roles(C7)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать жрецом!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} доказывает свою крепость веры и посвящает себя духовной жизни.*', color=0xffffff)
                emb.set_image(url="http://i.imgur.com/6qo1Xbt.png")
                await author.add_roles(C8)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать чернокнижником!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} готовится отдать всё, ради силы.*', color=0x9482c9)
                emb.set_image(url="http://i.imgur.com/rFUdNuY.png")
                await author.add_roles(C9)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать рыцарем смерти!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} возвращается к жизни, чтобы упиваться страданиями.*', color=0xc41f3b)
                emb.set_image(url="http://i.imgur.com/ca1TYsQ.png")
                await author.add_roles(C10)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать монахом!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} разминает кулаки и готовится к медитации.*', color=0x00ffba)
                emb.set_image(url="http://i.imgur.com/SQACbXd.png")
                await author.add_roles(C11)
                return await msg.edit(embed=emb, components=[])
            elif responce.component.label == 'Стать охотником на демонов!':
                await responce.edit_origin()
                emb = discord.Embed(title=f'*{author.display_name} жервует всем, чтобы спасти Азерот.*', color=0xa330c9)
                emb.set_image(url="http://i.imgur.com/608iTQz.png")
                await author.add_roles(C12)
                return await msg.edit(embed=emb, components=[])
            else:
                await responce.edit_origin()
                await msg.edit(embed=embed, components=[Select(placeholder="Выбрать здесь:", options=[SelectOption(label="Воин", value="Воин", emoji=war), SelectOption(label="Охотник", value="Охотник", emoji=hun), SelectOption(label="Разбойник", value="Разбойник", emoji=rog), SelectOption(label="Паладин", value="Паладин", emoji=pal), SelectOption(label="Друид", value="Друид", emoji=dru), SelectOption(label="Шаман", value="Шаман", emoji=sha), SelectOption(label="Маг", value="Маг", emoji=mag), SelectOption(label="Жрец", value="Жрец", emoji=pri), SelectOption(label="Чернокнижник", value="Чернокнижник", emoji=loc), SelectOption(label="Рыцарь смерти", value="Рыцарь смерти", emoji=dk), SelectOption(label="Монах", value="Монах", emoji=mon), SelectOption(label="Охотник на демонов", value="Охотник на демонов", emoji=dh)])])

    @commands.command()
    @commands.cooldown(1, 240, commands.BucketType.user)
    async def сундук(self, ctx: Context):
        author = ctx.author
        CH=discord.utils.get(ctx.guild.roles, id=696014224442392717)
        if CH not in author.roles:
            return await ctx.send(f'*{author.display_name} жадно смотрит на склад сундуков.*')
        MAT = random.choice(self.MAT)
        embed = discord.Embed(title = f'*{author.display_name} берёт в руки {MAT} сундучок.*', colour=discord.Colour.gold())
        embed.set_thumbnail(url="https://wow.zamimg.com/uploads/screenshots/small/51397.jpg")
        embj = discord.Embed(title = '*К вам подходит старая тортолланка.*', description = 'Ого, какая древность! Я была бы очень рада поместить эту вещь в свою коллекцию! Если отдашь это мне, то я обучу тебя, как использовать силу таких артефактов. А знание, как говорится, сила!', colour=discord.Colour.blue())
        embj.set_thumbnail(url="https://cdn.discordapp.com/attachments/709367217229398016/888039785443246130/c8dbfd31a91404f4.png")
        embv = discord.Embed(title = '*Рядом неслышно появляется фигура в капюшоне.*', description = 'Эй! Эта вещь крайне опас-с-сна и должна покинуть это мес-с-сто. Я куплю её у тебя, и ты больше никогда о ней не ус-с-слышишь. Этого мешка с-с-с золотом думаю хватит.', colour=discord.Colour.green())
        embv.set_thumbnail(url="https://cdn.discordapp.com/attachments/709367217229398016/888040714448011304/D6JDdHhU0AAndrh.png")
        embvs = discord.Embed(title = '*Рядом неслышно появляется фигура в капюшоне.*', description = 'Не верь с-с-старой черепахе! Эта вещь крайне опас-с-сна и должна покинуть это мес-с-сто. Я куплю её у тебя, и ты больше никогда о ней не ус-с-слышишь. Этого мешка с-с-с золотом думаю хватит.', colour=discord.Colour.green())
        embvs.set_thumbnail(url="https://cdn.discordapp.com/attachments/709367217229398016/888040714448011304/D6JDdHhU0AAndrh.png")
        embo = discord.Embed(title = '*Крышка сундука резко захлопнулась.*')
        msg = await ctx.send(embed=embed, components = [[Button(style = ButtonStyle.green, label = 'Открыть сундук!'), Button(style = ButtonStyle.red, emoji = '❌')]])
        try:
            responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=55)
        except asyncio.TimeoutError:
            return await msg.edit(embed=embed, components = [])
        if responce.component.label == 'Открыть сундук!':
            await responce.edit_origin()
            emb = discord.Embed(title = f'*{author.display_name} открывает сундук.*', description = '*Внутри обнаруживается загадочный артефакт. Яркое сияние привлекло внимание обитателей храма.*', colour=discord.Colour.dark_gold())
            emb.set_image(url="https://cdn.discordapp.com/attachments/709367217229398016/887978198258819112/7d4fb496d44a4c5b.png")
            await msg.edit(embed=emb, components = [[Button(style = ButtonStyle.blue, label = 'Выслушать Джолу.'), Button(style = ButtonStyle.green, label = 'Выслушать Вессину.')]])
        else:
            await responce.edit_origin()
            await msg.delete()
            return
        try:
            responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=55)
        except asyncio.TimeoutError:
            return await msg.edit(embed=embo, components = [])
        if responce.component.label == 'Выслушать Джолу.':
            await responce.edit_origin()
            await msg.edit(embed=embj, components = [[Button(style = ButtonStyle.grey, label = 'Отдать артефакт Джоле.'), Button(style = ButtonStyle.green, label = 'Выслушать Вессину.')]])
        else:
            await responce.edit_origin()
            await msg.edit(embed=embv, components = [[Button(style = ButtonStyle.grey, label = 'Продать артефакт Вессине.'), Button(style = ButtonStyle.blue, label = 'Выслушать Джолу.')]])
        try:
            responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=55)
        except asyncio.TimeoutError:
            return await msg.edit(embed=embo, components = [])
        if responce.component.label == 'Выслушать Джолу.':
            await responce.edit_origin()
            await msg.edit(embed=embj, components = [[Button(style = ButtonStyle.grey, label = 'Отдать артефакт Джоле.'), Button(style = ButtonStyle.grey, label = 'Продать артефакт Вессине.')]])
        elif responce.component.label == 'Выслушать Вессину.':
            await responce.edit_origin()
            await msg.edit(embed=embvs, components = [[Button(style = ButtonStyle.grey, label = 'Отдать артефакт Джоле.'), Button(style = ButtonStyle.grey, label = 'Продать артефакт Вессине.')]])
        elif responce.component.label == 'Отдать артефакт Джоле.':
            await responce.edit_origin()
            emb = discord.Embed(title = f'*{author.display_name} отдаёт артефакт Джоле Древней.*', colour=discord.Colour.blue())
            emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/625192051042156565.png")
            await msg.edit(embed=emb, components = [])
            await self.getrank(ctx=ctx, user=author)
            await self.getart(ctx=ctx, art=0)
            return await author.remove_roles(CH)
        elif responce.component.label == 'Продать артефакт Вессине.':
            await responce.edit_origin()
            emb = discord.Embed(title = f'*{author.display_name} передаёт артефакт Вессине за увесистый мешок золотых монет.*', colour=discord.Colour.green())
            emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/624216995784687657.png")
            await msg.edit(embed=emb, components = [])
            authbal=await bank.get_balance(author)
            max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
            heal=random.randint(600, 700)
            if authbal>(max_bal-heal):
                heal=(max_bal-authbal)
            await bank.deposit_credits(author, heal)
            await self.getart(ctx=ctx, art=1)
            await ctx.send (f"*{author.display_name} получает {heal} золотых монет.*")
            return await author.remove_roles(CH)
        try:
            responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=55)
        except asyncio.TimeoutError:
            return await msg.edit(embed=embo, components = [])
        if responce.component.label == 'Отдать артефакт Джоле.':
            await responce.edit_origin()
            emb = discord.Embed(title = f'*{author.display_name} отдаёт артефакт Джоле Древней.*', colour=discord.Colour.blue())
            emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/625192051042156565.png")
            await msg.edit(embed=emb, components = [])
            await self.getrank(ctx=ctx, user=author)
            await self.getart(ctx=ctx, art=0)
            return await author.remove_roles(CH)
        elif responce.component.label == 'Продать артефакт Вессине.':
            await responce.edit_origin()
            emb = discord.Embed(title = f'*{author.display_name} передаёт артефакт Вессине за увесистый мешок золотых монет.*', colour=discord.Colour.green())
            emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/624216995784687657.png")
            await msg.edit(embed=emb, components = [])
            authbal=await bank.get_balance(author)
            max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
            heal=random.randint(600, 700)
            if authbal>(max_bal-heal):
                heal=(max_bal-authbal)
            await bank.deposit_credits(author, heal)
            await self.getart(ctx=ctx, art=1)
            await ctx.send (f"*{author.display_name} получает {heal} золотых монет.*")
            return await author.remove_roles(CH)

    @commands.group(name="книга", autohelp=False)
    async def книга(self, ctx: commands.GuildContext):
        """
        Исчерпывающая информация о заклинаниях разных школ.
        """
        pass

    @книга.command(name="воина")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_воина(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Воинское искусство\".', color=0xc79c6e)
        emb1.add_field(name="Заклинание: Боевой крик", value="Ранг: Не требуется.\nЦена: 40\nДействие: Даёт ~20 монет.", inline=True)
        emb1.add_field(name="Заклинание: Сокрушение", value="Ранг: Не требуется.\nЦена: 180\nДействие: Отнимает ~250 монет.", inline=True)
        emb1.add_field(name="Заклинание: Глухая оборона", value="Ранг: Подмастерье.\nЦена: 200\nДействие: Даёт защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Провокация (Исступление)", value="Ранг: Искусник.\nЦена: 170\nДействие: Снимает защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Ободряющий клич", value="Ранг: Мастер.\nЦена: 150\nДействие: Даёт 15 опыта.", inline=True)
        emb1.add_field(name="Заклинание: Казнь", value="Ранг: Магистр.\nЦена: X\nДействие: Обнуляет баланс цели.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833858160271370.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Воинское искусство\".', description = "`=боевой крик @цель` - вы издаете громкий крик, приводя вашего союзника в боевую готовность.\n**Стоимость:** 40 монет.\nКоманда: `=боевой крик @цель` - цель получает от 20 до 30 золотых монет.\n**Применение** - до 10 раз в сутки.\n\n`=сокрушение @цель` - вы можете причинить сильный урон вашему противнику.\n**Стоимость:** 180 монет.\nКоманда: `=сокрушение @цель` - цель теряет от 250 до 260 золотых монет.\n**Применение** - до 10 раз в сутки.", color=0xc79c6e)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833858160271370.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Воинское искусство\".', description = "`=глухая оборона` - толстая броня делает воина безразличным к негативным эффектам.\n**Стоимость:** 180 монет.\nКоманда: `=глухая оборона` - вы получаете эффект защиты от мута (🛡:Щит).\n**Применение** - не ограничено.", color=0xc79c6e)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833858160271370.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Воинское искусство\".', description = "`=провокация @цель` - вы насмехаетесь над противником, от стыда он теряет всяческую защиту перед заклинаниями.\n**Стоимость:** 170 монет.\nКоманда: `=провокация @цель` - лишает цель эффекта защиты от мута.\n**Применение** - не ограничено.\n\n*Если у воина имеется эффект 🛡:Щит, он может спровоцировать противника бесплатно, рискуя потерять этот эффект.*\n\nКоманда: `=исступление @цель` - лишает цель эффекта защиты от мута. Заклинатель может потерять эффект 🛡:Щит с вероятностью 50%.\n**Применение** - не ограничено.", color=0xc79c6e)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833858160271370.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Воинское искусство\".', description = "`=ободряющий клич @цель` - вы издаёте клич, ободряющий и воодушевляющий вашего союзника.\n**Стоимость:** 150 монет.\nКоманда: `=ободряющий клич @цель` - цель получает 15 единиц опыта.\n**Применение** - до 3 раз в сутки.", color=0xc79c6e)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833858160271370.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Воинское искусство\".', description = "`=казнь @цель` - вы пытаетесь прикончить своего противника.\n**Стоимость:** - количество отнимаемых монет.\nКоманда: `=казнь @цель` - цель теряет ВСЕ свои монеты.\n**Применение** - 1 раз в сутки.", color=0xc79c6e)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833858160271370.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} откладывает книгу и берёт топор.", color=0xc79c6e)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="охотника")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_охотника(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Охота, зверь, стрельба\".', color=0xabd473)
        emb1.add_field(name="Заклинание: Прицельный выстрел", value="Ранг: Не требуется.\nЦена: 90\nДействие: Отнимает ~120 монет.", inline=True)
        emb1.add_field(name="Заклинание: Морозная ловушка", value="Ранг: Не требуется.\nЦена: 240\nДействие: Замедляет отправку сообщений на канале.", inline=True)
        emb1.add_field(name="Заклинание: Контузящий выстрел", value="Ранг: Подмастерье.\nЦена: 210\nДействие: Выдаёт мут.", inline=True)
        emb1.add_field(name="Заклинание: Призыв питомца (Команда \"Взять\")", value="Ранг: Искусник.\nЦена: 160\nДействие: Зависит от выбранного питомца.", inline=True)
        emb1.add_field(name="Заклинание: Притвориться мёртвым", value="Ранг: Мастер.\nЦена: 260\nДействие: Снимает все эффекты.", inline=True)
        emb1.add_field(name="Заклинание: Шквал", value="Ранг: Магистр.\nЦена: 3500\nДействие: Отнимает ~3500 монет первой цели и ~1000 второй.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833963592503358.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Охота, зверь, стрельба\".', description = "`=прицельный выстрел @цель` - меткий выстрел по вашему противнику.\n**Стоимость:** 90 монет.\nКоманда: `=прицельный выстрел @цель` - цель теряет 120 золотых.\n**Применение** - до 10 раз в сутки.\n\n`=морозная ловушка` - вы устанавливаете замораживающую ловушку, попавшие в неё противники заковываются в лёд.\n**Стоимость:** 240 монет.\nКоманда: `=морозная ловушка` - отправка сообщений на канале становится возможна раз в 15 минут.\n**Применение** - до 5 раз в сутки.", color=0xabd473)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833963592503358.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Охота, зверь, стрельба\".', description = "`=контузящий выстрел @цель` - выстрел промеж глаз вызывает у противника эффект Контузии (мут).\n**Стоимость:** 210 монет.\nКоманда: `=контузящий выстрел @цель` - цель не может отправлять сообщения на основном канале.\n**Применение** - не ограничено.", color=0xabd473)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833963592503358.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Охота, зверь, стрельба\".', description = "Призыв питомца - вы можете призвать одного из трёх питомцев (волк, медведь или стая воронов), а затем отдать ему команду.\n**Стоимость:** 160 монет.\n\nКоманда: `=призыв волка` - вы призываете волка, способного нанести урон противнику.\n**Применение** - не ограничено.\nКоманда: `=команда взять @цель` - волк кусает цель на 1% от баланса цели.\n**Применение** - до 10 раз в сутки.\n\nКоманда: `=призыв медведя` - вы призываете медведя, защищающего вас. Под защитой медведя, вы получаете эффект защиты от мута (🛡).\n**Применение** - не ограничено.\nКоманда: `=команда взять @цель` - медведь атакует противника и ещё одну цель, нанося каждому урон от 75 до 85 монет.\n**Применение** - до 10 раз в сутки.\n\nКоманда: `=призыв воронов` - вы призываете стаю воронов, кружащих вокруг.\n**Применение** - не ограничено.\nКоманда: `=команда взять` - во время атаки воронов, отправлять сообщения можно лишь раз в 1 минуту.\n**Применение** - до 10 раз в сутки.", color=0xabd473)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833963592503358.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Охота, зверь, стрельба\".', description = "`=притвориться мёртвым` - охотник убедительно притворяется мёртвым, снимая с себя все эффекты.\n**Стоимость:** 260 монет.\nКоманда: `=притвориться мёртвым` - вы теряете все эффекты. Можно использовать на канале <#610767915997986816>.\n**Применение** - не ограничено.", color=0xabd473)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833963592503358.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Охота, зверь, стрельба\".', description = "`=шквал @цель1 @цель2` - серия выстрелов, эффективно наносящая урон сразу двум противникам.\n**Стоимость:** 3500 монет.\nКоманда: `=шквал @цель1 @цель2` - первая цель теряет 10% от своего баланса плюс от 3500 до 3600 золотых монет, вторая цель теряет от 1000 до 1100 монет.\n**Применение** - 2 раза в сутки.", color=0xabd473)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833963592503358.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} подбрасывает книгу в воздух и сбивает её метким выстрелом.", color=0xabd473)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="разбойника")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_разбойника(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Грязные приёмы и воровская честь\".', color=0xfff569)
        emb1.add_field(name="Заклинание: Плащ теней", value="Ранг: Не требуется.\nЦена: 280\nДействие: Снимает все эффекты и даёт защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Держи свою долю", value="Ранг: Не требуется.\nЦена: 90\nДействие: Даёт ~60 монет.", inline=True)
        emb1.add_field(name="Заклинание: Обшаривание карманов", value="Ранг: Подмастерье.\nЦена: 0\nДействие: Крадёт ~55 монет.", inline=True)
        emb1.add_field(name="Заклинание: Удар по почкам", value="Ранг: Искусник.\nЦена: 220\nДействие: Выдаёт мут.", inline=True)
        emb1.add_field(name="Заклинание: Ослепление", value="Ранг: Мастер.\nЦена: 240\nДействие: Выгоняет с канала.", inline=True)
        emb1.add_field(name="Заклинание: Маленькие хитрости", value="Ранг: Магистр.\nЦена: 2800\nДействие: Даёт ~1800 монет и получает ~750 обратно.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833821942460426.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Грязные приёмы и воровская честь\".', description = "`=плащ теней` - плащ с головой укрывает вас от эффектов мута.\n**Стоимость:** 280 монет.\nКоманда: `=плащ теней` - вы теряете все действующие эффекты и получаете эффект защиты от мута (🛡).\n**Применение** - не ограничено.\n\n`=держи долю @цель` - вы разделяете свой незаконный доход с союзником.\n**Стоимость:** 90 монет.\nКоманда: `=держи долю @цель` - цель получает от 60 до 70 золотых, если её баланс меньше баланса разбойника.\n**Применение** - до 10 раз в сутки.", color=0xfff569)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833821942460426.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Грязные приёмы и воровская честь\".', description = "`=обшаривание карманов @цель` - вы обчищаете карманы вашего противника.\n**Стоимость:** 0 монет.\nКоманда: `=обшаривание карманов @цель` - цель теряет от 1 до 110 золотых монет. Вы получаете эти монеты.\n**Применение** - до 5 раз в сутки.", color=0xfff569)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833821942460426.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Грязные приёмы и воровская честь\".', description = "`=по почкам @цель` - вы отбиваете противнику почки. Больно и эффективно.\n**Стоимость:** 220 монет.\nКоманда: `=по почкам @цель` - цель оглушена и не может произнести ни слова (получает мут).\n**Применение** - не ограничено.", color=0xfff569)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833821942460426.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Грязные приёмы и воровская честь\".', description = "`=ослепление @цель` - вы используете специальный порошок, чтобы лишить противника зрения.\n**Стоимость:** 240 монет.\nКоманда: `=ослепление @цель` - цель больше не видит основной канал.\n**Применение** - не ограничено.", color=0xfff569)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833821942460426.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Грязные приёмы и воровская честь\".', description = "`=маленькие хитрости @цель` - вы проводите хитрые манипуляции со счетами, чтобы обогатить себя и вашего союзника, по пути стягивая чей-то кошелёк.\n**Стоимость:** 2800 монет.\nКоманда: `=маленькие хитрости @цель` - цель получает от 1800 до 1900 золотых. Вы получаете от 300 до 1200 монет обратно.\nПрименение - 2 раза в сутки.", color=0xfff569)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833821942460426.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} продаёт книгу по выгодной цене.", color=0xfff569)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="паладина")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_паладина(self, ctx: Context):
        emb1 = discord.Embed(title='Манускрипт заклинаний.\nГлава \"Орден паладинов и перековка светом\".', color=0xf58cba)
        emb1.add_field(name="Заклинание: Молот гнева", value="Ранг: Не требуется.\nЦена: 100\nДействие: Отнимает ~120 монет.", inline=True)
        emb1.add_field(name="Заклинание: Свет небес", value="Ранг: Не требуется.\nЦена: 120\nДействие: Даёт ~70 монет.", inline=True)
        emb1.add_field(name="Заклинание: Божественный щит", value="Ранг: Подмастерье.\nЦена: 120\nДействие: Даёт защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Освящение", value="Ранг: Искусник.\nЦена: 360\nДействие: Снимает чары с области.", inline=True)
        emb1.add_field(name="Заклинание: Перековка светом (Порицание, Правосудие света)", value="Ранг: Мастер.\nЦена: 200\nДействие: Выдает эффект \"Озарение\".", inline=True)
        emb1.add_field(name="Заклинание: Возложение рук", value="Ранг: Магистр.\nЦена: 50% монет на счёту\nДействие: Даёт 35% от монет на счёту.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833946043514880.png")
        emb2 = discord.Embed(title='Манускрипт заклинаний.\nГлава \"Орден паладинов и перековка светом\".', description = "`=молот гнева @цель` - тяжёлый молот позволяет нанести тяжёлый урон вашему противнику.\n**Стоимость:** 100 монет.\nКоманда: `=молот гнева @цель` - цель теряет от 120 до 130 золотых.\n**Применение** - до 10 раз в сутки.\n\n`=свет небес @цель` - вы восстанавливаете силы своему союзнику.\n**Стоимость:** 120 монет.\nКоманда: `=свет небес @цель` - цель получает от 70 до 80 золотых.\n**Применение** - до 10 раз в сутки.", color=0xf58cba)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833946043514880.png")
        emb3 = discord.Embed(title='Манускрипт заклинаний.\nГлава \"Орден паладинов и перековка светом\".', description = "`=божественный щит` - Свет защищает вас от негативных эффектов.\n**Стоимость:** 210 монет.\nКоманда: `=божественный щит` - вы получаете эффект защиты от мута (🛡).\n**Применение** - не ограничено.", color=0xf58cba)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833946043514880.png")
        emb4 = discord.Embed(title='Манускрипт заклинаний.\nГлава \"Орден паладинов и перековка светом\".', description = "`=освящение` - вы благословляете землю вокруг себя.\n**Стоимость:** 360 монет.\nКоманда: `=освящение` - вы снимаете все негативные чары (замедляющие отправку сообщений), действующие на текущую область.\n**Применение** - до 5 раз в сутки.", color=0xf58cba)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833946043514880.png")
        emb5 = discord.Embed(title='Манускрипт заклинаний.\nГлава \"Орден паладинов и перековка светом\".', description = "`=перековка светом` - вы проходите обряд перековки Светом.\n**Стоимость:** 200 монет.\nКоманда: `=перековка светом` - вы получаете эффект \"Озарение\" и 50 единиц опыта.\n**Применение** - не ограничено.\n\n*С эффектом Озарения паладину доступно:*\n\nКоманда: `=порицание @цель` - цель осознаёт свои грехи и лишается эффекта защиты от мута. Заклинатель может потерять эффект Озарения и 50 опыта.\n**Стоимость:** 30 монет.\n**Применение** - не ограничено.\n\nКоманда: `=правосудие света @цель` - цель теряет 15% своего баланса. Заклинатель может потерять Озарение и 50 опыта.\n**Стоимость:** 2400 монет.\n**Применение** - 2 раза в сутки.", color=0xf58cba)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833946043514880.png")
        emb6 = discord.Embed(title='Манускрипт заклинаний.\nГлава \"Орден паладинов и перековка светом\".', description = "`=возложение рук @цель` - вы спасаете жизнь своему союзнику.\n**Стоимость:**  - половина всех имеющихся у вас монет.\nКоманда: `=возложение рук @цель` - цель получает 35% от вашего баланса.\n**Применение** - 2 раза в сутки.", color=0xf58cba)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833946043514880.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} делает пасс рукой, закрывает манускрипт и озаряется светом.", color=0xf58cba)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="друида")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_друида(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Введение в друидизм и Изумрудный сон\".', color=0xff7d0a)
        emb1.add_field(name="Заклинание: Знак дикой природы", value="Ранг: Не требуется.\nЦена: 50\nДействие: Даёт ~30 монет.", inline=True)
        emb1.add_field(name="Заклинание: Железный мех", value="Ранг: Не требуется.\nЦена: 160\nДействие: Даёт защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Взбучка", value="Ранг: Подмастерье.\nЦена: 110\nДействие: Отнимает ~140 монет.", inline=True)
        emb1.add_field(name="Заклинание: Сноходец (Сновидение)", value="Ранг: Искусник.\nЦена: 200\nДействие: Даёт эффект \"Изумрудный сон\".", inline=True)
        emb1.add_field(name="Заклинание: Обновление", value="Ранг: Мастер.\nЦена: 4500\nДействие: Даёт ~3000 монет сразу и ещё ~500 в течении минуты.", inline=True)
        emb1.add_field(name="Заклинание: Гнев деревьев", value="Ранг: Магистр.\nЦена: 230\nДействие: Выдаёт мут.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833977177845790.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Введение в друидизм и Изумрудный сон\".', description = "`=знак природы @цель` - вы усиливаете своего союзника символом лапки над головой.\n**Стоимость:** 50 монет.\nКоманда: `=знак природы @цель` - цель получает от 30 до 40 золотых монет.\n**Применение** - до 10 раз в сутки.\n\n`=железный мех` - вы обращаетесь к духу медведя, чтобы он даровал вам защиту от негативных эффектов.\n**Стоимость:** 160 монет.\nКоманда: `=железный мех` - вы получаете эффект защиты от мута (🛡).\n**Применение** - не ограничено.", color=0xff7d0a)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833977177845790.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Введение в друидизм и Изумрудный сон\".', description = "`=взбучка @цель` - хороший удар по голове отрезвляет любого соперника.\n**Стоимость:** 110 монет.\nКоманда: `=взбучка @цель` - цель теряет от 140 до 150 золотых монет.\n**Применение** - до 10 раз в сутки.", color=0xff7d0a)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833977177845790.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Введение в друидизм и Изумрудный сон\".', description = "`=сноходец` - вы погружаетесь в Изумрудный сон. Пока вы в нём находитесь, раз в сутки вас могут посещать полезные видения.\n**Стоимость:** 200 монет.\nКоманда: `=сноходец` - вы получаете эффект \"Изумрудный сон.\" Применение - не ограничено.\n\n*В Изумрудном сне доступно:*\n\nКоманда: `=сновидение` - вы получаете от 50 до 60 монет и 10 опыта. Эффект Изумрудного сна не снимается.\n**Применение** - 1 раз в сутки.", color=0xff7d0a)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833977177845790.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Введение в друидизм и Изумрудный сон\".', description = "`=обновление @цель` - вы обращаетесь к силам природы, чтобы они исцелили вашего союзника.\n**Стоимость:** 4500 монет.\nКоманда: `=обновление @цель` - цель получает от 3000 до 3100 золотых монет. Дополнительно может дать от 495 до 505 монет через 30 секунд. Повторяется от 1 до 3 раз.\n**Применение** - 2 раза в сутки.", color=0xff7d0a)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833977177845790.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Введение в друидизм и Изумрудный сон\".', description = "`=гнев деревьев @цель` - вы призываете корни деревьев, полностью опутывающие вашего противника.\n**Стоимость:** 230 монет.\nКоманда: `=гнев деревьев @цель` - цель не может отправлять сообщения (получает мут).\n**Применение** - не ограничено.", color=0xff7d0a)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833977177845790.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} вешает книгу на свои оленьи рога.", color=0xff7d0a)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="шамана")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_шамана(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Шаманизм, основные понятия и язык стихий\".', color=0x0070de)
        emb1.add_field(name="Заклинание: Удар бури", value="Ранг: Не требуется.\nЦена: 60\nДействие: Отнимает ~70 монет.", inline=True)
        emb1.add_field(name="Заклинание: Волна исцеления", value="Ранг: Не требуется.\nЦена: 140\nДействие: Даёт ~90 монет.", inline=True)
        emb1.add_field(name="Заклинание: Сглаз", value="Ранг: Подмастерье.\nЦена: 190\nДействие: Снимает защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Выброс лавы", value="Ранг: Искусник.\nЦена: 2500\nДействие: Отнимает ~3000 монет. Может поджечь.", inline=True)
        emb1.add_field(name="Заклинание: Раскол", value="Ранг: Мастер.\nЦена: 360\nДействие: Замедляет отправку сообщений на канале.", inline=True)
        emb1.add_field(name="Заклинание: Цепное исцеление", value="Ранг: Магистр.\nЦена: 5500\nДействие: Даёт ~3500 монет. Лечит до пяти целей.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833872785805323.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Шаманизм, основные понятия и язык стихий\".', description = "`=удар бури @цель` - вы призываете силу стихий, чтобы нанести сокрушительный урон сопернику.\n**Стоимость:** 60 монет.\nКоманда: `=удар бури @цель` - цель теряет от 70 до 80 золотых монет.\n**Применение** - до 10 раз в сутки.\n\n`=волна исцеления @цель` - вы направляете мощный поток исцеления на вашего союзника.\n**Стоимость:** 140 монет.\nКоманда: `=волна исцеления @цель` - цель получает от 90 до 100 золотых монет.\n**Применение** - до 10 раз в сутки.", color=0x0070de)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833872785805323.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Шаманизм, основные понятия и язык стихий\".', description = "`=сглаз @цель` - вы превращаете противника в мелкого зверька, он теряет защиту от мута.\n**Стоимость:** 190 монет.\nКоманда: `=сглаз @цель` - превращает цель в лягушку, змею, мышь, живой мёд или улитку, по вашему выбору (на выбор даётся 5 секунд). Цель теряет эффект защиты от мута.\n**Применение** - не ограничено.", color=0x0070de)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833872785805323.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Шаманизм, основные понятия и язык стихий\".', description = "`=выброс лавы @цель` - огненная атака, наносящая урон и поджигающая противника.\n**Стоимость:** 2500 монет.\nКоманда: `=выброс лавы @цель` - цель теряет от 3000 до 3100 золотых монет, и если на балансе цели осталось больше 1000 монет, то огонь отнимает ещё 6% от остатка в течении 45 секунд.\n**Применение** - 2 раза в сутки.", color=0x0070de)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833872785805323.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Шаманизм, основные понятия и язык стихий\".', description = "`=раскол` - шаман раскалывает землю под ногами, вызывая у всех панику.\n**Стоимость:** 360 монет.\nКоманда: `=раскол` - отправка сообщений на основном канале становится возможна лишь раз в 1 час.\n**Применение** - до 5 раз в сутки.", color=0x0070de)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833872785805323.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Шаманизм, основные понятия и язык стихий\".', description = "`=цепное исцеление @цель` - вы вызываете поток исцеляющей энергии, восстанавливающий силы вашим союзникам.\n**Стоимость:** 5500 монет.\nКоманда: `=цепное исцеление @цель` - цель получает от 3500 до 3600 золотых монет, затем вторая цель (случайная, как и все последующие) получает от 800 до 900 монет, третья - от 600 до 700, четвёртая от 400 до 500 и пятая - от 200 до 300. Случайные цели могут повторяться не подряд, включая самого заклинателя.\n**Применение** - 2 раза в сутки.", color=0x0070de)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833872785805323.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} подкладывает книгу заклинаний под тотем, чтобы он не качался.", color=0x0070de)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="мага")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_мага(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Магия арканы, льда и пламени\".', color=0x69ccf0)
        emb1.add_field(name="Заклинание: Кольцо льда", value="Ранг: Не требуется.\nЦена: 160\nДействие: Замедляет отправку сообщений на канале.", inline=True)
        emb1.add_field(name="Заклинание: Превращение", value="Ранг: Не требуется.\nЦена: 210\nДействие: Снимает защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Огненный шар", value="Ранг: Подмастерье.\nЦена: 80\nДействие: Отнимает ~100 монет.", inline=True)
        emb1.add_field(name="Заклинание: Чародейский интеллект", value="Ранг: Искусник.\nЦена: 250\nДействие: Даёт 25 опыта.", inline=True)
        emb1.add_field(name="Заклинание: Сотворение пищи", value="Ранг: Мастер.\nЦена: 400\nДействие: Сотворить стол с едой.", inline=True)
        emb1.add_field(name="Заклинание: Метеор", value="Ранг: Магистр.\nЦена: 2800\nДействие: Отнимает ~3500 монет.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833910631014430.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Магия арканы, льда и пламени\".', description = "`=кольцо льда` - всё вокруг вас сковывается льдом.\n**Стоимость:** 160 монет.\nКоманда: `=кольцо льда` - отправка сообщений на основном канале возможна раз в 5 минут.\n**Применение** - до 5 раз в сутки.\n\n`=превращение @цель`- вы превращаете вашего противника в безобидную зверушку. Хорошо действует на цели с низким интеллектом.\n**Стоимость:** 210 монет.\nКоманда: `=превращение @цель` - цель превращается в овцу, кролика, обезьяну, пчелу или свинью по вашему выбору (на выбор даётся 5 секунд) и теряет эффект защиты от мута.\n**Применение** - не ограничено.", color=0x69ccf0)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833910631014430.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Магия арканы, льда и пламени\".', description = "`=огненный шар @цель` - поджигает противника вместе с его средствами.\n**Стоимость:** 100 монет.\nКоманда: `=огненный шар @цель` - цель теряет от 80 до 90 золотых монет.\n**Применение** - до 10 раз в сутки.", color=0x69ccf0)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833910631014430.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Магия арканы, льда и пламени\".', description = "`=чародейский интеллект @цель` - вы усиливаете умственные способности цели.\n**Стоимость:** 100 монет.\nКоманда: `=чародейский интеллект @цель` - цель получает 25 единиц опыта.\n**Применение** - до 3 раз в сутки.", color=0x69ccf0)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833910631014430.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Магия арканы, льда и пламени\".', description = "`=сотворение пищи` - вы создаёте стол с тремя блюдами, которыми может угоститься любой желающий.\n**Стоимость:** 400 монет.\nКоманда: `=сотворение пищи` - вы получаете три эффекта \"Пища\". Повторное применение обновляет количество пищи.\n**Применение** - до 5 раз в сутки.\n\n*Всем доступна команда:*\n\n`=угоститься у @цели` - цель теряет один эффект \"Пища\", а вы получаете от 80 до 90 монет.\n**Применение** - 1 раз в 5 минут.", color=0x69ccf0)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833910631014430.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Магия арканы, льда и пламени\".', description = "`=метеор @цель` - вы вызываете метеор, который падает на голову вашего противника.\n**Стоимость:** 2800 монет.\nКоманда: `=метеор @цель` - цель теряет 3500 золотых монет и ещё 5% от оставшегося счёта.\n**Применение** - 2 раза в сутки.", color=0x69ccf0)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833910631014430.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} аккуратно ставит книгу на полку.", color=0x69ccf0)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="жреца")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_жреца(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Служение Свету и Тьме\".', color=0xffffff)
        emb1.add_field(name="Заклинание: Слово силы: щит", value="Ранг: Не требуется.\nЦена: 70\nДействие: Даёт ~50 монет.", inline=True)
        emb1.add_field(name="Заклинание: Слово тьмы: молчание", value="Ранг: Не требуется.\nЦена: 250\nДействие: Выдаёт мут.", inline=True)
        emb1.add_field(name="Заклинание: Священная земля", value="Ранг: Подмастерье.\nЦена: 320\nДействие: Снимает чары с области.", inline=True)
        emb1.add_field(name="Заклинание: Молитва исцеления", value="Ранг: Искусник.\nЦена: 6000\nДействие: Даёт ~4000 монет.", inline=True)
        emb1.add_field(name="Заклинание: Облик Бездны (Воззвание)", value="Ранг: Мастер.\nЦена: 650\nДействие: Выдаёт эффект \"Облик Бездны\".", inline=True)
        emb1.add_field(name="Заклинание: Слово тьмы: безумие", value="Ранг: Магистр.\nЦена: 220\nДействие: Снимает защиту от мута.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833892759089173.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Служение Свету и Тьме\".', description = "`=щит @цель`- вы благословляете вашего союзника.\n**Стоимость:** 70 монет.\nКоманда: `=щит @цель` - цель получает от 50 до 60 золотых монет.\n**Применение** - до 10 раз в сутки.\n\n`=молчание @цель` - вы накладываете на врага проклятие немоты.\n**Стоимость:** 250 монет.\nКоманда: `=молчание @цель` - цель не может отправлять сообщения (получает мут).\n**Применение** - не ограничено.", color=0xffffff)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833892759089173.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Служение Свету и Тьме\".', description = "`=священная земля` - вы создаёте участок святой земли, на которой не действуют любые чары.\n**Стоимость:** 320 монет.\nКоманда: `=священная земля` - вы снимаете все негативные чары (замедляющие отправку сообщений), действующие на текущую область.\n**Применение** - до 5 раз в сутки.", color=0xffffff)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833892759089173.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Служение Свету и Тьме\".', description = "`=молитва исцеления @цель` - вы возносите молитву богам, чтобы исцелить духовные и телесные раны вашего союзника.\n**Стоимость:** 6000 монет.\nКоманда: `=молитва исцеления @цель` - цель получает от 4000 до 4100 золотых монет.\n**Применение** - 1 раз в минуту.", color=0xffffff)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833892759089173.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Служение Свету и Тьме\".', description = "`=облик бездны` - любое дело становится проще, когда у вас есть парочка вспомогательных щупалец. Раз в день вам доступно воззвание к Бездне.\n**Стоимость:** 650 монет.\nКоманда: `=облик бездны` - вы принимаете облик Бездны.\n**Применение** - не ограничено.\n\n*В облике Бездны становится доступно:*\n\nКоманда: `=воззвание` - вы получаете от 190 до 210 монет и теряете 15 единиц опыта. Облик Бездны не отменяется.\n**Применение** - 1 раз в сутки.", color=0xffffff)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833892759089173.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Служение Свету и Тьме\".', description = "`=безумие @цель` - вы вторгаетесь в разум вашего противника и сводите его с ума.\n**Стоимость:** 220 монет.\nКоманда: `=безумие @цель` - цель теряет эффект защиты от мута.\n**Применение** - не ограничено.", color=0xffffff)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833892759089173.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} жертвует книгу бедным.", color=0xffffff)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="тьмы")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def чёрная_книга(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Чёрная магия и чем её запивать\".', color=0x9482c9)
        emb1.add_field(name="Заклинание: Страх", value="Ранг: Не требуется.\nЦена: 190\nДействие: Выдаёт мут.", inline=True)
        emb1.add_field(name="Заклинание: Стрела тьмы", value="Ранг: Не требуется.\nЦена: 70\nДействие: Отнимает ~90 монет.", inline=True)
        emb1.add_field(name="Заклинание: Катаклизм", value="Ранг: Подмастерье.\nЦена: 240\nДействие: Замедляет отправку сообщений на канале.", inline=True)
        emb1.add_field(name="Заклинание: Тёмный пакт", value="Ранг: Искусник.\nЦена: 170\nДействие: Даёт ~120 монет и беса.", inline=True)
        emb1.add_field(name="Заклинание: Ожог души", value="Ранг: Мастер.\nЦена: 2700\nДействие: Отнимает ~50 опыта и до 3300 монет.", inline=True)
        emb1.add_field(name="Заклинание: Преисподняя", value="Ранг: Магистр.\nЦена: 360\nДействие: Серьёзно замедляет отправку сообщений на канале.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833865638723615.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Чёрная магия и чем её запивать\".', description = "`=страх @цель` - вы вызываете у вашего противника чувство инфернального страха, от чего он долго бежит в стену.\n**Стоимость:** 190 монет.\nКоманда: `=страх @цель` - цель не может отправлять сообщения на основном канале (получает мут).\n**Применение** - не ограничено.\n\n`=стрела тьмы @цель` - вы поражаете противника тёмной магией.\n**Стоимость:** 70 монет.\nКоманда: `=стрела тьмы @цель` - цель теряет от 90 до 100 золотых монет.\n**Применение** - до 10 раз в сутки.", color=0x9482c9)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833865638723615.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Чёрная магия и чем её запивать\".', description = "`=катаклизм` - вы вызываете бедствие небольшого масштаба, досаждающее всем противникам вокруг.\n**Стоимость:** 240 монет.\nКоманда: `=катаклизм` - отправка сообщений на основном канале возможна лишь раз в 15 минут.\n**Применение** - до 5 раз в сутки.", color=0x9482c9)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833865638723615.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Чёрная магия и чем её запивать\".', description = "`=тёмный пакт @цель` - вы заключаете договор с бесом, продавая ему душу вашего союзника.\n**Стоимость:** 170 монет.\nКоманда: `=тёмный пакт @цель` - цель получает от 120 до 130 золотых монет и недовольного беса впридачу (эффект \"Контракт\").\n**Применение** - до 5 раз в сутки.\n\n*Бес на плече оказывает негативное влияние, может украсть ваши \"Предметы\", а также позволяет использовать команду:*\n\n`=расплата @цель` - вы расплачиваетесь со своим бесом за чужой счёт.\n`=расплата @цель` - цель теряет от 120 до 130 монет. Вы теряете эффект \"Контракт\".\n**Применение** - до 10 раз в сутки.", color=0x9482c9)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833865638723615.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Чёрная магия и чем её запивать\".', description = "`=ожог души @цель` - вы сжигаете душу противника, нанося ему серьёзный урон.\n**Стоимость:** 2700 монет.\nКоманда: `=ожог души @цель` - цель теряет от 10 до 100 единиц опыта, а также до 3300 золотых монет (сумма уменьшается на 10 монет за каждую единицу отнятого опыта).\n**Применение** - 2 раза в сутки.", color=0x9482c9)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833865638723615.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Чёрная магия и чем её запивать\".', description = "`=преисподняя` - вы открываете червоточину в Круговерть Пустоты, которая засасывает в себя любого неосторожного противника.\n**Стоимость:** 360 монет.\nКоманда: `=преисподняя` - отправка сообщений на основном канале возможна лишь раз в 6 часов.\n**Применение** - 2 раза в сутки.", color=0x9482c9)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/889833865638723615.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} поджигает книгу в руках и странно смеётся.", color=0x9482c9)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="смерти")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_смерти(self, ctx: Context):
        emb1 = discord.Embed(title='Книга, написанная кровью, в переплёте из человеческой кожи.', color=0xc41f3b)
        emb1.add_field(name="Заклинание: Осквернение", value="Ранг: Не требуется.\nЦена: 240\nДействие: Замедляет отправку сообщений на канале.", inline=True)
        emb1.add_field(name="Заклинание: Удар Плети", value="Ранг: Не требуется.\nЦена: 160\nДействие: Отнимает ~240 монет.", inline=True)
        emb1.add_field(name="Заклинание: Уничтожение", value="Ранг: Подмастерье.\nЦена: 3000\nДействие: Отнимает ~4000 монет.", inline=True)
        emb1.add_field(name="Заклинание: Антимагический панцирь", value="Ранг: Искусник.\nЦена: 140\nДействие: Выдаёт защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Перерождение (Взрыв трупа)", value="Ранг: Мастер.\nЦена: 200\nДействие: Меняет защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Беспощадность зимы", value="Ранг: Магистр.\nЦена: 360\nДействие: Обнуляет баланс цели.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280885926531083.png")
        emb2 = discord.Embed(title='Книга, написанная кровью, в переплёте из человеческой кожи.', description = "`=осквернение` - вы оскверняете землю под вашими противниками.\n**Стоимость:** 240 монет.\nКоманда: `=осквернение` - отправка сообщений на основном канале возможна раз в 15 минут.\n**Применение** - до 5 раз в сутки.\n\n`=удар плети @цель` - вы поражаете слабое место противника нечестивым ударом.\n**Стоимость:** 160 монет.\nКоманда: `=удар плети @цель` - цель теряет от 240 до 250 золотых монет.\n**Применение** - до 10 раз в сутки.", color=0xc41f3b)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280885926531083.png")
        emb3 = discord.Embed(title='Книга, написанная кровью, в переплёте из человеческой кожи.', description = "`=уничтожение @цель` - жестокая атака, не оставляющая от противника и мокрого места.\n**Стоимость:** 3000 монет.\nКоманда: `=уничтожение @цель` - цель теряет 4% своего баланса и от 4000 до 4100 золотых монет. Вы накапливаете брызги крови(🩸). Если их достаточно, вы получаете 1% от баланса противника.\n**Применение** - 2 раза в сутки.", color=0xc41f3b)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280885926531083.png")
        emb4 = discord.Embed(title='Книга, написанная кровью, в переплёте из человеческой кожи.', description = "`=антимагический панцирь` - вы окружаете себя защитным панцирем, поглощающим заклинания.\n**Стоимость:** 140 монет.\nКоманда: `=антимагический панцирь` - вы получаете эффект защиты от мута (🛡).\n**Применение** - не ограничено.", color=0xc41f3b)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280885926531083.png")
        emb5 = discord.Embed(title='Книга, написанная кровью, в переплёте из человеческой кожи.', description = "`=перерождение @цель` - вы взываете к силам нечестивости и льда, чтобы ваш противник стал нежитью.\n**Стоимость:** 200 монет.\nКоманда: `=перерождение @цель` - цель получает эффект защиты от мута (🛡:Нежить). Он заменяет любой другой эффект защиты при наличии.\n**Применение** - не ограничено.\n\n`=взрыв трупа @цель` - вы взрываете тело противника с эффектом 🛡:Нежить, разбрасывая вокруг кровь, куски мяса и кости.\n**Стоимость:** 80 золотых.\nКоманда: `=взрыв трупа @цель` - цель теряет от 100 до 110 золотых монет и эффект 🛡:Нежить.\n**Применение** - до 10 раз в сутки.\n\n*Взрыв трупа может применять любой рыцарь смерти, не зависимо от ранга.*", color=0xc41f3b)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280885926531083.png")
        emb6 = discord.Embed(title='Книга, написанная кровью, в переплёте из человеческой кожи.', description = "`=беспощадность зимы` - вы призываете неистовую снежную бурю, вытягивающую жизнь из противников вокруг вас.\n**Стоимость:** 360 монет.\nКоманда: `=беспощадность зимы` - отправка сообщений на основном канале возможна лишь раз в 1 час. Каждую минуту случайная цель теряет 1% от своего баланса, повторяется, пока не отнимет 200 монет.\n**Применение** - 2 раза в сутки.", color=0xc41f3b)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280885926531083.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} выкидывает книгу и забывает всё, что в ней было написано.", color=0xc41f3b)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="монаха")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_монаха(self, ctx: Context):
        emb1 = discord.Embed(title='Книга заклинаний.\nГлава \"Рукопашный бой и энергия Ци\".', color=0x00ffba)
        emb1.add_field(name="Заклинание: Маначай", value="Ранг: Не требуется.\nЦена: 60\nДействие: Даёт ~40 монет.", inline=True)
        emb1.add_field(name="Заклинание: Пошатывание", value="Ранг: Не требуется.\nЦена: 150\nДействие: Даёт защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Бочонок эля", value="Ранг: Подмастерье.\nЦена: 3500\nДействие: Выдаёт предмет \"Бочонок эля\".", inline=True)
        emb1.add_field(name="Заклинание: Трансцендентность (Медитация)", value="Ранг: Искусник.\nЦена: 350\nДействие: Даёт эффект \"Трансцендентность\".", inline=True)
        emb1.add_field(name="Заклинание: Рука-копьё", value="Ранг: Мастер.\nЦена: 200\nДействие: Выдаёт мут.", inline=True)
        emb1.add_field(name="Заклинание: Духовное путешествие (Возвращение)", value="Ранг: Магистр.\nЦена: от 11111\nДействие: Даёт эффект \"Астрал\".", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280924782571550.png")
        emb2 = discord.Embed(title='Книга заклинаний.\nГлава \"Рукопашный бой и энергия Ци\".', description = "`=маначай @цель` - вы завариваете вкусный маначай и угощаете им своего союзника.\n**Стоимость:** 60 монет.\nКоманда: `=маначай @цель` - цель получает от 40 до 50 золотых монет.\n**Применение** - до 10 раз в сутки.\n\n`=пошатывание` - лёгкое опьянение защищает вас от ряда заклинаний.\n**Стоимость:** 150 монет.\nКоманда: `=пошатывание` - вы получаете эффект защиты от мута (🛡).\n**Применение** - не ограничено.", color=0x00ffba)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280924782571550.png")
        emb3 = discord.Embed(title='Книга заклинаний.\nГлава \"Рукопашный бой и энергия Ци\".', description = "`=бочонок эля @цель` - вы бросает союзнику бочонок доброго эля, способного помирить кого угодно.\n**Стоимость:** 3500 монет.\nКоманда: `=бочонок эля @цель` - цель получает \"Предмет: Бочонок эля\".\n**Применение** - 2 раза в сутки.\n\n*\"Предмет: Бочонок эля\" даёт доступ к командам:*\n\n`=выпить эль` - вы откупориваете бочонок и опустошаете его.\n`=выпить эль` - вы получаете от 2500 до 2600 золотых монет и теряете \"Предмет: Бочонок эля\".\n**Применение** - не ограничено.\n\n`=распить эль @цель` - вы делитесь содержимым бочонка с другом.\n`=распить эль @цель` - вы и цель получаете от 1250 до 1300 золотых монет каждый, вы теряете \"Предмет: Бочонок эля\".\n**Применение** - не ограничено.\n\n`=отдать эль @цель` - вы отдаёте союзнику бочонок доброго эля.\n`=отдать эль @цель` - вы передаёте цели \"Предмет: Бочонок эля\".\n**Применение** - не ограничено.", color=0x00ffba)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280924782571550.png")
        emb4 = discord.Embed(title='Книга заклинаний.\nГлава \"Рукопашный бой и энергия Ци\".', description = "`=трансцендентность` - ваш дух внезапно отделяется от телесной оболочки. Ежедневные медитации дают о себе знать.\n**Стоимость:** 350 монет.\nКоманда: `=трансцендентность` - вы получаете эффект \"Трансцендентность\".\n**Применение** - не ограничено.\n\n*С эффектом Трансцендентности монаху доступна команда:*\n\nКоманда: `=медитация` - вы получаете от 90 до 100 золотых. Эффект Трансцендентности не отменяется.\n**Применение** - 1 раз в сутки.", color=0x00ffba)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280924782571550.png")
        emb5 = discord.Embed(title='Книга заклинаний.\nГлава \"Рукопашный бой и энергия Ци\".', description = "`=рука копьё @цель` - вы наносите резкий удар в горло противника.\n**Стоимость:** 200 монет.\nКоманда: `=рука копьё @цель` - цель хрипит и не может отправлять сообщения в основном канале (получает мут).\n**Применение** - не ограничено.", color=0x00ffba)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280924782571550.png")
        emb6 = discord.Embed(title='Книга заклинаний.\nГлава \"Рукопашный бой и энергия Ци\".', description = "`=духовное путешествие`- вы создаёте астрального двойника, который отправляется в небывалое путешествие.\n**Стоимость:** - 10% от вашего баланса плюс 10000 монет.\nКоманда: `=духовное путешествие` - вы переходите в состояние \"Астрал\".\n**Применение** - не ограничено.\n\n*Находясь в состоянии Астрала, монаху доступна команда:*\n\n`=возвращение` - вы меняетесь местами со своим астральным духом.\n`=возвращение` - вы получаете 10% от текущего баланса и 10000 золотых монет впридачу и теряете состояние \"Астрал\".\n**Применение** - не ограничено.", color=0x00ffba)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280924782571550.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                emb=discord.Embed(description=f"{ctx.author.display_name} оставляет в книге закладку и убирает за пазуху.", color=0x00ffba)
                await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="демонов")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_демонов(self, ctx: Context):
        emb1 = discord.Embed(title='Книга, написанная на языке демонов.', color=0xa330c9)
        emb1.add_field(name="Заклинание: Мрак", value="Ранг: Не требуется.\nЦена: 160\nДействие: Замедляет отправку сообщений на канале.", inline=True)
        emb1.add_field(name="Заклинание: Демонические шипы", value="Ранг: Не требуется.\nЦена: 170\nДействие: Даёт защиту от мута.", inline=True)
        emb1.add_field(name="Заклинание: Пронзающий взгляд", value="Ранг: Подмастерье.\nЦена: 120\nДействие: Забирает 12 опыта.", inline=True)
        emb1.add_field(name="Заклинание: Печать немоты", value="Ранг: Искусник.\nЦена: 170\nДействие: Выдаёт мут.", inline=True)
        emb1.add_field(name="Заклинание: Танец клинков", value="Ранг: Мастер.\nЦена: 0\nДействие: Забирает по ~50 монет у пяти жертв.", inline=True)
        emb1.add_field(name="Заклинание: Сожжение заживо", value="Ранг: Магистр.\nЦена: 4000\nДействие: Отнимает 25% монет.", inline=True)
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280848689528852.png")
        emb2 = discord.Embed(title='Книга, написанная на языке демонов.', description = "`=кэлор` (мрак) - вы распространяете вокруг себя мрак, скрывающий всё из виду.\n**Стоимость:** 160 монет.\nКоманда: `=кэлор` - отправка сообщений на основном канале возможна раз в 5 минут.\n**Применение** - до 5 раз в сутки.\n\n`=эраде сарг` (демонические шипы) - вас переполняет энергия Скверны, усиливающая вашу броню страшными наростами.\n**Стоимость:** 170 монет.\nКоманда: `=эраде сарг` - вы получаете эффект защиты от мута (🛡).\n**Применение** - не ограничено.", color=0xa330c9)
        emb2.set_footer(text="Ранг не требуется.")
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280848689528852.png")
        emb3 = discord.Embed(title='Книга, написанная на языке демонов.', description = "`=гором хагуул @цель` (пронзающий взгляд) - энергия Скверны бьёт из ваших глаз в противника.\n**Стоимость:** 120 монет.\nКоманда: `=гором хагуул @цель` - цель теряет 12 единиц опыта, вы получаете отнятый опыт.\n**Применение** - до 3 раз в сутки.", color=0xa330c9)
        emb3.set_footer(text="Ранг Подмастерье.")
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280848689528852.png")
        emb4 = discord.Embed(title='Книга, написанная на языке демонов.', description = "`=шах кигон @цель` (печать немоты) - возле вас загорается яркий рисунок печати. Попавшая в неё цель - умолкает ~~навечно~~.\n**Стоимость:** 180 монет.\nКоманда: `=шах кигон @цель` - цель не может отправлять сообщения в основной канал (получает мут). Печать срабатывает через минуту.\n**Применение** - не ограничено.", color=0xa330c9)
        emb4.set_footer(text="Ранг Искусник.")
        emb4.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280848689528852.png")
        emb5 = discord.Embed(title='Книга, написанная на языке демонов.', description = "`=эраз закзир` (танец клинков) - вы атакует 5 противников разом.\n**Стоимость:** 0 монет.\nКоманда: `=эраз закзир` - каждая из 5 случайных целей теряет от 1 до 100 золотых монет. Вы получаете все отнятые монеты.\n**Применение** - 1 раз в сутки.", color=0xa330c9)
        emb5.set_footer(text="Ранг Мастер.")
        emb5.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280848689528852.png")
        emb6 = discord.Embed(title='Книга, написанная на языке демонов.', description = "`=катра шукил @цель` (сожжение заживо) - вы ставите на противника демоническое клеймо, которое мгновенно сжигает его плоть.\n**Стоимость:** 4000 монет.\nКоманда: `=катра шукил @цель` - цель теряет 25% от своего баланса.\n**Применение** - 2 раза в сутки.", color=0xa330c9)
        emb6.set_footer(text="Ранг Магистр.")
        emb6.set_thumbnail(url="https://cdn.discordapp.com/emojis/921280848689528852.png")
        msg = await ctx.send(embed=emb1, components=[Select(placeholder="Подробнее:", options=[SelectOption(label="Без ранга", value="1"), SelectOption(label="Подмастерье", value="2"), SelectOption(label="Искусник", value="3"), SelectOption(label="Мастер", value="4"), SelectOption(label="Магистр", value="0")])])
        try:
            interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await msg.edit(embed=emb1, components = [])
        await interaction.edit_origin()
        i=int(interaction.values[0])
        while True:
            if i%5 == 1:
                emb0=emb2
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 2:
                emb0=emb3
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 3:
                emb0=emb4
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            elif i%5 == 4:
                emb0=emb5
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            else:
                emb0=emb6
                await msg.edit(embed=emb0, components = [[Button(style = ButtonStyle.green, label = 'Назад'), Button(style = ButtonStyle.green, label = 'Вперёд'), Button(style = ButtonStyle.red, label = 'Закрыть')]])
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Вперёд':
                i+=1
            elif responce.component.label == 'Назад':
                i-=1
            else:
                authbal=await bank.get_balance(ctx.author)
                if authbal>0:
                    await bank.withdraw_credits(ctx.author, 1)
                    emb=discord.Embed(description=f"Книга демонов кусает {ctx.author.display_name} за палец.\nОт неожиданности {ctx.author.mention} теряет одну монетку.", color=0xa330c9)
                    await msg.edit(embed=emb, components=[])
                else:
                    emb=discord.Embed(description=f"Книга демонов пытается укусить {ctx.author.display_name} за палец.", color=0xa330c9)
                    await msg.edit(embed=emb, components=[])
                return

    @книга.command(name="анклава")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def книга_анклава(self, ctx: Context):
        scr=self.bot.get_emoji(625192051042156565)
        mag=self.bot.get_emoji(893780879648894987)
        faq=self.bot.get_emoji(893780946204110858)
        clas=self.bot.get_emoji(893784527237959690)
        com=self.bot.get_emoji(893785089115295767)
        clos=self.bot.get_emoji(893785873240428565)
        emb0 = discord.Embed(title="*Перед вами лежит толстая книга, в которой собрано немало мудростей.*", colour=discord.Colour.gold())
        emb0.set_thumbnail(url="https://static.wikia.nocookie.net/wow/images/1/17/Inv_misc_book_09.png/revision/latest/scale-to-width-down/68?cb=20170402101159&path-prefix=ru")
        emb1 = discord.Embed(title="**Книга Анклава Солнца и Луны.\nГлава \"Подсчёт опыта\".**", description = "На сервере идёт подсчёт опыта за активность каждого участника - от 1 до 3 единиц опыта за сообщение, в зависимости от его размера.\n\nУзнать свой или чужой уровень и количество опыта можно с помощью команды:\n`=уровень` или `=ур`\nОбщий список лидеров:\n`=лидеры`\n\nНа каждом пятом уровне вас ждёт награда в виде какого-то сундука (будет выдана роль <@&696014224442392717>).\nОткрыть его можно с помощью команды:\n`=сундук`\n\nЗа открытие сундука можно получить некоторую сумму золотых монет или повышение ранга мастерства, нужного для применения различных заклинаний.\n\nРангов всего 10:\nУченик -> Подмастерье -> Умелец -> Искусник -> Знаток -> Мастер -> Специалист -> Магистр -> Профессионал -> Эксперт.\nРанг Профессионал может быть получен с шансом 25%, а ранг Эксперт - 22,2%.\n\n*При достижении ранга Эксперт, участник получает новое заклинание для своего класса (по своему выбору).*", colour=discord.Colour.gold())
        emb2 = discord.Embed(title="**Книга Анклава Солнца и Луны.\nГлава \"Правила магии\".**", description = "Использование магии досупно только на канале <#603151774009786393>, за редким исключением.\nМагию могут применять участники, обладающие классом.\n\nБудьте внимательны при написании команд:\n*Соблюдайте указание целей для тех заклинаний, которые это требуют, и не указывайте там, где это не требуется. Это крайне опасно!*\n*Соблюдайте регистр и пунктуацию, магия очень чувствительна к этому.*\nУ каждого заклинания есть свой кулдаун.\n\nНа канале <#610767915997986816> в закреплённых сообщениях есть информация как приобрести предметы, снимающие те или иные эффекты.\nНапоминание: Если вам срочно нужна помощь, но доступ в <#603151774009786393> закрыт из-за негативного магического эффекта, можете обратиться за помощью в общий канал своей фракции в Окрестностях Фераласа.", colour=discord.Colour.gold())
        emb3 = discord.Embed(title="**Книга Анклава Солнца и Луны.\nГлава \"О классах\".**", description = "Чтобы выбрать себе класс - введите команду:\n`=выбрать класс`\n\nЧтобы узнать, на что способен ваш класс, введите одну из перечисленных команд, соответствующую интересующему вас классу:\n`=книга воина`,\n`=книга друида`,\n`=книга жреца`,\n`=книга мага`,\n`=книга монаха`,\n`=книга охотника`,\n`=книга паладина`,\n`=книга разбойника`,\n`=книга шамана`,\nа также:\n`=книга тьмы` - для чернокнижника,\n`=книга демонов` - для охотника на демонов\nи\n`=книга смерти` - для рыцаря смерти.", colour=discord.Colour.gold())
        emb4 = discord.Embed(title="**Книга Анклава Солнца и Луны.\nГлава \"Общие команды\".**", description = "**Команды информации:**\n*Использование этих команд доступно на любом канале.*\n\n`=уровень` или `=ур` - узнать свой или чужой прогресс.\n`=лидеры` - список наиболее опытных участников.\n`=баланс` или `=б` - узнать состояние своего или чужого счёта.\n`=счета` - список наиболее богатых участников. Чтобы увидеть больше, нужно указывать число отображаемых участников (например, `=счета 25`).\n\n**Команды эмоций:**\n\n`=бросить @цель` - и так понятно.\n`=обнять @цель` - можно указать силу обнимашек.\n`=ответь <вопрос?>` - задать вопрос старой тортолланке.\n`=выбери <несколько вариантов>` - сделать выбор.\n\n**Команды покупок:**\nДоступны на канале <#610767915997986816>\n\n`=купить зелье` - приобрести предмет \"Зелье рассеивания чар\".\n`=выпить зелье` - снять с себя все Эффекты.\n`=купить свиток` - приобрести предмет \"Свиток антимагии\"\n`=прочесть свиток` - снять все чары с канала (отправлять команду нужно на том канале, на который хотите подействовать).\n`=купить пропуск` - приобрести временный VIP-пропуск на закрытые каналы.\n`=выбросить пропуск` - вернуться на общедоступные каналы.", colour=discord.Colour.gold())
        emb5 = discord.Embed(title="**Книга Анклава Солнца и Луны.\nГлава \"Часто задаваемые вопросы\". Часть 1.**", description = "Q: Как мне узнать свой уровень?\nA: Написать команду `=уровень` или `=ур`, и подождать пару секунд.\nQ: Там есть шкала опыта, за что я его получаю?\nA: За каждое сообщение на общедоступных каналах (кроме строчилки) - 1 единица опыта. Если сообщение >15 символов - 2 единицы, если >30 - 3.\nQ: Я флужу, как потерпевший, а опыт растёт медленно!\nA: Опыт начисляется раз в 90 секунд.\nQ: Как мне получить роль класса?\nA: Нужно написать команду `=выбрать класс` и выбрать класс, следуя инструкциям.\nQ: Мне постоянно не хватает золота, где его можно взять?!\nA: На данный момент золото можно получить: играя в викторину, получить в наградном уровневом сундуке, выиграть что-нибудь в казино, получить от других участников заклинаниями лечения и усиления, а также монеты выдаются в ходе различных турниров и ивентов на сервере. В планах команды на выполнение поручений и отражение атак огров.\nQ: Почему я должен платить золото за каждое использование заклинаний, они очень дорогие, что за грабительская система?!\nA: Систему придумал и реализовал гоблин.\nQ: Я не могу писать на канале <#603151774009786393>!\nA: Скорее всего вас кто-то заглушил заклинанием, проверьте свои роли на наличие отрицательных эффектов. Можете их рассеять, купив и выпив зелье в <#610767915997986816>, подробности в его закрепах.\nQ: Меня постоянно атакуют и сжигают все мои монеты! Казлы!\nA: Чаще всего атаками наказывают за неадекватное поведение и грубость в чате. Ведите себя дружелюбно и ситуация улучшится.", colour=discord.Colour.gold())
        emb6 = discord.Embed(title="**Книга Анклава Солнца и Луны.\nГлава \"Часто задаваемые вопросы\". Часть 2.**", description = "Q: Меня постоянно глушит один недоброжелатель, что делать?\nA: Некоторые классы имеют сейвы, которые дают защиту от мута. Если его у вас нет, вы можете договориться с другим участниками (или подкупить их), чтобы совместно атаковать вашего врага.\nQ: Что за ранги мастерства?\nA: Это уровень владения заклинаниями вашего класса. Каждые 5 уровней вам будет предложен выбор, улучшить ранг или получить некоторую сумму золотых монет.\nQ: Могу ли я передать золото другому участнику?\nA: Только с помощью заклинаний лечения/усиления.\nQ: Можно ли выбрать два разных класса?\nA: Двойная специализация в разработке. К моменту появления первого Эксперта своего класса, она уже должна заработать.", colour=discord.Colour.gold())
        msg = await ctx.send(embed=emb0, components=[Select(placeholder="Выбрать главу:", options=[SelectOption(label="Подсчёт опыта", value="exp", emoji=scr), SelectOption(label="Правила магии", value="magic", emoji=mag), SelectOption(label="О классах", value="class", emoji=clas), SelectOption(label="Общие команды", value="commands", emoji=com), SelectOption(label="Частые вопросы, часть 1", value="faq1", emoji=faq), SelectOption(label="Частые вопросы, часть 2", value="faq2", emoji=faq), SelectOption(label="Запретная глава (не открывать!)", value="close", emoji=clos)])])
        embed=emb0
        while True:
            try:
                interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=60)
            except asyncio.TimeoutError:
                return await msg.edit(embed=embed, components = [])
            await interaction.edit_origin()
            if interaction.values[0] == 'exp':
                embed=emb1
            elif interaction.values[0] == 'magic':
                embed=emb2
            elif interaction.values[0] == 'class':
                embed=emb3
            elif interaction.values[0] == 'commands':
                embed=emb4
            elif interaction.values[0] == 'faq1':
                embed=emb5
            elif interaction.values[0] == 'faq2':
                embed=emb6
            else:
                embed=discord.Embed(description=f"*Книга осуждающе смотрит на {ctx.author.display_name} и растворяется в воздухе.*")
                return await msg.edit(embed=embed, components = [])
            await msg.edit(embed=embed, components=[Select(placeholder="Выбрать главу:", options=[SelectOption(label="Подсчёт опыта", value="exp", emoji=scr), SelectOption(label="Правила магии", value="magic", emoji=mag), SelectOption(label="О классах", value="class", emoji=clas), SelectOption(label="Общие команды", value="commands", emoji=com), SelectOption(label="Частые вопросы, часть 1", value="faq1", emoji=faq), SelectOption(label="Частые вопросы, часть 2", value="faq2", emoji=faq), SelectOption(label="Запретная глава (не открывать!)", value="close", emoji=clos)])])

    @commands.command()
    async def бросить(self, ctx, user: discord.Member = None):
        if user is not None:
            msg = ""
            if user.id == ctx.bot.user.id or user.id == 384719867653259264:
                user = ctx.author
                msg = "Хорошая попытка. Вы думаете это смешно?\n Как насчет __этого__ тогда:\n\n"
            char = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎzɐƍʚɹɓǝǝжεиņʞvwноudɔɯʎфхǹҺmmqqqєoʁ"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z∀ƍʚɹɓƎƎжεИИʞVWНОuԀƆɯʎФХǹҺmmqqqєoʁ"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await ctx.send(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await ctx.send("*бросок топора и... " + random.choice(["ОТРУБЛЕННАЯ ГОЛОВА!*", "КРОВЬ, КИШКИ, ГОВНО!!!*"]))

    @commands.command()
    async def обнять(self, ctx, user: discord.Member = None, intensity: int = 1):
        if user is None:
            online=[]
            async for mes in ctx.message.channel.history(limit=100,oldest_first=False):
                if mes.author!=ctx.bot.user and mes.author not in online:
                    online.append(mes.author)
            user=random.choice(online)
        if user==ctx.bot.user:
            return await ctx.send("Спасибо, я тоже тебя люблю! <:zHeart:620973874556829747>")
        name = italics(user.display_name)
        if intensity <= 0:
            msg = "(っ˘̩╭╮˘̩)っ" + name
        elif intensity <= 3:
            msg = "(っ´▽｀)っ" + name
        elif intensity <= 6:
            msg = "╰(*´︶`*)╯" + name
        elif intensity <= 9:
            msg = "(つ≧▽≦)つ" + name
        elif intensity >= 10:
            msg = "(づ￣ ³￣)づ{} ⊂(´・ω・｀⊂)".format(name)
        await ctx.send(msg)
        
    @commands.command()
    async def ответь(self, ctx, *, question: str = ""):
        if question=="":
            await ctx.send("И на что ответить тебе?")
        elif question.endswith("?") and question != "?":
            await ctx.send(random.choice(self.ANS))
        else:
            await ctx.send("Да... Нет... Как на это можно ответить? Это вообще вопрос?!")

    @commands.command(usage="<choice> <choices...>")
    async def выбери(self, ctx, *choices):
        choices = [escape(c, mass_mentions=True) for c in choices if c]
        if len(choices) < 2:
            await ctx.send("Слишком мало вариков!")
        else:
            await ctx.send(random.choice(choices))

    @commands.command()
    async def скажи(self, ctx, room: discord.TextChannel = None, *, text):
        GOB=discord.utils.get(ctx.guild.roles, id=583993057330855946)
        TAE=discord.utils.get(ctx.guild.roles, id=602362721660305433)
        SOL=discord.utils.get(ctx.guild.roles, id=848948041696542731)
        CHE=discord.utils.get(ctx.guild.roles, id=709346269491101757)
        ELS=discord.utils.get(ctx.guild.roles, id=899150508139376660)
        if GOB in ctx.author.roles or TAE in ctx.author.roles or SOL in ctx.author.roles or CHE in ctx.author.roles or ELS in ctx.author.roles:
            msg = await room.send(text)
        else:
            await ctx.send(text)
            await ctx.send("И что дальше?")

    @commands.group(name="позорный", autohelp=False)
    async def позорный(self, ctx: commands.GuildContext):
        pass

    @позорный.command(name="столб")
    async def позорный_столб(self, ctx, user: discord.Member = None):
        GOB=discord.utils.get(ctx.guild.roles, id=583993057330855946)
        TAE=discord.utils.get(ctx.guild.roles, id=602362721660305433)
        SOL=discord.utils.get(ctx.guild.roles, id=848948041696542731)
        CHE=discord.utils.get(ctx.guild.roles, id=709346269491101757)
        ELS=discord.utils.get(ctx.guild.roles, id=899150508139376660)
        MUT=discord.utils.get(ctx.guild.roles, id=601992011838652427)
        if GOB in ctx.author.roles or TAE in ctx.author.roles or SOL in ctx.author.roles or CHE in ctx.author.roles or ELS in ctx.author.roles:
            await user.add_roles(MUT)
            await self.delarm(ctx=ctx, user=user)
            await self.deleff(ctx=ctx, user=user)
            await ctx.send(f"{user.mention} отправляется на позорный столб.")
        else:
            await ctx.send(f"{ctx.author.mention} отправляется на позорный столб на 0 секунд.")
            await ctx.send(f"{ctx.author.mention} отбыл своё наказание.")

    @commands.command()
    async def уборка(self, ctx, i: int = 1):
        GOB=discord.utils.get(ctx.guild.roles, id=583993057330855946)
        DES=discord.utils.get(ctx.guild.roles, id=903847910951751692)
        if GOB not in ctx.author.roles and DES not in ctx.author.roles:
            return await ctx.send(f"*{ctx.author.display_name} подметает полы.*")
        j=0
        async for mes in ctx.message.channel.history(limit=i,oldest_first=False):
            if not mes.pinned:
                await mes.delete()
                await asyncio.sleep(1.5)
                j+=1
        msg = await ctx.send(f"Удалено {j} сообщений.")

    @commands.command()
    async def амнистия(self, ctx, user: discord.Member = None):
        GOB=discord.utils.get(ctx.guild.roles, id=583993057330855946)
        TAE=discord.utils.get(ctx.guild.roles, id=602362721660305433)
        SOL=discord.utils.get(ctx.guild.roles, id=848948041696542731)
        CHE=discord.utils.get(ctx.guild.roles, id=709346269491101757)
        ELS=discord.utils.get(ctx.guild.roles, id=899150508139376660)
        MUT=discord.utils.get(ctx.guild.roles, id=601992011838652427)
        if GOB in ctx.author.roles or TAE in ctx.author.roles or SOL in ctx.author.roles or CHE in ctx.author.roles or ELS in ctx.author.roles:
            if MUT in user.roles:
                await user.remove_roles(MUT)
                await ctx.send(f"{user.mention} отбыл своё наказание.")
        else:
            await ctx.send(f"{ctx.author.mention} отправляется на позорный столб на 0 секунд.")
            await ctx.send(f"{ctx.author.mention} отбыл своё наказание.")

    @commands.command()
    async def напоминание(self, ctx: Context):
        msg = await ctx.send ("Напоминаю! :point_up_tone1:")
        msg0 = (":point_right_tone1: У кого нету роли фракции - может получить её, ткнув реакцию на канале <#675969784965496832>.")
        msg1 = (":point_right_tone1: Получить роль класса может любой желающий, отправив команду:\n`=выбрать класс`")
        msg2 = (":point_right_tone1: Если у вас есть роль <@&696014224442392717>, вы можете открыть его, отправив команду:\n`=сундук`")
        msg3 = ("Основные команды, что нужно знать:\n`=баланс`\n`=уровень`\nи\n`=книга анклава`")
        try:
            await msg.add_reaction("\N{CROSS MARK}")
            await msg.add_reaction("<:Lantern:609362645992341515>")
            await msg.add_reaction("<:Scrolls:625192051042156565>")
            await msg.add_reaction("<:zGold:620315740993617920>")
            await msg.add_reaction("<:zCandle:620973875714588673>")
        except discord.errors.Forbidden:
            return
        pred = ReactionPredicate.same_context(msg, ctx.author)
        try:
            react, user = await self.bot.wait_for("reaction_add", check=pred, timeout=300)
        except asyncio.TimeoutError:
            return
        if str(react.emoji) == "<:Lantern:609362645992341515>":
            await msg.edit(content=msg0)
        if str(react.emoji) == "<:Scrolls:625192051042156565>":
            await msg.edit(content=msg1)
        if str(react.emoji) == "<:zGold:620315740993617920>":
            await msg.edit(content=msg2)
        if str(react.emoji) == "<:zCandle:620973875714588673>":
            await msg.edit(content=msg3)
        if str(react.emoji) == "\N{CROSS MARK}":
            return await msg.delete()
        await msg.clear_reactions()

    @commands.group(name="зов", autohelp=False)
    async def зов(self, ctx: commands.GuildContext):
        pass

    @зов.command(name="стихий")
    @commands.cooldown(1, 3600, commands.BucketType.user)#server
    async def зов_стихий(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        author=ctx.author
        x=random.randint(1, 7)
        x1=random.randint(1, 10)
        if x==1:
             if x1<10:
                msg=discord.Embed(title="Повелитель огня Рагнарос в ярости!", description="Как ты смеешь взывать ко мне?! УМРИ, НАСЕКОМОЕ!!! *У вас сгорает {x2} золотых монет, у {user2} сгорает {x3} золотых монет.*".format(x2=10-x1, user2=random.choice(ctx.message.guild.members).display_name, x3=random.randint(1, 5)), colour=discord.Colour.red())
                msg.set_author(name="{author.display_name} делает подношение тотему огня на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
                msg.set_thumbnail(url="https://vignette.wikia.nocookie.net/wow/images/e/e2/Ragnaros_the_Firelord.png/revision/latest/scale-to-width-down/340?cb=20131027083613&path-prefix=ru")
             else:
                msg=discord.Embed(title="Повелитель огня Рагнарос доволен!".format(author=ctx.author, x1=x1), description="Восстань, слуга пламени! Поглоти их плоть! *Повелитель огня назначает вас своим мажордомом.*", colour=discord.Colour.dark_red())
                msg.set_author(name="{author.display_name} делает подношение тотему огня на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
                msg.set_thumbnail(url="https://vignette.wikia.nocookie.net/wow/images/e/e2/Ragnaros_the_Firelord.png/revision/latest/scale-to-width-down/340?cb=20131027083613&path-prefix=ru")
        if x==2:
             msg=discord.Embed(title="Повелитель огня Пеплорон обращает на вас свой взор!".format(author=ctx.author, x1=x1), description="На колени, смертный! *Пеплорон сжигает {x1} золотых монет у {user.display_name}.*".format(x1=x1, user=user), colour=discord.Colour.orange())
             msg.set_author(name="{author.display_name} делает подношение тотему огня на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
             msg.set_thumbnail(url="https://wow.zamimg.com/uploads/screenshots/normal/660184-.jpg")
        if x==3:
             msg=discord.Embed(title="Герцог Гидраксис в ярости!".format(author=ctx.author, x1=x1), description="Как ты смеешь взывать ко мне?! Умри, насекомое!!!", colour=discord.Colour.blue())
             msg.set_author(name="{author.display_name} делает подношение тотему воды на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
             msg.set_thumbnail(url="https://wow.zamimg.com/modelviewer/live/webthumbs/npc/246/58870.png")
        if x==4:
             msg=discord.Embed(title="Повелитель воды Нептулон в ярости!".format(author=ctx.author, x1=x1), description="Нерадивое сухопутное! Ты решил потревожить владыку вод?! Почувствуй силу чистой воды!!!", colour=discord.Colour.dark_blue())
             msg.set_author(name="{author.display_name} делает подношение тотему воды на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
             msg.set_thumbnail(url="https://wow.blizzwiki.ru/images/thumb/9/95/Neptulon.jpg/200px-Neptulon.jpg")
        if x==5:
             msg=discord.Embed(title="Повелитель воздуха Громораан в ярости!".format(author=ctx.author, x1=x1), description="Я дарую тебе силу ветров!", colour=0xD0D0D0)
             msg.set_author(name="{author.display_name} делает подношение тотему воздуха на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
             msg.set_thumbnail(url="https://wow.zamimg.com/uploads/screenshots/small/683871.jpg")
        if x==6:
             msg=discord.Embed(title="Повелитель воздуха Алакир в ярости!".format(author=ctx.author, x1=x1), description="Жалкий смертный, твои попытки приводят меня в ЯРОСТЬ!!!", colour=0x808080)
             msg.set_author(name="{author.display_name} делает подношение тотему воздуха на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
             msg.set_thumbnail(url="https://vignette.wikia.nocookie.net/wow/images/3/37/Al%27Akir_the_Windlord_TCG.jpg/revision/latest/scale-to-width-down/340?cb=20131018201518&path-prefix=ru")
        if x==7:
             if x1<6:
                msg=discord.Embed(title="Теразан в ярости!".format(author=ctx.author, x1=x1), description="Смертные погубили моё дитя! Почувствуй же мой гнев!", colour=discord.Colour.gold())
                msg.set_author(name="{author.display_name} делает подношение тотему земли на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
                msg.set_thumbnail(url="https://rpwiki.ru/images/thumb/d/d6/Теразан.jpg/250px-Теразан.jpg")
             else:
                msg=discord.Embed(title="Теразан удовлетворена!".format(author=ctx.author, x1=x1), description="Ты решил потревожить мать-скалу? Получи моё благославение.", colour=discord.Colour.dark_gold())
                msg.set_author(name="{author.display_name} делает подношение тотему земли на {x1} золотых монет.".format(author=ctx.author, x1=x1), url=author.avatar_url, icon_url=author.avatar_url)
                msg.set_thumbnail(url="https://rpwiki.ru/images/thumb/d/d6/Теразан.jpg/250px-Теразан.jpg")
        await ctx.send (embed=msg)

    @commands.command()
    async def счета(self, ctx: commands.Context, top: int = 10, show_global: bool = False):
        guild = ctx.guild
        author = ctx.author
        embed_requested = await ctx.embed_requested()
        footer_message = "Страница {page_num}/{page_len}."
        max_bal = await bank.get_max_balance(ctx.guild)

        if top < 1:
            top = 10

        base_embed = discord.Embed(title="Список богатеищ.")
        if await bank.is_global() and show_global:
            bank_sorted = await bank.get_leaderboard(positions=top, guild=None)
            base_embed.set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.avatar_url)
        else:
            bank_sorted = await bank.get_leaderboard(positions=top, guild=guild)
            if guild:
                base_embed.set_author(name=guild.name, icon_url=guild.icon_url)

        try:
            bal_len = len(humanize_number(bank_sorted[0][1]["balance"]))
            bal_len_max = len(humanize_number(max_bal))
            if bal_len > bal_len_max:
                bal_len = bal_len_max
        except IndexError:
            return await ctx.send("There are no accounts in the bank.")
        pound_len = len(str(len(bank_sorted)))
        header = "{pound:{pound_len}}{score:{bal_len}}{name:2}\n".format(
            pound="#",
            name="Имя",
            score="Счёт",
            bal_len=bal_len + 6,
            pound_len=pound_len + 3,
        )
        highscores = []
        pos = 1
        temp_msg = header
        for acc in bank_sorted:
            try:
                name = guild.get_member(acc[0]).display_name
            except AttributeError:
                user_id = ""
                if await ctx.bot.is_owner(ctx.author):
                    user_id = f"({str(acc[0])})"
                name = f"{acc[1]['name']} {user_id}"

            balance = acc[1]["balance"]
            if balance > max_bal:
                balance = max_bal
                await bank.set_balance(MOCK_MEMBER(acc[0], guild), balance)
            balance = humanize_number(balance)
            if acc[0] != author.id:
                temp_msg += (
                    f"{f'{humanize_number(pos)}.': <{pound_len+2}} "
                    f"{balance: <{bal_len + 5}} {name}\n"
                )

            else:
                temp_msg += (
                    f"{f'{humanize_number(pos)}.': <{pound_len+2}} "
                    f"{balance: <{bal_len + 5}} "
                    f"<<{author.display_name}>>\n"
                )
            if pos % 10 == 0:
                if embed_requested:
                    embed = base_embed.copy()
                    embed.description = box(temp_msg, lang="md")
                    embed.set_footer(
                        text=footer_message.format(
                            page_num=len(highscores) + 1,
                            page_len=ceil(len(bank_sorted) / 10),
                        )
                    )
                    highscores.append(embed)
                else:
                    highscores.append(box(temp_msg, lang="md"))
                temp_msg = header
            pos += 1

        if temp_msg != header:
            if embed_requested:
                embed = base_embed.copy()
                embed.description = box(temp_msg, lang="md")
                embed.set_footer(
                    text=footer_message.format(
                        page_num=len(highscores) + 1,
                        page_len=ceil(len(bank_sorted) / 10),
                    )
                )
                highscores.append(embed)
            else:
                highscores.append(box(temp_msg, lang="md"))

        if highscores:
            await menu(
                ctx,
                highscores,
                DEFAULT_CONTROLS if len(highscores) > 1 else {"\N{CROSS MARK}": close_menu},
            )
        else:
            await ctx.send("Усё пропало.")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def ставка(self, ctx: commands.Context, bid=None):
        if ctx.message.channel.id != 684600533834792996:
            return await ctx.send("Здесь вам не тут!\nИди заниматься подобным в <#684600533834792996>.")
        FRY=self.bot.get_emoji(675570659975495698)
        ONE=self.bot.get_emoji(618806054268043305)
        TOP=self.bot.get_emoji(660098359012360214)
        COIN=self.bot.get_emoji(624216995784687657)
        KEK=self.bot.get_emoji(609362609983979520)
        GOBL=self.bot.get_emoji(732588769567440956)
        GOLD=self.bot.get_emoji(620315740993617920)
        NEED=self.bot.get_emoji(605429832007942174)
        MUR=self.bot.get_emoji(620973875219529788)
        OGR=self.bot.get_emoji(620973875714457600)
        roll=[FRY, ONE, TOP, COIN, KEK, GOBL, GOLD, NEED, MUR, OGR]
        if bid==None:
            return await ctx.send("Нужно больше золота!")
        try:
            bid=int(bid)
        except ValueError:
            return await ctx.send("Мы такое не принимаем. Убери это подальше от меня.")
        author=ctx.author
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if bid>authbal or bid<=0:
            return await ctx.send("Нужно больше золота!")
        P1=random.choice(roll)
        P2=random.choice(roll)
        P3=random.choice(roll)
        P4=random.choice(roll)
        P5=random.choice(roll)
        P6=random.choice(roll)
        P7=random.choice(roll)
        P8=random.choice(roll)
        P9=random.choice(roll)
        embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', color = discord.Colour.random())
        msg=await ctx.send(f"{P1}{P2}{P3}\n{P4}{P5}{P6}\n{P7}{P8}{P9}")
        msg1=await ctx.send(embed=embed)
        await bank.withdraw_credits(author, bid)
        i=0
        j=random.randint(8, 10)
        while i<j:
            await asyncio.sleep(0.85) 
            if i<=4:
                P7=P4
                P4=P1
                P1=random.choice(roll)
            if i>=4:
                P1="⬇"
                P7="⬆"
            if i<=6:
                P8=P5
                P5=P2
                P2=random.choice(roll)
            if i>=6:
                P2="⬇"
                P8="⬆"
            P9=P6
            P6=P3
            i+=1
            if i==(j-1) and authbal<200:
                roll1=[P4, P5]
                P3=random.choice(roll1)
            else:
                P3=random.choice(roll)
            if i==j:
                P3="⬇"
                P9="⬆"
            await msg.edit(f"{P1}{P2}{P3}\n{P4}{P5}{P6}\n{P7}{P8}{P9}")
        if P4==P5 and P5==P6:
            if P5==GOLD:
                bid1=bid*50
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"НЕБЫВАЛАЯ УДАЧКА - ДЖЕКПОТ!!! *В зал казино вносят три золотых сундука!* Ставка умножается на 50!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==TOP:
                bid1=bid*25
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Легендарная тройка! Не обошлось без подкрутки! Ставка умножается на 25!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==COIN:
                bid1=bid*20
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Три мешка с золотом, какое прекрасное бремя! Ставка умножается на 20!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==FRY:
                bid1=bid*10
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Заткнись и бери мои деньги! Ставка умножается на 10!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==ONE:
                bid1=bid*10
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"*Игровой автомат клинит, и {author.display_name} одним ударом выбивает из него {bid1} золотых монет!*\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==KEK:
                bid1=bid*10
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Орочий смех заразен, как красная оспа! Ставка умножается на 10!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==GOBL:
                bid1=bid*10
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"*Игровой автомат начинает подозрительно тикать!* Ставка умножается на 10!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==NEED:
                bid1=bid*10
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Наш рудник скоро иссякнет! Ставка умножается на 10!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==OGR:
                bid1=bid*10
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Горианская империя пала жертвой азарта. Ставка умножается на 10!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==MUR:
                bid1=bid*10
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Мрглглглгл! <Пора сходить на рыбалку!> Ставка умножается на 10!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            return await msg1.edit(embed=embed)
        elif P4==P5 or P5==P6:
            if P5==GOLD:
                bid1=bid*4
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Неплохо сыграно! Два золотых сундука! Ставка умножается на 4!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==TOP:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Легендарная карта! Встречается один раз на 40 ставок! Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==COIN:
                bid1=bid*3
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"ЗОЛОТАЯ ЖИЛА!!! Ставка умножается на 3!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==FRY:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Кто-то бросал деньги в экран игрового автомата. Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==ONE:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Скидка на услуги парикмахера! Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==KEK:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Хочешь рассмешить орка - расскажи ему о своих планах наступления! Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==GOBL:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Бесплатный напиток за счёт заведения! Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==NEED:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Склоняюсь перед вашей волей! Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==OGR:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Одна голова - хорошо, а две - уже огр-маг! Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            elif P5==MUR:
                bid1=bid*2
                if (authbal+bid1)>max_bal:
                    bid1=max_bal-authbal
                await bank.deposit_credits(author, bid1)
                newbal=await bank.get_balance(author)
                embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"Мргл мргл! <Звучит весёлая песенка.> Ставка умножается на 2!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            return await msg1.edit(embed=embed)
        else:
            bid1=0
            newbal=await bank.get_balance(author)
            embed=discord.Embed(title = f'*{author.display_name} бросает в автомат {bid} золотых монет.*', description = f"И ничего не получает!\n{authbal} - {bid} (Ставка) + {bid1} (Выигрыш) → {newbal}!", color = discord.Colour.random())
            return await msg1.edit(embed=embed)

    async def getart(self, ctx: commands.GuildContext, art: int):
        artj=discord.utils.get(ctx.guild.roles, id=893293699704975360)
        artv=discord.utils.get(ctx.guild.roles, id=893294216036360242)
        oldart=0
        if art==0:
            while oldart<1000:
                if artj.name=="Артефакты: "+str(oldart):
                    return await artj.edit(name="Артефакты: "+str(oldart+1))
                oldart+=1
        else:
            while oldart<1000:
                if artv.name=="Артефакты: "+str(oldart):
                    return await artv.edit(name="Артефакты: "+str(oldart+1))
                oldart+=1
    
    async def chkrank(self, ctx: commands.GuildContext, user: discord.Member) -> int:
        R0=discord.utils.get(ctx.guild.roles, id=687903691587846158)#от Ученика 1
        R1=discord.utils.get(ctx.guild.roles, id=696008498764578896)#2
        R2=discord.utils.get(ctx.guild.roles, id=687903789457735680)#3
        R3=discord.utils.get(ctx.guild.roles, id=696008500240973885)#4
        R4=discord.utils.get(ctx.guild.roles, id=687903789843218457)#5
        R5=discord.utils.get(ctx.guild.roles, id=696008502497378334)#6
        R6=discord.utils.get(ctx.guild.roles, id=687903807405162506)#7
        R7=discord.utils.get(ctx.guild.roles, id=696008504153997322)#8
        R8=discord.utils.get(ctx.guild.roles, id=687903808268927002)#9
        R9=discord.utils.get(ctx.guild.roles, id=687904030713708575)#до Эксперта 10
        ret=0
        for R in R0, R1, R2, R3, R4, R5, R6, R7, R8, R9:
            ret+=1
            if R in user.roles:
                return ret #возврат от 1 до 10
        return 0

    async def getrank(self, ctx: commands.GuildContext, user: discord.Member):
        rank=await self.chkrank(ctx=ctx, user=user)
        R0=discord.utils.get(ctx.guild.roles, id=687903691587846158)
        R1=discord.utils.get(ctx.guild.roles, id=696008498764578896)
        R2=discord.utils.get(ctx.guild.roles, id=687903789457735680)
        R3=discord.utils.get(ctx.guild.roles, id=696008500240973885)
        R4=discord.utils.get(ctx.guild.roles, id=687903789843218457)
        R5=discord.utils.get(ctx.guild.roles, id=696008502497378334)
        R6=discord.utils.get(ctx.guild.roles, id=687903807405162506)
        R7=discord.utils.get(ctx.guild.roles, id=696008504153997322)
        R8=discord.utils.get(ctx.guild.roles, id=687903808268927002)
        R9=discord.utils.get(ctx.guild.roles, id=687904030713708575)
        i=0
        if rank==8 or rank==9:
            x=random.randint(1, rank)
            if x>3:
                userbal=await bank.get_balance(user)
                max_bal=await bank.get_max_balance(guild=getattr(user, "guild", None))
                heal=random.randint(400, 500)
                if userbal>(max_bal-heal):
                    heal=(max_bal-userbal)
                await bank.deposit_credits(user, heal)
                return await ctx.send (f"Сожалею, но сегодня я ничему не смогу тебя научить. Прими {heal} золотых монет качестве утешения.")
        for R in R0, R1, R2, R3, R4, R5, R6, R7, R8, R9:
            if R in user.roles and i<9:
                await user.remove_roles(R)
            if i==rank:
                await user.add_roles(R)
                return await ctx.send (f"*{user.display_name} получает ранг мастерства {R}.*")
            i+=1
        if rank==10:
            userbal=await bank.get_balance(user)
            max_bal=await bank.get_max_balance(guild=getattr(user, "guild", None))
            heal=random.randint(400, 500)
            if userbal>(max_bal-heal):
                heal=(max_bal-userbal)
            await bank.deposit_credits(user, heal)
            return await ctx.send (f"*{user.display_name} достигает максимального ранга мастерства в своём классе, за что получает премию в размере {heal} золотых монет.*")
    
    async def buffexp(self, ctx, user: discord.Member, exp: int):
        lvl = await self.profiles._get_level(user)
        oldxp = await self.profiles.data.member(user).exp()
        lvlup = await self.profiles.givexp(lvl)
        lvldown = await self.profiles.givexp(lvl-1)
        if (oldxp + exp) >= lvlup:
            exp = lvlup - oldxp - 1
        elif oldxp + exp < lvldown:
            exp = lvldown - oldxp
        await self.profiles._give_exp(user, exp)
        return abs(exp)
        
    async def delarm(self, ctx: commands.GuildContext, user: discord.Member):
        for r in user.roles:
            if r.name.startswith("🛡️"):
                await user.remove_roles(r)
        await ctx.send (f"*{user.display_name} теряет все защитные чары.*")

    async def getarm(self, user: discord.Member, role: discord.Role):
        for r in user.roles:
            if r.name.startswith("🛡️"):
                await user.remove_roles(r)
        await user.add_roles(role)
        
    async def getpet(self, user: discord.Member, role: discord.Role):
        for r in user.roles:
            if "Питомец" in r.name:
                await user.remove_roles(r)
        await user.add_roles(role)

    async def getfood(self, ctx: commands.GuildContext, user: discord.Member):
        BUL=discord.utils.get(ctx.guild.roles, id=772380354803793920)
        PLU=discord.utils.get(ctx.guild.roles, id=772380359454490624)
        BIS=discord.utils.get(ctx.guild.roles, id=772380362927636500)
        for r in user.roles:
            if "Пища" in r.name:
                await user.remove_roles(r)
        for r in BUL, PLU, BIS:
            await user.add_roles(r)
    
    async def deleff(self, ctx: commands.GuildContext, user: discord.Member):
        for r in user.roles:
            if r.name.startswith("🛡️"):
                await user.remove_roles(r)
        for r in user.roles:
            if r.name.startswith("Эффект"):
                await user.remove_roles(r)
        for r in user.roles:
            if r.name.startswith("Питомец"):
                await user.remove_roles(r)
        for r in user.roles:
            if r.name.startswith("Контракт"):
                await user.remove_roles(r)
        await ctx.send (f"*{user.display_name} теряет все действующие чары.*")

    async def zadd(self, who: discord.Member, give):
        await who.add_roles(give)

    @commands.group(name="боевой", autohelp=False)
    async def боевой(self, ctx: commands.GuildContext):
        pass

    @боевой.command(name="крик")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def боевой_крик(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724787397361695)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается крикнуть что-то боевое, но лишь хрипит и кашляет.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=40
        if authbal<cst:
            return await ctx.send (f"*У {author.display_name} слёзы наворачиваются на глазах при виде {authbal} золотых монет у себя на счету.*")
        heal=random.randint(20, 30)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} кричит так, что у {user.mention} на счету прибавляется {heal} золотых монет!*")

    @commands.command()
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def сокрушение(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724787397361695)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} замахивается, но теряет равновесие и падает.*\nХа-ха!")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=180
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} пересчитывает {authbal} золотых монет в кошельке и передумывает лезть в драку.*")
        dmg=random.randint(250, 260)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} обрушивает на {user.mention} мощный удар. Бедняга теряет {dmg} золотых монет!*")

    @commands.group(name="глухая", autohelp=False)
    async def глухая(self, ctx: commands.GuildContext):
        pass

    @глухая.command(name="оборона")
    async def глухая_оборона(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724787397361695)
        ARM=discord.utils.get(ctx.guild.roles, id=765245696047317002)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} укрывается за огромным бумажным щитом. Через секунду щит уносит ветром.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} пытается поднять щит с земли, но не может подцепить его край.*\nПозови на помощь подмастерье!")
        authbal=await bank.get_balance(author)
        cst=200
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} растеряно смотрит по сторонам в поисках {cst-authbal} монет.*")
        await bank.withdraw_credits(author, cst)
        await self.getarm(user=author, role=ARM)
        await ctx.send (f"*{author.display_name} укрывается за огромным щитом.*")

    @commands.command()
    async def провокация(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724787397361695)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} вежливо предлагает {user.display_name} носовой платок.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} молча буравит взглядом {user.display_name}. Кажется кто-то затаил обиду.*")
        authbal=await bank.get_balance(author)
        cst=170
        if authbal<cst:
            return await ctx.send (f"*У {author.display_name} закончились перчатки для бросания, надо закупить новых.*\nС тебя {cst} монет.")
        await bank.withdraw_credits(author, cst)
        await ctx.send(f"*{author.display_name} с размаху бросает латную перчатку в лицо {user.display_name}, вызывая на честный поединок.*")
        await self.delarm(ctx=ctx, user=user)
        await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
        await user.edit(reason=get_audit_reason(ctx.author, None), nick="😡 Сгусток ярости")

    @commands.command()
    async def исступление(self, ctx, user: discord.Member = None):
        author = ctx.author
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        ARM=discord.utils.get(ctx.guild.roles, id=765245696047317002)
        rank=await self.chkrank(ctx=ctx, user=author)
        if ARM not in author.roles or rank<=3:
            return await ctx.send(f"*{author.display_name} чувствует себя слишком уязвимым для боя.*")
        x=random.randint(1, 4)
        if x>2:
            await author.remove_roles(ARM)
            await ctx.send(f"*{author.display_name} отбрасывает щит в сторону и бежит на {user.display_name}, яростно крича!*")
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            return await user.edit(reason=get_audit_reason(ctx.author, None), nick="😡 Сгусток ярости")
        await ctx.send(f"*{author.display_name} делает выпад, толкая щитом {user.display_name}, и провоцируя на ближний бой.*")
        await self.delarm(ctx=ctx, user=user)
        await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
        await user.edit(reason=get_audit_reason(ctx.author, None), nick="😡 Сгусток ярости")

    @commands.group(name="ободряющий", autohelp=False)
    async def ободряющий(self, ctx: commands.GuildContext):
        pass

    @ободряющий.command(name="клич")
    @commands.cooldown(3, 86400, commands.BucketType.user)
    async def ободряющий_клич(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724787397361695)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается подобрать ободряющие слова, но в голову ничего не идёт.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} пытается крикнуть что-то ободряющее, но случайно оскорбляет всех вокруг.*\nТы явно не мастер произносить речи.")
        authbal=await bank.get_balance(author)
        cst=150
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} грустно смотрит на свой баланс, где всего {authbal} золотых монет.*")
        xp=await self.buffexp(ctx, user, 15)
        await bank.withdraw_credits(author, cst)
        await ctx.send (f"*{author.display_name} воодушевляющим кличем придаёт {user.mention} сил на {xp} единиц опыта!*")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def казнь(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724787397361695)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} замахивается для смертельного удара, но вспоминает, что с утра и крошки во рту не было, и падает в голодный обморок.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{user.display_name} обладает недюженной силой. Победить в этом бою может лишь магистр воинских искусств!*")
        authbal=await bank.get_balance(author)
        targbal=await bank.get_balance(user)
        if authbal<targbal:
            return await ctx.send (f"*{author.display_name} растеряно смотрит по сторонам в поисках своего оружия и мешочка с {targbal-authbal} золотыми монетами.*")
        await bank.withdraw_credits(author, targbal)
        await bank.withdraw_credits(user, targbal)
        await ctx.send (f"*-УМРИ!!! – кричит {author.display_name} и наносит смертельный удар {user.mention}. Вместе с кровью утекают {targbal} золотых монет.*")

    @commands.group(name="прицельный", autohelp=False)
    async def прицельный(self, ctx: commands.GuildContext):
        pass

    @прицельный.command(name="выстрел")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def прицельный_выстрел(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} швыряется камушками. Выглядит забавно.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=90
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} нащупывает пустоту вместо боеприпасов. Нужно ещё {cst-authbal} золотых монет для пополнения запасов.*")
        dmg=random.randint(120, 130)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} поражает {user.mention} прямо в глаз. Боль уносит {dmg} золотых монет.*")

    @commands.group(name="морозная", autohelp=False)
    async def морозная(self, ctx: commands.GuildContext):
        pass

    @морозная.command(name="ловушка")
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def морозная_ловушка(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается взвести капкан, но прищемляет себе палец.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        slw=ctx.channel.slowmode_delay
        if slw>=900:
            return await ctx.send ("*Здесь действуют более мощные чары, даже капкан некуда поставить.*")
        authbal=await bank.get_balance(author)
        cst=240
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} проверяет направление ветра и состояние своего кошелька. Ветер юго-западный, а в кошельке всего {authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        await ctx.send (f"*{author.display_name} бросает на землю морозную ловушку!*\nНикому не двигаться, или примёрзнете на 15 минут!")
        await ctx.channel.edit(slowmode_delay=900)

    @commands.group(name="контузящий", autohelp=False)
    async def контузящий(self, ctx: commands.GuildContext):
        pass

    @контузящий.command(name="выстрел")
    async def контузящий_выстрел(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        MUT=discord.utils.get(ctx.guild.roles, id=687886232336072741)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} заглядывает в дуло заряженного мушкета.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{user.display_name} - сильный враг, с ног так просто не свалить.*\nМожет подмастерье поможет?")
        authbal=await bank.get_balance(author)
        cst=210
        if authbal<cst:
            return await ctx.send (f"*Материальное положение {author.display_name} весьма печально - всего {authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=MUT)
        await ctx.send(f"*{author.display_name} производит выстрел, который подобно взрыву оглушает {user.mention}. Кажется это серьёзно.*")
            
    @commands.group(name="призыв", autohelp=False)
    async def призыв(self, ctx: commands.GuildContext):
        pass

    @призыв.command(name="медведя")
    async def призыв_медведя(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        PET=discord.utils.get(ctx.guild.roles, id=687887026808291338)
        KTZ=discord.utils.get(ctx.guild.roles, id=688044643052421127)
        UNDEAD=discord.utils.get(ctx.guild.roles, id=687901221645975636)
        if KTZ in author.roles:
            return await ctx.send("*Мистер Бигглсуорт закатывает ярко-синие глазки и урчит.*")
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} в ужасе убегает от огромного злого медведя.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} с тоской смотрит на убегающего медведя.*\nНужно больше тренироваться в искусстве приручения.")
        authbal=await bank.get_balance(author)
        cst=160
        if authbal<cst:
            return await ctx.send (f"*Прокормить медведя весьма сложно - нужно накопить ещё {cst-authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        if UNDEAD in author.roles:
            await self.zadd(who=author, give=KTZ)
            return await ctx.send(f"*Прищурив ярко-синие глазки, мистер Бигглсуорт примостился на холодных коленках у {author.display_name}.*\nЕго так просто не прогнать.")
        await self.getpet(user=author, role=PET)
        await self.getarm(user=author, role=PET)
        await ctx.send(f"*Верный друг присоединяется к {author.display_name}.*")
            
    @призыв.command(name="волка")
    async def призыв_волка(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        PET=discord.utils.get(ctx.guild.roles, id=687887153878925334)
        KTZ=discord.utils.get(ctx.guild.roles, id=688044643052421127)
        UNDEAD=discord.utils.get(ctx.guild.roles, id=687901221645975636)
        if KTZ in author.roles:
            return await ctx.send("*Мистер Бигглсуорт закатывает ярко-синие глазки и урчит.*")
        if CLS not in author.roles:
            await ctx.send (f"*-Волки! Волки! - кричит {author.display_name}, но никто в это не верит.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*Сколько волка не корми, он всё смотрит на {author.display_name}.*\nНужно больше тренироваться в искусстве приручения.")
        authbal=await bank.get_balance(author)
        cst=160
        if authbal<cst:
            return await ctx.send (f"*У волков воистину волчий аппетит - не хватило буквально {cst-authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        if UNDEAD in author.roles:
            await self.zadd(who=author, give=KTZ)
            return await ctx.send(f"*Прищурив ярко-синие глазки, мистер Бигглсуорт примостился на холодных коленках у {author.display_name}.*\nЕго так просто не прогнать.")
        await self.getpet(user=author, role=PET)
        await ctx.send(f"*Опасный зверь теперь лучший друг для {author.display_name}.*")

    @призыв.command(name="воронов")
    async def призыв_воронов(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        PET=discord.utils.get(ctx.guild.roles, id=692695614596841513)
        KTZ=discord.utils.get(ctx.guild.roles, id=688044643052421127)
        UNDEAD=discord.utils.get(ctx.guild.roles, id=687901221645975636)
        if KTZ in author.roles:
            return await ctx.send("*Мистер Бигглсуорт закатывает ярко-синие глазки и урчит.*")
        if CLS not in author.roles:
            await ctx.send (f"*Стая злых птиц явно охотится за {author.display_name}.*\nСоветую спрятаться.")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} залезает на столб и громко каркает.*\nЭх, нужно больше тренироваться в искусстве приручения.")
        authbal=await bank.get_balance(author)
        cst=160
        if authbal<cst:
            return await ctx.send (f"*Чтобы приманить целую стаю воронов, потребуется ещё не меньше {cst-authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        if UNDEAD in author.roles:
            await self.zadd(who=author, give=KTZ)
            return await ctx.send(f"*Прищурив ярко-синие глазки, мистер Бигглсуорт примостился на холодных коленках у {author.display_name}.*\nЕго так просто не прогнать.")
        await self.getpet(user=author, role=PET)
        await ctx.send(f"*Теперь над {author.display_name} вьётся стая голодных воронов, ожидая приказа.*")
            
    @commands.group(name="команда", autohelp=False)
    async def команда(self, ctx: commands.GuildContext):
        pass

    @команда.command(name="взять")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def команда_взять(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        PETB=discord.utils.get(ctx.guild.roles, id=687887026808291338)
        PETW=discord.utils.get(ctx.guild.roles, id=687887153878925334)
        PETR=discord.utils.get(ctx.guild.roles, id=692695614596841513)
        KTZ=discord.utils.get(ctx.guild.roles, id=688044643052421127)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} отдаёт приказ, но {user.display_name} почему-то не слушается.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if PETB in author.roles:
            dmg=random.randint(75, 85)
            dmg1=random.randint(75, 85)
            user1=random.choice(ctx.message.guild.members)
            while user1 is author:
                user1 = random.choice(ctx.message.guild.members)
            targbal=await bank.get_balance(user)
            targ1bal=await bank.get_balance(user1)
            if targbal<dmg:
                dmg=targbal
            if targ1bal<dmg1:
                dmg1=targ1bal
            await bank.withdraw_credits(user, dmg)
            await bank.withdraw_credits(user1, dmg1)
            await author.remove_roles(PETB)
            await ctx.send(f"*Медведь ревёт и яростно машет лапами. Попав под удары {user.mention} и {user1.mention}, теряют {dmg} и {dmg1} золотых монет, соответственно.*")
        elif PETW in author.roles:
            targbal=await bank.get_balance(user)
            dmg=targbal//100
            await bank.withdraw_credits(user, dmg)
            await author.remove_roles(PETW)
            await ctx.send(f"*Волк кусает {user.mention} за пятую точку. От боли и неожиданности {user.display_name} теряет {dmg} золотых монет.*")
        elif PETR in author.roles:
            slw=ctx.channel.slowmode_delay
            if slw>=60:
                return await ctx.send ("*Здесь действуют более мощные чары.*")
            await ctx.channel.edit(slowmode_delay=60)
            await author.remove_roles(PETR)
            await ctx.send("*Стая воронов бросается на всех подряд. Сказать что-либо удаётся лишь раз в 1 минуту.*")
        elif KTZ in author.roles:
            await ctx.send("*Мистер Бигглсуорт закатывает ярко-синие глазки и урчит.*")
        else:
            await ctx.send ("Ну и кому ты это сказал?!")
            
    @commands.group(name="притвориться", autohelp=False)
    async def притвориться(self, ctx: commands.GuildContext):
        pass

    @притвориться.command(name="мёртвым")
    async def притвориться_мёртвым(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} закатывает глаза и высовывает язык.*\nБеее!")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393 and ctx.message.channel.id != 610767915997986816:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> или в <#610767915997986816> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} театрально закрывает глаза и медленно сползает на землю, прощально махая рукой.*\nТебе бы поучиться у мастера.")
        authbal=await bank.get_balance(author)
        cst=260
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} случайно рассыпает монеты на землю. {cst-authbal} бесследно пропали!*")
        await bank.withdraw_credits(author, cst)
        if ctx.message.channel.id == 603151774009786393:
            await ctx.send (f"*{author.display_name} падает замертво.*\nГоворят судьбу не обманешь. Врут, собаки!")
        else:
            room=self.bot.get_channel(603151774009786393)
            await room.send(f"*{author.display_name} падает замертво.*\nГоворят судьбу не обманешь. Врут, собаки!\n*{author.display_name} теряет все действующие чары.*")
        await self.deleff(ctx=ctx, user=author)

    @commands.command()
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def шквал(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724790425649157)
        while user1 is None or user1 is author:
            user1 = random.choice(ctx.message.guild.members)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} направляет палец на {user1.display_name} и говорит: -Бабах!*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user2 is None or user2 is author or user2==user1:
            user2 = random.choice(ctx.message.guild.members) 
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} чертит что-то на земле, безуспешно пытаясь вычислить траекторию выстрела.*")
        authbal=await bank.get_balance(author)
        cst=3500
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} не идёт на конфликт, когда в кошельке меньше {cst} золотых монет.*")
        targ1bal=await bank.get_balance(user1)
        targ2bal=await bank.get_balance(user2)
        dmg1=3500+(targ1bal//10)
        dmg2=random.randint(1000, 1100)
        if targ1bal<dmg1:
            dmg1=targ1bal
        if targ2bal<dmg2:
            dmg2=targ2bal
        await bank.withdraw_credits(user1, dmg1)
        await bank.withdraw_credits(user2, dmg2)
        await bank.withdraw_credits(author, cst)
        await ctx.send (f"*{author.display_name} производит серию мощных выстрелов, которая прошибает {user1.mention} насквозь, вышибая {dmg1} золотых монет, а следом и {user2.mention}, нанося урон на {dmg2} золотых монет!*")

    @commands.group(name="держи", autohelp=False)
    async def держи(self, ctx: commands.GuildContext):
        pass

    @держи.command(name="долю")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def держи_долю(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724791914758147)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается разделить числа столбиком, но безуспешно.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        targbal=await bank.get_balance(user)
        cst=90
        if authbal<targbal:
            return await ctx.send (f"*{author.display_name} с жадностью смотрит на кошелёк {user.display_name}. С такими богатеями ещё и делиться?! Обойдутся!*")
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} ещё не обладает достаточной суммой для дележа.*")
        heal=random.randint(60, 70)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} делит добычу с {user.mention}, отсыпая {heal} золотых монет.*")
 
    @commands.group(name="обшаривание", autohelp=False)
    async def обшаривание(self, ctx: commands.GuildContext):
        pass

    @обшаривание.command(name="карманов")
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def обшаривание_карманов(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724791914758147)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} ведёт себя подозрительно. На всякий случай приготовили верёвку и позорный столб.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} пытается стянуть несколько монет, но {user.display_name} это замечает и ловит за наглую руку.*")
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        targbal=await bank.get_balance(user)
        dmg=random.randint(1, 110)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(user, dmg)
        if authbal>(max_bal-dmg):
            dmg=(max_bal-authbal)
        await bank.deposit_credits(author, dmg)
        await ctx.send (f"*{author.display_name} вытаскивает у {user.mention} из кармана {dmg} золотых монет.*")

    @commands.group(name="плащ", autohelp=False)
    async def плащ(self, ctx: commands.GuildContext):
        pass

    @плащ.command(name="теней")
    async def плащ_теней(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724791914758147)
        ARM=discord.utils.get(ctx.guild.roles, id=765245702888226896)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} прячется под дырявое одеяло.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393 and ctx.message.channel.id != 610767915997986816:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> или в <#610767915997986816> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=280
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} просит одолжить {cst-authbal} золотых монет на очень нужное дело!*")
        await bank.withdraw_credits(author, cst)
        if ctx.message.channel.id == 603151774009786393:
            await ctx.send (f"*{author.display_name} накидывает на голову тёмный капюшон плаща и исчезает в тени.*")
        else:
            room=self.bot.get_channel(603151774009786393)
            await room.send(f"*{author.display_name} накидывает на голову тёмный капюшон плаща и исчезает в тени.*\n*{author.display_name} теряет все действующие чары.*")
        await self.deleff(ctx=ctx, user=author)
        await self.getarm(user=author, role=ARM)

    @commands.group(name="по", autohelp=False)
    async def по(self, ctx: commands.GuildContext):
        pass

    @по.command(name="почкам")
    async def по_почкам(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724791914758147)
        MUT=discord.utils.get(ctx.guild.roles, id=687889161046327364)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} отрабатывает удары на манекене с лицом {user.display_name}.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} подкрадывается к {user.display_name}, но теряет цель из виду.*\nНужно больше практики!")
        authbal=await bank.get_balance(author)
        cst=220
        if authbal<cst:
            return await ctx.send (f"*У {author.display_name} нет сил, чтобы поднять руки.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=MUT)
        await ctx.send(f"*{author.display_name} появляется из ниоткуда и подлым ударом выводит {user.mention} из строя.*")

    @commands.command()
    async def ослепление(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724791914758147)
        MUT=discord.utils.get(ctx.guild.roles, id=687888806287769638)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} светит фонариком в лицо {user.display_name}.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} суёт руку в потайной карман с ослепляющим порошком, но нащупывает там дырку.*")
        authbal=await bank.get_balance(author)
        cst=240
        if authbal<cst:
            return await ctx.send (f"*Ослепляющий порошок закончился.*\n{author.display_name}, тебе нужно посетить торговца сомнительными товарами.")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=MUT)
        await ctx.send(f"*{author.display_name} бросает горсть ослепляющего порошка в глаза {user.mention}.*")

    @commands.group(name="маленькие", autohelp=False)
    async def маленькие(self, ctx: commands.GuildContext):
        pass

    @маленькие.command(name="хитрости")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def маленькие_хитрости(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724791914758147)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} задумывает коварный план, но держит его при себе.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} советует {user.display_name} вложить деньги в гоблинское казино. Звучит не очень выгодно.*")
        authbal=await bank.get_balance(author)
        cst=2800
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} даже с места не сдвинется, пока не найдёт ещё {cst-authbal} золотых монет.*")
        heal=random.randint(1800, 1900)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.deposit_credits(user, heal)
        per=random.randint(300, 1200)
        await bank.withdraw_credits(author, (cst-per))
        await ctx.send (f"*{author.display_name} помогает {user.mention} разжиться на {heal} золотых монет, не забывая прикарманить себе {per} монет за посредничество.*")

    @commands.group(name="знак", autohelp=False)
    async def знак(self, ctx: commands.GuildContext):
        pass

    @знак.command(name="природы")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def знак_природы(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724794586398761)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} лепит на ранку подорожник.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=50
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} чувствует природный дисбаланс на {cst-authbal} золотых монет.*")
        heal=random.randint(30, 40)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} делает пасс рукой и у {user.mention} над головой появляется символ лапки, символизирующий усиление на {heal} золотых монет!*")

    @commands.command()
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def взбучка(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724794586398761)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} плюёт на руки и засучивает рукава.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{user.display_name} грозно рычит, но не решается вступить в драку.*")
        authbal=await bank.get_balance(author)
        cst=110
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} ощущает истощение, нужно срочно пополнить силы на {cst-authbal} золотых монет.*")
        dmg=random.randint(140, 150)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} бьёт лапой {user.mention} по голове. {user.mention} теряет {dmg} золотых монет, но получает лёгкое сотрясение.*")

    @commands.command()
    async def сноходец(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724794586398761)
        BAF=discord.utils.get(ctx.guild.roles, id=686202649858670686)
        BES=discord.utils.get(ctx.guild.roles, id=687899248892706830)
        HOR=discord.utils.get(ctx.guild.roles, id=687898434341961749)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} кладёт ладошку под щеку и крепко засыпает.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} нужно достичь необходимого уровня друидизма, чтобы путешествовать по Изумрудному сну.*")
        authbal=await bank.get_balance(author)
        cst=200
        if authbal<cst:
            return await ctx.send (f"*Когда в кошельке есть {cst} золотых монет, тогда и спится крепче.*")
        await bank.withdraw_credits(author, cst)
        if BES in author.roles:
            await self.zadd(who=author, give=HOR)
            await ctx.send (f"*{author.display_name} попадает под власть Изумрудного кошмара!*\nНужно срочно вызволять!")
        else:
            await self.zadd(who=author, give=BAF)
            await ctx.send (f"*{author.display_name} закрывает глаза и погружается в Изумрудный сон.*")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def сновидение(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724794586398761)
        BAF=discord.utils.get(ctx.guild.roles, id=686202649858670686)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} видит во сне радугу.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if BAF not in author.roles:
            return await ctx.send (f"*{author.display_name} пытается грезит наяву, но ничего не выходит.*")
#        cur_time = calendar.timegm(ctx.message.created_at.utctimetuple())
#        next_payday = await self.config.user(author).next_payday()
#        if cur_time < next_payday:
#            dtime = self.display_time(next_payday - cur_time)
#            return await ctx.send(f"На сегодня достаточно. Следующий раз будет через {dtime}")
        amount=random.randint(50, 60)
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if authbal>(max_bal-amount):
            amount=(max_bal-authbal)
        await bank.deposit_credits(author, amount)
        xp=await self.buffexp(ctx, author, 10)
#        next_payday = cur_time + await self.config.PAYDAY_TIME()
#        await self.config.user(author).next_payday.set(next_payday)
        await ctx.send(f"Пребывая в Изумрудном сне, {author.display_name} наблюдает пророческое видение. Полезное знание позволяет усилиться на {amount} золотых монет и стать опытнее на {xp} единиц.")

    @commands.command()
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def обновление(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724794586398761)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} призывает силы природы, но они чего-то не призываются.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} ещё не является мастером исцеления ран.*")
        authbal=await bank.get_balance(author)
        cst=4500
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} перетряхивает кошелёк, в котором болтается всего {authbal} золотых монет.*")
        heal=random.randint(3000, 3100)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} призывает силы природы, которые исцеляют {user.mention} на {heal} золотых монет!*")
        tic=random.randint(1, 9)
        while tic<10:
            tic+=random.randint(3, 10)
            targbal=await bank.get_balance(user)
            if (targbal+500)>=max_bal:
                return
            await asyncio.sleep(30)
            heal1=random.randint(495, 505)
            await bank.deposit_credits(user, heal1)
            await ctx.send (f"*Cилы природы исцеляют {user.mention} ещё на {heal1} золотых монет!*")

    @commands.group(name="железный", autohelp=False)
    async def железный(self, ctx: commands.GuildContext):
        pass

    @железный.command(name="мех")
    async def железный_мех(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724794586398761)
        ARM=discord.utils.get(ctx.guild.roles, id=765245704007319563)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} надевает шестяные носки и залазит под плед.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=160
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} чувствует голод. А в кошельке всего лишь {authbal} монет.*")
        await bank.withdraw_credits(author, cst)
        await self.getarm(user=author, role=ARM)
        await ctx.send (f"*{author.display_name} обращается в могучего зверя, покрываясь жёстким мехом.*")

    @commands.group(name="гнев", autohelp=False)
    async def гнев(self, ctx: commands.GuildContext):
        pass

    @гнев.command(name="деревьев")
    async def гнев_деревьев(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724794586398761)
        MUT=discord.utils.get(ctx.guild.roles, id=687894891237605376)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} изображает злого древня.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} слышит зов леса, но может на него ответить.*")
        authbal=await bank.get_balance(author)
        cst=230
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} просит пожертвовать на защиту деревьев {cst-authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=MUT)
        await ctx.send(f"*{author.display_name} призывает дикую лозу, чтобы опутать {user.mention} с ног до головы.*")

    @commands.group(name="молот", autohelp=False)
    async def молот(self, ctx: commands.GuildContext):
        pass

    @молот.command(name="гнева")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def молот_гнева(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} в гневе бросает на пол молоток и гвозди.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=100
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} качает головой, отмечая нехватку {cst-authbal} золотых монет для свершения правосудия.*")
        dmg=random.randint(120, 130)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} бросает свой молот в {user.mention}. Мощный удар заставляет {user.mention} потерять {dmg} золотых монет!*")

    @commands.group(name="свет", autohelp=False)
    async def свет(self, ctx: commands.GuildContext):
        pass

    @свет.command(name="небес")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def свет_небес(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} берёт в руки факел, но он тут же гаснет.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=120
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} искренне верит, что нехватка {cst-authbal} золотых монет не позволяет помочь ближнему.*")
        heal=random.randint(70, 80)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} озаряет {user.mention} светом, восстанавливая силы и улучшая настроение на {heal} золотых монет!*")

    @commands.command()
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def освящение(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} обходит лужу стороной.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} не находит в себе достаточно сил, чтобы противостоять чужой магии.*")
        authbal=await bank.get_balance(author)
        cst=360
        if authbal<cst:
            return await ctx.send (f"*Луч света пробил небеса и осветил {authbal} золотых монет в кошельке у {author.display_name}.*")
        await bank.withdraw_credits(author, cst)
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send (f"*{author.display_name} вскидывает своё оружие и освящает землю вокруг себя, рассеивая все чары.*")

    @commands.group(name="божественный", autohelp=False)
    async def божественный(self, ctx: commands.GuildContext):
        pass

    @божественный.command(name="щит")
    async def божественный_щит(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        ARM=discord.utils.get(ctx.guild.roles, id=765245699717595188)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} прячется в домике.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} изучает древний манускрипт в поисках способа защиты.*")
        authbal=await bank.get_balance(author)
        cst=120
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} внезапно понимает, что {cst-authbal} золотых монет остались дома.*")
        await bank.withdraw_credits(author, cst)
        await self.getarm(user=author, role=ARM)
        await ctx.send (f"*{author.display_name} окружает себя сияющим щитом и нащупывает камень возвращения в кармане.*")

    @commands.group(name="перековка", autohelp=False)
    async def перековка(self, ctx: commands.GuildContext):
        pass

    @перековка.command(name="светом")
    async def перековка_светом(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        HLY=discord.utils.get(ctx.guild.roles, id=772378594625454130)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} латает свой доспех.*")
            return await ctx.message.delete()
        if HLY in author.roles:
            return await ctx.send (f"*{author.display_name} любуется на свои сияющие золотые татуировки.*")
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send ("*Не каждый достоин быть перекованным светом.*")
        authbal=await bank.get_balance(author)
        cst=200
        if authbal<cst:
            return await ctx.send (f"*Пройти испытание может лишь тот, кто обладает {cst} золотыми монетами.*")#склонение
        await bank.withdraw_credits(author, cst)
        xp=await self.buffexp(ctx, author, 50)
        await self.zadd(who=author, give=HLY)
        await ctx.send (f"*Сияние света наполняет тело {author.display_name} и показывает видение будущего, что придаёт {xp} единиц опыта в будущих делах.*")

    @commands.command()
    async def порицание(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        HLY=discord.utils.get(ctx.guild.roles, id=772378594625454130)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} многозначительно качает пальцем в воздухе.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if HLY not in author.roles:
            return await ctx.send (f"*{author.display_name} выглядит недостаточно внушительно.*")
        authbal=await bank.get_balance(author)
        cst=30
        if authbal<cst:
            return await ctx.send (f"*У {author.display_name} пропадает голос при виде {authbal} золотых монет в своём кошельке.")
        await bank.withdraw_credits(author, cst)
        x=random.randint(1, 4)
        if x>2:
            await ctx.send(f"*Совесть {user.display_name} отягощают грехи.*")
        else:
            await author.remove_roles(HLY)
            xp=await self.buffexp(ctx, author, -50)
            await ctx.send(f"*Совесть {user.display_name} отягощают грехи. Из-за сомнений в правильности совершенного поступка {author.display_name} теряет {xp} единиц опыта, а сияние света гаснет.*")
        await self.delarm(ctx=ctx, user=user)
        await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
        await user.edit(reason=get_audit_reason(ctx.author, None), nick="😰 Скопище грехов")

    @commands.group(name="правосудие", autohelp=False)
    async def правосудие(self, ctx: commands.GuildContext):
        pass

    @правосудие.command(name="света")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def правосудие_света(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        HLY=discord.utils.get(ctx.guild.roles, id=772378594625454130)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} требует справедливого суда для {user.display_name}.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if HLY not in author.roles:
            return await ctx.send (f"*{author.display_name} не находит в себе достаточно уверенности для свершения правосудия.*")
        authbal=await bank.get_balance(author)
        cst=2400
        if authbal<cst:
            return await ctx.send (f"*Оружие {author.display_name} загорается ярким огнём, но тут же гаснет.*")
        targbal=await bank.get_balance(user)
        dmg=3*(targbal//20)#15%
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        x=random.randint(1, 4)
        if x>2:
            await ctx.send (f"*Молот, сотканный из чистого света, прилетает прямо в лоб {user.mention}, вышибая {dmg} золотых монет.*")
        else:
            await author.remove_roles(HLY)
            xp=await self.buffexp(ctx, author, -50)
            await ctx.send(f"*Молот, сотканный из чистого света, прилетает прямо в лоб {user.mention}, вышибая {dmg} золотых монет. Из-за сомнений в правильности совершенного поступка {author.display_name} теряет {xp} единиц опыта, а сияние света гаснет.*")

    @commands.group(name="возложение", autohelp=False)
    async def возложение(self, ctx: commands.GuildContext):
        pass

    @возложение.command(name="рук")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def возложение_рук(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724793567444995)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} делится теплом своих ладоней.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} чувствует кризис веры.*")
        authbal=await bank.get_balance(author)
        cst=authbal//2
        heal=7*(authbal//20)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} спасает жизнь {user.mention}, восстанавливая здоровья на {heal} золотых монет!*")

    @commands.group(name="волна", autohelp=False)
    async def волна(self, ctx: commands.GuildContext):
        pass

    @волна.command(name="исцеления")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def волна_исцеления(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724796075769889)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} берёт в руки ведро с водой и хихикает.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=140
        if authbal<cst:
            return await ctx.send (f"*Водная стихия сегодня капризна и {authbal} золотых монет не хватает, чтобы её задобрить.*")
        heal=random.randint(90, 120)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} окатывает {user.mention} потоком освежающей воды. Намокший кошелёк потяжелел на {heal} золотых монет.*")

    @commands.group(name="удар", autohelp=False)
    async def удар(self, ctx: commands.GuildContext):
        pass

    @удар.command(name="бури")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def удар_бури(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724796075769889)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} колотит поварёшкой по кастрюлям.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        authbal=await bank.get_balance(author)
        cst=60
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} не получает благословения стихий и решает набить морду {user.display_name} в другой раз.*")
        dmg=random.randint(70, 80)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*Под раскаты грома {author.display_name} наносит сокрушительный удар по {user.mention}, нанося урон здоровью на {dmg} золотых монет.*")

    @commands.group(name="выброс", autohelp=False)
    async def выброс(self, ctx: commands.GuildContext):
        pass

    @выброс.command(name="лавы")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def выброс_лавы(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724796075769889)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} идёт выбрасывать мусор.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} не может совладать с духами огня и поджигает стоящее недалеко дерево.*")
        authbal=await bank.get_balance(author)
        cst=2500
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} чувствует гнев стихий из-за нехватки {cst-authbal} золотых монет.*")
        dmg=random.randint(3000, 3100)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} направляет поток раскалённой лавы в лицо {user.mention}, расплавляя {dmg} золотых монет.*")
        dmg=(targbal-dmg)//100
        if dmg>10:
            await ctx.send (f"*{user.display_name} горит.*")
        else:
            return
        for tic in 3, 2, 1:
            await asyncio.sleep(15)
            brn=dmg*tic
            targbal=await bank.get_balance(user)
            if targbal<brn:
                return
            await bank.withdraw_credits(user, brn)
            await ctx.send (f"*{user.mention} теряет в огне {brn} золотых монет!*")

    @commands.command()
    async def сглаз(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        msg = await ctx.send(f"*{author.display_name} что-то шепчет в кулак, глядя на {user.mention}.*", components = [[Button(style = ButtonStyle.green, emoji = '🐸', id = "1"), Button(style = ButtonStyle.green, emoji = '🐍', id = "2"), Button(style = ButtonStyle.green, emoji = '🐭', id = "3"), Button(style = ButtonStyle.green, emoji = '🍯', id = "4"), Button(style = ButtonStyle.green, emoji = '🐌', id = "5")]])
        CLS=discord.utils.get(ctx.guild.roles, id=685724796075769889)
        try:
            responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=5)
        except asyncio.TimeoutError:
            if CLS not in author.roles:
                await msg.edit ("*Где-то вдалеке послышался смех Крагвы.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            rank=await self.chkrank(ctx=ctx, user=author)
            if rank<=1:
                return await msg.edit (f"*{author.display_name} представляет образ лягушки, но не может воплотить его в жизнь.*", components = [])
            authbal=await bank.get_balance(author)
            cst=190
            if authbal<cst:
                return await msg.edit (f"*{author.display_name} придумывает гениальное наказание для {user.display_name}и отправляется на болото, собирать все необходимые ингридиенты.", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} что-то шепчет в кулак, и {user.display_name} превращается в маленькое зелёное земноводное.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            return await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐸 Лягушка")
        if responce.component.id == '1':
            if CLS not in author.roles:
                await msg.edit ("*Где-то вдалеке послышался смех Крагвы.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            rank=await self.chkrank(ctx=ctx, user=author)
            if rank<=1:
                return await msg.edit (f"*{author.display_name} представляет образ лягушки, но не может воплотить его в жизнь.*", components = [])
            authbal=await bank.get_balance(author)
            cst=190
            if authbal<cst:
                return await msg.edit (f"*{author.display_name} придумывает гениальное наказание для {user.display_name}и отправляется на болото, собирать все необходимые ингридиенты.", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} что-то шепчет в кулак, и {user.display_name} превращается в маленькое зелёное земноводное.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐸 Лягушка")
        elif responce.component.id == '2':
            if CLS not in author.roles:
                await msg.edit ("*Где-то вдалеке послышался смех Хетисса.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            rank=await self.chkrank(ctx=ctx, user=author)
            if rank<=1:
                return await msg.edit (f"*{author.display_name} представляет образ змеи, но не может воплотить его в жизнь.*", components = [])
            authbal=await bank.get_balance(author)
            cst=190
            if authbal<cst:
                return await msg.edit (f"*{author.display_name} придумывает гениальное наказание для {user.display_name}и отправляетс-с-ся, с-с-собирать вс-с-се необходимые ингридиенты.", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} что-то шепчет в кулак, и {user.display_name} превращается в маленькое чешуйчатое пресмыкающееся.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐍 Змея")
        elif responce.component.id == '3':
            if CLS not in author.roles:
                await msg.edit ("*Где-то вдалеке послышался смех Хирика.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            rank=await self.chkrank(ctx=ctx, user=author)
            if rank<=1:
                return await msg.edit (f"*{author.display_name} представляет образ мыши, но не может воплотить его в жизнь.*", components = [])
            authbal=await bank.get_balance(author)
            cst=190
            if authbal<cst:
                return await msg.edit (f"*{author.display_name} придумывает гениальное наказание для {user.display_name}и отправляется за сыром.", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} что-то шепчет в кулак, и {user.display_name} превращается в маленького серого грызуна.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐭 Мышь")
        elif responce.component.id == '4':
            if CLS not in author.roles:
                await msg.edit ("*Где-то вдалеке послышался рёв Урсола.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            rank=await self.chkrank(ctx=ctx, user=author)
            if rank<=1:
                return await msg.edit (f"*{author.display_name} представляет себе баночку мёда, но голод не утихает.*", components = [])
            authbal=await bank.get_balance(author)
            cst=190
            if authbal<cst:
                return await msg.edit (f"*{author.display_name} придумывает нетривиальное наказание для {user.display_name} и начинает танцевать с пчёлами.", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} что-то шепчет в кулак, и {user.display_name} превращается в жёлтую липкую субстанцию.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🍯 Живой мёд")
        elif responce.component.id == '5':
            if CLS not in author.roles:
                await msg.edit ("*Где-то вдалеке послышался шёпот Неспиры.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            rank=await self.chkrank(ctx=ctx, user=author)
            if rank<=1:
                return await msg.edit (f"*{author.display_name} представляет образ улитки, но не может воплотить его в жизнь.*", components = [])
            authbal=await bank.get_balance(author)
            cst=190
            if authbal<cst:
                return await msg.edit (f"*{author.display_name} придумывает гениальное наказание для {user.display_name} и уже вот-вот отправится собирать все необходимые ингридиенты.", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} что-то шепчет в кулак, и {user.display_name} превращается в маленького брюхоногого моллюска.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐌 Улитка")

    @commands.command()
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def раскол(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724796075769889)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} с размаху бьёт землю молотком. Молоток отскакивает и чудом никого не задевает.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*У {author.display_name} не хватает сил расколоть земную твердь.*")
        slw=ctx.channel.slowmode_delay
        if slw>=3600:
            return await ctx.send ("*Здесь действуют более мощные чары.*")
        authbal=await bank.get_balance(author)
        cst=360
        if authbal<cst:
            return await ctx.send (f"*У {author.display_name} кружится голова, а перед глазами летают {cst-authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        await ctx.channel.edit(slowmode_delay=3600)
        await ctx.send (f"*Земля раскалывается и пол заливает лава. Любой ступивший на пол не сможет вразумительно говорить как минимум час.*")

    @commands.group(name="цепное", autohelp=False)
    async def цепное(self, ctx: commands.GuildContext):
        pass

    @цепное.command(name="исцеление")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def цепное_исцеление(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724796075769889)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} вешает чайник над костром.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*Связь {author.display_name} со стихиями ещё недостаточно крепка.*")
        authbal=await bank.get_balance(author)
        cst=5500
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} размахивает руками, но {cst-authbal} золотых монет на счету не появляются.*")
        await bank.withdraw_credits(author, cst)
        heal=random.randint(3500, 3600)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.deposit_credits(user, heal)
        targ2=random.choice(ctx.message.guild.members)
        if targ2==user:
            return await ctx.send (f"*{author.display_name} пускает исцеляющий луч в {user.mention}. Луч восполняет {heal} золотых монет, а затем, не найдя другой цели, растворяется в пустоте.*")
        targ2bal=await bank.get_balance(targ2)
        heal2=random.randint(800, 900)
        if targ2bal>(max_bal-heal2):
            heal2=(max_bal-targ2bal)
        await bank.deposit_credits(targ2, heal2)
        targ3=random.choice(ctx.message.guild.members)
        if targ3==targ2:
            return await ctx.send (f"*{author.display_name} пускает исцеляющий луч в {user.mention}. Луч, восполнив {heal} золотых монет, продолжает свой путь, исцеляя по пути {targ2.mention} на {heal2} золотых монет, а затем растворяется в пустоте.*")
        targ3bal=await bank.get_balance(targ3)
        heal3=random.randint(600, 700)
        if targ3bal>(max_bal-heal3):
            heal3=(max_bal-targ3bal)
        await bank.deposit_credits(targ3, heal3)
        targ4=random.choice(ctx.message.guild.members)
        if targ4==targ3:
            return await ctx.send (f"*{author.display_name} пускает исцеляющий луч в {user.mention}. Луч, восполнив {heal} золотых монет, продолжает свой путь, исцеляя на своём пути {targ2.mention} на {heal2} золотых монет, потом {targ3.mention} на {heal3} золотых монет, а затем растворяется в пустоте.*")
        targ4bal=await bank.get_balance(targ4)
        heal4=random.randint(400, 500)
        if targ4bal>(max_bal-heal4):
            heal4=(max_bal-targ4bal)
        await bank.deposit_credits(targ4, heal4)
        targ5=random.choice(ctx.message.guild.members)
        if targ5==targ4:
            return await ctx.send (f"*{author.display_name} пускает исцеляющий луч в {user.mention}. Луч, восполнив {heal} золотых монет, продолжает свой путь, исцеляя на своём пути {targ2.mention} на {heal2} золотых монет, потом {targ3.mention} на {heal3} золотых монет и ещё {targ4.mention} на {heal4} золотых монет, а затем растворяется в пустоте.*")
        targ5bal=await bank.get_balance(targ5)
        heal5=random.randint(200, 300)
        if targ5bal>(max_bal-heal5):
            heal5=(max_bal-targ5bal)
        await bank.deposit_credits(targ5, heal5)
        await ctx.send (f"*{author.display_name} пускает исцеляющий луч в {user.mention}. Луч, восполнив {heal} золотых монет, продолжает свой путь, исцеляя на своём пути {targ2.mention} на {heal2} золотых монет, потом {targ3.mention} на {heal3} золотых монет, ещё {targ4.mention} лечит на {heal4} золотых монет, и наконец попадает в {targ5.mention}, излечивая на {heal5} золотых монет.*")

    @commands.command()
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def щит(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724797266952219)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} открывает зонтик над головой.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=70
        if authbal<cst:
            return await ctx.send (f"*Чтобы защитить словом, нужно иметь богатый словарный запас!*")
        heal=random.randint(50, 60)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} окружает {user.mention} непроницаемым пузырём, излечивающий от повреждений на {heal} золотых монет.*")

    @commands.group(name="молитва", autohelp=False)
    async def молитва(self, ctx: commands.GuildContext):
        pass

    @молитва.command(name="исцеления")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def молитва_исцеления(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724797266952219)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} склоняет голову и благодарит богов за посланную еду.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} не может подобрать слова, чтобы передать свои чувства.*")
        authbal=await bank.get_balance(author)
        cst=6000
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} испытывает кризис веры на {cst-authbal} золотых монет.*")
        heal=random.randint(4000, 4100)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} возносит молитву, даруя {user.mention} надежду и возможность разбогатеть на {heal} золотых монет!*")

    @commands.group(name="священная", autohelp=False)
    async def священная(self, ctx: commands.GuildContext):
        pass

    @священная.command(name="земля")
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def священная_земля(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724797266952219)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} грезит образом наару.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} благославляет землю под ногами, но это ничего не меняет.*")
        authbal=await bank.get_balance(author)
        cst=320
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} встаёт на колени и воздаёт молитву земле под ногами, но этого оказывается недостаточно.*")
        await bank.withdraw_credits(author, cst)
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send (f"*Вспышка чудодейственного света озаряет окрестности и снимает все действующие на область чары.*")

    @commands.group(name="облик", autohelp=False)
    async def облик(self, ctx: commands.GuildContext):
        pass

    @облик.command(name="бездны")
    async def облик_бездны(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724797266952219)
        BAF=discord.utils.get(ctx.guild.roles, id=686202652392292357)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} точит ритуальный нож.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} хватается за голову, пытаясь совладать с навязчивым шёпотом.")
        authbal=await bank.get_balance(author)
        cst=650
        if authbal<cst:
            return await ctx.send (f"*Голоса в вашей голове требуют принести человеческую жертву или {cst} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=author, give=BAF)
        await ctx.send (f"*Струйки фиолетовой энергии обвалакивают тело {author.display_name}.*")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def воззвание(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724797266952219)
        BAF=discord.utils.get(ctx.guild.roles, id=686202652392292357)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} безответственно играет с могущественными силами.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if BAF not in author.roles:
            return await ctx.send (f"*Нужно добиться большего единения с Бездной, чтобы призвать её в наш мир.*")
#        cur_time = calendar.timegm(ctx.message.created_at.utctimetuple())
#        next_payday = await self.config.user(author).next_payday()
#        if cur_time < next_payday:
#            dtime = self.display_time(next_payday - cur_time)
#            return await ctx.send(f"Окружающему миру нужно восстановиться. Следующий прорыв Бездны возможен через {dtime}")
        amount=random.randint(190, 210)
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if authbal>(max_bal-amount):
            amount=(max_bal-authbal)
        await bank.deposit_credits(author, amount)
        xp=await self.buffexp(ctx, author, -15)
#        next_payday = cur_time + await self.config.PAYDAY_TIME()
#        await self.config.user(author).next_payday.set(next_payday)
        await ctx.send(f"{author.display_name} взывает к Бездне, теряя {xp} единиц опыта. Несколько тёмных щупалец прорывают реальность и высасывают энергию из окружающего мира на {amount} золотых монет.")

    @commands.command()
    async def безумие(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724797266952219)
        if CLS not in author.roles:
            await ctx.send (f"*Голоса в голове {author.display_name} начали перепалку.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} слышит чей-то проникновенный шёпот: 'Твой разум слишком слаб. Все друзья предадут тебя! {user.display_name} предаст тебя!'*")
        authbal=await bank.get_balance(author)
        cst=220
        if authbal<cst:
            return await ctx.send (f"*Взывать к Тьме, имея на счету лишь {authbal} золотых монет - чревато нежелательными последствиями.")
        await bank.withdraw_credits(author, cst)
        await ctx.send(f"*Липкие щупальца обвивают голову {user.display_name}, погружая разум в безумие.*")
        await self.delarm(ctx=ctx, user=user)
        await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
        await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐙 Пожиратель разума")

    @commands.command()
    async def молчание(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724797266952219)
        MUT=discord.utils.get(ctx.guild.roles, id=685725960368160787)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} молчит с умным видом. Очень умным!*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=250
        if authbal<cst:
            return await ctx.send (f"*Сомнения терзают душу {author.display_name}: стоит ли обращаться к тёмным силам за такую цену?*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=MUT)
        await ctx.send(f"*Глаза {author.display_name} наливаются фиолетовым светом, и инфернальный вопль 'МОЛЧАТЬ!' заставляет {user.mention} умолкнуть.*")

    @commands.group(name="стрела", autohelp=False)
    async def стрела(self, ctx: commands.GuildContext):
        pass

    @стрела.command(name="тьмы")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def стрела_тьмы(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724799527551042)
        if CLS not in author.roles:
            await ctx.send (f"*Тьма сгущается вокруг {author.display_name}, но дальше никуда не идёт.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=70
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} концентрируется на тьме, но жизненной силы недостаточно для сохранения самообладания.*")
        dmg=random.randint(90, 100)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*Концентрированная чёрная магия устремляется к {user.mention}, поглощая {dmg} золотых монет.*")

    @commands.group(name="ожог", autohelp=False)
    async def ожог(self, ctx: commands.GuildContext):
        pass

    @ожог.command(name="души")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def ожог_души(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724799527551042)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} отжигает.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} пытается потушить внезапно загоревшуюся руку.*")
        authbal=await bank.get_balance(author)
        cst=2700
        if authbal<cst:
            return await ctx.send (f"*Чтобы поджечь чужую душу, нужно укрепить свою ещё {cst-authbal} золотыми монетами.*")
        xp=random.randint(-100, -10)
        xp=await self.buffexp(ctx, user, xp)
        dmg=3300-(10*xp)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} выпускает сгусток пламени, который поражает {user.mention}, терзая душу на {xp} единиц опыта и сжигая {dmg} золотых монет.*")

    @commands.command()
    async def страх(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724799527551042)
        MUT=discord.utils.get(ctx.guild.roles, id=687897801836724235)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} рассказывает страшную историю у костра.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=190
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} приглядывается к {user.display_name}, оценивая фобии. Данных недостаточно.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=MUT)
        await ctx.send(f"*{author.display_name} вскидывает  руки, выпуская страшное заклятие. {user.mention} в ужасе бежит в стену.*")

    @commands.group(name="тёмный", autohelp=False)
    async def тёмный(self, ctx: commands.GuildContext):
        pass

    @тёмный.command(name="пакт")
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def тёмный_пакт(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724799527551042)
        BES=discord.utils.get(ctx.guild.roles, id=687899248892706830)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} тщётно пытается прочесть мелкий текст на свитке заклинания.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name}    .*")
        authbal=await bank.get_balance(author)
        cst=170
        if authbal<cst:
            return await ctx.send (f"*Для заклинания не хватает жизненной силы. Оленята в ужасе разбегаются в стороны.*")
        if BES in user.roles:
            return await ctx.send (f"*Бес на плече {user.display_name} бросается огненными шариками и грязно ругает конкурентов.*")
        heal=random.randint(120, 130)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await self.zadd(who=user, give=BES)
        await ctx.send (f"*{author.display_name} подделывает подпись кровью {user.mention} на контракте с демоном. {user.display_name} получает {heal} золотых монет и долговое обязательство перед мелким бесом.*")

    @commands.command()
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def расплата(self, ctx, user: discord.Member = None):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724799527551042)
        BES=discord.utils.get(ctx.guild.roles, id=687899248892706830)
        if BES not in author.roles:
            await ctx.send (f"*{author.display_name} угрожающе помахивает своим оружием.*")
            return await ctx.message.delete()
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        targbal=await bank.get_balance(user)
        authbal=await bank.get_balance(author)
        dmg=random.randint(120, 130)
        if CLS in user.roles:
            dmg1=random.randint(1, dmg)
            dmg-=dmg1
            if authbal<dmg1:
                dmg1=authbal
            if targbal<dmg:
                dmg=targbal
            await bank.withdraw_credits(user, dmg)
            await bank.withdraw_credits(author, dmg1)
            await author.remove_roles(BES)
            return await ctx.send(f"*{author.display_name} натравливает беса на {user.mention}. Довольный бес наносит урон в размере {dmg} золотых монет и обжигает плечо {author.mention}, боль забирает сил на {dmg1} золотых монет.*")
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(user, dmg)
        await author.remove_roles(BES)
        await ctx.send(f"*{author.display_name} натравливает беса на {user.mention}. Довольный бес наносит урон в размере {dmg} золотых монет и тут же исчезает.*")

    @commands.command()
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def катаклизм(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724799527551042)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} бегает вокруг, размахивая руками, и кричит: 'КОНЕЦ БЛИЗОК!'*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} вздымает руки ввысь и начинает яростно смеяться.*")
        slw=ctx.channel.slowmode_delay
        if slw>=900:
            return await ctx.send ("*Здесь действуют более мощные чары.*")
        authbal=await bank.get_balance(author)
        cst=240
        if authbal<cst:
            return await ctx.send (f"*С неба падают несколько камушков, чудом никого не задевая.*")
        await bank.withdraw_credits(author, cst)
        await ctx.channel.edit(slowmode_delay=900)
        await ctx.send (f"*С небес начинают сыпаться раскалённые булыжники, оглушающие каждого попавшего под них на 15 минут. {author.display_name} злобно хохочет.*")

    @commands.command()
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def преисподняя(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724799527551042)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} ловит зелёных чертей в междуящичном пространстве.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} пытается открыть портал в Круговерть Пустоты. Из возникшей бреши вылетела пустая бутылка и разлом захлопнулся.*")
        slw=ctx.channel.slowmode_delay
        if slw>=21600:
            return await ctx.send ("*Здесь действуют более мощные чары.*")
        authbal=await bank.get_balance(author)
        cst=360
        if authbal<cst:
            return await ctx.send (f"*Не хватает {cst-authbal} монет, чтобы выложить пентаграмму на земле.*")
        await bank.withdraw_credits(author, cst)
        await ctx.channel.edit(slowmode_delay=21600)
        await ctx.send (f"*{author.display_name} открывает портал в Круговерть Пустоты, в который затягивает всё подряд. Каждому, кто туда попадёт, потребуется около шести часов, чтобы вернуться обратно.*")

    @commands.group(name="огненный", autohelp=False)
    async def огненный(self, ctx: commands.GuildContext):
        pass

    @огненный.command(name="шар")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def огненный_шар(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724798193762365)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} надувает воздушный шарик ярко-красного цвета.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} находит лужу магмы и пытается скатать 'снежок'.*")
        authbal=await bank.get_balance(author)
        cst=80
        if authbal<cst:
            return await ctx.send (f"*На кончиках пальцев {author.display_name} вспыхивают огоньки, но их тут же сдувает ветром. Нужно больше топлива!*")
        dmg=random.randint(100, 110)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} запускает огненную сферу. На этот раз {user.mention} отделывается лёгким ожогом, но {dmg} золотых монет в кошельке оказались расплавлены.*")

    @commands.group(name="кольцо", autohelp=False)
    async def кольцо(self, ctx: commands.GuildContext):
        pass

    @кольцо.command(name="льда")
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def кольцо_льда(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724798193762365)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} ловит ртом снежинки.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        slw=ctx.channel.slowmode_delay
        if slw>=300:
            return await ctx.send ("*Здесь действуют более мощные чары.*")
        authbal=await bank.get_balance(author)
        cst=160
        if authbal<cst:
            return await ctx.send (f"*От {author.display_name} начинает бежать волна холода, но резко тает.*")
        await bank.withdraw_credits(author, cst)
        await ctx.send (f"Воздух вокруг резко наполняет морозная свежесть. Есть опасность заморозить лёгкие на 5 минут.")
        await ctx.channel.edit(slowmode_delay=300)

    @commands.group(name="чародейский", autohelp=False)
    async def чародейский(self, ctx: commands.GuildContext):
        pass

    @чародейский.command(name="интеллект")
    @commands.cooldown(3, 86400, commands.BucketType.user)
    async def чародейский_интеллект(self, ctx, user: discord.Member = None):
        author=ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724798193762365)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} бросает в {user.display_name} учебник по тайной магии.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{author.display_name} безуспешно ищет нужный свиток среди творческого беспорядка.*")
        authbal=await bank.get_balance(author)
        cst=250
        if authbal<cst:
            return await ctx.send (f"*{cst-authbal} маны недостаточно для этого заклинания!*")
        await bank.withdraw_credits(author, cst)
        xp=await self.buffexp(ctx, user, 25)
        await ctx.send (f"*{author.display_name} накладывает хитроумное заклинание на {user.mention}, усиливающее интеллект и опыт на {xp} единиц.*")

    @commands.command()
    async def превращение(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        msg = await ctx.send(f"*{author.display_name} собирается сделать выбор, глядя на {user.mention}.*", components = [[Button(style = ButtonStyle.blue, emoji = '🐑', id = '1'), Button(style = ButtonStyle.blue, emoji = '🐰', id = '2'), Button(style = ButtonStyle.blue, emoji = '🐒', id = '3'), Button(style = ButtonStyle.blue, emoji = '🐝', id = '4'), Button(style = ButtonStyle.blue, emoji = '🐷', id = '5')]])
        CLS=discord.utils.get(ctx.guild.roles, id=685724798193762365)
        try:
            responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=5)
        except asyncio.TimeoutError:
            if CLS not in author.roles:
                await msg.edit (f"*{author.display_name} ищет знания.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            authbal=await bank.get_balance(author)
            cst=210
            if authbal<cst:
                return await msg.edit (f"*Уровень интеллекта {user.display_name} превышает количество вашей маны.*", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} накладывает на {user.display_name} заклинание, придающее более подходящую форму.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            return await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐑 Овечка")
        if responce.component.id == '1':
            if CLS not in author.roles:
                await msg.edit (f"*{author.display_name} ищет знания.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            authbal=await bank.get_balance(author)
            cst=210
            if authbal<cst:
                return await msg.edit (f"*Уровень интеллекта {user.display_name} превышает количество вашей маны.*", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} накладывает на {user.display_name} заклинание, придающее более подходящую форму.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐑 Овечка")
        elif responce.component.id == '2':
            if CLS not in author.roles:
                await msg.edit (f"*{author.display_name} ищет что-то похожее на морковку.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            authbal=await bank.get_balance(author)
            cst=210
            if authbal<cst:
                return await msg.edit (f"*Уровень интеллекта {user.display_name} превышает интеллект кролика или количество вашей маны.*", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} накладывает на {user.display_name} заклинание, придающее более подходящую форму.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐰 Кролик")
        elif responce.component.id == '3':
            if CLS not in author.roles:
                await msg.edit (f"*{author.display_name} ищет что-то похожее на банан.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            authbal=await bank.get_balance(author)
            cst=210
            if authbal<cst:
                return await msg.edit (f"*Уровень интеллекта {user.display_name} превышает интеллект обезьяны или количество вашей маны.*", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} накладывает на {user.display_name} заклинание, придающее более подходящую форму.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐒 Обезьяна")
        elif responce.component.id == '4':
            if CLS not in author.roles:
                await msg.edit (f"*{author.display_name} ищет что-то похожее на пыльцу.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            authbal=await bank.get_balance(author)
            cst=210
            if authbal<cst:
                return await msg.edit (f"*Уровень интеллекта {user.display_name} превышает интеллект роя или количество вашей маны.*", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} накладывает на {user.display_name} заклинание, придающее более жужжащую форму.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐝 Пчела")
        elif responce.component.id == '5':
            if CLS not in author.roles:
                await msg.edit (f"*{author.display_name} ищет что-то похожее на жёлуди.*", components = [])
                return await ctx.message.delete()
            if ctx.message.channel.id != 603151774009786393:
                return await msg.edit("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.", components = [])
            authbal=await bank.get_balance(author)
            cst=210
            if authbal<cst:
                return await msg.edit (f"*Уровень интеллекта {user.display_name} превышает интеллект свиньи или количество вашей маны.*", components = [])
            await bank.withdraw_credits(author, cst)
            await msg.edit(f"*{author.display_name} накладывает на {user.display_name} заклинание, придающее более подходящую форму.*", components = [])
            await self.delarm(ctx=ctx, user=user)
            await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
            await user.edit(reason=get_audit_reason(ctx.author, None), nick="🐷 Свинья")

    @commands.group(name="сотворение", autohelp=False)
    async def сотворение(self, ctx: commands.GuildContext):
        pass

    @сотворение.command(name="пищи")
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def сотворение_пищи(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724798193762365)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} вспоминает про пирожки, забытые в духовке, и убегает.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} материлизует возле себя стол, наполненный различными камнями и угольками.*")
        authbal=await bank.get_balance(author)
        cst=400
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} собирается накормить всех вокруг, но обнаруживает что одежда совершенно не подходит для готовки!*")
        await bank.withdraw_credits(author, cst)
        await self.getfood(ctx=ctx, user=author)
        await ctx.send (f"*{author.display_name} материлизует возле себя стол, наполненный ароматной выпечкой. Любой желающий может угоститься.*")

    @commands.group(name="угоститься", autohelp=False)
    async def угоститься(self, ctx: commands.GuildContext):
        pass

    @угоститься.command(name="у")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def угоститься_у(self, ctx, user: discord.Member = None):
        author=ctx.author
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if user is None:
            user=random.choice(ctx.message.guild.members)
        KTZ=discord.utils.get(ctx.guild.roles, id=688044643052421127)
        BUL=discord.utils.get(ctx.guild.roles, id=772380354803793920)
        PLU=discord.utils.get(ctx.guild.roles, id=772380359454490624)
        BIS=discord.utils.get(ctx.guild.roles, id=772380362927636500)
        if BUL in user.roles:
            heal=random.randint(80, 90)
            authbal=await bank.get_balance(author)
            max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
            if authbal>(max_bal-heal):
                heal=(max_bal-authbal)
            await user.remove_roles(BUL)
            await bank.deposit_credits(author, heal)
            await ctx.send (f"*{author.display_name} берёт со стола аппетитную манабулочку и с упоением уплетает, восстанавливая сил на {heal} золотых монет.*")
        elif PLU in user.roles:
            if KTZ in author.roles:
                await user.remove_roles(KTZ)
                await user.remove_roles(PLU)
                await ctx.send (f"*{author.display_name} протягивает руку к аппетитной манаплюшке, но мистер Бигглсуорт хватает её первее и скрывается с ней за углом.*")
            else:
                heal=random.randint(80, 90)
                authbal=await bank.get_balance(author)
                max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
                if authbal>(max_bal-heal):
                    heal=(max_bal-authbal)
                await user.remove_roles(PLU)
                await bank.deposit_credits(author, heal)
                await ctx.send (f"*{author.display_name} берёт со стола аппетитную манаплюшку и с упоением уплетает, восстанавливая сил на {heal} золотых монет.*")
        elif BIS in user.roles:
            heal=random.randint(80, 90)
            authbal=await bank.get_balance(author)
            max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
            if authbal>(max_bal-heal):
                heal=(max_bal-authbal)
            await user.remove_roles(BIS)
            await bank.deposit_credits(author, heal)
            await ctx.send (f"*{author.display_name} берёт со стола аппетитный манабисквит и с упоением уплетает, восстанавливая сил на {heal} золотых монет.*")
        else:
            await ctx.send (f"*{author.display_name} протягивает руку к столу, но она сжимает лишь пустоту.*")

    @commands.command()
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def метеор(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724798193762365)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} наблюдает за движением небесных тел.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} читает заклинание призыва метеорита, но постоянно путается в словах.*")
        authbal=await bank.get_balance(author)
        cst=2800
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} бросает камень в воздух и кричит: - Ложись!*")
        dmg=random.randint(3500, 3600)
        targbal=await bank.get_balance(user)
        dmg+=(targbal-dmg)//20
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        targ1=random.choice(ctx.message.guild.members)
        await ctx.send (f"*В небе появляется метеорит! Он скоро упадёт туда, где стоит {targ1.mention}!*\nЛучше отойди в сторону.")
        await asyncio.sleep(20)
        targ2=random.choice(ctx.message.guild.members)
        await ctx.send (f"*Тень здоровенного метеорита накрыла собой {targ2.mention}!*\nУбегай скорее!")
        await asyncio.sleep(20)
        targ3=random.choice(ctx.message.guild.members)
        await ctx.send (f"*Метеорит приближается и вот-вот упадёт на {targ3.mention}!*\nСпасайся кто может!!!")
        await asyncio.sleep(20)
        await ctx.send (f"*Огромный пылающий валун прилетает с небес и врезается в {user.mention}. Во все стороны брызнули {dmg} раскалённых золотых монет.*")
        await bank.withdraw_credits(user, dmg)

    @удар.command(name="плети")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def удар_плети(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724801486290947)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} ищет свою любимую плётку.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=160
        if authbal<cst:
            return await ctx.send (f"*Нужно больше некротической энергии! Принесите в жертву ещё {cst-authbal} мелких зверей.*")
        dmg=random.randint(240, 250)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*Усиленный нечестивой магией удар выбивает из {user.mention} дух и {dmg} золотых монет.*")
        if "🩸🩸🩸" in author.display_name:
            await ctx.send (f"*{author.display_name} упивается страданиями!*")

    @commands.command()
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def уничтожение(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724801486290947)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} бросает уничтожающе презрительный взгляд на {user.display_name}.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} копит в себе ненависть. Однажды, кто-то от этого пострадает.*")
        authbal=await bank.get_balance(author)
        cst=3000
        if authbal<cst:
            return await ctx.send (f"*Рунная гравировка на оружии требует обновления. Вам не хватает {cst-authbal} золотых монет.*")
        targbal=await bank.get_balance(user)
        dmg=random.randint(4000, 4100)+targbal//25
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} жестоким ударом потрошит {user.mention}. Из нутра жертвы на пол шлёпаются {dmg} золотых монет.*")
        if "🩸🩸🩸" in author.display_name:
            heal=targbal//100
            max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
            if authbal>(max_bal-heal):
                heal=(max_bal-authbal)
            await bank.deposit_credits(author, heal)
            await ctx.send (f"*{author.display_name} упивается страданиями {user.display_name} на {heal} золотых монет!*")
        else:
            try:
                await author.edit(reason=get_audit_reason(ctx.author, None), nick=author.display_name + "🩸")
            except discord.HTTPException:
                await author.edit(reason=get_audit_reason(ctx.author, None), nick="Брызги крови 🩸")

    @commands.group(name="антимагический", autohelp=False)
    async def антимагический(self, ctx: commands.GuildContext):
        pass

    @антимагический.command(name="панцирь")
    async def антимагический_панцирь(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724801486290947)
        ARM=discord.utils.get(ctx.guild.roles, id=765245698240413706)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} обводит мелом место на котором стоит.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*Чтобы поставить защиту от магии, нужно больше тренировок!*")
        authbal=await bank.get_balance(author)
        cst=140
        if authbal<cst:
            return await ctx.send (f"*Из-за недостатка чужих страданий {author.display_name} чувствует свою уязвимость.*")
        await bank.withdraw_credits(author, cst)
        await self.getarm(user=author, role=ARM)
        await ctx.send (f"*{author.display_name} окружает себя коконом, непроницаемым для любых видов магии.*")

    @commands.command()
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def осквернение(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724801486290947)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} бросает мусор на пол.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        slw=ctx.channel.slowmode_delay
        if slw>=900:
            return await ctx.send ("*Здесь действуют более мощные чары.*")
        authbal=await bank.get_balance(author)
        cst=240
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} жаждет больше страданий.*")
        await bank.withdraw_credits(author, cst)
        await ctx.send (f"Область по ногами {author.display_name} наполняется силами разложения и тлена.")
        if "🩸🩸🩸" in author.display_name:
            await ctx.send (f"*{author.display_name} упивается страданиями!*")
        await ctx.channel.edit(slowmode_delay=900)

    @commands.command()
    async def перерождение(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724801486290947)
        ARM=discord.utils.get(ctx.guild.roles, id=687901221645975636)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} раздаёт указания своим прихвостням.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*'Нельзя сотворить здесь!' - донеслось откуда-то.*")
        authbal=await bank.get_balance(author)
        cst=200
        if authbal<cst:
            return await ctx.send (f"*{user.display_name} источает слишком много жизненной силы.")
        await bank.withdraw_credits(author, cst)
        await ctx.send(f"*{author.display_name} призывает некротические энергии, чтобы умертвить и переродить {user.display_name} в качестве прислужника.*")
#        await self.delarm(ctx=ctx, user=user)
        await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
        await user.edit(reason=get_audit_reason(ctx.author, None), nick="💀 Живая мертвечина")
        await self.getarm(user=user, role=ARM)

    @commands.group(name="взрыв", autohelp=False)
    async def взрыв(self, ctx: commands.GuildContext):
        pass

    @взрыв.command(name="трупа")
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def взрыв_трупа(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724801486290947)
        ARM=discord.utils.get(ctx.guild.roles, id=687901221645975636)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} балуется с динамитом и чьим-то трупом.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if ARM not in user.roles:
            return await ctx.send (f"*{author.display_name} берёт лопату и идёт на поиски трупа.*")
        authbal=await bank.get_balance(author)
        cst=80
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} жутко раздражается при виде {user.display_name}, но ничего поделать не может.*")
        dmg=random.randint(100, 110)
        targbal=await bank.get_balance(user)
        if targbal<dmg:
            dmg=targbal
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await user.remove_roles(ARM)
        await ctx.send (f"*{author.display_name} устремляет взгляд на пробегающего мимо вурдалака, странно похожего на {user.display_name}, и тот взрывается фонтаном крови, костей и {dmg} золотых монет.*")
        await ctx.send(f"*{user.display_name} теперь {user.mention}.*")
        await user.edit(reason=get_audit_reason(ctx.author, None), nick="🩸☠️🥩 Кровавые ошмётки")

    @commands.group(name="беспощадность", autohelp=False)
    async def беспощадность(self, ctx: commands.GuildContext):
        pass

    @беспощадность.command(name="зимы")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def беспощадность_зимы(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724801486290947)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} заявляет, что 'Зима близко' и облокачивается на свой двуручный меч.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*{author.display_name} в злости вызывает снегопад, но для большего эффекта не хватает мастерства.*")
        slw=ctx.channel.slowmode_delay
        if slw>=3600:
            return await ctx.send ("*Здесь действуют более мощные чары.*")
        authbal=await bank.get_balance(author)
        cst=360
        if authbal<cst:
            return await ctx.send (f"*Рунной энергии недостаточно.*")
        await bank.withdraw_credits(author, cst)
        await ctx.channel.edit(slowmode_delay=3600)
        await ctx.send (f"*{author.display_name} промораживает насквозь каждого, кто попадает в зону поражения. Жертвы не могут двигаться в течении часа.*")
        if "🩸🩸🩸" in author.display_name:
            await ctx.send (f"*{author.display_name} упивается страданиями!*")
        await asyncio.sleep(60)
        slw1=ctx.channel.slowmode_delay
        dmg1=0
        while slw1>1600 and dmg1<200:
            user = random.choice(ctx.message.guild.members)
            while user is author:
                user = random.choice(ctx.message.guild.members)
            targbal=await bank.get_balance(user)
            dmg=targbal//100
            await bank.withdraw_credits(user, dmg)
            await ctx.send (f"*Ледяной ветер промораживает до костей {user.mention}, отнимая сил на {dmg} золотых монет. Ветер немного стихает.*")
            if dmg*10 < slw1:
                slw1-=dmg*10
            else:
                slw1=0
            dmg1+=dmg
            await ctx.channel.edit(slowmode_delay=slw1)
            if "🩸🩸🩸" in author.display_name:
                await ctx.send (f"*{author.display_name} упивается страданиями!*")
            await asyncio.sleep(60)
            slw1=ctx.channel.slowmode_delay

    @commands.group(name="гором", autohelp=False)
    async def гором(self, ctx: commands.GuildContext):
        pass

    @гором.command(name="хагуул")
    @commands.cooldown(3, 86400, commands.BucketType.user)
    async def гором_хагуул(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724803105161216)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} достаёт сварочный аппарат.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} снимает повязку и пристально смотрит на {user.display_name} горящими глазами.*")
        authbal=await bank.get_balance(author)
        cst=120
        if authbal<cst:
            return await ctx.send (f"*Повязка на глазах мешает заметить недостаток {cst-authbal} золотых монет на счёте.*")
        await bank.withdraw_credits(author, cst)
        xp1=await self.buffexp(ctx, user, -12)
        xp2=await self.buffexp(ctx, author, -xp1)
        await ctx.send (f"*{author.display_name} прожигает взглядом дыру в {user.mention} и вытягивает оттуда {xp1} единиц опыта.*")

    @commands.group(name="катра", autohelp=False)
    async def катра(self, ctx: commands.GuildContext):
        pass

    @катра.command(name="шукил")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def катра_шукил(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724803105161216)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} разводит костёр с зелёным пламенем. Находиться возле него не очень приятно.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*У {user.display_name} слишком плотная шкура, нужно больше энергии, чтобы её прожечь.*")
        authbal=await bank.get_balance(author)
        cst=4000
        if authbal<cst:
            return await ctx.send (f"*У {author.display_name} загораются глаза, но запал быстро пропадает.*")
        targbal=await bank.get_balance(user)
        dmg=targbal//4
        await bank.withdraw_credits(author, cst)
        await bank.withdraw_credits(user, dmg)
        await ctx.send (f"*{author.display_name} выжигает на {user.mention} демоническое клеймо, сжигающее плоть и {dmg} золотых монет.*")

    @commands.command()
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def кэлор(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724803105161216)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} ждёт наступления ночи.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        slw=ctx.channel.slowmode_delay
        if slw>=300:
            return await ctx.send ("*Здесь действуют более мощные чары.*")
        authbal=await bank.get_balance(author)
        cst=160
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} в бессильном гневе сжимает в кулаке {authbal} золотых монет.*")
        await bank.withdraw_credits(author, cst)
        await ctx.send (f"*{author.display_name} распространяет вокруг мрак, в котором легко потеряться и плутать минут 5.*")
        await ctx.channel.edit(slowmode_delay=300)

    @commands.group(name="эраз", autohelp=False)
    async def эраз(self, ctx: commands.GuildContext):
        pass

    @эраз.command(name="закзир")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def эраз_закзир(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724803105161216)
        dmg1=random.randint(1, 100)
        dmg2=random.randint(1, 100)
        dmg3=random.randint(1, 100)
        dmg4=random.randint(1, 100)
        dmg5=random.randint(1, 100)
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается совершить акробатический трюк.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} метается из стороны в сторону, но для нескольких атак не хватает ловкости.*")
        targ1=random.choice(ctx.message.guild.members)
        while targ1==author:
            targ1=random.choice(ctx.message.guild.members)
        targ1bal=await bank.get_balance(targ1)
        if targ1bal<dmg1:
            dmg1=targ1bal
        await bank.withdraw_credits(targ1, dmg1)
        targ2=random.choice(ctx.message.guild.members)
        while targ2==author or targ2==targ1:
            targ2=random.choice(ctx.message.guild.members)
        targ2bal=await bank.get_balance(targ2)
        if targ2bal<dmg2:
            dmg2=targ2bal
        await bank.withdraw_credits(targ2, dmg2)
        targ3=random.choice(ctx.message.guild.members)
        while targ3==author or targ3==targ1 or targ3==targ2:
            targ3=random.choice(ctx.message.guild.members)
        targ3bal=await bank.get_balance(targ3)
        if targ3bal<dmg3:
            dmg3=targ3bal
        await bank.withdraw_credits(targ3, dmg3)
        targ4=random.choice(ctx.message.guild.members)
        while targ4==author or targ4==targ1 or targ4==targ2 or targ4==targ3:
            targ4=random.choice(ctx.message.guild.members)
        targ4bal=await bank.get_balance(targ4)
        if targ4bal<dmg4:
            dmg4=targ4bal
        await bank.withdraw_credits(targ4, dmg4)
        targ5=random.choice(ctx.message.guild.members)
        while targ5==author or targ5==targ1 or targ5==targ2 or targ5==targ3 or targ5==targ4:
            targ5=random.choice(ctx.message.guild.members)
        targ5bal=await bank.get_balance(targ5)
        if targ5bal<dmg5:
            dmg5=targ5bal
        await bank.withdraw_credits(targ5, dmg5)
        heal=dmg1+dmg2+dmg3+dmg4+dmg5
        if authbal>(max_bal-heal):
            heal=(max_bal-authbal)
        await bank.deposit_credits(author, heal)
        if heal==0:
            return await ctx.send(f"*{author.display_name} злится на всех сразу и впустую растрачивает свой гнев.*")
        await ctx.send (f"*{author.display_name} метается из стороны в сторону, поражая одновременными ударами клинков {targ1.mention}, {targ2.mention} и {targ3.mention}, нанося им урон на {dmg1}, {dmg2} и {dmg3} монет, соответственно, на ходу подрезая когтями кошелёк {targ4.mention}, рассыпая {dmg4} монет, и попутно вырывая зубами {dmg5} монет прямо из рук {targ5.mention}. Вернувшись на место, {author.display_name} ощущает прибавку сил и средств на {heal} золотых монет.*")

    @commands.group(name="эраде", autohelp=False)
    async def эраде(self, ctx: commands.GuildContext):
        pass

    @эраде.command(name="сарг")
    async def эраде_сарг(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724803105161216)
        ARM=discord.utils.get(ctx.guild.roles, id=765245705904062474)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} примеряет шкуру демона.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=170
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} протыкает живот шилом и облизывает с него кровь.*")
        await bank.withdraw_credits(author, cst)
        await self.getarm(user=author, role=ARM)
        await ctx.send (f"*{author.display_name} обрастает шипами и уродливыми наростами.*")

    @commands.group(name="шах", autohelp=False)
    async def шах(self, ctx: commands.GuildContext):
        pass

    @шах.command(name="кигон")
    async def шах_кигон(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724803105161216)
        MUT=discord.utils.get(ctx.guild.roles, id=687902497137885214)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} рисует на земле демонические узоры.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*{user.display_name} размещает печать немоты, но она исчезает, не сработав.*")
        authbal=await bank.get_balance(author)
        cst=180
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} с такой силой сжимает в кулаке {authbal} золотых монет, что они уходят под кожу.*")
        await bank.withdraw_credits(author, cst)
        await ctx.send(f"*{author.display_name} размещает печать немоты недалеко от себя.*")
        await asyncio.sleep(60)
        await ctx.send(f"*Печать срабатывает. Попав под её воздействие, {user.mention} немеет.*")
        await self.zadd(who=user, give=MUT)

    @commands.command()
    @commands.cooldown(10, 86400, commands.BucketType.user)
    async def маначай(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается отхлебнуть из пустой чашки.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=60
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} ощупывает пустой кисет, где хранились травы.*")
        heal=random.randint(40, 50)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if targbal>(max_bal-heal):
            heal=(max_bal-targbal)
        await bank.withdraw_credits(author, cst)
        await bank.deposit_credits(user, heal)
        await ctx.send (f"*{author.display_name} разливает ароматный маначай по чашкам. {user.mention} чувствует себя бодрее на {heal} золотых монет.*")
            
    @commands.group(name="отдать", autohelp=False)
    async def отдать(self, ctx: commands.GuildContext):
        pass

    @отдать.command(name="эль")
    async def отдать_эль(self, ctx, user: discord.Member = None):
        author = ctx.author
        ALE=discord.utils.get(ctx.guild.roles, id=860777944305631243)
        if ALE not in author.roles:
            await ctx.send (f"*{author.display_name} собирается сделать пожертвование.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        await author.remove_roles(ALE)
        if ALE in user.roles:
            return await ctx.send (f"*{author.display_name} подбрасывает бочонок эля, и тот случайно вылетает в открытое окно.*")
        await self.zadd(who=user, give=ALE)
        await ctx.send (f"*{author.display_name} бросает бочонок эля, и {user.mention} ловко его ловит.*")

    @commands.group(name="распить", autohelp=False)
    async def распить(self, ctx: commands.GuildContext):
        pass

    @распить.command(name="эль")
    async def распить_эль(self, ctx, user: discord.Member = None):
        author = ctx.author
        ALE=discord.utils.get(ctx.guild.roles, id=860777944305631243)
        if ALE not in author.roles:
            await ctx.send (f"*{author.display_name} ищет собутыльника.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        heal1=random.randint(1250, 1300)
        heal2=random.randint(1250, 1300)
        authbal=await bank.get_balance(author)
        targbal=await bank.get_balance(user)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if authbal>(max_bal-heal1):
            heal1=(max_bal-authbal)
        if targbal>(max_bal-heal2):
            heal2=(max_bal-targbal)
        heal=heal1+heal2
        await author.remove_roles(ALE)
        await ctx.send (f"*{author.display_name} откупоривает бочонок доброго эля за {heal} золотых монет и приглашает {user.mention} распить его. {author.display_name} и {user.display_name} теперь лучшие друзья!*")

    @commands.group(name="выпить", autohelp=False)
    async def выпить(self, ctx: commands.GuildContext):
        pass

    @выпить.command(name="эль")
    async def выпить_эль(self, ctx):
        author = ctx.author
        ALE=discord.utils.get(ctx.guild.roles, id=860777944305631243)
        if ALE not in author.roles:
            await ctx.send (f"*{author.display_name} мучается похмельем.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        await author.remove_roles(ALE)
        heal=random.randint(2500, 2600)
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if authbal>(max_bal-heal):
            heal=(max_bal-authbal)
        await bank.deposit_credits(author, heal)
        await ctx.send (f"*{author.display_name} откупоривает бочонок доброго эля за {heal} золотых монет и с наслаждением его опустошает!*")

    @commands.group(name="бочонок", autohelp=False)
    async def бочонок(self, ctx: commands.GuildContext):
        pass

    @бочонок.command(name="эля")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def бочонок_эля(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается унять внезапно напавшую икоту.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=1:
            return await ctx.send (f"*{author.display_name} пытается пробить крышку бочонка, но сил маловато.*")
        authbal=await bank.get_balance(author)
        cst=3500
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} заглядывает в пустые бочки в поисках хоть капли спиртного.*")
        ALE=discord.utils.get(ctx.guild.roles, id=860777944305631243)
        if ALE in user.roles:
            return await ctx.send (f"*{author.display_name} подбрасывает бочонок эля, и тот случайно вылетает в открытое окно.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=ALE)
        await ctx.send (f"*{author.display_name} бросает бочонок эля, и {user.mention} ловко его ловит.*")

    @commands.command()
    async def пошатывание(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        ARM=discord.utils.get(ctx.guild.roles, id=765245701978193920)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} сегодня навеселе.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        authbal=await bank.get_balance(author)
        cst=150
        if authbal<cst:
            return await ctx.send (f"*Бутылка выпита до дна, но {author.display_name} так и не пробрало.*")
        await bank.withdraw_credits(author, cst)
        await self.getarm(user=author, role=ARM)
        await ctx.send (f"*Хмельной туман ударяет в голову, {author.display_name} мастерски избегает всяческие невзгоды.*")

    @commands.command()
    async def трансцендентность(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        BAF=discord.utils.get(ctx.guild.roles, id=687899960066572328)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается постичь тайны бытия.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=3:
            return await ctx.send (f"*У {author.display_name} недостаточно чистые чакры.")
        authbal=await bank.get_balance(author)
        cst=350
        if authbal<cst:
            return await ctx.send (f"*Для входа в транс нужно больше энергии Ци. Где-то на {cst-authbal} монет больше.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=author, give=BAF)
        await ctx.send (f"*Духовная оболочка {author.display_name} отделяется от тела и устремляется в астральное путешествие.*")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def медитация(self, ctx):
        author = ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        BAF=discord.utils.get(ctx.guild.roles, id=687899960066572328)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} пытается сесть в позу лотоса, но левая нога постоянно выскакивает.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if BAF not in author.roles:
            return await ctx.send (f"*{author.display_name} садится в позу лотоса и пытается сосредоточиться, но какая-то назойливая муха постоянно мешает!*")
#        cur_time = calendar.timegm(ctx.message.created_at.utctimetuple())
#        next_payday = await self.config.user(author).next_payday()
#        if cur_time < next_payday:
#            dtime = self.display_time(next_payday - cur_time)
#            return await ctx.send(f"{author.display_name} совсем без сил. До следующего раза нужно отдохнуть {dtime}")
        amount=random.randint(90, 110)
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        if authbal>(max_bal-amount):
            amount=(max_bal-authbal)
        await bank.deposit_credits(author, amount)
#        next_payday = cur_time + await self.config.PAYDAY_TIME()
#        await self.config.user(author).next_payday.set(next_payday)
        await ctx.send(f"{author.display_name} погружается в транс, приводя внутренние силы в порядок. Чувствует себя сильнее на {amount} золотых монет.")

    @commands.group(name="рука", autohelp=False)
    async def рука(self, ctx: commands.GuildContext):
        pass

    @рука.command(name="копьё")
    async def рука_копьё(self, ctx, user: discord.Member = None):
        author = ctx.author
        while user is None or user is author:
            user = random.choice(ctx.message.guild.members)
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        MUT=discord.utils.get(ctx.guild.roles, id=687899619392225320)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} тренирует Адский-Проникающий-Удар-Вырывающий-Сердце в воздухе.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=5:
            return await ctx.send (f"*{author.display_name} учится правильно складывать кулак.*")
        authbal=await bank.get_balance(author)
        cst=200
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} замахивается для удара, но урчание в животе заставляет устроить быстрый перекус.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=user, give=MUT)
        await ctx.send(f"*{author.display_name} резко выбрасывает вперёд руку с вытянутыми пальцами, перебивая {user.mention} горло.*")

    @commands.group(name="духовное", autohelp=False)
    async def духовное(self, ctx: commands.GuildContext):
        pass

    @духовное.command(name="путешествие")
    async def духовное_путешествие(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        AST=discord.utils.get(ctx.guild.roles, id=772380413947543582)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} мечтает когда-нибудь попасть на другой континент.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if AST in author.roles:
            return await ctx.send (f"*{author.display_name} рассказывает историю о далёких землях.*")
        rank=await self.chkrank(ctx=ctx, user=author)
        if rank<=7:
            return await ctx.send (f"*В трудный момент {author.display_name} вспоминает слова своего учителя. В основном его ругательства.*")
        authbal=await bank.get_balance(author)
        cst=10000+(authbal//10)
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} пытается представить себя в другом месте, но голод сбивает с мысли.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=author, give=AST)
        await ctx.send (f"*Астральное тело отделяется от телесной оболочки {author.display_name} и вместе с {cst} золотыми монетами устремляется ввысь.*")

    @commands.command()
    async def возвращение(self, ctx):
        author=ctx.author
        CLS=discord.utils.get(ctx.guild.roles, id=685724800169410631)
        AST=discord.utils.get(ctx.guild.roles, id=772380413947543582)
        if CLS not in author.roles:
            await ctx.send (f"*{author.display_name} мечтает вернуться домой поскорее.*")
            return await ctx.message.delete()
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("*Защитные чары не позволяют использовать здесь это заклинание.*\nИди в <#603151774009786393> и попробуй там.")
        if AST not in author.roles:
            return await ctx.send (f"*{author.display_name} пытается быть в двух местах сразу.*")
        authbal=await bank.get_balance(author)
        astr=10000+(authbal//10)
        await bank.deposit_credits(author, astr)
        await author.remove_roles(AST)
        await ctx.send (f"*{author.display_name} меняется местами со своим астральным духом, обретая {astr} золотых монет.*")

    @commands.group(name="купить", autohelp=False)
    async def купить(self, ctx: commands.GuildContext):
        pass

    @купить.command(name="зелье")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def купить_зелье(self, ctx):
        if ctx.message.channel.id != 610767915997986816:
            return await ctx.send("Торговый автомат стоит вон там -> <#610767915997986816>.")
        author=ctx.author
        POT=discord.utils.get(ctx.guild.roles, id=685830280464039954)
        BES=discord.utils.get(ctx.guild.roles, id=687899248892706830)
        authbal=await bank.get_balance(author)
        cst=350
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} бросает {authbal} монет в Блескотрон, но они вываливаются обратно. На табло загорается цифра `{cst}`.*")
        await bank.withdraw_credits(author, cst)
        if BES in author.roles:
            await author.remove_roles(BES)
            return await ctx.send (f"*Бес на плече {author.display_name} хватает выпавший свиток и убегает, крича что-то о выполненном договоре.*")
        await self.zadd(who=author, give=POT)
        await ctx.send (f"*{author.display_name} бросает монеты в Блескотрон и забирает выпавшую склянку с зельем рассеивания чар.*")

    @купить.command(name="свиток")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def купить_свиток(self, ctx):
        if ctx.message.channel.id != 610767915997986816:
            return await ctx.send("Торговый автомат стоит вон там -> <#610767915997986816>.")
        author=ctx.author
        SCR=discord.utils.get(ctx.guild.roles, id=686206326371516498)
        BES=discord.utils.get(ctx.guild.roles, id=687899248892706830)
        authbal=await bank.get_balance(author)
        cst=400
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} бросает {authbal} монет в Блескотрон, но они вываливаются обратно. На табло загорается цифра `{cst}`.*")
        await bank.withdraw_credits(author, cst)
        if BES in author.roles:
            await author.remove_roles(BES)
            return await ctx.send (f"*Бес на плече {author.display_name} хватает выпавший свиток и убегает, крича что-то о выполненном договоре.*")
        await self.zadd(who=author, give=SCR)
        await ctx.send (f"*{author.display_name} бросает монеты в Блескотрон и забирает выпавший свиток с заклинанием Антимагии.*")

    @выпить.command(name="зелье")
    async def выпить_зелье(self, ctx):
        if ctx.message.channel.id != 610767915997986816 and ctx.message.channel.id != 603151774009786393:
            return await ctx.send("Со своими напитками нельзя! Можешь выпить своё зелье тут -> <#610767915997986816> или тут -> <#603151774009786393>.")
        author=ctx.author
        POT=discord.utils.get(ctx.guild.roles, id=685830280464039954)
        if POT in author.roles:
            await author.remove_roles(POT)
            await ctx.send (f"*{author.display_name} залпом осушает бутылку зелья, которое выжигает все следы наложенных чар.*")
            await self.deleff(ctx=ctx, user=author)
        else:
            await ctx.send (f"*{author.display_name} прикладывается к бутылке, но она оказывается пустой.*\nСдайте пустую тару!")

    @commands.group(name="прочесть", autohelp=False)
    async def прочесть(self, ctx: commands.GuildContext):
        pass

    @прочесть.command(name="свиток")
    async def прочесть_свиток(self, ctx):
        if ctx.message.channel.id != 603151774009786393:
            return await ctx.send("Защитные чары не позволяют использовать здесь этот свиток. Иди в <#603151774009786393> и читай там.")
        author=ctx.author
        SCR=discord.utils.get(ctx.guild.roles, id=686206326371516498)
        if SCR in author.roles:
            await author.remove_roles(SCR)
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send (f"*{author.display_name} разворачивает свиток и читает написанное на нём заклинание. Вспыхнувшие в воздухе руны разлетаются, уничтожая любое магическое заклятие на своём пути.*")
        else:
            await ctx.send (f"*{author.display_name} разворачивает свиток, но он оказывается девственно чист.*")

    @купить.command(name="пропуск")
    async def купить_пропуск(self, ctx):
        if ctx.message.channel.id != 610767915997986816:
            return await ctx.send("Торговый автомат стоит вон там -> <#610767915997986816>.")
        author=ctx.author
        VIP=discord.utils.get(ctx.guild.roles, id=832557988401119243)
        authbal=await bank.get_balance(author)
        cst=10
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} бросает {authbal} монет в Блескотрон, но они вываливаются обратно. На табло загорается цифра `{cst}`.*")
        await bank.withdraw_credits(author, cst)
        await self.zadd(who=author, give=VIP)
        await ctx.send (f"*{author.display_name} бросает монеты в Блескотрон и забирает подозрительно тикающий VIP-пропуск на VIP-каналы.*")

    @commands.group(name="выбросить", autohelp=False)
    async def выбросить(self, ctx: commands.GuildContext):
        pass

    @выбросить.command(name="пропуск")
    async def выбросить_пропуск(self, ctx):
        author=ctx.author
        VIP=discord.utils.get(ctx.guild.roles, id=832557988401119243)
        if VIP in author.roles:
            await author.remove_roles(VIP)
            room=self.bot.get_channel(603151774009786393)
            await room.send (f"*Где-то прогремел взрыв. Высоко в небе можно разглядеть {author.display_name}.*")
        else:
            await ctx.send (f"*Где-то прогремел взрыв. {author.display_name} не имеет к этому никакого отношения.*")
            return await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def блескотрон(self, ctx):
        author = ctx.author
        enc=self.bot.get_emoji(921290887651291146)
        magic=self.bot.get_emoji(893780879648894987)
        gob=self.bot.get_emoji(732590031981641789)
#       if ctx.message.channel.id != 610767915997986816:
#           return await ctx.send("Торговый автомат стоит вон там -> <#610767915997986816>.")
        emb0 = discord.Embed(title=f"*{author.display_name} подходит к торговому автомату 'Блескотрон-800' и рассматривает его разбитое табло.*", colour=discord.Colour.gold())
        emb0.set_thumbnail(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
        emb1 = discord.Embed(title="Товары Анклава Солнца и Луны.", description = "*Выберите товар, деньги будут сняты со счёта автоматически.*\n\n1. Читательский билет - даёт доступ на канал сокрытой библиотеки раздела Хранителей историй.\nСтоимость - 150 монет.\n\n2. VIP-пропуск - даёт доступ к расширенному журналу аудита сервера (все изменения и удаления сообщений, посещения голосовых каналов, фотографии участников через веб-камеры и т.п.) и каналу гоблинской книги, где можно оставить свои пожелания и предложения по устройству сервера или последить за гоблинской активностью.\nСтоимость - 10 монет и временная потеря доступа к остальным каналам (на время использования VIP-пропуска).\n*Не забудьте команду `=выбросить пропуск`!*\n\n3.Выбрать другую фракцию.\nСтоимость - 100 монет.\n\n4. Выбрать другой класс.\nСтоимость - 1000 монет.", colour=discord.Colour.gold())
        emb1.set_thumbnail(url="https://cdn.discordapp.com/emojis/921290887651291146.png")
        emb2 = discord.Embed(title="Магические товары и услуги.", description = "*Выберите товар, деньги будут сняты со счёта автоматически.*\n*Нижеприведённые команды допускается использовать на канале <#610767915997986816> в качестве исключения.*\n\n1. <@&685830280464039954> - зелье рассеивает любые эффекты наложенные на вас.\nСтоимость - 350 монет.\n*Не забудьте команду `=выпить зелье`!*\n\n2. <@&686206326371516498> - свиток рассеивает замедляющие чары, наложенные на канал.\nСтоимость - 400 монет.\n*Не забудьте команду `=прочесть свиток`!*", colour=discord.Colour.gold())
        emb2.set_thumbnail(url="https://cdn.discordapp.com/emojis/893780879648894987.png")
        emb3 = discord.Embed(title="Товары от Оззи К.", description = "*Договариваться лично!*\n\n1. Наследный аксессуар 'Касание Бездны'. Любой сервер - привязывается к аккаунту.\nСтоимость - от 400 монет.\n\n2. Один дейлик на 1500 опыта в Hearthstone.\nПокупка - от 500 монет, продажа - цена договорная.", colour=discord.Colour.gold())
        emb3.set_thumbnail(url="https://cdn.discordapp.com/emojis/732590031981641789.png")
        msg = await ctx.send(embed=emb0, components=[Select(placeholder="Выбрать категорию товаров:", options=[SelectOption(label="Всё для дома", value="enc", emoji=enc), SelectOption(label="Всё для магии", value="mag", emoji=magic), SelectOption(label="Гоблинские товары", value="ozzi", emoji=gob)])])
        embed=emb0
        while True:
            try:
                interaction = await self.bot.wait_for("select_option", check = lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(embed=emb0, components = [])
            await interaction.edit_origin()
            if interaction.values[0] == 'enc':
                embed=emb1
                await msg.edit(embed=embed, components = [[Button(style = ButtonStyle.blue, label = 'Читательский билет'), Button(style = ButtonStyle.blue, label = 'VIP-пропуск'), Button(style = ButtonStyle.blue, label = 'Сменить фракцию'), Button(style = ButtonStyle.blue, label = 'Сменить класс'), Button(style = ButtonStyle.blue, label = 'Вернуться к покупкам.')]])
            elif interaction.values[0] == 'mag':
                embed=emb2
                await msg.edit(embed=embed, components = [[Button(style = ButtonStyle.green, label = 'Зелье рассеивания чар'), Button(style = ButtonStyle.green, label = 'Свиток антимагии'), Button(style = ButtonStyle.green, label = 'Вернуться к покупкам.')]])
            elif interaction.values[0] == 'ozzi':
                embed=emb3
                await msg.edit(embed=embed, components = [[Button(style = ButtonStyle.red, label = 'Связаться с гоблином'), Button(style = ButtonStyle.red, label = 'Вернуться к покупкам.')]])
            else:
                return
            try:
                responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=60)
            except asyncio.TimeoutError:
                return await msg.edit(embed=embed, components = [])
            await responce.edit_origin()
            if responce.component.label == 'Читательский билет':
                emb = discord.Embed(title='*Бип-буп-бип.*', colour=discord.Colour.gold())
                emb.set_image(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
                await msg.edit(embed=emb, components=[])
                return await self.читательский_билет(ctx)
            elif responce.component.label == 'VIP-пропуск':
                emb = discord.Embed(title='*Бип-буп-тик-так.*', colour=discord.Colour.gold())
                emb.set_image(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
                await msg.edit(embed=emb, components=[])
                return await self.купить_пропуск(ctx)
            elif responce.component.label == 'Сменить фракцию':
                emb = discord.Embed(title='*Бип-буп-бррр.*', colour=discord.Colour.gold())
                emb.set_image(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
                await msg.edit(embed=emb, components=[])
                return await self.сменить_фракцию(ctx)
            elif responce.component.label == 'Сменить класс':
                emb = discord.Embed(title='*Бип-буп-бззз.*', colour=discord.Colour.gold())
                emb.set_image(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
                await msg.edit(embed=emb, components=[])
                return await self.сменить_класс(ctx)
            elif responce.component.label == 'Зелье рассеивания чар':
                emb = discord.Embed(title='*Бип-буп-дзынь.*', colour=discord.Colour.gold())
                emb.set_image(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
                await msg.edit(embed=emb, components=[])
                return await self.купить_зелье(ctx)
            elif responce.component.label == 'Свиток антимагии':
                emb = discord.Embed(title='*Бип-бип-буп.*', colour=discord.Colour.gold())
                emb.set_image(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
                await msg.edit(embed=emb, components=[])
                return await self.купить_свиток(ctx)
            elif responce.component.label == 'Связаться с гоблином':
                emb = discord.Embed(title='*Бип-буп-бам.*', colour=discord.Colour.gold())
                emb.set_image(url="https://media.discordapp.net/attachments/921279850956877834/921280721803415572/59042.jpg")
                nom=random.randint(1, 9000000)
                await ctx.send(f"Ваше обращение зарегистрировано под номером {nom}. Вам ответит первый освободившийся гоблин.")
                return await msg.edit(embed=emb, components=[])
            else:
                await msg.edit(embed=emb0, components=[Select(placeholder="Выбрать категорию товаров:", options=[SelectOption(label="Всё для дома", value="enc", emoji=enc), SelectOption(label="Всё для магии", value="mag", emoji=magic), SelectOption(label="Гоблинские товары", value="ozzi", emoji=gob)])])

    @commands.group(name="читательский", autohelp=False)
    async def читательский(self, ctx: commands.GuildContext):
        pass

    @читательский.command(name="билет")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def читательский_билет(self, ctx):
        if ctx.message.channel.id != 610767915997986816:
            return await ctx.send("Торговый автомат стоит вон там -> <#610767915997986816>.")
        author=ctx.author
        TICK=discord.utils.get(ctx.guild.roles, id=616665313123406827)
        BES=discord.utils.get(ctx.guild.roles, id=687899248892706830)
        authbal=await bank.get_balance(author)
        cst=150
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} бросает {authbal} монет в Блескотрон, но они вываливаются обратно. На табло загорается цифра `{cst}`.*")
        await bank.withdraw_credits(author, cst)
        if BES in author.roles:
            await author.remove_roles(BES)
            return await ctx.send (f"*Бес на плече {author.display_name} хватает выпавший билет и убегает в библиотеку, крича что-то о выполненном договоре.*")
        await self.zadd(who=author, give=TICK)
        await ctx.send (f"*{author.display_name} бросает монеты в Блескотрон и забирает выпавший читательский билет в сокрытую библиотеку.*")

    @commands.group(name="сменить", autohelp=False)
    async def сменить(self, ctx: commands.GuildContext):
        pass

    @сменить.command(name="фракцию")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def сменить_фракцию(self, ctx):
        if ctx.message.channel.id != 610767915997986816:
            return await ctx.send("Торговый автомат стоит вон там -> <#610767915997986816>.")
        author=ctx.author
        HORD=discord.utils.get(ctx.guild.roles, id=583992582447693834)
        ALLY=discord.utils.get(ctx.guild.roles, id=583992639968378880)
        NEUT=discord.utils.get(ctx.guild.roles, id=583992930394570776)
        authbal=await bank.get_balance(author)
        cst=100
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} бросает {authbal} монет в Блескотрон, но они вываливаются обратно. На табло загорается цифра `{cst}`.*")
        await bank.withdraw_credits(author, cst)
        for r in HORD, ALLY, NEUT:
            if r in author.roles:
                await author.remove_roles(r)
                embed = discord.Embed(title = f'*{author.display_name} переосмысливает свою принадлежность к фракции.*', colour=discord.Colour.gold())
                msg = await ctx.send(embed=embed, components = [[Button(style = ButtonStyle.blue, label = 'За Альянс!'), Button(style = ButtonStyle.red, label = 'За Орду!'), Button(style = ButtonStyle.green, emoji = label = 'За Азерот!')]])
                try:
                    responce = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author, timeout=30)
                except asyncio.TimeoutError:
                    return await msg.edit(embed=embed, components = [])
                await responce.edit_origin()
                if responce.component.label == 'За Альянс!':
                    embed = discord.Embed(title = f'*{author.display_name} встаёт на сторону доблестных воинов Альянса.*', colour=discord.Colour.gold())
                    await self.zadd(who=author, give=ALLY)
                    return await msg.edit(embed=embed, components = [])
                elif responce.component.label == 'За Орду!':
                    embed = discord.Embed(title = f'*{author.display_name} присоединяется к воинственным сынам Орды.*', colour=discord.Colour.gold())
                    await self.zadd(who=author, give=HORD)
                    return await msg.edit(embed=embed, components = [])
                elif responce.component.label == 'За Азерот!':
                    embed = discord.Embed(title = f'*{author.display_name} считает, что Азерот - наш общий дом.*', colour=discord.Colour.gold())
                    await self.zadd(who=author, give=NEUT)
                    return await msg.edit(embed=embed, components = [])
                else:
                    return
        return await ctx.send ("Роль фракции можно выбрать на канале <#675969784965496832>.")

    @сменить.command(name="класс")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def сменить_класс(self, ctx):
        if ctx.message.channel.id != 610767915997986816:
            return await ctx.send("Торговый автомат стоит вон там -> <#610767915997986816>.")
        author=ctx.author
        C1=discord.utils.get(ctx.guild.roles, id=685724787397361695)#war
        C2=discord.utils.get(ctx.guild.roles, id=685724790425649157)#hunt
        C3=discord.utils.get(ctx.guild.roles, id=685724791914758147)#rog
        C4=discord.utils.get(ctx.guild.roles, id=685724793567444995)#pal
        C5=discord.utils.get(ctx.guild.roles, id=685724794586398761)#dru
        C6=discord.utils.get(ctx.guild.roles, id=685724796075769889)#sham
        C7=discord.utils.get(ctx.guild.roles, id=685724798193762365)#mage
        C8=discord.utils.get(ctx.guild.roles, id=685724797266952219)#priest
        C9=discord.utils.get(ctx.guild.roles, id=685724799527551042)#lock
        C10=discord.utils.get(ctx.guild.roles, id=685724801486290947)#dk
        C11=discord.utils.get(ctx.guild.roles, id=685724800169410631)#monk
        C12=discord.utils.get(ctx.guild.roles, id=685724803105161216)#dh
        R0=discord.utils.get(ctx.guild.roles, id=687903691587846158)#от Ученика 1
        R1=discord.utils.get(ctx.guild.roles, id=696008498764578896)#2
        R2=discord.utils.get(ctx.guild.roles, id=687903789457735680)#3
        R3=discord.utils.get(ctx.guild.roles, id=696008500240973885)#4
        R4=discord.utils.get(ctx.guild.roles, id=687903789843218457)#5
        R5=discord.utils.get(ctx.guild.roles, id=696008502497378334)#6
        R6=discord.utils.get(ctx.guild.roles, id=687903807405162506)#7
        R7=discord.utils.get(ctx.guild.roles, id=696008504153997322)#8
        R8=discord.utils.get(ctx.guild.roles, id=687903808268927002)#9
        R9=discord.utils.get(ctx.guild.roles, id=687904030713708575)#до Эксперта 10
        authbal=await bank.get_balance(author)
        cst=1000
        if authbal<cst:
            return await ctx.send (f"*{author.display_name} бросает {authbal} монет в Блескотрон, но они вываливаются обратно. На табло загорается цифра `{cst}`.*")
        await bank.withdraw_credits(author, cst)
        for r in C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12:
            if r in author.roles:
                for RAN in R0, R1, R2, R3, R4, R5, R6, R7, R8, R9:
                    if RAN in author.roles:
                        await author.remove_roles(RAN)
                await author.remove_roles(r)
                await ctx.send (f"*{author.display_name} забывает все свои навыки и отправляется к классовому тренеру.*")
                return self.выбрать_класс(ctx)
        return await ctx.send ("Получить роль класса может любой желающий, отправив команду:\n`=выбрать класс`")