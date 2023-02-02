FROM python:3.10

WORKDIR /

RUN mkdir -p ./image_folder/predicted_images

COPY ./config ./config	
COPY ./model ./model
COPY ./utilits ./utilits
COPY ./yolov5 ./yolov5
COPY ./main.py ./main.py

RUN apt-get update && apt-get install libgl1 -y

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt


CMD ["python", "./main.py"]