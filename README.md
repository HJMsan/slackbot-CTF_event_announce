# summary

This is a tool that is automating the announcement of CTF for every week. You have to configure a slack app and prepare a server to deploy this python app. 

# conguration
[Here](https://api.slack.com/apps) is the link for configuration of slack bot.
1. Click "Create New App".
2. Install the new app to your own workspace
3. Click "OAuth & Permissions" and add OAuth Scopes that noted below: 
   * channels: join, manage, read
   * chat: write, write.public
   * groups: read, write
   * im: read, write
   * links: write
   * mpim: read, write
4. Write "Bot User OAuth Token" to .env instead of "your_slack_bot_token".
5. Click "Socket Mode" and Enable socket mode. 
6. Write App Token to .env instead of "your_slack_app_token"
7. Run ` python3 run.py` on your server  (You may have to configure .env as a environment variables before running)

# Function
Announcements of the week are made every Thursday 12:00(JST). The interface is like below: 
![interface](/interface.png)

* Title: Name of the CTF with the official link. 
* Duration(JST)
* ctftime: The link of ctftime
* weight 
* format
* "Join" button: A new channel would be made if some one clicking this button.