import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.assistant.rules import reply  

def run_benchmark():
    base_dir = os.path.dirname(__file__)
    cases_path = os.path.join(base_dir, "cases.csv")
    
    if not os.path.exists(cases_path):
        print(f"Error: Could not find {cases_path}")
        return

    correct = 0
    total = 0

    with open(cases_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            question = row.get("question", "")
            expected = row.get("expected_answer", "")
            
            response = reply(question)
            
            if expected.lower() in response.lower():
                correct += 1

    accuracy = (correct / total * 100) if total > 0 else 0
    print(f"Benchmark Results: {correct}/{total} correct ({accuracy:.2f}% accuracy)")

if __name__ == "__main__":
    run_benchmark()