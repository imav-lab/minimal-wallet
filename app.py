import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import date

# --- CONFIGURATION ---
PAGE_TITLE = "Minimal Wallet"
PAGE_ICON = "🐉"
LAYOUT = "wide"

# Filenames
FILE_TRANSACTIONS = 'transactions.csv'
FILE_CAT_EXPENSES = 'categories_expenses.csv'
FILE_CAT_INCOME = 'categories_income.csv'

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

# --- 🎨 THEME ENGINE ---

def apply_synthwave_flat():
    """Synthwave style but without the Neon Glow (Flat design)."""
    st.markdown(
        """
        <style>
        .stApp { background-color: #2b213a; }
        [data-testid="stSidebar"] { background-color: #1f1a24; border-right: 1px solid #ff71ce; }
        h1, h2, h3 { color: #ff71ce !important; font-family: 'Courier New', monospace; }
        p, label, .stMarkdown, div { color: #01cdfe !important; font-family: 'Courier New', monospace; }
        .stButton>button { color: #fff01f !important; background-color: #2b213a !important; border: 1px solid #01cdfe !important; }
        .stButton>button:hover { background-color: #01cdfe !important; color: #2b213a !important; }
        .stTextInput>div>div>input, .stNumberInput>div>div>input { color: #fff01f; background-color: #1f1a24; border: 1px solid #ff71ce; }
        </style>
        """, unsafe_allow_html=True
    )

def apply_solarized_dark():
    """The classic Solarized Dark theme."""
    st.markdown(
        """
        <style>
        .stApp { background-color: #002b36; }
        [data-testid="stSidebar"] { background-color: #073642; border-right: 1px solid #586e75; }
        h1, h2, h3 { color: #b58900 !important; font-family: 'Consolas', monospace; }
        p, label, .stMarkdown, div { color: #839496 !important; font-family: 'Consolas', monospace; }
        .stButton>button { color: #93a1a1 !important; background-color: #073642 !important; border: 1px solid #586e75 !important; }
        .stButton>button:hover { background-color: #586e75 !important; color: #fdf6e3 !important; }
        .stTextInput>div>div>input, .stNumberInput>div>div>input { color: #839496; background-color: #073642; border: 1px solid #2aa198; }
        .streamlit-expanderHeader { background-color: #073642; color: #2aa198; }
        </style>
        """, unsafe_allow_html=True
    )

