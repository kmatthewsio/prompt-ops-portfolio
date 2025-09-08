#!/usr/bin/env python3
"""
Create ArcOS Databases - Fixed Version
Sets up all 5 core databases for the ArcOS system
"""

import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))


def get_parent_page():
    """Get or create a parent page for databases"""
    try:
        print("📄 Creating ArcOS workspace page...")
        response = notion.pages.create(
            parent={"type": "workspace", "workspace": True},
            properties={
                "title": {
                    "title": [{"type": "text", "text": {"content": "ArcOS Workspace"}}]
                }
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "ArcOS Database Hub"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {
                            "content": "All ArcOS databases for personal automation and intelligence."}}]
                    }
                }
            ]
        )

        page_id = response["id"]
        print(f"✅ Created ArcOS workspace page: {page_id}")
        return page_id

    except Exception as e:
        print(f"❌ Error creating workspace page: {e}")
        print("\n🔧 Manual Setup Required:")
        print("1. Create a new page in Notion called 'ArcOS Workspace'")
        print("2. Copy the page ID from the URL")
        print("3. Enter it below:")

        page_id = input("Enter page ID (32 characters): ").strip()
        if len(page_id) == 32:
            return page_id
        else:
            print("❌ Invalid page ID")
            return None


def create_tasks_database(parent_page_id):
    """Create the Tasks database"""
    print("📋 Creating Tasks Database...")

    try:
        response = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Tasks"}}],
            properties={
                "Title": {"title": {}},
                "Status": {
                    "select": {
                        "options": [
                            {"name": "New", "color": "gray"},
                            {"name": "In Progress", "color": "yellow"},
                            {"name": "Completed", "color": "green"},
                            {"name": "Blocked", "color": "red"}
                        ]
                    }
                },
                "Pillar": {
                    "select": {
                        "options": [
                            {"name": "Content", "color": "blue"},
                            {"name": "Health", "color": "green"},
                            {"name": "Finance", "color": "yellow"},
                            {"name": "Training", "color": "purple"},
                            {"name": "Operations", "color": "orange"}
                        ]
                    }
                },
                "Priority": {
                    "select": {
                        "options": [
                            {"name": "High", "color": "red"},
                            {"name": "Medium", "color": "yellow"},
                            {"name": "Low", "color": "gray"}
                        ]
                    }
                },
                "Created": {"date": {}},
                "Notes": {"rich_text": {}}
            }
        )

        db_id = response['id']
        print(f"✅ Tasks Database: {db_id}")
        return db_id

    except Exception as e:
        print(f"❌ Tasks Database error: {e}")
        return None


def create_content_database(parent_page_id):
    """Create the Content database"""
    print("📝 Creating Content Database...")

    try:
        response = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Content"}}],
            properties={
                "Title": {"title": {}},
                "Status": {
                    "select": {
                        "options": [
                            {"name": "Idea", "color": "gray"},
                            {"name": "Draft", "color": "orange"},
                            {"name": "Review", "color": "purple"},
                            {"name": "Published", "color": "green"},
                            {"name": "AI Generated", "color": "blue"}
                        ]
                    }
                },
                "Content Type": {
                    "select": {
                        "options": [
                            {"name": "Article", "color": "blue"},
                            {"name": "Blog Post", "color": "green"},
                            {"name": "Social Post", "color": "yellow"},
                            {"name": "Email", "color": "purple"}
                        ]
                    }
                },
                "Word Count": {"number": {}},
                "Topic": {"rich_text": {}},
                "Created": {"date": {}}
            }
        )

        db_id = response['id']
        print(f"✅ Content Database: {db_id}")
        return db_id

    except Exception as e:
        print(f"❌ Content Database error: {e}")
        return None


def create_health_database(parent_page_id):
    """Create the Health database"""
    print("💪 Creating Health Database...")

    try:
        response = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Health"}}],
            properties={
                "Title": {"title": {}},
                "Activity Type": {
                    "select": {
                        "options": [
                            {"name": "Workout", "color": "red"},
                            {"name": "Cardio", "color": "orange"},
                            {"name": "Strength", "color": "purple"},
                            {"name": "Walk", "color": "blue"},
                            {"name": "Sleep", "color": "gray"}
                        ]
                    }
                },
                "Duration": {"number": {}},
                "Date": {"date": {}},
                "Notes": {"rich_text": {}}
            }
        )

        db_id = response['id']
        print(f"✅ Health Database: {db_id}")
        return db_id

    except Exception as e:
        print(f"❌ Health Database error: {e}")
        return None


