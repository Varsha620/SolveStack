#!/usr/bin/env python3
"""
Recategorize all existing problems in the database using the new smart categorizer.
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://solvestack:solvestack123@localhost:5432/solvestack_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

from models import Problem
from categorizer import categorize_problem

def recategorize_all():
    """Recategorize all problems in the database."""
    
    try:
        # Get all problems
        problems = session.query(Problem).all()
        print(f"Found {len(problems)} problems to recategorize\n")
        
        # Track results
        stats = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0}
        changes = 0
        
        for i, problem in enumerate(problems, 1):
            old_difficulty = problem.difficulty
            
            # Categorize using new system
            new_difficulty = categorize_problem(
                problem.title,
                problem.description or "",
                problem.suggested_tech or ""
            )
            
            # Update if changed
            if new_difficulty != old_difficulty:
                problem.difficulty = new_difficulty
                changes += 1
                print(f"{i}. '{problem.title[:50]}...'")
                print(f"   {old_difficulty} → {new_difficulty} (Tech: {problem.suggested_tech or 'N/A'})")
            else:
                if i % 5 == 0:
                    print(f"{i}. [{new_difficulty}] {problem.title[:50]}...")
            
            stats[new_difficulty] += 1
        
        # Commit changes
        session.commit()
        
        print(f"\n{'='*60}")
        print("RECATEGORIZATION COMPLETE")
        print(f"{'='*60}")
        print(f"Total problems: {len(problems)}")
        print(f"Changes made: {changes}")
        print(f"\nNew Distribution:")
        print(f"  Beginner: {stats['Beginner']} ({stats['Beginner']*100//len(problems)}%)")
        print(f"  Intermediate: {stats['Intermediate']} ({stats['Intermediate']*100//len(problems)}%)")
        print(f"  Advanced: {stats['Advanced']} ({stats['Advanced']*100//len(problems)}%)")
        
    except Exception as e:
        session.rollback()
        print(f"Error during recategorization: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    recategorize_all()
