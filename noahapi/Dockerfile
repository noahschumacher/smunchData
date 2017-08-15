#to build, do:
#docker build -t noahapi .

#To run:
#docker run -it --rm -p 8080:8080 noahapi


FROM frolvlad/alpine-python3
COPY ./script.py /home/script.py

COPY ./prediction.py /home/prediction.py
COPY ./script.py /home/script.py
COPY ./timeInfo.py /home/timeInfo.py
COPY ./timePrediction.py /home/timePrediction.py


EXPOSE 8080
CMD ["python", "/home/script.py"]
