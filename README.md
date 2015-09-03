No Context Bot
==============

No Context Bot is a Reddit bot that does two things:

1) Listen to comments that seem to make no sense outside of its context.
It finds these comments by listening for when users reply to a comment with
"/r/nocontext"

2) Reply to comments that say "/r/nocontext" with a random and odd out of
context quote from its collection.

No Context Bot is run using python. Namely, two scripts, one for crawling (1), 
and one for posting (2), are executed concurrently. They both access a MongoDb
database to keep track of out of context comments and which comments it has
already replied to.

Running the bot
---------------

Running the bot is simple:


```
./start.sh
```


start.sh uses nohup to execute both parts in the background.

