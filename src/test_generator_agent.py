import google.generativeai as genai
from config import GOOGLE_AI_API_KEY, DEFAULT_MODEL


class TestGeneratorAgent:
    """
    AI Agent for generating comprehensive API test cases
    """

    def __init__(self):
        print("TestGeneratorAgent initialized!")
        self.agent_name = "Smart API Test Case Generator"
        self.supported_methods = ["GET", "POST", "PUT", "DELETE"]

        # Configure AI tool
        genai.configure(api_key=GOOGLE_AI_API_KEY)
        self.model = genai.GenerativeModel(DEFAULT_MODEL)
        print("AI Connection established!")

    def generate_test_cases(
        self, endpoint_info
    ):  # we call the AI to get test case descriptions
        """
        Main method that uses AI to generates test cases for given endpoint
        """
        analysis = self.analyze_endpoint(endpoint_info)
        print("Generating AI-powered test cases...")
        # Create AI Prompt

        prompt = f"""
        Generate comprehensive API test cases for this endpoint: {endpoint_info}
         Endpoint Details:
        - HTTP Method: {analysis['method']}
        - Resource Type: {analysis['resource_type']}
        - Path Parameters: {analysis['path_parameters']}
        - Likely requires authentication: {analysis['requires_auth']}
        
        Include:
        1. Positive test cases (valid scenarios)
        2. Negative test cases (invalid inputs)
        3. Boundary test cases (edge values)
        4. Security test cases (basic security checks)
        
        Format each test case as: "Test Case X: Description"
        Provide exactly 8 test cases.
        """

        try:
            # Get AI Response
            response = self.model.generate_content(prompt)
            # Clean up the response and split into individual test cases
            test_cases_text = response.text.strip()
            test_cases = [
                case.strip()
                for case in test_cases_text.split("\n")
                if case.strip() and "Test Case" in case
            ]
            print(f"Successfully generated {len(test_cases)} test cases")
            return test_cases

        except Exception as e:
            print(f"AI generation failed: {e}")
            print("Switching to intelligent fallback generation...")
            return self._generate_fallback_test_cases(analysis)

    def analyze_endpoint(self, endpoint_info):
        """
        Analyzes an API endpoint and prepares for test generation
        """
        print(f"Agent analyzing: {endpoint_info}")
        # Extract HTTP method
        method = "GET"  # default
        if endpoint_info.upper().startswith(("GET", "POST", "PUT", "DELETE", "PATCH")):
            method = endpoint_info.split()[0].upper()
            path = endpoint_info.split()[1] if len(endpoint_info.split()) > 1 else ""
        else:
            path = endpoint_info

        # Find path parameters (like {id}, {userId})
        import re

        path_params = re.findall(r"\{(\w+)\}", path)

        # Determine resource type - check custom domains first, then defaults
        resource_type = "unknown"
        if "/" in path:
            potential_resource = path.split("/")[1].lower()
            if potential_resource and not potential_resource.startswith("{"):
                resource_type = potential_resource

        analysis_result = {
            "method": method,
            "path": path,
            "path_parameters": path_params,
            "resource_type": resource_type,
            "requires_auth": len(path_params) > 0,  # Simple heuristic
        }

        print(
            f"Analysis result: Method={method}, Resource={resource_type}, Params={path_params}"
        )

        return analysis_result

    def _generate_fallback_test_cases(self, analysis):
        """
        Generates intelligent test cases without AI when API limits are hit
        """
        print("Using intelligent fallback test generation...")

        method = analysis["method"]
        resource = analysis["resource_type"]
        path_params = analysis["path_parameters"]

        test_cases = []

        # Positive test cases
        test_cases.append(
            f"Test Case 1: Valid {method} request - Retrieve existing {resource} with valid ID"
        )
        test_cases.append(
            f"Test Case 2: Success response validation - Verify {method} {resource} returns correct data structure"
        )

        # Negative test cases
        test_cases.append(
            f"Test Case 3: Invalid ID format - {method} {resource} with non-numeric ID"
        )
        test_cases.append(
            f"Test Case 4: Non-existent resource - {method} {resource} with ID that doesn't exist"
        )

        # Boundary test cases
        if path_params:
            test_cases.append(
                f"Test Case 5: Boundary value testing - {method} {resource} with ID = 0"
            )
            test_cases.append(
                f"Test Case 6: Large ID value - {method} {resource} with very large ID number"
            )

        # Security test cases
        test_cases.append(
            f"Test Case 7: Authorization check - {method} {resource} without authentication token"
        )
        test_cases.append(
            f"Test Case 8: SQL injection attempt - {method} {resource} with malicious ID parameter"
        )

        return test_cases

    def generate_executable_test_code(self, endpoint_info):
        """
        Public method to generate executable Python test code for an API endpoint
        """
        print("Generating executable test code...")
        # Get endpoint analysis
        analysis=self.analyze_endpoint(endpoint_info)
        # Generate the executable code using our private method
        executable_code=self._generate_executable_code(analysis,[])
        print("Executable test code generated successfully!")
        return executable_code


    def _generate_executable_code(self, analysis, test_case_descriptions):
        """
        Converts test case descriptions into executable Python code
        """
        print("Converting to executable test code...")

        method = analysis["method"]
        path = analysis["path"]
        resource = analysis["resource_type"]

        # Create base URL placeholder
        base_url = "https://api.example.com"
        full_endpoint = f"{base_url}{path}"  # string concatination

        executable_code = []  # creation of empty lis executable_code
        executable_code.append("import requests")
        executable_code.append("import pytest")
        executable_code.append("")
        executable_code.append("# Generated API Test Cases")
        executable_code.append(f"BASE_URL = '{base_url}'")
        executable_code.append("")

        # Generate test functions based on test case types
        test_functions = [  # Creates a list test_functions that will contain the results of calling 4 different methods
            self._generate_positive_test(method, path, resource),
            self._generate_negative_test(method, path, resource),
            self._generate_boundary_test(method, path, resource),
            self._generate_security_test(method, path, resource),
        ]

        for func in test_functions:
            executable_code.extend(func)
            executable_code.append("")

        # Takes our list of code lines and joins them into one big string, with newlines between each line
        # puts each line on a new line, creating proper Python code format
        return "\n".join(executable_code)

    def _generate_positive_test(self, method, path, resource):
        """Generate positive test case code"""
        endpoint = path.replace("{id}", "123")  # Replace with valid ID

        return [
            f"def test_valid_{resource}_retrieval():",
            f'    """Test successful {method} request for {resource}"""',
            f"    url = BASE_URL + '{endpoint}'",
            f"    response = requests.{method.lower()}(url)",
            f"    assert response.status_code == 200",
            f"    assert response.json() is not None",
        ]

    def _generate_negative_test(self, method, path, resource):
        """Generate negative test case code"""
        endpoint = path.replace("{id}", "invalid_id")

        return [
            f"def test_invalid_{resource}_id():",
            f'    """Test {method} request with invalid ID"""',
            f"    url = BASE_URL + '{endpoint}'",
            f"    response = requests.{method.lower()}(url)",
            f"    assert response.status_code in [400, 404]",
        ]

    def _generate_boundary_test(self, method, path, resource):
        """Generate boundary test case code"""
        endpoint = path.replace("{id}", "0")

        return [
            f"def test_{resource}_boundary_id():",
            f'    """Test {method} request with boundary ID value"""',
            f"    url = BASE_URL + '{endpoint}'",
            f"    response = requests.{method.lower()}(url)",
            f"    assert response.status_code in [200, 400, 404]",
        ]


    def _generate_security_test(self, method, path, resource):
        """Generate security test case code"""
        endpoint = path.replace("{id}", "1\\'; DROP TABLE users--")

        return [
            f"def test_{resource}_sql_injection():",
            f'    """Test {method} request for SQL injection vulnerability"""',
            f"    url = BASE_URL + '{endpoint}'",
            f"    response = requests.{method.lower()}(url)",
            f"    assert response.status_code in [400, 403]",
            f"    # Should not return database error messages",
        ]
