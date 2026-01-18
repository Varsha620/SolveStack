"""
Smart Problem Difficulty Categorizer

Uses multi-dimensional analysis to classify problems into:
- Beginner: Foundational concepts, simple implementations
- Intermediate: Professional frameworks, real-world integrations
- Advanced: System-level problems, architectural challenges

Dimensions analyzed:
1. Technology Stack Complexity (0-30 points)
2. Problem Scope & Scale (0-25 points)  
3. Semantic Complexity Keywords (0-25 points)
4. Effort Estimation Markers (0-20 points)
"""

from typing import Dict, List, Tuple
import re

# ============ DIMENSION 1: Technology Stack Complexity ============

TECH_COMPLEXITY_SCORES = {
    # Beginner (1-2 points each)
    'html': 1, 'css': 1, 'markdown': 1, 'xml': 1, 'json': 1,
    'javascript': 2, 'js': 2, 'python': 2, 'sql': 2, 'bash': 2, 'shell': 2,
    'c': 2, 'java': 2, 'typescript': 2,
    
    # Intermediate (3-5 points each)
    'react': 4, 'vue': 4, 'angular': 4, 'svelte': 4,
    'node': 4, 'nodejs': 4, 'express': 4, 'fastapi': 4,
    'django': 4, 'flask': 3, 'spring': 4, 'rails': 4,
    'rest': 3, 'graphql': 4, 'api': 3, 'http': 2,
    'postgresql': 3, 'mysql': 3, 'mongodb': 4, 'redis': 4,
    'docker': 4, 'compose': 3, 'git': 2, 'github': 2,
    'aws': 4, 'gcp': 4, 'azure': 4, 'firebase': 3,
    'java': 3, 'kotlin': 3, 'go': 4, 'golang': 4,
    'ruby': 3, 'php': 3, 'laravel': 4, 'symfony': 4,
    
    # Advanced (6-10 points each)
    'kubernetes': 8, 'k8s': 8, 'microservices': 7, 'serverless': 6,
    'tensorflow': 9, 'pytorch': 9, 'keras': 8,
    'machine learning': 9, 'ml': 9, 'ai': 8, 'deep learning': 9,
    'nlp': 9, 'computer vision': 9, 'cv': 8,
    'distributed': 8, 'spark': 8, 'hadoop': 8, 'mapreduce': 8,
    'blockchain': 8, 'ethereum': 8, 'solidity': 8, 'web3': 7,
    'cryptography': 9, 'encryption': 8, 'security': 7,
    'performance': 7, 'optimization': 7, 'bottleneck': 7,
    'architecture': 8, 'system design': 8, 'devops': 7,
    'terraform': 7, 'ansible': 6, 'jenkins': 5,
    'rust': 8, 'c++': 8, 'cpp': 8, 'embedded': 7,
    'quantum': 10, 'gpu': 7, 'cuda': 8, 'opencl': 8,
    'rtc': 7, 'websocket': 6, 'grpc': 7, 'protobuf': 6,
}

# ============ DIMENSION 2: Problem Scope & Scale Indicators ============

SCALE_MARKERS = {
    # Beginner scale (1 point each)
    'beginner': 1, 'simple': 1, 'basic': 1, 'easy': 1, 'small': 1,
    'single': 1, 'one': 1, 'individual': 1, 'standalone': 1,
    
    # Intermediate scale (2-3 points each)
    'moderate': 2, 'medium': 2, 'feature': 2, 'module': 2,
    'application': 3, 'app': 2, 'system': 3, 'service': 2,
    'multiple': 2, 'several': 2, 'handful': 1, 'couple': 1,
    
    # Advanced scale (3-5 points each)
    'large-scale': 5, 'enterprise': 4, 'production': 3,
    'complex': 4, 'sophisticated': 4, 'intricate': 4,
    'distributed': 5, 'scalable': 4, 'high-performance': 5,
    'billions': 5, 'millions': 4, 'thousands': 2,
    'concurrent': 4, 'parallel': 4, 'asynchronous': 3,
    'real-time': 4, 'low-latency': 4, 'streaming': 3,
}

