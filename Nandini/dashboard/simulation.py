import numpy as np
import time
from PIL import Image, ImageDraw
import streamlit as st

def draw_human(draw, x, y, color):
    draw.ellipse([x+20, y, x+40, y+20], fill=color)
    draw.rectangle([x+25, y+20, x+35, y+60], fill=color)
    draw.line([(x+25, y+30), (x, y+45)], fill=color, width=4)
    draw.line([(x+35, y+30), (x+60, y+45)], fill=color, width=4)
    draw.line([(x+27, y+60), (x+10, y+100)], fill=color, width=4)
    draw.line([(x+33, y+60), (x+50, y+100)], fill=color, width=4)

def generate_frame(show_boxes=True):

    img = Image.new("RGB", (700, 450), "white")
    draw = ImageDraw.Draw(img)

    # Generateing random number of worker so no fixed no. of workers
    worker_count = np.random.randint(1, 6)

    # Drawing worker 
    for i in range(worker_count):

        x = np.random.randint(50, 500)
        y = np.random.randint(80, 250)

        violation = np.random.choice(
            ["None", "Helmet Missing", "No Vest", "No Boots"],
            p=[0.55, 0.25, 0.12, 0.08]
        )

        severity = (
            "Critical" if violation == "Helmet Missing"
            else "Warning" if violation != "None"
            else "Safe"
        )

        color = "green" if violation == "None" else "red"

        if show_boxes:
            draw_human(draw, x, y, color)
            draw.text((x, y - 10), f"P{i+1}: {severity}", fill=color)

        if violation != "None":
            st.session_state.logs.append({
                "Time": time.strftime("%H:%M:%S"),
                "Person": f"P{i+1}",
                "Violation": violation,
                "Severity": severity
            })
            st.session_state.today_count += 1

    
    return img, worker_count




