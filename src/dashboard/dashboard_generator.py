"""
DIBIE - Dashboard Generator
Generate interactive dashboards for data analysis results
"""
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging


class DashboardGenerator:
    """Generate dashboards for visualizing analysis results"""
    
    def __init__(self, config_path: str = "config/dashboard.json", output_dir: str = "dashboard/output"):
        """Initialize dashboard generator
        
        Args:
            config_path: Path to dashboard configuration
            output_dir: Directory for dashboard output
        """
        self.config = self._load_config(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the generator"""
        logger = logging.getLogger('DashboardGenerator')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/dashboard_generator.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def create_kpi_card(self, title: str, value: Any, unit: str = "", trend: Optional[str] = None) -> Dict:
        """Create a KPI card component
        
        Args:
            title: KPI title
            value: KPI value
            unit: Unit of measurement
            trend: Trend indicator (up, down, neutral)
            
        Returns:
            KPI card definition
        """
        return {
            "type": "kpi_card",
            "title": title,
            "value": value,
            "unit": unit,
            "trend": trend,
            "timestamp": datetime.now().isoformat()
        }
    
    def create_chart(self, chart_type: str, title: str, data: List[Dict], x_field: str, y_field: str) -> Dict:
        """Create a chart component
        
        Args:
            chart_type: Type of chart (bar, line, pie, scatter)
            title: Chart title
            data: Data for the chart
            x_field: Field for x-axis
            y_field: Field for y-axis
            
        Returns:
            Chart definition
        """
        return {
            "type": chart_type,
            "title": title,
            "data": data,
            "config": {
                "x_field": x_field,
                "y_field": y_field,
                "responsive": True
            }
        }
    
    def create_table(self, title: str, data: List[Dict], columns: List[str]) -> Dict:
        """Create a data table component
        
        Args:
            title: Table title
            data: Table data
            columns: Column names to display
            
        Returns:
            Table definition
        """
        return {
            "type": "table",
            "title": title,
            "data": data,
            "columns": columns,
            "config": {
                "sortable": True,
                "filterable": True,
                "paginated": True,
                "page_size": 20
            }
        }
    
    def create_dashboard(self, title: str, components: List[Dict]) -> Dict:
        """Create a complete dashboard
        
        Args:
            title: Dashboard title
            components: List of dashboard components
            
        Returns:
            Dashboard definition
        """
        dashboard = {
            "title": title,
            "created": datetime.now().isoformat(),
            "config": self.config.get("dashboard", {}),
            "layout": {
                "type": "grid",
                "columns": 12,
                "rows": "auto"
            },
            "components": components,
            "metadata": {
                "framework": "DIBIE",
                "version": "1.0.0"
            }
        }
        
        self.logger.info(f"Created dashboard: {title}")
        return dashboard
    
    def add_quality_metrics(self, dashboard: Dict, quality_report: Dict) -> Dict:
        """Add data quality metrics to dashboard
        
        Args:
            dashboard: Dashboard definition
            quality_report: Data quality report
            
        Returns:
            Updated dashboard
        """
        kpis = [
            self.create_kpi_card(
                "Data Quality Score",
                f"{quality_report.get('quality_score', 0):.1f}",
                "%",
                "up" if quality_report.get('quality_score', 0) > 80 else "down"
            ),
            self.create_kpi_card(
                "Total Records",
                quality_report.get('record_count', 0),
                "records"
            ),
            self.create_kpi_card(
                "Completeness",
                f"{quality_report.get('completeness', {}).get('overall_completeness_pct', 0):.1f}",
                "%"
            ),
            self.create_kpi_card(
                "Duplicates",
                f"{quality_report.get('duplicates', {}).get('duplicate_pct', 0):.1f}",
                "%",
                "down" if quality_report.get('duplicates', {}).get('duplicate_pct', 0) < 5 else "up"
            )
        ]
        
        dashboard["components"].extend(kpis)
        return dashboard
    
    def generate_html(self, dashboard: Dict) -> str:
        """Generate HTML for dashboard
        
        Args:
            dashboard: Dashboard definition
            
        Returns:
            HTML string
        """
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{dashboard['title']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }}
        .dashboard {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header .timestamp {{ opacity: 0.9; font-size: 0.9em; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .kpi-card {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .kpi-card h3 {{ color: #666; font-size: 0.9em; margin-bottom: 10px; text-transform: uppercase; }}
        .kpi-card .value {{ font-size: 2.5em; font-weight: bold; color: #333; }}
        .kpi-card .unit {{ color: #999; font-size: 0.8em; margin-left: 5px; }}
        .trend-up {{ color: #4caf50; }}
        .trend-down {{ color: #f44336; }}
        .chart {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .chart h2 {{ color: #333; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; background: white; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #667eea; color: white; font-weight: 600; }}
        tr:hover {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>{dashboard['title']}</h1>
            <div class="timestamp">Generado: {dashboard['created']}</div>
        </div>
        
        <div class="grid">
"""
        
        # Add KPI cards
        for component in dashboard['components']:
            if component['type'] == 'kpi_card':
                trend_class = f"trend-{component.get('trend', 'neutral')}" if component.get('trend') else ""
                html += f"""
            <div class="kpi-card">
                <h3>{component['title']}</h3>
                <div class="value {trend_class}">{component['value']}<span class="unit">{component.get('unit', '')}</span></div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="charts">
"""
        
        # Add charts and tables
        for component in dashboard['components']:
            if component['type'] in ['bar_chart', 'line_chart', 'pie_chart']:
                html += f"""
            <div class="chart">
                <h2>{component['title']}</h2>
                <p>Visualización de datos (requiere biblioteca de gráficos)</p>
            </div>
"""
            elif component['type'] == 'table':
                html += f"""
            <div class="chart">
                <h2>{component['title']}</h2>
                <table>
                    <thead><tr>{''.join([f'<th>{col}</th>' for col in component['columns']])}</tr></thead>
                    <tbody>
"""
                for row in component['data'][:10]:  # Limit to 10 rows
                    html += f"<tr>{''.join([f'<td>{row.get(col, '')}</td>' for col in component['columns']])}</tr>"
                
                html += """
                    </tbody>
                </table>
            </div>
"""
        
        html += """
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def save_dashboard(self, dashboard: Dict, filename: str, format: str = 'json') -> str:
        """Save dashboard to file
        
        Args:
            dashboard: Dashboard definition
            filename: Output filename
            format: Output format (json, html)
            
        Returns:
            Path to saved file
        """
        output_path = self.output_dir / f"{filename}.{format}"
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(dashboard, f, indent=2, ensure_ascii=False)
        elif format == 'html':
            html = self.generate_html(dashboard)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
        
        self.logger.info(f"Saved dashboard: {output_path}")
        return str(output_path)


if __name__ == "__main__":
    # Example usage
    generator = DashboardGenerator()
    dashboard = generator.create_dashboard("Test Dashboard", [])
    print(json.dumps(dashboard, indent=2))
