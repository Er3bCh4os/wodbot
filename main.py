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


@bot.command()
async def combat(ctx):
    await ctx.send('Для броска инициативы нужно написать ' + settings['prefix'] + 'inc цифра')
    await ctx.send('Для броска урона нужно написать ' + settings['prefix'] + 'd кол-во успехов')
# global results list

result = []
pros = []
cons = []


def check_ten(cube: int):  # additional roll check for 10
    if cube == 10:
        result.append(cube)
        pros.append(cube)
        check_ten(random.randint(1, 10))
    else:
        result.append(cube)
        return


@bot.command()
async def d(ctx, dice: int):
    global result, pros, cons
    result, pros = [], []  # nullification of lists
    for i in range(dice):
        cube = random.randint(1, 10)
        check_ten(cube)
        if cube >= 6 and cube != 10:  # difficulty check
            pros.append(cube)
    await ctx.send(result)
    print(len(pros))  # debug info
    if len(pros) <= 0:
        await ctx.send('Неудача!')
    else:
        await ctx.send(str(len(pros)-len(cons))+' урона нанесено')


@bot.command()
async def r(ctx, dice: int, dif: int):
    global result, pros, cons
    result, pros, cons = [], [], []  # nullification of lists
    for i in range(dice):
        cube = random.randint(1, 10)
        check_ten(cube)
        if cube >= dif and cube != 10:  # difficulty check
            pros.append(cube)
        if cube == 1:  # failure check
            cons.append(cube)
    await ctx.send(result)
    print(len(cons), len(pros))  # debug info
    if len(cons) >= 1 and len(pros) == 0:
        await ctx.send('Провал!')
    elif len(pros) - len(cons) <= 0:
        await ctx.send('Неудача!')
    else:
        await ctx.send(str(len(pros)-len(cons))+' успеха(ов)!')


@bot.command()
async def lu(ctx):  # lucky throw
    cube = random.randint(1, 10)
    if cube == 10:
        await ctx.send('Получилось!')
    elif cube == 1:
        await ctx.send('Критический провал...')
    else:
        await ctx.send('Провал...')


@bot.command()
async def inc(ctx, init: int):
    rnd = random.randint(1, 10)
    await ctx.send("Инициатива: ["+str(rnd+init)+"]")

bot.run(settings['token'])
