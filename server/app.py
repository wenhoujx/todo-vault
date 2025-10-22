import json
import boto3
from uuid import uuid4
import os 

dynamodb = boto3.resource("dynamodb")
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]

    if method == "GET" and path == "/todos":
        return list_todos()
    elif method == "POST" and path == "/todos":
        return add_todo(event)
    elif method == "DELETE" and path.startswith("/todos/"):
        todo_id = path.split("/")[-1]
        return delete_todo(todo_id)
    else:
        return response(404, {"error": "Not found"})

def add_todo(event):
    body = json.loads(event.get("body", "{}"))
    description = body.get("description")
    if not description:
        return response(400, {"error": 'Missing "description"'})

    todo = {"id": str(uuid4()), "description": description, "done": False}
    table.put_item(Item=todo)
    return response(201, todo)

def list_todos():
    res = table.scan()
    return response(200, res.get("Items", []))

def delete_todo(todo_id):
    table.delete_item(Key={"id": todo_id})
    return {"statusCode": 204}

def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
