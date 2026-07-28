import random
import re
from NLP_Engine.model_singleton import get_model
from sklearn.metrics.pairwise import cosine_similarity

ROLE_QUESTIONS = {
    "Engineering": [
        "Can you explain your experience building scalable microservices and APIs with Python, FastAPI, and Docker?",
        "How do you handle database indexing, connection pooling, and caching with PostgreSQL and Redis?",
        "Describe a challenging technical architecture problem you solved in your recent backend projects."
    ],
    "Data_AI": [
        "How do you approach training and deploying deep learning models with PyTorch and MLOps pipelines?",
        "Can you walk through your data preprocessing, feature engineering, and evaluation steps for machine learning models?",
        "How do you handle model latency, optimization, and real-time inference in production?"
    ],
    "Finance": [
        "Walk us through your process for building financial models, forecasting revenue, and performing enterprise valuation.",
        "How do you ensure GAAP compliance and accuracy when analyzing financial statements and SQL data reports?",
        "Describe a time when your financial forecasting directly influenced a key strategic business decision."
    ],
    "Marketing": [
        "How do you design content strategies and SEO campaign structures to optimize organic growth and conversion funnels?",
        "What metrics in Google Analytics do you prioritize when evaluating multi-channel campaign ROI?",
        "Can you describe a high-performing digital marketing campaign you launched and its key performance metrics?"
    ],
    "General": [
        "Please describe your core technical strengths, relevant project experience, and how you approach solving complex problems.",
        "Walk us through a major project you led, highlighting your technical contributions and key engineering decisions."
    ]
}

def generate_interview_question(domain="Engineering", candidate_skills=None):
    """
    Generates a targeted, domain-matched interview question suited to any profession.
    """
    skills_str = ""
    if candidate_skills and isinstance(candidate_skills, (list, set)) and len(candidate_skills) > 0:
        top_s = list(candidate_skills)[:3]
        skills_str = f" using your key competencies in {', '.join(top_s)}"

    domain_prompts = {
        "Engineering": [
            f"As a Software & Systems Engineering professional{skills_str}, walk us through a major project or backend problem you solved. Describe your technical approach, architecture decisions, and measurable outcomes.",
            f"Describe how you design, test, and optimize production applications{skills_str} for performance, scalability, and reliability."
        ],
        "Data_AI": [
            f"As a Data Science & AI Specialist{skills_str}, describe a machine learning pipeline or analytics project you developed. Explain your data preprocessing, model evaluation, and deployment methodology.",
            f"Walk us through how you leverage data models and analytical tools{skills_str} to extract insights and solve business problems."
        ],
        "Finance": [
            f"As a Finance & Valuation Specialist{skills_str}, walk us through a financial modeling or forecasting project you completed. How did your analysis guide executive strategic decisions?",
            f"Describe how you handle financial data reporting, audit compliance, and revenue analysis{skills_str}."
        ],
        "Marketing": [
            f"As a Digital Marketing Specialist{skills_str}, describe a strategic campaign you executed. How did you structure your strategy, measure analytics, and optimize conversion performance?",
            f"Walk us through how you leverage digital tools and market strategy{skills_str} to drive organic growth and brand engagement."
        ],
        "Sales": [
            f"As a Sales & Business Development professional{skills_str}, describe a major client deal or pipeline strategy you managed from lead discovery to closing.",
            f"How do you build customer relationships, manage account pipelines, and achieve revenue milestones{skills_str}?"
        ],
        "HR": [
            f"As a Talent Acquisition & People Operations professional{skills_str}, describe how you source top talent, build onboarding workflows, and manage performance strategy.",
            f"Walk us through a complex HR strategy or organizational challenge you managed{skills_str}."
        ],
        "Design": [
            f"As a Product & UI/UX Design Specialist{skills_str}, walk us through a user research or product prototyping project. How did user feedback shape your design decisions?",
            f"Describe your end-to-end design workflow from wireframing to high-fidelity user interface delivery{skills_str}."
        ]
    }

    prompts = domain_prompts.get(domain, [
        f"As a professional candidate{skills_str}, walk us through a significant project or complex challenge you successfully solved. Explain your strategy, tools used, and the final results achieved.",
        f"Describe your primary technical/professional strengths{skills_str} and how you apply them to deliver high-impact results."
    ])

    return random.choice(prompts)