def create_finance_database(parent_page_id):
    """Create the Finance database"""
    print("💰 Creating Finance Database...")

    try:
        response = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Finance"}}],
            properties={
                "Title": {"title": {}},
                "Category": {
                    "select": {
                        "options": [
                            {"name": "Income", "color": "green"},
                            {"name": "Expense", "color": "red"},
                            {"name": "Investment", "color": "blue"},
                            {"name": "Budget", "color": "orange"}
                        ]
                    }
                },
                "Amount": {"number": {"format": "dollar"}},
                "Date": {"date": {}},
                "Notes": {"rich_text": {}}
            }
        )

        db_id = response['id']
        print(f"✅ Finance Database: {db_id}")
        return db_id

    except Exception as e:
        print(f"❌ Finance Database error: {e}")
        return None


def create_training_database(parent_page_id):
    """Create the Training database"""
    print("🎓 Creating Training Database...")

    try:
        response = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Training"}}],
            properties={
                "Title": {"title": {}},
                "Skill Area": {
                    "select": {
                        "options": [
                            {"name": "Technical", "color": "blue"},
                            {"name": "Business", "color": "green"},
                            {"name": "Creative", "color": "purple"},
                            {"name": "Personal", "color": "yellow"}
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": "Not Started", "color": "gray"},
                            {"name": "In Progress", "color": "yellow"},
                            {"name": "Completed", "color": "green"}
                        ]
                    }
                },
                "Progress": {"number": {"format": "percent"}},
                "Start Date": {"date": {}},
                "Notes": {"rich_text": {}}
            }
        )

        db_id = response['id']
        print(f"✅ Training Database: {db_id}")
        return db_id

    except Exception as e:
        print(f"❌ Training Database error: {e}")
        return None


def create_env_file(database_ids):
    """Create .env file with database IDs"""
    print("\n📝 Creating environment configuration...")

    env_content = f"""# ArcOS Environment Configuration
NOTION_API_KEY={os.getenv('NOTION_API_KEY', 'your_notion_token')}
OPENAI_API_KEY={os.getenv('OPENAI_API_KEY', 'your_openai_key')}

# Database IDs
TASKS_DB_ID={database_ids.get('tasks', 'not_created')}
CONTENT_DB_ID={database_ids.get('content', 'not_created')}
HEALTH_DB_ID={database_ids.get('health', 'not_created')}
FINANCE_DB_ID={database_ids.get('finance', 'not_created')}
TRAINING_DB_ID={database_ids.get('training', 'not_created')}

# Server
PORT=5000
"""

    with open('.env.arcos', 'w') as f:
        f.write(env_content)

    print("✅ Created .env.arcos file")


def main():
    print("🚀 ArcOS Database Setup")
    print("=" * 40)

    # Check API key
    if not os.getenv("NOTION_API_KEY"):
        print("❌ NOTION_API_KEY not found")
        print("Add your Notion integration token to .env file")
        return

    # Test connection
    try:
        notion.search(filter={"property": "object", "value": "database"})
        print("✅ Notion connection successful")
    except Exception as e:
        print(f"❌ Notion connection failed: {e}")
        return

    # Get parent page
    parent_page_id = get_parent_page()
    if not parent_page_id:
        print("❌ Cannot create parent page")
        return

    print(f"\n🏗️  Creating databases in page: {parent_page_id}")

    # Create all databases
    database_ids = {}
    database_ids['tasks'] = create_tasks_database(parent_page_id)
    database_ids['content'] = create_content_database(parent_page_id)
    database_ids['health'] = create_health_database(parent_page_id)
    database_ids['finance'] = create_finance_database(parent_page_id)
    database_ids['training'] = create_training_database(parent_page_id)

    # Create env file
   #create_env_file(database_ids)

    # Summary
    successful = [k for k, v in database_ids.items() if v]
    print(f"\n🎉 Created {len(successful)}/5 databases successfully!")

    if len(successful) == 5:
        print("\n📋 Next Steps:")
        print("1. Rename .env.arcos to .env")
        print("2. Add your OpenAI API key")
        print("3. Run: python arcos.py")
    else:
        print(f"⚠️  {5 - len(successful)} databases failed - check errors above")


if __name__ == "__main__":
    main()