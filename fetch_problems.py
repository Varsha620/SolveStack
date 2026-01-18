#!/usr/bin/env python3
"""
Fetch real scraped problems and populate database.
Simpler approach - get problems from each scraper and add them.
"""

import sys
sys.path.insert(0, '/workspaces/SolveStack')

from database import SessionLocal
from models import Problem
from categorizer import categorize_problem
from datetime import datetime

# Import scrapers
from scrapers.reddit_scraper import scrape_reddit
from scrapers.github_scraper import scrape_github

db = SessionLocal()

try:
    print("🔄 Fetching real problems from platforms...\n")
    
    all_problems = []
    
    # GitHub - more reliable
    print("📡 Fetching from GitHub...")
    try:
        github_problems = scrape_github(limit=15)
        print(f"✅ Got {len(github_problems)} problems from GitHub\n")
        all_problems.extend(github_problems)
    except Exception as e:
        print(f"⚠️  GitHub: {str(e)[:100]}\n")
    
    # Reddit - if it works
    print("📡 Fetching from Reddit...")
    try:
        reddit_problems = scrape_reddit(limit=10)
        print(f"✅ Got {len(reddit_problems)} problems from Reddit\n")
        all_problems.extend(reddit_problems)
    except Exception as e:
        print(f"⚠️  Reddit: {str(e)[:100]}\n")
    
    if not all_problems:
        print("❌ No problems fetched from any platform")
        print("Using seed data instead...")
        import json
        with open('/workspaces/SolveStack/problems.json', 'r') as f:
            seed_data = json.load(f)
        all_problems = seed_data[:20]
    
    # Clear existing and add new problems
    print(f"\n💾 Adding {len(all_problems)} problems to database...\n")
    db.query(Problem).delete()
    db.commit()
    
    added = 0
    for problem_data in all_problems:
        try:
            # Categorize difficulty
            title = problem_data.get('title', 'Untitled')
            desc = problem_data.get('description', '')
            tech = problem_data.get('suggested_tech', '')
            difficulty = categorize_problem(title, desc, tech)
            
            problem = Problem(
                title=title,
                description=desc,
                source=problem_data.get('source', 'Unknown'),
                suggested_tech=tech,
                reference_link=problem_data.get('reference_link', f'unknown_{added}'),
                author_name=problem_data.get('author_name', 'Anonymous'),
                author_id=problem_data.get('author_id'),
                tags=problem_data.get('tags', []),
                date=problem_data.get('date', datetime.utcnow().isoformat()),
                scraped_at=datetime.utcnow(),
                difficulty=difficulty,
            )
            db.add(problem)
            added += 1
            print(f"  ✅ {title[:60]}... [{difficulty}]")
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)[:80]}")
    
    db.commit()
    print(f"\n✨ Successfully added {added} problems!\n")
    
    # Stats
    total = db.query(Problem).count()
    beginner = db.query(Problem).filter(Problem.difficulty == 'Beginner').count()
    intermediate = db.query(Problem).filter(Problem.difficulty == 'Intermediate').count()
    advanced = db.query(Problem).filter(Problem.difficulty == 'Advanced').count()
    
    print("📊 Database Statistics:")
    print(f"  Total: {total}")
    print(f"  🟢 Beginner: {beginner}")
    print(f"  🟡 Intermediate: {intermediate}")
    print(f"  🔴 Advanced: {advanced}")
    print("\n✅ Ready! Refresh your browser to see the problems.\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
