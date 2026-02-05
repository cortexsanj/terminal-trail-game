"""
Level Configuration for Terminal Trail
Maps challenges to levels (game-like structure)
"""

LEVELS = {
    1: {
        "name": "First Steps",
        "description": "Basic navigation and examining objects",
        "commands": ["ls", "cat", "cd"],
        "challenges": list(range(1, 7)),  # Challenges 1-6
        "emoji": "🌱"
    },
    2: {
        "name": "Navigation Mastery",
        "description": "Multi-level navigation and understanding paths",
        "commands": ["pwd", "cd"],
        "challenges": list(range(7, 16)),  # Challenges 7-15
        "emoji": "🗺️"
    },
    3: {
        "name": "Hidden Things",
        "description": "Discovering hidden files and directories",
        "commands": ["ls -a"],
        "challenges": list(range(16, 23)),  # Challenges 16-22
        "emoji": "🔍"
    },
    4: {
        "name": "Moving Things",
        "description": "Moving files and directories around",
        "commands": ["mv"],
        "challenges": list(range(23, 31)),  # Challenges 23-30
        "emoji": "📦"
    },
    5: {
        "name": "Speaking Up",
        "description": "Using echo for output and conversation",
        "commands": ["echo"],
        "challenges": list(range(31, 41)),  # Challenges 31-40
        "emoji": "💬"
    },
    6: {
        "name": "Advanced Exploration",
        "description": "Combining all learned commands",
        "commands": ["all"],
        "challenges": list(range(41, 51)),  # Challenges 41-50
        "emoji": "🎯"
    },
    7: {
        "name": "The Power to Remove",
        "description": "Using rm and understanding permissions",
        "commands": ["rm", "chmod"],
        "challenges": list(range(51, 64)),  # Challenges 51-63
        "emoji": "⚔️"
    }
}


def get_level_for_challenge(challenge_num: int) -> int:
    """Get the level number for a given challenge"""
    for level_num, level_data in LEVELS.items():
        if challenge_num in level_data["challenges"]:
            return level_num
    return 1  # Default to level 1


def get_level_info(level_num: int) -> dict:
    """Get information about a specific level"""
    return LEVELS.get(level_num, LEVELS[1])


def get_challenge_position_in_level(challenge_num: int) -> tuple:
    """
    Get the position of a challenge within its level
    Returns: (level_num, position_in_level, total_in_level)
    """
    level_num = get_level_for_challenge(challenge_num)
    level_info = get_level_info(level_num)
    challenges = level_info["challenges"]
    
    position = challenges.index(challenge_num) + 1 if challenge_num in challenges else 1
    total = len(challenges)
    
    return (level_num, position, total)


def get_level_progress(current_challenge: int) -> dict:
    """
    Get progress information for the current level
    Returns dict with level info and progress
    """
    level_num, position, total = get_challenge_position_in_level(current_challenge)
    level_info = get_level_info(level_num)
    
    return {
        "level_num": level_num,
        "level_name": level_info["name"],
        "level_emoji": level_info["emoji"],
        "level_description": level_info["description"],
        "challenge_position": position,
        "total_challenges": total,
        "progress_percent": int((position / total) * 100)
    }
