from backend.writer import publisher
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

print("Starting manual publication...")
publisher.publish_pending_dossiers()
print("Manual publication finished.")
