import thread
from flexo import irc

def main():
    bot = irc.Bot(('irc.cafeen.org', 6667))
    bot.connect()
    bot.receiver()

if __name__ == '__main__':
    main()
