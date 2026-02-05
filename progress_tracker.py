"""
Progress Tracker
Handles saving and loading game progress
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from level_config import get_level_for_challenge, get_level_progress


class ProgressTracker:
    """Tracks and persists game progress"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.progress_file = self.base_dir / "progress.json"
        self.debug = False  # Add debug flag
    
    def save_progress(self, challenge: int, step: int):
        """Save current progress"""
        level_info = get_level_progress(challenge)
        
        progress_data = {
            "challenge": challenge,
            "step": step,
            "level": level_info["level_num"],
            "level_name": level_info["level_name"],
            "completed_challenges": self._get_completed_challenges(challenge, step),
            "applied_modifications": self._get_applied_modifications(challenge, step)
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
    
    def _get_applied_modifications(self, current_challenge: int, current_step: int) -> list:
        """Get list of all modifications that should be applied up to current progress"""
        import json
        from pathlib import Path
        
        modifications = []
        challenges_dir = self.base_dir / "challenges"
        
        # Go through all completed challenges and current challenge up to current step
        for challenge_num in range(1, current_challenge + 1):
            challenge_file = challenges_dir / f"challenge_{challenge_num:02d}.json"
            
            if not challenge_file.exists():
                continue
            
            try:
                with open(challenge_file, 'r') as f:
                    challenge_data = json.load(f)
                
                steps = challenge_data.get('steps', [])
                
                # For completed challenges, include all steps
                # For current challenge, only include completed steps
                max_step = len(steps) if challenge_num < current_challenge else current_step
                
                for step_num in range(1, max_step + 1):
                    if step_num <= len(steps):
                        step_data = steps[step_num - 1]
                        step_mods = step_data.get('modifications', [])
                        if step_mods:
                            # Add challenge and step info for tracking
                            for mod in step_mods:
                                mod_with_info = mod.copy()
                                mod_with_info['_challenge'] = challenge_num
                                mod_with_info['_step'] = step_num
                                modifications.append(mod_with_info)
            
            except Exception as e:
                if self.debug:
                    print(f"Warning: Could not load modifications from challenge {challenge_num}: {e}")
        
        return modifications
    
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