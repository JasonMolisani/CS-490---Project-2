# Chat App

**Jason Molisani's (jm979) CS 490 project 2 - milestone 1** This is a basic chat application built using flask, python, socketio, react, and more. As this is only milestone one, there is still a lot of room for improvements.

## DEPLOYMENT

If you just wish to run the application, it is already deployed on [heroku](https://obscure-badlands-93399.herokuapp.com/). If you want to deploy it yourself, follow these instructions.

### Prep-work to get this running locally (only do once)
1. Clone this repository: `git clone https://github.com/NJIT-CS490/project2-m1-jm979.git` (all `commands` are to be executed in the terminal)
2. Use the reactSetup.sh to set up the react software: `sh reactSetup.sh`
3. Use the PSQLsetup.sh to set up the psql software and ineractions with python: `sh PSQLsetup.sh`. Enter yes to any prompts and don't worry about if you see two errors at the end saying "could not change directory"
4. Create a new file called `project2.env` in this root folder of this repositry
5. Add the following lines to the `project2.env` file:
   - `DATABASE_URL='postgresql://[username]:[password]@localhost/postgres` (replace `[username]` and `[password]` whatever username and password you want)
6. Start the PSQL interpretter: `psql`
7. Enter the following command (replacing `[username]` and `[password]` with the values you used in step 5): `create user [username] superuser password '[password]';`
8. Use `\q` to exit the psql interpretter and return to the normal terminal
9. Open this file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
10. Replace all values of `ident` with `md5` in Vim (you may need to type this instead of copying and pasting): `:%s/ident/md5/g`
11. Save the changes and close vim: `:wq`
12. Create a [google developer account](https://console.developers.google.com/)
13. Under `Credentials` (in the side bar), click `+ CREATE CREDENTIALS` and select `OAuth Client ID` from the drop down
14. Select `Web Application` and give it an appropriate name
15. Follow the steps to get this running locally and copy the address of the preview. Add this address as a `URI` to both `Authorized Javascript origins` and `Authorized redirect URIs`
16. Click `CREATE` to save this
17. Back at the `Credentials` page, find your new client ID under `OAuth 2.0 Client IDs` and copy the `Client ID` (use the icon immediately to the right of the client ID)
18. Open `GoogleButton.jsx` (found in the `scripts` sub-folder) and replace the value of the string being assigned on line 28 with your `Client ID`

### Steps to take every time to run this locally
1. (Re)start PSQL: `sudo service postgresql restart`
2. Start npm start building and maintaining the script.js file: `npm run watch`
3. In a different terminal, run the app.py fine: `python app.py`
4. Click the preview button at the top of the screen and select "Preview Running Application" from the drop down
5. Once you are finished, use CTRL+C in both terminals to kill the app

### How to deploy this to Heroku
1. Do all the prep-work to get this running locally (see above).
2. Login in to your heroku account (sign up for an account if you don't already have one) in the terminal using `heroku login -i` and entering your username and password when prompted
3. Create a new app with `heroku create`
4. Create a database for the new app with `heroku addons:create heroku-postgresql:hobby-dev`
5. Tell heroku to get ready? `heroku pg:wait`
6. Push the database to heroku `heroku pg:push postgres HEROKU_POSTGRESQL_ROSE_URL`
7. You can use `heroku pg:psql` to have the terminal start using psql queries to the heroku verion of the database to check things (or just skip this step) (`\q` will exit back to the regular terminal)
8. Push the current repository up to heroku with `git push heroku master`
9. Open the google developer account you created to get this running locally and add the domain where your heroku deployment is to both `Authorized Javascript origins` and `Authorized redirect URIs`

## Technical Problems
1. When deplying to Heroku, I had a hard time using `SELECT * FROM [my_database]` to test that my databse had been pushed up correctly. I searched the local database to see that `flask_sqlalchemy` had converted my chosen class name (`ChatHistory_DB`) to `chat_history_DB`, but when I ran `SELECT * FROM chat_history_DB` I kept getting an error about there not being a database with that name. The `usps` database that still existed from the lectures had been pushed up, but my new database wasn't resonding to the select query. Wondering if it was something in the table name, I did an internet search about table naming conventions that led me [here](https://stackoverflow.com/questions/2878248/postgresql-naming-conventions). There was a bunch of useful info, but the key part was "Postgresql treats identifiers case insensitively when not quoted (it actually folds them to lowercase internally), and case sensitively when quoted." This means my query of `SELECT * FROM chat_history_DB` was being treated the same as `SELECT * FROM chat_history_db`. In order to preserve the capitolization, I needed to rephrase the query as `SELECT * FROM "chat_history_DB"` (which worked).
2. After deplying to Heroku, I still couldn't get my program to run after fixing the environmental variables. Looking at the heroku logs, I was able to see that I still had the `import editdistance` line from where I used it in hw10 (which I repurposed for the project instead of building from scratch). HW10 was built off the completed lecture 11 example, which already had a requirements.txt file. This requirements.txt file didn't have a line for the edit distace module I started importing later, so when heroku tried to build it failed.
3. When I first started to program the chat bot, I was trying to figure out how to get it to have its own socket to reply on. I spent more time trying to figure this out than I would like to admit, but I eventually realized the very simple solution. The chat bot didn't need to broadcast anything. It just needed to reply to any message the server flagged as a potential command and passed into the bot. It just needed to take in a string and return a string. The server could then add its response to the message history and rebroadcast that with no issues, since that is what it was doing with all other messages anyway. That was much simpler and easier to implement.
4. When making the help command for the chat bot, I made a rather long string. This was the first time I had sent a long message through the chat app and when I prompted the chat bot to see that response, I didn't see anything. The bot still responded to the rest of my messages, but not this. Looking at the server logs, I was able to see that the problem occurred when I tried to save that message in the chat history database. When I made the database, I didn't put too much thought into it and left only 120 characters as the maximum amount i could store for a single message. Having identified the problem, there were two solutions: Redo the database to allow for the longer message, or make sure chat bot will never send a message that is too long and add a check in the server to handle user submitted messages that are too long. Redoing the database only temporarily solves the problem as the limit will still exist, just at a higher level. I implemented the second solution, but did add the database resize as a possible improvement for the future.
5. When starting milestone 2, I needed to set up the server to only respond to the specific user who was had just logged in. For milestone 1 I got by with broadcasting everything and having the clients and server pick put the messages that were relevant to them. This left a loophole that could have multiple users be assigned the same default username. This wasn't a big problem since no security regarding the usernames had been implemented anyway. With the implementation of OAurh, this was no longer accdeptable. Searching around on stack overflow eventually revealed that I could use the default room given by `request.sid` to communicate with the single client who had sent the message the server was replying to. Unfortunately, it took me longer than I would like to admit to understand that I needed to explicitly import request from the flask library. I couldn't just refer to request by importing flask (though there may be a way using `flask.request.sid` or something like that).
6. With the idea of a logged in and not logged in state, came the need to render components in different ways to reflect that change. Googling `react conditional html` brought me to a [webpage](https://reactjs.org/docs/conditional-rendering.html) with a number of different ways to do this. I decided to use the if version, though the example used a prop instead of a state. Using a react state worked just as well.
7. When deploying this milestone to its own heroku app, I had difficulties getting the database to link properly. This mostly happened because I tried to fix the requirements.txt first. In testing that, I saw that I did not have a `DATABASE_URL` environmental value. I manually added it by copying from the previous deployment. This caused my efforts to copy the tables over with `heroku pg:push postgres DATABASE_URL` to cause errors as `DATABASE_URL` was no longer available. I used the new value (`HEROKU_POSTGRESQL_ROSE_URL`) heroku was suggesting and was able to push the databases up, but the running code could not find the databases. After a lot of time searching, I eventually noticed that heroku had added `HEROKU_POSTGRESQL_ROSE_URL` as its own environmental variable and the value for `DATABASE_URL` that I copied from the preivous deployment was different from my local envoronmental variable. This (and a bit of internet searching) let me understand that heroku creates its own environmental variables for databases that are pushed up. Unfortunately, my code was still reading the `DATABASE_URL` environmental variable, which wasn't tied to the right table. I changed the code (and my local .env file) to look for (and store) an environmental variable named `HEROKU_POSTGRESQL_ROSE_URL` and everything started working again on heroku (and continued working locally).

## TODOs and Improvements
1. Add a background image to the chat room
   - **Resolved** - Added my dragon origami picture as a backgound to the chat history div and added to diagonal gradient to the main body to "match" 
2. Make number of connected users always visible
   - **Resolved** - Added a new react component to the page that takes in the number of users and updates it with hooks triggered on emits that will have a new value
3. Make sure page doesn't scroll
   - **Resolved** - Fixed the number of displayed messages to not exceed a certain amount (currently set at 14)
4. Chatbot
   - Uses its own class
     - **Resolved** - Chat bot is a class that is the server can ask for responses. Addtional functions still need to be added to customize chat bot's responses, but the querying of chat bot and broadcasting its' replies is finished
   - Identifiable visually
     - **Resolved** - Added a class to each 'li'  element of chat history to differentiate formatting between 'user' and 'bot' messages.
   - `!!about` make chat bot give a self description
     - **Resolved** - Chat bot has a self introduction. This could be improved in the future, but will work for now.
   - `!!help` chat bot sends a message with all of its commands
     - **Resolved** - Will need to update help in the future to provide help messages for new commands
   - `!!funtranslate [message]` makes bot echo message translated into choice of [fun language](https://funtranslations.com/api)
     - **Resolved** - funtranslate will now translate into pirate (up the the maximum number of free API calls, which is 5/hour and 60/day)
   - 1 command that uses some API
     - **Resolved** - Dadbot now uses the icanhazdadjoke API to tell dad jokes.
   - 1 command that doesn't have to use an API
     - **Partially Resolved** - Added an !!echo command, but that is really a simplified !!funtranslate. I may want to add another more interesting command later.
5. Clients update count on connect/disconnect
   - **Resolved** - Added a new react component to the page that takes in the number of users and updates it with hooks triggered on emits that will have a new value.
6. Clean up dead and commented out code
   - **Resolved** - Commented out code has been removed.
7. HTML/CSS improvements
   - **Resolved** - Basic formatting is done, but there is a lot of room for improvement. EDIT: acceptable levels of styling have been achieved
8. Rework Database to increase max message length from 120 characters, decrease username max length from 120 characters, and add a class attribute that will be either 'user' or 'bot' (not required for milestone)
   - **Resolved** - Database was entirely reworked to tie message sender to a foreign key in the new database of registered users
9. My patch of default usernames could assign to users the same username if an already connected user manually deletes their assigned username and someone new connects while that field is blank
   - **Resolved** - Setting up google authentication has wound up solving this issue
10. Currently, the server always emits the chat history to all clients. The client code is the only thing preventing the viewing of the chat history. I should create a room of logged in users and only let the server transmit to the logged in users.
    - **Resolved** - The server now maintains a set of logged in user's `request.sid` values and transmits chat history only to those rooms. This could probably be further improved using the `rooms` from `socket.io` to send a single message to the room of logged in users instead of a series of individual copies of the message to each logged in users personal room.
11. Display images in inline
    - **Resolved** - images are being rendered and basic css is still implemented
12. Display urls as hyperlink
    - **Resolved** - Valid URLs that are not also images links, become clickable hyperlinks
13. MessageHistory now parses html tags that are included in messages. I should add a method to the bot the screens and cleans incoming messages to prevent abuse
    - **Unresolved** - Currently unattempted
14. The number of users in the chat room may be lower than expedcted. It decreases on every disconnect, but only increases with login
    - **Resolved** - (implemented this I did use a set of sid values) The points where I am emitting the number of users is fine, but I should change to create a list of clients that are logged in (see improvement 10) and be sending the length of that list instead of tracking on an int. The actual implementation will have something to do with socketio's rooms and may not actually be a list.
