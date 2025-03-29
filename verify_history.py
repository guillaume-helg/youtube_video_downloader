import os
import json
import sys
sys.path.append(os.path.join(os.getcwd(), 'src'))
from pytubeApi import PytubeApi

def test_history():
    print("Testing History Manager...")
    api = PytubeApi()
    
    # Check if history file exists
    if os.path.exists(api.history_file):
        print(f"✓ History file found at {api.history_file}")
    else:
        print("✗ History file NOT found")
        return

    # Add a dummy entry
    test_id = "test_abc_123"
    test_title = "Test Song"
    api._add_to_history(test_id, test_title)
    
    # Verify it exists
    if api.is_already_downloaded(test_id):
        print(f"✓ Dummy song '{test_title}' correctly added to history.")
    else:
        print("✗ Dummy song NOT found in history after adding.")

    # List history
    history = api._get_history()
    print(f"Current history count: {len(history)}")
    
    # Cleanup (manual if needed, or leave it)
    print("Test Complete.")

if __name__ == "__main__":
    test_history()
