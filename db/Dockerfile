FROM python:3.10
WORKDIR /wildfire
COPY dbserve.py CEC.parquet ./
RUN pip install duckdb
CMD ["python", "dbserve.py"]
