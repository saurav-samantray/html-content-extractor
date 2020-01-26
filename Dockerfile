FROM ubuntu:latest
LABEL maintainer="saurav"

# Install OpenJDK 8
RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Install Python
RUN \
    apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-virtualenv && \
    rm -rf /var/lib/apt/lists/*

# Install PySpark and Numpy
RUN \
    pip3 install --upgrade pip && \
    pip3 install numpy && \
    pip3 install pyspark

# Define working directory
# WORKDIR /data

ENV PATH="$PATH:/usr/bin/python3.6/"

ENV PYTHONPATH="$PYTHONPATH:/usr/bin/python3.6/"

ENV PYTHONIOENCODING="utf8"

ENV PYSPARK_PYTHON="/usr/bin/python3.6"

RUN chmod 777 /usr/bin/python3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"]