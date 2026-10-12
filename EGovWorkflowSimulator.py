class EGovWorkflowSimulator:
    def __init__(self, workflow_name="Subsidy Application"):
        self.workflow_name = workflow_name
        self.current_state = "S0_APPLICATION_SUBMITTED"
        self.identity_confirmed = False
        self.provisional_flag_exposed = False
        self.audit_log_history = []

    def reset(self):
        self.current_state = "S0_APPLICATION_SUBMITTED"
        self.identity_confirmed = False
        self.provisional_flag_exposed = False
        self.audit_log_history = []

    def execute_action(self, action_name, payload=None):
        self.audit_log_history.append({"action": action_name, "state_before": self.current_state})

        if action_name == "SUBMIT_APPLICATION":
            self.current_state = "S1_ID_VERIFICATION_PENDING"

        elif action_name == "SUBSYSTEM_A_PROVISIONAL_CHECK":
            # Exposes provisional flag for internal caseworker UI (Boundary Gap Origin)
            self.provisional_flag_exposed = True
            self.current_state = "S1_PROVISIONAL_VISIBLE"

        elif action_name == "SUBSYSTEM_A_CONFIRM_IDENTITY":
            self.identity_confirmed = True
            self.current_state = "S2_IDENTITY_VERIFIED"

        elif action_name == "TRIGGER_ELIGIBILITY_REVIEW":
            # Subsystem B evaluation logic
            use_bypass = payload and payload.get("exploit_provisional", False)

            if use_bypass and self.provisional_flag_exposed and not self.identity_confirmed:
                # Covert logic vulnerability triggered!
                self.current_state = "S3_ELIGIBILITY_REVIEW"
                return {
                    "status": "VULNERABILITY_TRIGGERED",
                    "message": "Boundary assumption gap exploited: Subsystem B accepted provisional status as valid.",
                    .state: self.current_state
                }
            elif self.identity_confirmed:
                self.current_state = "S3_ELIGIBILITY_REVIEW"
                return {
                    "status": "AUTHORIZED_SUCCESS",
                    "message": "Precondition Φ(σ) satisfied: Confirmed identity record validated.",
                    "state": self.current_state
                }
            else:
                return {
                    "status": "REJECTED_PRECONDITION_VIOLATED",
                    "message": "Transition blocked: Identity not fully confirmed.",
                    "state": self.current_state
                }

        elif action_name == "FINAL_APPROVAL" and self.current_state == "S3_ELIGIBILITY_REVIEW":
            self.current_state = "F_SUBSIDY_APPROVED"
            return {"status": "SUCCESS", "state": self.current_state}

        return {"status": "INVALID_TRANSITION", "state": self.current_state}

# Example execution testing both authorized and vulnerable paths
if __name__ == "__main__":
    sim = EGovWorkflowSimulator()
    print("--- Testing Vulnerable Path (Exploiting Boundary Gap) ---")
    sim.execute_action("SUBMIT_APPLICATION")
    sim.execute_action("SUBSYSTEM_A_PROVISIONAL_CHECK")
    result = sim.execute_action("TRIGGER_ELIGIBILITY_REVIEW", payload={"exploit_provisional": True})
    print(result)