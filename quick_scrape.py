#!/usr/bin/env python3
"""
Quick scraper - tries to get real data, falls back to seed if needed
"""
import sys
sys.path.insert(0, '/workspaces/SolveStack')

from database import SessionLocal
from models import Problem
import json

db = SessionLocal()

# First check if we already have problems
existing = db.query(Problem).count()
print(f"📊 Database currently has {existing} problems")

# If we have none, seed with sample data
if existing == 0:
    print("\n📝 Loading seed data...")
    try:
        with open('/workspaces/SolveStack/problems.json', 'r') as f:
            problems_data = json.load(f)
        
        from categorizer import categorize_problem
        
        for idx, p in enumerate(problems_data[:20], 1):
            # Categorize
            difficulty = categorize_problem(
                p.get('title', ''),
                p.get('description', ''),
                p.get('suggested_tech', '')
            )
            
            problem = Problem(
                title=p.get('title', 'Untitled'),
                description=p.get('description', ''),
                suggested_tech=p.get('suggested_tech', ''),
                difficulty=difficulty,
                estimated_effort=p.get('estimated_effort', '1-3 days'),
                source=p.get('source', 'seed'),
                url=p.get('url', ''),
                problem_type=p.get('problem_type', 'general')
            )
            db.add(problem)
            print(f"  ✅ [{idx}] {p.get('title', 'Untitled')[:50]}... ({difficulty})")
        
        db.commit()
        print(f"\n✅ Seeded {idx} problems with difficulty categorization")
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"\n✅ Database already populated with {existing} problems")

# Show what we have
print("\n📊 FINAL DATABASE STATE:")
problems = db.query(Problem).all()
print(f"Total: {len(problems)}")

difficulties = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0}
for p in problems:
    diff = p.difficulty or 'Intermediate'
    difficulties[diff] += 1

print(f"🟢 Beginner: {difficulties['Beginner']}")
print(f"🟡 Intermediate: {difficulties['Intermediate']}")
print(f"🔴 Advanced: {difficulties['Advanced']}")

# Show sample
print("\n📋 Sample problems:")
for i, p in enumerate(problems[:3], 1):
    print(f"  {i}. {p.title[:60]}... [{p.difficulty}]")

db.close()
