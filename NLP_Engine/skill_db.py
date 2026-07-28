# =============================================================================
# MASTER SKILL DATABASE — Universal across all job domains
# =============================================================================

MASTER_SKILLS = {

    # ── Programming Languages ─────────────────────────────────────────────────
    "languages": {
        "python", "java", "c", "c++", "c#", "javascript", "typescript",
        "go", "golang", "rust", "kotlin", "swift", "php", "ruby", "scala",
        "r", "elixir", "dart", "objective-c", "perl", "haskell", "clojure",
        "assembly", "matlab", "bash", "shell scripting", "groovy", "abap",
        "plsql", "pl/sql", "cobol", "fortran", "vba", "powershell",
    },

    # ── Frontend ──────────────────────────────────────────────────────────────
    "frontend": {
        "react", "react.js", "reactjs", "angular", "vue", "vue.js",
        "next.js", "nextjs", "nuxt", "nuxt.js", "svelte", "sveltekit",
        "remix", "astro", "html", "css", "sass", "less", "tailwind",
        "bootstrap", "redux", "redux toolkit", "react query", "zustand",
        "webpack", "vite", "rollup", "parcel", "babel",
        "responsive design", "web developer", "frontend developer",
        "frontend engineer", "ui developer",
    },

    # ── Backend ───────────────────────────────────────────────────────────────
    "backend": {
        "node.js", "nodejs", "express", "express.js", "nestjs", "nest.js",
        "fastify", "django", "fastapi", "flask", "spring", "spring boot",
        "laravel", "symfony", "codeigniter", "rails", "ruby on rails",
        "actix", "phoenix", "ktor", "quarkus",
        "rest api", "graphql", "grpc", "soap", "websocket", "microservices",
        "backend developer", "backend engineer", "api developer",
    },

    # ── Full Stack ────────────────────────────────────────────────────────────
    "fullstack": {
        "full stack", "fullstack", "full-stack", "mern", "mean", "pern",
        "lamp stack", "full stack developer", "full stack engineer",
        "fullstack developer",
    },

    # ── Mobile ────────────────────────────────────────────────────────────────
    "mobile": {
        "android", "ios", "react native", "flutter", "dart", "swift",
        "swiftui", "uikit", "objective-c", "kotlin", "jetpack compose",
        "xamarin", "ionic", "expo", "xcode", "android studio",
        "mobile developer", "mobile engineer", "mobile app developer",
    },

    # ── Databases ─────────────────────────────────────────────────────────────
    "databases": {
        "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
        "oracle", "dynamodb", "cassandra", "elasticsearch", "influxdb",
        "mariadb", "cockroachdb", "neo4j", "firestore", "cosmos db",
        "supabase", "prisma", "sqlalchemy", "hibernate",
        "nosql", "sql", "plsql", "pl/sql", "t-sql", "stored procedures",
        "database administration", "dba", "replication", "sharding",
    },

    # ── Cloud ─────────────────────────────────────────────────────────────────
    "cloud": {
        "aws", "azure", "gcp", "google cloud", "firebase", "cloudflare",
        "vercel", "netlify", "heroku", "digitalocean",
        "ec2", "s3", "lambda", "rds", "ecs", "eks", "cloudformation",
        "azure functions", "aks", "gke", "cloud run", "bigquery",
        "serverless", "cloud infrastructure", "cloud architect",
        "aws engineer", "azure engineer", "gcp engineer", "cloud engineer",
    },

    # ── DevOps / Infrastructure ───────────────────────────────────────────────
    "devops": {
        "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins",
        "github actions", "gitlab ci", "circleci", "travis ci",
        "helm", "istio", "linux", "ubuntu", "centos", "bash",
        "ci/cd", "continuous integration", "continuous delivery",
        "prometheus", "grafana", "datadog", "new relic", "pagerduty",
        "elk stack", "kibana", "logstash",
        "devops engineer", "site reliability engineer", "sre",
        "platform engineer", "infrastructure engineer",
    },

    # ── Data Engineering ──────────────────────────────────────────────────────
    "data_engineering": {
        "spark", "apache spark", "hadoop", "airflow", "apache airflow",
        "kafka", "apache kafka", "flink", "beam", "databricks",
        "dbt", "snowflake", "redshift", "delta lake",
        "etl", "data pipeline", "data warehouse", "data lake",
        "talend", "informatica", "nifi",
        "data engineer", "etl developer", "analytics engineer",
    },

    # ── Data Science / ML / AI ────────────────────────────────────────────────
    "machine_learning": {
        "machine learning", "deep learning", "nlp",
        "natural language processing", "computer vision",
        "pytorch", "tensorflow", "scikit-learn", "sklearn",
        "xgboost", "lightgbm", "catboost", "hugging face", "transformers",
        "bert", "gpt", "llm", "langchain", "openai", "stable diffusion",
        "rag", "retrieval augmented generation", "vector database",
        "pinecone", "mlops", "mlflow", "kubeflow",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
        "jupyter", "cuda", "reinforcement learning",
        "machine learning engineer", "ml engineer", "ai engineer",
        "data scientist", "nlp engineer", "computer vision engineer",
        "llm engineer", "generative ai", "gen ai", "prompt engineering",
    },

    # ── Data Analytics / BI ───────────────────────────────────────────────────
    "data_analytics": {
        "tableau", "power bi", "looker", "lookml", "dax", "power query",
        "excel", "google sheets", "data visualization", "data analysis",
        "business intelligence", "reporting", "dashboards", "analytics",
        "data analyst", "bi developer", "reporting analyst",
    },

    # ── Testing / QA ─────────────────────────────────────────────────────────
    "testing": {
        "selenium", "cypress", "playwright", "jest", "mocha", "chai",
        "pytest", "unittest", "testng", "junit", "appium", "jmeter",
        "gatling", "k6", "postman", "swagger",
        "manual testing", "automated testing", "test automation",
        "e2e testing", "performance testing", "load testing",
        "regression testing", "functional testing",
        "qa engineer", "quality assurance", "sdet", "test engineer",
        "automation engineer", "test automation engineer",
    },

    # ── Security ──────────────────────────────────────────────────────────────
    "security": {
        "cybersecurity", "penetration testing", "ethical hacking",
        "owasp", "kali linux", "burp suite", "metasploit",
        "network security", "application security", "appsec",
        "siem", "soc", "threat analysis", "incident response",
        "vulnerability assessment", "vapt", "devsecops", "snyk",
        "gdpr", "pci dss", "iso 27001",
        "security engineer", "cybersecurity engineer", "soc analyst",
        "penetration tester", "ethical hacker",
    },

    # ── Architecture / System Design ──────────────────────────────────────────
    "architecture": {
        "microservices", "monolith", "serverless", "event driven",
        "event-driven architecture", "service-oriented architecture",
        "system design", "scalability", "distributed systems",
        "high availability", "fault tolerance", "api design",
        "domain driven design", "ddd", "cqrs", "event sourcing",
        "solution architect", "software architect", "technical architect",
        "enterprise architecture", "togaf",
    },

    # ── Tools / Collaboration ─────────────────────────────────────────────────
    "tools": {
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "slack", "notion", "trello", "asana", "figma", "postman",
        "docker compose", "linux terminal",
    },

    # ── Blockchain / Web3 ─────────────────────────────────────────────────────
    "blockchain": {
        "blockchain", "solidity", "ethereum", "web3", "smart contracts",
        "defi", "nft", "hardhat", "truffle", "web3.js", "ethers.js",
        "solana", "substrate", "polkadot", "ipfs",
    },

    # ── Embedded / Hardware / IoT ─────────────────────────────────────────────
    "embedded": {
        "embedded c", "embedded systems", "rtos", "freertos", "arm",
        "microcontroller", "stm32", "arduino", "raspberry pi",
        "fpga", "vhdl", "verilog", "vlsi", "asic",
        "iot", "mqtt", "firmware", "pcb design", "altium",
        "firmware engineer", "embedded systems engineer",
    },

    # ── Game Development / AR / VR ────────────────────────────────────────────
    "game_dev": {
        "unity", "unreal engine", "godot", "blueprints",
        "opengl", "directx", "vulkan", "game development",
        "3d modeling", "blender", "maya", "3ds max", "cinema 4d",
        "ar", "vr", "xr", "arkit", "arcore", "oculus sdk", "openxr",
        "game developer", "unity developer",
    },

    # ── Design / UX / Creative ────────────────────────────────────────────────
    "design": {
        "figma", "sketch", "adobe xd", "photoshop", "illustrator",
        "indesign", "after effects", "premiere pro", "final cut pro",
        "davinci resolve", "blender", "cinema 4d", "zbrush",
        "wireframing", "prototyping", "user research", "usability testing",
        "design systems", "ui design", "ux design", "interaction design",
        "visual design", "graphic design", "motion graphics", "animation",
        "brand design", "typography", "accessibility",
        "ui/ux designer", "ux designer", "ui designer", "product designer",
        "graphic designer", "visual designer", "motion designer",
        "web designer", "figma designer",
    },

    # ── Product Management ────────────────────────────────────────────────────
    "product": {
        "product roadmap", "product strategy", "user stories",
        "backlog management", "backlog", "okrs", "kpis",
        "go-to-market", "competitive analysis", "stakeholder management",
        "product analytics", "feature prioritization", "mvp",
        "product discovery", "customer discovery", "sprint planning",
        "product lifecycle", "product management", "agile product",
        "product manager", "product owner", "technical product manager",
    },

    # ── Project Management ────────────────────────────────────────────────────
    "project_management": {
        "project management", "program management", "pmp", "prince2",
        "agile", "scrum", "kanban", "waterfall", "sprint planning",
        "retrospectives", "risk management", "delivery management",
        "project manager", "scrum master", "agile coach",
        "program manager", "delivery manager",
    },

    # ── HR / People Operations ────────────────────────────────────────────────
    "hr": {
        "talent acquisition", "recruitment", "staffing", "sourcing",
        "onboarding", "offboarding", "employee relations", "labor relations",
        "performance management", "performance reviews", "performance appraisal",
        "compensation", "benefits", "benefits administration",
        "compensation administration", "total rewards", "executive compensation",
        "workforce planning", "headcount planning", "succession planning",
        "organizational development", "org development",
        "learning and development", "l&d", "training and development",
        "leadership development", "executive coaching", "career coaching",
        "hr policy", "hr operations", "hr strategy", "hr analytics",
        "workforce analytics", "hr reporting", "hris", "hris implementation",
        "hr technology", "hr systems", "workday", "oracle hris", "sap hr",
        "adp", "bamboohr", "employee engagement", "change management",
        "diversity and inclusion", "dei", "compliance", "labor law",
        "employment law", "regulatory compliance", "hr compliance",
        "hr best practices", "mergers and acquisitions", "m&a integration",
        "due diligence", "hr budgeting", "cross-functional leadership",
        "shrm", "shrm-cp", "shrm-scp", "sphr", "phr",
        "employee performance", "performance improvement",
        "hr restructuring", "talent management", "talent development",
        "workforce development", "hr shared services", "hr transformation",
        "organizational effectiveness", "culture building",
        "employee experience", "hr infrastructure", "hr process design",
        "hr policy development", "hr program management",
        "hr manager", "hr executive", "hrbp", "hr business partner",
        "recruiter", "technical recruiter", "talent acquisition specialist",
        "staff training", "staff development", "team coaching",
        "sales coaching", "sales mentoring", "employee training",
    },

    # ── Marketing ─────────────────────────────────────────────────────────────
    "marketing": {
        "seo", "sem", "ppc", "google ads", "facebook ads", "bing ads",
        "google analytics", "ga4", "content marketing", "email marketing",
        "social media marketing", "social media management",
        "copywriting", "brand management", "brand strategy",
        "market research", "hubspot", "marketo", "mailchimp", "klaviyo",
        "a/b testing", "marketing automation", "demand generation",
        "lead generation", "growth marketing", "performance marketing",
        "product marketing", "marketing analytics", "content strategy",
        "influencer marketing", "community management",
        "digital marketing", "growth hacking",
        "seo specialist", "digital marketing specialist",
        "performance marketer", "social media manager",
        "marketing strategy", "brand awareness", "market penetration",
        "promotional strategy", "marketing campaigns",
    },

    # ── Sales / Business Development ──────────────────────────────────────────
    "sales": {
        # Core sales skills
        "b2b sales", "b2c sales", "account management", "cold calling",
        "lead generation", "pipeline management", "negotiation",
        "revenue growth", "upselling", "cross-selling",
        "sales strategy", "sales operations", "enterprise sales",
        "solution selling", "consultative selling", "customer success",
        "salesforce", "sfdc", "crm management", "sales forecasting",
        "quota attainment", "partnerships", "business development",
        "sales manager", "sales executive", "account executive",
        "account manager", "business development manager",
        # Sales leadership & director level
        "new business development", "key account management",
        "contract negotiations", "contract negotiation",
        "customer relationship management", "market expansion",
        "sales leadership", "sales director", "regional sales",
        "national sales", "sales team management", "sales performance management",
        "revenue targets", "sales campaigns", "pricing strategy",
        "market share", "sales vision", "strategic accounts",
        "high-performance sales", "sales quota", "sales metrics",
        "sales incentive programs", "sales incentive",
        "turnaround", "business turnaround", "revenue turnaround",
        "strategic sales planning", "sales plan",
        "profit performance", "profitability",
        "market presence", "customer acquisition",
        "sales growth", "sales results", "sales performance",
        "sales targets", "sales budget", "revenue targets",
        "sales representative", "sales rep",
        "inside sales", "outside sales", "field sales",
        "channel sales", "indirect sales", "direct sales",
        "sales enablement", "sales training",
        "crm software", "crm tools", "crm platform",
        "relationship building", "client relationships",
        "prospect management", "prospecting",
        "territory management", "territory planning",
    },

    # ── Finance / Accounting ──────────────────────────────────────────────────
    "finance": {
        "financial modeling", "financial models", "financial analysis",
        "financial reporting", "financial planning",
        "valuation", "dcf", "equity research", "investment analysis",
        "portfolio management", "budgeting", "forecasting",
        "variance analysis", "fp&a", "treasury", "tax", "audit",
        "accounts payable", "accounts receivable", "balance sheet",
        "income statement", "cash flow", "p&l", "cost accounting",
        "management accounting", "financial controls",
        "accounting", "gaap", "ifrs", "risk management",
        "bloomberg", "quickbooks", "sap finance", "oracle finance",
        "tally", "gst", "tds", "excel financial modeling",
        "financial analyst", "finance analyst", "finance manager",
        "chartered accountant", "ca", "accountant", "investment analyst",
        "risk analyst", "financial controller",
        # Sales-finance overlap
        "p&l management", "profit and loss management", "revenue forecasting",
        "sales budget", "budget management", "budget planning",
        "budgeting and forecasting", "budgeting & forecasting",
        "cost management", "cost reduction", "profit growth",
        "revenue management", "pricing management",
    },

    # ── Operations ────────────────────────────────────────────────────────────
    "operations": {
        "supply chain", "logistics", "procurement", "vendor management",
        "lean", "six sigma", "lean six sigma", "erp", "sap", "odoo",
        "operations management", "process improvement", "business operations",
        "operational efficiency", "resource planning", "capacity planning",
        "quality management", "iso", "continuous improvement",
        "inventory management", "warehouse management",
        "business analysis", "business process", "workflow automation",
        "operations manager", "supply chain manager", "logistics manager",
        "procurement manager", "business management",
    },

    # ── Legal / Compliance ────────────────────────────────────────────────────
    "legal": {
        "legal research", "contract drafting", "litigation",
        "intellectual property", "regulatory", "corporate law",
        "westlaw", "lexisnexis", "compliance", "contract management",
        "legal writing", "employment law", "labor law", "privacy law",
        "gdpr", "contract review", "legal counsel", "compliance officer",
    },

    # ── Healthcare ────────────────────────────────────────────────────────────
    "healthcare": {
        "ehr", "epic", "hipaa", "clinical trials", "patient care",
        "medical coding", "icd-10", "cpt", "nursing", "pharmacology",
        "telemedicine", "healthcare compliance", "clinical operations",
        "medical records", "population health", "hl7", "fhir",
        "mirth connect", "emr",
    },

    # ── Soft Skills / Leadership ──────────────────────────────────────────────
    "soft_skills": {
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "presentation",
        "cross-functional", "strategic planning", "decision making",
        "conflict resolution", "executive leadership", "people management",
        "team management", "relationship management", "influencing",
        "collaboration", "adaptability", "innovation", "strategic thinking",
        "mentoring", "coaching", "stakeholder management",
        "team leadership", "team building", "talent development",
        "organizational skills", "multitasking", "attention to detail",
        "negotiation",
    },

    # ── CMS / eCommerce ───────────────────────────────────────────────────────
    "cms_ecommerce": {
        "wordpress", "shopify", "magento", "woocommerce", "drupal",
        "webflow", "contentful", "strapi", "sanity", "ghost",
        "liquid", "shopify apps", "ecommerce",
    },

    # ── Enterprise / ERP / CRM / Integration ──────────────────────────────────
    "enterprise": {
        "sap", "sap hana", "s4 hana", "sap fico", "sap mm", "sap sd",
        "abap", "oops abap", "bapi", "idoc", "rfc",
        "oracle erp", "oracle fusion", "oracle apex",
        "dynamics 365", "dynamics crm", "microsoft dynamics",
        "servicenow", "mulesoft", "boomi", "informatica", "talend",
        "power apps", "power automate", "power platform", "sharepoint",
        "microsoft 365", "azure ad", "active directory",
        "hubspot", "zoho", "zoho crm",
        "crm", "erp",
    },

    # ── Telecom ───────────────────────────────────────────────────────────────
    "telecom": {
        "5g", "lte", "nr", "core network", "ran", "voip", "rf",
        "radio frequency", "antenna", "telecom", "networking",
        "cisco", "ccna", "ccnp", "routing", "switching", "firewall",
        "vpn", "tcp/ip",
    },

    # ── Low-code / No-code ────────────────────────────────────────────────────
    "low_code": {
        "power apps", "power automate", "bubble", "retool", "outsystems",
        "mendix", "webflow", "airtable", "zapier", "make",
        "low-code", "no-code", "low code", "no code",
    },
}


# =============================================================================
# ALL_SKILLS — flat set used by job_parser and skill_extractor
# =============================================================================
ALL_SKILLS = set()
for category in MASTER_SKILLS.values():
    ALL_SKILLS.update(category)
