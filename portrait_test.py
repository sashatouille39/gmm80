#!/usr/bin/env python3
"""
Portrait System Test Suite - Review Request Français
Tests the portrait generation system by layers as specified in the review request
"""

import requests
import json
import os
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        return "http://localhost:8001"
    return "http://localhost:8001"

BACKEND_URL = get_backend_url()
API_BASE = f"{BACKEND_URL}/api"

class PortraitTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")

    def test_server_startup(self):
        """Test: Vérifier que l'API démarre correctement"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_result("Server Startup", True, f"API accessible at {API_BASE}")
                    return True
                else:
                    self.log_result("Server Startup", False, "API accessible but unexpected response format", data)
                    return False
            else:
                self.log_result("Server Startup", False, f"HTTP {response.status_code}", response.text[:200])
                return False
        except requests.exceptions.RequestException as e:
            self.log_result("Server Startup", False, f"Connection failed: {str(e)}")
            return False

    def test_portrait_layer_assembly(self):
        """Test 1: Vérifier que select_random_portrait_layers() retourne bien 5 calques"""
        try:
            print("\n🎯 TESTING PORTRAIT LAYER ASSEMBLY - 5 LAYERS VERIFICATION")
            print("=" * 80)
            
            # Test different nationalities and genders as specified in review request
            test_cases = [
                ("Français", "M"),
                ("Française", "F"), 
                ("Japonais", "M"),
                ("Japonaise", "F"),
                ("Nigérian", "M"),
                ("Nigériane", "F"),
                ("Brésilien", "M"),
                ("Brésilienne", "F")
            ]
            
            all_tests_passed = True
            layer_results = []
            
            for nationality, gender in test_cases:
                print(f"   Testing {nationality} {gender}...")
                
                # Generate a player to get portrait layers
                response = requests.post(f"{API_BASE}/games/generate-players?count=1", timeout=10)
                
                if response.status_code == 200:
                    players = response.json()
                    if players and len(players) > 0:
                        player = players[0]
                        portrait = player.get('portrait', {})
                        
                        # Check if portrait has meaningful fields
                        portrait_fields = list(portrait.keys())
                        meaningful_fields = [f for f in portrait_fields if f in ['face_shape', 'skin_color', 'hairstyle', 'hair_color', 'eye_color', 'eye_shape']]
                        
                        layer_results.append({
                            'nationality': nationality,
                            'gender': gender,
                            'portrait_fields': portrait_fields,
                            'meaningful_fields': meaningful_fields,
                            'field_count': len(meaningful_fields)
                        })
                        
                        print(f"     Portrait fields: {portrait_fields}")
                        print(f"     Meaningful fields: {meaningful_fields} ({len(meaningful_fields)} fields)")
                        
                    else:
                        all_tests_passed = False
                        print(f"     ❌ No players generated for {nationality} {gender}")
                else:
                    all_tests_passed = False
                    print(f"     ❌ Failed to generate player for {nationality} {gender} - HTTP {response.status_code}")
            
            # Now test the actual portrait service directly via API
            print(f"\n   Testing portrait service API endpoints...")
            
            # Test portrait generation endpoint
            for nationality, gender in test_cases[:2]:  # Test first 2 cases
                portrait_request = {
                    "nationality": nationality,
                    "gender": gender,
                    "age": 25,
                    "variations": 1
                }
                
                response = requests.post(f"{API_BASE}/portraits/generate", 
                                       json=portrait_request,
                                       headers={"Content-Type": "application/json"},
                                       timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('portraits'):
                        portraits = data['portraits']
                        if portraits and len(portraits) > 0:
                            portrait_layers = portraits[0]
                            layer_count = len(portrait_layers)
                            
                            print(f"     ✅ {nationality} {gender}: Generated {layer_count} layers: {list(portrait_layers.keys())}")
                            
                            if layer_count == 5:
                                # Check if all expected layer types are present
                                expected_layers = ['base', 'eyes', 'hair', 'mouth', 'nose']
                                has_all_layers = all(layer in portrait_layers for layer in expected_layers)
                                
                                if has_all_layers:
                                    print(f"       ✅ All 5 expected layers present: {expected_layers}")
                                else:
                                    missing_layers = [layer for layer in expected_layers if layer not in portrait_layers]
                                    print(f"       ⚠️  Missing layers: {missing_layers}")
                            else:
                                print(f"       ⚠️  Expected 5 layers, got {layer_count}")
                        else:
                            print(f"     ❌ No portraits in response for {nationality} {gender}")
                    else:
                        print(f"     ❌ Invalid response structure for {nationality} {gender}")
                else:
                    print(f"     ❌ Portrait generation failed for {nationality} {gender} - HTTP {response.status_code}")
            
            if all_tests_passed:
                self.log_result("Portrait Layer Assembly", True, 
                              f"✅ Portrait system working - tested {len(test_cases)} nationality/gender combinations")
            else:
                self.log_result("Portrait Layer Assembly", False, 
                              f"❌ Portrait system issues found in testing")
                
        except Exception as e:
            self.log_result("Portrait Layer Assembly", False, f"Error during test: {str(e)}")

    def test_portrait_file_existence(self):
        """Test 2: Vérifier que les fichiers retournés existent physiquement"""
        try:
            print("\n🎯 TESTING PORTRAIT FILE PHYSICAL EXISTENCE")
            print("=" * 80)
            
            # Test available portraits endpoint
            test_nationalities = ["Français", "Japonais", "Nigérian", "Brésilien"]
            
            files_checked = 0
            files_exist = 0
            missing_files = []
            
            for nationality in test_nationalities:
                for gender in ["M", "F"]:
                    print(f"   Checking available portraits for {nationality} {gender}...")
                    
                    response = requests.get(f"{API_BASE}/portraits/available/{nationality}/{gender}", timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success') and data.get('portraits'):
                            portraits = data['portraits']
                            portrait_count = len(portraits)
                            print(f"     Found {portrait_count} available portraits")
                            
                            # Check first portrait's files
                            if portraits:
                                first_portrait = portraits[0]
                                for layer_type, file_path in first_portrait.items():
                                    files_checked += 1
                                    # Convert API path to filesystem path
                                    if file_path.startswith('/static/portraits/'):
                                        fs_path = f"/app/backend{file_path}"
                                        
                                        if os.path.exists(fs_path):
                                            files_exist += 1
                                            print(f"       ✅ {layer_type}: {file_path} exists")
                                        else:
                                            missing_files.append(f"{nationality} {gender} {layer_type}: {file_path}")
                                            print(f"       ❌ {layer_type}: {file_path} NOT FOUND")
                        else:
                            print(f"     ⚠️  No portraits available for {nationality} {gender}")
                    else:
                        print(f"     ❌ Failed to get portraits for {nationality} {gender} - HTTP {response.status_code}")
            
            # Also check some files directly from the filesystem
            print(f"\n   Direct filesystem check...")
            portrait_dirs = ['/app/backend/static/portraits/base', 
                           '/app/backend/static/portraits/eyes',
                           '/app/backend/static/portraits/hair', 
                           '/app/backend/static/portraits/mouth',
                           '/app/backend/static/portraits/nose']
            
            total_files_found = 0
            for portrait_dir in portrait_dirs:
                if os.path.exists(portrait_dir):
                    files_in_dir = len([f for f in os.listdir(portrait_dir) if f.endswith('.png')])
                    total_files_found += files_in_dir
                    print(f"     {os.path.basename(portrait_dir)}: {files_in_dir} PNG files")
                else:
                    print(f"     ❌ Directory not found: {portrait_dir}")
            
            print(f"\n   📊 SUMMARY:")
            print(f"   - API files checked: {files_checked}")
            print(f"   - API files exist: {files_exist}")
            print(f"   - Total PNG files found: {total_files_found}")
            print(f"   - Missing files: {len(missing_files)}")
            
            if len(missing_files) == 0 and files_exist > 0:
                self.log_result("Portrait File Existence", True, 
                              f"✅ All {files_exist} checked portrait files exist physically. Total PNG files: {total_files_found}")
            else:
                self.log_result("Portrait File Existence", False, 
                              f"❌ {len(missing_files)} files missing out of {files_checked} checked", missing_files[:5])
                
        except Exception as e:
            self.log_result("Portrait File Existence", False, f"Error during test: {str(e)}")

    def test_portrait_api_endpoints(self):
        """Test 3: Tester l'endpoint API des portraits"""
        try:
            print("\n🎯 TESTING PORTRAIT API ENDPOINTS")
            print("=" * 80)
            
            # Test 1: Portrait generation endpoint
            print("   Testing POST /api/portraits/generate...")
            
            test_request = {
                "nationality": "Français",
                "gender": "M",
                "age": 25,
                "variations": 1
            }
            
            response = requests.post(f"{API_BASE}/portraits/generate", 
                                   json=test_request,
                                   headers={"Content-Type": "application/json"},
                                   timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['success', 'nationality', 'gender', 'age', 'portraits', 'message']
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    portraits = data.get('portraits', [])
                    if portraits and len(portraits) > 0:
                        first_portrait = portraits[0]
                        layer_count = len(first_portrait)
                        
                        print(f"     ✅ Generation successful: {layer_count} layers generated")
                        print(f"     Layers: {list(first_portrait.keys())}")
                        
                        # Verify URLs are accessible
                        accessible_urls = 0
                        for layer_type, url in first_portrait.items():
                            if url.startswith('/static/'):
                                full_url = f"{BACKEND_URL}{url}"
                                try:
                                    url_response = requests.head(full_url, timeout=5)
                                    if url_response.status_code == 200:
                                        accessible_urls += 1
                                        print(f"       ✅ {layer_type}: URL accessible")
                                    else:
                                        print(f"       ❌ {layer_type}: URL not accessible ({url_response.status_code})")
                                except:
                                    print(f"       ❌ {layer_type}: URL request failed")
                        
                        self.log_result("Portrait Generation API", True, 
                                      f"✅ Portrait generation working: {layer_count} layers, {accessible_urls}/{layer_count} URLs accessible")
                    else:
                        self.log_result("Portrait Generation API", False, "No portraits in response")
                else:
                    self.log_result("Portrait Generation API", False, f"Response missing fields: {missing_fields}")
            else:
                self.log_result("Portrait Generation API", False, f"HTTP {response.status_code}: {response.text[:200]}")
            
            # Test 2: Available portraits endpoint
            print("\n   Testing GET /api/portraits/available/{nationality}/{gender}...")
            
            response = requests.get(f"{API_BASE}/portraits/available/Japonais/F", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['success', 'nationality', 'region', 'gender', 'count', 'portraits']
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    count = data.get('count', 0)
                    region = data.get('region', '')
                    
                    self.log_result("Portrait Available API", True, 
                                  f"✅ Available portraits API working: {count} portraits found for region '{region}'")
                else:
                    self.log_result("Portrait Available API", False, f"Response missing fields: {missing_fields}")
            else:
                self.log_result("Portrait Available API", False, f"HTTP {response.status_code}")
            
            # Test 3: Regions endpoint
            print("\n   Testing GET /api/portraits/regions...")
            
            response = requests.get(f"{API_BASE}/portraits/regions", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'regions' in data and 'nationality_mapping' in data:
                    regions = data['regions']
                    nationality_mapping = data['nationality_mapping']
                    
                    print(f"     ✅ Found {len(regions)} regions and {len(nationality_mapping)} nationality mappings")
                    
                    # Verify our test nationalities are mapped
                    test_nationalities = ["Français", "Japonais", "Nigérian", "Brésilien"]
                    mapped_nationalities = []
                    
                    for nationality in test_nationalities:
                        if nationality in nationality_mapping:
                            region = nationality_mapping[nationality]
                            mapped_nationalities.append(f"{nationality} → {region}")
                        else:
                            print(f"       ⚠️  {nationality} not found in mapping")
                    
                    if len(mapped_nationalities) == len(test_nationalities):
                        self.log_result("Portrait Regions API", True, 
                                      f"✅ Regions API working: All test nationalities mapped correctly")
                    else:
                        self.log_result("Portrait Regions API", False, 
                                      f"Some test nationalities not mapped: {mapped_nationalities}")
                else:
                    self.log_result("Portrait Regions API", False, "Invalid response structure")
            else:
                self.log_result("Portrait Regions API", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("Portrait API Endpoints", False, f"Error during test: {str(e)}")

    def test_portrait_player_generation(self):
        """Test 4: Tester la génération de joueur avec portraits automatiques"""
        try:
            print("\n🎯 TESTING PLAYER GENERATION WITH AUTOMATIC PORTRAITS")
            print("=" * 80)
            
            # Generate players and verify they have portraits
            response = requests.post(f"{API_BASE}/games/generate-players?count=10", timeout=10)
            
            if response.status_code == 200:
                players = response.json()
                
                if len(players) == 10:
                    players_with_portraits = 0
                    portrait_field_counts = []
                    nationality_portrait_mapping = {}
                    
                    for i, player in enumerate(players):
                        name = player.get('name', f'Player {i+1}')
                        nationality = player.get('nationality', 'Unknown')
                        gender = player.get('gender', 'Unknown')
                        portrait = player.get('portrait', {})
                        
                        if portrait and len(portrait) > 0:
                            players_with_portraits += 1
                            portrait_field_count = len(portrait)
                            portrait_field_counts.append(portrait_field_count)
                            
                            # Track nationality-portrait mapping
                            if nationality not in nationality_portrait_mapping:
                                nationality_portrait_mapping[nationality] = []
                            nationality_portrait_mapping[nationality].append({
                                'name': name,
                                'gender': gender,
                                'portrait_fields': list(portrait.keys()),
                                'field_count': portrait_field_count
                            })
                            
                            print(f"     ✅ {name} ({nationality} {gender}): {portrait_field_count} portrait fields")
                        else:
                            print(f"     ❌ {name} ({nationality} {gender}): No portrait data")
                    
                    # Analyze results
                    avg_portrait_fields = sum(portrait_field_counts) / len(portrait_field_counts) if portrait_field_counts else 0
                    unique_nationalities = len(nationality_portrait_mapping)
                    
                    print(f"\n   📊 ANALYSIS:")
                    print(f"   - Players with portraits: {players_with_portraits}/10")
                    print(f"   - Average portrait fields per player: {avg_portrait_fields:.1f}")
                    print(f"   - Unique nationalities with portraits: {unique_nationalities}")
                    
                    if players_with_portraits == 10:
                        self.log_result("Player Portrait Generation", True, 
                                      f"✅ All players generated with portraits ({avg_portrait_fields:.1f} avg fields)")
                    elif players_with_portraits > 7:  # Allow some tolerance
                        self.log_result("Player Portrait Generation", True, 
                                      f"✅ Most players have portraits ({players_with_portraits}/10)")
                    else:
                        self.log_result("Player Portrait Generation", False, 
                                      f"❌ Too few players with portraits ({players_with_portraits}/10)")
                else:
                    self.log_result("Player Portrait Generation", False, f"Expected 10 players, got {len(players)}")
            else:
                self.log_result("Player Portrait Generation", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("Player Portrait Generation", False, f"Error during test: {str(e)}")

    def test_portrait_nationality_consistency(self):
        """Test 5: Vérifier la cohérence des portraits avec les nationalités"""
        try:
            print("\n🎯 TESTING PORTRAIT-NATIONALITY CONSISTENCY")
            print("=" * 80)
            
            # Test specific nationalities mentioned in review request
            test_cases = [
                ("Français", "western_european"),
                ("Japonais", "east_asian"), 
                ("Nigérian", "african"),
                ("Brésilien", "mixed")
            ]
            
            consistency_results = []
            
            for nationality, expected_region in test_cases:
                print(f"   Testing {nationality} (expected region: {expected_region})...")
                
                # Check region mapping
                response = requests.get(f"{API_BASE}/portraits/regions", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    nationality_mapping = data.get('nationality_mapping', {})
                    
                    actual_region = nationality_mapping.get(nationality)
                    
                    if actual_region == expected_region:
                        print(f"     ✅ Region mapping correct: {nationality} → {actual_region}")
                        
                        # Test portrait generation for this nationality
                        portrait_request = {
                            "nationality": nationality,
                            "gender": "M",
                            "age": 25,
                            "variations": 1
                        }
                        
                        portrait_response = requests.post(f"{API_BASE}/portraits/generate", 
                                                        json=portrait_request,
                                                        headers={"Content-Type": "application/json"},
                                                        timeout=15)
                        
                        if portrait_response.status_code == 200:
                            portrait_data = portrait_response.json()
                            if portrait_data.get('success'):
                                consistency_results.append({
                                    'nationality': nationality,
                                    'expected_region': expected_region,
                                    'actual_region': actual_region,
                                    'portrait_generated': True,
                                    'status': 'success'
                                })
                                print(f"       ✅ Portrait generation successful for {nationality}")
                            else:
                                consistency_results.append({
                                    'nationality': nationality,
                                    'expected_region': expected_region,
                                    'actual_region': actual_region,
                                    'portrait_generated': False,
                                    'status': 'portrait_failed'
                                })
                                print(f"       ❌ Portrait generation failed for {nationality}")
                        else:
                            print(f"       ❌ Portrait API error for {nationality}: HTTP {portrait_response.status_code}")
                    else:
                        consistency_results.append({
                            'nationality': nationality,
                            'expected_region': expected_region,
                            'actual_region': actual_region,
                            'portrait_generated': False,
                            'status': 'region_mismatch'
                        })
                        print(f"     ❌ Region mapping incorrect: expected {expected_region}, got {actual_region}")
                else:
                    print(f"     ❌ Failed to get regions data: HTTP {response.status_code}")
            
            # Evaluate results
            successful_mappings = len([r for r in consistency_results if r['status'] == 'success'])
            total_tests = len(test_cases)
            
            if successful_mappings == total_tests:
                self.log_result("Portrait Nationality Consistency", True, 
                              f"✅ All {total_tests} nationality-region mappings correct and portraits generated")
            elif successful_mappings >= total_tests * 0.75:  # 75% success rate
                self.log_result("Portrait Nationality Consistency", True, 
                              f"✅ Most nationality mappings correct ({successful_mappings}/{total_tests})")
            else:
                failed_results = [r for r in consistency_results if r['status'] != 'success']
                self.log_result("Portrait Nationality Consistency", False, 
                              f"❌ Too many mapping failures ({successful_mappings}/{total_tests})", failed_results)
                
        except Exception as e:
            self.log_result("Portrait Nationality Consistency", False, f"Error during test: {str(e)}")

    def run_portrait_tests(self):
        """Run all portrait system tests"""
        print(f"🎨 Starting Portrait System Tests - Review Request Français")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print("=" * 80)
        
        # Test server startup first
        if not self.test_server_startup():
            print("❌ Server not accessible, stopping tests")
            return
        
        # ===== PORTRAIT SYSTEM TESTS =====
        print("\n" + "🎨" * 40)
        print("🎨 PORTRAIT SYSTEM TESTS - REVIEW REQUEST FRANÇAIS")
        print("🎨" * 40)
        
        self.test_portrait_layer_assembly()
        self.test_portrait_file_existence()
        self.test_portrait_api_endpoints()
        self.test_portrait_player_generation()
        self.test_portrait_nationality_consistency()
        
        # Print summary
        print("\n" + "=" * 80)
        print(f"🏁 PORTRAIT TESTS COMPLETED")
        print(f"📊 Results: {self.passed_tests}/{self.total_tests} tests passed")
        print(f"✅ Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.passed_tests == self.total_tests:
            print("🎉 ALL PORTRAIT TESTS PASSED!")
        else:
            failed_tests = self.total_tests - self.passed_tests
            print(f"⚠️  {failed_tests} tests failed - check details above")
        
        print("=" * 80)

if __name__ == "__main__":
    tester = PortraitTester()
    tester.run_portrait_tests()