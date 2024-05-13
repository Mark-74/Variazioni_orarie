FROM python:3
WORKDIR /app
COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]
