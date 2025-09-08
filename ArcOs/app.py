#!/usr/bin/env python3
"""
Force create a single entry in the health database
"""

import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_API_KEY"))


def force_health_entry():
    """Create entry in health database with minimal properties"""
    health_db_id = os.getenv("HEALTH_DB_ID")

    if not health_db_id:
        print("No HEALTH_DB_ID found in .env")
        return

    print(f"Forcing entry into health database: {health_db_id}")

    try:
        # Try with just Title first
        response = notion.pages.create(
            parent={"database_id": health_db_id},
            properties={
                "Title": {"title": [{"text": {"content": "Morning jog - 30 minutes"}}]}
            }
        )

        page_id = response["id"]
        url = response["url"]

        print(f"SUCCESS: Created health entry")
        print(f"Page ID: {page_id}")
        print(f"URL: {url}")

        return {"success": True, "page_id": page_id, "url": url}

    except Exception as e:
        print(f"FAILED: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    print("Creating manual health database entry...")
    result = force_health_entry()

    if result.get("success"):
        print("\nGo check your Health database in Notion!")
        print("You should see: 'Morning jog - 30 minutes'")
    else:
        print("\nHealth database creation failed - there may be schema issues with that database")
