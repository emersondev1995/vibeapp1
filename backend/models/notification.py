# Import the complete Notification model from main.py to avoid conflicts
# The main.py file contains the complete Notification model with all fields
from main import Notification

# Re-export Notification for compatibility with existing imports
__all__ = ['Notification']
