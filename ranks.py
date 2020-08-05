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
import os

import ba
import bombsquad_chat_commands


class RanksCommand:
    def __init__(self, msg, client_id, account_id, ranks, DIR):
        self.msg = msg
        self.client_id = client_id
        self.account_id = account_id
        self.info_message = ''
        self.ranks = ranks
        self.DIR = DIR
        self.permission = []
        self.sub_options = ['add', 'remove', 'info']
        self.execute()

    @staticmethod
    def commandhelp():
        help_text = "Command to add/modify/remove ranks." \
                    "\nTo Add Rank : /ranks add <rank_name>" \
                    "\nTo Add Player : /ranks add <rank_name> <player_name> <accountID/clientID" \
                    "\nTo Remove Rank : /ranks remove <rank_name>" \
                    "\nTo Remove Player:  /ranks remove <rank_name> <player_name>" \
                    "\nFor Rank Info : /ranks info" \
                    "\nNote: Player names and Rank names should NOT contain spaces"
        return help_text

    def validate_command(self):
        if self.permission:
            flag = False
            for x in self.ranks:
                if x in self.permission:
                    if self.account_id in self.ranks[x]:
                        flag = True

            if not flag:
                ba.screenmessage("You Don't have permission to use this command!", transient=True,
                                 clients=[self.client_id])
                return False

        if len(self.msg) < 2 or (len(self.msg) == 4 and self.msg[1] != 'remove'):
            ba.screenmessage("Too few arguments", transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
            return False
        if len(self.msg) > 6:
            ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
            return False
        if self.msg[1] not in self.sub_options:
            ba.screenmessage("Available sub options are " + ','.join(x for x in self.sub_options),
                             transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
            return False
        if len(self.msg) == 2:
            if self.msg[1] != "info":
                ba.screenmessage("Too few arguments", transient=True, clients=[self.client_id])
                ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                return False
            else:
                return True

        if len(self.msg) == 5:

            if not self.msg[2] in self.ranks:
                ba.screenmessage("No such rank found", transient=True, clients=[self.client_id])
                ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                return False

            if not self.msg[4].isnumeric():
                if not (self.msg[4].startswith("pb-") and self.msg[4].endswith("==")):
                    ba.screenmessage("Player ID must be client ID or account ID", transient=True,
                                     clients=[self.client_id])
                    ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                return False
            else:
                ac_id = bombsquad_chat_commands.client_to_account(self.msg[4])
                if ac_id:
                    self.msg[4] = ac_id
                else:
                    ba.screenmessage(f"No player found with given client ID", transient=True,
                                     clients=[self.client_id])
                    ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                    return False
            if self.msg[4] in self.ranks[self.msg[2]]:
                ba.screenmessage(f"Player already exist in {self.msg[2]}", transient=True,
                                 clients=[self.client_id])
                ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                return False
        if len(self.msg) == 4:
            if self.msg[1] == 'remove' and not self.msg[3] in [self.ranks[self.msg[2]][x] for x in
                                                               self.ranks[self.msg[2]]]:
                ba.screenmessage(f"No such player found in {self.msg[2]}", transient=True,
                                 clients=[self.client_id])
                ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                return False

        if len(self.msg) == 3:
            if self.msg[2] in self.ranks:

                if self.msg[1] == 'add':
                    ba.screenmessage("Rank already present", transient=True,
                                     clients=[self.client_id])
                    ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                    return False
            else:
                if self.msg[1] == 'remove':
                    ba.screenmessage("No such rank found", transient=True, clients=[self.client_id])
                    ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                    return False
        return True

    def modify_ranks(self):
        with open(os.path.join(self.DIR, 'ranks.json'), "r") as f:
            f_read = json.loads(f.read())
        f_read['ranks'] = self.ranks
        with open(os.path.join(self.DIR, 'ranks.json'), "w+") as f:
            f.write(json.dumps(f_read))

    def execute(self):
        if not self.validate_command(): return
        if self.msg[1] == "info":
            text = f'Ranks:'
            for i, rank in enumerate(self.ranks):
                text += f'\n{i + 1}. {rank}: ' + ','.join(
                    self.ranks[rank][x] for x in self.ranks[rank])
            ba.screenmessage(text, transient=True, clients=[self.client_id])
            return
        if len(self.msg) == 3 and self.msg[1] == 'add':
            self.ranks[self.msg[2]] = {}
            self.modify_ranks()
            return
        if len(self.msg) == 5 and self.msg[1] == 'add':
            self.ranks[self.msg[2]][self.msg[4]] = self.msg[3]
            self.modify_ranks()
            return
        if len(self.msg) == 3 and self.msg[1] == 'remove':
            del self.ranks[self.msg[2]]
            self.modify_ranks()
            return
        if len(self.msg) == 4 and self.msg[1] == 'remove':
            for x in self.ranks[self.msg[2]]:
                if self.ranks[self.msg[2]][x] == self.msg[3]:
                    del self.ranks[self.msg[2]][x]
                    break
            self.modify_ranks()
            return
