FROM python:3.8
RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
EXPOSE 5000