# ============ DIMENSION 3: Semantic Complexity Keywords ============

SEMANTIC_COMPLEXITY = {
    'Advanced': {
        'machine learning': 5, 'neural network': 5, 'deep learning': 5, 'tensorflow': 5, 'pytorch': 5,
        'algorithm': 5, 'algorithmic': 5, 'optimization': 5, 'complexity': 4, 'performance': 4, 
        'bottleneck': 5, 'race condition': 5, 'deadlock': 4, 'memory leak': 5, 'garbage collection': 4,
        'concurrency': 4, 'threading': 4, 'async': 3, 'synchronization': 4,
        'refactoring': 3, 'architecture': 5, 'design pattern': 3,
        'integration': 3, 'migration': 4, 'legacy': 3,
        'monolith': 3, 'microservice': 4, 'service mesh': 5,
        'security': 4, 'vulnerability': 4, 'breach': 4, 'exploit': 4,
        'compliance': 3, 'scalability': 4, 'reliability': 3, 'distributed': 4,
    },
    'Intermediate': {
        'integration': 3, 'workflow': 2, 'pipeline': 2, 'deployment': 2,
        'testing': 2, 'debugging': 2, 'monitoring': 2, 'logging': 2,
        'caching': 2, 'indexing': 2, 'query': 2, 'aggregation': 2,
        'authentication': 2, 'authorization': 2, 'permission': 2,
        'validation': 1, 'serialization': 2, 'parsing': 2,
        'formatting': 1, 'encoding': 2, 'decoding': 2,
    },
    'Beginner': {
        'help': 1, 'tutorial': 1, 'example': 1, 'sample': 1,
        'learn': 1, 'understand': 1, 'how to': 2, 'getting started': 2,
        'first time': 2, 'newbie': 2, 'beginner': 2, 'beginner-friendly': 2,
        'struggling': 2, 'stuck': 2, 'doesn\'t work': 2, 'error': 1,
        'issue': 1, 'bug': 1, 'fix': 1, 'broken': 2,
    },
}

# ============ DIMENSION 4: Effort & Estimation Patterns ============

EFFORT_TIME_PATTERNS = {
    'advanced_effort': [
        (r'(\d+\s+)?(week|month|quarter|year)', 5),  # weeks+ → Advanced
        (r'long[- ]?term', 4), (r'extensive', 4), (r'comprehensive', 3),
        (r'from scratch', 3), (r'redesign', 3), (r'overhaul', 4),
        (r'billions?', 5), (r'millions?', 4), (r'scale', 4),
        (r'inference', 4), (r'latency', 4), (r'throughput', 4),
        (r'optimize', 3), (r'optimization', 4), (r'performance', 3),
    ],
    'intermediate_effort': [
        (r'(\d+\s+)?(day|afternoon|morning)', 2),  # days → Intermediate
        (r'medium[- ]?term', 2), (r'several', 2), (r'multiple iterations', 2),
        (r'integrate', 2), (r'connect', 1), (r'implement', 2),
    ],
    'beginner_effort': [
        (r'(\d+\s+)?(hour|minute)', 2),  # hours → Beginner
        (r'quick', 1), (r'simple', 1), (r'straightforward', 1),
        (r'getting started', 2), (r'basic', 1), (r'fundamental', 1),
    ],
}

# ============ BONUS FACTORS ============

BONUS_PATTERNS = {
    'research_required': (r'(research|investigate|explore|study|analyze)', 2),
    'open_ended': (r'(design|architecture|approach|strategy|framework)', 2),
    'multi_domain': (r'(\w+\s+and\s+\w+\s+and\s+\w+)', 2),  # 3+ "and" phrases
    'ambiguous': (r'(unclear|ambiguous|vague|not sure|figure out)', 1),
    'ml_bonus': (r'(machine learning|neural network|deep learning|tensorflow|pytorch)', 8),  # ML always complex
}

NEGATIVE_FACTORS = {
    'very_simple': (r'(trivial|one[- ]?liner|copy[- ]?paste)', -2),
    'typo_help': (r'(typo|syntax error|missing semicolon)', -2),
}


