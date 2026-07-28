# =============================================================================
# SKILL SYNONYMS & CANONICAL NORMALIZATION
# Every variant maps to one canonical form so the matcher never sees
# two different strings for the same concept.
# =============================================================================

# The single source of truth: variant -> canonical
CANONICAL_MAP = {
    # ── Tech: Frameworks / Tools ──────────────────────────────────────────────
    "apache airflow": "airflow",
    "apache kafka": "kafka",
    "apache spark": "spark",
    "oops abap": "abap",
    "android studio": "android",
    "aws engineer": "aws",
    "amazon web services": "aws",
    "azure engineer": "azure",
    "azure ad": "azure",
    "azure functions": "azure",
    "microsoft azure": "azure",
    "gcp engineer": "gcp",
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "react.js": "react",
    "reactjs": "react",
    "vue.js": "vue",
    "nodejs": "node.js",
    "node": "node.js",
    "nextjs": "next.js",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "k8s": "kubernetes",
    "sfdc": "salesforce",
    "sf crm": "salesforce",
    "continuous integration": "ci/cd",
    "continuous delivery": "ci/cd",
    "continuous integration continuous delivery": "ci/cd",
    "github actions": "ci/cd",
    "gitlab ci": "ci/cd",

    # ── Tech: ML / AI ─────────────────────────────────────────────────────────
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "machine learning models": "machine learning",
    "nlp": "natural language processing",
    "text processing": "natural language processing",
    "language models": "natural language processing",
    "cv": "computer vision",
    "image processing": "computer vision",
    "object detection": "computer vision",
    "computer vision engineer": "computer vision",
    "dl": "deep learning",
    "sklearn": "scikit-learn",

    # ── Tech: Languages ───────────────────────────────────────────────────────
    "python3": "python",
    "py": "python",
    "js": "javascript",
    "es6": "javascript",
    "ecmascript": "javascript",
    "ts": "typescript",
    "cpp": "c++",
    "golang": "go",
    "pl sql": "pl/sql",
    "plsql": "pl/sql",

    # ── Tech: Data ────────────────────────────────────────────────────────────
    "ga4": "google analytics",
    "google analytics 4": "google analytics",
    "powerbi": "power bi",
    "power-bi": "power bi",
    "microsoft power bi": "power bi",

    # ── Tech: Other ───────────────────────────────────────────────────────────
    "etl developer": "etl",
    "data pipeline": "etl",
    "analytics engineer": "analytics",
    "hr analytics": "analytics",
    "reporting": "analytics",
    "dashboards": "analytics",
    "data analysis": "analytics",
    "sales metrics": "analytics",
    "agile coach": "agile",
    "agile product": "agile",
    "backlog": "backlog management",
    "digital marketing specialist": "digital marketing",
    "seo specialist": "seo",
    "search engine optimization": "seo",
    "search engine marketing": "sem",
    "pay per click": "ppc",
    "cybersecurity engineer": "cybersecurity",
    "cross-functional leadership": "cross-functional",

    # ── Sales ─────────────────────────────────────────────────────────────────
    "key account management": "account management",
    "strategic account management": "account management",
    "major account management": "account management",
    "client account management": "account management",
    "named account management": "account management",
    "new business development": "business development",
    "new business acquisition": "business development",
    "business growth": "business development",
    "growing the business": "business development",
    "new revenue streams": "business development",
    "identifying new opportunities": "business development",
    "business development manager": "business development",
    "contract negotiations": "negotiation",
    "contract negotiation": "negotiation",
    "deal negotiation": "negotiation",
    "terms negotiation": "negotiation",
    "high-value contracts": "negotiation",
    "contract management": "negotiation",
    "customer relationship management": "crm",
    "client relationship management": "crm",
    "client relationships": "crm",
    "customer relationships": "crm",
    "relationship management": "crm",
    "account relationships": "crm",
    "crm management": "crm",
    "crm platform": "crm",
    "crm software": "crm",
    "crm tools": "crm",
    "forecasting": "sales forecasting",
    "revenue forecasting": "sales forecasting",
    "pipeline forecasting": "sales forecasting",
    "demand forecasting": "sales forecasting",
    "revenue targets": "revenue growth",
    "revenue generation": "revenue growth",
    "revenue expansion": "revenue growth",
    "revenue achievement": "revenue growth",
    "revenue increase": "revenue growth",
    "growing revenue": "revenue growth",
    "growing sales": "revenue growth",
    "increasing sales": "revenue growth",
    "sales increase": "revenue growth",
    "sales results": "revenue growth",
    "sales growth": "revenue growth",
    "profit growth": "profitability",
    "profit improvement": "profitability",
    "profit and loss": "profitability",
    "p&l performance": "profitability",
    "p&l": "profitability",
    "p&l management": "profitability",
    "margin improvement": "profitability",
    "profitable growth": "profitability",
    "profit performance": "profitability",
    "market share": "market expansion",
    "market growth": "market expansion",
    "market penetration": "market expansion",
    "market development": "market expansion",
    "market presence": "market expansion",
    "new markets": "market expansion",
    "growing market share": "market expansion",
    "pipeline development": "pipeline management",
    "opportunity management": "pipeline management",
    "deal management": "pipeline management",
    "sales pipeline": "pipeline management",
    "managing pipeline": "pipeline management",
    "national sales": "sales leadership",
    "regional sales": "sales leadership",
    "head of sales": "sales leadership",
    "vp sales": "sales leadership",
    "sales director": "sales leadership",
    "managing sales teams": "sales leadership",
    "directing sales": "sales leadership",
    "leading sales teams": "sales leadership",
    "sales campaigns": "marketing strategy",
    "marketing campaigns": "marketing strategy",
    "promotional strategy": "marketing strategy",
    "go-to-market": "marketing strategy",
    "brand strategy": "marketing strategy",
    "customer acquisition": "lead generation",
    "prospecting": "lead generation",
    "new customers": "lead generation",
    "acquiring customers": "lead generation",
    "strategic partnerships": "partnerships",
    "business partnerships": "partnerships",
    "business turnaround": "turnaround",
    "revenue turnaround": "turnaround",
    "organizational turnaround": "turnaround",
    "revived operations": "turnaround",
    "turning around": "turnaround",

    # ── Finance ───────────────────────────────────────────────────────────────
    "financial models": "financial modeling",
    "financial modelling": "financial modeling",
    "financial analysis": "financial modeling",
    "financial planning and analysis": "fp&a",
    "financial planning & analysis": "fp&a",
    "fp & a": "fp&a",
    "budgeting & forecasting": "budgeting",
    "budgeting and forecasting": "budgeting",
    "hr budgeting": "budgeting",
    "sales budget": "budgeting",
    "budget management": "budgeting",
    "budget planning": "budgeting",
    "annual budget": "budgeting",
    "cost management": "budgeting",
    "gaap": "gaap",
    "ifrs": "ifrs",

    # ── HR ────────────────────────────────────────────────────────────────────
    "recruitment": "talent acquisition",
    "recruiting": "talent acquisition",
    "staffing": "talent acquisition",
    "talent sourcing": "talent acquisition",
    "hiring": "talent acquisition",
    "talent recruitment": "talent acquisition",
    "l&d": "learning and development",
    "training and development": "learning and development",
    "employee training": "learning and development",
    "learning & development": "learning and development",
    "staff training": "learning and development",
    "staff development": "learning and development",
    "team coaching": "learning and development",
    "employee performance": "performance management",
    "performance reviews": "performance management",
    "performance appraisal": "performance management",
    "performance improvement": "performance management",
    "sales performance management": "performance management",
    "sales performance": "performance management",
    "hris implementation": "hris",
    "hr technology": "hris",
    "hr systems": "hris",
    "hr tech": "hris",
    "human resource information system": "hris",
    "hris platform": "hris",
    "enterprise hr systems": "hris",
    "headcount planning": "workforce planning",
    "workforce management": "workforce planning",
    "resource planning": "workforce planning",
    "manpower planning": "workforce planning",
    "leadership pipeline": "succession planning",
    "succession management": "succession planning",
    "org development": "organizational development",
    "organization development": "organizational development",
    "organisational development": "organizational development",
    "organizational change": "change management",
    "change leadership": "change management",
    "transformation": "change management",
    "dei": "diversity and inclusion",
    "diversity equity inclusion": "diversity and inclusion",
    "d&i": "diversity and inclusion",
    "diversity & inclusion": "diversity and inclusion",
    "m&a": "mergers and acquisitions",
    "m&a integration": "mergers and acquisitions",
    "post-acquisition integration": "mergers and acquisitions",
    "acquisition integration": "mergers and acquisitions",
    "merger integration": "mergers and acquisitions",
    "shrm scp": "shrm-scp",
    "shrm senior certified professional": "shrm-scp",
    "society of human resources management senior certified professional": "shrm-scp",
    "senior professional in human resources": "sphr",
    "professional in human resources": "phr",
    "labor relations": "employee relations",
    "employee experience": "employee engagement",
    "compensation administration": "compensation",
    "executive compensation": "compensation",
    "benefits administration": "benefits",
    "compliance officer": "compliance",
    "hr compliance": "compliance",
    "healthcare compliance": "compliance",
    "regulatory compliance": "compliance",
    "chartered accountant": "accountant",
    "career coaching": "coaching",
    "executive coaching": "coaching",
    "sales coaching": "coaching",

    # ── Soft Skills / Leadership ───────────────────────────────────────────────
    "executive leadership": "leadership",
    "strategic thinking": "leadership",
    "decision making": "leadership",
    "influencing": "leadership",
    "team management": "team leadership",
    "managing teams": "team leadership",
    "leading teams": "team leadership",
    "people management": "team leadership",
    "people leadership": "team leadership",
    "managing people": "team leadership",
    "managing staff": "team leadership",
    "managing employees": "team leadership",
    "team building": "team leadership",
    "presentation": "communication",
    "public speaking": "communication",
    "interpersonal skills": "communication",
    "teamwork": "collaboration",
    "critical thinking": "problem solving",
    "analytical skills": "problem solving",
    "organizational skills": "time management",
    "multitasking": "time management",
    "executive stakeholders": "stakeholder management",
    "stakeholder engagement": "stakeholder management",
    "strategic sales planning": "strategic planning",
    "sales planning": "strategic planning",
    "business planning": "strategic planning",
    "annual planning": "strategic planning",
    "go-to-market planning": "strategic planning",

    # ── Operations ────────────────────────────────────────────────────────────
    "business operations": "operations management",
    "operational efficiency": "operations management",
    "business management": "operations management",
    "supply chain management": "supply chain",
    "enterprise resource planning": "erp",
    "lean six sigma": "six sigma",
    "6 sigma": "six sigma",
    "program management": "project management",
    "pmp": "project management",

    # ── Product ────────────────────────────────────────────────────────────────
    "product manager": "product management",
    "product owner": "product management",
    "kpi": "kpis",
    "key performance indicator": "kpis",
    "key performance indicators": "kpis",
    "okr": "okrs",
    "objectives and key results": "okrs",
}


