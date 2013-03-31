# generate picture url for jekyll post

import os

def main():
    currentDir = os.getcwd()
    files = os.listdir(currentDir)
    prefix = "/home/k100/workspace/blog"
    dirPrefix = currentDir[len(prefix):] + '/'
    for file in sorted(files):
        url = "![Alt](" + dirPrefix + file + ")"
        print url


if __name__ == "__main__":
    main()

