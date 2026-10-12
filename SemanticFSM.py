class SemanticFSM:
    def __init__(self, states, initial_states, accepting_states):
        self.states = set(states)
        self.initial_states = set(initial_states)
        self.accepting_states = set(accepting_states)
        self.delta_impl = {}  # Implemented transitions: (state, action) -> next_state
        self.delta_auth = {}  # Authorized transitions governed by preconditions Φ(σ)
        self.preconditions = {} # (state, action) -> precondition description

    def add_implemented_transition(self, source, action, target):
        self.delta_impl[(source, action)] = target

    def add_authorized_transition(self, source, action, target, precondition_rule):
        self.delta_auth[(source, action)] = target
        self.preconditions[(source, action)] = precondition_rule

    def is_valid_authorized_path(self, path):
        """Verifies whether a path respects regulatory preconditions Φ(σ)."""
        current_state = path.get("start")
        for action in path.get("actions", []):
            if (current_state, action) not in self.delta_auth:
                return False
            current_state = self.delta_auth[(current_state, action)]
        return current_state in self.accepting_states