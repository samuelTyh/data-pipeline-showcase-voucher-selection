# Voucher Selection

To run ETL and host the endpoint via FastAPI in docker container. 
1. Transform parquet format object to structured data to ingest into Postgres database.
2. Serve the endpoint for POST method, having voucher amount response for the customer's request.
3. Store the request to main table to update segments' values.

### Prerequisites
1. Install [docker](https://docs.docker.com/get-docker/)

### Run data import with container

```shell
docker-compose up -d
```

Open another prompt and connect postgres via psql to check the result
```shell
docker exec -it postgres_db psql -h postgres_db -U user -d voucher_selection
```