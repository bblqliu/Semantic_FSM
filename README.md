# Semantic FSM

A lightweight Python project for modeling, verifying, and exploring covert logic flaws in stateful workflows using a semantic finite-state machine (FSM) approach.

This repository focuses on the gap between what a system implements (`delta_impl`) and what is actually authorized under semantic or regulatory preconditions (`delta_auth`). The project provides a simple framework for detecting boundary-condition vulnerabilities in workflow logic and scoring suspicious execution paths.

## What this project does

The core idea is to treat a workflow as an FSM with:

- implemented transitions
- authorized transitions
- precondition rules
- reachable execution paths

The project then searches for paths that are reachable in the implemented system but absent from the authorized model. This is useful for identifying "covert logic" or privilege-bypass behaviors that arise when a subsystem accepts a partially valid or semantically unsafe condition.

## Repository contents

- `SemanticFSM.py` — core semantic FSM model
- `EGovWorkflowSimulator.py` — e-government subsidy workflow simulator showing an exploit path
- `VulnerabilitySearchEngine.py` — bounded symbolic search for unauthorized state transitions
- `Intent_Inference.py` — scoring module for suspicious behavioral intent
- `generate_tier2_evaluation_dataset.py` — dataset generation utility for evaluation scenarios
- `Vulnerability_Engine-v2.py` — alternate/expanded version of the vulnerability search logic

## Core concepts

### SemanticFSM

The `SemanticFSM` class stores:

- `states`: all possible states
- `initial_states`: allowed entry states
- `accepting_states`: valid terminating states
- `delta_impl`: implemented transitions
- `delta_auth`: authorized transitions
- `preconditions`: precondition descriptions for each authorized action

It supports:

- `add_implemented_transition(source, action, target)`
- `add_authorized_transition(source, action, target, precondition_rule)`
- `is_valid_authorized_path(path)`

### VulnerabilitySearchEngine

The `VulnerabilitySearchEngine` explores reachable action sequences and checks whether those sequences are present in the implemented transitions but not the authorized transitions. It flags paths where the implementation accepts a transition that violates the regulatory precondition model.

### IntentInferenceModule

The `IntentInferenceModule` scores suspicious paths using:

- structural deviation from a normal trajectory baseline
- a probing indicator based on request patterns such as `/api/provisional-status`

This produces a simple threat score and priority label such as `HIGH` or `MEDIUM`.

### EGovWorkflowSimulator

The simulator models a subsidy-application workflow with states such as:

- `S0_APPLICATION_SUBMITTED`
- `S1_ID_VERIFICATION_PENDING`
- `S1_PROVISIONAL_VISIBLE`
- `S2_IDENTITY_VERIFIED`
- `S3_ELIGIBILITY_REVIEW`
- `F_SUBSIDY_APPROVED`

It demonstrates the boundary-gap exploit where a provisional status is treated as valid even when identity confirmation has not completed.

## Example workflow

The following example shows the semantic FSM structure used in the project:

```python
from SemanticFSM import SemanticFSM

states = {"S0", "S1", "S2", "S3", "F"}
initial = {"S0"}
accepting = {"F"}

fsm = SemanticFSM(states, initial, accepting)

fsm.add_implemented_transition("S0", "SUBMIT_APPLICATION", "S1")
fsm.add_implemented_transition("S1", "SUBSYSTEM_A_PROVISIONAL_CHECK", "S1_PROVISIONAL")
fsm.add_implemented_transition("S1_PROVISIONAL", "TRIGGER_ELIGIBILITY_REVIEW", "S3")

fsm.add_authorized_transition("S0", "SUBMIT_APPLICATION", "S1", "Application must be submitted")
fsm.add_authorized_transition("S1", "TRIGGER_ELIGIBILITY_REVIEW", "S3", "Identity must be confirmed")

path = {"start": "S0", "actions": ["SUBMIT_APPLICATION", "TRIGGER_ELIGIBILITY_REVIEW"]}
print(fsm.is_valid_authorized_path(path))
```

## Quick start

Run the simulator directly:

```bash
python EGovWorkflowSimulator.py
```

This demonstrates both the authorized execution flow and the vulnerable path triggered by a boundary-gap condition.

## Related logic

The project is designed to support a pipeline roughly like this:

1. Build the FSM model
2. Define implemented and authorized transitions
3. Search for paths that violate authorization rules
4. Rank suspicious paths by intent or deviation score
5. Review evidence chains for human auditing

## Example vulnerability pattern

A canonical issue in this project is a condition like:

- implemented workflow accepts a provisional state as if it were verified identity
- authorized model requires identity confirmation before eligibility review
- the missing rule is exposed as a covert logic flaw

This is exactly the type of logic gap the project is built to detect.

## Notes

This repository is a research-oriented and demonstration-style implementation rather than a production API package. It is best understood as a conceptual prototype for semantic verification and covert-logic flaw discovery in stateful systems.

For a deeper evaluation workflow, the dataset-generation scripts and search modules are designed to support empirical validation of suspicious path discovery.

## License

No explicit license file is currently included in the repository. If this project is meant for public distribution or reuse, adding a LICENSE file is recommended.

## Summary

This project demonstrates how a semantic FSM can be used to model:

- authorized state evolution
- implemented-but-unauthorized behavior
- vulnerability discovery through path analysis
- heuristic scoring for suspicious intent

It is especially relevant for audits of high-stakes decision workflows, including digital government systems and similar stateful processes with regulatory constraints.
