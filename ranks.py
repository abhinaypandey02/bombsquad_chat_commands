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
    head = "ranks"

    def __init__(self, msg, client_id, account_id, ranks):
        self.msg = [x.lower() for x in msg]
        if len(self.msg) == 5 and self.msg[1] == 'addplayer':
            self.msg[4] = msg[4]
        self.client_id = client_id
        self.account_id = account_id
        self.info_message = ''
        self.ranks = ranks
        self.sub_options = [('addplayer', 5), ('addrank', 3), ('removeplayer', 4),
                            ('removerank', 3), ('info', 2)]
        if self.validate_command(): self.execute()

    @staticmethod
    def commandhelp():
        help_text = "Command to add/modify/remove ranks." \
                    "\nTo Add Rank : /ranks addrank <rank_name>" \
                    "\nTo Add Player : /ranks addplayer <rank_name> <player_name> <accountID/clientID>" \
                    "\nTo Remove Rank : /ranks removerank <rank_name>" \
                    "\nTo Remove Player:  /ranks removeplayer <rank_name> <player_name>" \
                    "\nFor Rank Info : /ranks info" \
                    "\nNote: Player names and Rank names should NOT contain spaces"
        return help_text

    def on_error_command(self):
        ba.screenmessage(f"Use '/help {self.head}' for help about this command", transient=True,
                         clients=[self.client_id])

    def validate_command(self):
        if len(self.msg) == 1:
            ba.screenmessage("No arguments found", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        flag = False
        for x in self.sub_options:
            if self.msg[1] == x[0]:
                if len(self.msg) < x[1]:
                    ba.screenmessage("Too few arguments", transient=True, clients=[self.client_id])
                    self.on_error_command()
                    return False
                if len(self.msg) > x[1]:
                    ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
                    self.on_error_command()
                    return False
                flag = True
        if not flag:
            ba.screenmessage(
                "Available sub options are " + ','.join(x[0] for x in self.sub_options),
                transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        if not self.msg[1] in ["info", "addrank"]:
            if not self.msg[2] in self.ranks:
                ba.screenmessage("No such rank found", transient=True, clients=[self.client_id])
                self.on_error_command()
                return False
        if self.msg[1] == "addplayer":
            if not self.msg[4].isnumeric():
                if not (self.msg[4].startswith("pb-") and self.msg[4].endswith("==")):
                    ba.screenmessage("Player ID must be client ID or account ID", transient=True,
                                     clients=[self.client_id])
                    self.on_error_command()
                    return False
            else:
                ac_id = bombsquad_chat_commands.client_to_account(self.msg[4])
                if ac_id:
                    self.msg[4] = ac_id
                else:
                    ba.screenmessage(f"No player found with given client ID", transient=True,
                                     clients=[self.client_id])
                    self.on_error_command()
                    return False
            for x, j in self.ranks[self.msg[2]]['players'].items():
                if self.msg[4] == x or self.msg[3] == j:
                    ba.screenmessage(f"Player already exists in {self.msg[2]}", transient=True,
                                     clients=[self.client_id])
                    self.on_error_command()
                    return False
        if self.msg[1] == "removeplayer" and not self.msg[3] in [j for x, j in
                                                                 self.ranks[self.msg[2]][
                                                                     'players'].items()]:
            ba.screenmessage(f"No such player found in {self.msg[2]}", transient=True,
                             clients=[self.client_id])
            self.on_error_command()
            return False

        if self.msg[1] == 'addrank' and self.msg[2] in self.ranks:
            ba.screenmessage("Rank already present", transient=True,
                             clients=[self.client_id])
            self.on_error_command()
            return False
        return True

    def modify_ranks(self):
        with open(os.path.join(bombsquad_chat_commands.DIR, 'ranks.json'), "r") as f:
            f_read = json.loads(f.read())
        f_read['ranks'] = self.ranks
        with open(os.path.join(bombsquad_chat_commands.DIR, 'ranks.json'), "w+") as f:
            f.write(json.dumps(f_read))

    def execute(self):
        if self.msg[1] == "info":
            text = f'Ranks:'
            for i, rank in enumerate(self.ranks):
                text += f'\n{i + 1}. {rank}: ' + ','.join(
                    j for x, j in self.ranks[rank]['players'].items())
            ba.screenmessage(text, transient=True, clients=[self.client_id])
            return
        if self.msg[1] == 'addrank':
            self.ranks[self.msg[2]] = {"players": {}, "permissions": []}
            self.modify_ranks()
            return
        if self.msg[1] == 'addplayer':
            self.ranks[self.msg[2]]['players'][self.msg[4]] = self.msg[3]
            self.modify_ranks()
            return
        if self.msg[1] == 'removerank':
            del self.ranks[self.msg[2]]
            self.modify_ranks()
            return
        if self.msg[1] == 'removeplayer':
            for x, y in self.ranks[self.msg[2]]['players'].items():
                if y == self.msg[3]:
                    del self.ranks[self.msg[2]]['players'][x]
                    break
            self.modify_ranks()
            return


class PermissionsCommand:
    head = "perm"

    def __init__(self, msg, client_id, account_id, ranks):
        self.msg = msg
        self.client_id = client_id
        self.account_id = account_id
        self.info_message = ''
        self.ranks = ranks
        self.sub_options = ['add', 'remove', 'info']
        if self.validate_command(): self.execute()

    @staticmethod
    def commandhelp():
        help_text = "Command to add/remove permissions." \
                    "\nTo Add Permission : /perm add <rank_name> <command>" \
                    "\nTo Remove Permission : /perm remove <rank_name> <command>" \
                    "\nFor Permission Info : /perm info"
        return help_text

    def on_error_command(self):
        ba.screenmessage(f"Use '/help {self.head}' for help about this command", transient=True,
                         clients=[self.client_id])

    def validate_command(self):
        if len(self.msg) == 1:
            ba.screenmessage("No arguments found", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        if len(self.msg) < 4 and not self.msg[1] == "info":
            ba.screenmessage("Too few arguments", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        if len(self.msg) > 4 and not self.msg[1] == "info":
            ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        if self.msg[1] not in self.sub_options:
            ba.screenmessage("Available sub options are " + ','.join(x for x in self.sub_options),
                             transient=True, clients=[self.client_id])
            self.on_error_command()
            return False

        if not self.msg[1] == "info" and not self.msg[2] in self.ranks:
            ba.screenmessage("No such rank found", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False

        if self.msg[1] == 'remove' and not self.msg[3] in self.ranks[self.msg[2]]['permissions']:
            ba.screenmessage(f"No such permission found in {self.msg[2]}", transient=True,
                             clients=[self.client_id])
            self.on_error_command()
            return False

        if self.msg[1] == 'add':
            if self.msg[3] in self.ranks[self.msg[2]]['permissions']:
                ba.screenmessage("Permission already present", transient=True,
                                 clients=[self.client_id])
                self.on_error_command()
                return False
            if self.msg[3] not in [x[0].head for x in bombsquad_chat_commands.ACTIVE_COMMANDS]:
                ba.screenmessage("No Such Command", transient=True,
                                 clients=[self.client_id])
                self.on_error_command()
                return False
        return True

    def modify_ranks(self):
        with open(os.path.join(bombsquad_chat_commands.DIR, 'ranks.json'), "r") as f:
            f_read = json.loads(f.read())
        f_read['ranks'] = self.ranks
        with open(os.path.join(bombsquad_chat_commands.DIR, 'ranks.json'), "w+") as f:
            f.write(json.dumps(f_read))

    def execute(self):
        if self.msg[1] == "info":
            text = f'Permissions:'
            for i, rank in enumerate(self.ranks):
                text += f'\n{i + 1}. {rank}: ' + ','.join(
                    j for j in self.ranks[rank]['permissions'])
            ba.screenmessage(text, transient=True, clients=[self.client_id])
            return
        if self.msg[1] == 'add':
            self.ranks[self.msg[2]]['permissions'].append(self.msg[3])
            self.modify_ranks()
            return
        if self.msg[1] == 'remove':
            self.ranks[self.msg[2]]['permissions'].remove(self.msg[3])
            self.modify_ranks()
            return
