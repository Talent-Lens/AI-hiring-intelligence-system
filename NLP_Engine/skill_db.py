MASTER_SKILLS = {

    "languages": {
        "python","java","c","c++","c#","javascript","typescript","go","rust","kotlin","swift","php"
    },

    "frontend": {
        "react","angular","vue","next.js","html","css","tailwind","bootstrap","redux"
    },

    "backend": {
        "node.js","express","django","flask","spring","spring boot","fastapi","laravel"
    },

    "databases": {
        "mysql","postgresql","mongodb","redis","sqlite","oracle","dynamodb"
    },

    "cloud": {
        "aws","azure","gcp","firebase","cloudflare"
    },

    "devops": {
        "docker","kubernetes","terraform","ansible","jenkins","github actions",
        "linux","bash","ci/cd","prometheus","grafana"
    },

    "machine_learning": {
        "machine learning","deep learning","nlp","computer vision","pytorch",
        "tensorflow","scikit-learn","xgboost","pandas","numpy"
    },

    "tools": {
        "git","github","gitlab","bitbucket","jira","slack","postman"
    }

}

ALL_SKILLS = set()

for category in MASTER_SKILLS.values():
    ALL_SKILLS.update(category)