from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.dns import analyze_dns_health
from app.models import save_analysis_result, get_analysis_result
from uuid import uuid4
import json

app = FastAPI()

class DomainRequest(BaseModel):
    domain: str

class AnalysisResponse(BaseModel):
    analysis_id: str

class AnalysisResultResponse(BaseModel):
    domain: str
    result: dict
    timestamp: str

@app.post("/start-analysis", response_model=AnalysisResponse)
async def start_analysis(request: DomainRequest):
    domain = request.domain
    try:
        # Analyze DNS health (either using Go tool or Python alternative)
        result = analyze_dns_health(domain)

        # Save the result in the database
        analysis_id = str(uuid4())
        save_analysis_result(analysis_id, domain, result)
        
        return AnalysisResponse(analysis_id=analysis_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-analysis/{analysis_id}", response_model=AnalysisResultResponse)
async def get_analysis(analysis_id: str):
    # Retrieve the analysis result from the database
    result = get_analysis_result(analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return result

@app.get("/")
def read_root():
    return {"message": "Welcome to DNS Health API!"}
