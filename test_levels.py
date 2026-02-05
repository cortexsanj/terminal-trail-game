#!/usr/bin/env python3
"""
Test script for level system
"""

from level_config import (
    LEVELS,
    get_level_for_challenge,
    get_level_info,
    get_challenge_position_in_level,
    get_level_progress
)

def test_level_system():
    """Test the level system implementation"""
    
    print("=" * 60)
    print("Testing Terminal Trail Level System")
    print("=" * 60)
    print()
    
    # Test 1: Display all levels
    print("📚 All Levels:")
    print("-" * 60)
    for level_num, level_data in LEVELS.items():
        print(f"{level_data['emoji']} Level {level_num}: {level_data['name']}")
        print(f"   Description: {level_data['description']}")
        print(f"   Commands: {', '.join(level_data['commands'])}")
        print(f"   Challenges: {level_data['challenges'][0]}-{level_data['challenges'][-1]} ({len(level_data['challenges'])} total)")
        print()
    
    # Test 2: Test specific challenges
    print("🎮 Testing Specific Challenges:")
    print("-" * 60)
    test_challenges = [1, 7, 16, 23, 31, 41, 51, 63]
    
    for challenge_num in test_challenges:
        level_num = get_level_for_challenge(challenge_num)
        level_info = get_level_info(level_num)
        position, total = get_challenge_position_in_level(challenge_num)[1:]
        progress = get_level_progress(challenge_num)
        
        print(f"Challenge {challenge_num}:")
        print(f"  {level_info['emoji']} Level {level_num}: {level_info['name']}")
        print(f"  Position: {position}/{total} ({progress['progress_percent']}% of level)")
        print()
    
    # Test 3: Verify all challenges are mapped
    print("✅ Verification:")
    print("-" * 60)
    all_challenges = set()
    for level_data in LEVELS.values():
        all_challenges.update(level_data['challenges'])
    
    expected_challenges = set(range(1, 64))
    missing = expected_challenges - all_challenges
    extra = all_challenges - expected_challenges
    
    if missing:
        print(f"❌ Missing challenges: {sorted(missing)}")
    if extra:
        print(f"❌ Extra challenges: {sorted(extra)}")
    if not missing and not extra:
        print(f"✅ All 63 challenges correctly mapped to levels")
        print(f"✅ Total levels: {len(LEVELS)}")
        print(f"✅ Challenge distribution:")
        for level_num, level_data in LEVELS.items():
            print(f"   Level {level_num}: {len(level_data['challenges'])} challenges")
    
    print()
    print("=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_level_system()
