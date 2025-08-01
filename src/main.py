# Smart API Test Case Generator Agent
from test_generator_agent import TestGeneratorAgent

def main():
    print("Welcome to Smart API Test Case Generator Agent!")
    
    # Create our AI agent instance
    agent = TestGeneratorAgent()
    
    # Test the agent with a sample endpoint
    sample_endpoint = "GET /users/{id}"
    
    # analysis = agent.analyze_endpoint(sample_endpoint)
    # print(analysis)
    
    test_cases = agent.generate_test_cases(sample_endpoint)
    print("Generated test cases:")
    for case in test_cases:
        print(f"- {case}")

    print("\n" + "="*50)
    print("EXECUTABLE TEST CODE:")
    print("="*50)

    test_code = agent.generate_executable_test_code(sample_endpoint)
    print(test_code)

if __name__ == "__main__":
    main()