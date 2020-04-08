import os, shutil

import requests
import vcr

FIXTURES_FOLDER = "tests/fixtures"

for file_name in os.listdir(FIXTURES_FOLDER):
    print(f"Deleting {FIXTURES_FOLDER}/{file_name}")
    os.remove(f"{FIXTURES_FOLDER}/{file_name}")


with vcr.use_cassette(f"{FIXTURES_FOLDER}/json_placeholder_crud2.yaml"):
    r = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    r = requests.get("https://jsonplaceholder.typicode.com/posts")

    r = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json={"title": "foo", "body": "bar", "userId": 1},
    )

    r = requests.patch(
        "https://jsonplaceholder.typicode.com/posts/1", json={"body": "baz"}
    )

    r = requests.put(
        "https://jsonplaceholder.typicode.com/posts/1",
        json={"title": "foo", "body": "baz", "userId": 1},
    )

    r = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
