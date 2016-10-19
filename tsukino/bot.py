import asyncio
import logging
import shlex
import time
import inspect
import random
import urllib.request
import urllib.parse
import os
import json

import discord
from googleapiclient.discovery import build

from .config import Config
from .data import botVersion, helpText, changeLog, aboutText, introText, randomText
from .exception import CommandError
from .response import Response
from . import poker


samLen = len([name for name in os.listdir('images/sammy/') if os.path.splitext(name)[1] == '.jpg'])
ratLen = len([name for name in os.listdir('images/rats/') if os.path.splitext(name)[1] == '.jpg'])
husLen = len([name for name in os.listdir('images/husky/') if os.path.splitext(name)[1] == '.jpg'])
shiLen = len([name for name in os.listdir('images/shibe/') if os.path.splitext(name)[1] == '.jpg'])
corLen = len([name for name in os.listdir('images/corg/') if os.path.splitext(name)[1] == '.jpg'])

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
service = build("customsearch", "v1", developerKey="AIzaSyBUozaYC1n5QT1wuwfT-2SdFciHjO6nUn8")
# I hate Google custom search.

class Tsukino(discord.Client):
    '''
        A modified Discord client.
        Shamelessly based on SexualRhinoceros's way of making one.
    '''
    def __init__(self, config_file='config/config.ini'):
        super().__init__()
        
        self.config = Config(config_file)
        self.game_channels = []
        
    def run(self):
        return super().run(self.config.token)
        
    async def on_ready(self):
        print('Logged in as %s with ID %s at %s' % (self.user.name, self.user.id, time.asctime(time.localtime())))
        print('Bot version: v' + botVersion)
        print('I am online in %s servers.' % len(self.servers))
        await self.change_presence(game=discord.Game(name='{}help'.format(self.config.prefix)))
        
    async def on_server_join(self, server):
        log.info('Joined a new server, {} ({})'.format(server.name, server.id))
        try:
            await self.send_message(server, introText.format(prefix=self.config.prefix))
        except discord.Forbidden:
            log.info('Tried to send a forbidden intro message.')
        
    async def cmd_hello(self):
        '''
        Hello! How are you?
        '''
        return Response(introText.format(prefix=self.config.prefix))
        
    async def cmd_ily(self):
        '''
        I love you <3
        '''
        return Response('ily2')
        
    async def cmd_help(self, cmd=None):
        '''
        Try `help [command]` to learn about a certain command.
        '''
        if not cmd:
            return Response(helpText.format(prefix=self.config.prefix), private=True)
        else:
            handle = getattr(self, 'cmd_%s' % cmd, None)
            
            if not handle:
                raise CommandError('Oops, no command with that name exists.')
                
            docs = getattr(handle, '__doc__', None)
            docs = '\n'.join(l.strip() for l in docs.split('\n'))
            
            if not docs:
                return Response('That command doesn\'t have any help text. Try using it!')
            else:
                return Response(docs)
    
    async def cmd_about(self):
        '''
        Do you want to know more about me or something?
        '''
        return Response(aboutText)
        
    async def cmd_changelog(self):
        '''
        I change pretty frequently, just like any other girl.
        '''
        return Response(changeLog)
        
    async def cmd_invite(self):
        '''
        Invite me to your other servers or something.
        '''
        return Response('https://discordapp.com/oauth2/authorize?&client_id=170281668773412865&scope=bot')
        
    async def cmd_ping(self, message):
        '''
        I couldn't think of a witty response to put here.
        '''
        msg = await self.send_message(message.channel, 'Pong!')
        differ = (message.timestamp - msg.timestamp)
        await self.edit_message(msg, 'Pong! {:d}ms'.format(int(differ.microseconds/1000)))
        
    async def cmd_choose(self, args=None):
        '''
        Select from a variable number of choices at random. "Quotation marks" can be used to group multiple words together.
        `choose [choice 1] [choice 2] etc.`
        '''
        if args:
            return Response(random.choice(args))
        else:
            raise CommandError('Oops, you need to supply me with choices. `choose [choices]`')
        
    async def cmd_yikes(self):
        '''
        yikerino
        '''
        return Response('images/yikes.JPG', file=True)
        
    async def cmd_eval(self, args=None):
        '''
        Type some sort of thing you'd put in Google to do math for you.
        `eval [expression]`
        '''
        if args:
            query = ' '.join(args)
            response = urllib.request.urlopen('https://www.calcatraz.com/calculator/api?c=' + urllib.parse.quote(query))
            if response.read().decode('utf-8').strip() == 'answer':
                raise CommandError('Oops, I couldn\'t find a suitable answer for that.')
            else:
                return Response(response.read().decode('utf-8').strip())
        else:
            raise CommandError('Oops, you need to supply me with an expression to evaluate. `eval [expression]`')
        
    async def cmd_image(self, args=None):
        '''
        Perform a Google Image search, returning the first 3 images I find from it.
        Please note that I am limited to 100 searches per day because Google wants my money to use their API.
        `image [search]`
        '''
        if args:
            try:
                query = ' '.join(args)
                res = service.cse().list(q=query, cx='014997929530961218084:xt2x2idcvzk', searchType = 'image', num = 3, safe='high').execute()
                return Response('{}\n{}\n{}'.format(res['items'][0]['link'], res['items'][1]['link'], res['items'][2]['link']))
            except KeyError:
                raise CommandError('I didn\'t find any results for that query.')
        else:
            raise CommandError('Oops, you need to supply me with an image query to search. `image [query]`')
            
    async def cmd_ximage(self, args=None):
        '''
        Do the same thing as `image`, but with SafeSearch off.
        `ximage [search]`
        '''
        if args:
            try:
                query = ' '.join(args)
                res = service.cse().list(q=query, cx='014997929530961218084:xt2x2idcvzk', searchType = 'image', num = 3, safe='off').execute()
                return Response('{}\n{}\n{}'.format(res['items'][0]['link'], res['items'][1]['link'], res['items'][2]['link']))
            except KeyError:
                raise CommandError('I didn\'t find any results for that query.')
        else:
            raise CommandError('Oops, you need to supply me with an image query to search. `ximage [query]`')
            
    async def cmd_samoyed(self):
        foo = random.randint(1, samLen)
        return Response('images/sammy/sam (%s).jpg' % foo, file=True)
        
    async def cmd_shiba(self):
        foo = random.randint(1, shiLen)
        return Response('images/shibe/shibe (%s).jpg' % foo, file=True)
        
    async def cmd_husky(self):
        foo = random.randint(1, husLen)
        return Response('images/husky/husk (%s).jpg' % foo, file=True)
        
    async def cmd_corgi(self):
        foo = random.randint(1, corLen)
        return Response('images/corg/corg (%s).jpg' % foo, file=True)
        
    async def cmd_rat(self):
        foo = random.randint(1, ratLen)
        return Response('images/rats/rat (%s).jpg' % foo, file=True)
            
    async def cmd_random(self, cmd=None, arg1=None, arg2=None):
        '''
        Perform a variety of random functions. `random help` to receive a list of them.
        `random [command]`
        '''
        if not cmd:
            raise CommandError('Oops, you have to specify what random function you want me to do. Try checking `random help` for more info.')
        elif cmd == 'help':
            return Response(randomText.format(prefix=self.config.prefix), private=True)
        elif cmd not in ['samoyed', 'shiba', 'husky', 'corgi', 'rat', 'range', 'dice', 'rival', 'weapon']:
            return
        elif cmd == 'samoyed':
            return await self.cmd_samoyed()
        elif cmd == 'shiba':
            return await self.cmd_shiba()
        elif cmd == 'husky':
            return await self.cmd_husky()
        elif cmd == 'corgi':
            return await self.cmd_corgi()
        elif cmd == 'rat':
            return await self.cmd_rat()
        elif cmd == 'range':
            if not arg1:
                raise CommandError('Oops, you need to specify a range. `random range [lower] [upper]`')
            elif not arg2:
                raise CommandError('Oops, you need to specify the upper range. `random range [lower] [upper]`')
            elif arg1 and arg2:
                try:
                    result = random.randint(int(arg1), int(arg2))
                    return Response(result)
                except ValueError:
                    raise CommandError('Oops, the ranges to be integers.')
        elif cmd == 'dice':
            try:
                times, sides = map(int, arg1.split('d'))
                bar = []
                for i in range(times):
                    foo = str(random.randint(1, sides))
                    bar.append(foo)
                return Response(', '.join(bar))
            except:
                raise CommandError('Oops, you have to give me dice in NdN format. `random dice NdN`')
        elif cmd == 'rival':
            foo = random.randint(0, 7)
            rivals = ['Forsburn', 'Zetterburn', 'Wrastor', 'Absa', 'Maypul', 'Kragg', 'Orcane', 'Etalus']
            return Response(rivals[foo])
        elif cmd == 'weapon':
            baz = random.randint(0, 13)
            if baz == 13:
                return Response('Prowler')
            else:
                styles = ['Guild', 'Adept', 'Aerial', 'Striker']
                weapons = ['Great Sword', 'Long Sword', 'Sword and Shield', 'Hammer', 'Hunting Horn', 'Lance', 'Gunlance', 'Switch Axe', 'Charge Blade', 'Insect Glaive', 'Bow', 'Light Bowgun', 'Heavy Bowgun']
                foo = random.randint(0, 3)
                return Response('{} {}'.format(styles[foo], weapons[baz]))
                
    async def add_to_coin(self, user, fr):
        fr[user.id] = 100
        with open('config/coins.json', 'w') as fo:
            json.dump(fr, fo, indent=4, sort_keys=True)
        return Response('{} has joined the coin party! You start off with 100 coins.'.format(user.name))
                
    async def cmd_coins(self, message, arg1=None, arg2=None, arg3=None):
        '''
        Perform coin management-related commands. `coins help` to receive a list of them.
        `coins [commamd]`
        '''
        if not arg1:
            with open('config/coins.json', 'r') as fp:
                fr = json.load(fp)
                if message.author.id in fr:
                    return Response('{} has {} coins in their inventory.'.format(message.author.name, fr[message.author.id]))
                else:
                    return await self.add_to_coin(message.author, fr)
        elif arg1 == 'help':
            return Response('`give [amount] [username]` Donate your coins to another user. Please note you must use their actual username, and not the server\'s nickname. If there are spaces in their name, wrap their name in quotation marks. If two people have the same name, use the `name#0000` format to pick out a specific person.', private=True)
        elif arg1 == 'give':
            if arg2:
                try:
                    if isinstance(int(arg2), int):
                        arg2 = int(arg2)
                        if arg3:
                            user = message.server.get_member_named(arg3)
                        else:
                            raise CommandError('Oops, you need a name in the second field. `give [amount] [username]`')
                        if user:
                            with open('config/coins.json', 'r') as fp:
                                fr = json.load(fp)
                                if message.author.id in fr:
                                    amount = fr[message.author.id]
                                else:
                                    await self.send_message(message.channel, 'Oops, looks like you haven\'t joined the coin party yet! I\'ll add you right now.')
                                    return await add_to_coin(message.author, fr)
                            if arg2 < 0:
                                raise CommandError('Hey, you can\'t give a negative amount!')
                            if arg2 > amount:
                                raise CommandError('Oops, looks like you don\'t have enough coins to give that many.')
                            with open('config/coins.json', 'r') as fp:
                                fr = json.load(fp)
                                if user.id in fr:
                                    fr[message.author.id] -= arg2
                                    fr[user.id] += arg2
                                    with open('config/coins.json', 'w') as fo:
                                        json.dump(fr, fo, indent=4, sort_keys=True)
                                    return Response('Successfully gave {} {} of {}\'s coins!'.format(user.name, arg2, message.author.name))
                                else:
                                    await self.send_message(message.channel, 'Oops, {} is not in the coin party. I will add them right now. You will need to use the `coin` function again.'.format(user.name))
                                    return await self.add_to_coin(user, fr)
                        else:
                            raise CommandError('Oops, that person does not exist. Please note names are case-sensitive. `give [amount] [username]`')
                except ValueError:
                    raise CommandError('Oops, that amount isn\'t an integer. `give [amount] [username]`')
            else:
                raise CommandError('Oops, you didn\'t tell me the amount or who to give it to. `give [amount] [username]`')
                
    async def cmd_slots(self, message, bet=None):
        '''
        Play a simple games of slots.
        Match two of any kind to get your coins back.
        Match three to get double ($), triple ($$), or quadruple ($$$) your coins back.
        `slots [bet]`
        '''
        if bet:
            try:
                bet = int(bet)
            except ValueError:
                raise CommandError('Oops, your bet needs to be a number. `slots [bet]`')
                
            if bet < 0:
                return Response('Hey, you can\'t put negative coins in the machine! Are you trying to cheat?')
                
            with open('config/coins.json', 'r') as fp:
                fr = json.load(fp)
                if message.author.id in fr:
                    coins = fr[message.author.id]
                else:
                    await self.send_message(message.channel, 'Oops, looks like you\'re not in the coin party! I\'ll add you right now.')
                    return await self.add_to_coin(message.author, fr)
                    
            if bet > coins:
                return Response('That\'s a bit much, isn\'t it? Try a smaller bet. (Preferably one you can afford.) You have {} coins.'.format(coins))
                
            coins -= bet
                
            line1 = random.randint(1, 4)
            line2 = random.randint(1, 4)
            line3 = random.randint(1, 4)
            
            slot = {
                1 : '   ',
                2 : ' $ ',
                3 : '$ $',
                4 : '$$$',
            }
            
            win = 0
            
            if (line1 == line2 and line1 != 1) or (line1 == line3 and line1 != 1) or (line2 == line3 and line2 != 1):
                win = bet
            elif line1 == 2 and line2 == 2 and line3 == 2:
                win = bet * 2
            elif line1 == 3 and line2 == 3 and line3 == 3:
                win = bet * 3
            elif line1 == 4 and line2 == 4 and line3 == 4:
                win = bet * 4
                
            coins += win
            fr[message.author.id] = coins

            with open('config/coins.json', 'w') as fo:
                json.dump(fr, fo, indent=4, sort_keys=True)
                
            return Response('```| {} | {} | {} |```\nYou win {} coins!'.format(slot[line1], slot[line2], slot[line3], win))
        else:
            raise CommandError('Oops, you need to give me a bet! `slots [bet]`')
            
    async def cmd_poker(self, message, cmd=None):
        '''
        Play poker with your friends! Try `poker help` to display the rankings of different hands. 
        `poker [bet]`
        '''
        if message.channel.is_private:
            return Response('Did you just try to start a poker game in our private messages? Go find some friends to play with!')
            
        if message.channel.id in self.game_channels:
            return Response('You can\'t start multiple games at once! You\'re pretty silly. Try playing in a different channel if you really want to.')
            
        if cmd == 'help':
            return Response('http://www.24pokersite.com/wp-content/uploads/2011/01/Poker-_Hand_Chart.gif')
        elif not cmd:
            raise CommandError('Oops, you need to specify a starting bet! `poker [bet]`')
        else:
            try:
                bet = int(cmd)
            except ValueError:
                raise CommandError('Oops, your starting bet needs to be an integer! `poker [bet]`')
            if bet < 0:
                return Response('Hey, you can\'t start a game with a negative bet! Are you trying to cheat?')
                
            with open('config/coins.json', 'r') as fp:
                fr = json.load(fp)
                if message.author.id in fr:
                    coin = fr[message.author.id]
                else:
                    await self.send_message(message.channel, 'Oops, looks like you\'re not in the coin party! I\'ll add you right now.')
                    return await self.add_to_coin(message.author, fr)
            
            if coin < bet * 2:
                return Response('Oops, you don\'t have enough coins to play with a bet that high! Try starting a new game with a lower bet.')
                
            self.game_channels.append(message.channel.id)
            
            players = [message.author]
            await self.send_message(message.channel, '{} has joined the game.\nAnyone who wants to join, type `join`\nWe need at least 1 more person, and up to 4 can join!\nType `cancel` in this channel at any time during the signup period to cancel the game.'.format(message.author.name))
            
            def joinFirst(msg):
                if msg.content in ('%sjoin' % self.config.prefix, '%scancel' % self.config.prefix):
                    return True
            
            while True:
                msg = await self.wait_for_message(check=joinFirst, channel=message.channel)
                
                if msg.content == '%scancel' % self.config.prefix:
                    self.game_channels.remove(message.channel.id)
                    return Response('The game has been cancelled.')
                    
                if msg.author in players:
                    await self.send_message(message.channel, 'Hey, you\'re already in the game! Someone else, please?')
                else:
                    with open('config/coins.json', 'r') as fp:
                        fr = json.load(fp)
                        if msg.author.id in fr:
                            coin = fr[msg.author.id]
                        else: 
                            await self.send_message(message.channel, 'Oops, looks like you haven\'t joined the coin party yet! I\'ll add you right now.')
                            response = await self.add_to_coin(msg.author, fr)
                            await self.send_message(message.channel, response.content)
                            coin = 100
                    if coin < bet * 2:
                        await self.send_message(message.channel, 'Oops, it looks like you don\'t have enough coins to play! Either get some richer friends, or `cancel` the game and start with a lower bet.')
                    else:
                        break
            
            players.append(msg.author)
            await self.send_message(message.channel, '{} has joined the game.\nIf you wish to begin, type `ready` If more people want to join, type `join`\nUp to 3 more people can join.'.format(msg.author.name))
            
            def isJoin(msg):
                if msg.content in ('%sjoin' % self.config.prefix, '%scancel' % self.config.prefix, '%sready' % self.config.prefix):
                    return True
                    
            for i in range(3):
                while True:
                    msg = await self.wait_for_message(channel=message.channel, check=isJoin)
                    
                    if msg.content == '%scancel' % self.config.prefix:
                        self.game_channels.remove(message.channel.id)
                        return Response('The game has been cancelled.')
                    elif msg.content == '%sjoin' % self.config.prefix:
                        if msg.author in players:
                            await self.send_message(message.channel, 'Hey, you\'re already in the game! Someone else, please?')
                        else:
                            with open('config/coins.json', 'r') as fp:
                                fr = json.load(fp)
                                if msg.author.id in fr:
                                    coin = fr[msg.author.id]
                                else: 
                                    await self.send_message(message.channel, 'Oops, looks like you haven\'t joined the coin party yet! I\'ll add you right now.')
                                    response = await self.add_to_coin(msg.author, fr)
                                    await self.send_message(message.channel, response.content)
                                    coin = 100
                                
                            if coin < bet * 2:
                                await self.send_message(message.channel, 'Oops, it looks like you don\'t have enough coins to play! Either get some richer friends, or `cancel` the game and start with a lower bet.')
                            else:
                                break
                    else:
                        break
                            
                if msg.content == '%sready' % self.config.prefix:
                    await self.send_message(message.channel, 'The game is now beginning with {} players! Be sure to check your private messages, I will notify you when it is your turn. Good luck!'.format(len(players)))
                    break
                else:
                    players.append(msg.author)
                    await self.send_message(message.channel, '{} has joined the game.\nIf you wish to begin, type `ready` If more people want to join, type `join`\nUp to {} more people can join.'.format(msg.author.name, 2-i))
                    
            pot = bet * len(players)
            
            for i in players:
                with open('config/coins.json', 'r') as fp:
                    fr = json.load(fp)
                    fr[i.id] -= bet
                    with open('config/coins.json', 'w') as fo:
                        json.dump(fr, fo, indent=4, sort_keys=True)
                        
            s = []
            hlist = []
            d  = poker.Deck()
            d.shuffle()
            
            for i in players:
                h = poker.Hand(d)
                handrank = h.evaluateHand()
                handscore = h.score()
                s.append(handscore)
                hlist.append(handrank)
                with open('config/coins.json', 'r') as fp:
                    fr = json.load(fp)
                    coin = fr[i.id]
                await self.send_message(i, 'Your hand is:\n{}'.format(h))
                
            i = 0
            while i < len(players):
                with open('config/coins.json', 'r') as fp:
                    fr = json.load(fp)
                    coin = fr[players[i].id]
                pm = await self.send_message(players[i], 'The current bet is {}, there are {} coins in the pot, and you have {} coins.\nWould you like to `fold`, `call`, or `raise`?'.format(bet, pot, coin))
                def isHand(msg):
                    if msg.content.startswith('%sfold' % self.config.prefix):
                        return True
                    if msg.content.startswith('%scall' % self.config.prefix):
                        return True
                    if msg.content.startswith('%sraise' % self.config.prefix):
                        return True
                msg = await self.wait_for_message(channel=pm.channel, check=isHand)
                
                if msg.content.startswith('%sfold' % self.config.prefix):
                    await self.send_message(players[i], 'You have forfeited the game.')
                    await self.send_message(message.channel, '{} has folded their cards, forfeiting the game.'.format(players[i].name))
                    s.pop(i)
                    hlist.pop(i)
                    players.pop(i)
                    i -= 1
                    if len(players) == 1:
                        self.game_channels.remove(message.channel.id)
                        with open('config/coins.json', 'r') as fp:
                            fr = json.load(fp)
                            fr[players[0].id] += pot
                            with open('config/coins.json', 'w') as fo:
                                json.dump(fr, fo, indent=4, sort_keys=True)
                        return Response('Everyone but {0} folded! Congratulations {0}, you have won {1} coins!'.format(players[i].name, pot))
                        
                if msg.content.startswith('%scall' % self.config.prefix):
                    if coin < bet:
                        await self.send_message(players[i], 'Someone raised the bet past the amount you own. Your only choice now is to fold.')
                        await self.send_message(message.channel, '{} didn\'t have enough money to fulfil the raise, so they had to fold.'.format(players[i].name))
                        s.pop(i)
                        hlist.pop(i)
                        players.pop(i)
                        i -= 1
                        if len(players) == 1:
                            self.game_channels.remove(message.channel.id)
                            with open('config/coins.json', 'r') as fp:
                                fr = json.load(fp)
                                fr[players[0].id] += pot
                                with open('config/coins.json', 'w') as fo:
                                    json.dump(fr, fo, indent=4, sort_keys=True)
                            return Response('Everyone but {0} folded! Congratulations {0}, you have won {1} coins!'.format(players[i].name, pot))
                    else:
                        await self.send_message(players[i], 'You have called your cards. You push {} coins into the pot.'.format(bet))
                        await self.send_message(message.channel, '{} has called their cards, pushing {} coins into the pot.'.format(players[i].name, bet))
                        pot += bet
                        with open('config/coins.json', 'r') as fp:
                            fr = json.load(fp)
                            fr[players[i].id] -= bet
                            with open('config/coins.json', 'w') as fo:
                                json.dump(fr, fo, indent=4, sort_keys=True)
                                
                if msg.content.startswith('%sraise' % self.config.prefix):      
                    def isRaise(msg):
                        try:
                            int(msg.content)
                            return True
                        except ValueError:
                            return False
                        
                    await self.send_message(players[i], 'How much do you want to raise?')
                    
                    while True:
                        msg = await self.wait_for_message(channel=pm.channel, check=isRaise)
                        ras = int(msg.content)
                        if ras > coin - bet:
                            await self.send_message(players[i], 'You don\'t have enough coins to raise by that much! Try a lower number.')
                        if ras <= 0:
                            await self.send_message(players[i], 'You cannot raise by zero or a negative amount. Are you trying to cheat? Try a positive number.')
                        if ras > 0 and ras < coin - bet:
                            break
                                
                    bet += ras
                    pot += bet
                    await self.send_message(players[i], 'You have raised the bet by {}. You push {} coins into the pot.'.format(ras, bet))
                    await self.send_message(message.channel, '{} has raised the bet by {}, pushing {} coins into the pot.'.format(players[i].name, ras, bet))
                    with open('config/coins.json', 'r') as fp:
                        fr = json.load(fp)
                        fr[players[i].id] -= bet
                        with open('config/coins.json', 'w') as fo:
                            json.dump(fr, fo, indent=4, sort_keys=True)
                i += 1
            
        winner = max(s)
            
        bar = []
        foo = 0
        for i in range(len(players)):
            bar.append(0)
            if s[i] == winner:
                foo += 1
                bar[i] = foo
                
        if foo == len(players):
            for i in range(len(players)):
                with open('config/coins.json', 'r') as fp:
                    fr = json.load(fp)
                    fr[players[i]] += int(pot / len(players))
                    with open('config/coins.json', 'w') as fo:
                        json.dump(fr, fo, indent=4, sort_keys=True)
            self.game_channels.remove(message.channel.id)
            return Response('The game was somehow a complete tie! Everyone gets {} coins back.'.format(int(pot / len(players))))
        elif foo == 2:
            for i in range(2):
                with open('config/coins.json', 'r') as fp:
                    fr = json.load(fp)
                    fr[players[i]] += int(pot / 2)
                    with open('config/coins.json', 'w') as fo:
                        json.dump(fr, fo, indent=4, sort_keys=True)
            self.game_channels.remove(message.channel.id)
            return Response('The game was a draw between two players, {} and {}. They each get half the pot, {} coins.'.format(players[bar.index(1)], players[bar.index(2)], int(pot / 2)))
        elif foo == 3:
            for i in range(3):
                with open('config/coins.json', 'r') as fp:
                    fr = json.load(fp)
                    fr[players[i]] += int(pot / 3)
                    with open('config/coins.json', 'w') as fo:
                        json.dump(fr, fo, indent=4, sort_keys=True)
            self.game_channels.remove(message.channel.id)
            return Response('The game was a draw between three players, {}, {} and {}. They each get a third of the pot, {} coins.'.format(players[bar.index(1)], players[bar.index(2)], players[bar.index(3)], int(pot / 3)))
        elif foo == 4:
            for i in range(4):
                with open('config/coins.json', 'r') as fp:
                    fr = json.load(fp)
                    fr[players[i]] += int(pot / 4)
                    with open('config/coins.json', 'w') as fo:
                        json.dump(fr, fo, indent=4, sort_keys=True)
            self.game_channels.remove(message.channel.id)
            return Response('The game was a draw between four players, {}, {}, {} and {}. They each get a fourth of the pot, {} coins.'.format(players[bar.index(1)], players[bar.index(2)], players[bar.index(3)], players[bar.index(4)], int(pot / 4)))
        
        winnerIndex = s.index(winner)
        
        with open('config/coins.json', 'r') as fp:
            fr = json.load(fp)
            fr[players[winnerIndex].id] += pot
            with open('config/coins.json', 'w') as fo:
                json.dump(fr, fo, indent=4, sort_keys=True)
                
        self.game_channels.remove(message.channel.id)
        
        return Response('{} wins {} coins with their hand, {}! Congrats!'.format(players[winnerIndex].name, pot, hlist[winnerIndex]))
                        
    # There was a secret command here, but I hid it.
        
    async def on_message(self, message):
        await self.wait_until_ready()
        
        message_content = message.content.strip()
        
        if not message_content.startswith(self.config.prefix):
            return
            
        if message.author == self.user:
            return
            
        command, *args = shlex.split(message_content)
        command = command[len(self.config.prefix):].lower().strip()
        
        handler = getattr(self, 'cmd_%s' % command, None)
        
        if not handler:
            return
        
        argspec = inspect.signature(handler)
        params = argspec.parameters.copy()
        
        try:
            handler_kwargs = {}
            
            if params.pop('message', None):
                handler_kwargs['message'] = message
                
            if params.pop('args', None):
                handler_kwargs['args'] = args
            
            for key, param in list(params.items()):
                if not args and param.default is not inspect.Parameter.empty:
                    params.pop(key)
                    continue
                    
                if args:
                    handler_kwargs[key] = args.pop(0)
                    params.pop(key)
                    
            try:
                response = await handler(**handler_kwargs)
            except discord.DiscordException as e:
                response = None
                print('Exception on {}({}) in channel {}\n\t{}'.format(message.server.name, message.server.id, message.channel.name, traceback.format_exc()))
                
            if response and isinstance(response, Response):
                content = response.content
                route = message.channel
                
                if response.private:
                    route = message.author
                
                if not response.file:
                    try:
                        await self.send_message(route, content)
                    except:
                        pass
                else:
                    try:
                        await self.send_file(route, content)
                    except:
                        pass
                    
        except CommandError as e:
            await self.send_message(message.channel, e.message)
