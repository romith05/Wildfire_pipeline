FROM python:3.10-slim
WORKDIR /wildfire
COPY model_api.py model.pkl ./
RUN pip install flask numpy scikit-learn
CMD ["python", "model_api.py"]
