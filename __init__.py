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

import _ba
from chat_commands.help import HelpCommand
from chat_commands.info import InfoCommand
from chat_commands.moderation import KickCommand

DIR = os.path.join(os.getcwd(), 'ba_root', 'mods', 'chat_commands')
ACTIVE_COMMANDS = ['info', 'help']

if not os.path.exists(os.path.join(DIR, 'ranks.json')):
    with open(os.path.join(DIR, 'ranks.json'), "w+") as f:
        f.write('{"ranks":{"admin":["pb-IF4tVRAtLA=="]}}')
    RANKS = {}
else:
    with open(os.path.join(DIR, 'ranks.json'), "r") as f:
        f_read = f.read()
        if f_read == '':
            f_read = '{}'
    RANKS = json.loads(f_read)['ranks']


def handlechatmessage(msg, client_id):
    msg = msg[1:].split(" ")
    command_head = msg[0]
    roster = _ba.get_game_roster()
    for i in roster:
        if i['client_id'] == client_id:
            if command_head == "kick" and command_head in ACTIVE_COMMANDS:
                KickCommand(msg, client_id, i['account_id'], RANKS)
            if command_head == "info" and command_head in ACTIVE_COMMANDS:
                InfoCommand(msg, client_id, roster, i['account_id'], RANKS)
            if command_head == "help" and command_head in ACTIVE_COMMANDS:
                HelpCommand(msg, client_id, i['account_id'], RANKS, ACTIVE_COMMANDS)
