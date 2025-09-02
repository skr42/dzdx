import logging
from typing import Dict, Any
from transformers import pipeline
from models import AnalysisResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ToxicityFilter:
    def __init__(self, model_name: str = "unitary/toxic-bert"):
        self.model_name = model_name
        self.classifier = None
        self.threshold = 0.7
        self._load_model()
    
    def _load_model(self):
        try:
            logger.info(f"Loading toxicity model: {self.model_name}")
            self.classifier = pipeline(
                "text-classification",
                model=self.model_name,
                return_all_scores=True
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {str(e)}")
            # Fallback to a more commonly available model
            try:
                logger.info("Attempting fallback to martin-ha/toxic-bert")
                self.classifier = pipeline(
                    "text-classification",
                    model="martin-ha/toxic-bert",
                    return_all_scores=True
                )
                logger.info("Fallback model loaded successfully")
            except Exception as fallback_error:
                logger.error(f"Fallback model also failed: {str(fallback_error)}")
                raise RuntimeError("Unable to load any toxicity classification model")
    
    def analyze_comment(self, comment: str) -> AnalysisResult:
        if not self.classifier:
            raise RuntimeError("Model not loaded")
        
        if not comment or not comment.strip():
            return AnalysisResult(label="non-toxic", score=0.0)
        
        try:
            # Get predictions from the model
            results = self.classifier(comment.strip())
            
            # Handle different model output formats
            toxic_score = self._extract_toxic_score(results)
            
            # Determine label based on score and threshold
            is_toxic = toxic_score > self.threshold
            label = "toxic" if is_toxic else "non-toxic"
            
            logger.info(f"Comment analysis - Label: {label}, Score: {toxic_score:.3f}")
            
            return AnalysisResult(
                label=label,
                score=round(toxic_score, 4)
            )
            
        except Exception as e:
            logger.error(f"Error analyzing comment: {str(e)}")
            # Return safe default in case of error
            return AnalysisResult(label="non-toxic", score=0.0)
    
    def _extract_toxic_score(self, results) -> float:
        """
        Extract toxic score from model results, handling different output formats.
        
        Args:
            results: Raw model output
            
        Returns:
            float: Toxicity score between 0 and 1
        """
        if isinstance(results, list) and len(results) > 0:
            # Handle list of predictions
            predictions = results[0] if isinstance(results[0], list) else results
            
            # Look for toxic/toxicity labels
            for pred in predictions:
                label = pred.get('label', '').lower()
                if 'toxic' in label and 'non' not in label:
                    return pred.get('score', 0.0)
            
            # If no toxic label found, assume first prediction is toxic score
            if predictions:
                return predictions[0].get('score', 0.0)
        
        return 0.0
    
    def is_comment_allowed(self, comment: str) -> bool:
        analysis = self.analyze_comment(comment)
        return analysis.label == "non-toxic"

# Global instance
toxicity_filter = ToxicityFilter()
