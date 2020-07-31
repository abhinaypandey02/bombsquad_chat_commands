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
from chat_commands.moderation import KickCommand
from chat_commands.info import InfoCommand,HelpCommand
import _ba,ba

ADMINS=['pb-IF4tVRAtLA==']
COMMANDS=['kick','info','help']

def handlemessage(msg,id):
    msg=msg[1:].split(" ")
    command_head=msg[0]
    roster = _ba.get_game_roster()
    print(id)
    for i in roster:
        if i['client_id'] ==id:
            if not i['account_id'] in ADMINS:
                ba.screenmessage("You are not an admin!",transient=True,clients=[id])
                return
            else:
                    if command_head=="kick":
                        KickCommand(msg,id)                  
                    if command_head=="info":
                        InfoCommand(msg,id,roster)
                    if command_head=="help":
                        HelpCommand()