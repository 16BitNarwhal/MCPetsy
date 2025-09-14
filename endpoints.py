from flask import Flask, request, jsonify
import asyncio
import threading
from agent import main as run_agent

app = Flask(__name__)

agent_running = False

@app.route('/trigger-agent', methods=['POST'])
def trigger_agent():
    """POST endpoint to trigger the agent.py script"""
    global agent_running
    
    if agent_running:
        return jsonify({"error": "Agent already running"}), 400
    
    agent_running = True
    
    def run_agent_async():
        global agent_running
        try:
            asyncio.run(run_agent())
        finally:
            agent_running = False
    
    threading.Thread(target=run_agent_async, daemon=True).start()
    
    return jsonify({"message": "Agent started"}), 200

@app.route('/conversation-finished', methods=['POST'])
def conversation_finished():
    """POST endpoint called when conversation is finished"""
    global agent_running
    
    agent_running = False
    return jsonify({"message": "Conversation finished"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)