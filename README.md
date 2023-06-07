# voice-to-text-tg-bot
### Description
Telegram bot that uses whisper module to translate voice and circle messages to text.

### Usage
1. Put your bot token you gor from @BotFather into .env file
```
BOT_TOKEN="<token_from_tg>"
```
2. Run the script
```
$ python3.9 main.py
```

### FFmpeg Installation ###  
**Installation for Windows:**  
For Windows, you can install it via the [download](https://ffmpeg.org/download.html#build-windows) link, then add it to the PATH.  
Or install the scoop installer in Windows and use it to register a command.
In PowerShell, write the command:
```
iwr -useb get.scoop.sh | iex
```
Next, install ffmpeg:
```
scoop install ffmpeg
```


**Installation for Linux and macOS:**
```  
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg
```

### Installing Whisper ###
It is advisable to install whisper using the command below, as it significantly increases the download speed.
```
pip install git+https://github.com/openai/whisper.git
```
Update:
``` 
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
``` 
