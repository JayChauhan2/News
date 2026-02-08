import json
import os
import sys

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.journalist import dossier

# Create dummy assignment
ASSIGNMENTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'public', 'assignments.json')
os.makedirs(os.path.dirname(ASSIGNMENTS_FILE), exist_ok=True)

test_ticket = {
    "id": "thinking_test_789",
    "title": "NASA announces discovery of water on Mars moon",
    "source_link": "https://twitter.com/NASA/status/987654321",
    "category": "Science",
    "status": "assigned"
}

with open(ASSIGNMENTS_FILE, 'w') as f:
    json.dump([test_ticket], f)

print("Created dummy assignment for thinking test.")

# Run dossier processing
try:
    dossier.process_assignments()
except Exception as e:
    print(f"Error processing assignments: {e}")

# Check result
dossier_path = os.path.join(os.path.dirname(ASSIGNMENTS_FILE), 'dossiers', 'thinking_test_789.json')
if os.path.exists(dossier_path):
    print("Dossier created.")
else:
    print("Dossier not created.")
