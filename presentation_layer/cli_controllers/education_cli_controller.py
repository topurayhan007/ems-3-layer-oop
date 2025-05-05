from application_layer.classes.education import EducationalDegree
from application_layer.services.input_validator_service import InputValidator
from application_layer.services.education_service import EducationService
from presentation_layer.table_printer import Printer

class EducationCliController:
    def __init__(self, education_service: EducationService):
        self.validator = InputValidator()
        self.printer = Printer()
        self.education_service = education_service

    def add_educational_degree(self, _employee_id):
        _degree_name = self.validator.get_input_and_validate(str, "Enter educational degree name: ")
        _institute_name = self.validator.get_input_and_validate(str, "Enter educational institute name: ")
        _major = self.validator.get_input_and_validate(str, "Enter educational major: ")
        _location = self.validator.get_input_and_validate(str, "Enter institute location: ")
        _gpa = self.validator.get_input_and_validate(float, "Enter GPA: ")
        _gpa_scale = self.validator.get_input_and_validate(float, "Enter GPA scale: ")
        _year_of_passing = self.validator.get_input_and_validate(str, "Enter year of passing (YYYY): ", self.validator.validate_year, "⚠️  Invalid year format")

        degree = EducationalDegree(None, _employee_id, _degree_name, _institute_name, _major, _location, _gpa, _gpa_scale, _year_of_passing)
        degree_id = self.education_service.add_degree(degree)

        if degree_id is not None:
            print("✅ Educational degree saved into database!")
        else:
            print("⚠️  Couldn't add to database!")

    def search_educational_degrees_of_an_employee(self, employee_id):
        degrees = self.education_service.search_degrees_of_an_employee(employee_id)
        if degrees is None or len(degrees) == 0:
            print("⚠️  No educational degrees found for the employee!")
            return None
        else: 
            print(self.printer.print_degree_table(degrees, "multiple"))
            return degrees


    def delete_educational_degree(self, degree_id):
        result = self.education_service.delete_a_degree_of_an_employee(degree_id)
        if result == 1:
            print("✅ Educational degree deleted from database!")
        else:
            print("⚠️  Couldn't delete from database!")

    def update_degree_fields_and_put_into_db(self, degree: EducationalDegree):
        item = degree
        print("=> Degree selected:")
        print(self.printer.print_degree_table(item, "single"))
        print("These are the fields you can update: ")
        print("Degree Name, Institute Name, Major, Location, GPA, GPA Scale, Year of Passing")
        fields = input("From the above fields type the fields you want to update separated by commas: ")
        fields = fields.split(",")

        for field in fields:
            if field.strip().lower() in "Degree Name".lower():
                item._degree_name  = self.validator.get_input_and_validate(str, "Enter new degree name: ")
            elif field.strip().lower() in "Institute Name".lower():
                item._institute_name  = self.validator.get_input_and_validate(str, "Enter new institute name: ")
            elif field.strip().lower() in "Major".lower():
                item._major  = self.validator.get_input_and_validate(str, "Enter new major: ")
            elif field.strip().lower() in "Location".lower():
                item._location  = self.validator.get_input_and_validate(str, "Enter new location: ")
            elif field.strip().lower() in "GPA".lower():
                item._gpa  = self.validator.get_input_and_validate(float, "Enter new gpa: ")
            elif field.strip().lower() in "GPA Scale".lower():
                item._gpa_scale  = self.validator.get_input_and_validate(float, "Enter new gpa scale: ")
            elif field.strip().lower() in "Year of Passing".lower():
                item._year_of_passing  = self.validator.get_input_and_validate(str, "Enter new year of passing (YYYY): ", self.validator.validate_year, "⚠️  Invalid year format")
            else:
                print("⚠️  You entered an invalid field, skipping this field...")

        result = self.education_service.update_a_degree_of_an_employee(item)
        if result == 1:
            print("✅ Education degree updated successfully!") 
        else:
            print("⚠️  Couldn't update degree, please try again!") 

    def update_educational_degree(self, degrees: list[EducationalDegree], degree_id):
        for item in degrees:
            if item._degree_id == degree_id:
                self.update_degree_fields_and_put_into_db(item)

