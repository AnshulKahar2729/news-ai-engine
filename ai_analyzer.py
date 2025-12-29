import subprocess
import json

def analyze_news(text, model):
    with open("prompts/impact_prompt.txt") as f:
        prompt = f.read()

    prompt = prompt.replace("{{NEWS_TEXT}}", text[:4000])

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True
    )

    try:
        return json.loads(result.stdout)
    except:
        return None
