from fastapi import APIRouter, HTTPException
from models import CommentRequest, CommentResponse
from filter_ml import toxicity_filter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/api/comment", response_model=CommentResponse)
async def analyze_comment(request: CommentRequest):

    try:
        
        if not request.comment.strip():
            raise HTTPException(status_code=400, detail="Comment cannot be empty")
    
        analysis = toxicity_filter.analyze_comment(request.comment)
        
        allowed = analysis.label == "non-toxic"
        
        logger.info(f"Comment analyzed - Allowed: {allowed}, Label: {analysis.label}, Score: {analysis.score}")
        
        return CommentResponse(
            allowed=allowed,
            analysis=analysis
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing comment: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
