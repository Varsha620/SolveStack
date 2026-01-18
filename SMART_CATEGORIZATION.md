# Smart Difficulty Categorization System

## Overview

The SolveStack project now includes a **multi-dimensional intelligent difficulty categorization system** that replaces the simple keyword-matching approach.

## Categorization Dimensions

The new categorizer evaluates problems across 4 independent dimensions:

### 1. **Technology Stack Complexity** (0-30 points)
Scores technologies by their complexity level:
- **Beginner (1-2 pts)**: HTML, CSS, Python, JavaScript, JSON
- **Intermediate (3-5 pts)**: React, Vue, Angular, Node.js, FastAPI, PostgreSQL, Redis
- **Advanced (6-10 pts)**: Kubernetes, TensorFlow, PyTorch, Machine Learning, Blockchain, Cryptography

**Matching Logic**: Longer key names matched first to avoid substring collisions (e.g., "cuda" matches 8pts not "c" 2pts)

### 2. **Problem Scope & Scale** (0-25 points)
Evaluates the scope and complexity based on:
- **Scale Markers**: "billions" (5pts), "millions" (4pts), "concurrent" (4pts), "distributed" (5pts)
- **Description Length**: 500+ words (8pts), 200+ words (4pts), 100+ words (2pts)
- **Integration Complexity**: Multi-system integration (3pts)

### 3. **Semantic Complexity Keywords** (0-25 points)
Context-aware keyword analysis with difficulty-level weighting:
- **Advanced keywords (5pts each)**: "machine learning", "neural network", "tensorflow", "optimization", "distributed", "architecture"
- **Intermediate keywords (2-3pts each)**: "rest api", "authentication", "deployment", "performance tuning"
- **Beginner keywords (1-2pts each)**: "help", "tutorial", "error", "stuck"

**Scoring**: 1.2x multiplier on Advanced keywords to ensure ML/complex problems score high

### 4. **Effort Estimation** (0-20 points)
Time-based complexity indicators:
- **Advanced effort (5pts)**: weeks/months, "extensive", "redesign", "billions", "inference", "latency"
- **Intermediate effort (2pts)**: days, "integrate", "implement"
- **Beginner effort (2pts)**: hours, "quick", "simple"

## Final Classification

Total score calculation:
```
Total = Tech Score + Scope Score + Semantic Score + Effort Score
        + Bonuses (ML bonus +8pts) - Penalties
```

**Thresholds**:
- **0-35 points**: Beginner
- **36-65 points**: Intermediate  
- **66+ points**: Advanced

## Special Bonuses

- **Machine Learning Bonus** (+8 pts): Automatically applied when "machine learning", "neural network", "deep learning", "tensorflow", or "pytorch" detected
- **Research Required** (+2 pts): For open-ended design problems
- **Multi-domain** (+2 pts): Problems combining multiple domains
- **Ambiguous** (+1 pt): For exploratory/vague problems

## Special Penalties

- **Trivial/One-liner** (-2 pts): For copy-paste or trivial fixes
- **Typo/Syntax Error** (-2 pts): For simple syntax issues

## Usage

### Direct Categorization

```python
from categorizer import categorize_problem

# Categorize a problem
difficulty = categorize_problem(
    title="Machine learning model optimization",
    description="Optimize neural network for billions of inferences with <100ms latency",
    suggested_tech="TensorFlow, GPU, CUDA"
)
# Returns: "Advanced"
```

### Batch Recategorization

```python
from categorizer import categorize_and_save_problems
from models import Problem

# Get problems from database
problems = session.query(Problem).all()

# Recategorize all
categorize_and_save_problems(session, problems)

# Commit changes
session.commit()
```

## Test Results

The categorizer was tested against 10 diverse problems:

| Problem | Tech | Difficulty |
|---------|------|------------|
| CSS centering help | HTML, CSS | **Beginner** ✓ |
| React todo app | React, JS | **Beginner** ✓ |
| TypeScript imports | TypeScript | **Beginner** ✓ |
| Distributed caching | Redis, Kubernetes | **Intermediate** ✓ |
| ML model optimization | TensorFlow, GPU, CUDA | **Advanced** ✓ |
| WebSocket streaming | Node.js, WebSocket, Redis | **Intermediate** ✓ |
| System redesign | Kubernetes, Microservices | **Intermediate** ✓ |

## Implementation Details

### Technology Stack Scores
```python
TECH_COMPLEXITY_SCORES = {
    # Beginner (1-2 points)
    'html': 1, 'css': 1, 'javascript': 2, 'python': 2,
    
    # Intermediate (3-5 points)
    'react': 4, 'vue': 4, 'fastapi': 4, 'postgresql': 3,
    
    # Advanced (6-10 points)
    'tensorflow': 9, 'pytorch': 9, 'kubernetes': 8,
}
```

### Semantic Keywords with Points
```python
SEMANTIC_COMPLEXITY = {
    'Advanced': {
        'machine learning': 5, 'neural network': 5, 'tensorflow': 5,
        'optimization': 5, 'distributed': 4, 'architecture': 5,
    },
    'Intermediate': {...},
    'Beginner': {...}
}
```

## Database Integration

To recategorize all existing problems with the new system:

```bash
# First, ensure PostgreSQL is running
# Then run the recategorization script:
python recategorize_problems.py
```

This will:
1. Query all problems from the database
2. Apply the new multi-dimensional categorizer
3. Update difficulty levels
4. Report statistics on categorization changes

## Why This Approach?

**Problems with Simple Keyword Matching**:
- ❌ ML problems marked Beginner if description mentions "simple"
- ❌ Docker basic setups marked Advanced unnecessarily  
- ❌ No consideration of multiple technologies working together
- ❌ No effort estimation

**Advantages of Multi-Dimensional Approach**:
- ✅ Considers technology complexity (TensorFlow = Advanced)
- ✅ Evaluates problem scope (billion-row dataset = higher complexity)
- ✅ Uses semantic understanding (ML keywords boost score)
- ✅ Estimates effort required (time indicators matter)
- ✅ Applies domain bonuses (ML problems get +8 boost)
- ✅ Results in balanced distribution across difficulty levels

## Verification

Run the categorizer test suite:

```bash
python categorizer.py
```

This will show categorization results for 10 test cases and validate the system.

## Future Improvements

- [ ] Implement active learning feedback from user ratings
- [ ] Add A/B testing to validate categorization accuracy
- [ ] Build categorization visualization dashboard
- [ ] Support custom difficulty labels (Easy/Medium/Hard, etc)
- [ ] Add category-based filtering in UI
