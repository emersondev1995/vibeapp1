# Import the complete User model from main.py to avoid conflicts
# The main.py file contains the complete User model with all fields
from main import User

# Re-export User for compatibility with existing imports
__all__ = ['User']
