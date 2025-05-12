from app import Game

import os

if __name__ == "__main__":
    total = 0
    cwd = os.getcwd()

    for root, dirs, files in os.walk(f"{cwd}/app"):
        for fileName in files:
            if not fileName.endswith(".py"):
                continue
            with open(os.path.join(root, fileName), "r") as fileInstance:
                while fileInstance.readline():
                    total += 1

    print(f"Total app lines in: {total}")

    game = Game()
    game.start()
