# bombsquad_chat_commands
# Installation:
Clone the repo in the mods folder.

In python/ba/_hooks.py 
  add `if len(msg) > 1 and msg[0] == '/':handlechatmessage(msg, client_id)` as the first line in `filter_chat_message()`
