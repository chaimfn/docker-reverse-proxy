FROM python:3.9.17-slim.netfree

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install Flask 

# copy every content from the local file to the image
COPY server.py ./

EXPOSE 9090
# configure the container to run in an executed manner
ENTRYPOINT [ "python", "server.py" ]

