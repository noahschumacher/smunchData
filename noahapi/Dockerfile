
#to build, do:
#first, navigate to the repository of this very Docker file, then run
#docker build -t noahapi .

#To run:
#docker run -it --rm -p 8080:8080 noahapi


FROM python:3.5-alpine 

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk add --update --no-cache ca-certificates gcc g++ curl openblas-dev@community postgresql-dev libpq pkgconfig freetype-dev libpng-dev

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install psycopg2
RUN pip3 install pandas


COPY ./prediction.py /home/prediction.py
COPY ./script.py /home/script.py
COPY ./timeInfo.py /home/timeInfo.py
COPY ./timePrediction.py /home/timePrediction.py

EXPOSE 8080
CMD python "/home/script.py"

#Once done, try it out with http://192.168.99.100:8080/?dow=3&cID=22&rID=23&cOR=12&year=2017&mon=8&day=16
# or replace the IP address with the container IP