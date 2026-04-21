#############################################################################
# login_page.py
#
# Fake login page for development and database testing.
# Bypasses real authentication by always signing in as FAKE_USER_ID.
# Change FAKE_USER_ID to simulate a different user from the BigQuery Users table.
#############################################################################

import streamlit as st

# Change this variable to switch which user's data is loaded across the app
FAKE_USER_ID = 'user1'


def display_login_page():
    st.set_page_config(layout="centered", page_title="Sign In")

    # ── Inject fonts + all CSS first, in its own isolated markdown call ──
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1a1a1a;
        }

        #MainMenu, footer, header { visibility: hidden; }

        .logo-container {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 110px;
            margin-bottom: 20px;
        }

        .login-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 40px 36px 28px 36px;
            font-family: 'DM Sans', sans-serif;
        }

        .card-title {
            font-family: 'DM Serif Display', serif;
            font-style: italic;
            font-size: 1.8rem;
            color: rgba(255, 255, 255, 0.93);
            margin-bottom: 28px;
            text-align: center;
        }

        .field-group {
            margin-bottom: 20px;
        }

        .field-label {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .field-display {
            font-family: 'DM Sans', sans-serif;
            font-size: 1rem;
            color: rgba(255, 255, 255, 0.93);
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 6px;
            padding: 12px 14px;
            width: 100%;
            box-sizing: border-box;
        }

        .stButton > button {
            background-color: #f08080 !important;
            color: #1a1a1a !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 12px 0 !important;
            width: 100% !important;
            cursor: pointer !important;
            margin-top: 8px !important;
            transition: background-color 0.2s ease !important;
        }

        .stButton > button:hover {
            background-color: #d96060 !important;
            border: none !important;
        }

        .success-card {
            background: rgba(240, 128, 128, 0.12);
            border: 1px solid rgba(240, 128, 128, 0.35);
            border-radius: 12px;
            padding: 32px 36px;
            font-family: 'DM Sans', sans-serif;
            text-align: center;
        }

        .success-title {
            font-family: 'DM Serif Display', serif;
            font-style: italic;
            font-size: 1.5rem;
            color: rgba(255, 255, 255, 0.93);
            margin-bottom: 10px;
        }

        .success-sub {
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.6);
        }

        .success-user {
            color: #f08080;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:

        # ── Signed-in state (after button click + rerun) ─────────────────
        if st.session_state.get('logged_in'):
            user_id = st.session_state.get('user_id', FAKE_USER_ID)
            st.markdown(
                f"""
                <div class="logo-container"></div>
                <div class="success-card">
                  <div class="success-title">Signed in</div>
                  <div class="success-sub">
                    Authenticated as <span class="success-user">{user_id}</span>.<br>
                    Navigate to the app to continue.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # ── Logo placeholder ─────────────────────────────────────────────
        st.markdown('<div class="logo-container"></div>', unsafe_allow_html=True)

        # ── Login card ───────────────────────────────────────────────────
        st.markdown(
            """
            <div class="login-card">
              <div class="card-title">Sign In</div>

              <div class="field-group">
                <div class="field-label">Email</div>
                <div class="field-display">exampleemail@gmail.com</div>
              </div>

              <div class="field-group">
                <div class="field-label">Password</div>
                <div class="field-display">&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Sign In button ───────────────────────────────────────────────
        if st.button("Sign In", use_container_width=True):
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = FAKE_USER_ID
            st.rerun()


if __name__ == '__main__':
    display_login_page()