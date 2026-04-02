# core/scorer.py
from core.radar_object import RadarObject

class Scorer:
    """
    Evaluates user tags against ground truth.
    Scores final decisions only — not intermediate clicks.
    """

    def __init__(self):
        self.history: list[dict] = []

    def evaluate_live(self, obj: RadarObject) -> str:
        """
        Called on each click for live console feedback only.
        Does NOT affect the final summary.
        """
        return self._classify(obj.tag, obj.get_type())

    def evaluate_session(self, objects: list[RadarObject]):
        """
        Called once at session end.
        Scores the final tag state of every object.
        """
        self.history.clear()
        for obj in objects:
            tag    = obj.tag
            truth  = obj.get_type()
            result = self._classify(tag, truth)
            self.history.append({
                "obj_id": obj.obj_id,
                "tag":    tag,
                "truth":  truth,
                "result": result,
            })

    def _classify(self, tag: str, truth: str) -> str:
        if tag is None:
            return "untagged"
        if tag == "real"  and truth == "aircraft": return "correct"
        if tag == "noise" and truth == "noise":    return "correct"
        if tag == "real"  and truth == "noise":    return "incorrect"
        if tag == "noise" and truth == "aircraft": return "incorrect"
        return "untagged"

    def get_summary(self) -> dict:
        tp = sum(1 for h in self.history if h["tag"] == "real"  and h["truth"] == "aircraft")
        tn = sum(1 for h in self.history if h["tag"] == "noise" and h["truth"] == "noise")
        fp = sum(1 for h in self.history if h["tag"] == "real"  and h["truth"] == "noise")
        fn = sum(1 for h in self.history if h["tag"] == "noise" and h["truth"] == "aircraft")
        untagged = sum(1 for h in self.history if h["tag"] is None)

        total   = tp + tn + fp + fn
        correct = tp + tn

        return {
            "total":           total,
            "correct":         correct,
            "incorrect":       total - correct,
            "untagged":        untagged,
            "true_positives":  tp,
            "true_negatives":  tn,
            "false_positives": fp,
            "false_negatives": fn,
            "accuracy":        round(correct / total * 100, 1) if total > 0 else 0.0,
        }

    def print_summary(self, objects: list[RadarObject]):
        self.evaluate_session(objects)
        s = self.get_summary()

        print("\n" + "=" * 40)
        print("        RADAR SESSION SUMMARY")
        print("=" * 40)
        print(f"  Objects in session:  {len(objects)}")
        print(f"  Tagged:              {s['total']}")
        print(f"  Untagged:            {s['untagged']}")
        print(f"  Correct:             {s['correct']}")
        print(f"  Incorrect:           {s['incorrect']}")
        print(f"  True  positives:     {s['true_positives']}")
        print(f"  True  negatives:     {s['true_negatives']}")
        print(f"  False positives:     {s['false_positives']}")
        print(f"  False negatives:     {s['false_negatives']}")
        print(f"  Accuracy:            {s['accuracy']}%")
        print("=" * 40)

        print("\n  Per object breakdown:")
        print(f"  {'ID':<8} {'Truth':<12} {'Your Tag':<10} {'Result'}")
        print(f"  {'-'*40}")
        for h in self.history:
            tag = h['tag'] if h['tag'] else "—"
            print(f"  {h['obj_id']:<8} {h['truth']:<12} {tag:<10} {h['result']}")
        print()