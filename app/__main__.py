import uvicorn

def main():
    """ Entry point """
    uvicorn.run(
        "app.application:get_app",
        workers=1,
        log_level="debug",
        factory=True,
        reload=True,
    )

if __name__ == "__main__":
    main()