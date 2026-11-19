import json
from os.path import dirname, abspath, join
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


current_dir = dirname(abspath(__file__))
wellknown_path = join(current_dir, ".well-known")
historical_data = join(current_dir, "weather.json")

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=wellknown_path), name="static")


# load historical json data and serialize it:
with open(historical_data, "r") as f:
    data = json.load(f)

@app.get('/')
def root():
    """
    Allows to open the API documentation in the browser directly instead of
    requiring to open the /docs path.
    """
    return RedirectResponse(url='/docs', status_code=301)


@app.get('/countries')
def countries():
    return list(data.keys())


@app.get('/countries/{country}/{city}/{month}')
def monthly_average(country: str, city: str, month: str):
    return data[country][city][month]

@app.get('/regions/{region}')
def cities(region: str):
    if region not in data:
        raise HTTPException(status_code=404, detail="Region not found")
    return list(data[region].keys())


@app.get('/regions/{region}/{city}/{month}')
def region_monthly_average(region: str, city: str, month: str):
    if region not in data:
        raise HTTPException(status_code=404, detail="Region not found")
    if city not in data[region]:
        raise HTTPException(status_code=404, detail="City not found")
    if month not in data[region][city]:
        raise HTTPException(status_code=404, detail="Month not found")
    return data[region][city][month]

# Generate the OpenAPI schema:
openapi_schema = app.openapi()
with open(join(wellknown_path, "openapi.json"), "w") as f:
    json.dump(openapi_schema, f)