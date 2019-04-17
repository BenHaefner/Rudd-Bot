# Rudd-Bot
A Discord bot to do various tasks on my discord server, themed loosley around the actor Paul Rudd.

This bot is partially based on [dxbot](https://github.com/crypticism/dxbot2.0), a bot developed for use in Slack. This bot is able to retain quotes from people in the chat as well as score users. Rudd-Bot's implementation of these features are slightly different. Additionally I was interested in adding in more functionality on top of that enabled by dxbot.

This bot is part of a personal project to become better about applying coding knowledge and skills to improve my every day life and make something to benefit myself and my friends.


## Commands
- $quote: Gets a random quote from the quote database.
- $quote `mention` `text`: Adds a quote to the database attibuted to a specific person.
- $grab: Adds the last message sent before this command to the quote database.
- $lookup `mention`: Gets a random quote from the quote database attributed to the user mentioned.
- $score `mention`: Retrieves the score of a specific user.
- $++ `mention`: Increases the score of a specific user by one.
- $-- `mention`: Decreases the score of a specific user by one.
- $scores: Gets a list of scores for everyone in the database.
- $add_task `keyword` `text`: Adds a task to the database accessible through the keyword.
- $lookup_task `keyword`: Gets the text associated with a task.
- $list_tasks: Lists all the task keywords.
- $end_task `keyword`: Deletes the task associated with a keyword.
- $pin: Pins the last comment. Requires 'manage messages' permissions.


## Work
### Features Complete
- Quote saving and selection
   - Using SQL
- User scoring system
- The ability to store "tasks" and retrieve those tasks based on a single word key.
- Pin comments
- Name requirement enforcement


### Current Features To Implement
- Quote numbering
- Server analytics
- Server-based games (Family Fued)
- Ensure database associated people, tasks, scores, and anything else with specific servers. 
   - Optional for now
- A "Thanos" feature for fun.
- Users will complete 6 challenges and when they do they will be able to mute half the server at random temporarily.
- On user join, add user to the user list if they arent already there.


### Other Maintence
- Comment everything
- Speed up '$scores' function
- Fix styling so things are more consistent



