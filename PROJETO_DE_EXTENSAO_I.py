#!/usr/bin/env python3
"""
Test script for the path registry system in PROJETO_DE_EXTENSAO_I.py
Verifies that the path validation and registry functions work correctly.
"""

import sys
import os

# Add current directory to Python path to import our main module
sys.path.insert(0, os.getcwd())

# Import the functions from our main module
from PROJETO_DE_EXTENSAO_I import (
    validar_caminho_seguro,
    _get_safe_path,
    _register_safe_path,
    _validated_paths,
    BASE_ALLOWED_ROOT
)

def test_path_registry():
    """Test the path registry system"""
    print("Testing Path Registry System")
    print("=" * 40)
    
    # Test 1: Basic path validation and registration
    print(f"\n1. Testing with current directory: {os.getcwd()}")
    
    # Clear any existing paths
    _validated_paths.clear()
    
    # Test current directory (should be within BASE_ALLOWED_ROOT)
    current_dir = os.getcwd()
    print(f"   Current directory: {current_dir}")
    print(f"   Base allowed root: {BASE_ALLOWED_ROOT}")
    
    is_valid, path_id = validar_caminho_seguro(current_dir)
    print(f"   Validation result: {is_valid}")
    print(f"   Path ID: {path_id}")
    
    if is_valid:
        # Test retrieving the path from registry
        retrieved_path = _get_safe_path(path_id)
        print(f"   Retrieved path: {retrieved_path}")
        print(f"   Registry contents: {len(_validated_paths)} entries")
        
        # Verify path matches
        if retrieved_path == current_dir:
            print("   ✓ Path registry working correctly!")
        else:
            print(f"   ✗ Path mismatch: expected {current_dir}, got {retrieved_path}")
    else:
        print(f"   ✗ Path validation failed: {path_id}")
    
    # Test 2: Invalid path (outside base root)
    print(f"\n2. Testing with invalid path (C:\\):")
    
    is_valid, error_msg = validar_caminho_seguro("C:\\")
    print(f"   Validation result: {is_valid}")
    print(f"   Error message: {error_msg}")
    
    if not is_valid:
        print("   ✓ Invalid path correctly rejected!")
    else:
        print("   ✗ Invalid path was accepted - security issue!")
    
    # Test 3: Registry state
    print(f"\n3. Registry state:")
    print(f"   Total registered paths: {len(_validated_paths)}")
    for path_id, path in _validated_paths.items():
        print(f"   - {path_id}: {path}")

if __name__ == "__main__":
    test_path_registry()
