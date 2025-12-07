# 💳 Smart Wallet

A **Simple**, **Minimal**, and **Self-hosted** personal finance tool built for privacy enthusiasts.

Designed to run locally on your home server (Proxmox, Raspberry Pi, etc.) without relying on external cloud services or complex databases.

## 🚀 Key Features

* **Simple:** Built with Python & Streamlit. No database setup required (uses local CSV files).
* **Minimal UI:** Clean interface with support for multiple themes (Solarized Light/Dark, Synthwave '84).
* **Privacy-First:** Your financial data never leaves your machine.
* **Forecasting:** Automatically predicts next month's fixed costs based on recurring expenses.
* **Edit & Manage:** Full control to edit or delete categories and transactions via the UI.

## 🛠️ Tech Stack

* **Python 3.x**
* **Streamlit** (Frontend/Backend)
* **Pandas** (Data handling)

## 📦 How to Run

1.  Clone the repository:
    ```bash
    git clone [https://github.com/TO_ONOMA_SOU/smart-wallet.git](https://github.com/imav-lab/smart-wallet.git)
    cd smart-wallet
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    streamlit run app.py
    ```

---
*Created by Giannis*
