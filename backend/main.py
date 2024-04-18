import uvicorn

if __name__ == "__main__":

    uvicorn.run("app.app:app", host="localhost", port=8000, log_level="debug",
                proxy_headers=True, reload=True)