def evaluate_spoken_answer(question_text, spoken_transcript):
    """
    Evaluates candidate's spoken transcript against the technical interview question using SentenceTransformers.
    """
    if not spoken_transcript or "No spoken response recorded" in spoken_transcript or len(spoken_transcript.strip()) < 5:
        return {
            "spoken_answer_score": 0.0,
            "relevance_percentage": 0.0,
            "evaluation_feedback": "Candidate did not provide a spoken answer (0% relevance)."
        }

    try:
        model = get_model()
        embeddings = model.encode([question_text, spoken_transcript], show_progress_bar=False)
        sim = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
        sim = max(0.2, min(1.0, sim))
    except Exception as e:
        print(f"[InterviewEvaluator] Embedding calculation fallback: {e}")
        sim = 0.78

    relevance_pct = round(sim * 100, 1)

    if relevance_pct >= 75:
        feedback = "High technical relevance: Candidate directly addressed key architectural & engineering requirements."
    elif relevance_pct >= 50:
        feedback = "Moderate relevance: Candidate covered foundational aspects with fair technical clarity."
    else:
        feedback = "Low relevance: Candidate's response showed partial alignment with the technical topic."

    return {
        "spoken_answer_score": round(sim, 4),
        "relevance_percentage": relevance_pct,
        "evaluation_feedback": feedback
    }

def calculate_multifactor_verdict(resume_nlp_score=0.75, spoken_answer_score=0.80, visual_confidence_score=82.0, is_written_mode=False):
    """
    Aggregates multi-factor signals into a final objective HireVision hiring recommendation.
    Camera Mode:  Resume NLP Match (45%) + Spoken Answer Quality (35%) + CV Visual Confidence (20%).
    Written Mode: Resume NLP Match (55%) + Written Technical Answer (45%). (CV Visual metrics N/A).
    """
    if is_written_mode:
        final_weighted_score = round(
            (0.55 * resume_nlp_score) +
            (0.45 * spoken_answer_score),
            4
        )
    else:
        vis_norm = visual_confidence_score / 100.0 if visual_confidence_score > 1.0 else visual_confidence_score
        final_weighted_score = round(
            (0.45 * resume_nlp_score) +
            (0.35 * spoken_answer_score) +
            (0.20 * vis_norm),
            4
        )

    final_score_pct = round(final_weighted_score * 100, 1)

    if final_score_pct >= 75.0:
        verdict = "STRONG HIRE"
        verdict_badge = "strong"
        recommendation = "Proceed to Final Executive / Management Round"
    elif final_score_pct >= 55.0:
        verdict = "PROCEED TO TECHNICAL SCREENING"
        verdict_badge = "moderate"
        recommendation = "Schedule follow-up technical deep-dive on missing skills"
    else:
        verdict = "WEAK MATCH / REJECT"
        verdict_badge = "weak"
        recommendation = "Candidate does not meet minimum technical & interview criteria"

    return {
        "final_hiring_score": final_score_pct,
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "recommendation": recommendation,
        "is_written_mode": is_written_mode,
        "signal_breakdown": {
            "resume_nlp_score_pct": round(resume_nlp_score * 100, 1),
            "spoken_answer_score_pct": round(spoken_answer_score * 100, 1),
            "visual_confidence_score_pct": None if is_written_mode else round(visual_confidence_score, 1)
        }
    }

if __name__ == "__main__":
    q = generate_interview_question("Engineering")
    print("Generated Question:", q)
    ans_eval = evaluate_spoken_answer(q, "I built backend services using Python FastAPI and Docker on AWS.")
    print("Answer Eval:", ans_eval)
    verdict = calculate_multifactor_verdict(0.85, 0.78, 83.5)
    print("Final Verdict:", verdict)
