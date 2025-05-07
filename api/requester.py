# Do API requests
import http.client
import json

class Requester():
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



