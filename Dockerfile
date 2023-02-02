FROM python:3.10

WORKDIR /

RUN mkdir -p ./image_folder/predicted_images

COPY ./config ./config	
COPY ./model ./model
COPY ./utilits ./utilits
COPY ./main.py ./main.py
COPY ./yolov5 ./yolov5

RUN apt-get update && apt-get install libgl1 -y

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt


CMD ["python", "./main.py"]