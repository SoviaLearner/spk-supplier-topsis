import json

def render_dashboard_js(json_records, risk_counts, avg_market):
    risk_json = json.dumps(risk_counts)
    avg_json = json.dumps(avg_market)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #0d1117; margin: 0; padding: 0; overflow: hidden; }}
            .chart-box {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; height: 380px; }}
            .chart-title {{ color: #58a6ff; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 12px; }}
        </style>
    </head>
    <body>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 p-2">
            <div class="chart-box">
                <div class="chart-title">Pemetaan Kedekatan Solusi (SAW & TOPSIS)</div>
                <div id="scat" style="height:330px;"></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">Analisis Komparasi Kinerja Utama</div>
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

                // Scatter Chart
                const scat = echarts.init(document.getElementById('scat'), 'dark');
                scat.setOption({{
                    backgroundColor: 'transparent',
                    tooltip: {{ trigger: 'item', formatter: p => p.data[2] }},
                    xAxis: {{ name: 'SAW', splitLine: {{show: false}} }},
                    yAxis: {{ name: 'TOPSIS', splitLine: {{lineStyle:{{color:'#333'}}}} }},
                    series: [{{ type: 'scatter', symbolSize: 15, data: data.map(d => [d.Skor_SAW, d.Skor_TOPSIS, d.Supplier_Name]), itemStyle: {{color: '#58a6ff'}} }}]
                }});

                // Radar Chart
                const radar = echarts.init(document.getElementById('radar'), 'dark');
                radar.setOption({{
                    backgroundColor: 'transparent',
                    legend: {{ data: [topV.Supplier_Name, 'Rata-rata'], bottom: 0, textStyle: {{fontSize: 10}} }},
                    radar: {{ 
                        indicator: [
                            {{name:'Harga', max:Math.max(...data.map(d=>d.Unit_Price || 0))}},
                            {{name:'Stok', max:Math.max(...data.map(d=>d.Stock_Quantity || 0))}},
                            {{name:'Turnover', max:Math.max(...data.map(d=>d.Inventory_Turnover_Rate || 0))}}
                        ],
                        splitArea:{{show:false}}, splitLine:{{lineStyle:{{color:'#333'}}}}
                    }},
                    series: [{{ type: 'radar', data: [
                        {{value:[topV.Unit_Price, topV.Stock_Quantity, topV.Inventory_Turnover_Rate], name:topV.Supplier_Name, areaStyle:{{color:'rgba(88,166,255,0.1)'}} }},
                        {{value:avgData, name:'Rata-rata', lineStyle:{{type:'dashed', color:'#f0883e'}}}} 
                    ] }}]
                }});

                // Pie Chart
                const pie = echarts.init(document.getElementById('pie'), 'dark');
                pie.setOption({{
                    backgroundColor: 'transparent',
                    series: [{{ type: 'pie', radius: ['40%','70%'], label:{{show:true, fontSize:10}}, data: [
                        {{value:riskData.Aman, name:'Aman', itemStyle:{{color:'#238636'}} }},
                        {{value:riskData.Waspada, name:'Waspada', itemStyle:{{color:'#f0883e'}} }},
                        {{value:riskData.Bahaya, name:'Bahaya', itemStyle:{{color:'#da3633'}} }}
                    ] }}]
                }});
                window.addEventListener('resize', () => {{ [scat, radar, pie].forEach(c => c.resize()); }});
            }} catch(e) {{ console.error(e); }}
        </script>
    </body>
    </html>
    """