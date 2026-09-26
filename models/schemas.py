from pydantic import BaseModel, Field
from typing import List


class SkillAnalysis(BaseModel):
    skill: str
    status: str = Field(
        description="One of: Strong Match, Partial Match, Missing"
    )
    evidence: str


class ResumeAnalysis(BaseModel):
    summary: str

    overall_match_percentage: float = Field(
        ge=0,
        le=100
    )

    required_skills: List[str]

    skill_analysis: List[SkillAnalysis]

    matched_skills: List[str]

    partial_skills: List[str]

    missing_skills: List[str]

    strengths: List[str]

    weaknesses: List[str]

    experience_match: str

    education_match: str

    improvement_suggestions: List[str]