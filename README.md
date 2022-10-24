# Voucher Selection

To run ETL and host the endpoint via FastAPI in docker container. 
1. Transform parquet format object to structured data to ingest into Postgres database.
2. Serve the endpoint for POST method, having voucher amount response for the customer's [request](sample.json).
3. Store the request to main table to update segments' values.
   - `{"vocher_amount": 10}`

### Prerequisites
1. Install [docker](https://docs.docker.com/get-docker/)

### Run data import with container and serve the endpoint

```shell
docker-compose up -d
```

Open another prompt and connect postgres via psql to check the result
```shell
docker exec -it postgres_db psql -h postgres_db -U user -d voucher_selection
```


### Test developement
```shell
pip install pytest
pytest
```

### Test endpoint
```shell
curl http://0.0.0.0:8080/voucher -X POST \
  -H "Content-type: application/json" \
  -d '{"customer_id": 555, "country_code": "Peru", "last_order_ts": "2022-05-03 00:00:00", \
  "first_order_ts": "2017-05-03 00:00:00", "total_orders": 35, "segment_name": "frequency_segment"}'
```
