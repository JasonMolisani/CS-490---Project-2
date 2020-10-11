# Chat App

**Jason Molisani's (jm979) CS 490 project 2 - milestone 1** This is a basic chat application built using flask, python, socketio, react, and more. As this is only milestone one, there is still a lot of room for improvements.

## DEPLOYMENT

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
3. 

## TODOs and Improvements
1. Add a background image to the chat room
   - **Unresolved** - unattempted
2. Make number of connected users always visible
   - **Unresolved** - unattempted
3. Make sure page doesn't scroll
   - **Unresolved** - unattempted
4. Chatbot
   - Uses its own class
     - **Unresolved** - unattempted
   - Identifiable visually
     - **Unresolved** - unattempted
   - `!!about` make chat bot give a self description
     - **Unresolved** - unattempted
   - `!!help` chat bot sends a message with all of its commands
     - **Unresolved** - unattempted
   - `!!funtranslate [message]` makes bot echo message translated into choice of [fun language](https://funtranslations.com/api)
     - **Unresolved** - unattempted
   - 1 command that uses some API
     - **Unresolved** - unattempted
   - 1 command that doesn't have to use an API
     - **Unresolved** - unattempted
5. Clients update count on connect/disconnect
   - **Unresolved** - unattempted
6. Clean up dead and commented out code
   - **Unresolved** - unattempted
7. HTML/CSS improvements
   - **Unresolved** - unattempted