def normalize_skills(extracted_skills):
    """
    Maps every extracted skill string to its canonical form.
    Handles both lists and dicts (skill_weights from job_parser).
    Falls back to lowercased original if no mapping found.
    """
    if isinstance(extracted_skills, dict):
        keys = list(extracted_skills.keys())
    else:
        keys = list(extracted_skills)

    normalized = set()
    for skill in keys:
        skill_lower = skill.lower().strip()
        # Look up canonical form — fall back to the skill itself
        canonical = CANONICAL_MAP.get(skill_lower, skill_lower)
        normalized.add(canonical)

    return list(normalized)


# =============================================================================
# DOMAIN BRIDGE — implies canonical skills from resume phrases
# when the exact keyword never appears verbatim
# =============================================================================

DOMAIN_BRIDGE_PHRASES = {
    "business development": [
        "new business", "new business opportunities", "market expansion",
        "revenue generation", "growing the business", "new revenue streams",
        "sales growth", "achieving sales targets", "achieving sales budgets",
        "exceeding sales targets", "driving sales results",
    ],
    "lead generation": [
        "new business", "prospecting", "new customers",
        "acquiring customers", "customer acquisition",
    ],
    "negotiation": [
        "closing sales", "closing deals", "pricing negotiations",
        "contract negotiations", "negotiating contracts",
    ],
    "account management": [
        "client relationships", "customer relationships",
        "managing accounts", "client retention", "customer retention",
        "key clients", "strategic accounts",
    ],
    "crm": [
        "point of sale", "pos system", "sales tracking",
        "client relationship", "customer relationship",
    ],
    "sales leadership": [
        "leading sales teams", "managing sales teams",
        "directing sales", "head of sales", "sales director",
        "regional manager", "sales manager",
    ],
    "market expansion": [
        "market growth", "expanding market", "market penetration",
        "new markets", "market share growth", "market share",
    ],
    "profitability": [
        "profit and loss", "p&l", "managing costs",
        "cost management", "revenue performance", "profit performance",
    ],
    "budgeting": [
        "managing budgets", "budget planning", "annual budget",
        "sales budget", "budget management", "cost management",
    ],
    "turnaround": [
        "revived operations", "turned around", "turnaround success",
        "business transformation", "performance improvement",
    ],
    "strategic planning": [
        "strategic sales planning", "sales planning",
        "business planning", "annual planning", "go-to-market planning",
    ],
    "team leadership": [
        "managing teams", "leading teams", "people management",
        "managing employees", "team management", "managing staff",
    ],
    "revenue growth": [
        "growing revenue", "revenue increase", "sales growth",
        "increasing sales", "growing sales", "sales increase",
        "revenue achievement", "exceeding targets",
    ],
    "analytics": [
        "sales reporting", "performance metrics", "data-driven",
        "sales analytics", "business analytics", "kpi tracking",
    ],
    "marketing strategy": [
        "sales campaigns", "promotional activities", "brand awareness",
        "go-to-market strategy", "marketing initiatives",
    ],
    "partnerships": [
        "strategic alliances", "channel partners", "business alliances",
        "partner relationships", "partner management",
    ],
    "new business development": [
        "new business", "business development", "new revenue generation",
        "new business opportunities", "market expansion",
    ],
    "key account management": [
        "strategic account management", "major account management",
        "key clients", "strategic accounts", "named accounts",
    ],
    "p&l management": [
        "profit and loss", "p&l", "managing costs",
        "cost management", "budget management", "managing budgets",
    ],
}


def expand_with_domain_bridge(resume_text_lower: str) -> set:
    """
    Returns canonical skills implied by domain-bridge phrases found
    in the resume, even if the exact skill keyword never appears verbatim.
    """
    implied_skills = set()
    for canonical_skill, phrases in DOMAIN_BRIDGE_PHRASES.items():
        for phrase in phrases:
            if phrase in resume_text_lower:
                implied_skills.add(canonical_skill)
                break
    return implied_skills