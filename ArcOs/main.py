#!/usr/bin/env python3
"""
ArcOS - Simplified Personal Operating System
Integrates Notion, OpenAI, and Make.com for intelligent automation
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


class ArcOSQuarterback:
    """The main AI quarterback that routes commands"""

    def __init__(self):
        self.system_prompt = """You are the ArcOS Quarterback - an intelligent personal operating system.

Your job is to analyze user commands and determine:
1. Which pillar this belongs to: content, health, finance, training, or general tasks
2. What action to take: create_task, generate_content, log_activity, etc.
3. Whether to trigger automation (true/false)

Respond with JSON only:
{
    "pillar": "content|health|finance|training|tasks",
    "action": "create_task|generate_content|log_activity|track_expense|schedule_learning",
    "title": "descriptive title for the task",
    "data": {"key": "value pairs of relevant data"},
    "automation": true/false
}

Examples:
- "Write an article about AI" → content pillar, generate_content action
- "Log 30 minute workout" → health pillar, log_activity action  
- "Track $50 grocery expense" → finance pillar, track_expense action
- "Learn Python Flask" → training pillar, schedule_learning action"""

    def analyze_command(self, command):
        """Analyze user command and return routing decision"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze this command: {command}"}
                ],
                max_tokens=300,
                temperature=0.3
            )

            result = response.choices[0].message.content.strip()

            # Try to parse JSON response
            try:
                if '{' in result:
                    json_start = result.find('{')
                    json_end = result.rfind('}') + 1
                    json_str = result[json_start:json_end]
                    return json.loads(json_str)
                else:
                    return self._fallback_analysis(command)
            except json.JSONDecodeError:
                return self._fallback_analysis(command)

        except Exception as e:
            print(f"QB analysis error: {e}")
            return self._fallback_analysis(command)

    def _fallback_analysis(self, command):
        """Simple keyword-based fallback if GPT fails"""
        command_lower = command.lower()

        if any(word in command_lower for word in ['write', 'article', 'content', 'blog', 'post']):
            return {
                "pillar": "content",
                "action": "generate_content",
                "title": f"Content: {command}",
                "data": {"topic": command, "word_count": 500},
                "automation": True
            }
        elif any(word in command_lower for word in ['workout', 'exercise', 'run', 'walk', 'health']):
            return {
                "pillar": "health",
                "action": "log_activity",
                "title": f"Health: {command}",
                "data": {"activity": command, "duration": 30},
                "automation": False
            }
        elif any(word in command_lower for word in ['expense', 'spend', 'buy', 'cost', 'budget']):
            return {
                "pillar": "finance",
                "action": "track_expense",
                "title": f"Finance: {command}",
                "data": {"description": command},
                "automation": False
            }
        elif any(word in command_lower for word in ['learn', 'study', 'course', 'skill', 'training']):
            return {
                "pillar": "training",
                "action": "schedule_learning",
                "title": f"Training: {command}",
                "data": {"skill": command},
                "automation": False
            }
        else:
            return {
                "pillar": "tasks",
                "action": "create_task",
                "title": command,
                "data": {"description": command},
                "automation": False
            }


# Initialize QB
quarterback = ArcOSQuarterback()


def create_notion_task(pillar, title, data, status="New"):
    """Create a task in the appropriate Notion database"""
    try:
        db_id = DATABASES.get(pillar)
        if not db_id:
            return {"error": f"Database not configured for {pillar}"}

        # Base properties all databases should have
        properties = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Created": {"date": {"start": datetime.now().isoformat()}},
        }

        # Add pillar-specific properties
        if pillar == 'content':
            properties.update({
                "Status": {"select": {"name": "Idea"}},
                "Content Type": {"select": {"name": "Article"}},
                "Topic": {"rich_text": [{"text": {"content": data.get('topic', '')}}]},
                "Word Count": {"number": data.get('word_count', 0)}
            })
        elif pillar == 'health':
            properties.update({
                "Activity Type": {"select": {"name": "Workout"}},
                "Duration": {"number": data.get('duration', 30)},
                "Date": {"date": {"start": datetime.now().isoformat()}}
            })
        elif pillar == 'finance':
            properties.update({
                "Category": {"select": {"name": "Expense"}},
                "Amount": {"number": data.get('amount', 0)},
                "Date": {"date": {"start": datetime.now().isoformat()}}
            })
        elif pillar == 'training':
            properties.update({
                "Skill Area": {"select": {"name": "Technical"}},
                "Status": {"select": {"name": "Not Started"}},
                "Progress": {"number": 0}
            })
        elif pillar == 'tasks':
            properties.update({
                "Status": {"select": {"name": "New"}},
                "Priority": {"select": {"name": "Medium"}},
                "Pillar": {"select": {"name": "Operations"}}
            })

        response = notion.pages.create(
            parent={"database_id": db_id},
            properties=properties
        )

        return {"success": True, "page_id": response["id"], "url": response["url"]}

    except Exception as e:
        print(f"Notion error: {e}")
        return {"error": str(e)}


