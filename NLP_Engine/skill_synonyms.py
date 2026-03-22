SKILL_SYNONYMS = {

    "machine learning": [
        "ml",
        "machine-learning",
        "machine learning models"
    ],
    "deep learning": [
        "dl"
    ],
    "computer vision": [
        "cv",
        "image processing",
        "object detection"
    ],
    "javascript":["js"],
    "typescript":["ts"],
    "node.js":["node","nodejs"],
    "spring boot":["springboot", "spring-boot","spring boot framework"],
    "express":["express.js"],
    "scikit-learn":["sklearn","scikit learn"],
    "pytorch":["torch"],
     # Databases
    "postgresql": ["postgres", "psql"],
    "mongodb": ["mongo"],
    "mysql": ["my sql"],
    
    "kubernetes": ["k8s"],
    "tfl": ["tensorflow"],

    
    "pandas": ["pd"],
    "numpy": ["np"],

    "natural language processing": [
        "nlp",
        "text processing",
        "language models"
    ],
    
    "ci/cd":[
        "ci/cd pipelines",
        "ci cd",
        "ci/cd pipeline",
        "continuous integration",
        "continuous delivery",
    ],

    "python": [
        "python3",
        "py"
    ],

    "sql": [
        "mysql",
        "postgresql",
        "sqlite",
        "database querying"
    ],

    "pytorch": [
        "torch",
        "pytorch framework"
    ],

    "aws": [
        "amazon web services",
        "aws cloud"
    ]

}
def normalize_skills(extracted_skills):

    normalized = set()

    for skill in extracted_skills:
        skill = skill.lower()

        found = False

        for canonical, synonyms in SKILL_SYNONYMS.items():

            if skill == canonical or skill in synonyms:
                normalized.add(canonical)
                found = True
                break

        if not found:
            normalized.add(skill)

    return list(normalized)