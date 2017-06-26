import discord

botVersion = '1.0.3'

introText = 'Hello! I\'m a bot created by Linzolle to satisfy her eternal lust for programming. All my commands start with `{prefix}`, so type `about` to learn more about me, or `help` to display my list of commands!'

changeLog = '''Version {}:
Bug fixes so the bot doesn't completely fuck up.
Added `uptime` command.
Added cycling status messages.
Added `coins add` so that you have a way to acquire more coins when you run out. <3'''.format(botVersion)

helpText = '''The current command prefix is `{prefix}`

`help` Lists my commands. (What you just did!) Try `help [command]` to (potentially) learn more about a specific command.

`about` Makes me tell you about myself!

`changelog` Show you my recent changes in my current version.

`hello` Reposts my introduction message that I sent when I joined the server.

`invite` Posts the link used to invite me to your other servers.

`ping` Test my connection to you.

`choose [choice1] [choice2] [etc.]` Type at least two words or phrases, and I\'ll randomly select one for you. (Spaces separate words, but you can use quotes to group phrases together.)

`random [action]` Have me perform a variety of randomised functions! Please tell me `random help` if you want to learn more.

`ily` I love you <3

`yikes` Post Linzolle\'s favourite picture of all time.

`coins` Join the coin party if you haven\'t already, or display how many coins you have! Required to play poker and other games. Type `coins help` to display a list of subcommands.

`poker [bet]` Initiate a game of poker! I will walk you through it after you start it up. (Type `poker help` to display a ranking of each hand if you need a reference.)

`slots [bet]` Play a simple game of slots. Don\'t go wasting all your money!

`image [query]` Grab the first three images from Google Images for a query.

`eval [query]` Evaluate a mathematical expression or similar things, such as \'65kg to pounds\'

`uptime` Find out how long it\'s been since I woke up.'''

randomText = '''`samoyed` Posts a random picture of Linzolle\'s favourite dog breed, the Samoyed! (`{prefix}samoyed` is aliased to this.)

`shiba` Like the Samoyed command, but with Shibas. (`{prefix}shiba` is aliased to this.)

`husky` Snow dogger. (`{prefix}husky` is aliased to this.)

`corgi` Follow @IAmCorgii on Twitter! (`{prefix}corgi` is aliased to this.)

`rat` Posts a random picture of Linzolle\'s boyfriend\'s favourite animal, a rat! (He made her do this; `{prefix}rat` is aliased to this.)

`range [intMin] [intMax]` Picks a random integer between two integers you specify, in which intMin and intMax are the two integers. (No brackets, inclusive)

`dice NdN` Rolls some dice, in which N1 is the number of dice to roll and N2 is the number of sides.

`rival` Posts a random character from the Rivals of Aether roster.

`weapon` Picks a weapon and style from the Monster Hunter series.'''

aboutText = '''Hello, my name is Tsukino Mai（月野舞）, and you\'re viewing version %s of me! I was created by Linzolle#2608 in order for her to create a customised bot based on whatever functions she wanted to implement. If you have any questions, join Linzolle\'s development server https://discord.gg/Qj4HXeX, or contact her on her Twitter, @Linzolle.
You can call me Mai, and use female pronouns for me. (Even though I\'m actually just a sequence of binary programmed to respond to you!)
I run on Python 3.5, using the discord.py library created by Rapptz on version %s.
(see here for more details: https://github.com/Rapptz/discord.py)
(view my source code on GitHub like you're looking at my panties: https://github.com/Linzolle/tsukino)''' % (botVersion, discord.__version__)