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
def handlehelp():
    pass
def handleinfo(msg,id,roster):
    if len(msg)>2:
        ba.screenmessage("Too many arguments",transient=True,clients=[id])
        return
    infomessage=''
    if len(msg)==1:
        for i in roster:
            if int(i['client_id'])==-1:continue
            spec = json.loads(i['spec_string'])
            player_names=[str(x['name']) for x in i['players']]
            infomessage+="*Account name:{0} *Client ID:{1} *Account ID:{2} *Players:{3}\n".format(str(spec['n']),str(i['client_id']),str(i['account_id']),str("/".join(player_names)))
            ba.screenmessage(infomessage[:-1],transient=True,clients=[id])
    else:        
        for i in roster:
            spec = json.loads(i['spec_string'])
            player_names=[str(x['name']) for x in i['players']]
            if msg[1].lower() in spec['n'].lower() or msg[1].lower() in [x.lower() for x in player_names]:
                infomessage="*Account name:{0} *Client ID:{1} *Account ID:{2} *Players:{3}".format(str(spec['n']),str(i['client_id']),str(i['account_id']),str("/".join(player_names)))
                ba.screenmessage(infomessage,transient=True,clients=[id])
