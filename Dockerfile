FROM python:3.8

RUN mkdir -p voucher_selection
WORKDIR /voucher_selection
COPY . .
RUN pip install --ignore-installed -e .

ENV APP_SERVER_HOST=0.0.0.0
ENV APP_SERVER_PORT=8080

EXPOSE 8080
CMD ["python", "main.py"]