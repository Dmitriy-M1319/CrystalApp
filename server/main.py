from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def index():
    return {'success': True}


