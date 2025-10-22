# deploy to AWS

```sh
# run BE 
uv run flask --app ./server/app.py run  --host=0.0.0.0 --port=8080
# run FE 
uv run npm run dev
# go to http://localhost:5002/


```

```sh
# example curl 
curl -XPOST localhost:8080/api/todos -H 'content-type: application/json' -d '{"title": "foo"}'
curl -XPOST https://stcc0splr5.execute-api.us-east-1.amazonaws.com/prod/api/todos  -H 'content-type: application/json' -d '{"title": "foo"}'
curl -XPOST https://m5wd3zbs25oorfj53afzmnwhwi0mnuhg.lambda-url.us-east-1.on.aws/api/todos  -H 'content-type: application/json' -d '{"title": "foo"}'
```

```sh
docker run -d -p 8080:8080 $(docker build -q .)
```

## deploy BE via cdk

```sh
uv pip compile pyproject.toml -o requirements.txt

```
