import os, shutil

import requests
import vcr

FIXTURES_FOLDER = "tests/fixtures"

for file_name in os.listdir(FIXTURES_FOLDER):
	print(f"Deleting {FIXTURES_FOLDER}/{file_name}")
	os.remove(f"{FIXTURES_FOLDER}/{file_name}")


print("Generating cassette for GET /posts/1")
with vcr.use_cassette(f"{FIXTURES_FOLDER}/get_post.yaml"):
	r = requests.get("https://jsonplaceholder.typicode.com/posts/1", headers={"Accept-Encoding": "gzip"})

print("Generating cassette for GET /posts")
with vcr.use_cassette(f"{FIXTURES_FOLDER}/get_posts.yaml"):
	r = requests.get("https://jsonplaceholder.typicode.com/posts", headers={"Accept-Encoding": "gzip"})

print("Generating cassette for POST /posts")
with vcr.use_cassette(f"{FIXTURES_FOLDER}/post_post.yaml"):
	r = requests.post(
		"https://jsonplaceholder.typicode.com/posts", 
		json={
			"title": "foo",
			"body": "bar",
      		"userId": 1
  		}
	)

print("Generating cassette for PATCH /posts")
with vcr.use_cassette(f"{FIXTURES_FOLDER}/patch_post.yaml"):
	r = requests.patch(
		"https://jsonplaceholder.typicode.com/posts/1", 
		json={
			"body": "baz"
  		}
	)
