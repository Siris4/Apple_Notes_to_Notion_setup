# My program syncs Notion database entries to Apple Notes via AppleScript

import subprocess
from notion_client import Client

# Initialize a Notion client with an integration token
notion = Client(auth="Notion_integration_token")

# ID of the Notion database
database_id = "your_database_id"


def sync_to_apple_notes(title, content):
    """Uses AppleScript to sync items to Apple Notes."""
    applescript = f'''
    tell application "Notes"
        tell account "iCloud"
            set new_note to make new note with properties {{name: "{title}", body: "{content}"}}
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])


def fetch_and_sync():
    try:
        results = notion.databases.query(database_id=database_id)
        for page in results.get("results", []):
            properties = page.get("properties", {})
            title = properties.get("Name", {}).get("title", [])
            content = properties.get("Content", {}).get("rich_text", [])

            if title and content:
                title_text = title[0]['plain_text']
                content_text = content[0]['plain_text']
                sync_to_apple_notes(title_text, content_text)

    except Exception as e:
        print("An error occurred:", e)


# Run the sync process
fetch_and_sync()
