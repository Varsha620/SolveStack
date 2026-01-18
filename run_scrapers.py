#!/usr/bin/env python3
"""
Run all scrapers and populate the database with real problems.
Also categorizes problems by difficulty.
"""

import sys
sys.path.insert(0, '/workspaces/SolveStack')

from database import SessionLocal
from models import Problem
from categorizer import categorize_problem

# Import all scrapers
from scrapers.reddit_scraper import scrape_reddit
from scrapers.github_scraper import scrape_github
from scrapers.stackoverflow_scraper import scrape_stackoverflow
from scrapers.hackernews_scraper import scrape_hackernews

db = SessionLocal()

try:
    print("🔄 Starting to scrape problems from all sources...")
    
    # Clear existing problems (optional - comment out to keep them)
    # db.query(Problem).delete()
    # db.commit()
    # print("✓ Cleared existing problems")
    
    all_problems = []
    
    # Reddit
    print("\n📱 Scraping Reddit...")
    try:
        reddit_problems = scrape_reddit(limit=20)
        print(f"✓ Got {len(reddit_problems)} problems from Reddit")
        all_problems.extend(reddit_problems)
    except Exception as e:
        print(f"✗ Reddit scraping failed: {e}")
    
    # GitHub
    print("\n🐙 Scraping GitHub...")
    try:
        github_problems = scrape_github(limit=20)
        print(f"✓ Got {len(github_problems)} problems from GitHub")
        all_problems.extend(github_problems)
    except Exception as e:
        print(f"✗ GitHub scraping failed: {e}")
    
    # Stack Overflow
    print("\n📚 Scraping Stack Overflow...")
    try:
        so_problems = scrape_stackoverflow(limit=20)
        print(f"✓ Got {len(so_problems)} problems from Stack Overflow")
        all_problems.extend(so_problems)
    except Exception as e:
        print(f"✗ Stack Overflow scraping failed: {e}")
    
    # HackerNews
    print("\n📰 Scraping HackerNews...")
    try:
        hn_problems = scrape_hackernews(limit=20)
        print(f"✓ Got {len(hn_problems)} problems from HackerNews")
        all_problems.extend(hn_problems)
    except Exception as e:
        print(f"✗ HackerNews scraping failed: {e}")
    
    # Add problems to database with difficulty categorization
    print(f"\n💾 Adding {len(all_problems)} problems to database with difficulty categorization...")
    added_count = 0
    for problem_data in all_problems:
        try:
            # Check if problem already exists (by reference_link)
            existing = db.query(Problem).filter(
                Problem.reference_link == problem_data.get('reference_link')
            ).first()
            
            if not existing:
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
                    date=problem_data.get('date', ''),
                    suggested_tech=problem_data.get('suggested_tech', ''),
                    author_name=problem_data.get('author_name', 'Anonymous'),
                    author_id=problem_data.get('author_id', ''),
                    reference_link=problem_data.get('reference_link', f"unknown_{added_count}"),
                    tags=problem_data.get('tags', []),
                    source_id=problem_data.get('source_id', ''),
                    difficulty=difficulty,
                )
                db.add(problem)
                added_count += 1
                print(f"  ✓ Added: {problem_data.get('title', '')[:60]}... [{difficulty}]")
        except Exception as e:
            print(f"  ✗ Error adding problem: {e}")
    
    db.commit()
    print(f"\n✅ Successfully added {added_count} new problems to database!")
    print("\n📊 Problem statistics:")
    
    total = db.query(Problem).count()
    beginner = db.query(Problem).filter(Problem.difficulty == 'Beginner').count()
    intermediate = db.query(Problem).filter(Problem.difficulty == 'Intermediate').count()
    advanced = db.query(Problem).filter(Problem.difficulty == 'Advanced').count()
    
    print(f"  Total problems: {total}")
    print(f"  Beginner: {beginner}")
    print(f"  Intermediate: {intermediate}")
    print(f"  Advanced: {advanced}")
    
finally:
    db.close()
