import ssl
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date, datetime
import urllib3
from requests.adapters import HTTPAdapter



class StoreBusinessNumberModel(BaseModel):
    uuid: Optional[str] = None  # INT
    
class UUIDModel(BaseModel):
    store_business_number: Optional[str] = None  # INT