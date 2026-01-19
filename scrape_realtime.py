#!/usr/bin/env python3
"""
Real-time scraper runner with live progress display and difficulty categorization.
Fetches actual problems from Reddit, GitHub, StackOverflow, and HackerNews.
"""

import sys
import time
sys.path.insert(0, '/workspaces/SolveStack')

from database import SessionLocal
from models import Problem
from categorizer import categorize_problem

# Import all scrapers
from scrapers.reddit_scraper import scrape_reddit
from scrapers.github_scraper import scrape_github
from scrapers.stackoverflow_scraper import scrape_stackoverflow
from scrapers.hackernews_scraper import scrape_hackernews

def print_banner(text):
    """Print a formatted banner"""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def print_status(message, status='info'):
    """Print status message with emoji"""
    emojis = {
        'info': 'ℹ️ ',
        'success': '✅',
        'error': '❌',
        'loading': '⏳',
        'added': '✓',
        'skip': '⊘'
    }
    print(f"{emojis.get(status, '→')} {message}")

def run_scrapers(limit_per_source=25):
    """Run all scrapers with real-time progress display"""
    
    print_banner("🚀 REAL-TIME PROBLEM SCRAPER")
    
    db = SessionLocal()
    all_problems = []
    scraper_results = {}
    
    try:
        # Get initial count
        initial_count = db.query(Problem).count()
        print_status(f"Database currently has {initial_count} problems", 'info')
        
        # REDDIT
        print_banner("📱 SCRAPING REDDIT")
        try:
            print_status(f"Fetching up to {limit_per_source} problems from Reddit...", 'loading')
            reddit_problems = scrape_reddit(limit=limit_per_source)
            print_status(f"Retrieved {len(reddit_problems)} problems from Reddit", 'success')
            all_problems.extend(reddit_problems)
            scraper_results['reddit'] = len(reddit_problems)
            
            # Show sample
            if reddit_problems:
                print("\n  Sample problems:")
                for p in reddit_problems[:3]:
                    print(f"    • {p.get('title', '')[:70]}")
        except Exception as e:
            print_status(f"Reddit scraping failed: {str(e)[:100]}", 'error')
            scraper_results['reddit'] = 0
        
        # GITHUB
        print_banner("🐙 SCRAPING GITHUB")
        try:
            print_status(f"Fetching up to {limit_per_source} problems from GitHub...", 'loading')
            github_problems = scrape_github(limit=limit_per_source)
            print_status(f"Retrieved {len(github_problems)} problems from GitHub", 'success')
            all_problems.extend(github_problems)
            scraper_results['github'] = len(github_problems)
            
            # Show sample
            if github_problems:
                print("\n  Sample problems:")
                for p in github_problems[:3]:
                    print(f"    • {p.get('title', '')[:70]}")
        except Exception as e:
            print_status(f"GitHub scraping failed: {str(e)[:100]}", 'error')
            scraper_results['github'] = 0
        
        # STACKOVERFLOW
        print_banner("📚 SCRAPING STACKOVERFLOW")
        try:
            print_status(f"Fetching up to {limit_per_source} problems from Stack Overflow...", 'loading')
            so_problems = scrape_stackoverflow(limit=limit_per_source)
            print_status(f"Retrieved {len(so_problems)} problems from Stack Overflow", 'success')
            all_problems.extend(so_problems)
            scraper_results['stackoverflow'] = len(so_problems)
            
            # Show sample
            if so_problems:
                print("\n  Sample problems:")
                for p in so_problems[:3]:
                    print(f"    • {p.get('title', '')[:70]}")
        except Exception as e:
            print_status(f"Stack Overflow scraping failed: {str(e)[:100]}", 'error')
            scraper_results['stackoverflow'] = 0
        
        # HACKERNEWS
        print_banner("📰 SCRAPING HACKERNEWS")
        try:
            print_status(f"Fetching up to {limit_per_source} problems from HackerNews...", 'loading')
            hn_problems = scrape_hackernews(limit=limit_per_source)
            print_status(f"Retrieved {len(hn_problems)} problems from HackerNews", 'success')
            all_problems.extend(hn_problems)
            scraper_results['hackernews'] = len(hn_problems)
            
            # Show sample
            if hn_problems:
                print("\n  Sample problems:")
                for p in hn_problems[:3]:
                    print(f"    • {p.get('title', '')[:70]}")
        except Exception as e:
            print_status(f"HackerNews scraping failed: {str(e)[:100]}", 'error')
            scraper_results['hackernews'] = 0
        
        # DATABASE INSERTION WITH CATEGORIZATION
        print_banner(f"💾 ADDING {len(all_problems)} PROBLEMS TO DATABASE")
        
        added_count = 0
        skipped_count = 0
        error_count = 0
        
        for idx, problem_data in enumerate(all_problems, 1):
            try:
                # Check if problem already exists (by reference_link)
                reference_link = problem_data.get('reference_link', f"unknown_{idx}")
                existing = db.query(Problem).filter(
                    Problem.reference_link == reference_link
                ).first()
                
                if existing:
                    print_status(f"[{idx}/{len(all_problems)}] Skipping (duplicate): {problem_data.get('title', '')[:60]}...", 'skip')
                    skipped_count += 1
                else:
                    # Categorize difficulty using smart system
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
                        reference_link=reference_link,
                        tags=problem_data.get('tags', []),
                        source_id=problem_data.get('source_id', ''),
                        difficulty=difficulty,
                    )
                    db.add(problem)
                    added_count += 1
                    print_status(f"[{idx}/{len(all_problems)}] Added [{difficulty:12}]: {problem_data.get('title', '')[:50]}...", 'added')
                    
            except Exception as e:
                error_count += 1
                print_status(f"[{idx}/{len(all_problems)}] Error: {str(e)[:60]}...", 'error')
        
        # Commit all changes
        db.commit()
        
        # RESULTS SUMMARY
        print_banner("📊 SCRAPING COMPLETE - RESULTS SUMMARY")
        
        print("\n🔄 Scraper Results:")
        for source, count in scraper_results.items():
            print(f"  {source.upper():20} : {count:3} problems")
        
        total_retrieved = sum(scraper_results.values())
        print(f"  {'TOTAL RETRIEVED':20} : {total_retrieved:3} problems")
        
        print(f"\n💾 Database Operations:")
        print(f"  Added:    {added_count:3} new problems")
        print(f"  Skipped:  {skipped_count:3} duplicates")
        print(f"  Errors:   {error_count:3} failed")
        
        # Get final statistics
        final_count = db.query(Problem).count()
        beginner = db.query(Problem).filter(Problem.difficulty == 'Beginner').count()
        intermediate = db.query(Problem).filter(Problem.difficulty == 'Intermediate').count()
        advanced = db.query(Problem).filter(Problem.difficulty == 'Advanced').count()
        
        print(f"\n📈 Database Statistics:")
        print(f"  Total problems:     {final_count:3} (was {initial_count}, +{added_count})")
        print(f"  Beginner:           {beginner:3} ({beginner*100//max(final_count,1)}%)")
        print(f"  Intermediate:       {intermediate:3} ({intermediate*100//max(final_count,1)}%)")
        print(f"  Advanced:           {advanced:3} ({advanced*100//max(final_count,1)}%)")
        
        print(f"\n{'='*80}")
        print("✅ SCRAPING PIPELINE COMPLETE!")
        print(f"{'='*80}\n")
        
        return {
            'success': True,
            'added': added_count,
            'skipped': skipped_count,
            'errors': error_count,
            'total_in_db': final_count,
            'by_difficulty': {
                'Beginner': beginner,
                'Intermediate': intermediate,
                'Advanced': advanced
            }
        }
        
    except Exception as e:
        print_status(f"Critical error: {str(e)}", 'error')
        db.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run real-time problem scrapers")
    parser.add_argument('--limit', type=int, default=25, help='Limit per source (default: 25)')
    args = parser.parse_args()
    
    result = run_scrapers(limit_per_source=args.limit)
    sys.exit(0 if result.get('success') else 1)
