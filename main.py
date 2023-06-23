import discord
import random
from discord.ext import commands
from config import settings
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


@bot.command()
async def helper(ctx):
    await ctx.send('Для броска необходимо написать '+settings['prefix']+'r и два числа через пробел')
    await ctx.send('Первое число - это количество кубов, а второе - сложность броска.')
    await ctx.send('Пример броска: '+settings['prefix']+'r 2 6')
    await ctx.send('Для броска на удачу нужно написать ' + settings['prefix'] + 'lu')

result = []


def check_ten(cube: int):
    if cube == 10:  # additional roll
        result.append(cube)
        check_ten(random.randint(1, 10))
    else:
        result.append(cube)
        return


@bot.command()
async def r(ctx, dice: int, dif: int):
    global result
    result, pros, cons = [], [], []  # initial roll list and +/- lists
    # count = 0  # cycle counter
    for i in range(dice):
        cube = random.randint(1, 10)
        # result.append(cube)
        check_ten(cube)
        # count += 1
        if cube >= dif:  # difficulty check
            pros.append(cube)
        if cube == 1:  # failure check
            cons.append(1)
    await ctx.send(result)
    print(len(cons), len(pros))  # debug info
    if len(cons) >= 1 and len(pros) == 0:
        await ctx.send('Провал!')
    elif len(pros) - len(cons) <= 0:
        await ctx.send('Неудача!')
    else:
        await ctx.send(str(len(pros)-len(cons))+' успеха(ов)!')


@bot.command()
async def lu(ctx):
    cube = random.randint(1, 10)
    if cube == 10:
        await ctx.send('Получилось')
    elif cube == 1:
        await ctx.send('Критический провал...')
    else:
        await ctx.send('Провал...')

bot.run(settings['token'])
