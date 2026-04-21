import sys
sys.path.append('c:\\Users\\varun\\Desktop\\Sports-Website\\Backend')
from app import get_ai_predictions

from flask import Flask
app = Flask(__name__)

with app.app_context():
    from nba_ai_system import initialize_nba_ai, get_top_scorers
    initialize_nba_ai()
    try:
        print("Top scorers:", get_top_scorers(2))
    except Exception as e:
        import traceback
        traceback.print_exc()
