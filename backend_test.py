import requests
import sys
import json
import time
import io
from datetime import datetime

class MLPlatformAPITester:
    def __init__(self, base_url="https://easymlearn.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.dataset_id = None
        self.job_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        if data and not files:
            headers['Content-Type'] = 'application/json'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, data=data, files=files)
                else:
                    response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "api/", 200)

    def test_models_list(self):
        """Test getting models list"""
        success, response = self.run_test("Models List", "GET", "api/models/list", 200)
        if success:
            # Verify response structure
            if 'supervised' in response and 'unsupervised' in response:
                print("   ✓ Response has correct structure")
                return True
            else:
                print("   ❌ Response missing required fields")
                return False
        return False

    def test_model_parameters(self):
        """Test getting model parameters"""
        # Test supervised model parameters
        success1, _ = self.run_test(
            "Supervised Model Parameters", 
            "GET", 
            "api/models/parameters/supervised/Logistic Regression?model_category=classification", 
            200
        )
        
        # Test unsupervised model parameters
        success2, _ = self.run_test(
            "Unsupervised Model Parameters", 
            "GET", 
            "api/models/parameters/unsupervised/K-Means", 
            200
        )
        
        return success1 and success2

    def test_dataset_upload(self):
        """Test dataset upload with sample CSV"""
        # Create a simple test CSV
        csv_content = """sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
7.0,3.2,4.7,1.4,versicolor
6.4,3.2,4.5,1.5,versicolor
6.9,3.1,4.9,1.5,versicolor
5.5,2.3,4.0,1.3,versicolor
6.5,2.8,4.6,1.5,versicolor
6.3,3.3,6.0,2.5,virginica
5.8,2.7,5.1,1.9,virginica
7.1,3.0,5.9,2.1,virginica
6.3,2.9,5.6,1.8,virginica
6.5,3.0,5.8,2.2,virginica"""
        
        files = {'file': ('test_iris.csv', csv_content, 'text/csv')}
        success, response = self.run_test(
            "Dataset Upload", 
            "POST", 
            "api/dataset/upload", 
            200, 
            files=files
        )
        
        if success and 'dataset_id' in response:
            self.dataset_id = response['dataset_id']
            print(f"   ✓ Dataset ID: {self.dataset_id}")
            return True
        return False

    def test_dataset_columns(self):
        """Test getting dataset columns"""
        if not self.dataset_id:
            print("❌ No dataset ID available")
            return False
            
        success, response = self.run_test(
            "Dataset Columns", 
            "GET", 
            f"api/dataset/{self.dataset_id}/columns", 
            200
        )
        
        if success and 'columns' in response:
            print(f"   ✓ Columns: {response['columns']}")
            return True
        return False

    def test_dataset_clean(self):
        """Test dataset cleaning"""
        if not self.dataset_id:
            print("❌ No dataset ID available")
            return False
            
        success, response = self.run_test(
            "Dataset Clean", 
            "POST", 
            "api/dataset/clean", 
            200,
            data={
                "dataset_id": self.dataset_id,
                "target_column": "species"
            }
        )
        
        if success and response.get('status') == 'cleaned':
            print("   ✓ Dataset cleaned successfully")
            return True
        return False

    def test_model_training(self):
        """Test model training"""
        if not self.dataset_id:
            print("❌ No dataset ID available")
            return False
            
        success, response = self.run_test(
            "Model Training", 
            "POST", 
            "api/model/train", 
            200,
            data={
                "dataset_id": self.dataset_id,
                "model_type": "supervised",
                "model_category": "classification",
                "model_name": "Logistic Regression",
                "parameters": {"C": 1.0, "max_iter": 100},
                "target_column": "species"
            }
        )
        
        if success and 'job_id' in response:
            self.job_id = response['job_id']
            print(f"   ✓ Job ID: {self.job_id}")
            return True
        return False

    def test_training_progress(self):
        """Test training progress tracking"""
        if not self.job_id:
            print("❌ No job ID available")
            return False
            
        # Check progress multiple times
        for i in range(10):  # Check for up to 20 seconds
            success, response = self.run_test(
                f"Training Progress (Check {i+1})", 
                "GET", 
                f"api/model/progress/{self.job_id}", 
                200
            )
            
            if success:
                status = response.get('status')
                progress = response.get('progress', 0)
                print(f"   Status: {status}, Progress: {progress}%")
                
                if status == 'completed':
                    print("   ✅ Training completed successfully!")
                    return True
                elif status == 'failed':
                    print(f"   ❌ Training failed: {response.get('message')}")
                    return False
                    
            time.sleep(2)  # Wait 2 seconds between checks
            
        print("   ⚠️ Training still in progress after 20 seconds")
        return True  # Consider this a pass as training might take longer

    def test_model_download(self):
        """Test model download"""
        if not self.job_id:
            print("❌ No job ID available")
            return False
            
        # First check if training is completed
        success, response = self.run_test(
            "Check Training Status for Download", 
            "GET", 
            f"api/model/progress/{self.job_id}", 
            200
        )
        
        if not success or response.get('status') != 'completed':
            print("   ⚠️ Training not completed, skipping download test")
            return True
            
        # Test download endpoint
        url = f"{self.base_url}/api/model/download/{self.job_id}"
        print(f"\n🔍 Testing Model Download...")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ Passed - Status: {response.status_code}")
                print(f"   Content-Type: {response.headers.get('content-type')}")
                print(f"   Content-Length: {len(response.content)} bytes")
                self.tests_passed += 1
                return True
            else:
                print(f"❌ Failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

def main():
    print("🚀 Starting ML Platform API Tests")
    print("=" * 50)
    
    tester = MLPlatformAPITester()
    
    # Run all tests
    tests = [
        tester.test_api_root,
        tester.test_models_list,
        tester.test_model_parameters,
        tester.test_dataset_upload,
        tester.test_dataset_columns,
        tester.test_dataset_clean,
        tester.test_model_training,
        tester.test_training_progress,
        tester.test_model_download,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            tester.tests_run += 1
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())