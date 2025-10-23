import json
import boto3
from uuid import uuid4
import os 

dynamodb = boto3.resource("dynamodb")
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]
    if method == 'OPTIONS': 
        return response(200, {})
    elif method == "GET" and path == "/todos":
        return list_todos()
    elif method == "POST" and path == "/todos":
        return add_todo(event)
    elif method == "PUT" and path.startswith("/todos/"): 
        todo_id = path.split("/")[-1]
        return toggle_todo(todo_id)
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

def toggle_todo(todo_id): 
    if not todo_id:
        return response(400, {"error": 'Missing "id" in path'})

    # Retrieve current todo
    item = table.get_item(Key={"id": todo_id}).get("Item")
    if not item:
        return response(404, {"error": "Todo not found"})

    # Flip the "done" flag
    new_done = not item.get("done", False)
    table.update_item(
        Key={"id": todo_id},
        UpdateExpression="SET done = :d",
        ExpressionAttributeValues={":d": new_done},
        ReturnValues="ALL_NEW"
    )

    # Return updated todo
    updated = table.get_item(Key={"id": todo_id}).get("Item")
    return response(200, updated)
    
def list_todos():
    res = table.scan()
    return response(200, res.get("Items", []))

def delete_todo(todo_id):
    table.delete_item(Key={"id": todo_id})
    return response(204, {})

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,PUT,POST,OPTIONS,DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body)
    }
