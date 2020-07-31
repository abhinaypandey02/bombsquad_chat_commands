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
    def __init__(self, msg, client_id, account_id, ranks, ban_time=30):
        self.msg = msg
        self.client_id = client_id
        self.ban_time = ban_time * 60
        self.account_id = account_id
        self.ranks = ranks
        self.permission = ['admin']
        self.execute()

    @staticmethod
    def commandhelp():
        help_text = "Command to kick any player on the server" \
                    "\nUsage: /kick <playername>(required)"
        return help_text

    def validate_command(self):
        if self.permission:
            for x in self.ranks:
                if x in self.permission:
                    if self.account_id in self.ranks[x]:
                        return True
            return False
        if len(self.msg) > 2:
            ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
            return False
        return True

    def execute(self):
        kick_id = int(self.msg[1])
        _ba.disconnect_client(client_id=kick_id, ban_time=self.ban_time)
