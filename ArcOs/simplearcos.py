#!/usr/bin/env python3
"""
Simple Working ArcOS - Only uses basic properties that exist
"""

import os
import json
from flask import Flask, request, jsonify
from notion_client import Client
import openai
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Initialize services
notion = Client(auth=os.getenv("NOTION_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database IDs
DATABASES = {
    'tasks': os.getenv("TASKS_DB_ID"),
    'content': os.getenv("CONTENT_DB_ID"),
    'health': os.getenv("HEALTH_DB_ID"),
    'finance': os.getenv("FINANCE_DB_ID"),
    'training': os.getenv("TRAINING_DB_ID")
}


class SimpleQuarterback:
    """Simplified QB that only uses basic properties"""

    def analyze_command(self, command):
        """Simple keyword-based analysis"""
        command_lower = command.lower()

        if any(word in command_lower for word in ['write', 'article', 'content', 'blog', 'post']):
            return {
                "pillar": "content",
                "action": "generate_content",
                "title": command,
                "automation": True
            }
        elif any(word in command_lower for word in
                 ['workout', 'exercise', 'run', 'walk', 'health', 'jog', 'gym', 'cardio', 'fitness']):
            return {
                "pillar": "health",
                "action": "log_activity",
                "title": command,
                "automation": False
            }
        elif any(word in command_lower for word in ['expense', 'spend', 'buy', 'cost', 'budget', '$']):
            return {
                "pillar": "finance",
                "action": "track_expense",
                "title": command,
                "automation": False
            }
        elif any(word in command_lower for word in ['learn', 'study', 'course', 'skill', 'training']):
            return {
                "pillar": "training",
                "action": "schedule_learning",
                "title": command,
                "automation": False
            }
        else:
            return {
                "pillar": "tasks",
                "action": "create_task",
                "title": command,
                "automation": False
            }


quarterback = SimpleQuarterback()


def create_simple_notion_task(pillar, title):
    """Create task with ONLY Title - the most basic approach"""
    try:
        db_id = DATABASES.get(pillar)
        if not db_id:
            return {"error": f"Database not configured for {pillar}"}

        # ONLY use Title - the one property that should always work
        properties = {
            "Title": {"title": [{"text": {"content": title}}]}
        }

        # Try to add Status if it's a known working database
        if pillar in ['content', 'tasks']:
            if pillar == 'content':
                properties["Status"] = {"select": {"name": "Idea"}}
            elif pillar == 'tasks':
                properties["Status"] = {"select": {"name": "New"}}

        response = notion.pages.create(
            parent={"database_id": db_id},
            properties=properties
        )

        return {"success": True, "page_id": response["id"], "url": response["url"]}

    except Exception as e:
        print(f"Notion error: {e}")
        return {"error": str(e)}


@app.route('/command', methods=['POST'])
def process_command():
    """Simplified command processing"""
    try:
        data = request.json
        command = data.get('command')

        if not command:
            return jsonify({"error": "Command required"}), 400

        print(f"Processing: {command}")

        # QB analyzes the command
        analysis = quarterback.analyze_command(command)
        print(f"QB Analysis: {analysis}")

        # Create task with minimal properties
        pillar = analysis.get('pillar', 'tasks')
        title = analysis.get('title', command)

        notion_result = create_simple_notion_task(pillar, title)

        # Trigger automation if needed
        automation_result = None
        if analysis.get('automation', False):
            webhook_url = os.getenv("MAKE_WEBHOOK_URL")
            if webhook_url:
                try:
                    payload = {
                        "source": "simple_arcos",
                        "pillar": pillar,
                        "action": analysis.get('action'),
                        "page_id": notion_result.get('page_id'),
                        "title": title,
                        "timestamp": datetime.now().isoformat()
                    }
                    response = requests.post(webhook_url, json=payload, timeout=10)
                    automation_result = {"success": response.status_code == 200}
                except Exception as e:
                    automation_result = {"error": str(e)}

        return jsonify({
            "success": True,
            "command": command,
            "quarterback_analysis": analysis,
            "notion_result": notion_result,
            "automation_result": automation_result
        })

    except Exception as e:
        print(f"Command error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def system_status():
    """Check which databases actually work"""
    status = {
        "system": "Simple ArcOS",
        "databases": {}
    }

    # Test each database with a simple Title-only creation
    for pillar, db_id in DATABASES.items():
        if db_id:
            try:
                # Just check if we can retrieve the database
                notion.databases.retrieve(db_id)
                status["databases"][pillar] = "Connected"
            except Exception as e:
                status["databases"][pillar] = f"Error: {str(e)[:50]}"
        else:
            status["databases"][pillar] = "Not Configured"

    return jsonify(status)


@app.route('/', methods=['GET'])
def home():
    return """
    <h1>Simple ArcOS - Working Version</h1>
    <p>This version only uses basic Title properties that work in all databases.</p>

    <h3>Test Commands (PowerShell):</h3>
    <pre>
# Content (works well)
Invoke-RestMethod -Uri "http://localhost:5000/command" -Method POST -ContentType "application/json" -Body '{"command": "Write about productivity"}'

# Tasks (works well)  
Invoke-RestMethod -Uri "http://localhost:5000/command" -Method POST -ContentType "application/json" -Body '{"command": "Plan next week"}'

# Others (basic title only)
Invoke-RestMethod -Uri "http://localhost:5000/command" -Method POST -ContentType "application/json" -Body '{"command": "Morning workout"}'
Invoke-RestMethod -Uri "http://localhost:5000/command" -Method POST -ContentType "application/json" -Body '{"command": "Grocery shopping"}'
Invoke-RestMethod -Uri "http://localhost:5000/command" -Method POST -ContentType "application/json" -Body '{"command": "Learn React"}'
    </pre>
    """


if __name__ == '__main__':
    print("Simple ArcOS Starting...")
    print("This version uses minimal properties to ensure compatibility")
    app.run(host='0.0.0.0', port=5000, debug=True)