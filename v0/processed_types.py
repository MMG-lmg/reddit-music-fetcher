    
class Award:
    name:str
    coin_price:float
    days_of_premium:int
    description: str
    count:int
    
class Post:
    title: str
    flair: str
    subreddit: str
    upvote_ratio : float
    upvotes: int
    downvotes: int
    total_awards: int
    is_original_content: bool
    score: int
    created_utc:int
    awards = [Award]
    id:str
    author:str
    num_comments:str
    url:str
    num_crossposts:int
    is_music_post:bool
    artist = str
    genre = [str]
    song_title = str
    media_url = str
    
class Comment:
    subreddit:str
    author:str
    created_utc:int
    total_awards: int
    awards = [Award]
    score: int
    body: str
    upvote_ratio : float
    upvotes: int
    downvotes: int
    url:str
    parent_id:str

class User:
    id:str
    verified: bool
    mod:bool
    gold:bool
    total_karma:int
    awarder_karma:int
    link_karma:int
    name:str
    created_utc:int
    comment_karma:int
    