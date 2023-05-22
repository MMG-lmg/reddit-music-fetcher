# SBP mongo project & finals helper

With this little markdown I will try to add and update kinda randomly all possibly important informations. Will skip some so watch out and @me for more.

# Motivation and basic idea

Project idea is basicly to import a large amount of data as a dataset and plop it into *MongoDB* so that we can see how bad acctualy performances are and we are supposed to optimise that with **magic**. 
- [Project information](http://www.acs.uns.ac.rs/sr/filebrowser/download/7726441)
- [Basic Document database modeling](https://www.acs.uns.ac.rs/sr/filebrowser/download/7726442)  
- [Other usefull links]([https://](https://www.acs.uns.ac.rs/sr/node/237/2629244))


## Data source

Our test set will be provided by my final assignement python script / program of witch more data will be provided further down.  
In its core data is sourced from *Reddit* and its subreddit *r/Music* witch contains a lot of varried music related data.
Feel free to read more about [Reddit API]((https://www.reddit.com/dev/api)) but concepts that intrest me the most are:
- Posts aka. Articles
- Comments on them and replies to comments
- Karma - ratio of upwotes and downvotes
- Awards - user given awards to the article or comment
- Reddit users
- Flairs - super short description of the contents of the article, something like an article type
- Stuctured titles of articles containing *Youtube* links if form of `Artist - Title [Genre]` with multiple genres separated via '/'
- Cake day - the day of opening users reddit account

### Most frequest usage of reddit api

Most common usage of reddit api will be in a form of fetching posts and comments.
Fetching posts can be done in a form of API get request in JSON format via eg. `https://www.reddit.com/r/music/top.json?limit=100&t=all`.
Quite similarly you can do the same with comments `https://www.reddit.com/r/Music/comments/hbhk01.json`. In this case `hbhk01` is Base 36 encoded id of the article found in respective *id* field of the article JSON. 

## Data procesing
Since most of the data is followed with some bloat form Reddit API my python code will be responcible for projecting fetched JSON documents into others more usable documents.  
Procesed JSON documents are going to be dumped into mongo DB via aforementioned python code using basic MongoDB driver [Pymongo](https://www.mongodb.com/docs/drivers/pymongo/) since Object-Document mappers are mostly forbiden and quite frankly usualy a pile of depricated and outdated hot garbage.

### Known limitations

Reddit API is limmiting its usage to up to 60 requests per minute, with 100 items per request.