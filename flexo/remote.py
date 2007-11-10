# -*- encoding: utf-8 -*-

import traceback
import sys

from flexo.prelude import is_oper
from flexo.plugin import Plugin

class Remote(Plugin):
    def on_private_msg(self, message):
        if not is_oper(message.sender):
            return

        pieces = message.tail.split(None, 1)
        cmd = pieces[0]
        if len(pieces) > 1:
            rest = pieces[1]
        else:
            rest = ''

        if cmd == 'eval':
            ctx = {
                'bot': self.bot,
            }
            try:
                result = eval(rest, ctx)
                if not result is None:
                    text = repr(result)
                    if len(text) > 60:
                        text = text[:60] + ' [..]'
                    message.reply(text)
            except Exception, e:
                message.reply('Failed: %r' % e)
                traceback.print_exc()
            return True

        elif cmd == 'load':
            try:
                replacement = self.load(rest)
            except Exception, e:
                message.reply('Failed: %r' % e)
                traceback.print_exc()
                return True
                
            for i, plugin in enumerate(self.bot.plugins):
                if plugin.__class__.__name__ == replacement.__class__.__name__:
                    self.bot.plugins[i] = replacement
                    message.reply('Reloaded.')
                    break
            else:
                self.bot.plugins.append(replacement)
                message.reply('Loaded.')

            return True

        elif cmd == 'graceful':
            self.restarter = message.nick
            self.bot.graceful()

    def load(self, name):
        module = __import__('flexo.' + name, fromlist=['plugin'])
        klass = module.plugin
        plugin = klass(self.bot)
        plugin.name = name
        return plugin

plugin = Remote
