# -*- encoding: utf-8 -*-

def main(host='localhost'):
    bot = irc.Bot((host, 6667))
    bot.connect()
    bot.receiver()

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    main(*args)
