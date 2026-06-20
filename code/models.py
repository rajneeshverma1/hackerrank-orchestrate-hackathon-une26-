from pydantic import BaseModel, Field
from typing import List, Literal

class ClaimPrediction(BaseModel):
    """
    Pydantic schema representing the structured outputs required for 
    HackerRank Orchestrate damage claim verification. Matches the output 
    schema specification detailed in problem_statement.md.
    """
    evidence_standard_met: bool = Field(description="True if the image set is sufficient to evaluate the claim; otherwise false")

    evidence_standard_met_reason: str = Field(description="Short reason for the evidence decision")
    
    risk_flags: List[Literal[
        "none", "blurry_image", "cropped_or_obstructed", "low_light_or_glare", 
        "wrong_angle", "wrong_object", "wrong_object_part", "damage_not_visible", 
        "claim_mismatch", "possible_manipulation", "non_original_image", 
        "text_instruction_present", "user_history_risk", "manual_review_required"
    ]] = Field(description="List of applicable risk flags, or just ['none']")
    
    issue_type: Literal[
        "dent", "scratch", "crack", "glass_shatter", "broken_part", 
        "missing_part", "torn_packaging", "crushed_packaging", "water_damage", 
        "stain", "none", "unknown"
    ] = Field(description="Visible issue type")
    
    object_part: Literal[
        # Car
        "front_bumper", "rear_bumper", "door", "hood", "windshield", 
        "side_mirror", "headlight", "taillight", "fender", "quarter_panel", "body",
        # Laptop
        "screen", "keyboard", "trackpad", "hinge", "lid", "corner", "port", "base",
        # Package
        "box", "package_corner", "package_side", "seal", "label", "contents", "item",
        # General
        "unknown"
    ] = Field(description="Relevant object part visible with the issue")
    
    claim_status: Literal["supported", "contradicted", "not_enough_information"] = Field(description="Final decision")
    
    claim_status_justification: str = Field(description="Concise image-grounded explanation")
    
    supporting_image_ids: List[str] = Field(description="Image IDs supporting the decision, or ['none']")
    
    valid_image: bool = Field(description="True if the image set is usable for automated review; otherwise false")
    
    severity: Literal["none", "low", "medium", "high", "unknown"] = Field(description="Severity of the issue")
