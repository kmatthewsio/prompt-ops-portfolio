#!/usr/bin/env python3
"""
Simple Integration Test
Tests Notion, OpenAI, and Make.com connections
"""

import os
import requests
import json
from notion_client import Client
import openai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def test_notion():
    """Test Notion connection"""
    print("🔵 Testing Notion...")

    try:
        notion = Client(auth=os.getenv("NOTION_API_KEY"))

        # Test 1: Create a simple page
        response = notion.pages.create(
            parent={"database_id": os.getenv("TEST_DATABASE_ID")},
            properties={
                "Title": {
                    "title": [{"text": {"content": f"Test Page {datetime.now().strftime('%H:%M')}"}}]
                },
                "Status": {
                    "select": {"name": "Test"}
                }
            }
        )

        page_id = response["id"]
        print(f"✅ Notion: Created test page {page_id}")

        # Test 2: Read the page back
        page = notion.pages.retrieve(page_id)
        title = page["properties"]["Title"]["title"][0]["text"]["content"]
        print(f"✅ Notion: Read page title '{title}'")

        return page_id

    except Exception as e:
        print(f"❌ Notion error: {e}")
        return None


def test_openai():
    """Test OpenAI connection"""
    print("\n🟢 Testing OpenAI...")

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Write one sentence about automation."}
            ],
            max_tokens=50
        )

        content = response.choices[0].message.content
        print(f"✅ OpenAI: Generated content: '{content}'")

        return content

    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return None


def test_make_webhook():
    """Test Make.com webhook"""
    print("\n🟠 Testing Make.com webhook...")

    webhook_url = os.getenv("MAKE_WEBHOOK_URL")

    if not webhook_url:
        print("⚠️  Make.com: No webhook URL configured")
        print("   Set MAKE_WEBHOOK_URL in your .env file")
        return False

    try:
        test_data = {
            "test": True,
            "message": "Integration test from Python",
            "timestamp": datetime.now().isoformat(),
            "source": "integration_test"
        }

        response = requests.post(webhook_url, json=test_data, timeout=10)

        if response.status_code == 200:
            print(f"✅ Make.com: Webhook responded {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
            return True
        else:
            print(f"❌ Make.com: Webhook failed {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Make.com error: {e}")
        return False


def test_full_workflow():
    """Test complete workflow: Notion → OpenAI → Make.com"""
    print("\n🚀 Testing Complete Workflow...")

    # Step 1: Create Notion page
    page_id = test_notion()
    if not page_id:
        print("❌ Workflow failed: Cannot create Notion page")
        return

    # Step 2: Generate content
    content = test_openai()
    if not content:
        print("❌ Workflow failed: Cannot generate content")
        return

    # Step 3: Send to Make.com
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")
    if webhook_url:
        try:
            workflow_data = {
                "page_id": page_id,
                "generated_content": content,
                "action": "test_workflow",
                "timestamp": datetime.now().isoformat()
            }

            response = requests.post(webhook_url, json=workflow_data, timeout=10)

            if response.status_code == 200:
                print("✅ Complete workflow successful!")
                print(f"   Page ID: {page_id}")
                print(f"   Content: {content[:50]}...")
                print(f"   Make.com: {response.status_code}")
            else:
                print(f"⚠️  Workflow partial: Make.com failed {response.status_code}")

        except Exception as e:
            print(f"⚠️  Workflow partial: Make.com error {e}")
    else:
        print("⚠️  Workflow partial: No Make.com webhook configured")
        print("   But Notion + OpenAI work!")


def check_environment():
    """Check if environment variables are set"""
    print("🔧 Checking Environment Variables...")

    required_vars = {
        "NOTION_API_KEY": "Notion integration token",
        "TEST_DATABASE_ID": "Notion database ID for testing",
        "OPENAI_API_KEY": "OpenAI API key"
    }

    optional_vars = {
        "MAKE_WEBHOOK_URL": "Make.com webhook URL (optional for testing)"
    }

    all_good = True

    for var, description in required_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing ({description})")
            all_good = False

    for var, description in optional_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️  {var}: Not set ({description})")

    return all_good


def setup_instructions():
    """Print setup instructions"""
    print("\n📋 Setup Instructions:")
    print("=" * 50)

    print("\n1. Create .env file with:")
    print("NOTION_API_KEY=secret_your_notion_token")
    print("TEST_DATABASE_ID=your_test_database_id")
    print("OPENAI_API_KEY=sk-your_openai_key")
    print("MAKE_WEBHOOK_URL=https://hook.eu1.make.com/your_webhook")

    print("\n2. Notion Setup:")
    print("   - Go to notion.so/my-integrations")
    print("   - Create integration, copy token")
    print("   - Create a simple database with Title and Status properties")
    print("   - Share database with your integration")
    print("   - Copy database ID from URL")

    print("\n3. OpenAI Setup:")
    print("   - Go to platform.openai.com/api-keys")
    print("   - Create new API key")

    print("\n4. Make.com Setup (Optional):")
    print("   - Go to make.com, create account")
    print("   - Create scenario with Custom Webhook")
    print("   - Copy webhook URL")

    print("\n5. Run test:")
    print("   python test_integrations.py")


if __name__ == "__main__":
    print("🧪 Integration Testing Suite")
    print("=" * 50)

    # Check environment
    if not check_environment():
        setup_instructions()
        exit(1)

    print()

    # Run individual tests
    test_notion()
    test_openai()
    test_make_webhook()

    # Run complete workflow
    test_full_workflow()

    print("\n" + "=" * 50)
    print("🏁 Testing Complete!")
    print("\nIf all tests passed, you're ready to build the full ArcOS system!")
    print("If any failed, check the setup instructions above.")