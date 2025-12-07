import math
import numbers
from river import compose, preprocessing, forest, metrics


def transformer(x_: dict):
    x = x_.copy()
    x["body_index"] = x["weight"] / (x["height"] ** 2)
    x["bio_length_log1p"] = math.log1p(x["bio_length"])
    x["age_log"] = math.log(x["age"])

    lat_rad = math.radians(x["lat"])
    lon_rad = math.radians(x["lon"])

    x["coord_x"] = math.cos(lat_rad) * math.cos(lon_rad)
    x["coord_y"] = math.cos(lat_rad) * math.sin(lon_rad)
    x["coord_z"] = math.sin(lat_rad)

    x.pop("weight")
    x.pop("height")
    x.pop("bio_length")
    x.pop("lat")
    x.pop("lon")
    x.pop("age")
    return x


numeric_transformer = compose.Pipeline(
    compose.SelectType(numbers.Number),
    preprocessing.StandardScaler(),
)

categorical_transformer = compose.Pipeline(
    compose.Select("sex", "sport", "experience_level"),
    preprocessing.OneHotEncoder(),
)

amfc_forest = forest.AMFRegressor()

model = compose.Pipeline(
    compose.FuncTransformer(transformer),
    compose.TransformerUnion(
        ("num", numeric_transformer),
        ("cat", categorical_transformer),
    ),
    amfc_forest,
)

metric = metrics.MAE()
