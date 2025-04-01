from datetime import date

from beanie import Document


class Claim(Document):
    policy_number: str
    claim_type: str
    description: str
    date_of_incident: date
