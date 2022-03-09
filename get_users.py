import sys
import csv
from twitter_utils import get_retweeters, get_likers

WRONG_PARAM = (
    "Zły parametr. Dostępne opcje:"
    "\n\tlikes - konta co polubiły tweet"
    "\n\tretweets - konta co retweetowały tweet"
    "\n\tall - konta co polubiły lub retweetowały tweet."
)


def save_to_file(usernames, filename, url):
    # gets status id
    status_id = url.split("/")[-1]

    with open(f"output/{status_id}_{filename}.txt", "w") as file:
        for username in usernames:
            file.write(f"{username}\n")


def get_input():
    # opens input file and reads urls
    with open("input.csv", "r") as input:
        inputreader = csv.reader(input)
        urls = []
        for index, row in enumerate(inputreader):
            # skips first row with column names
            if index == 0:
                continue
            urls.append((row[0]))
        return urls


def main():
    # check shell params. If none given, prints out error msg and kills program
    if len(sys.argv) == 1:
        print(WRONG_PARAM)
        sys.exit()

    # get shell params
    param = sys.argv[1]

    # gets urls from input file
    urls = get_input()

    if param == "likes":
        # for each url from input file gets likers and saves to file in output folder.
        # Filename format [status_id]_likes.txt
        for url in urls:
            likers = get_likers(url)
            save_to_file(likers, "likers", url)
    elif param == "retweets":
        # for each url from input file gets getweeters and saves to file in output folder.
        # Filename format [status_id]_retweeters.txt
        for url in urls:
            retweeters = get_retweeters(url)
            save_to_file(retweeters, "retweeters", url)
    elif param == "all":
        # for each url from input file gets likers and getweeters and saves to file in output folder.
        # Filename format [status_id]_likes.txt
        # Filename format [status_id]_retweeters.txt
        for url in urls:
            likers = get_likers(url)
            save_to_file(likers, "likers", url)
            retweeters = get_retweeters(url)
            save_to_file(retweeters, "retweeters", url)

    else:
        print(WRONG_PARAM)


if __name__ == "__main__":
    main()
