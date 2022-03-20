FROM python:3.9.9

EXPOSE 80

COPY . .

RUN pip install fastapi uvicorn aiofiles fastapi-async-sqlalchemy python-multipart sqlalchemy

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]