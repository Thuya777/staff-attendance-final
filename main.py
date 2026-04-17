import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- ပုံစံပြင်ဆင်ခြင်း ---
st.set_page_config(page_title="Staff Attendance System", layout="wide")

def init_connection():
    try:
        # Streamlit Secrets ထဲက 'gcp_service_account' ကို ယူသုံးတာပါ
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)
        client = gspread.authorize(creds)
        
        # သင့် Google Sheet ID
        SHEET_ID = "1p9o6B-88uLhVBy_nC4-N1zX_F5j66C3v87z9q9S_I8U"
        return client.open_by_key(SHEET_ID)
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

sh = init_connection()

if sh:
    try:
        attendance_sheet = sh.worksheet("Attendance")
        leave_sheet = sh.worksheet("Leave_Requests")
        
        st.title("📅 Staff Attendance System")
        
        # Admin ပိုင်း
        st.divider()
        correct_password = "1234"
        password_input = st.text_input("Password", type="password")
        
        if password_input == correct_password:
            st.success("Admin Login Successful")
            tab1, tab2 = st.tabs(["ရုံးတက်/ဆင်း မှတ်တမ်း", "ခွင့်တိုင်ကြားမှုများ"])
            
            with tab1:
                data1 = attendance_sheet.get_all_records()
                st.dataframe(data1)
            with tab2:
                data2 = leave_sheet.get_all_records()
                st.dataframe(data2)
        elif password_input != "":
            st.error("❌ Password မှားယွင်းနေပါသည်။")
            
    except Exception as e:
        st.error(f"Worksheet Error: {e}")
else:
    st.warning("⚠️ Google Sheet နှင့် ချိတ်ဆက်၍ မရသေးပါ။ Secrets ထဲတွင် Key ကို ပြန်စစ်ပေးပါ။")
