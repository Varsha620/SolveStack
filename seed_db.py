#!/usr/bin/env python3
"""Quick script to populate database with sample problems"""

import json
import sys
from datetime import datetime
sys.path.insert(0, '/workspaces/SolveStack')

from database import SessionLocal
from models import Problem
from categorizer import categorize_problem

# Load problems from JSON
with open('/workspaces/SolveStack/problems.json', 'r') as f:
    problems_data = json.load(f)

db = SessionLocal()

try:
    # Clear existing problems
    db.query(Problem).delete()
    db.commit()
    print(f"✅ Cleared existing problems")
    
    # Add new problems with difficulty categorization
    added = 0
    for problem_data in problems_data[:30]:  # Add first 30 problems
        # Categorize difficulty
        difficulty = categorize_problem(
            problem_data.get('title', ''),
            problem_data.get('description', ''),
            problem_data.get('suggested_tech', '')
        )
        
        problem = Problem(
            title=problem_data.get('title', 'Untitled'),
            description=problem_data.get('description', ''),
            source=problem_data.get('source', 'Unknown'),
            suggested_tech=problem_data.get('suggested_tech', 'General'),
            reference_link=problem_data.get('reference_link', f'unknown_{added}'),
            author_name=problem_data.get('author_name', 'Anonymous'),
            author_id=problem_data.get('author_id'),
            tags=problem_data.get('tags', []),
            date=problem_data.get('date', datetime.utcnow().isoformat()),
            scraped_at=datetime.utcnow(),
            difficulty=difficulty,  # Set difficulty
        )
        db.add(problem)
        added += 1
    
    db.commit()
    print(f"✅ Added {added} sample problems with difficulty categorization")
    
    # Display statistics
    total = db.query(Problem).count()
    beginner = db.query(Problem).filter(Problem.difficulty == 'Beginner').count()
    intermediate = db.query(Problem).filter(Problem.difficulty == 'Intermediate').count()
    advanced = db.query(Problem).filter(Problem.difficulty == 'Advanced').count()
    
    print(f"\n📊 Problem Statistics:")
    print(f"  Total: {total}")
    print(f"  🟢 Beginner: {beginner}")
    print(f"  🟡 Intermediate: {intermediate}")
    print(f"  🔴 Advanced: {advanced}")
    
finally:
    db.close()

