# Rudd-Bot
A Discord bot to do various tasks on my discord server, themed loosley around the actor Paul Rudd.

This bot is partially based on [dxbot](https://github.com/crypticism/dxbot2.0), a bot developed for use in Slack. This bot is able to retain quotes from people in the chat as well as score users. Rudd-Bot's implementation of these features are slightly different. Additionally I was interested in adding in more functionality on top of that enabled by dxbot.

## Commands
- $quote: Gets a random quote from the quote database.
- $quote /<mention user/> <text>: Adds a quote to the database attibuted to a specific person.
- $grab: Adds the last message sent before this command to the quote database.
- $lookup /<mention user/>: Gets a random quote from the quote database attributed to the user mentioned.
- $score /<mention user/>: Retrieves the score of a specific user.
- $++ /<mention user/>: Increases the score of a specific user by one.
- $-- /<mention user/>: Decreases the score of a specific user by one.
- $scores: Gets a list of scores for everyone in the database.
- $add_task /<keyword/> /<text/>: Adds a task to the database accessible through the keyword.
- $lookup_task /<keyword/>: Gets the text associated with a task.
- $list_tasks: Lists all the task keywords.
- $end_task /<keyword/>: Deletes the task associated with a keyword.

## Work
### Features Complete
- Quote Saving and Selection
   - Using SQL
- User Scoring System
- The ability to store "tasks" and retrieve those tasks based on a single word key.

### Current Features To Implement
 - Quote numbering
 - Name Requirement Enforcement
 - Server Analytics
 - Server-Based Games (Family Fued)
 - Pin comments
 - Ensure database associated people, tasks, scores, and anything else with specific servers.
 - Implement a "Thanos" feature for fun.
   - Users will complete 6 challenges and when they do they will be able to mute half the server at random temporarily.