def score_technology_stack(suggested_tech: str) -> Tuple[int, List[str]]:
    """
    Score technology stack complexity (0-30 points).
    
    Returns: (score, reasons)
    """
    if not suggested_tech:
        return 5, ["No specific tech requirements"]
    
    score = 0
    reasons = []
    tech_list = [t.strip().lower() for t in suggested_tech.split(',')]
    
    # Score each technology - match longer keys first to avoid substring issues
    tech_scores = []
    matched = set()
    
    for tech in tech_list:
        # Sort by key length descending to match more specific terms first
        sorted_keys = sorted(TECH_COMPLEXITY_SCORES.items(), key=lambda x: len(x[0]), reverse=True)
        
        for tech_key, points in sorted_keys:
            if tech_key.lower() in tech and tech not in matched:
                tech_scores.append(points)
                matched.add(tech)
                if points >= 8:
                    reasons.append(f"Advanced tech: {tech.title()}")
                elif points >= 4:
                    reasons.append(f"Framework: {tech.title()}")
                break
    
    if tech_scores:
        # Weighted score: give priority to highest complexity tech, average with others
        score = max(tech_scores) + sum(tech_scores) // len(tech_scores)
    else:
        score = 3
        reasons.append("General tech stack")
    
    return min(score, 30), reasons


def score_problem_scope(title: str, description: str) -> Tuple[int, List[str]]:
    """
    Score problem scope & scale (0-25 points).
    
    Returns: (score, reasons)
    """
    combined_text = f"{title} {description}".lower()
    score = 0
    reasons = []
    
    # Scale indicators
    for marker, points in SCALE_MARKERS.items():
        if marker in combined_text:
            score += points
            if points >= 3:
                reasons.append(f"Scale: {marker.title()}")
    
    # Description length as proxy for complexity
    word_count = len(combined_text.split())
    if word_count > 500:
        score += 8
        reasons.append("Large problem scope (500+ words)")
    elif word_count > 200:
        score += 4
        reasons.append("Moderate scope (200+ words)")
    elif word_count > 100:
        score += 2
        reasons.append("Detailed scope (100+ words)")
    
    # Multiple stakeholders/systems
    if 'user' in combined_text and 'system' in combined_text:
        score += 3
        reasons.append("Multi-system integration")
    
    return min(score, 25), reasons


def score_semantic_complexity(title: str, description: str) -> Tuple[int, List[str]]:
    """
    Score semantic complexity using keywords (0-25 points).
    
    Returns: (score, reasons)
    """
    combined_text = f"{title} {description}".lower()
    scores = {'Advanced': 0, 'Intermediate': 0, 'Beginner': 0}
    reasons = []
    
    # Check all semantic keywords
    for difficulty_level, keywords_dict in SEMANTIC_COMPLEXITY.items():
        for keyword, points in keywords_dict.items():
            if keyword.lower() in combined_text:
                scores[difficulty_level] += points
                if points >= 4 and difficulty_level == 'Advanced':
                    reasons.append(f"Semantic: {keyword.title()}")
    
    # Normalize scores to 0-25 range
    max_score = max(scores.values())
    if max_score == 0:
        return 5, ["Standard complexity"]
    
    # Return highest difficulty score - weighted toward Advanced keywords
    if scores['Advanced'] > 0:
        return min(scores['Advanced'] * 1.2, 25), reasons
    elif scores['Intermediate'] > 0:
        return min(scores['Intermediate'], 25), reasons
    else:
        return min(scores['Beginner'] * 0.6, 25), reasons


