import sys
import time
import random
import traceback
import json
from pathlib import Path
from litellm import completion

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.graph.orchestrator_v10 import V10Orchestrator

def generate_topics(count):
    prompt = f"Generate a JSON array of {count} highly engaging, technical, and educational topics for LinkedIn carousels for software engineers, data engineers, and tech professionals. Just return the raw JSON array of strings, nothing else."
    
    response = completion(
        model="gemini/gemini-1.5-pro",
        messages=[{"role": "user", "content": prompt}],
    )
    
    text = response.choices[0].message.content.strip()
    # Clean markdown if present
    if text.startswith("`"):
        text = "\n".join(text.split("\n")[1:-1])
    return json.loads(text)

def main():
    print("🚀 Starting Mass Scale Production (Phase 1) 🚀", flush=True)
    target_count = 100
    
    print(f"\n1. Generating {target_count} unique topics via AI...", flush=True)
    try:
        topics = generate_topics(target_count)
        print(f"✅ Generated {len(topics)} topics successfully.", flush=True)
    except Exception as e:
        print(f"❌ Failed to generate topics: {e}", flush=True)
        # Fallback topics
        topics = [
            "Advanced Git Commands You Probably Don't Use",
            "Why Docker Changed Software Development Forever",
            "Understanding Dependency Injection in 5 Minutes",
            "How to Optimize Your SQL Queries Like a Pro",
            "CI/CD Best Practices for Modern Teams",
            "Demystifying Oauth 2.0 and OpenID Connect",
            "The True Cost of Technical Debt",
            "How WebSockets Work Under the Hood",
            "Why Go is the Best Language for Microservices",
            "The Fundamentals of Apache Kafka"
        ]
        print("Using 10 fallback topics instead.", flush=True)

    orchestrator = V10Orchestrator()
    success_count = 0
    fail_count = 0
    
    print("\n2. Beginning Production Loop...", flush=True)
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*50}", flush=True)
        print(f"[{i}/{len(topics)}] Generating: {topic}", flush=True)
        print(f"{'='*50}", flush=True)
        
        try:
            res = orchestrator.run(topic=topic)
            success_count += 1
            print(f"✅ Success! Saved to {res['output_dir']}", flush=True)
        except Exception as e:
            fail_count += 1
            print(f"❌ Failed: {e}", flush=True)
            traceback.print_exc()
        
        # We don't want to blast the LLM provider, and we want to let the system cool down.
        sleep_time = random.uniform(5, 12)
        print(f"💤 Sleeping for {sleep_time:.1f}s to avoid rate limits...", flush=True)
        time.sleep(sleep_time)
        
    print("\n" + "="*50, flush=True)
    print("MASS PRODUCTION COMPLETE", flush=True)
    print(f"Total: {len(topics)} | Success: {success_count} | Failed: {fail_count}", flush=True)
    print("="*50, flush=True)

if __name__ == "__main__":
    main()
