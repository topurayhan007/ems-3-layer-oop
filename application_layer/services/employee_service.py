# Bridge between CLI controllers and DB managers
from application_layer.classes.employee import Employee
from database_layer.db_setup import DatabaseManager
from database_layer.storage_managers.employee_db_manager import EmployeeDBManager

class EmployeeService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.employee_db_manager = EmployeeDBManager(db_manager)
    
    def add_employee(self, employee: Employee):
        result = self.employee_db_manager.add_employee(employee)
        return result
    
    def get_all_employee(self)-> list[Employee]:
        employees = self.employee_db_manager.get_all_employee()
        return employees
    
    def search_employee(self, input_text):
        employees = self.employee_db_manager.search_employee(input_text)
        return employees
    
    def delete_an_employee(self, employee_id):
        result = self.employee_db_manager.delete_an_employee(employee_id)
        return result

    def update_an_employee(self, employee: Employee):
        result = self.employee_db_manager.update_an_employee(employee)
        return result
