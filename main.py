from app import Game

import os

if __name__ == "__main__":
    print(os.getcwd())
    total = 0

    for root, dirs, files in os.walk(f"{os.getcwd()}/app"):
        for fileName in files:
            if not fileName.endswith(".py"):
                continue
            with open(os.path.join(root, fileName), "r") as fileInstance:
                while fileInstance.readline():
                    total += 1

    print(f"Total app lines: {total}")

    game = Game()
    game.start()
