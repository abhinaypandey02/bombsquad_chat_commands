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
import subprocess
import sys

import _ba
import ba
from bombsquad_chat_commands.help import HelpCommand
from bombsquad_chat_commands.info import InfoCommand
from bombsquad_chat_commands.moderation import KickCommand
from bombsquad_chat_commands.ranks import RanksCommand, PermissionsCommand

# ba_meta require api 6
 

# The boolean specifies if the command is available for all
#remove the command tuple from the list if you want to disable it
ACTIVE_COMMANDS = [(KickCommand, False), (InfoCommand, True), (HelpCommand, True),
                   (RanksCommand, False), (PermissionsCommand, False)]
DIR = os.path.dirname(__file__)
# add your account id or more than one here
OWNER = ["pb-IF4tVRAtLA=="]
 

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
                    if command[1] or account_id in OWNER:
                        command[0](self.msg, self.client_id, account_id, self.RANKS)
                        return
                    for x, rank in self.RANKS.items():

                        if self.command_head in rank['permissions']:
                            if account_id in rank['players']:
                                command[0](self.msg, self.client_id, account_id, self.RANKS)
                                return
                    ba.screenmessage(
                        f"You dont have permission to execute {self.command_head} command.",
                        transient=True, clients=[self.client_id])
                    return


# ba_meta export plugin
class Plugin(ba.Plugin):
    def on_app_launch(self) -> None:

        self.check_for_update()

        insert_data_hooks = "    from bombsquad_chat_commands import BombsquadChatCommands\n" \
                            "    BombsquadChatCommands(msg,client_id).handlechatmessage()\n"
        if self.validate_installation("_hooks.py",
                                      os.path.join('ba_data', 'python', 'ba', "_hooks.py"),
                                      insert_data_hooks, "filter_chat_message", insert_data_hooks):
            print("Installation verified in _hooks.py.")

    def validate_installation(self, filename, file_location, test_string, test_function,
                              insert_data):
        try:
            with open(os.path.join(file_location), "r") as f:
                f_read = f.read()
        except:
            print(f"{filename} not found / Couldn't open file!")
            return False
        if not test_string in f_read:
            print(f"Commands are not installed in {filename}!\n"
                  "Installing\n")
            if self.handle_file(file_location, test_function, insert_data):
                print(f"Installed Successfully in {filename}! Restarting!")
                sys.exit(0)
            else:
                print("Error in Installation!")

                sys.exit(1)
        else:
            return True

    def handle_file(self, file_location, test_function, insert_data):
        try:
            print(f"Searching for {file_location}")
            with open(file_location, "r") as f:
                temp_read = f.readlines()
                print(f"Checking for {test_function} line")
                flag = False
                for i, line in enumerate(temp_read):
                    if test_function in line:
                        flag = True
                        print("Line found! Installing below this line!")
                        temp_read.insert(i + 1, insert_data)

                temp_read = "".join(temp_read)
                if not flag:
                    print("File Scheme has been changed by Eric!"
                          "Please hit me up on github so I can update the commands!"
                          "Meanwhile switch off my plugin by changing value back to false in config.py")
                    return False
        except:
            print(f"{filename} not found / Couldn't open file!")
            return False
        try:
            with open(file_location, "w") as f:
                print("Writing back on the file!")
                f.write(temp_read)
                return True
        except:
            print(f"{filename} not found / Couldn't write file!")
            return False

    def do_update(self):

        from threading import Thread
        print(subprocess.check_output(["git", "commit", "-a", "-m", "localcommit"], cwd=DIR))
        def git_pull():
            subprocess.Popen(["git", "pull"], cwd=DIR)

        t = Thread(target=git_pull)
        t.start()

        print("UPDATING BOMBSQUAD CHAT COMMANDS PLEASE RESTART SERVER ONCE ITS DONE!")
        sys.exit(0)

    def check_for_update(self):
        print(subprocess.check_output(["git", "remote", "update"], cwd=DIR))

        local = subprocess.check_output(["git", "rev-parse", "@"], cwd=DIR)
        base = subprocess.check_output(["git", "merge-base", "@", "@{u}"], cwd=DIR)
        remote = subprocess.check_output(["git", "rev-parse", "@{u}"], cwd=DIR)
        if local != remote and remote!=base:
            self.do_update()
