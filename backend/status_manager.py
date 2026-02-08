import json
import os
import time
from datetime import datetime

# Path to the public status file
STATUS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public', 'agent_status.json')

def update_agent_status(name, role, status, current_assignment):
    """
    Updates the status of a specific agent in the shared JSON file.
    """
    agents = []
    
    # Read existing status
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                agents = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    # Find and update, or append new agent
    agent_found = False
    for agent in agents:
        if agent['name'] == name:
            agent['role'] = role
            agent['status'] = status
            agent['current_assignment'] = current_assignment
            agent['last_updated'] = datetime.now().isoformat()
            agent_found = True
            break
    
    if not agent_found:
        agents.append({
            "name": name,
            "role": role,
            "status": status,
            "current_assignment": current_assignment,
            "last_updated": datetime.now().isoformat()
        })
    
    # Write back to file
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(agents, f, indent=2)
    except IOError as e:
        print(f"Status Manager: Failed to update status for {name}: {e}")

def get_agent_status(name):
    """
    Retrieves the current status of a specific agent.
    """
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                agents = json.load(f)
                for agent in agents:
                    if agent['name'] == name:
                        return agent
        except:
            pass
    return None
