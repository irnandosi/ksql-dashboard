from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

KSQLDB_URL = "http://ksqldb-route-confluent.apps.ocpdemo.imid.local:8088"

@app.get("/api/branch-summary")
async def get_summary():
    query = {
        "ksql": "SELECT * FROM branch_summary EMIT CHANGES LIMIT 20;",
        "streamsProperties": {}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{KSQLDB_URL}/query-stream", json=query)
        return response.text
