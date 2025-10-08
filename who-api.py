import requests
import json
import hashlib
import hmac
import base64
from typing import List, Dict
from datetime import datetime

class MedicalDiagnosisSystem:
    """
    Medical diagnosis system using ApiMedic (Priaid) API
    """
    
    def __init__(self):
        # API Credentials
        self.client_id = "eb26eb83-f519-4735-931c-4165b93fdfcd_bb9fd5b6-9f40-4b9c-b78a-e7a46f0e3abc"
        self.client_secret = "w/rNjqX3N2aEZELH3BDc9pnXf7bXGP8iWpeiKFg0KjI="
        
        # API endpoints
        self.auth_url = "https://authservice.priaid.ch/login"
        self.api_url = "https://healthservice.priaid.ch"
        
        # Token storage
        self.token = None
        self.token_expiry = None
        
        # Cache
        self.symptoms_cache = None
        self.issues_cache = None
    
    def get_auth_token(self):
        """
        Authenticate and get access token
        """
        try:
            # Create authentication string
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_string.encode('utf-8')
            auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            headers = {
                'Authorization': f'Basic {auth_b64}'
            }
            
            response = requests.post(self.auth_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['Token']
                self.token_expiry = datetime.now()
                print("✓ Authentication successful!")
                return self.token
            else:
                print(f"✗ Authentication failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return None
    
    def ensure_authenticated(self):
        """Ensure we have a valid token"""
        if not self.token:
            return self.get_auth_token()
        return self.token
    
    def get_all_symptoms(self, language='en-gb'):
        """
        Fetch all available symptoms from API
        """
        if self.symptoms_cache:
            return self.symptoms_cache
        
        if not self.ensure_authenticated():
            return None
        
        try:
            url = f"{self.api_url}/symptoms"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            params = {
                'language': language,
                'format': 'json'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                self.symptoms_cache = response.json()
                print(f"✓ Fetched {len(self.symptoms_cache)} symptoms")
                return self.symptoms_cache
            else:
                print(f"✗ Error fetching symptoms: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def search_symptoms(self, keyword):
        """
        Search for symptoms by keyword
        """
        symptoms = self.get_all_symptoms()
        if not symptoms:
            return []
        
        keyword_lower = keyword.lower()
        matches = [
            s for s in symptoms 
            if keyword_lower in s['Name'].lower()
        ]
        
        return matches
    
    def get_diagnosis(self, symptom_ids, gender, year_of_birth, language='en-gb'):
        """
        Get diagnosis based on symptoms
        
        Args:
            symptom_ids: List of symptom IDs (e.g., [10, 15, 223])
            gender: 'male' or 'female'
            year_of_birth: Birth year (e.g., 1990)
            language: Language code (default: 'en-gb')
        """
        if not self.ensure_authenticated():
            return None
        
        try:
            url = f"{self.api_url}/diagnosis"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            params = {
                'symptoms': json.dumps(symptom_ids),
                'gender': gender,
                'year_of_birth': year_of_birth,
                'language': language,
                'format': 'json'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"✗ Diagnosis error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def get_issue_info(self, issue_id, language='en-gb'):
        """
        Get detailed information about a specific issue/disease
        """
        if not self.ensure_authenticated():
            return None
        
        try:
            url = f"{self.api_url}/issues/{issue_id}/info"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            params = {
                'language': language,
                'format': 'json'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"✗ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def get_body_locations(self, language='en-gb'):
        """
        Get all body locations
        """
        if not self.ensure_authenticated():
            return None
        
        try:
            url = f"{self.api_url}/body/locations"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            params = {
                'language': language,
                'format': 'json'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"✗ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def get_symptoms_by_body_location(self, location_id, gender, language='en-gb'):
        """
        Get symptoms for a specific body location
        """
        if not self.ensure_authenticated():
            return None
        
        try:
            url = f"{self.api_url}/symptoms/{location_id}/{gender}"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            params = {
                'language': language,
                'format': 'json'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"✗ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Error: {e}")
            return None


# ===== USAGE EXAMPLES =====

def example_1_search_symptoms():
    """Example: Search for symptoms"""
    print("="*70)
    print("EXAMPLE 1: Search Symptoms")
    print("="*70)
    
    system = MedicalDiagnosisSystem()
    
    # Search for fever-related symptoms
    print("\nSearching for 'fever' symptoms...")
    results = system.search_symptoms('fever')
    
    if results:
        print(f"\nFound {len(results)} matching symptoms:")
        for symptom in results[:5]:  # Show first 5
            print(f"  ID: {symptom['ID']} - {symptom['Name']}")
    

def example_2_get_diagnosis():
    """Example: Get diagnosis from symptoms"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Get Diagnosis")
    print("="*70)
    
    system = MedicalDiagnosisSystem()
    
    # First, let's find symptom IDs
    print("\nStep 1: Finding symptom IDs...")
    fever_symptoms = system.search_symptoms('fever')
    cough_symptoms = system.search_symptoms('cough')
    headache_symptoms = system.search_symptoms('headache')
    
    if fever_symptoms and cough_symptoms and headache_symptoms:
        symptom_ids = [
            fever_symptoms[0]['ID'],
            cough_symptoms[0]['ID'],
            headache_symptoms[0]['ID']
        ]
        
        print(f"Selected symptoms: {symptom_ids}")
        
        # Get diagnosis
        print("\nStep 2: Getting diagnosis...")
        diagnosis = system.get_diagnosis(
            symptom_ids=symptom_ids,
            gender='male',
            year_of_birth=1990
        )
        
        if diagnosis:
            print("\n" + "-"*70)
            print("DIAGNOSIS RESULTS:")
            print("-"*70)
            for i, issue in enumerate(diagnosis[:5], 1):  # Top 5 results
                print(f"\n{i}. {issue['Issue']['Name']}")
                print(f"   Professional Name: {issue['Issue']['ProfName']}")
                print(f"   Accuracy: {issue['Issue']['Accuracy']}%")
                print(f"   ICD: {issue['Issue'].get('Icd', 'N/A')}")
                
                # Get detailed info
                details = system.get_issue_info(issue['Issue']['ID'])
                if details:
                    print(f"   Description: {details.get('Description', 'N/A')[:200]}...")


def example_3_body_locations():
    """Example: Get symptoms by body location"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Symptoms by Body Location")
    print("="*70)
    
    system = MedicalDiagnosisSystem()
    
    print("\nFetching body locations...")
    locations = system.get_body_locations()
    
    if locations:
        print(f"\nAvailable body locations ({len(locations)} total):")
        for loc in locations[:10]:  # Show first 10
            print(f"  ID: {loc['ID']} - {loc['Name']}")
        
        # Get symptoms for head
        head_location = next((l for l in locations if 'head' in l['Name'].lower()), None)
        if head_location:
            print(f"\nGetting symptoms for: {head_location['Name']}")
            symptoms = system.get_symptoms_by_body_location(
                location_id=head_location['ID'],
                gender='male'
            )
            
            if symptoms:
                print(f"Found {len(symptoms)} symptoms:")
                for symptom in symptoms[:10]:  # Show first 10
                    print(f"  - {symptom['Name']}")


def interactive_diagnosis():
    """Interactive diagnosis example"""
    print("\n" + "="*70)
    print("INTERACTIVE DIAGNOSIS TOOL")
    print("="*70)
    
    system = MedicalDiagnosisSystem()
    
    print("\nThis tool helps you get a diagnosis based on symptoms.")
    print("Note: This is NOT medical advice. Always consult a doctor.")
    
    # Get patient info
    print("\nPatient Information:")
    gender = input("Gender (male/female): ").lower()
    year_of_birth = int(input("Year of birth (e.g., 1990): "))
    
    # Get symptoms
    print("\nEnter symptoms (one per line, empty line to finish):")
    symptom_keywords = []
    while True:
        symptom = input("Symptom: ").strip()
        if not symptom:
            break
        symptom_keywords.append(symptom)
    
    # Find symptom IDs
    print("\nSearching for symptoms...")
    symptom_ids = []
    for keyword in symptom_keywords:
        results = system.search_symptoms(keyword)
        if results:
            symptom_ids.append(results[0]['ID'])
            print(f"  ✓ Found: {results[0]['Name']}")
        else:
            print(f"  ✗ Not found: {keyword}")
    
    if not symptom_ids:
        print("\nNo valid symptoms found. Please try again.")
        return
    
    # Get diagnosis
    print("\nAnalyzing symptoms...")
    diagnosis = system.get_diagnosis(
        symptom_ids=symptom_ids,
        gender=gender,
        year_of_birth=year_of_birth
    )
    
    if diagnosis:
        print("\n" + "="*70)
        print("POSSIBLE CONDITIONS (Top 5):")
        print("="*70)
        for i, issue in enumerate(diagnosis[:5], 1):
            print(f"\n{i}. {issue['Issue']['Name']}")
            print(f"   Accuracy: {issue['Issue']['Accuracy']}%")
            print(f"   Specialist: {issue['Specialisation'][0]['Name'] if issue['Specialisation'] else 'General'}")


if __name__ == "__main__":
    # Run examples
    example_1_search_symptoms()
    example_2_get_diagnosis()
    example_3_body_locations()
    
    # Uncomment for interactive mode:
    # interactive_diagnosis()
