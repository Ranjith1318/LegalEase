from fastapi import APIRouter, HTTPException

from backend.schemas import DocumentRequest, DocumentResponse
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):

    try:
        generator = GeminiDocumentGenerator()

        document = generator.generate(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            instructions=request.instructions,
        )

        return DocumentResponse(document=document)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )