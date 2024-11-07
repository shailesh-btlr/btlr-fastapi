from fastapi import FastAPI


app = FastAPI(
    servers=[
        dict(url="https://fast.aws.btlr.vip/gpt", description="Development"),
    ]
)


@app.get("/")
def hello():
    return "Hello World"
