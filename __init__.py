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


from __future__ import annotations

import json
import os

import _ba
import ba
from bombsquad_chat_commands.help import HelpCommand
from bombsquad_chat_commands.info import InfoCommand
from bombsquad_chat_commands.moderation import KickCommand
from bombsquad_chat_commands.ranks import RanksCommand,PermissionsCommand

#The boolean specifies if the command is available for all
ACTIVE_COMMANDS = [(KickCommand, False), (InfoCommand, True), (HelpCommand, True),
                   (RanksCommand, False),(PermissionsCommand,False)]
DIR = __file__.replace(os.path.basename(__file__), '')
OWNER="pb-IF4tVRAtLA=="

def client_to_account(client_id):
    for i in _ba.get_game_roster():
        if str(i['client_id']) == str(client_id):
            return i['account_id']
    return False


class BombsquadChatCommands:

    def __init__(self, msg, client_id):
        if len(msg) <= 1 or msg[0] != '/':
            self.msg = ''
            return

        if not os.path.exists(os.path.join(DIR, 'ranks.json')):
            with open(os.path.join(DIR, 'ranks.json'), "w+") as f:
                f.write(
                    '{"ranks":{}}')
            self.RANKS = {}
        else:
            with open(os.path.join(DIR, 'ranks.json'), "r") as f:
                f_read = f.read()
                if f_read == '':
                    f_read = '{}'
            self.RANKS = json.loads(f_read)['ranks']
        self.msg = msg[1:].split(" ")
        while '' in self.msg:
            self.msg.pop(self.msg.index(''))

        self.command_head = self.msg[0]
        self.client_id = client_id

    def handlechatmessage(self):
        if not self.msg: return
        account_id = client_to_account(self.client_id)
        if account_id:
            for command in ACTIVE_COMMANDS:
                if self.command_head == command[0].head:
                    if command[1] or account_id ==OWNER:
                        command[0](self.msg, self.client_id, account_id, self.RANKS)
                        return
                    for x,rank in self.RANKS.items():

                        if self.command_head in rank['permissions']:
                            if account_id in rank['players']:
                                command[0](self.msg, self.client_id, account_id, self.RANKS)
                                return
                    ba.screenmessage(
                        f"You dont have permission to execute {self.command_head} command.",
                        transient=True, clients=[self.client_id])
                    return
