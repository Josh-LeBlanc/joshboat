# joshboat
discord music bot
## run it yourself
1. ensure you have `ffmpeg` installed and in your path. (python too but i think that's obvious)
2. create the app in the discord developer portal. grant it __bot__ permissions and check all the permissions in the __text permissions__ and __voice permissions__ columns
3. invite the bot to your server
4. make a `.env` file and set the token value: `BOT_TOKEN=<token>`
5. run these to set the enviromnent up:
```bash
git clone https://github.com/Josh-LeBlanc/joshboat
cd joshboat
mkdir downloads # this is where it puts the audio it downloads
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
6. run the bot
```bash
python main.py
```
7. use the bot with the commands listed below
## commands
### play
`?play <url>` OR `?play <search term>`
### pause
`?pause`
pauses the song
### resume
`?resume`
resumes the song
### skip
`?skip`
skips the current song
### stop
`?stop`
stops playing and the bot leaves the voice call
## todo
- clear queue command
- view queue command
- help command
- watch video command ?
