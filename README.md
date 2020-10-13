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
6. Push the database to heroku `heroku pg:push postgres DATABASE_URL`
7. You can use `heroku pg:psql` to have the terminal start using psql queries to the heroku verion of the database to check things (or just skip this step) (`\q` will exit back to the regular terminal)
8. Push the current repository up to heroku with `git push heroku master`

## Technical Problems
1. When deplying to Heroku, I had a hard time using `SELECT * FROM [my_database]` to test that my databse had been pushed up correctly. I searched the local database to see that `flask_sqlalchemy` had converted my chosen class name (`ChatHistory_DB`) to `chat_history_DB`, but when I ran `SELECT * FROM chat_history_DB` I kept getting an error about there not being a database with that name. The `usps` database that still existed from the lectures had been pushed up, but my new database wasn't resonding to the select query. Wondering if it was something in the table name, I did an internet search about table naming conventions that led me [here](https://stackoverflow.com/questions/2878248/postgresql-naming-conventions). There was a bunch of useful info, but the key part was "Postgresql treats identifiers case insensitively when not quoted (it actually folds them to lowercase internally), and case sensitively when quoted." This means my query of `SELECT * FROM chat_history_DB` was being treated the same as `SELECT * FROM chat_history_db`. In order to preserve the capitolization, I needed to rephrase the query as `SELECT * FROM "chat_history_DB"` (which worked).
2. After deplying to Heroku, I still couldn't get my program to run after fixing the environmental variables. Looking at the heroku logs, I was able to see that I still had the `import editdistance` line from where I used it in hw10 (which I repurposed for the project instead of building from scratch). HW10 was built off the completed lecture 11 example, which already had a requirements.txt file. This requirements.txt file didn't have a line for the edit distace module I started importing later, so when heroku tried to build it failed.
3. When I first started to program the chat bot, I was trying to figure out how to get it to have its own socket to reply on. I spent more time trying to figure this out than I would like to admit, but I eventually realized the very simple solution. The chat bot didn't need to broadcast anything. It just needed to reply to any message the server flagged as a potential command and passed into the bot. It just needed to take in a string and return a string. The server could then add its response to the message history and rebroadcast that with no issues, since that is what it was doing with all other messages anyway. That was much simpler and easier to implement.
4. When making the help command for the chat bot, I made a rather long string. This was the first time I had sent a long message through the chat app and when I prompted the chat bot to see that response, I didn't see anything. The bot still responded to the rest of my messages, but not this. Looking at the server logs, I was able to see that the problem occurred when I tried to save that message in the chat history database. When I made the database, I didn't put too much thought into it and left only 120 characters as the maximum amount i could store for a single message. Having identified the problem, there were two solutions: Redo the database to allow for the longer message, or make sure chat bot will never send a message that is too long and add a check in the server to handle user submitted messages that are too long. Redoing the database only temporarily solves the problem as the limit will still exist, just at a higher level. I implemented the second solution, but did add the database resize as a possible improvement for the future.
5. 

## TODOs and Improvements
1. Add a background image to the chat room
   - **Resolved** - Added my dragon origami picture as a backgound to the chat history div and added to diagonal gradient to the main body to "match" 
2. Make number of connected users always visible
   - **Resolved** - Added a new react component to the page that takes in the number of users and updates it with hooks triggered on emits that will have a new value
3. Make sure page doesn't scroll
   - **Resolved** - Fixed the number of displayed messages to not exceed a certain amount (currently set at 24)
4. Chatbot
   - Uses its own class
     - **Resolved** - Chat bot is a class that is the server can ask for responses. Addtional functions still need to be added to customize chat bot's responses, but the querying of chat bot and broadcasting its' replies is finished
   - Identifiable visually
     - **Partially Resolved** - Added a class to each 'li'  element of chat history to differentiate formatting between 'user' and 'bot' messages. Currently, the class is being derived from the sender's username. When I am eventually forced to redo the database format, this class will be stored and retrueved directly from the database.
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
   - **Resolved** - Added a new react component to the page that takes in the number of users and updates it with hooks triggered on emits that will have a new value
6. Clean up dead and commented out code
   - **Partially Resolved** - Most commented out code has been removed, but I did leave the list comprehension that will be utilized again after the database is reworked.
7. HTML/CSS improvements
   - **Resolved** - Basic formatting is done, but there is a lot of room for improvement. EDIT: acceptable levels of styling have been achieved
8. Rework Database to increase max message length from 120 characters, decrease username max length from 120 characters, and add a class attribute that will be either 'user' or 'bot' (not required for milestone)
   - **Unresolved** - unattempted
9. My patch of default usernames could assign to users the same username if an already connected user manually deletes their assigned username and someone new connects while that field is blank
   - **Unresolved** - I suspect later milestones will have a more rigorous login system implemented and this problem will be removed and overwritten, but I am noting it here just in case it doesn't.
