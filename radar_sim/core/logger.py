# core/logger.py
import json
import os
from datetime import datetime

class Logger:
    """
    Records click events during a session and writes
    a full session report to a JSON file on completion.
    """

    def __init__(self, output_dir: str = "sessions"):
        self.output_dir   = output_dir
        self.click_events: list[dict] = []
        self.session_start = datetime.now()
        os.makedirs(output_dir, exist_ok=True)

    def log_click(self, obj_id: str, tag: str, result: str):
        """Record a single tagging event with a timestamp."""
        self.click_events.append({
            "timestamp": self._elapsed_seconds(),
            "obj_id":    obj_id,
            "tag":       tag,
            "result":    result,
        })

    def save_session(self, summary: dict, history: list[dict]):
        """
        Write the full session to a timestamped JSON file.
        summary  — from scorer.get_summary()
        history  — from scorer.history (final per-object decisions)
        """
        duration = self._elapsed_seconds()
        filename = self._build_filename()

        session_data = {
            "metadata": {
                "session_start": self.session_start.isoformat(),
                "duration_seconds": round(duration, 2),
                "total_objects": summary["total"] + summary["untagged"],
            },
            "summary":       summary,
            "final_decisions": history,
            "click_history": self.click_events,
        }

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(session_data, f, indent=2)

        print(f"\n  Session saved → {filepath}")

    def _elapsed_seconds(self) -> float:
        return (datetime.now() - self.session_start).total_seconds()

    def _build_filename(self) -> str:
        stamp = self.session_start.strftime("%Y%m%d_%H%M%S")
        return f"session_{stamp}.json"