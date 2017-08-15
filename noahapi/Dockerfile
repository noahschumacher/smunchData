#to build, do:
#docker build -t noahapi .

#To run:
#docker run -it --rm -p 80:80 noahapi


FROM jfloff/alpine-python:3.4-slim
COPY ./script.py /home/script.py


EXPOSE 8080
CMD ["python", "/home/script.py"]