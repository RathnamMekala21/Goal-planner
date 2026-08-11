import asyncio
import os
from google import genai
from ddgs import DDGS
from dotenv import load_dotenv

# Load env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found")

client = genai.Client(api_key=API_KEY)

print("✅ API Ready!")


# ---------------- AI FUNCTION ----------------
async def ask_ai(model, role, task, context=""):
    prompt = f"""
You are a {role}.

Context:
{context}

Task:
{task}

Return structured output:
- Summary
- Key Points
- Steps
"""

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=model,
            contents=prompt
        )
        return response.text or "Empty response"
    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------------- SEARCH ----------------
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))

        return "\n\n".join(
            f"Title: {r.get('title')}\nSnippet: {r.get('body')}"
            for r in results
        )
    except Exception as e:
        return f"Search Error: {str(e)}"


# ---------------- PIPELINE ----------------
async def run_pipeline(goal):
    print("\n🚀 Running agents...\n")

    analysis_task = ask_ai(
        "gemini-2.5-flash",
        "Problem Analyzer",
        f"Break down this goal: {goal}"
    )

    search_task = asyncio.to_thread(web_search, goal)

    analysis, web_data = await asyncio.gather(
        analysis_task,
        search_task
    )

    research = await ask_ai(
        "gemini-2.5-flash",
        "Tech Researcher",
        "Find best tools",
        web_data
    )

    await asyncio.sleep(2)

    plan = await ask_ai(
        "gemini-2.5-flash",
        "System Architect",
        "Create execution roadmap",
        f"{analysis[:1000]}\n{research[:1000]}"
    )

    await asyncio.sleep(2)

    validation = await ask_ai(
        "gemini-2.5-flash",
        "QA Expert",
        "Find flaws",
        plan[:1000]
    )

    return {
        "analysis": analysis,
        "research": research,
        "plan": plan,
        "validation": validation
    }


# ---------------- MAIN ----------------
async def main():
    goal = input("🎯 Enter your goal: ")

    result = await run_pipeline(goal)

    print("\n" + "="*50)
    print("🔍 ANALYSIS\n", result["analysis"])
    print("\n🌐 RESEARCH\n", result["research"])
    print("\n🛠 PLAN\n", result["plan"])
    print("\n✅ VALIDATION\n", result["validation"])
    print("="*50)


if __name__ == "__main__":
    asyncio.run(main())
