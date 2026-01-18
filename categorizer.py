"""
Categorize problems into Beginner, Intermediate, or Advanced based on:
1. Technology stack complexity
2. Keywords in title/description
3. Problem characteristics
"""

from typing import Dict, List
import re

# Technology difficulty mapping
TECH_DIFFICULTY = {
    # Beginner
    'html': 'Beginner', 'css': 'Beginner', 'javascript': 'Beginner',
    'python': 'Beginner', 'sql': 'Beginner', 'bash': 'Beginner',
    'basic': 'Beginner', 'simple': 'Beginner', 'js': 'Beginner',
    
    # Intermediate
    'react': 'Intermediate', 'vue': 'Intermediate', 'angular': 'Intermediate',
    'node': 'Intermediate', 'express': 'Intermediate', 'django': 'Intermediate',
    'flask': 'Intermediate', 'rest': 'Intermediate', 'api': 'Intermediate',
    'database': 'Intermediate', 'docker': 'Intermediate', 'kubernetes': 'Intermediate',
    'aws': 'Intermediate', 'gcp': 'Intermediate', 'azure': 'Intermediate',
    'java': 'Intermediate', 'c#': 'Intermediate', 'csharp': 'Intermediate',
    'golang': 'Intermediate', 'go': 'Intermediate', 'ruby': 'Intermediate',
    'php': 'Intermediate', 'laravel': 'Intermediate', 'symfony': 'Intermediate',
    'postgres': 'Intermediate', 'mongodb': 'Intermediate', 'redis': 'Intermediate',
    'git': 'Intermediate', 'cicd': 'Intermediate', 'jenkins': 'Intermediate',
    
    # Advanced
    'machine learning': 'Advanced', 'ml': 'Advanced', 'ai': 'Advanced',
    'tensorflow': 'Advanced', 'pytorch': 'Advanced', 'keras': 'Advanced',
    'nlp': 'Advanced', 'computer vision': 'Advanced', 'deep learning': 'Advanced',
    'microservices': 'Advanced', 'distributed': 'Advanced', 'concurrent': 'Advanced',
    'blockchain': 'Advanced', 'cryptography': 'Advanced', 'security': 'Advanced',
    'performance': 'Advanced', 'optimization': 'Advanced', 'scaling': 'Advanced',
    'architecture': 'Advanced', 'system design': 'Advanced', 'devops': 'Advanced',
    'kubernetes': 'Advanced', 'terraform': 'Advanced', 'serverless': 'Advanced',
    'rust': 'Advanced', 'c++': 'Advanced', 'cpp': 'Advanced', 'embedded': 'Advanced',
    'quantum': 'Advanced', 'gpu': 'Advanced', 'cuda': 'Advanced',
}

# Keyword difficulty modifiers
DIFFICULTY_KEYWORDS = {
    'Advanced': [
        'complex', 'advanced', 'sophisticated', 'scalable', 'high-performance',
        'distributed', 'optimization', 'architecture', 'real-time', 'algorithm',
        'ai', 'ml', 'neural', 'blockchain', 'cryptocurrency', 'security',
        'production', 'enterprise', 'large-scale', 'billions', 'millions',
        'system design', 'refactor', 'bottleneck', 'parallel', 'concurrent',
    ],
    'Intermediate': [
        'intermediate', 'moderate', 'enhance', 'improve', 'feature', 'integration',
        'api', 'database', 'authentication', 'authorization', 'workflow',
        'deployment', 'testing', 'debugging', 'monitoring', 'logging',
    ],
    'Beginner': [
        'beginner', 'simple', 'basic', 'easy', 'help', 'how to', 'learn',
        'understand', 'start', 'getting started', 'tutorial', 'example',
        'first', 'newbie', 'struggling', 'stuck', 'issue', 'bug',
    ],
}


def categorize_problem(title: str, description: str, suggested_tech: str = "") -> str:
    """
    Categorize a problem into Beginner, Intermediate, or Advanced.
    
    Args:
        title: Problem title
        description: Problem description
        suggested_tech: Comma-separated technology tags
    
    Returns:
        Difficulty level: "Beginner", "Intermediate", or "Advanced"
    """
    combined_text = f"{title} {description} {suggested_tech}".lower()
    
    # Track difficulty scores
    scores = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0}
    
    # Check technology stack
    if suggested_tech:
        tech_list = [t.strip().lower() for t in suggested_tech.split(',')]
        for tech in tech_list:
            for tech_key, difficulty in TECH_DIFFICULTY.items():
                if tech_key in tech:
                    scores[difficulty] += 2
                    break
    
    # Check keywords in text
    for difficulty, keywords in DIFFICULTY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in combined_text:
                scores[difficulty] += 1
    
    # Special cases - boost Advanced if certain patterns exist
    advanced_patterns = [
        r'\b(ml|ai|machine\s+learning|deep\s+learning)\b',
        r'\b(distributed|microservices|kubernetes)\b',
        r'\b(billion|million|scale|performance|optimization)\b',
        r'\b(algorithm|complexity|architecture)\b',
    ]
    for pattern in advanced_patterns:
        if re.search(pattern, combined_text):
            scores['Advanced'] += 3
    
    # Special cases - boost Beginner if certain patterns exist
    beginner_patterns = [
        r'\b(how\s+to|help|struggling|first\s+time|newbie)\b',
        r'\b(error|issue|bug|doesn\'t\s+work)\b',
    ]
    for pattern in beginner_patterns:
        if re.search(pattern, combined_text):
            scores['Beginner'] += 2
    
    # Determine difficulty based on highest score
    max_score = max(scores.values())
    if max_score == 0:
        # Default to Intermediate if no clear indicators
        return 'Intermediate'
    
    # Get difficulty with highest score
    for difficulty, score in scores.items():
        if score == max_score:
            return difficulty
    
    return 'Intermediate'


def categorize_and_save_problems(db_session, problems: List[Dict]) -> List[Dict]:
    """
    Categorize a list of problems and update their difficulty level.
    """
    from models import Problem
    
    for problem_data in problems:
        if isinstance(problem_data, Problem):
            title = problem_data.title
            description = problem_data.description or ""
            tech = problem_data.suggested_tech or ""
        else:
            title = problem_data.get('title', '')
            description = problem_data.get('description', '')
            tech = problem_data.get('suggested_tech', '')
        
        difficulty = categorize_problem(title, description, tech)
        
        if isinstance(problem_data, Problem):
            problem_data.difficulty = difficulty
        else:
            problem_data['difficulty'] = difficulty
    
    return problems


if __name__ == "__main__":
    # Test the categorizer
    test_cases = [
        ("How to center a div with CSS?", "I'm struggling with CSS centering", "HTML, CSS"),
        ("Build a React todo app", "Create a simple todo application", "React, JavaScript"),
        ("Implement distributed caching system", "Design a high-performance cache across multiple servers", "Python, Redis, Kubernetes"),
        ("Machine learning model optimization", "Optimize neural network performance for billions of records", "Python, TensorFlow, AI"),
    ]
    
    for title, desc, tech in test_cases:
        difficulty = categorize_problem(title, desc, tech)
        print(f"Title: {title}")
        print(f"Difficulty: {difficulty}\n")
