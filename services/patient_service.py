from pathlib import Path

from anthropic import Anthropic
from sqlalchemy.orm import Session

from db.note_repository import get_notes_by_patient_id
from db.patient_repository import get_patient_by_id
from models.summary import AISummary

PROMPT_PATH = Path(__file__).parent / "prompts" / "patient_summary_prompt.md"
PATIENT_SUMMARY_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")

client = Anthropic()


def get_summary(session: Session, id: int):
    patient = get_patient_by_id(session, id)

    notes = get_notes_by_patient_id(session, id)

    if patient is None or notes is None:
        return None

    user_message = f"""
                    Patient Info:
                    {patient}

                    Notes:
                    {notes}
                    """

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=PATIENT_SUMMARY_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    block = response.content[0]
    if block.type != "text":
        raise ValueError("Unexpected response from Claude")

    text = (
        block.text.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )

    return AISummary.model_validate_json(text)
