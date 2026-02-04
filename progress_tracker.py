"""
Progress Tracker
Handles saving and loading game progress
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional


class ProgressTracker:
    """Tracks and persists game progress"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.progress_file = self.base_dir / "progress.json"
    
    def save_progress(self, challenge: int, step: int):
        """Save current progress"""
        progress_data = {
            "challenge": challenge,
            "step": step,
            "completed_challenges": self._get_completed_challenges(challenge, step)
        }
        
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")
    
    def load_progress(self) -> Optional[Dict]:
        """Load saved progress"""
        if not self.progress_file.exists():
            return None
        
        try:
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load progress: {e}")
            return None
    
    def _get_completed_challenges(self, current_challenge: int, current_step: int) -> list:
        """Get list of completed challenges"""
        completed = []
        
        # Add all previous challenges
        for i in range(1, current_challenge):
            completed.append(i)
        
        return completed
    
    def reset_progress(self):
        """Reset all progress"""
        if self.progress_file.exists():
            self.progress_file.unlink()
    
    def get_completion_percentage(self) -> float:
        """Get completion percentage (0-100)"""
        progress = self.load_progress()
        if not progress:
            return 0.0
        
        total_challenges = 10  # We have 10 challenges
        completed = len(progress.get('completed_challenges', []))
        
        return (completed / total_challenges) * 100