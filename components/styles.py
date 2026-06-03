THEMES = {
    "Light": {
        "bg": "#f6f8fb",
        "surface": "#ffffff",
        "surface_alt": "#eef3f8",
        "text": "#16202a",
        "muted": "#64748b",
        "border": "#dbe4ef",
        "primary": "#0f766e",
        "primary_soft": "#d9f3ef",
        "accent": "#2563eb",
        "success": "#15803d",
        "warning": "#b7791f",
        "danger": "#dc2626",
        "shadow": "0 18px 45px rgba(15, 23, 42, 0.08)",
        "chart_theme": "light",
    },
    "Dark": {
        "bg": "#111827",
        "surface": "#182231",
        "surface_alt": "#202c3c",
        "text": "#edf2f7",
        "muted": "#a8b3c5",
        "border": "#314156",
        "primary": "#2dd4bf",
        "primary_soft": "rgba(45, 212, 191, 0.14)",
        "accent": "#60a5fa",
        "success": "#4ade80",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "shadow": "0 18px 45px rgba(0, 0, 0, 0.22)",
        "chart_theme": "dark",
    },
}


def get_theme(mode="Light"):
    return THEMES.get(mode, THEMES["Light"])


def get_custom_css(mode="Light"):
    theme = get_theme(mode)
    return f"""
    <style>
        :root {{
            --app-bg: {theme['bg']};
            --app-surface: {theme['surface']};
            --app-surface-alt: {theme['surface_alt']};
            --app-text: {theme['text']};
            --app-muted: {theme['muted']};
            --app-border: {theme['border']};
            --app-primary: {theme['primary']};
            --app-primary-soft: {theme['primary_soft']};
            --app-accent: {theme['accent']};
            --app-success: {theme['success']};
            --app-warning: {theme['warning']};
            --app-danger: {theme['danger']};
            --app-shadow: {theme['shadow']};
        }}

        html, body, [data-testid="stAppViewContainer"] {{
            background: var(--app-bg);
            color: var(--app-text);
            font-family: Inter, "Segoe UI", Arial, sans-serif;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .main .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }}

        [data-testid="stSidebar"] {{
            background: var(--app-surface);
            border-right: 1px solid var(--app-border);
        }}

        [data-testid="stSidebar"] * {{
            color: var(--app-text);
        }}

        h1, h2, h3, h4, h5, h6, p, label, span, div {{
            color: var(--app-text);
        }}

        .app-hero {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 8px;
            padding: 22px 24px;
            margin-bottom: 18px;
            box-shadow: var(--app-shadow);
        }}

        .eyebrow {{
            color: var(--app-primary);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .hero-title {{
            color: var(--app-text);
            font-size: 30px;
            line-height: 1.18;
            font-weight: 800;
            margin: 0;
        }}

        .hero-subtitle {{
            color: var(--app-muted);
            font-size: 15px;
            line-height: 1.6;
            margin: 9px 0 0;
            max-width: 850px;
        }}

        .section-label {{
            color: var(--app-muted);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            margin: 12px 0 8px;
        }}

        .recommendation-card,
        .backup-card,
        .insight-card {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 8px;
            box-shadow: var(--app-shadow);
        }}

        .recommendation-card {{
            padding: 24px;
            border-top: 4px solid var(--app-primary);
        }}

        .recommendation-label,
        .rank-label {{
            color: var(--app-muted);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
        }}

        .recommendation-name {{
            color: var(--app-text);
            font-size: 28px;
            font-weight: 800;
            line-height: 1.2;
            margin-top: 8px;
        }}

        .recommendation-score {{
            color: var(--app-primary);
            font-size: 18px;
            font-weight: 800;
            margin-top: 8px;
        }}

        .recommendation-copy {{
            color: var(--app-muted);
            font-size: 14px;
            line-height: 1.55;
            margin-top: 14px;
        }}

        .backup-card {{
            padding: 16px;
            margin-bottom: 12px;
        }}

        .vendor-name {{
            color: var(--app-text);
            font-size: 17px;
            font-weight: 800;
            margin: 5px 0 9px;
        }}

        .business-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 14px;
            margin: 8px 0 18px;
        }}

        .business-title {{
            color: var(--app-text);
            font-size: 16px;
            font-weight: 800;
            line-height: 1.35;
            margin: 5px 0 9px;
        }}

        .score-badge {{
            display: inline-block;
            background: var(--app-primary-soft);
            color: var(--app-primary);
            border: 1px solid var(--app-border);
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 12px;
            font-weight: 800;
        }}

        .insight-card {{
            padding: 16px;
            margin: 8px 0 16px;
        }}

        .insight-card p {{
            color: var(--app-muted);
            line-height: 1.65;
            margin: 0;
        }}

        [data-testid="stMetric"] {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: var(--app-shadow);
        }}

        [data-testid="stMetricLabel"] p {{
            color: var(--app-muted);
            font-weight: 700;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--app-text);
        }}

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {{
            border: 1px solid var(--app-border);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: var(--app-shadow);
        }}

        .stButton > button,
        .stDownloadButton > button {{
            border-radius: 8px;
            border: 1px solid var(--app-border);
            background: var(--app-primary);
            color: #ffffff;
            font-weight: 800;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            border-color: var(--app-primary);
            filter: brightness(0.98);
        }}

        .stRadio [role="radiogroup"],
        .stSegmentedControl {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 8px;
            padding: 6px;
        }}

        .stSelectbox, .stNumberInput, .stSlider, .stTextInput {{
            color: var(--app-text);
        }}

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {{
            color: var(--app-text) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stSelectbox"],
        [data-testid="stSidebar"] [data-testid="stNumberInput"],
        [data-testid="stSidebar"] [data-testid="stSlider"],
        [data-testid="stSidebar"] [data-testid="stRadio"] {{
            color: var(--app-text) !important;
        }}

        input, textarea, select,
        [data-baseweb="input"] input,
        [data-baseweb="select"] > div {{
            background: var(--app-surface) !important;
            color: var(--app-text) !important;
            border-color: var(--app-border) !important;
        }}

        [data-baseweb="input"],
        [data-baseweb="select"],
        [data-baseweb="textarea"] {{
            background: var(--app-surface) !important;
            border-color: var(--app-border) !important;
        }}

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] > div {{
            background: var(--app-surface) !important;
            border: 1px solid var(--app-border) !important;
            border-radius: 8px !important;
            color: var(--app-text) !important;
        }}

        [data-baseweb="input"] input {{
            -webkit-text-fill-color: var(--app-text) !important;
            opacity: 1 !important;
        }}

        [data-baseweb="input"] button {{
            background: var(--app-surface-alt) !important;
            border-left: 1px solid var(--app-border) !important;
            color: var(--app-text) !important;
        }}

        [data-baseweb="input"] button svg,
        [data-baseweb="select"] svg {{
            fill: var(--app-text) !important;
            color: var(--app-text) !important;
        }}

        [data-baseweb="select"] div[role="button"],
        [data-baseweb="select"] div[aria-selected],
        [data-baseweb="select"] input {{
            color: var(--app-text) !important;
            -webkit-text-fill-color: var(--app-text) !important;
        }}

        [data-baseweb="popover"] > div,
        [role="listbox"] {{
            background: var(--app-surface) !important;
            border: 1px solid var(--app-border) !important;
            color: var(--app-text) !important;
        }}

        [role="option"] {{
            background: var(--app-surface) !important;
            color: var(--app-text) !important;
        }}

        [role="option"]:hover,
        [aria-selected="true"] {{
            background: var(--app-primary-soft) !important;
            color: var(--app-text) !important;
        }}

        [data-testid="stSlider"] [role="slider"] {{
            background: var(--app-primary) !important;
            border-color: var(--app-primary) !important;
        }}

        [data-testid="stSlider"] div[data-testid="stTickBar"] {{
            color: var(--app-muted) !important;
        }}

        [data-baseweb="radio"] {{
            background: transparent !important;
        }}

        [data-baseweb="radio"] div {{
            color: var(--app-text) !important;
        }}

        [data-testid="stSidebar"] div[data-baseweb="select"],
        [data-testid="stSidebar"] div[data-baseweb="input"] {{
            background: var(--app-surface-alt) !important;
            border-radius: 8px !important;
        }}

        [data-testid="stSidebar"] div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] div[data-baseweb="input"] > div {{
            background: var(--app-surface-alt) !important;
            border: 1px solid var(--app-border) !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] div[data-baseweb="select"] *,
        [data-testid="stSidebar"] div[data-baseweb="input"] *,
        [data-testid="stSidebar"] div[data-baseweb="radio"] * {{
            color: var(--app-text) !important;
            -webkit-text-fill-color: var(--app-text) !important;
        }}

        [data-testid="stSidebar"] div[data-baseweb="input"] input {{
            background: var(--app-surface-alt) !important;
            color: var(--app-text) !important;
            caret-color: var(--app-primary) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stNumberInput"] button,
        [data-testid="stSidebar"] div[data-baseweb="input"] button {{
            background: var(--app-surface) !important;
            border-color: var(--app-border) !important;
            color: var(--app-text) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover,
        [data-testid="stSidebar"] div[data-baseweb="input"] button:hover {{
            background: var(--app-primary-soft) !important;
            color: var(--app-primary) !important;
        }}

        [data-testid="stSidebar"] svg {{
            color: var(--app-text) !important;
            fill: currentColor !important;
        }}

        [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] > div {{
            color: var(--app-text) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stSlider"] div {{
            color: var(--app-muted) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {{
            background-color: var(--app-primary) !important;
            box-shadow: 0 0 0 4px var(--app-primary-soft) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            background: var(--app-primary) !important;
        }}

        [data-baseweb="popover"] ul,
        [data-baseweb="popover"] li,
        [data-baseweb="menu"] {{
            background: var(--app-surface) !important;
            color: var(--app-text) !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="select"],
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
        section[data-testid="stSidebar"] div[data-baseweb="input"],
        section[data-testid="stSidebar"] div[data-baseweb="input"] > div {{
            background-color: {theme['surface_alt']} !important;
            color: {theme['text']} !important;
            border-color: {theme['border']} !important;
            box-shadow: none !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="select"] *,
        section[data-testid="stSidebar"] div[data-baseweb="input"] *,
        section[data-testid="stSidebar"] div[data-baseweb="radio"] * {{
            color: {theme['text']} !important;
            -webkit-text-fill-color: {theme['text']} !important;
            fill: {theme['text']} !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="input"] input,
        section[data-testid="stSidebar"] input {{
            background-color: {theme['surface_alt']} !important;
            color: {theme['text']} !important;
            -webkit-text-fill-color: {theme['text']} !important;
            caret-color: {theme['primary']} !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="input"] button,
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {{
            background-color: {theme['surface']} !important;
            color: {theme['text']} !important;
            border-color: {theme['border']} !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button,
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button[kind],
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button[data-testid] {{
            background: {theme['surface_alt']} !important;
            background-color: {theme['surface_alt']} !important;
            color: {theme['text']} !important;
            border: 1px solid {theme['border']} !important;
            box-shadow: none !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover,
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button:focus {{
            background: {theme['primary_soft']} !important;
            background-color: {theme['primary_soft']} !important;
            color: {theme['primary']} !important;
            border-color: {theme['primary']} !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSlider"] *,
        section[data-testid="stSidebar"] [data-testid="stSlider"] span,
        section[data-testid="stSidebar"] [data-testid="stSlider"] p {{
            color: {theme['text']} !important;
            -webkit-text-fill-color: {theme['text']} !important;
        }}

        div[data-baseweb="popover"],
        div[data-baseweb="popover"] *,
        ul[role="listbox"],
        ul[role="listbox"] * {{
            background-color: {theme['surface']} !important;
            color: {theme['text']} !important;
            -webkit-text-fill-color: {theme['text']} !important;
        }}

        hr {{
            border-color: var(--app-border);
        }}

        .small-muted {{
            color: var(--app-muted);
            font-size: 13px;
        }}
    </style>
    """


def get_header_style(title, subtitle, mode="Light", label="Decision Support System"):
    return f"""
    <div class="app-hero">
        <div class="eyebrow">{label}</div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """
