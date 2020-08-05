# bombsquad_chat_commands
# Installation:
Clone the repo in the mods folder.

In python/ba/_hooks.py 
  add:
  
      from bombsquad_chat_commands import BombsquadChatCommands
  
      BombsquadChatCommands(msg,client_id).handlechatmessage()
   
  at the start of `filter_chat_message()`
