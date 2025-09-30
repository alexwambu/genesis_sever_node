from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

app = FastAPI()

class GenesisRequest(BaseModel):
    chainId: int
    signer: str
    balance: str = "1000000000000000000000"
    gasLimit: str = "8000000"

@app.post("/genesis")
def generate_genesis(req: GenesisRequest):
    signer = req.signer.lower().replace("0x", "")
    if len(signer) != 40:
        return {"error": "Signer must be a 20-byte hex string (40 chars)"}

    extradata = "0x" + "00" * 32 + signer + "00" * 65

    genesis = {
        "config": {
            "chainId": req.chainId,
            "clique": {"period": 5, "epoch": 30000},
            "homesteadBlock": 0,
            "eip150Block": 0,
            "eip155Block": 0,
            "eip158Block": 0,
            "byzantiumBlock": 0,
            "constantinopleBlock": 0,
            "petersburgBlock": 0,
            "istanbulBlock": 0,
            "berlinBlock": 0,
            "londonBlock": 0
        },
        "alloc": {req.signer: {"balance": req.balance}},
        "coinbase": "0x0000000000000000000000000000000000000000",
        "difficulty": "1",
        "extraData": extradata,
        "gasLimit": req.gasLimit,
        "timestamp": "0x00"
    }

    # Save to file so Geth can fetch
    with open("genesis.json", "w") as f:
        json.dump(genesis, f, indent=2)

    return genesis

@app.get("/genesis.json")
def serve_genesis():
    return FileResponse("genesis.json", media_type="application/json")

@app.get("/health")
def health():
    return {"status": "ok", "service": "GBTNetwork Genesis Server"}
