import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 1. GOOGLE SHEETS SETUP ---
st.set_page_config(page_title="Staff Attendance System", layout="wide")

def init_connection():
    try:
        # Google API သုံးရန် Scope သတ်မှတ်ခြင်း
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Streamlit Secrets ထဲက Key ကို ယူသုံးခြင်း
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # သင့် Google Sheet ID
        SHEET_ID = "1p9o6B-88uLhVBy_nC4-N1zX_F5j66C3v87z9q9S_I8U"
        return client.open_by_key(SHEET_ID)
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

# Connection ကို စတင်ချိတ်ဆက်ခြင်း
sh = init_connection()

if sh:
    try:
        # Worksheet အသီးသီးကို ချိတ်ဆက်ခြင်း
        attendance_sheet = sh.worksheet("Attendance")
        leave_sheet = sh.worksheet("Leave_Requests")
        employee_list_sheet = sh.worksheet("Sheet1")
        
        # --- UI ပိုင်းဆိုင်ရာများ ---
        st.title("📅 Staff Attendance System")
        
        # ဒီနေရာမှာ နင့်ရဲ့ ကျန်တဲ့ logic တွေ (ဥပမာ - ရုံးတက်/ဆင်း မှတ်တမ်းတင်တာတွေ) ဆက်ရေးနိုင်ပါတယ်
        
        # --- Admin ပိုင်း (နင့်ပုံထဲကအတိုင်း) ---
        st.divider()
        st.subheader("🔑 Admin Panel")
        
        # Sheet ထဲတွင် ဖတ်၍မရပါက အောက်ပါ password ရိုက်ပါ
        correct_password = "1234"
        password_input = st.text_input("Password", type="password")
        
        if password_input == correct_password:
            st.success("Admin Login Successful")
            tab1, tab2 = st.tabs(["ရုံးတက်/ဆင်း မှတ်တမ်း", "ခွင့်တိုင်ကြားမှုများ"])
            
            with tab1:
                st.subheader("ဝန်ထမ်း ရုံးတက်/ဆင်း စာရင်း")
                data1 = attendance_sheet.get_all_records()
                st.dataframe(data1)
                
            with tab2:
                st.subheader("ခွင့်တိုင်ကြားထားသည့် စာရင်း")
                data2 = leave_sheet.get_all_records()
                st.dataframe(data2)
                
        elif password_input != "":
            st.error("❌ Password မှားယွင်းနေပါသည်။")
            st.info("💡 Google Sheet Settings Tab (Admin သာ)")
            
    except Exception as e:
        st.error(f"Worksheet Error: {e}")
else:
    st.warning("⚠️ Google Sheet နှင့် ချိတ်ဆက်၍ မရသေးပါ။ Secrets ထဲတွင် Key မှန်မမှန် ပြန်စစ်ပေးပါ။")
