FROM python:3.10
COPY . .
RUN pip install -r requirements.txt
ENV PORT=5000
WORKDIR /app
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000" , "server:app"]
