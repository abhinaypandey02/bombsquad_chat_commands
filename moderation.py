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
    head = "kick"

    def __init__(self, msg, client_id, account_id, ranks):
        self.msg = msg
        self.msg = [x.lower() for x in msg]
        self.ban_id = 0
        self.client_id = client_id
        self.ban_time = -1
        self.account_id = account_id
        self.ranks = ranks
        if self.validate_command(): self.execute()

    @staticmethod
    def commandhelp():
        help_text = "Command to kick any player on the server" \
                    "\nUsage: /kick <client id>(required) <ban time hours>(optional)"
        return help_text
    def on_error_command(self):
        ba.screenmessage(f"Use '/help {self.head}' for help about this command", transient=True,
                         clients=[self.client_id])
    def validate_command(self):

        if len(self.msg) < 2:
            ba.screenmessage("Too few arguments", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        if len(self.msg) > 3:
            ba.screenmessage("Too many arguments", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False

        if not self.msg[1].isnumeric():
            ba.screenmessage("Client ID must be integer", transient=True, clients=[self.client_id])
            self.on_error_command()
            return False
        if len(self.msg) == 3:
            if not self.msg[2].isnumeric():
                ba.screenmessage("Ban Time must be an integer (minutes)", transient=True,
                                 clients=[self.client_id])
                self.on_error_command()
                return False
        return True

    def execute(self):
        self.ban_id = int(self.msg[1])
        if len(self.msg) == 3: self.ban_time = int(self.msg[2])*60
        if self.ban_time == -1:
            if not _ba.disconnect_client(client_id=self.ban_id):
                ba.screenmessage("No such Client ID found!", transient=True,
                                 clients=[self.client_id])
            return
        if not _ba.disconnect_client(client_id=self.ban_id, ban_time=self.ban_time):
            ba.screenmessage("No such Client ID found!", transient=True, clients=[self.client_id])
