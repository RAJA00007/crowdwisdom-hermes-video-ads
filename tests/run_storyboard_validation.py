import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.storyboard_agent import StoryboardAgent
from agents.style_prompt_validator import StylePromptValidator

agent = StoryboardAgent()
sb = agent.generate_phase9_company_storyboard(verbose=True)

sb_path = Path("outputs/videos/editorial_storyboard.json")
report_path = Path("outputs/videos/style_prompt_validation.json")
validator = StylePromptValidator()
results = validator.validate_and_save_report(sb_path, report_path)
print("Validation Result:", results["valid"], "errors:", len(results["errors"]))
if not results["valid"]:
    for e in results["errors"]:
        print("  ERROR:", e)
assert results["valid"] is True, f"Validation failed: {results['errors']}"
print("Phase 9.1 Storyboard contract and prompt validation SUCCESS!")
