# Do API requests
import http.client
import json

class Request():
    @staticmethod
    def request(http_method, end_point, body=None):
        headers = {"Content-type": "application/json"}
        conn = http.client.HTTPConnection("localhost", 8000)
        if body:
            body = json.dumps(body.__dict__)
        
        try:
            conn.request(http_method, end_point, body, headers)
            response = conn.getresponse()
            parsed_data = response.read().decode('utf-8')
            data = json.loads(parsed_data)
            return data
        except Exception as e:
            print("error: ", e)
            return e
        finally:
            conn.close()



"""
import http.client, urllib.parse

params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})

headers = {"Content-type": "application/x-www-form-urlencoded",

           "Accept": "text/plain"}

conn = http.client.HTTPConnection("bugs.python.org")

conn.request("POST", "", params, headers)

response = conn.getresponse()

print(response.status, response.reason)
302 Found

data = response.read()

data
b'Redirecting to <a href="https://bugs.python.org/issue12524">https://bugs.python.org/issue12524</a>'

conn.close()

-----
import http.client

BODY = "***filecontents***"

conn = http.client.HTTPConnection("localhost", 8080)

conn.request("PUT", "/file", BODY)

response = conn.getresponse()

print(response.status, response.reason)
-----

import http.client
import json
import urllib.parse
from typing import Optional, Union, Dict, Any

def request(
    method: str,
    host: str,
    endpoint: str,
    port: int = 8000,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[Dict[str, Any], str]] = None,
    ssl: bool = False
) -> Dict[str, Any]:

    # Initialize default headers if none provided
    if headers is None:
        headers = {}
    
    # Add Content-Type header for requests with body
    if body and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    
    # Encode query parameters if provided
    if params:
        endpoint += "?" + urllib.parse.urlencode(params)
    
    # Convert body to JSON string if it's a dict
    if isinstance(body, dict):
        body = json.dumps(body)
    
    # Create connection based on SSL flag
    ConnectionClass = http.client.HTTPSConnection if ssl else http.client.HTTPConnection
    conn = ConnectionClass(host, port)
    
    try:
        # Make the request
        conn.request(method, endpoint, body=body, headers=headers)
        
        # Get response
        response = conn.getresponse()
        
        # Read and parse response data
        response_data = response.read().decode('utf-8')
        try:
            parsed_data = json.loads(response_data) if response_data else None
        except json.JSONDecodeError:
            parsed_data = response_data
        
        # Prepare result dictionary
        result = {
            "status": response.status,
            "reason": response.reason,
            "headers": dict(response.getheaders()),
            "data": parsed_data
        }
        
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "status": 500,
            "reason": "Internal Client Error"
        }
    finally:
        conn.close()


# Example usage:

if __name__ == "__main__":
    # GET request example
    print("GET /api/employees:")
    response = request("GET", "localhost", "/api/employees")
    print(json.dumps(response, indent=2))
    
    # POST request example
    print("\nPOST /api/employees:")
    new_employee = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        # ... other employee fields
    }
    response = request("POST", "localhost", "/api/employees", body=new_employee)
    print(json.dumps(response, indent=2))
    
    # PUT request example
    print("\nPUT /api/employees/1:")
    updated_employee = {
        "name": "John Doe Updated",
        "email": "john.updated@example.com",
        # ... other updated fields
    }
    response = request("PUT", "localhost", "/api/employees/1", body=updated_employee)
    print(json.dumps(response, indent=2))
    
    # DELETE request example
    print("\nDELETE /api/employees/1:")
    response = request("DELETE", "localhost", "/api/employees/1")
    print(json.dumps(response, indent=2))
    
    # Request with parameters example
    print("\nGET /api/employees with search:")
    response = request(
        "GET", 
        "localhost", 
        "/api/employees", 
        params={"q": "John"}
    )
    print(json.dumps(response, indent=2))
"""