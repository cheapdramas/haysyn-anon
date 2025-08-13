## Service for holding posts from website

Here we have (nonvolatile)Redis as posts storage

post_id : {
    "text": str,
    "tg_id": str | None,
    etc
}

# Work principle: 
    When website adding post, connect to redis storage, store post there
    Telegram bot listening websocket, which send every new post appiered in Redis to admin
    Admin approves or declines post:
        Approves: send POST request to website API /post with post data, remove post from Redis storage
        Declines: simply remove post from Redis storage




