from fastapi import FastAPI
from routes import user, agent,script_gen,finalize_script



app = FastAPI(title="AI Mail Agent")
@app.get("/") 
def health():
   return {"status": "AI Mail Agent running"}

# Include the routers
app.include_router(user.router, tags=["User Data"])
app.include_router(
    script_gen.router,
    prefix="/script",
    tags=["Script Preparation"]
)
app.include_router(agent.router, prefix="/agent", tags=["Agent Operations"])
app.include_router(
    finalize_script.router,
    prefix="/finalScript",
    tags=["Finalize Script"]
)


