def get_custom_css():
    return """
    <style>
        /* Dasar Tema */
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
        
        /* Kartu Utama (Peringkat 1) */
        .glow-card {
            background: linear-gradient(145deg, #1c2128, #161b22);
            border: 2px solid #58a6ff;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.15);
            margin-bottom: 20px;
        }
        .glow-label { color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold; }
        .glow-name { color: #ffffff; font-size: 28px; font-weight: 800; margin: 10px 0; }
        .glow-score { color: #39d353; font-size: 18px; font-weight: 600; }

        /* Kartu Cadangan (Peringkat 2 & 3) */
        .backup-card {
            background: #161b22;
            border-left: 4px solid #444c56;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 12px;
            transition: 0.3s;
        }
        .backup-card:hover {
            border-left: 4px solid #58a6ff;
            background: #1c2128;
        }
        .rank-label { color: #8b949e; font-size: 10px; font-weight: bold; }
        .vendor-name { color: #adbac7; font-size: 16px; font-weight: 600; margin: 2px 0; }
        .score-badge { 
            background: #21262d; color: #58a6ff; padding: 2px 8px; 
            border-radius: 4px; font-size: 11px; font-weight: bold; 
        }

        /* Tipografi & Metrik */
        .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; }
        h2, h3 { color: #adbac7 !important; }
    </style>
    """

def get_header_style(title, subtitle):
    return f"""
    <div style="background: #161b22; padding: 20px 25px; border-radius: 12px; border: 1px solid #30363d; border-left: 6px solid #58a6ff; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 700;">{title}</h1>
        <p style="color: #8b949e; margin-top: 4px; font-size: 13px;">{subtitle}</p>
    </div>
    """