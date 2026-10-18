FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY crucible/ ./crucible/
COPY furnace/ ./furnace/
COPY settlement/ ./settlement/
COPY organs/ ./organs/
COPY synapses/ ./synapses/
COPY contract.json .
COPY kernel.py .

CMD ["python", "kernel.py"]
