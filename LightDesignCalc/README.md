# 💡 AI Interior Lighting Estimator & 3D Visualizer

Maine ye project interior designers aur architects ki madad ke liye banaya hai. Ye sirf ek calculator nahi hai, balki ye ek complete tool hai jo batata hai ki kisi kamre (room) mein kitni light honi chahiye, kaunse bulb (fixtures) best rahenge aur unhe kahan lagana chahiye.

Isme maine **3D Visualization** ka use kiya hai taaki user dekh sake ki unka room light hone ke baad kaisa lagega.

## 🌟 Key Features

*   **3D Room Visualization:** Plotly ka use karke maine ek interactive 3D model banaya hai jo fixtures aur light cone (roshni ka ghera) dikhata hai.
*   **Smart Calculations:** 
    *   Room Area aur Volume calculation.
    *   Natural light contribution (khidki se aane wali roshni).
    *   Wall/Ceiling reflectance (deewaron ke rang ke mutabiq roshni ka palatna).
*   **Fixture Recommendations:** Ye script batati hai ki kitne Lumens ki zaroorat hai aur energy-efficient bulbs suggest karti hai.
*   **Cost Analysis:** Initial cost aur saalana bijli ka kharcha (Annual Energy Cost) bhi calculate karta hai.
*   **PDF Report Generation:** Saari analysis khatam hone ke baad, aap ek click mein poori PDF report download kar sakte ho.

## 🚀 Technology Stack

- **Frontend:** Streamlit (For a smooth web UI)
- **Visualization:** Plotly (Interactive 3D charts)
- **Calculations:** NumPy & Custom Math Logic
- **Report Generation:** FPDF
- **Backend:** Python

## 🛠️ Installation & Setup

1.  **Repository Clone Karein:**
    ```bash
    git clone github.com
    cd interior-lighting-estimator
    ```

2.  **Dependencies Install Karein:**
    ```bash
    pip install streamlit plotly numpy fpdf
    ```

3.  **App Ko Run Karein:**
    ```bash
    streamlit run app.py
    ```

## 📁 Folder Structure

- `app.py`: Main Streamlit application.
- `utils/calculations.py`: Saare mathematical formulas (Area, Lumens, Positions).
- `utils/constants.py`: Standard lighting data (Lux levels for different rooms).
- `utils/calculator.py`: 3D Visualization aur PDF generate karne ka logic.

## 📖 Kaise Use Karein?

1.  Sidebar mein apne room ki Dimensions (Length, Width, Height) daalein.
2.  Room ka type select karein (Kitchen, Bedroom, Office, etc.).
3.  Deewaron aur ceiling ka color choose karein (is-se reflectance par asar padta hai).
4.  Real-time 3D model mein light fixtures ki positions check karein.
5.  **"Download Report"** par click karke apni technical PDF hasil karein.

---
**Developed by [Piyush Kalbande](github.com)** 
*Mera maqsad hai complex architectural calculations ko simple banana.*
