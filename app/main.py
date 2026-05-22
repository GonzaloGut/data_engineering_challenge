from fastapi import FastAPI

app = FastAPI(
    title="Data Engineering Challenge API",
    version="1.0.0"
)

@app.get("/")
def healtcheck():
    return {"status": "ok", "service": "Data Engineering Challenge API"}
