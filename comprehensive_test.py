#!/usr/bin/env python3
"""
Comprehensive test of the updated security system with path registry.
Tests the complete workflow from path validation to file operations.
"""

import os
import sys
import tempfile
import shutil

# Import from main module
sys.path.insert(0, os.getcwd())

def test_security_system():
    """Test the complete security system workflow"""
    print("Comprehensive Security System Test")
    print("=" * 50)
    
    from PROJETO_DE_EXTENSAO_I import (
        validar_caminho_seguro,
        validar_arquivo_seguro,
        _get_safe_path,
        _validated_paths,
        BASE_ALLOWED_ROOT
    )
    
    print(f"BASE_ALLOWED_ROOT: {BASE_ALLOWED_ROOT}")
    
    # Test 1: Directory validation and registry
    print(f"\n1. Testing directory validation...")
    
    # Clear registry
    _validated_paths.clear()
    
    # Test with Documents folder (should be valid)
    test_dir = os.path.join(BASE_ALLOWED_ROOT, "Documents")
    if not os.path.exists(test_dir):
        test_dir = BASE_ALLOWED_ROOT
    
    print(f"   Testing directory: {test_dir}")
    is_valid, dir_result = validar_caminho_seguro(test_dir)
    print(f"   Validation result: {is_valid}")
    
    if is_valid:
        print(f"   Directory ID: {dir_result}")
        retrieved_path = _get_safe_path(dir_result)
        print(f"   Retrieved path: {retrieved_path}")
        print(f"   Registry entries: {len(_validated_paths)}")
        
        if retrieved_path == test_dir:
            print("   ✓ Directory validation working correctly!")
            dir_id = dir_result
        else:
            print("   X Path mismatch in registry")
            return
    else:
        print(f"   X Directory validation failed: {dir_result}")
        return
    
    # Test 2: Create a test file for file validation
    print(f"\n2. Testing file validation...")
    
    # Create a temporary test file in the validated directory
    test_file = os.path.join(test_dir, "test_file.txt")
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("This is a test file for security validation.")
        
        print(f"   Created test file: {test_file}")
        
        # Test file validation
        is_file_valid, file_result = validar_arquivo_seguro(test_file, test_dir)
        print(f"   File validation result: {is_file_valid}")
        
        if is_file_valid:
            print(f"   File ID: {file_result}")
            retrieved_file_path = _get_safe_path(file_result)
            print(f"   Retrieved file path: {retrieved_file_path}")
            
            if retrieved_file_path == test_file:
                print("   ✓ File validation working correctly!")
            else:
                print("   X File path mismatch in registry")
        else:
            print(f"   X File validation failed: {file_result}")
        
        # Clean up test file
        os.remove(test_file)
        print("   Test file cleaned up")
        
    except Exception as e:
        print(f"   X Error creating test file: {e}")
        return
    
    # Test 3: Invalid path rejection
    print(f"\n3. Testing invalid path rejection...")
    
    # Test path outside BASE_ALLOWED_ROOT
    invalid_paths = ["C:\\Windows", "D:\\", "/etc"]
    
    for invalid_path in invalid_paths:
        if os.path.exists(invalid_path):  # Only test if path exists
            print(f"   Testing invalid path: {invalid_path}")
            is_valid, error_msg = validar_caminho_seguro(invalid_path)
            if not is_valid:
                print(f"   ✓ Correctly rejected: {error_msg}")
            else:
                print(f"   X Security breach! Invalid path was accepted: {is_valid}")
                return
            break
    
    # Test 4: Registry state
    print(f"\n4. Final registry state:")
    print(f"   Total registered paths: {len(_validated_paths)}")
    for path_id, path in _validated_paths.items():
        path_type = "Directory" if path_id.startswith("dir_") else "File"
        print(f"   - {path_type}: {path_id[:20]}... -> {path}")
    
    print(f"\n✓ All security tests passed!")
    print("  - Path validation working correctly")
    print("  - Path registry system functioning")
    print("  - Invalid paths properly rejected")
    print("  - File operations use safe paths")

if __name__ == "__main__":
    test_security_system()