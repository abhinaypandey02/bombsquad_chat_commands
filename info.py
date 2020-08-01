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
import json

import ba


class InfoCommand:
    def __init__(self, msg, client_id, roster, account_id, ranks):
        self.msg = msg
        self.client_id = client_id
        self.account_id = account_id
        self.roster = roster
        self.info_message = ''
        self.ranks = ranks
        self.permission = []
        self.execute()

    @staticmethod
    def commandhelp():
        help_text = "Command to get info of any/every player on the server" \
                    "\nUsage: /info <playername>(optional)" \
                    "\nLeave <playername> empty for all player info."
        return help_text

    def validate_command(self):
        if self.permission:
            for x in self.ranks:
                if x in self.permission:
                    if self.account_id in self.ranks[x]:
                        return True
            ba.screenmessage("You Don't have permission to use this command!", transient=True,
                             clients=[self.client_id])
            return False
        if len(self.msg) > 2:
            ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
            return False
        return True

    def execute(self):
        if not self.validate_command(): return
        found=False
        for i in self.roster:
            if i['client_id'] == -1: continue
            spec = json.loads(i['spec_string'])
            player_names = [str(x['name']) for x in i['players']]
            if len(self.msg) == 1 \
                    or self.msg[1].lower() in spec['n'].lower() \
                    or self.msg[1].lower() in [x.lower() for x in player_names]:
                found=True
                self.info_message += f"*Account name:{spec['n']} " \
                                     f"*Client ID:{i['client_id']} " \
                                     f"*Account ID:{i['account_id']} " \
                                     f"*Players:{','.join(player_names)}\n"
                ba.screenmessage(self.info_message[:-1], transient=True, clients=[self.client_id])
        if not found:
            ba.screenmessage("No such player found!", transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
