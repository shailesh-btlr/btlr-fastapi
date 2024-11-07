# btlr-fastapi

`btlr-fastapi` is a FastAPI project organized under a root directory assumed to be named `btlr-fastapi`.

## Installation
- `pip install -r requirements.txt`

## Run server
- `cd app`
- `uvicorn main:app`

## Test AWS Codepipeline build locally
```
DOCKER_BUILDKIT=1 ./codebuild_build.sh -d -i public.ecr.aws/codebuild/amazonlinux2-x86_64-standard:4.0 -a ./out
```