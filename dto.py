from pydantic import BaseModel
from model import model, metric
import threading


# our features
class Features(BaseModel):
    age: int
    sex: int
    weight: float
    height: float
    experience_level: int
    bio_length: int
    sport: str
    lat: float
    lon: float


class Data(BaseModel):
    x: Features
    y: float


class LearnResponse(BaseModel):
    metric: float


class PredictResponse(BaseModel):
    prediction: float
    current_metric: float


class ClosestRequest(BaseModel):
    user: Features
    people: list[Features]


class ClosestResponse(BaseModel):
    closest_person: Features


class ModelState:
    def __init__(self):
        self.model = model
        self.metric = metric
        self.lock = threading.Lock()
