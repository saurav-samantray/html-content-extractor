FROM openjdk:8-jre-alpine

RUN apk add --no-cache python3 bash\
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

COPY . /app

WORKDIR /app

#install dependencies for requirement installation, once done remove the dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libxml2-dev libxslt-dev linux-headers\
    && pip3 install --upgrade pip \
    && pip3 install pypandoc \
	&& python3 -m pip install lxml \
    && pip3 install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk del .build-deps


# Define working directory
# WORKDIR /data

ENV PATH="$PATH:/usr/bin/python3.6/"

ENV PYTHONPATH="$PYTHONPATH:/usr/bin/python3.6/"

ENV PYTHONIOENCODING="utf8"

ENV PYSPARK_PYTHON="/usr/bin/python3.6"

RUN chmod 777 /usr/bin/python3.6

ENTRYPOINT ["python3"]

CMD ["app.py"]