import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 1. GOOGLE SHEETS SETUP ---
st.set_page_config(page_title="Staff Attendance System", layout="wide")

def init_connection():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Secrets ထဲက key ကို ယူသုံးခြင်း
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # သင့် Google Sheet ID (မူရင်းအတိုင်း ထားပါ)
        SHEET_ID = "1Lnh_L7v7vDs-6WRosR1KXzNSoqAN1jgAKRc5VvAtpFs"
        return client.open_by_key(SHEET_ID)
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

sh = init_connection()

if sh:
    try:
        attendance_sheet = sh.worksheet("Attendance")
        leave_sheet = sh.worksheet("Leave_Requests")
        employee_list_sheet = sh.worksheet("Sheet1")
        settings_sheet = sh.worksheet("Settings")
    except Exception as e:
        st.error(f"❌ Worksheet Error: Tab အမည်များ မှားနေနိုင်ပါသည်။ ({e})")
        st.stop()
else:
    st.stop()

# --- 2. SIDEBAR MENU ---
menu = st.sidebar.selectbox("Main Menu", ["ရုံးတက်/ရုံးဆင်း လုပ်ရန်", "ခွင့်တိုင်ရန်", "Admin Panel"])

# --- 3. ATTENDANCE SECTION ---
if menu == "ရုံးတက်/ရုံးဆင်း လုပ်ရန်":
    st.title("📸 Staff Attendance System")
    
    names = employee_list_sheet.col_values(1)[1:]
    selected_name = st.selectbox("သင့်အမည်ကို ရွေးပါ", names)
    status = st.radio("အမျိုးအစား", ["ရုံးတက် (Check-In)", "ရုံးဆင်း (Check-Out)"])
    
    img_file = st.camera_input("ဓာတ်ပုံရိုက်ပါ")
    
    if img_file and st.button("Submit"):
        now = datetime.now()
        attendance_sheet.append_row([selected_name, status, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])
        st.success(f"✅ {selected_name} အတွက် {status} မှတ်တမ်းတင်ပြီးပါပြီ။")

# --- 4. LEAVE REQUEST SECTION ---
elif menu == "ခွင့်တိုင်ရန်":
    st.title("📝 Leave Request Form")
    
    # Settings ထဲမှ စည်းကမ်းချက်များကို ဖတ်ခြင်း
    rules = settings_sheet.cell(2, 2).value if settings_sheet else "စည်းကမ်းချက်များ မရှိသေးပါ။"
    
    with st.expander("⚠️ ခွင့်မတိုင်မီ စည်းကမ်းချက်များကို ဖတ်ရှုရန်"):
        st.info(rules)
        agree = st.checkbox("ကျွန်ုပ် စည်းကမ်းချက်များကို သဘောတူပါသည်။")
        
    if agree:
        names = employee_list_sheet.col_values(1)[1:]
        selected_name = st.selectbox("အမည်ရွေးပါ", names)
        reason = st.text_area("အကြောင်းအရင်း")
        
        if st.button("Confirm Leave Request"):
            if reason:
                now = datetime.now()
                leave_sheet.append_row([selected_name, reason, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])
                
                # Viber Link
                msg = f"ခွင့်တိုင်ကြားစာ\nအမည်: {selected_name}\nအကြောင်းရင်း: {reason}"
                viber_url = f"viber://forward?text={msg}"
                
                st.success("✅ ခွင့်တိုင်ကြားမှု အောင်မြင်ပါသည်။")
                st.markdown(f'[🟣 Viber သို့ ပို့ရန် နှိပ်ပါ]({viber_url})')
            else:
                st.warning("⚠️ ခွင့်တိုင်ရသည့် အကြောင်းအရင်းကို ရေးသားပေးပါ။")

# --- 5. ADMIN PANEL SECTION ---
elif menu == "Admin Panel":
    st.title("🔑 Admin Control")
    
    # Google Sheet ရဲ့ Settings tab၊ Cell A1 ထဲက password ကို လှမ်းဖတ်ခြင်း
    try:
        # (1, 1) သည် Row 1, Column A (A1) ကို ဆိုလိုသည်
        correct_password = settings_sheet.cell(1, 1).value 
    except:
        # Sheet ထဲတွင် ဖတ်၍မရပါက အောက်ပါ password ကို default သုံးမည်
        correct_password = "1234" 

    password_input = st.text_input("Password ရိုက်ထည့်ပါ", type="password")
    
    if password_input == correct_password:
        st.success("Admin Login Successful")
        tab1, tab2 = st.tabs(["ရုံးတက်/ဆင်း မှတ်တမ်းများ", "ခွင့်တိုင်ကြားမှု မှတ်တမ်းများ"])
        
        with tab1:
            st.subheader("ဝန်ထမ်း ရုံးတက်/ဆင်း စာရင်း")
            # Attendance sheet ထဲက အချက်အလက်အားလုံးကို ပြသရန်
            data1 = attendance_sheet.get_all_records()
            st.dataframe(data1)
            
        with tab2:
            st.subheader("ခွင့်တိုင်ကြားထားသည့် စာရင်း")
            # Leave Requests sheet ထဲက အချက်အလက်အားလုံးကို ပြသရန်
            data2 = leave_sheet.get_all_records()
            st.dataframe(data2)
            
    elif password_input != "":
        st.error("❌ Password မှားယွင်းနေပါသည်။")
        st.info("💡 Google Sheet ရဲ့ Settings Tab (A1) ထဲမှာ Password ကို ပြန်စစ်ကြည့်ပါဗျာ။")
