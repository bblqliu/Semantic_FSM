import json
import os

def generate_tier2_evaluation_dataset():
    departments = [
        "Department of Civil Affairs",
        "Enterprise Registration Bureau",
        "Subsidies & Grants Administration Office",
        "Residency & Household Status Division",
        "Digital Public Services Bureau"
    ]
    
    procedures = [
        "Subsidy Application",
        "Business License Renewal",
        "Residency Status Transfer",
        "Disability Allowance Registration",
        "SME Digital Transformation Grant"
    ]

    dataset = []

    for i in range(1, 16):
        dept = departments[i % len(departments)]
        proc = procedures[i % len(procedures)]
        
        record = {
            "document_id": f"GOV-GUIDE-{i:03d}",
            "title": f"Standard Operating Procedure for {proc} (Version {1.0 + (i % 3)*0.1:.1f})",
            "issuing_agency": dept,
            "document_type": "Public Service Guide & Administrative Manual",
            "regulatory_text": (
                f"Section {i}.1: The administration of {proc} requires strict adherence to workflow milestones. "
                f"Applications must be submitted via the portal, followed by mandatory identity verification under Subsystem A. "
                f"No eligibility review under Subsystem B may commence unless a confirmed identity verification record "
                f"timestamped after the applicant's latest profile update is received. Provisional statuses are strictly "
                f"reserved for internal caseworker visibility and must never be interpreted as final approval prerequisites."
            ),
            "ground_truth_fsm": {
                "states": [
                    "S0_Application_Submitted",
                    "S1_Identity_Verification_Pending",
                    "S2_Identity_Verified",
                    "S3_Eligibility_Review",
                    "F_Approved"
                ],
                "initial_state": "S0_Application_Submitted",
                "accepting_state": "F_Approved",
                "authorized_preconditions": {
                    "S2_to_S3": "Confirmed identity verification record timestamped after latest profile update."
                }
            }
        }
        dataset.append(record)

    output_filename = "tier2_government_guides_dataset.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"Successfully generated dataset file '{output_filename}' containing {len(dataset)} government service guides for Tier 2 evaluation.")

if __name__ == "__main__":
    generate_tier2_evaluation_dataset()