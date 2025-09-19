#i know that i can do that in different way, i do not care

case "$1" in
    post)
        cd post_service
        source $(poetry env info -p)/bin/activate
        python3 -m main
        ;;
    web)
        cd website
        source $(poetry env info -p)/bin/activate
        uvicorn backend.main:app --host 0.0.0.0
        ;;
    tg)
        cd telegram_bot
        source $(poetry env info -p)/bin/activate
        python3 -m main
        ;;
    appcli)
        cd website
        source $(poetry env info -p)/bin/activate
				
        python3 -m backend.appcli.main
        ;;
    *)
        echo "Usage: $0 {post|web|tg|appcli}"
        ;;
esac
