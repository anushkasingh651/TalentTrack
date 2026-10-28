from pathlib import Path
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TalentTrack | People Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DESIGN SYSTEM
# =========================================================

NAVY = "#172554"
BLUE = "#3157D5"
CYAN = "#0F9FAD"
PURPLE = "#7957D5"
ORANGE = "#E89436"
GREEN = "#16856B"
RED = "#D94F5C"
INK = "#17243B"
MUTED = "#53647D"
BORDER = "#DFE6F0"
BG = "#F4F7FC"
WHITE = "#FFFFFF"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {
        --navy: #172554;
        --blue: #3157D5;
        --ink: #17243B;
        --muted: #53647D;
        --border: #DFE6F0;
        --background: #F4F7FC;
    }

    /* Hide Streamlit chrome */
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer {
        display: none !important;
    }

    /* Global typography */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background: var(--background);
        color: var(--ink);
    }

    .block-container {
        max-width: 1550px;
        padding-top: 1.4rem !important;
        padding-bottom: 2.5rem !important;
    }

    /* Make text bold and readable */
    h1, h2, h3, h4, h5, h6 {
        color: #172554 !important;
        font-weight: 900 !important;
        letter-spacing: -0.5px;
    }

    p, label, li {
        color: #263650;
        font-weight: 650;
    }

    [data-testid="stMarkdownContainer"] p {
        font-weight: 650;
    }

    [data-testid="stCaptionContainer"] {
        color: #53647D !important;
        font-weight: 700 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #DFE6F0;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.3rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #172554 !important;
        font-weight: 900 !important;
    }

    section[data-testid="stSidebar"] label {
        color: #263650 !important;
        font-weight: 800 !important;
    }

    /* Brand */
    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 8px 0 22px 0;
        border-bottom: 1px solid #E7ECF4;
        margin-bottom: 22px;
    }

    .brand-icon {
        width: 43px;
        height: 43px;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #172554;
        color: #FFFFFF !important;
        font-size: 22px;
        font-weight: 900 !important;
        box-shadow: 0 7px 15px rgba(23, 37, 84, 0.18);
    }

    .brand-name {
        color: #172554 !important;
        font-size: 23px;
        font-weight: 900 !important;
        letter-spacing: -1px;
    }

    .brand-subtitle {
        color: #53647D !important;
        font-size: 9px;
        font-weight: 900 !important;
        letter-spacing: 1.5px;
        margin-top: 3px;
    }

    /* Top status strip */
    .status-strip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        padding: 13px 17px;
        background: #FFFFFF;
        border: 1px solid #DFE6F0;
        border-radius: 13px;
        margin-bottom: 25px;
        box-shadow: 0 3px 10px rgba(23, 37, 84, 0.025);
    }

    .status-left {
        color: #172554 !important;
        font-size: 12px;
        font-weight: 900 !important;
    }

    .status-right {
        color: #53647D !important;
        font-size: 11px;
        font-weight: 800 !important;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #16856B;
        border-radius: 50%;
        margin-right: 7px;
    }

    /* Section heading */
    .section-title {
        color: #172554 !important;
        font-size: 22px;
        font-weight: 900 !important;
        letter-spacing: -0.7px;
        margin-top: 26px;
        margin-bottom: 4px;
    }

    .section-description {
        color: #53647D !important;
        font-size: 12px;
        font-weight: 700 !important;
        line-height: 1.8;
        margin-bottom: 17px;
    }

    /* KPI cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #DFE6F0;
        border-radius: 15px;
        padding: 19px;
        min-height: 145px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(23, 37, 84, 0.035);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(23, 37, 84, 0.09);
    }

    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--accent, #3157D5);
    }

    .kpi-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
    }

    .kpi-label {
        color: #53647D !important;
        font-size: 10px;
        font-weight: 900 !important;
        letter-spacing: 0.55px;
        line-height: 1.6;
    }

    .kpi-icon {
        width: 33px;
        height: 33px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--icon-bg, #EDF2FF);
        color: var(--accent, #3157D5) !important;
        font-size: 16px;
        font-weight: 900 !important;
        flex-shrink: 0;
    }

    .kpi-value {
        color: #172554 !important;
        font-size: 31px;
        font-weight: 900 !important;
        letter-spacing: -1.1px;
        line-height: 1.2;
        margin-top: 17px;
    }

    .kpi-note {
        color: #53647D !important;
        font-size: 10px;
        font-weight: 750 !important;
        margin-top: 9px;
        line-height: 1.5;
    }

    /* Chart containers */
    .chart-panel {
        background: #FFFFFF;
        border: 1px solid #DFE6F0;
        border-radius: 15px;
        padding: 18px;
        box-shadow: 0 4px 15px rgba(23, 37, 84, 0.025);
        margin-bottom: 15px;
    }

    .panel-title {
        color: #172554 !important;
        font-size: 15px;
        font-weight: 900 !important;
        margin-bottom: 4px;
    }

    .panel-subtitle {
        color: #53647D !important;
        font-size: 10px;
        font-weight: 700 !important;
        line-height: 1.7;
        margin-bottom: 8px;
    }

    /* Insight cards */
    .insight-card {
        background: #FFFFFF;
        border: 1px solid #DFE6F0;
        border-radius: 13px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0 3px 10px rgba(23, 37, 84, 0.025);
    }

    .insight-header {
        display: flex;
        align-items: center;
        gap: 9px;
        margin-bottom: 10px;
    }

    .insight-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 10px;
        background: #EDF2FF;
        color: #3157D5 !important;
        font-size: 15px;
        font-weight: 900 !important;
        flex-shrink: 0;
    }

    .insight-title {
        color: #172554 !important;
        font-size: 12px;
        font-weight: 900 !important;
    }

    .insight-text {
        color: #40516A !important;
        font-size: 11px;
        line-height: 1.9;
        font-weight: 700 !important;
    }

    /* Follow-up summary */
    .priority-card {
        background: #FFFFFF;
        border: 1px solid #DFE6F0;
        border-radius: 13px;
        padding: 17px;
        margin-bottom: 10px;
    }

    .priority-label {
        font-size: 10px;
        font-weight: 900 !important;
        letter-spacing: 0.5px;
    }

    .priority-number {
        color: #172554 !important;
        font-size: 28px;
        font-weight: 900 !important;
        margin-top: 7px;
    }

    .priority-note {
        color: #53647D !important;
        font-size: 10px;
        font-weight: 750 !important;
        margin-top: 4px;
    }

    /* Inputs */
    .stTextInput input,
    .stDateInput input {
        color: #172554 !important;
        font-weight: 750 !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 9px !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: #172554 !important;
        color: #FFFFFF !important;
        border: 1px solid #172554 !important;
        border-radius: 9px !important;
        min-height: 42px;
        font-weight: 900 !important;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #3157D5 !important;
        border-color: #3157D5 !important;
        color: #FFFFFF !important;
        box-shadow: 0 5px 12px rgba(49, 87, 213, 0.18);
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #DFE6F0;
        border-radius: 11px;
        overflow: hidden;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 11px;
        font-weight: 750 !important;
    }

    /* Footer */
    .footer {
        margin-top: 40px;
        padding: 20px 10px 8px 10px;
        border-top: 1px solid #DFE6F0;
        text-align: center;
        color: #53647D !important;
        font-size: 10px;
        line-height: 2;
        font-weight: 800 !important;
    }

    .footer-brand {
        color: #172554 !important;
        font-size: 13px;
        font-weight: 900 !important;
        letter-spacing: 0.5px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.7rem !important;
        }

        .kpi-card {
            padding: 14px;
            min-height: 125px;
        }

        .kpi-value {
            font-size: 25px;
        }

        .section-title {
            font-size: 19px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA LOADING
# =========================================================

DATA_PATH = Path(__file__).parent / "data" / "candidates.csv"

if not DATA_PATH.exists():
    st.error(
        "Dataset not found. Please place candidates.csv "
        "inside the project's data folder."
    )
    st.code("TalentTrack/data/candidates.csv")
    st.stop()

try:
    df = pd.read_csv(DATA_PATH)
except Exception as error:
    st.error(f"Unable to read the candidate dataset: {error}")
    st.stop()


REQUIRED_COLUMNS = [
    "Candidate ID",
    "Job Role",
    "Location",
    "Application Date",
    "Source",
    "Recruitment Stage",
    "Contact Status",
    "Interview Date",
    "Interview Status",
    "Follow-up Date",
]

missing_columns = [
    column for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

if df.empty:
    st.warning("The candidate dataset is empty.")
    st.stop()


DATE_COLUMNS = [
    "Application Date",
    "Interview Date",
    "Follow-up Date",
]

TEXT_COLUMNS = [
    "Candidate ID",
    "Job Role",
    "Location",
    "Source",
    "Recruitment Stage",
    "Contact Status",
    "Interview Status",
]

for column in DATE_COLUMNS:
    df[column] = pd.to_datetime(
        df[column],
        errors="coerce",
    )

for column in TEXT_COLUMNS:
    df[column] = (
        df[column]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def section_heading(title, description):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def show_kpi(column, label, value, note, accent, icon, icon_bg):
    with column:
        st.markdown(
            f"""
            <div class="kpi-card"
                 style="--accent:{accent};--icon-bg:{icon_bg};">
                <div class="kpi-top">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-icon">{icon}</div>
                </div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_priority_card(column, label, value, note, accent):
    with column:
        st.markdown(
            f"""
            <div class="priority-card">
                <div class="priority-label" style="color:{accent};">
                    {label}
                </div>
                <div class="priority-number">{value}</div>
                <div class="priority-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def panel_heading(title, subtitle):
    st.markdown(
        f"""
        <div class="panel-title">{title}</div>
        <div class="panel-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color=INK,
            size=11,
        ),
        margin=dict(l=8, r=15, t=20, b=10),
        hoverlabel=dict(
            bgcolor=WHITE,
            font_size=12,
            font_color=INK,
            font_family="Inter",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        tickfont=dict(
            color=MUTED,
            size=10,
        ),
        title_font=dict(
            color=INK,
            size=11,
        ),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF1F7",
        zeroline=False,
        tickfont=dict(
            color=MUTED,
            size=10,
        ),
        title_font=dict(
            color=INK,
            size=11,
        ),
    )

    return fig


def add_insight(icon, title, description):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-header">
                <div class="insight-icon">{icon}</div>
                <div class="insight-title">{title}</div>
            </div>
            <div class="insight-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">T</div>
            <div>
                <div class="brand-name">
                    TalentTrack<span style="color:#3157D5;">.</span>
                </div>
                <div class="brand-subtitle">
                    PEOPLE ANALYTICS
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Dashboard Controls")
    st.caption("Use filters to explore recruitment data.")

    selected_roles = st.multiselect(
        "Job Role",
        options=sorted(df["Job Role"].unique().tolist()),
        default=sorted(df["Job Role"].unique().tolist()),
        key="roles_filter",
    )

    selected_locations = st.multiselect(
        "Location",
        options=sorted(df["Location"].unique().tolist()),
        default=sorted(df["Location"].unique().tolist()),
        key="locations_filter",
    )

    selected_stages = st.multiselect(
        "Recruitment Stage",
        options=sorted(df["Recruitment Stage"].unique().tolist()),
        default=sorted(df["Recruitment Stage"].unique().tolist()),
        key="stages_filter",
    )

    selected_sources = st.multiselect(
        "Candidate Source",
        options=sorted(df["Source"].unique().tolist()),
        default=sorted(df["Source"].unique().tolist()),
        key="sources_filter",
    )

    search_candidate = st.text_input(
        "Search Candidate ID",
        placeholder="Type candidate ID...",
        key="candidate_search",
    )

    valid_application_dates = df["Application Date"].dropna()

    selected_date_range = None

    if not valid_application_dates.empty:
        min_date = valid_application_dates.min().date()
        max_date = valid_application_dates.max().date()

        selected_date_range = st.date_input(
            "Application Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="application_date_filter",
        )

    st.markdown("---")

    if st.button("Reset All Filters", width="stretch"):
        for key in [
            "roles_filter",
            "locations_filter",
            "stages_filter",
            "sources_filter",
            "candidate_search",
            "application_date_filter",
        ]:
            st.session_state.pop(key, None)

        st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div style="
            background:#F0F4FF;
            border:1px solid #DCE5FF;
            padding:15px;
            border-radius:12px;
        ">
            <div style="
                font-size:11px;
                color:#172554;
                font-weight:900;
                margin-bottom:8px;
            ">
                PROJECT INFORMATION
            </div>
            <div style="
                color:#40516A;
                font-size:11px;
                font-weight:700;
                line-height:1.9;
            ">
                Recruitment pipeline monitoring<br>
                Candidate sourcing analytics<br>
                Interview and follow-up tracking<br>
                Exportable candidate records
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if selected_roles:
    filtered_df = filtered_df[
        filtered_df["Job Role"].isin(selected_roles)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_locations:
    filtered_df = filtered_df[
        filtered_df["Location"].isin(selected_locations)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_stages:
    filtered_df = filtered_df[
        filtered_df["Recruitment Stage"].isin(selected_stages)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_sources:
    filtered_df = filtered_df[
        filtered_df["Source"].isin(selected_sources)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if search_candidate.strip():
    filtered_df = filtered_df[
        filtered_df["Candidate ID"].str.contains(
            search_candidate.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ]

if (
    isinstance(selected_date_range, (tuple, list))
    and len(selected_date_range) == 2
):
    start_date, end_date = selected_date_range

    application_date_only = filtered_df["Application Date"].dt.date

    date_mask = application_date_only.between(
        start_date,
        end_date,
    )

    filtered_df = filtered_df[
        date_mask | filtered_df["Application Date"].isna()
    ]


# =========================================================
# DASHBOARD STATUS STRIP
# =========================================================

st.markdown(
    f"""
    <div class="status-strip">
        <div class="status-left">
            <span class="status-dot"></span>
            RECRUITMENT ANALYTICS WORKSPACE
        </div>
        <div class="status-right">
            {len(filtered_df):,} MATCHING CANDIDATES
            &nbsp; · &nbsp;
            UPDATED {date.today().strftime("%d %b %Y").upper()}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# RECRUITMENT OVERVIEW
# =========================================================

section_heading(
    "Recruitment Overview",
    "A clear view of candidate volume, recruitment progress and hiring outcomes.",
)

total_candidates = len(filtered_df)

stage_lower = filtered_df["Recruitment Stage"].str.lower()

shortlisted_count = int(
    stage_lower.isin(
        [
            "shortlisted",
            "interview scheduled",
            "interview completed",
            "selected",
        ]
    ).sum()
)

interview_scheduled = int(
    (stage_lower == "interview scheduled").sum()
)

selected_count = int(
    (stage_lower == "selected").sum()
)

selection_rate = (
    selected_count / total_candidates * 100
    if total_candidates
    else 0
)

kpi_columns = st.columns(4, gap="medium")

show_kpi(
    kpi_columns[0],
    "TOTAL CANDIDATES",
    f"{total_candidates:,}",
    "Candidate records matching filters",
    BLUE,
    "01",
    "#EDF2FF",
)

show_kpi(
    kpi_columns[1],
    "SHORTLISTED / INTERVIEW+",
    f"{shortlisted_count:,}",
    "Shortlisted, interview or selected",
    PURPLE,
    "02",
    "#F0EBFF",
)

show_kpi(
    kpi_columns[2],
    "INTERVIEWS SCHEDULED",
    f"{interview_scheduled:,}",
    "Candidates at scheduled stage",
    CYAN,
    "03",
    "#E6F8FA",
)

show_kpi(
    kpi_columns[3],
    "SELECTED CANDIDATES",
    f"{selected_count:,}",
    f"Selection rate: {selection_rate:.1f}%",
    GREEN,
    "04",
    "#E6F7F0",
)


# =========================================================
# PIPELINE ANALYTICS
# =========================================================

section_heading(
    "Pipeline Intelligence",
    "Understand where candidates are in the recruitment process and which roles attract the most applications.",
)

left_chart, right_chart = st.columns([1.25, 1], gap="medium")


with left_chart:

    with st.container(border=True):
        panel_heading(
            "Candidate Pipeline",
            "Candidate distribution across recruitment stages",
        )

        stage_order = [
            "New",
            "Screening",
            "Contacted",
            "Interested",
            "Shortlisted",
            "Interview Scheduled",
            "Interview Completed",
            "Selected",
            "Rejected",
        ]

        stage_counts = (
            filtered_df["Recruitment Stage"]
            .value_counts()
            .reindex(stage_order, fill_value=0)
            .rename_axis("Recruitment Stage")
            .reset_index(name="Candidates")
        )

        stage_counts = stage_counts.sort_values(
            "Candidates",
            ascending=True,
        )

        if stage_counts["Candidates"].sum() > 0:

            fig_pipeline = px.bar(
                stage_counts,
                x="Candidates",
                y="Recruitment Stage",
                orientation="h",
                text="Candidates",
                color="Candidates",
                color_continuous_scale=[
                    "#DDE6FF",
                    "#3157D5",
                    "#172554",
                ],
            )

            fig_pipeline.update_traces(
                textposition="outside",
                textfont=dict(
                    color=INK,
                    size=10,
                    family="Inter",
                ),
                cliponaxis=False,
            )

            fig_pipeline.update_layout(
                coloraxis_showscale=False,
                showlegend=False,
                xaxis_title="Number of Candidates",
                yaxis_title="",
            )

            st.plotly_chart(
                style_chart(fig_pipeline, 390),
                width="stretch",
            )

        else:
            st.info("No pipeline data matches the selected filters.")


with right_chart:

    with st.container(border=True):
        panel_heading(
            "Hiring by Job Role",
            "Share of candidate applications across job roles",
        )

        role_counts = (
            filtered_df["Job Role"]
            .value_counts()
            .rename_axis("Job Role")
            .reset_index(name="Candidates")
        )

        if not role_counts.empty:

            fig_roles = px.pie(
                role_counts,
                names="Job Role",
                values="Candidates",
                hole=0.68,
                color_discrete_sequence=[
                    BLUE,
                    PURPLE,
                    CYAN,
                    ORANGE,
                    GREEN,
                    "#D94F5C",
                    "#7892B8",
                ],
            )

            fig_roles.update_traces(
                textposition="inside",
                textinfo="percent",
                textfont=dict(
                    color=WHITE,
                    size=11,
                    family="Inter",
                ),
                marker=dict(
                    line=dict(
                        color=WHITE,
                        width=3,
                    )
                ),
            )

            fig_roles.add_annotation(
                text=(
                    f"<b>{total_candidates:,}</b>"
                    "<br><span style='font-size:10px'>CANDIDATES</span>"
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    color=NAVY,
                    size=21,
                    family="Inter",
                ),
            )

            fig_roles.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.24,
                    xanchor="center",
                    x=0.5,
                    font=dict(
                        color=INK,
                        size=10,
                    ),
                ),
            )

            st.plotly_chart(
                style_chart(fig_roles, 390),
                width="stretch",
            )

        else:
            st.info("No job-role data matches the selected filters.")


# =========================================================
# SOURCING ANALYTICS
# =========================================================

section_heading(
    "Sourcing & Engagement",
    "Measure candidate acquisition channels and monitor outreach progress.",
)

source_column, contact_column = st.columns(2, gap="medium")


with source_column:

    with st.container(border=True):

        panel_heading(
            "Candidate Sources",
            "Which channels contribute the most candidates?",
        )

        source_counts = (
            filtered_df["Source"]
            .value_counts()
            .rename_axis("Source")
            .reset_index(name="Candidates")
        )

        if not source_counts.empty:

            fig_source = px.bar(
                source_counts,
                x="Source",
                y="Candidates",
                text="Candidates",
                color="Source",
                color_discrete_sequence=[
                    BLUE,
                    PURPLE,
                    CYAN,
                    ORANGE,
                    GREEN,
                    "#D94F5C",
                ],
            )

            fig_source.update_traces(
                textposition="outside",
                textfont=dict(
                    color=INK,
                    size=10,
                    family="Inter",
                ),
            )

            fig_source.update_layout(
                showlegend=False,
                xaxis_title="Recruitment Source",
                yaxis_title="Candidates",
            )

            st.plotly_chart(
                style_chart(fig_source, 320),
                width="stretch",
            )

        else:
            st.info("No source data available.")


with contact_column:

    with st.container(border=True):

        panel_heading(
            "Contact Status",
            "Track candidate outreach and response status",
        )

        contact_counts = (
            filtered_df["Contact Status"]
            .value_counts()
            .rename_axis("Contact Status")
            .reset_index(name="Candidates")
        )

        if not contact_counts.empty:

            fig_contact = px.bar(
                contact_counts,
                x="Contact Status",
                y="Candidates",
                text="Candidates",
                color="Contact Status",
                color_discrete_sequence=[
                    BLUE,
                    CYAN,
                    GREEN,
                    ORANGE,
                    PURPLE,
                    "#D94F5C",
                ],
            )

            fig_contact.update_traces(
                textposition="outside",
                textfont=dict(
                    color=INK,
                    size=10,
                    family="Inter",
                ),
            )

            fig_contact.update_layout(
                showlegend=False,
                xaxis_title="Contact Status",
                yaxis_title="Candidates",
            )

            st.plotly_chart(
                style_chart(fig_contact, 320),
                width="stretch",
            )

        else:
            st.info("No contact-status data available.")


# =========================================================
# INTERVIEW TRACKER
# =========================================================

section_heading(
    "Interview Tracker",
    "Monitor scheduled interviews and interview outcomes.",
)

interview_df = filtered_df[
    filtered_df["Interview Date"].notna()
].copy()

interview_df = interview_df.sort_values(
    "Interview Date",
    ascending=True,
)

interview_columns = [
    "Candidate ID",
    "Job Role",
    "Location",
    "Recruitment Stage",
    "Interview Date",
    "Interview Status",
]

interview_display = interview_df[interview_columns].copy()

interview_display["Interview Date"] = (
    interview_display["Interview Date"].dt.date
)

with st.container(border=True):

    if not interview_display.empty:

        st.dataframe(
            interview_display,
            width="stretch",
            hide_index=True,
            height=270,
            column_config={
                "Interview Date": st.column_config.DateColumn(
                    "Interview Date",
                    format="DD MMM YYYY",
                ),
            },
        )

    else:
        st.info("No interview records match the current filters.")


# =========================================================
# FOLLOW-UP PRIORITIES
# =========================================================

section_heading(
    "Follow-up Priorities",
    "Identify candidates who need attention and keep recruitment follow-ups organized.",
)

today = date.today()

followup_df = filtered_df[
    filtered_df["Follow-up Date"].notna()
].copy()

followup_df = followup_df[
    ~followup_df["Recruitment Stage"].str.lower().isin(
        ["selected", "rejected"]
    )
].copy()

followup_df["Follow-up Date Only"] = (
    followup_df["Follow-up Date"].dt.date
)


def followup_priority(followup_date):
    if followup_date < today:
        return "Overdue"

    if followup_date == today:
        return "Due Today"

    return "Upcoming"


followup_df["Follow-up Priority"] = (
    followup_df["Follow-up Date Only"].apply(followup_priority)
)

followup_df = followup_df.sort_values("Follow-up Date")

overdue_count = int(
    (followup_df["Follow-up Priority"] == "Overdue").sum()
)

due_today_count = int(
    (followup_df["Follow-up Priority"] == "Due Today").sum()
)

upcoming_count = int(
    (followup_df["Follow-up Priority"] == "Upcoming").sum()
)

priority_columns = st.columns(3, gap="medium")

show_priority_card(
    priority_columns[0],
    "OVERDUE FOLLOW-UPS",
    f"{overdue_count:,}",
    "Scheduled before today",
    RED,
)

show_priority_card(
    priority_columns[1],
    "DUE TODAY",
    f"{due_today_count:,}",
    "Requires attention today",
    ORANGE,
)

show_priority_card(
    priority_columns[2],
    "UPCOMING FOLLOW-UPS",
    f"{upcoming_count:,}",
    "Scheduled for future dates",
    GREEN,
)


followup_display = followup_df[
    [
        "Candidate ID",
        "Job Role",
        "Recruitment Stage",
        "Contact Status",
        "Follow-up Date",
        "Follow-up Priority",
    ]
].copy()

followup_display["Follow-up Date"] = (
    followup_display["Follow-up Date"].dt.date
)

with st.container(border=True):

    if not followup_display.empty:

        st.dataframe(
            followup_display,
            width="stretch",
            hide_index=True,
            height=270,
            column_config={
                "Follow-up Date": st.column_config.DateColumn(
                    "Follow-up Date",
                    format="DD MMM YYYY",
                ),
            },
        )

    else:
        st.info("No follow-ups match the current filters.")


# =========================================================
# CANDIDATE DIRECTORY
# =========================================================

section_heading(
    "Candidate Directory",
    "Search, review and export candidate records using your selected filters.",
)

download_col, directory_count_col = st.columns([1, 2])

with download_col:

    csv_export = filtered_df.to_csv(
        index=False,
    ).encode("utf-8")

    st.download_button(
        label="Download Candidate CSV",
        data=csv_export,
        file_name="talenttrack_candidates.csv",
        mime="text/csv",
        width="stretch",
    )

with directory_count_col:

    st.markdown(
        f"""
        <div style="
            padding-top:13px;
            color:#172554;
            font-size:12px;
            font-weight:900;
        ">
            {len(filtered_df):,} RECORDS DISPLAYED
            <span style="color:#53647D;font-weight:750;">
                &nbsp; / &nbsp; {len(df):,} TOTAL RECORDS
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

directory_df = filtered_df.copy()

for column in DATE_COLUMNS:
    directory_df[column] = directory_df[column].dt.date

with st.container(border=True):

    st.dataframe(
        directory_df,
        width="stretch",
        hide_index=True,
        height=420,
        column_config={
            "Application Date": st.column_config.DateColumn(
                "Application Date",
                format="DD MMM YYYY",
            ),
            "Interview Date": st.column_config.DateColumn(
                "Interview Date",
                format="DD MMM YYYY",
            ),
            "Follow-up Date": st.column_config.DateColumn(
                "Follow-up Date",
                format="DD MMM YYYY",
            ),
        },
    )


# =========================================================
# AUTOMATED INSIGHTS
# =========================================================

section_heading(
    "Recruitment Insights",
    "Quick observations generated from the candidate records currently displayed.",
)

insight_left, insight_right = st.columns(2, gap="medium")


if filtered_df.empty:

    st.info("Select filters that return candidates to see recruitment insights.")

else:

    role_counts = filtered_df["Job Role"].value_counts()
    source_counts = filtered_df["Source"].value_counts()
    stage_counts = filtered_df["Recruitment Stage"].value_counts()

    with insight_left:

        if not role_counts.empty:

            top_role = role_counts.index[0]
            top_role_count = int(role_counts.iloc[0])
            top_role_share = top_role_count / total_candidates * 100

            add_insight(
                "01",
                "Most Represented Job Role",
                (
                    f"<b>{top_role}</b> has <b>{top_role_count}</b> candidates "
                    f"and accounts for <b>{top_role_share:.1f}%</b> of "
                    "the filtered dataset."
                ),
            )

        if not source_counts.empty:

            top_source = source_counts.index[0]
            top_source_count = int(source_counts.iloc[0])

            add_insight(
                "02",
                "Leading Candidate Source",
                (
                    f"<b>{top_source}</b> contributes the highest number "
                    f"of candidate records: <b>{top_source_count}</b>."
                ),
            )

    with insight_right:

        if not stage_counts.empty:

            top_stage = stage_counts.index[0]
            top_stage_count = int(stage_counts.iloc[0])

            add_insight(
                "03",
                "Largest Recruitment Stage",
                (
                    f"<b>{top_stage}</b> is the largest stage in the "
                    f"current pipeline, containing <b>{top_stage_count}</b> "
                    "candidates."
                ),
            )

        contacted_statuses = [
            "contacted",
            "replied",
            "responded",
            "connected",
        ]

        contacted_count = int(
            filtered_df["Contact Status"]
            .str.lower()
            .isin(contacted_statuses)
            .sum()
        )

        contact_rate = (
            contacted_count / total_candidates * 100
            if total_candidates
            else 0
        )

        add_insight(
            "04",
            "Candidate Outreach",
            (
                f"<b>{contact_rate:.1f}%</b> of candidate records have a "
                "contact status classified as contacted, replied, "
                "responded or connected."
            ),
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        <div class="footer-brand">
            TALENTTRACK<span style="color:#3157D5;">.</span>
        </div>
        Recruitment Analytics &nbsp; · &nbsp;
        Candidate Pipeline &nbsp; · &nbsp;
        Interview Tracking
        <br>
        Built with Python, Pandas, Streamlit and Plotly
        <br>
        Portfolio demonstration using fictional candidate data
    </div>
    """,
    unsafe_allow_html=True,
)