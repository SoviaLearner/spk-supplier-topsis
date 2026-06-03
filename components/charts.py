import json

from components.styles import get_theme


def render_dashboard_js(json_records, risk_counts, avg_market, mode="Light"):
    theme = get_theme(mode)
    risk_json = json.dumps(risk_counts)
    avg_json = json.dumps(avg_market)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{
                background-color: {theme['bg']};
                margin: 0;
                padding: 0;
                overflow: hidden;
                font-family: Inter, Segoe UI, Arial, sans-serif;
            }}
            .chart-box {{
                background: {theme['surface']};
                border: 1px solid {theme['border']};
                border-radius: 8px;
                padding: 15px;
                height: 380px;
            }}
            .chart-title {{
                color: {theme['muted']};
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
                margin-bottom: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 p-2">
            <div class="chart-box">
                <div class="chart-title">Pemetaan Kedekatan Solusi</div>
                <div id="scat" style="height:330px;"></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">Komparasi Kinerja Utama</div>
                <div id="radar" style="height:330px;"></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">Distribusi Kualifikasi Supplier</div>
                <div id="pie" style="height:330px;"></div>
            </div>
        </div>
        <script>
            try {{
                const data = {json_records};
                const riskData = {risk_json};
                const avgData = {avg_json};
                const topV = data[0] || {{}};
                const chartTheme = "{theme['chart_theme']}";
                const axisColor = "{theme['muted']}";
                const gridColor = "{theme['border']}";
                const primary = "{theme['primary']}";
                const accent = "{theme['accent']}";
                const success = "{theme['success']}";
                const warning = "{theme['warning']}";
                const danger = "{theme['danger']}";

                const textStyle = {{ color: axisColor, fontFamily: 'Inter, Segoe UI, Arial' }};

                const scat = echarts.init(document.getElementById('scat'), chartTheme);
                scat.setOption({{
                    backgroundColor: 'transparent',
                    tooltip: {{ trigger: 'item', formatter: p => p.data[2] }},
                    grid: {{ left: 46, right: 16, top: 28, bottom: 42 }},
                    xAxis: {{
                        name: 'SAW',
                        nameTextStyle: textStyle,
                        axisLabel: textStyle,
                        axisLine: {{ lineStyle: {{ color: gridColor }} }},
                        splitLine: {{ show: false }}
                    }},
                    yAxis: {{
                        name: 'TOPSIS',
                        nameTextStyle: textStyle,
                        axisLabel: textStyle,
                        axisLine: {{ lineStyle: {{ color: gridColor }} }},
                        splitLine: {{ lineStyle: {{ color: gridColor }} }}
                    }},
                    series: [{{
                        type: 'scatter',
                        symbolSize: 16,
                        data: data.map(d => [d.Skor_SAW, d.Skor_TOPSIS, d.Supplier_Name]),
                        itemStyle: {{ color: primary }}
                    }}]
                }});

                const radarMax = (key) => Math.max(...data.map(d => Number(d[key] || 0)), 1);
                const radar = echarts.init(document.getElementById('radar'), chartTheme);
                radar.setOption({{
                    backgroundColor: 'transparent',
                    legend: {{
                        data: [topV.Supplier_Name, 'Rata-rata'],
                        bottom: 0,
                        textStyle: {{ color: axisColor, fontSize: 10 }}
                    }},
                    radar: {{
                        indicator: [
                            {{ name: 'Harga', max: radarMax('Unit_Price') }},
                            {{ name: 'Stok', max: radarMax('Stock_Quantity') }},
                            {{ name: 'Turnover', max: radarMax('Inventory_Turnover_Rate') }}
                        ],
                        axisName: {{ color: axisColor }},
                        splitArea: {{ show: false }},
                        splitLine: {{ lineStyle: {{ color: gridColor }} }},
                        axisLine: {{ lineStyle: {{ color: gridColor }} }}
                    }},
                    series: [{{
                        type: 'radar',
                        data: [
                            {{
                                value: [topV.Unit_Price, topV.Stock_Quantity, topV.Inventory_Turnover_Rate],
                                name: topV.Supplier_Name,
                                lineStyle: {{ color: primary }},
                                areaStyle: {{ color: 'rgba(45, 212, 191, 0.14)' }}
                            }},
                            {{
                                value: avgData,
                                name: 'Rata-rata',
                                lineStyle: {{ type: 'dashed', color: accent }}
                            }}
                        ]
                    }}]
                }});

                const pie = echarts.init(document.getElementById('pie'), chartTheme);
                pie.setOption({{
                    backgroundColor: 'transparent',
                    tooltip: {{ trigger: 'item' }},
                    series: [{{
                        type: 'pie',
                        radius: ['42%', '70%'],
                        label: {{ show: true, fontSize: 10, color: axisColor }},
                        data: [
                            {{ value: riskData.Aman, name: 'Aman', itemStyle: {{ color: success }} }},
                            {{ value: riskData.Waspada, name: 'Waspada', itemStyle: {{ color: warning }} }},
                            {{ value: riskData.Bahaya, name: 'Bahaya', itemStyle: {{ color: danger }} }}
                        ]
                    }}]
                }});

                window.addEventListener('resize', () => {{ [scat, radar, pie].forEach(c => c.resize()); }});
            }} catch(e) {{ console.error(e); }}
        </script>
    </body>
    </html>
    """
