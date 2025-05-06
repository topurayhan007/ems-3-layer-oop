from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
from dotenv import load_dotenv

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_root)

from database_layer.db_setup import DatabaseManager
from application_layer.services.employee_service import EmployeeService
from application_layer.services.education_service import EducationService
from application_layer.services.experience_service import ExperienceService
from application_layer.classes.employee import Employee

PORT = 8000
load_dotenv()

config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'raise_on_warnings': True
}

db_manager = DatabaseManager(config)
employee_service = EmployeeService(db_manager)
education_service = EducationService(db_manager)
experience_service = ExperienceService(db_manager)

class Server(BaseHTTPRequestHandler):
    def _send_response(self, status_code, status_msg, data):
        self.send_response(status_code, status_msg)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        try:
            # http://localhost:8000/api
            if self.path == "/":
                self._send_response(200, "OK", "Server is running....")
            
            # employee APIs
            # http://localhost:8000/api/employees
            elif self.path == "/api/employees":
                employees = employee_service.get_all_employee()
                employee_dict = [employee.__dict__ for employee in employees]
                self._send_response(200, "OK", {"employees": employee_dict})
            
            # http://localhost:8000/api/employees?q={input}
            elif self.path.startswith("/api/employees?q="):
                search_text = self.path.split("?q=")[1]
                employees = employee_service.search_employee(search_text)
                employee_dict = [employee.__dict__ for employee in employees]
                self._send_response(200, "OK", {"employees": employee_dict})
                
            else:
                self._send_response(404, "Not Found", {"error": "Invalid route"})

        except Exception as e:
            self._send_response(500, "Server Error", {"error": str(e)})

    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        
        if content_length:
            input_json = self.rfile.read(content_length).decode('utf-8')
            input_data = json.loads(input_json)
        else:
            input_data = None
        
        try:
            if self.path == "/api/employees":
                employee = Employee(
                    input_data["_employee_id"],
                    input_data["_name"],
                    input_data["_date_of_birth"],
                    input_data["_nid"],
                    input_data["_email"],
                    input_data["_phone_no"],
                    input_data["_gender"],
                    input_data["_father_name"],
                    input_data["_mother_name"],
                    input_data["_marital_status"],
                    input_data["_dept"],
                    input_data["_designation"],
                    input_data["_nationality"],
                    input_data["_joining_date"],
                    input_data["_present_address"],
                    input_data["_permanent_address"]
                )

                result = employee_service.add_employee(employee)
                self._send_response(201, "Created", {"result": result})
            
            elif self.path == "/api/degrees":
                result = education_service.add_degree(input_data)
                self._send_response(201, "Created", {"result": result})

            else:
                self._send_response(404, "Not Found", {"error": "Invalid route"})

        except Exception as e:
            self._send_response(500, "Server Error", {"error": str(e)})
        
        
    
    def do_DELETE(self):
        raise NotImplementedError

def run(server_class=HTTPServer, handler_class=Server):
    server_address = ('', PORT)
    print(f"Server running at http://localhost:{PORT}")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
