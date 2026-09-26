from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from models.schemas import ResumeAnalysis
from utils.prompts import ANALYSIS_PROMPT


load_dotenv()


def analyze_resume(
    job_description: str,
    resume_text: str
) -> ResumeAnalysis:

    llm = ChatGoogleGenerativeAI(
        model='gemini-3.1-flash-lite',
        temperature=0
    )

    structured_llm = llm.with_structured_output(
        ResumeAnalysis
    )

    prompt = ChatPromptTemplate.from_template(
        ANALYSIS_PROMPT
    )

    chain = prompt | structured_llm

    result = chain.invoke({
        "job_description": job_description,
        "resume_text": resume_text
    })

    return result