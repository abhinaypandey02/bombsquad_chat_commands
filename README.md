# Bombsquad Chat Commands

ONLY FOR BOMBSQUAD VERSIONS > 1.5.23

# Installation:
# Step 0: Run the server once and exit to create ba_root directory.

# Step 1: Downloading and placing files in the right directory:

<b>Method 1</b>: Using git-<br>
  Install git if not already installed using `sudo apt-get install git`<br>
  Run your server atleast once to create a ba_root directory inside the dist directory.<br>
  Next cd into the mods folder by `cd dist/ba_root`<br>
  Now clone repo by `git clone https://github.com/abhinaypandey02/bombsquad_chat_commands.git`<br><br>
  
<b>Method 2</b>: Manually downloading the files-<br>
  Download the ZIP of this repository and extract it in the dist/ba_root/mods directory<br><br>

After both the steps you should see a folder _bombsquad_chat_commands_ in the mods folder.  <br>

# Step 2: Enabling the plugin:
  Run the server once to detect the plugin installed.<br>
  Open dist/ba_root/config.json and find `bombsquad_chat_commands.Plugin`,<br>
  Change `"enabled": false` to `"enabled":true`

# Step 3: Modifying server properties:
  Edit the \_\_init__.py file and add your id as owner and you are good to go
 
