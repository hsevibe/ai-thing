from fastapi import FastAPI
from dto import (
    Features,
    Data,
    ModelState,
    LearnResponse,
    PredictResponse,
    ClosestRequest,
    ClosestResponse,
)

router = FastAPI()
state = ModelState()


@router.post("/learn", response_model=LearnResponse)
def learn(data: Data) -> LearnResponse:
    with state.lock:
        dump = data.x.model_dump()
        y_pred = state.model.predict_one(dump)
        if y_pred is not None:
            state.metric.update(y_true=data.y, y_pred=y_pred)
        state.model.learn_one(dump, data.y)

    return LearnResponse(metric=state.metric.get())


@router.post("/predict", response_model=PredictResponse)
def predict(x: Features) -> PredictResponse:
    with state.lock:
        prediction = state.model.predict_one(x.model_dump())
        if prediction is None:
            prediction = 0.0

    return PredictResponse(
        prediction=prediction,
        current_metric=state.metric.get(),
    )


@router.post("/closest", response_model=ClosestResponse)
def closest(req: ClosestRequest) -> ClosestResponse:
    with state.lock:
        user_pred = state.model.predict_one(req.user.model_dump())
        if user_pred is None:
            user_pred = 0.0

        min_diff = float("inf")
        closest = None
        for person in req.people:
            pred = state.model.predict_one(person.model_dump())
            if pred is None:
                pred = 0.0
            diff = abs(pred - user_pred)
            if diff < min_diff:
                min_diff = diff
                closest = person

    return ClosestResponse(closest_person=closest)