def apply_solarized_light():
    """Solarized Light - Warm, creamy, and professional."""
    st.markdown(
        """
        <style>
        /* Base3 - Background (Cream) */
        .stApp {
            background-color: #fdf6e3;
        }
        
        /* Base2 - Sidebar */
        [data-testid="stSidebar"] {
            background-color: #eee8d5;
            border-right: 1px solid #93a1a1;
        }

        /* Base00 - Content Text (Dark Grey/Blue) */
        h1, h2, h3 {
            color: #cb4b16 !important; /* Orange */
            font-family: 'Consolas', 'Monaco', monospace;
        }
        
        p, label, .stMarkdown, div, span {
            color: #657b83 !important; /* Base00 */
            font-family: 'Consolas', 'Monaco', monospace;
        }

        /* Buttons */
        .stButton>button {
            color: #657b83 !important; 
            background-color: #eee8d5 !important; 
            border: 1px solid #93a1a1 !important;
        }
        .stButton>button:hover {
            background-color: #93a1a1 !important; 
            color: #fdf6e3 !important; 
        }

        /* Inputs - White background for contrast */
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            color: #586e75; /* Base01 */
            background-color: #ffffff;
            border: 1px solid #2aa198; /* Cyan accent */
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #eee8d5;
            color: #2aa198; 
        }
        
        /* Tables (fix font color in tables) */
        [data-testid="stDataFrame"] {
            color: #657b83;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- FUNCTIONS ---
def init_files():
    if not os.path.exists(FILE_TRANSACTIONS):
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Description", "Amount", "Is_Recurring"])
        df.to_csv(FILE_TRANSACTIONS, index=False)
    
    if not os.path.exists(FILE_CAT_EXPENSES):
        defaults = ["Supermarket 🛒", "Fuel ⛽", "Food 🍔", "Bills 📄", "Rent 🏠", "Subscriptions 📺"]
        pd.DataFrame(defaults, columns=["Category"]).to_csv(FILE_CAT_EXPENSES, index=False)

    if not os.path.exists(FILE_CAT_INCOME):
        defaults = ["Salary 💼", "Freelance 💻", "Gifts 🎁"]
        pd.DataFrame(defaults, columns=["Category"]).to_csv(FILE_CAT_INCOME, index=False)

def get_categories(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df["Category"].tolist()
    return []

def add_category_to_file(file_path, new_cat):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if new_cat not in df["Category"].values:
            new_row = pd.DataFrame({"Category": [new_cat]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file_path, index=False)
            return True
    return False

def add_transaction(t_type, category, description, amount, is_recurring=False):
    new_data = {
        "Date": [date.today()],
        "Type": [t_type],
        "Category": [category],
        "Description": [description],
        "Amount": [amount],
        "Is_Recurring": [is_recurring]
    }
    new_df = pd.DataFrame(new_data)
    new_df.to_csv(FILE_TRANSACTIONS, mode='a', header=not os.path.exists(FILE_TRANSACTIONS), index=False)

# --- STARTUP ---
init_files()

# --- SIDEBAR & THEME SELECTOR ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    # 1. THEME SWITCHER
    theme_choice = st.selectbox(
        "🎨 Choose Theme:", 
        ["Classic Dark", "Synthwave Flat", "Solarized Dark", "Solarized Light ☀️"]
    )
    
    if theme_choice == "Synthwave Flat":
        apply_synthwave_flat()
    elif theme_choice == "Solarized Dark":
        apply_solarized_dark()
    elif theme_choice == "Solarized Light ☀️":
        apply_solarized_light()
    
    st.divider()
    
    # 2. QUICK ADD CATEGORY
    st.header("Quick Add Category")
    cat_type = st.radio("Type:", ["Expenses", "Income"])
    new_cat_name = st.text_input("New Name:")
    if st.button("➕ Add"):
        if new_cat_name:
            target = FILE_CAT_EXPENSES if cat_type == "Expenses" else FILE_CAT_INCOME
            add_category_to_file(target, new_cat_name)
            st.success(f"Added {new_cat_name}")
            st.rerun()

st.title("💾Minimal Wallet")

# --- MAIN TABS ---
tab_expenses, tab_income, tab_overview, tab_edit, tab_cats = st.tabs([
    "💸 Expenses", "💰 Income", "📈 Overview", "📝 Transactions", "🗂️ Categories"
])

# --- TAB 1: EXPENSES ---
with tab_expenses:
    st.subheader("New Expense")
    cats = get_categories(FILE_CAT_EXPENSES)
    cols = st.columns(2)
    for i, cat in enumerate(cats):
        with cols[i % 2]:
            with st.expander(cat, expanded=False):
                with st.form(key=f"exp_{cat}"):
                    amt = st.number_input("Amount (€)", min_value=0.0, step=1.0, key=f"amt_{cat}")
                    desc = st.text_input("Description", key=f"desc_{cat}")
                    is_rec = st.checkbox("Monthly Fixed Cost", key=f"rec_{cat}")
                    
                    if st.form_submit_button("✅ Charge"):
                        if amt > 0:
                            add_transaction("EXPENSE", cat, desc if desc else cat, amt, is_rec)
                            st.toast(f"Charged {amt}€ to {cat}")
                        else:
                            st.warning("Amount needed")

# --- TAB 2: INCOME ---
with tab_income:
    st.subheader("New Income")
    cats = get_categories(FILE_CAT_INCOME)
    cols = st.columns(2)
    for i, cat in enumerate(cats):
        with cols[i % 2]:
            with st.expander(cat, expanded=False):
                with st.form(key=f"inc_{cat}"):
                    amt = st.number_input("Amount (€)", min_value=0.0, step=10.0, key=f"inc_amt_{cat}")
                    desc = st.text_input("Note", key=f"inc_desc_{cat}")
                    if st.form_submit_button("💾 Save Income"):
                        if amt > 0:
                            add_transaction("INCOME", cat, desc if desc else cat, amt, False)
                            st.toast(f"Added Income {amt}€")

# --- TAB 3: OVERVIEW ---
with tab_overview:
    if os.path.exists(FILE_TRANSACTIONS):
        df = pd.read_csv(FILE_TRANSACTIONS)
        if not df.empty:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month_Year'] = df['Date'].dt.strftime('%Y-%m')

            st.subheader("📅 Monthly Balance")
            monthly_data = df.groupby(['Month_Year', 'Type'])['Amount'].sum().unstack(fill_value=0)
            
            if 'INCOME' not in monthly_data.columns: monthly_data['INCOME'] = 0
            if 'EXPENSE' not in monthly_data.columns: monthly_data['EXPENSE'] = 0
            
            monthly_data['BALANCE'] = monthly_data['INCOME'] - monthly_data['EXPENSE']
            
            st.dataframe(monthly_data.style.format("{:.2f} €")
                         .background_gradient(subset=['BALANCE'], cmap="RdYlGn", vmin=-500, vmax=500), 
                         use_container_width=True)

            st.divider()
            st.subheader("🔮 Fixed Costs Forecast")
            recurring_df = df[(df['Type'] == "EXPENSE") & (df['Is_Recurring'] == True)]
            
            if not recurring_df.empty:
                last_30_days = pd.Timestamp.now() - pd.Timedelta(days=30)
                active_recurring = recurring_df[recurring_df['Date'] >= last_30_days]
                forecast_total = active_recurring['Amount'].sum()
                
                c1, c2 = st.columns([1, 3])
                c1.metric("Predicted Fixed Costs", f"{forecast_total} €")
                with c2:
                    st.dataframe(active_recurring[['Category', 'Description', 'Amount']], hide_index=True)
            else:
                st.info("No recurring expenses yet.")
        else:
            st.write("No data yet.")

# --- TAB 4: EDIT TRANSACTIONS ---
with tab_edit:
    st.subheader("📝 Edit Data")
    if os.path.exists(FILE_TRANSACTIONS):
        df = pd.read_csv(FILE_TRANSACTIONS)
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="editor_trans")
        if st.button("💾 Save Transactions"):
            edited_df.to_csv(FILE_TRANSACTIONS, index=False)
            st.success("Transactions Saved!")
            st.rerun()

# --- TAB 5: MANAGE CATEGORIES ---
with tab_cats:
    st.subheader("🗂️ Manage Categories")
    col1, col2 = st.columns(2)

    with col1:
        st.write("💸 **Expense Categories**")
        if os.path.exists(FILE_CAT_EXPENSES):
            df_exp = pd.read_csv(FILE_CAT_EXPENSES)
            edited_exp = st.data_editor(df_exp, num_rows="dynamic", key="editor_exp")
            if st.button("💾 Save Expenses Cats"):
                edited_exp.to_csv(FILE_CAT_EXPENSES, index=False)
                st.success("Updated!")
                st.rerun()

    with col2:
        st.write("💰 **Income Categories**")
        if os.path.exists(FILE_CAT_INCOME):
            df_inc = pd.read_csv(FILE_CAT_INCOME)
            edited_inc = st.data_editor(df_inc, num_rows="dynamic", key="editor_inc")
            if st.button("💾 Save Income Cats"):
                edited_inc.to_csv(FILE_CAT_INCOME, index=False)
                st.success("Updated!")
                st.rerun()