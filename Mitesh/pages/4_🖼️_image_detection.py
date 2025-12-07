# In pages/4_🖼️_image_detection.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils.helpers import load_model, run_detection
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Image PPE Detection - SafetyEye",
    page_icon="🖼️",
    layout="wide"
)

# Initialize session state
if 'image_model' not in st.session_state:
    st.session_state.image_model = None
    st.session_state.image_model_loaded = False

# Page title
st.title("🖼️ Image PPE Detection")
st.markdown("Upload an image to detect PPE compliance and identify missing safety equipment.")

# Sidebar controls
# Set default confidence threshold
confidence = 0.5

# Required PPE selection
st.sidebar.subheader("Required PPE Items")
st.sidebar.caption("Select which PPE items to check for compliance")

# Initialize session state for required PPE
if 'required_ppe_selection' not in st.session_state:
    st.session_state.required_ppe_selection = {
        'helmet': True,
        'vest': True,
        'glasses': False,
        'gloves': False,
        'boots': False,
        'mask': False
    }

helmet_req = st.sidebar.checkbox("Helmet/Hard Hat", value=st.session_state.required_ppe_selection['helmet'])
vest_req = st.sidebar.checkbox("Safety Vest", value=st.session_state.required_ppe_selection['vest'])
glasses_req = st.sidebar.checkbox("Safety Glasses", value=st.session_state.required_ppe_selection['glasses'])
gloves_req = st.sidebar.checkbox("Gloves", value=st.session_state.required_ppe_selection['gloves'])
boots_req = st.sidebar.checkbox("Safety Boots", value=st.session_state.required_ppe_selection['boots'])
mask_req = st.sidebar.checkbox("Face Mask", value=st.session_state.required_ppe_selection['mask'])

st.session_state.required_ppe_selection = {
    'helmet': helmet_req,
    'vest': vest_req,
    'glasses': glasses_req,
    'gloves': gloves_req,
    'boots': boots_req,
    'mask': mask_req
}

# Model path
model_path = "models/best (8).pt"

# Load model if not already loaded
if not st.session_state.image_model_loaded:
    with st.sidebar:
        with st.spinner("Loading YOLO model..."):
            st.session_state.image_model = load_model(model_path)
            st.session_state.image_model_loaded = True
            if st.session_state.image_model:
                st.success("✅ Model loaded successfully!")
                # Show available classes
                if hasattr(st.session_state.image_model, 'names'):
                    model_classes = list(st.session_state.image_model.names.values())
                    with st.expander("📋 Model Classes", expanded=False):
                        st.write(f"Model can detect {len(model_classes)} classes:")
                        st.write(", ".join(model_classes))
            else:
                st.error("❌ Failed to load model!")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")
    uploaded_image = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        help="Upload an image containing person(s) to check for PPE compliance"
    )
    
    # Display uploaded image
    if uploaded_image is not None:
        # Convert to PIL Image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Convert RGB to BGR if needed (PIL loads as RGB, OpenCV uses BGR)
        if len(img_array.shape) == 3:
            if img_array.shape[2] == 4:  # RGBA
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            else:  # RGB
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
    else:
        img_bgr = None
        st.info("👆 Please upload an image to begin detection")

