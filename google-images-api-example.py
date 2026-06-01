"""
Google Images API: A Quick Start Example
See more at: https://apify.com/johnvc/google-images-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-images-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Images API on Apify from Python and
read its structured JSON output. It exercises several input parameters so you
can see what is configurable, while keeping the run small so your first call
stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Inputs are kept small (a single query, just 5 results) to keep this first run
# inexpensive: you are billed per image returned. Raise maxResultsPerQuery and
# add more queries once you have your own API key and know your budget.
run_input = {
    "queries": ["golden retriever puppy"],  # one or more image searches
    "maxResultsPerQuery": 5,                 # small on purpose to keep it cheap
    "gl": "us",                              # country code for localization
    "hl": "en",                              # interface language code
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-images-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset
# (apify-client 3.x returns a Run object; use .default_dataset_id, not run["..."])
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} image(s).\n")

# Show a few key fields from each image result.
for item in items:
    position = item.get("position")
    title = item.get("title", "")
    image_url = item.get("imageUrl", "")
    width = item.get("imageWidth")
    height = item.get("imageHeight")
    source = item.get("source", "")
    page_link = item.get("link", "")
    print(f"{position}. {title}")
    print(f"   image:  {image_url}  ({width}x{height})")
    print(f"   source: {source}")
    print(f"   page:   {page_link}\n")
