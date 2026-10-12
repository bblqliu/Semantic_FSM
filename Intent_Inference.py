class IntentInferenceModule:
    def __init__(self, modal_trajectory_baseline):
        self.baseline_trajectory = modal_trajectory_baseline

    def compute_structural_deviation(self, path_actions):
        """Measures deviation from normal user modal trajectories."""
        common_len = min(len(path_actions), len(self.baseline_trajectory))
        mismatches = sum(1 for i in range(common_len) if path_actions[i] != self.baseline_trajectory[i])
        deviation_score = mismatches / max(len(path_actions), 1)
        return deviation_score

    def score_exploit_intent(self, path_actions, request_history_logs):
        """Scores vulnerability paths based on structural features and actor telemetry."""
        deviation = self.compute_structural_deviation(path_actions)
        
        # Check for rapid polling or suspicious timing patterns in logs
        probing_indicator = 0.0
        if "/api/provisional-status" in str(request_history_logs):
            probing_indicator = 0.85 # High weight for systematic probing

        threat_score = (0.4 * deviation) + (0.6 * probing_indicator)
        
        return {
            "threat_score": round(threat_score, 2),
            "priority": "HIGH" if threat_score > 0.75 else "MEDIUM",
            "hypothesis": "Actor systematically probed boundary gap rather than standard workflow execution."
        }