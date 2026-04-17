import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- ပုံစံပြင်ဆင်ခြင်း ---
st.set_page_config(page_title="Staff Attendance System", layout="wide")

def init_connection():
    try:
        # Google API သုံးရန် လိုအပ်သော Scope များ
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
        # Secrets ထဲက key ကို ယူသုံးခြင်း
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # သင့် Google Sheet ID
        SHEET_ID = "1p9o6B-88uLhVBy_nC4-N1zX_F5j66C3v87z9q9S_I8U"
        return client.open_by_key(SHEET_ID)
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

# Connection စတင်ချိတ်ဆက်ခြင်း
sh = init_connection()

if sh:
    try:
        # Worksheet အမည်များကို နင့် Google Sheet ထဲကအတိုင်း ပြန်စစ်ပါ
        attendance_sheet = sh.worksheet("Attendance")
        leave_sheet = sh.worksheet("Leave_Requests")
        
        st.title("📅 Staff Attendance System")
        st.success("✅ Google Sheet နှင့် ချိတ်ဆက်မှု အောင်မြင်ပါသည်။")
        
        # Admin Panel
        st.divider()
        st.subheader("🔑 Admin Panel")
        correct_password = "1234"
        password_input = st.text_input("စစ်ဆေးရန် Password ရိုက်ပါ", type="password")
        
        if password_input == correct_password:
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
            
    except Exception as e:
        st.error(f"⚠️ Worksheet Error: {e}")
        st.info("နင့် Google Sheet ထဲမှာ 'Attendance' နဲ့ 'Leave_Requests' ဆိုတဲ့ Tab အမည်တွေ ရှိမရှိ ပြန်စစ်ပေးပါ။")
else:
    st.warning("⚠️ Google Sheet နှင့် ချိတ်ဆက်၍ မရသေးပါ။")
