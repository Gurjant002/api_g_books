import uvicorn

def main():
    """ Entry point """
    uvicorn.run(
        "app.application:get_app",
        host="0.0.0.0",
        port=8080,
        workers=2,
        log_level="debug",
        factory=True,
        reload=True,
    )

if __name__ == "__main__":
    main()