FROM python:alpine

ARG CHATETTE_DIR="/opt/chatette"

ARG WHL_DIR=${CHATETTE_DIR}/dist
COPY dist/*.whl ${WHL_DIR}/
RUN pip install ${WHL_DIR}/*.whl

ENTRYPOINT ["python", "-m", "chatette"]