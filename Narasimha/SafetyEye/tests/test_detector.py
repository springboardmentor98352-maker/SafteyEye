import pytest
from utils.detector import SafetyDetector

def test_detect_compliant_equipment():
    detector = SafetyDetector()
    image_path = 'tests/test_images/compliant.jpg'  # Path to a test image with compliant equipment
    results = detector.detect(image_path)
    
    assert results['compliant'] == True
    assert 'NO-Hardhat' not in results['violations']
    assert 'NO-Safety Vest' not in results['violations']
    assert 'NO-Mask' not in results['violations']

def test_detect_violation():
    detector = SafetyDetector()
    image_path = 'tests/test_images/violation.jpg'  # Path to a test image with violations
    results = detector.detect(image_path)
    
    assert results['compliant'] == False
    assert 'NO-Hardhat' in results['violations'] or 'NO-Safety Vest' in results['violations'] or 'NO-Mask' in results['violations']

def test_empty_image():
    detector = SafetyDetector()
    image_path = 'tests/test_images/empty.jpg'  # Path to a test image with no people
    results = detector.detect(image_path)
    
    assert results['compliant'] == True
    assert results['violations'] == []  # No violations should be detected

def test_invalid_image_path():
    detector = SafetyDetector()
    image_path = 'tests/test_images/invalid.jpg'  # Path to a non-existent image
    
    with pytest.raises(FileNotFoundError):
        detector.detect(image_path)