def score_effort_estimation(title: str, description: str) -> Tuple[int, List[str]]:
    """
    Score effort estimation markers (0-20 points).
    
    Returns: (score, reasons)
    """
    combined_text = f"{title} {description}".lower()
    scores = {'advanced': 0, 'intermediate': 0, 'beginner': 0}
    reasons = []
    
    # Check effort patterns
    for effort_level, patterns in EFFORT_TIME_PATTERNS.items():
        for pattern, points in patterns:
            if re.search(pattern, combined_text):
                level_name = effort_level.split('_')[0]
                scores[level_name] += points
                if points >= 3:
                    reasons.append(f"Effort: {pattern.split('(')[0].title()}")
    
    # Determine primary effort level
    if scores['advanced'] >= 5:
        return min(scores['advanced'], 20), reasons
    elif scores['intermediate'] >= 3:
        return min(scores['intermediate'], 20), reasons
    else:
        return min(scores['beginner'], 20), reasons


def categorize_problem(title: str, description: str, suggested_tech: str = "") -> str:
    """
    Intelligently categorize a problem into Beginner, Intermediate, or Advanced.
    
    Multi-dimensional analysis:
    1. Technology Stack Complexity (0-30 points)
    2. Problem Scope & Scale (0-25 points)
    3. Semantic Complexity Keywords (0-25 points)
    4. Effort Estimation Markers (0-20 points)
    
    Total possible: 0-100 points
    - 0-35: Beginner
    - 36-65: Intermediate
    - 66+: Advanced
    
    Args:
        title: Problem title
        description: Problem description
        suggested_tech: Comma-separated technology tags
    
    Returns:
        Difficulty level: "Beginner", "Intermediate", or "Advanced"
    """
    combined_text = f"{title} {description} {suggested_tech}".lower()
    
    # Calculate component scores
    tech_score, tech_reasons = score_technology_stack(suggested_tech)
    scope_score, scope_reasons = score_problem_scope(title, description)
    semantic_score, semantic_reasons = score_semantic_complexity(title, description)
    effort_score, effort_reasons = score_effort_estimation(title, description)
    
    total_score = tech_score + scope_score + semantic_score + effort_score
    
    # Apply bonuses/penalties
    for pattern_name, (pattern, bonus) in BONUS_PATTERNS.items():
        if re.search(pattern, combined_text):
            total_score += bonus
    
    for pattern_name, (pattern, penalty) in NEGATIVE_FACTORS.items():
        if re.search(pattern, combined_text):
            total_score += penalty
    
    # Clamp score to 0-100
    total_score = max(0, min(100, total_score))
    
    # Classify difficulty
    if total_score <= 35:
        difficulty = 'Beginner'
    elif total_score >= 66:
        difficulty = 'Advanced'
    else:
        difficulty = 'Intermediate'
    
    return difficulty


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
    # Test the improved categorizer
    test_cases = [
        ("How to center a div with CSS?", "I'm struggling with CSS centering. Can anyone help?", "HTML, CSS"),
        ("Build a React todo app", "Create a simple todo application with React hooks", "React, JavaScript"),
        ("Fix my TypeScript import errors", "Getting module resolution errors, not sure what's wrong", "TypeScript"),
        ("Implement distributed caching system", "Design a high-performance, consistent cache across 100+ nodes", "Redis, Python, Kubernetes"),
        ("Machine learning model optimization", "Optimize neural network for billions of inferences per day with <100ms latency", "TensorFlow, GPU, CUDA"),
        ("Database query optimization", "Improve slow aggregation queries on million-row dataset", "PostgreSQL, SQL"),
        ("Setup Docker containers", "Deploy application using Docker Compose", "Docker, Docker Compose"),
        ("Real-time WebSocket streaming", "Build low-latency data streaming system for concurrent users", "Node.js, WebSocket, Redis"),
        ("Blockchain smart contract", "Implement secure ERC-20 token with complex access control", "Solidity, Ethereum"),
        ("System architecture redesign", "Refactor monolith to microservices for enterprise scalability", "Kubernetes, Microservices"),
    ]
    
    print("=" * 80)
    print("SMART DIFFICULTY CATEGORIZER TEST")
    print("=" * 80)
    
    for i, (title, desc, tech) in enumerate(test_cases, 1):
        difficulty = categorize_problem(title, desc, tech)
        print(f"\n{i}. [{difficulty.upper()}] {title}")
        print(f"   Tech: {tech}")
        print(f"   Desc: {desc[:60]}...")