with col2:
    st.subheader("🔍 Detection Results")
    
    if uploaded_image is not None and st.session_state.image_model is not None:
        if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
            with st.spinner("Analyzing image for PPE compliance..."):
                # Convert to RGB for YOLO
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                
                # Run detection
                detections = run_detection(st.session_state.image_model, img_rgb, confidence)
                
                # Define required PPE items and their variations (expanded list)
                # Common PPE class names the model might detect - including variations with underscores, hyphens, etc.
                required_ppe = {
                    'helmet': ['helmet', 'hardhat', 'hard hat', 'hard_hat', 'hard-hat', 'safety helmet', 
                              'safety_helmet', 'head', 'hat', 'cap', 'hard_helmet'],
                    'vest': ['vest', 'safety vest', 'safety_vest', 'reflective vest', 'reflective_vest',
                            'high vis', 'hi-vis', 'hi_vis', 'high-vis', 'highvis', 'hi vis vest',
                            'orange vest', 'yellow vest', 'safety jacket', 'work vest'],
                    'glasses': ['glasses', 'safety glasses', 'safety_glasses', 'eye protection', 
                               'eye_protection', 'goggles', 'sunglasses', 'eye', 'safety goggles',
                               'protective glasses', 'safety_eye'],
                    'gloves': ['gloves', 'safety gloves', 'safety_gloves', 'work gloves', 'work_gloves',
                              'hand protection', 'hand_protection', 'hand'],
                    'boots': ['boots', 'safety boots', 'safety_boots', 'steel toe', 'steel_toe',
                             'work boots', 'work_boots', 'safety shoes', 'safety_shoes', 'foot',
                             'footwear', 'safety footwear'],
                    'mask': ['mask', 'face mask', 'face_mask', 'respirator', 'face protection',
                            'face_protection', 'mouth', 'face', 'safety mask', 'safety_mask',
                            'dust mask', 'dust_mask']
                }
                
                # Get all class names from the model to understand what it can detect
                model_classes = []
                if st.session_state.image_model and hasattr(st.session_state.image_model, 'names'):
                    model_classes = list(st.session_state.image_model.names.values())
                
                # Process results
                detected_labels = []  # All detected labels (keep original case for display)
                detected_labels_lower = set()  # Normalized for matching
                detected_items_detail = []  # All detections with details
                person_detected = False
                
                # First pass: collect all detections
                for det in detections:
                    label = det['label']
                    label_lower = label.lower().strip()
                    detected_labels.append(label)
                    detected_labels_lower.add(label_lower)
                    detected_items_detail.append(det)
                    if 'person' in label_lower or 'worker' in label_lower or 'people' in label_lower:
                        person_detected = True
                
                # Identify detected PPE items by matching detected labels to PPE categories
                detected_ppe = {}
                violations = []
                compliance_items = []
                other_detections = []
                
                # Check which required PPE items are detected (improved matching)
                for ppe_category, variations in required_ppe.items():
                    for detected_label_lower in detected_labels_lower:
                        for variation in variations:
                            # Check if variation matches the detected label (substring or exact match)
                            if variation.lower() in detected_label_lower or detected_label_lower in variation.lower():
                                detected_ppe[ppe_category] = True
                                break
                        if ppe_category in detected_ppe:
                            break
                
                # Process each detection for display
                result_image = img_bgr.copy()
                
                for det in detected_items_detail:
                    x1, y1, x2, y2 = map(int, det['box'])
                    label = det['label']
                    conf = det['confidence']
                    label_lower = label.lower().strip()
                    
                    # Check if this is a PPE item or violation
                    is_ppe_item = False
                    is_violation_label = "No " in label or "Missing" in label or "no_" in label_lower
                    ppe_category_found = None
                    
                    # Check if it matches any required PPE (improved matching)
                    for ppe_category, variations in required_ppe.items():
                        for variation in variations:
                            # More flexible matching - check substring in either direction
                            if variation.lower() in label_lower or label_lower in variation.lower():
                                is_ppe_item = True
                                ppe_category_found = ppe_category
                                # Mark this category as detected
                                detected_ppe[ppe_category] = True
                                # Only add if not already added (check by category to avoid duplicates)
                                item_exists = any(item.get('category') == ppe_category for item in compliance_items)
                                if not item_exists:
                                    compliance_items.append({
                                        'item': label,
                                        'category': ppe_category,
                                        'confidence': conf,
                                        'box': (x1, y1, x2, y2)
                                    })
                                break
                        if is_ppe_item:
                            break
                    
                    if is_violation_label:
                        violations.append({
                            'item': label,
                            'confidence': conf,
                            'box': (x1, y1, x2, y2)
                        })
                        color = (0, 0, 255)  # Red for violations
                    elif is_ppe_item:
                        color = (0, 255, 0)  # Green for PPE compliance
                    elif 'person' in label_lower or 'worker' in label_lower:
                        color = (255, 255, 0)  # Yellow for person
                        other_detections.append({
                            'item': label,
                            'confidence': conf,
                            'box': (x1, y1, x2, y2)
                        })
                    else:
                        color = (255, 165, 0)  # Orange for other detections
                        other_detections.append({
                            'item': label,
                            'confidence': conf,
                            'box': (x1, y1, x2, y2)
                        })
                    
                    # Draw rectangle
                    cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 2)
                    
                    # Add label with confidence
                    label_text = f"{label} {conf:.2f}"
                    # Calculate text size for background
                    (text_width, text_height), baseline = cv2.getTextSize(
                        label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                    )
                    # Draw background rectangle for text
                    cv2.rectangle(
                        result_image,
                        (x1, y1 - text_height - 10),
                        (x1 + text_width, y1),
                        color,
                        -1
                    )
                    # Draw text
                    cv2.putText(
                        result_image,
                        label_text,
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )
                
                # NOW check for missing PPE (after processing all detections)
                # If person is detected, check for missing PPE (only for required items)
                if person_detected:
                    for ppe_category in required_ppe.keys():
                        # Only check for required PPE items that are enabled
                        if st.session_state.required_ppe_selection.get(ppe_category, False):
                            if ppe_category not in detected_ppe:
                                violations.append({
                                    'item': f"No {ppe_category.title()}",
                                    'category': ppe_category,
                                    'confidence': 0.0,  # We don't have confidence for missing items
                                    'box': None
                                })
                
                # Convert result back to RGB for display
                result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
                
                # Display annotated image
                st.image(result_image_rgb, caption="Detection Results", use_container_width=True)
                
                # Debug: Show what was actually detected
                with st.expander("🔍 Debug: Raw Detections", expanded=False):
                    if detected_labels:
                        st.write("**All detected labels:**")
                        for label in set(detected_labels):
                            st.write(f"- `{label}`")
                    else:
                        st.write("No detections found. Try lowering the confidence threshold.")
                    if model_classes:
                        st.write(f"\n**Model classes ({len(model_classes)} total):**")
                        st.write(", ".join(model_classes[:30]))  # Show first 30
                
                # Display compliance status
                st.markdown("---")
                
                # Compliance Summary
                total_violations = len(violations)
                total_compliance = len(compliance_items)
                total_persons = sum(1 for det in detected_items_detail if 'person' in det['label'].lower())
                
                if total_violations > 0:
                    st.error(f"❌ **PPE Violations Detected: {total_violations}**")
                    
                    st.markdown("### ⚠️ Missing Required PPE Items:")
                    missing_items = [v for v in violations if v.get('confidence', 0) == 0]
                    detected_violations = [v for v in violations if v.get('confidence', 0) > 0]
                    
                    if missing_items:
                        st.markdown("**Items NOT detected in the image (may be missing):**")
                        for i, violation in enumerate(missing_items, 1):
                            st.markdown(
                                f"{i}. **{violation['item']}** - Required but not found"
                            )
                    
                    if detected_violations:
                        st.markdown("**Detected violation indicators:**")
                        for i, violation in enumerate(detected_violations, 1):
                            st.markdown(
                                f"{i}. **{violation['item']}** "
                                f"(Confidence: {violation['confidence']:.1%})"
                            )
                    
                    # Log violation to session state for analytics
                    for violation in violations:
                        violation_record = {
                            'timestamp': datetime.now(),
                            'type': violation['item'],
                            'confidence': violation['confidence'],
                            'frame': img_array.copy(),  # Store frame for consistency with video detection
                            'source': 'image',
                            'image_name': uploaded_image.name
                        }
                        
                        if 'violations' not in st.session_state:
                            st.session_state.violations = []
                        st.session_state.violations.append(violation_record)
                    
                else:
                    if person_detected:
                        if total_compliance > 0:
                            st.success(f"✅ **PPE Compliance: All Required Items Detected**")
                            
                            st.markdown("### Detected PPE Items:")
                            # Group by category
                            ppe_by_category = {}
                            for item in compliance_items:
                                cat = item.get('category', 'Other')
                                if cat not in ppe_by_category:
                                    ppe_by_category[cat] = []
                                ppe_by_category[cat].append(item)
                            
                            for category, items in ppe_by_category.items():
                                for item in items:
                                    st.markdown(
                                        f"• **{item['item']}** ({category.title()}) - "
                                        f"Confidence: {item['confidence']:.1%}"
                                    )
                        else:
                            st.warning("⚠️ **Person detected but no PPE items found.** This may indicate missing safety equipment.")
                            if len(detected_labels) > 0:
                                st.info(f"Detected classes: {', '.join([det['label'] for det in detected_items_detail[:5]])}")
                    else:
                        if total_compliance > 0:
                            st.success(f"✅ **PPE Items Detected**")
                            st.markdown("### Detected PPE Items:")
                            for i, item in enumerate(compliance_items, 1):
                                st.markdown(
                                    f"{i}. **{item['item']}** "
                                    f"(Confidence: {item['confidence']:.1%})"
                                )
                        else:
                            st.warning("⚠️ **No persons or PPE items detected.** Please ensure the image contains people and try adjusting the confidence threshold.")
                            if len(model_classes) > 0:
                                with st.expander("📋 Model can detect these classes"):
                                    st.write(", ".join(model_classes[:20]))  # Show first 20 classes
                
                # Statistics
                st.markdown("---")
                st.markdown("### Detection Statistics")
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                with stat_col1:
                    st.metric("Total Detections", len(detections))
                with stat_col2:
                    st.metric("Violations", total_violations, delta=None, delta_color="inverse")
                with stat_col3:
                    st.metric("PPE Items Found", total_compliance)
                
                # Show other detections if any
                if len(other_detections) > 0:
                    with st.expander("🔍 Other Detections"):
                        for det in other_detections:
                            st.markdown(f"• **{det['item']}** (Confidence: {det['confidence']:.1%})")
    
    elif uploaded_image is not None and st.session_state.image_model is None:
        st.error("⚠️ Model not loaded. Please check the model file.")
    else:
        st.info("👆 Upload an image and click 'Analyze Image' to detect PPE compliance")

# Footer
st.markdown("---")
st.caption("SafetyEye - Image-based PPE Compliance Detection")

