#!/usr/bin/env -S python3.7 -O
# Copyright (c) 2011-2020 Eric Froemling
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

import ba
import bombsquad_chat_commands


class HelpCommand:
    head = "help"

    def __init__(self, msg, client_id, account_id, ranks):
        self.msg=[x.lower() for x in msg]
        self.client_id = client_id
        self.account_id = account_id
        self.ranks = ranks

        self.commands = bombsquad_chat_commands.ACTIVE_COMMANDS

        if self.validate_command(): self.execute()

    def commandhelp(self):
        help_text = "Supported Commands: " + ', '.join(x[0].head for x in self.commands) \
                    + "\nUse '/help <command-name>' for more info"
        ba.screenmessage(help_text, transient=True, clients=[self.client_id])
    def on_error_command(self):
        ba.screenmessage("Use '/help <command-name>' for more info", transient=True,
                         clients=[self.client_id])
    def validate_command(self):
        if len(self.msg) > 2:
            ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        return True

    def execute(self):
        if len(self.msg) == 1:
            self.commandhelp()
        else:
            for command in self.commands:
                if self.msg[1] == command[0].head and not self.msg[1]==self.head:
                    ba.screenmessage(command[0].commandhelp(), transient=True, clients=[self.client_id])
                    return
            ba.screenmessage("No such command", transient=True, clients=[self.client_id])
            self.commandhelp()
