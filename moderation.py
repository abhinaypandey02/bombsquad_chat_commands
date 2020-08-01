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

import _ba
import ba


class KickCommand:
    def __init__(self, msg, client_id, account_id, ranks):
        self.msg = msg
        self.ban_id = 0
        self.client_id = client_id
        self.ban_time = -1
        self.account_id = account_id
        self.ranks = ranks
        self.permission = ['admin']
        self.execute()

    @staticmethod
    def commandhelp():
        help_text = "Command to kick any player on the server" \
                    "\nUsage: /kick <client id>(required) <ban time hours>(optional)"
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
        if len(self.msg) < 2:
            ba.screenmessage("Too few arguments", transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
            return False
        if len(self.msg) > 3:
            ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
            return False

        try:
            self.ban_id = int(self.msg[1])
        except ValueError:
            ba.screenmessage("Client ID must be integer", transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
            return False
        except:
            ba.screenmessage("Error in command", transient=True, clients=[self.client_id])
            ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
            return False
        if len(self.msg) == 3:
            try:
                self.ban_time = int(self.msg[2])
            except ValueError:
                ba.screenmessage("Ban Time must be a number (hours)", transient=True,
                                 clients=[self.client_id])
                ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                return False
            except:
                ba.screenmessage("Error in command", transient=True, clients=[self.client_id])
                ba.screenmessage(self.commandhelp(), transient=True, clients=[self.client_id])
                return False
        return True

    def execute(self):
        if not self.validate_command(): return
        if self.ban_time==-1:
            if not _ba.disconnect_client(client_id=self.ban_id):
                ba.screenmessage("No such Client ID found!", transient=True, clients=[self.client_id])
            return
        if not _ba.disconnect_client(client_id=self.ban_id,ban_time=self.ban_time):
            ba.screenmessage("No such Client ID found!", transient=True, clients=[self.client_id])