def trigger_make_automation(pillar, action, data):
    """Trigger Make.com automation"""
    try:
        webhook_url = os.getenv("MAKE_WEBHOOK_URL")
        if not webhook_url:
            return {"message": "No webhook configured"}

        payload = {
            "source": "arcos",
            "pillar": pillar,
            "action": action,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

        response = requests.post(webhook_url, json=payload, timeout=10)

        if response.status_code == 200:
            return {"success": True, "message": "Automation triggered"}
        else:
            return {"error": f"Webhook failed: {response.status_code}"}

    except Exception as e:
        return {"error": f"Automation error: {str(e)}"}


@app.route('/command', methods=['POST'])
def process_command():
    """Main command endpoint - the heart of ArcOS"""
    try:
        data = request.json
        command = data.get('command')

        if not command:
            return jsonify({"error": "Command required"}), 400

        print(f"🧠 Processing: {command}")

        # QB analyzes the command
        analysis = quarterback.analyze_command(command)
        print(f"📊 QB Analysis: {analysis}")

        # Execute the action
        pillar = analysis.get('pillar', 'tasks')
        title = analysis.get('title', command)
        task_data = analysis.get('data', {})

        # Create task in Notion
        notion_result = create_notion_task(pillar, title, task_data)

        # Trigger automation if needed
        automation_result = None
        if analysis.get('automation', False):
            automation_result = trigger_make_automation(
                pillar,
                analysis.get('action'),
                {**task_data, 'page_id': notion_result.get('page_id')}
            )

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


@app.route('/specialist/<pillar>', methods=['POST'])
def specialist_advice(pillar):
    """Get advice from specialist GPTs"""
    try:
        data = request.json
        question = data.get('question', '')

        specialist_prompts = {
            'content': "You are a content creation specialist. Help with writing, editing, SEO, and content strategy.",
            'health': "You are a health and fitness specialist. Help with workouts, nutrition, and wellness.",
            'finance': "You are a personal finance specialist. Help with budgeting, investing, and money management.",
            'training': "You are a learning and development specialist. Help with skill acquisition and training plans.",
            'tasks': "You are a productivity specialist. Help with task management and workflow optimization."
        }

        if pillar not in specialist_prompts:
            return jsonify({"error": "Invalid specialist"}), 400

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": specialist_prompts[pillar]},
                {"role": "user", "content": question}
            ],
            max_tokens=500
        )

        advice = response.choices[0].message.content

        return jsonify({
            "specialist": pillar,
            "question": question,
            "advice": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/webhook/make', methods=['POST'])
def make_webhook():
    """Handle webhooks from Make.com"""
    try:
        data = request.json
        print(f"📡 Make.com webhook: {data}")

        action = data.get('action')
        page_id = data.get('page_id')

        if action == 'content_generated' and page_id:
            # Update the Notion page with completion status
            notion.pages.update(
                page_id=page_id,
                properties={
                    "Status": {"select": {"name": "AI Generated"}}
                }
            )
            print(f"✅ Updated page {page_id} status to AI Generated")

        return jsonify({"success": True, "message": "Webhook processed"})

    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def system_status():
    """Check ArcOS system status"""
    try:
        status = {
            "system": "ArcOS v0.1 - Simplified",
            "quarterback": "Active",
            "databases": {},
            "integrations": {}
        }

        # Check databases
        for pillar, db_id in DATABASES.items():
            if db_id:
                try:
                    notion.databases.retrieve(db_id)
                    status["databases"][pillar] = "✅ Connected"
                except:
                    status["databases"][pillar] = "❌ Error"
            else:
                status["databases"][pillar] = "⚠️ Not Configured"

        # Check integrations
        status["integrations"]["notion"] = "✅ Connected" if os.getenv("NOTION_API_KEY") else "❌ No API Key"
        status["integrations"]["openai"] = "✅ Connected" if os.getenv("OPENAI_API_KEY") else "❌ No API Key"
        status["integrations"]["make"] = "✅ Configured" if os.getenv("MAKE_WEBHOOK_URL") else "⚠️ No Webhook"

        return jsonify(status)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """Simple home page"""
    return """
    <h1>🤖 ArcOS - Personal Operating System</h1>
    <p>Your intelligent automation layer is running!</p>

    <h3>🧪 Test Commands:</h3>
    <pre>
    curl -X POST http://localhost:5000/command \\
      -H "Content-Type: application/json" \\
      -d '{"command": "Write an article about productivity"}'

    curl -X POST http://localhost:5000/command \\
      -H "Content-Type: application/json" \\
      -d '{"command": "Log 30 minute workout"}'

    curl http://localhost:5000/status
    </pre>

    <h3>📊 System Status:</h3>
    <a href="/status">Check Status</a>
    """


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("🚀 ArcOS Starting...")
    print(f"🧠 Quarterback: Online")
    print(f"🔗 Databases: {len([db for db in DATABASES.values() if db])}/5 configured")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"📡 Webhook: {'Configured' if os.getenv('MAKE_WEBHOOK_URL') else 'Not configured'}")
    print("=" * 50)

    app.run(host='0.0.0.0', port=port, debug=True)