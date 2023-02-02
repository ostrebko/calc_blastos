FROM python:3.10

WORKDIR /

COPY ./config ./config	
COPY ./image_folder ./image_folder
RUN ["mkdir", "./predicted_images"]
COPY ./model ./model
COPY ./utilits ./utilits
COPY ./requirements.txt ./requirements.txt
COPY ./main.py ./main.py
COPY ./yolov5 ./yolov5

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "./main.py"]