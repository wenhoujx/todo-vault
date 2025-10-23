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
curl -X POST https://mxvmaaocp7lsxttykgkn5w4qyy0mgcqd.lambda-url.us-east-1.on.aws/todos \
  -H "Content-Type: application/json" \
  -d '{"description": "buy milk"}'

curl https://mxvmaaocp7lsxttykgkn5w4qyy0mgcqd.lambda-url.us-east-1.on.aws/todos
curl -X DELETE https://mxvmaaocp7lsxttykgkn5w4qyy0mgcqd.lambda-url.us-east-1.on.aws/todos/<id>

```

```sh
docker run -d -p 8080:8080 $(docker build -q .)
```

## deploy BE via cdk

```sh
make build-fe 
make deploy 
```
