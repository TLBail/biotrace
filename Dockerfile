FROM python:3.10
WORKDIR /app
COPY . .
RUN "python3 -m venv .venv"
RUN "source .venv/bin/activate"
RUN "pip install -r requirements.txt"
ENV PORT=5000
CMD ["pipenv", "run", "dev"]
EXPOSE 5000
