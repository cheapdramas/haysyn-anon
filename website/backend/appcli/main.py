from colorama.ansi import clear_screen
from backend.db.crud import PostCrud, CommentCrud
from backend.db.utils import db_helper 
from backend.schemas.post import (
	PostBase,
	PostCreate,
	PostRead
)
from backend.schemas.comment import (
	CommentBase,
	CommentCreate,
	CommentRead
)
from faker import Faker
from enum import Enum
from colorama import Fore, Back, Style, init

import os

text_sizes = {"small" : 50, "big": 2000}
fake = Faker()

# Automatically reset color after each print statement
init(autoreset=True)


def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')


def createPost(text_size: str, amount: int = 1, ) -> bool:
    "Creates <amount> posts to db with random text"
    #check argument types
    if not isinstance(text_size, str) or not isinstance(amount, int):
        return False
    size_text:int | None = text_sizes.get(text_size)

    if not size_text: 
        print(Fore.RED + f"'{text_size}' is not valid size")
        print(f"Valid sizes: {[size for size in text_sizes.keys()]}")
        return False

    for _ in range(amount):
        post = PostCreate(title="Title", text=fake.text(max_nb_chars=size_text))
        with db_helper.session_factory() as session:
            try:
                created_post = PostCrud.create_post(post, session)
                print(Fore.GREEN + f"Post {created_post.id} created ✅")
            except Exception as e:
                print(Fore.RED + f"❌ Post creation failed! Exception: \n {str(e)}")
    return True


def createComment(post_id: int, amount:int, text_size: str) -> bool:
    if not isinstance(post_id, int) \
        or not isinstance(amount, int) \
        or not isinstance(text_size, str):
        return False
    size_text:int | None = text_sizes.get(text_size)

    if not size_text:
        print(Fore.RED + f"'{text_size}' is not valid size")
        print(f"Valid sizes: {[size for size in text_sizes.keys()]}")
        return False

    for _ in range(amount):
        comment = CommentCreate(post_id=post_id,text=fake.text(max_nb_chars=size_text))
        with db_helper.session_factory() as session:
            try:
                created_comment = CommentCrud.create_comment(comment, session)
                print(Fore.GREEN + f"Comment {created_comment.id} created ✅")
            except Exception as e:
                print(Fore.RED + f"❌ Comment creation failed! Exception: \n {str(e)}")
                break
    return True


def parse_user_input(tokens: list[str]) -> bool:
    operation = tokens[0]

    match operation:

        case 'q':
            return True
        case 'clear':
            clear_term()
            return False


        case "createPost":
            if len(tokens) < 3:
                print(Fore.RED + "Incorrect usage of 'createPost' command \n 'createPost <amount> <text_size: small | big>'")
                return False

            try:
                amount = int(tokens[1])
                text_size = tokens[2]

                createPost(text_size, amount)
            except ValueError:
                print(Fore.RED + "❌ Parameter №1 should be integer (amount of posts)")


        case "createCom":
            if len(tokens) < 4:
                print(Fore.RED + "Incorrect usage of 'createCom' command \n 'createCom <post_id> <amount> <text_size: small | big>'")
                return False
            try:
                post_id = int(tokens[1])
                amount = int(tokens[2])
                text_size = tokens[3]

                createComment(post_id, amount, text_size)
            except ValueError:
                print(Fore.RED + "❌ Parameter №1 should be integer (post_id) and parameter №2 should be integer (amount of comments)")

        case _:
            print(Fore.RED + f"Undefined command: {operation}")
    return False
    

def main():
    clear_term()
    print(Fore.BLUE + "'help' to view all commands")
    print(Fore.BLUE + "'p' to execute previous command")
    print(Fore.RED + "'q' to quit")
    previous_command = ""
    while True:
        user_input = input("\nHaysyn app control 🧰 > ")

        if user_input == 'p':
            #set user_input to previous command
            user_input = previous_command 
            print(previous_command)
        previous_command = user_input

        do_quit = parse_user_input(user_input.split(' '))
        
        if do_quit:
            return 
        
main()
