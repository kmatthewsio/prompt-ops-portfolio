#!/usr/bin/env python3
"""
Quick fix for ArcOS database schema issues
"""

import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_API_KEY"))


def get_database_properties(db_id):
    """Get the actual properties of a database"""
    try:
        db = notion.databases.retrieve(db_id)
        properties = {}
        for prop_name, prop_info in db['properties'].items():
            properties[prop_name] = prop_info['type']
        return properties
    except Exception as e:
        print(f"Error getting database properties: {e}")
        return {}


def create_safe_notion_task(pillar, title, data):
    """Create task with only properties that exist in the database"""
    try:
        db_id = {
            'tasks': os.getenv("TASKS_DB_ID"),
            'content': os.getenv("CONTENT_DB_ID"),
            'health': os.getenv("HEALTH_DB_ID"),
            'finance': os.getenv("FINANCE_DB_ID"),
            'training': os.getenv("TRAINING_DB_ID")
        }.get(pillar)

        if not db_id:
            return {"error": f"Database not configured for {pillar}"}

        # Get actual database properties
        db_props = get_database_properties(db_id)
        print(f"Available properties for {pillar}: {list(db_props.keys())}")

        # Start with just the title (which should always exist)
        properties = {}

        # Add Title (required)
        if 'Title' in db_props:
            properties["Title"] = {"title": [{"text": {"content": title}}]}
        elif 'title' in db_props:
            properties["title"] = {"title": [{"text": {"content": title}}]}

        # Add other properties only if they exist in the database
        if pillar == 'content':
            if 'Status' in db_props:
                properties["Status"] = {"select": {"name": "Idea"}}
            if 'Content Type' in db_props:
                properties["Content Type"] = {"select": {"name": "Article"}}
            if 'Topic' in db_props:
                properties["Topic"] = {"rich_text": [{"text": {"content": data.get('topic', '')}}]}
            if 'Word Count' in db_props:
                properties["Word Count"] = {"number": data.get('word_count', 0)}

        elif pillar == 'health':
            if 'Activity Type' in db_props:
                properties["Activity Type"] = {"select": {"name": "Workout"}}
            if 'Duration' in db_props and db_props['Duration'] == 'number':
                # Extract number from duration data
                duration = data.get('duration', 30)
                if isinstance(duration, str):
                    # Try to extract number from string like "45 minutes"
                    import re
                    numbers = re.findall(r'\d+', duration)
                    duration = int(numbers[0]) if numbers else 30
                properties["Duration"] = {"number": duration}
            if 'Date' in db_props:
                properties["Date"] = {"date": {"start": "2024-01-15"}}

        elif pillar == 'finance':
            if 'Category' in db_props:
                properties["Category"] = {"select": {"name": "Expense"}}
            if 'Amount' in db_props:
                properties["Amount"] = {"number": data.get('amount', 0)}
            if 'Date' in db_props:
                properties["Date"] = {"date": {"start": "2024-01-15"}}

        elif pillar == 'training':
            if 'Skill Area' in db_props:
                properties["Skill Area"] = {"select": {"name": "Technical"}}
            if 'Status' in db_props:
                properties["Status"] = {"select": {"name": "Not Started"}}
            if 'Progress' in db_props:
                properties["Progress"] = {"number": 0}

        elif pillar == 'tasks':
            if 'Status' in db_props:
                properties["Status"] = {"select": {"name": "New"}}
            if 'Priority' in db_props:
                properties["Priority"] = {"select": {"name": "Medium"}}
            if 'Pillar' in db_props:
                properties["Pillar"] = {"select": {"name": "Operations"}}

        print(f"Creating with properties: {properties}")

        response = notion.pages.create(
            parent={"database_id": db_id},
            properties=properties
        )

        return {"success": True, "page_id": response["id"], "url": response["url"]}

    except Exception as e:
        print(f"Notion error: {e}")
        return {"error": str(e)}


def test_all_databases():
    """Test what properties each database actually has"""
    databases = {
        'tasks': os.getenv("TASKS_DB_ID"),
        'content': os.getenv("CONTENT_DB_ID"),
        'health': os.getenv("HEALTH_DB_ID"),
        'finance': os.getenv("FINANCE_DB_ID"),
        'training': os.getenv("TRAINING_DB_ID")
    }

    print("🔍 Checking Database Schemas:")
    print("=" * 40)

    for pillar, db_id in databases.items():
        if db_id:
            props = get_database_properties(db_id)
            print(f"\n{pillar.upper()} Database:")
            for prop_name, prop_type in props.items():
                print(f"  - {prop_name}: {prop_type}")
        else:
            print(f"\n{pillar.upper()}: Not configured")


if __name__ == "__main__":
    print("🔧 ArcOS Database Schema Checker")
    test_all_databases()

    print("\n🧪 Testing Safe Task Creation:")

    # Test health task creation
    result = create_safe_notion_task(
        "health",
        "45 minute workout",
        {"duration": 45, "activity": "workout"}
    )
    print(f"Health task result: {result}")

    # Test content task
    result = create_safe_notion_task(
        "content",
        "Test article about AI",
        {"topic": "AI automation", "word_count": 500}
    )
    print(f"Content task result: {result}")