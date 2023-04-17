FROM python:3.10-alpine

RUN apk update
RUN apk add gcc musl-dev linux-headers python3-dev

# Copy requirements and all other files to image /app
COPY ./requirements.txt /app/requirements.txt
COPY . /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]
CMD ["app.py" ]