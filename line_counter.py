from os import getcwd, walk, path

def count_lines():
    total = 0
    cwd = getcwd()

    for root, dirs, files in walk(f"{cwd}/app"):
        for fileName in files:
            if not fileName.endswith(".py"):
                continue
            with open(path.join(root, fileName), "r") as fileInstance:
                while fileInstance.readline():
                    total += 1

    return total

def output_lines():
    print(f"Total app lines in project: {count_lines()}")
