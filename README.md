# Bombsquad Chat Commands
# Installation:

# Step 1: Downloading and placing files in the right directory

Method 1: Using git-
  Install git if not already installed using `sudo apt-get install git`
  Run your server atleast once to create a ba_root directory inside the dist directory.
  Next cd into the mods folder by `cd dist/ba_root`
  Now clone repo by `git clone https://github.com/abhinaypandey02/bombsquad_chat_commands.git`
  
Method 2: Manually downloading the files-
  Download the ZIP of this repository and extract it in the dist/ba_root/mods directory

After both the steps you should see a folder _bombsquad_chat_commands_ in the mods folder.  

# Step 2: Adding the implementation in bombsquad files
  In python/ba/_hooks.py 
  add:
  
      from bombsquad_chat_commands import BombsquadChatCommands
  
      BombsquadChatCommands(msg,client_id).handlechatmessage()
   
  at the start of `filter_chat_message()`

And delete the \_\_pycache__ folder in ba directory

# Step 3: Modifying server properties
  Edit the \_\_init__.py file and add your id as owner
