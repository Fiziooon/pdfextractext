from pydantic import BaseModel, Field, ConfigDict 
from datetime import datetime

class DocumentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    
    filename: str
    content: str
    checksum: str
    size_bytes: int
    created_at: datetime = Field(default_factory=datetime.now)