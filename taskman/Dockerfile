From python:3.8-slim
RUN pip install fastapi uvicorn
RUN pip install redis pymongo
RUN pip install requests
WORKDIR /src
COPY ./src /src
RUN chmod +x /src/start.sh
CMD ["/src/start.sh"]