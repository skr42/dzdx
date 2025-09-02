# Profanity and Abuse Filtering API

A FastAPI-based REST API that uses models to detect toxic and abusive content in text comments.


## Project Structure

```
DZDX/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── routes.py        # API route definitions
│   ├── models.py        # Pydantic request/response models
│   └── filter_ml.py     # ML-based filtering logic
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   or
   pip install fastapi "uvicorn[standard]" transformers torch pydantic python-multipart

   ```

## Usage

### Start the server:
```bash
cd app
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

### API Endpoints

#### POST `/api/comment`
Analyze a comment for toxicity.

**Request:**
```json
{
  "comment": "comment here"
}
```

**Response:**
```json
{
  "allowed": true,
  "analysis": {
    "label": "non-toxic",
    "score": 0.95
  }
}
```

**Response Fields:**
- `allowed`: Boolean indicating if comment is allowed (false if toxic score > 0.7)
- `analysis.label`: Classification result ("toxic" or "non-toxic")
- `analysis.score`: Confidence score between 0.0 and 1.0


## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API
Visit http://localhost:8000/docs to test the API interactively using Swagger UI.

## Dependencies

- **FastAPI:** Web framework
- **Uvicorn:** ASGI server
- **Transformers:** HuggingFace ML models
- **PyTorch:** ML framework
- **Pydantic:** Data validation
