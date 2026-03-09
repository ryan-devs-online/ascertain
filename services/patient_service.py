from pathlib import Path

from anthropic import AsyncAnthropic
from sqlalchemy.ext.asyncio import AsyncSession

from db.note_repository import get_notes_by_patient_id
from db.patient_repository import get_patient_by_id
from models.summary import AISummary

PROMPT_PATH = Path(__file__).parent / "prompts" / "patient_summary_prompt.md"
PATIENT_SUMMARY_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")

client = AsyncAnthropic()


async def get_summary(session: AsyncSession, id: int):
    patient = await get_patient_by_id(session, id)

    notes = await get_notes_by_patient_id(session, id)

    if patient is None or notes is None:
        return None

    user_message = f"""
                    Patient Info:
                    {patient}

                    Notes:
                    {notes}
                    """

    response = await client.messages.parse(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=PATIENT_SUMMARY_PROMPT,
        messages=[{"role": "user", "content": user_message}],
        output_format=AISummary,
    )
    return response.parsed_output
