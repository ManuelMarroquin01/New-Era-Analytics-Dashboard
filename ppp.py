import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import time
import warnings
import logging
from typing import Dict, Optional, List, Tuple, Any
from dataclasses import dataclass
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
import openpyxl
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class StockAnalysisConfig:
    """Configuración para el análisis de stock"""
    fecha_reporte: str
    colores_semaforo: Dict[str, str]
    umbrales: Dict[str, Tuple[float, float]]
    
    def __post_init__(self):
        self.fecha_reporte = datetime.now().strftime('%Y%m%d_%H%M')
        self.colores_semaforo = {
            "verde": "#28a745",
            "amarillo": "#ffc107",
            "rojo": "#dc3545",
            "gris": "#6c757d"
        }
        self.umbrales = {
            "verde": (1.0, 1.15),
            "amarillo": (1.15, float('inf')),
            "rojo": (0.0, 1.0)
        }

# Configuración inicial
warnings.filterwarnings("ignore", message="missing ScriptRunContext")
st.set_page_config(
    page_title="New Era Analytics Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.newera.com/support',
        'Report a bug': "https://www.newera.com/support",
        'About': "# New Era Stock Analytics Dashboard\nSistema profesional de análisis de inventario"
    }
)

# Instancia de configuración
config = StockAnalysisConfig(fecha_reporte="", colores_semaforo={}, umbrales={})

class ProfessionalDesign:
    """Gestor de diseño profesional para la aplicación"""
    
    def __init__(self):
        self.primary_color = "#6b7280"  # Gris medio
        self.secondary_color = "#9ca3af"  # Gris claro
        self.accent_color = "#374151"  # Gris oscuro
        self.success_color = "#10b981"  # Verde
        self.warning_color = "#f59e0b"  # Amarillo
        self.danger_color = "#ef4444"  # Rojo
        self.neutral_color = "#e5e7eb"  # Gris muy claro
        self.background_color = "#f9fafb"  # Gris de fondo
        
    def inject_custom_css(self):
        """Inyecta CSS personalizado para el diseño profesional"""
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            font-family: 'Inter', sans-serif;
            animation: fadeIn 0.8s ease-in-out;
        }
        
        /* Animaciones globales */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInFromLeft {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideInFromRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes scaleIn {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Header ultra moderno y cool */
        .main-header {
            background: linear-gradient(to right, #000000 0%, #1a1a1a 50%, #0a0a0a 100%);
            padding: 5rem 0;
            border-radius: 0;
            margin: 0 -5rem 3rem -5rem;
            box-shadow: 
                0 25px 60px rgba(0, 0, 0, 0.3),
                0 10px 30px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            animation: headerSlideIn 1s ease-out;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            border: none;
            backdrop-filter: blur(10px);
            min-height: 260px;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.08) 25%, 
                rgba(255, 255, 255, 0.15) 50%, 
                rgba(255, 255, 255, 0.08) 75%, 
                transparent 100%
            );
            animation: headerShine 8s ease-in-out infinite;
            z-index: 1;
        }
        
        @keyframes headerShine {
            0% { left: -100%; }
            15% { left: -100%; }
            50% { left: 100%; }
            85% { left: 100%; }
            100% { left: 100%; }
        }
        
        .main-header::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 80%, rgba(156, 163, 175, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(209, 213, 219, 0.1) 0%, transparent 50%);
            opacity: 0.6;
            animation: floatingParticles 8s ease-in-out infinite;
        }
        
        @keyframes headerSlideIn {
            from { 
                opacity: 0; 
                transform: translateY(-30px) scale(0.95); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
        }
        
        @keyframes floatingParticles {
            0%, 100% { 
                background: radial-gradient(circle at 20% 80%, rgba(156, 163, 175, 0.1) 0%, transparent 50%),
                            radial-gradient(circle at 80% 20%, rgba(209, 213, 219, 0.1) 0%, transparent 50%);
            }
            50% { 
                background: radial-gradient(circle at 30% 70%, rgba(156, 163, 175, 0.15) 0%, transparent 50%),
                            radial-gradient(circle at 70% 30%, rgba(209, 213, 219, 0.15) 0%, transparent 50%);
            }
        }
        
        /* Efecto hover removido para mantener encabezado fijo */
        
        /* Efecto de luz continuo - removido hover para que sea automático */
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            z-index: 2;
            padding: 0 4rem;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 3rem;
            position: relative;
            flex: 1;
        }
        
        .logo-section::before {
            content: '';
            position: absolute;
            left: -1rem;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 60px;
            background: linear-gradient(to bottom, transparent, #9ca3af, transparent);
            border-radius: 2px;
        }
        
        .logo-icon {
            font-size: 4rem;
            filter: drop-shadow(0 8px 16px rgba(0,0,0,0.3));
            position: relative;
            min-width: 140px;
        }
        
        .logo-section > div {
            margin-left: 1.5rem;
            flex: 1;
        }
        
        .header-title {
            color: #ffffff !important;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 4px 8px rgba(0,0,0,0.5);
        }
        
        
        /* Ocultar cualquier icono o flecha que pueda aparecer */
        .main-header .header-title + *:not(.header-subtitle) {
            display: none !important;
        }
        
        /* Ocultar elementos de navegación automáticos */
        .main-header [data-testid="stElementToolbar"] {
            display: none !important;
        }
        
        .header-subtitle {
            color: #ffffff !important;
            font-size: 1.2rem;
            font-weight: 500;
            margin: 0.5rem 0 0 0;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
            letter-spacing: 0.5px;
        }
        
        .header-stats {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .stat-item {
            text-align: center;
            color: #ffffff !important;
        }
        
        .stat-number {
            font-size: 1.8rem;
            font-weight: 700;
            display: block;
            color: #ffffff !important;
        }
        
        .stat-label {
            font-size: 0.9rem;
            font-weight: 300;
            color: #ffffff !important;
        }
        
        /* Pestañas profesionales */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: white;
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            padding: 0 2rem;
            background: transparent;
            border-radius: 8px;
            color: #6b7280;
            font-weight: 500;
            border: none;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6b7280, #9ca3af) !important;
            color: white !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(107, 114, 128, 0.3) !important;
        }
        
        /* Cards de bienvenida personalizadas por país con animaciones */
        .country-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 24px;
            padding: 3rem 2rem;
            text-align: center;
            margin: 1.5rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08), 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }
        
        .country-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.6s ease;
        }
        
        .country-card:hover::before {
            left: 100%;
        }
        
        /* Guatemala - Celeste */
        .country-card-gt {
            border-top: 4px solid #0ea5e9;
        }
        
        .country-card-gt:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(14, 165, 233, 0.3), 0 8px 20px rgba(0, 0, 0, 0.08);
            border-color: rgba(14, 165, 233, 0.3);
            background: linear-gradient(135deg, #ffffff 0%, rgba(186, 230, 253, 0.15) 100%);
        }
        
        /* Panamá - Rojo */
        .country-card-pa {
            border-top: 4px solid #dc2626;
        }
        
        .country-card-pa:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(220, 38, 38, 0.3), 0 8px 20px rgba(0, 0, 0, 0.08);
            border-color: rgba(220, 38, 38, 0.3);
            background: linear-gradient(135deg, #ffffff 0%, rgba(254, 202, 202, 0.15) 100%);
        }
        
        /* Honduras - Azul */
        .country-card-hn {
            border-top: 4px solid #1e40af;
        }
        
        .country-card-hn:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(30, 64, 175, 0.3), 0 8px 20px rgba(0, 0, 0, 0.08);
            border-color: rgba(30, 64, 175, 0.3);
            background: linear-gradient(135deg, #ffffff 0%, rgba(191, 219, 254, 0.15) 100%);
        }
        
        /* El Salvador - Azul oscuro */
        .country-card-sv {
            border-top: 4px solid #1e3a8a;
        }
        
        .country-card-sv:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(30, 58, 138, 0.3), 0 8px 20px rgba(0, 0, 0, 0.08);
            border-color: rgba(30, 58, 138, 0.3);
            background: linear-gradient(135deg, #ffffff 0%, rgba(191, 219, 254, 0.15) 100%);
        }
        
        /* Costa Rica - Verde */
        .country-card-cr {
            border-top: 4px solid #16a34a;
        }
        
        .country-card-cr:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(22, 163, 74, 0.3), 0 8px 20px rgba(0, 0, 0, 0.08);
            border-color: rgba(22, 163, 74, 0.3);
            background: linear-gradient(135deg, #ffffff 0%, rgba(187, 247, 208, 0.15) 100%);
        }
        
        /* Efectos de hover para banderas */
        .country-flag {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            display: block;
            transition: all 0.4s ease;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        }
        
        .country-card:hover .country-flag {
            transform: scale(1.15) rotate(5deg);
            filter: drop-shadow(0 8px 16px rgba(0,0,0,0.15));
        }
        
        /* Efectos de hover para títulos */
        .country-title {
            transition: all 0.3s ease;
        }
        
        .country-card:hover .country-title {
            transform: translateY(-2px);
        }
        
        /* Efectos de hover para descripciones */
        .country-description {
            transition: all 0.3s ease;
        }
        
        .country-card:hover .country-description {
            transform: translateY(-1px);
        }
        
        /* Pestañas minimalistas y elegantes */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 6px;
            margin: 2rem 0;
            box-shadow: 
                0 1px 3px rgba(0, 0, 0, 0.05),
                0 1px 2px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.08);
            position: relative;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            gap: 4px;
            backdrop-filter: blur(8px);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            margin: 0;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            z-index: 1;
            color: #64748b;
            letter-spacing: 0.25px;
            flex: 1;
            text-align: center;
            white-space: nowrap;
            min-width: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(248, 250, 252, 0.8) !important;
            color: #334155 !important;
            transform: translateY(-12px) scale(1.05) !important;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.15),
                0 12px 24px rgba(0, 0, 0, 0.12),
                0 4px 8px rgba(0, 0, 0, 0.08) !important;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: rgba(248, 250, 252, 0.2) !important;
            color: #6b7280 !important;
            font-weight: 520;
            position: relative;
        }
        
        .stTabs [data-baseweb="tab"][data-teststate="active"] {
            background: rgba(248, 250, 252, 0.2) !important;
            color: #6b7280 !important;
        }
        
        .stTabs [data-baseweb="tab"]:focus {
            background: rgba(248, 250, 252, 0.2) !important;
            color: #6b7280 !important;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"]:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 12px;
            height: 1px;
            background: rgba(156, 163, 175, 0.25);
            border-radius: 0.5px;
            opacity: 1;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"]:hover {
            background: rgba(249, 250, 251, 0.4) !important;
            transform: translateY(-8px) scale(1.04) !important;
            color: #52525b !important;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.12),
                0 8px 16px rgba(0, 0, 0, 0.08),
                0 2px 4px rgba(0, 0, 0, 0.04) !important;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"]:hover:after {
            width: 16px;
            background: rgba(156, 163, 175, 0.3);
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            display: none;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            padding: 2.5rem 0;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Métricas KPI mejoradas */
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #f1f5f9;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: scaleIn 0.6s ease-out;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.6s ease;
        }
        
        .metric-card:hover::before {
            left: 100%;
        }
        
        .metric-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }
        
        /* Botones mejorados */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #f59e0b, #d97706) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.75rem 2rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3) !important;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.5) !important;
        }
        
        /* Animaciones para pestañas */
        .stTabs [data-baseweb="tab-list"] {
            animation: slideInFromRight 0.6s ease-out;
        }
        
        .stTabs [data-baseweb="tab"] {
            transition: all 0.3s ease !important;
            border-radius: 10px !important;
            margin: 0 5px !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        }
        
        /* Animaciones para contenido de pestañas */
        .stTabs [data-baseweb="tab-panel"] {
            animation: fadeIn 0.8s ease-out;
        }
        
        /* Alertas mejoradas */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            animation: scaleIn 0.5s ease-out;
            transition: all 0.3s ease !important;
        }
        
        .stAlert:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        }
        
        /* Animaciones para tablas */
        .stDataFrame {
            animation: slideInFromLeft 0.8s ease-out;
            transition: all 0.3s ease !important;
        }
        
        .stDataFrame:hover {
            box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
        }
        
        /* Animaciones para gráficos */
        .js-plotly-plot {
            animation: fadeIn 1s ease-out;
            transition: all 0.3s ease !important;
        }
        
        .js-plotly-plot:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
        }
        
        /* Animaciones para elementos de carga */
        .stSpinner {
            animation: pulse 2s infinite;
        }
        
        /* Animaciones para elementos de entrada */
        .stFileUploader {
            animation: slideInFromRight 0.6s ease-out;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1) !important;
        }
        
        /* Tablas mejoradas */
        .stDataFrame {
            border-radius: 16px !important;
            overflow: hidden !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1) !important;
        }
        
        /* Sidebar mejorado */
        .stSidebar {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        /* File uploader mejorado */
        .stFileUploader {
            border: 2px dashed #d1d5db;
            border-radius: 16px;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: #6b7280;
            background: #f9fafb;
        }
        
        /* Spinner personalizado */
        .stSpinner {
            color: #6b7280 !important;
        }
        
        /* Ocultar elementos de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        
        </style>
        """, unsafe_allow_html=True)
    
    def create_main_header(self):
        """Crea el header principal profesional con hora en tiempo real y última actividad"""
        # Obtener conteos dinámicos
        total_countries = self._get_total_countries()
        total_stores = self._get_total_stores()
        
        # Obtener fecha de último trabajo con stock
        last_work_date = self._get_last_stock_work_date()
        
        # Crear contenedor para la hora que se puede actualizar
        header_container = st.container()
        
        with header_container:
            # Cargar logo de New Era
            try:
                logo_path = "LOGO NE NUEVO.png"
                with open(logo_path, "rb") as logo_file:
                    logo_data = logo_file.read()
                import base64
                logo_base64 = base64.b64encode(logo_data).decode()
                logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-icon" style="height: 100px; width: auto; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));">'
            except FileNotFoundError:
                # Fallback a corona si no encuentra la imagen
                logo_html = '<span class="logo-icon" style="font-size: 5rem; display: inline-block;">👑</span>'
            
            st.markdown(f"""
            <div class="main-header">
                <div class="header-content">
                    <div class="logo-section">
                        {logo_html}
                        <div>
                            <h1 class="header-title">New Era Analytics</h1>
                            <p class="header-subtitle">Dashboard de Análisis de Inventario</p>
                        </div>
                    </div>
                    <div class="header-stats">
                        <div class="stat-item">
                            <span class="stat-number">{total_countries}</span>
                            <span class="stat-label">Países</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">{total_stores}</span>
                            <span class="stat-label">Tiendas</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number" id="current-time">{datetime.now().strftime('%H:%M')}</span>
                            <span class="stat-label">Hora actual</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">{last_work_date}</span>
                            <span class="stat-label">Último trabajo</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
            function updateTime() {{
                const now = new Date();
                const timeString = now.toLocaleTimeString('es-ES', {{
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false
                }});
                const timeElement = document.getElementById('current-time');
                if (timeElement) {{
                    timeElement.textContent = timeString;
                }}
            }}
            
            // Actualizar cada segundo
            setInterval(updateTime, 1000);
            
            // Actualizar inmediatamente
            updateTime();
            </script>
            """, unsafe_allow_html=True)
    
    def _get_last_stock_work_date(self):
        """Obtiene la fecha del último trabajo con stock"""
        # Verificar si hay registro de última actividad en session_state
        if 'last_stock_work_date' in st.session_state:
            return st.session_state.last_stock_work_date
        else:
            # Si no hay actividad previa, mostrar "Sin actividad"
            return "Sin actividad"
    
    def _update_last_stock_work_date(self):
        """Actualiza la fecha del último trabajo con stock"""
        current_date = datetime.now().strftime('%d/%m/%Y')
        st.session_state.last_stock_work_date = current_date
        return current_date
    
    def _get_league_logo(self, logo_filename: str, league_name: str, fallback: str) -> str:
        """Carga el logo de la liga o usa fallback si no encuentra la imagen"""
        try:
            with open(logo_filename, "rb") as logo_file:
                logo_data = logo_file.read()
            import base64
            logo_base64 = base64.b64encode(logo_data).decode()
            return f'<img src="data:image/png;base64,{logo_base64}" alt="{league_name}" style="height: 75px; width: auto; margin-bottom: 0.5rem;">'
        except FileNotFoundError:
            # Fallback al emoji si no encuentra la imagen
            return f'<span style="font-size: 1.5rem;">{fallback}</span>'
    
    def _get_total_countries(self) -> int:
        """Obtiene el número total de países dinámicamente desde CountryManager"""
        global country_manager
        if country_manager is None:
            country_manager = CountryManager()
        return len(country_manager.countries)
    
    def _get_total_stores(self) -> int:
        """Obtiene el número total de tiendas excluyendo bodegas centrales"""
        global country_manager
        if country_manager is None:
            country_manager = CountryManager()
        
        # Bodegas centrales a excluir
        central_warehouses = {
            "CENTRAL NEW ERA",  # Guatemala
            "New Era Central",  # El Salvador  
            "Bodega Central NEW ERA",  # Costa Rica
            "Bodega Central Albrook",  # Panama
            "Almacén general"  # Panama
        }
        
        total_stores = 0
        for country_name, country_data in country_manager.countries.items():
            # Contar todas las bodegas menos las centrales
            for bodega in country_data.bodegas:
                if bodega not in central_warehouses:
                    total_stores += 1
        
        return total_stores
    
    def create_leagues_section(self):
        """Crea la sección de ligas deportivas con logos y estilo de pestañas de países"""
        # Cargar todos los logos
        mlb_logo = self._get_league_logo("LOGO_MLB.png", "MLB", "⚾")
        nba_logo = self._get_league_logo("LOGO_NBA.png", "NBA", "🏀")
        nfl_logo = self._get_league_logo("LOGO_NFL.png", "NFL", "🏈")
        f1_logo = self._get_league_logo("LOGO_F1.png", "MOTORSPORT", "🏎️")
        ne_logo = self._get_league_logo("LOGO_NE 2.png", "NEW ERA", "👑")
        
        # Estilos flotantes sin bordes para las tarjetas de ligas
        st.markdown("""
        <style>
        .league-card {
            background: transparent;
            border-radius: 12px;
            padding: 1.5rem 1rem 1rem 1rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            margin-bottom: 0.5rem;
            position: relative;
            overflow: visible;
        }
        
        .league-card::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, currentColor, transparent, currentColor);
            border-radius: 14px;
            opacity: 0;
            transition: opacity 0.4s ease;
            z-index: -1;
        }
        
        .league-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            opacity: 0;
            transition: all 0.4s ease;
            z-index: -1;
            backdrop-filter: blur(10px);
        }
        
        .league-card:hover::before,
        .league-card.selected::before {
            opacity: 0.1;
        }
        
        .league-card:hover::after,
        .league-card.selected::after {
            opacity: 1;
            box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        }
        
        .league-card:hover {
            transform: translateY(-8px) scale(1.02);
        }
        
        .league-card.selected {
            transform: translateY(-4px) scale(1.01);
        }
        
        .league-card img {
            height: 95px;
            width: auto;
            margin-bottom: 0.75rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
            position: relative;
            z-index: 1;
        }
        
        .league-card:hover img {
            transform: scale(1.1);
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.15));
        }
        
        .league-card.selected img {
            transform: scale(1.05);
            filter: drop-shadow(0 4px 8px currentColor);
        }
        
        .league-card p {
            margin: 0.75rem 0 0 0;
            font-weight: 400;
            color: #64748b;
            font-size: 1.1rem;
            transition: all 0.4s ease;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(255,255,255,0.8);
            transform: scaleY(0.9);
        }
        
        .league-card:hover p,
        .league-card.selected p {
            color: currentColor;
            font-weight: 400;
            text-shadow: 0 2px 4px rgba(255,255,255,0.9);
        }
        
        /* Colores específicos para cada liga */
        .mlb-card {
            color: #1e40af;
        }
        
        .mlb-card.selected::after {
            background: linear-gradient(135deg, rgba(191, 219, 254, 0.3), rgba(219, 234, 254, 0.3));
        }
        
        .nba-card {
            color: #ea580c;
        }
        
        .nba-card.selected::after {
            background: linear-gradient(135deg, rgba(254, 215, 170, 0.3), rgba(254, 243, 199, 0.3));
        }
        
        .nfl-card {
            color: #16a34a;
        }
        
        .nfl-card.selected::after {
            background: linear-gradient(135deg, rgba(187, 247, 208, 0.3), rgba(220, 252, 231, 0.3));
        }
        
        .f1-card {
            color: #dc2626;
        }
        
        .f1-card.selected::after {
            background: linear-gradient(135deg, rgba(254, 202, 202, 0.3), rgba(254, 226, 226, 0.3));
        }
        
        .newera-card {
            color: #7c3aed;
        }
        
        .newera-card.selected::after {
            background: linear-gradient(135deg, rgba(221, 214, 254, 0.3), rgba(237, 233, 254, 0.3));
        }
        
        /* Estilo minimalista para el selectbox */
        [data-testid="league_selector"] {
            margin: 0.25rem 0 !important;
        }
        
        [data-testid="league_selector"] select {
            background: #fafafa !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.4rem 0.6rem !important;
            font-size: 0.85rem !important;
            font-weight: 400 !important;
            color: #6b7280 !important;
            box-shadow: none !important;
            transition: all 0.15s ease !important;
        }
        
        [data-testid="league_selector"] label {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Descripción del sistema con imagen de fondo
        # Cargar imagen de fondo IMAGEN_NE
        try:
            with open("IMAGEN_NE.png", "rb") as bg_file:
                bg_data = bg_file.read()
            import base64
            bg_base64 = base64.b64encode(bg_data).decode()
            bg_image = f"data:image/png;base64,{bg_base64}"
        except FileNotFoundError:
            try:
                with open("IMAGEN_NE.jpg", "rb") as bg_file:
                    bg_data = bg_file.read()
                import base64
                bg_base64 = base64.b64encode(bg_data).decode()
                bg_image = f"data:image/jpeg;base64,{bg_base64}"
            except FileNotFoundError:
                # Si no encuentra la imagen, usar fondo blanco
                bg_image = None
        
        if bg_image:
            st.markdown(f"""
            <div style="
                position: relative;
                border-radius: 16px; 
                padding: 2rem; 
                margin-bottom: 2rem; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                background-image: url('{bg_image}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                overflow: hidden;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(255, 255, 255, 0.85);
                    border-radius: 16px;
                    z-index: 1;
                "></div>
                <div style="position: relative; z-index: 2;">
                    <h3 style="color: #374151; font-weight: 600; margin-bottom: 1rem;">Análisis Integral de Inventario</h3>
                    <p style="color: #6b7280; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">
                        Sistema profesional de análisis de stock por bodega, categorizado por ligas deportivas principales:
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback si no encuentra la imagen
            st.markdown("""
            <div style="background: white; border-radius: 16px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <h3 style="color: #374151; font-weight: 600; margin-bottom: 1rem;">Análisis Integral de Inventario</h3>
                <p style="color: #6b7280; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">
                    Sistema profesional de análisis de stock por bodega, categorizado por ligas deportivas principales:
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Inicializar session state para la liga seleccionada
        if 'selected_league' not in st.session_state:
            st.session_state.selected_league = None
        
        # Selectbox con placeholder para manejar la selección
        league_selection = st.selectbox(
            "Liga",
            ["Selecciona la Liga", "Todas", "MLB", "NBA", "NFL", "MOTORSPORT", "ENTERTAINMENT"],
            index=0,
            key="league_selector",
            label_visibility="collapsed"
        )
        
        # Actualizar session state basado en la selección
        if league_selection == "Selecciona la Liga":
            st.session_state.selected_league = None
        elif league_selection == "Todas":
            st.session_state.selected_league = None
        else:
            st.session_state.selected_league = league_selection
        
        # Crear tarjetas clickeables con estilo de pestañas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            selected_class = "selected" if st.session_state.selected_league == "MLB" else ""
            st.markdown(f"""
            <div class="league-card mlb-card {selected_class}" onclick="
                const selectbox = window.parent.document.querySelector('[data-testid=\\"league_selector\\"] select');
                if (selectbox) {{
                    selectbox.value = 'MLB';
                    selectbox.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            ">
                {mlb_logo}
                <p>MLB</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            selected_class = "selected" if st.session_state.selected_league == "NBA" else ""
            st.markdown(f"""
            <div class="league-card nba-card {selected_class}" onclick="
                const selectbox = window.parent.document.querySelector('[data-testid=\\"league_selector\\"] select');
                if (selectbox) {{
                    selectbox.value = 'NBA';
                    selectbox.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            ">
                {nba_logo}
                <p>NBA</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            selected_class = "selected" if st.session_state.selected_league == "NFL" else ""
            st.markdown(f"""
            <div class="league-card nfl-card {selected_class}" onclick="
                const selectbox = window.parent.document.querySelector('[data-testid=\\"league_selector\\"] select');
                if (selectbox) {{
                    selectbox.value = 'NFL';
                    selectbox.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            ">
                {nfl_logo}
                <p>NFL</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            selected_class = "selected" if st.session_state.selected_league == "MOTORSPORT" else ""
            st.markdown(f"""
            <div class="league-card f1-card {selected_class}" onclick="
                const selectbox = window.parent.document.querySelector('[data-testid=\\"league_selector\\"] select');
                if (selectbox) {{
                    selectbox.value = 'MOTORSPORT';
                    selectbox.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            ">
                {f1_logo}
                <p>MOTORSPORT</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            selected_class = "selected" if st.session_state.selected_league == "ENTERTAINMENT" else ""
            st.markdown(f"""
            <div class="league-card newera-card {selected_class}" onclick="
                const selectbox = window.parent.document.querySelector('[data-testid=\\"league_selector\\"] select');
                if (selectbox) {{
                    selectbox.value = 'ENTERTAINMENT';
                    selectbox.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            ">
                {ne_logo}
                <p>ENTERTAINMENT</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Agregar espacio entre las tarjetas de ligas y las pestañas de países
        st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
        
    
    def create_welcome_card(self, country_flag: str, country_name: str, description: str, stores_count: int, country_code: str = ""):
        """Crea una card de bienvenida profesional con colores personalizados por país"""
        
        # Determinar colores según el país
        if "Panamá" in country_name or "PANAMA" in country_name:
            # Rojo de la bandera de Panamá
            primary_color = "#dc2626"
            secondary_color = "#ef4444"
            accent_color = "#fecaca"
        elif "Honduras" in country_name or "HONDURAS" in country_name:
            # Azul 
            primary_color = "#1e40af"
            secondary_color = "#3b82f6"
            accent_color = "#bfdbfe"
        elif "El Salvador" in country_name or "EL SALVADOR" in country_name:
            # Azul oscuro de la bandera de El Salvador
            primary_color = "#1e3a8a"
            secondary_color = "#1d4ed8"
            accent_color = "#bfdbfe"
        elif "Costa Rica" in country_name or "COSTA RICA" in country_name:
            # Verde reciclaje de Costa Rica
            primary_color = "#16a34a"
            secondary_color = "#22c55e"
            accent_color = "#bbf7d0"
        elif "Guatemala" in country_name or "GUATEMALA" in country_name:
            # Celeste 
            primary_color = "#0ea5e9"
            secondary_color = "#38bdf8"
            accent_color = "#bae6fd"
        else:
            # Azul medio por defecto
            primary_color = "#1e40af"
            secondary_color = "#3b82f6"
            accent_color = "#bfdbfe"
        
        return f"""
<div class="welcome-card-{country_code.lower()}">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, {primary_color}, {secondary_color}); border-radius: 24px 24px 0 0; opacity: 0.8;"></div>
    
    <span class="country-flag">{country_flag}</span>
    
    <h3 style="color: {primary_color}; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem; transition: all 0.3s ease; text-shadow: 0 2px 4px rgba(0,0,0,0.02);">{country_name}</h3>
    
    <p style="color: #64748b; font-size: 1rem; font-weight: 500; line-height: 1.6; margin-bottom: 0; transition: all 0.3s ease; background: linear-gradient(135deg, rgba(255,255,255,0.7) 0%, {accent_color}20 100%); padding: 1rem; border-radius: 12px; border: 1px solid {accent_color}50;">
        {description}<br>
        <strong style="color: {primary_color};">{stores_count} tiendas</strong> en operación
    </p>
</div>"""
    
    def create_section_header(self, title: str, subtitle: str = "", icon: str = "📊"):
        """Crea un header de sección profesional con fondo degradado según el país"""
        subtitle_html = f"<p style='color: #d1d5db; margin: 0.5rem 0 0 0; font-size: 1.1rem;'>{subtitle}</p>" if subtitle else ""
        
        # Determinar colores según el país
        if "Panamá" in title or "PANAMA" in title:
            # Rojo de la bandera de Panamá
            background_gradient = "linear-gradient(135deg, #dc2626 0%, #ef4444 100%)"
            box_shadow = "0 10px 30px rgba(220, 38, 38, 0.3)"
        elif "Honduras" in title or "HONDURAS" in title:
            # Azul (anteriormente de Guatemala)
            background_gradient = "linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)"
            box_shadow = "0 10px 30px rgba(30, 64, 175, 0.3)"
        elif "El Salvador" in title or "EL SALVADOR" in title:
            # Azul oscuro de la bandera de El Salvador
            background_gradient = "linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%)"
            box_shadow = "0 10px 30px rgba(30, 58, 138, 0.3)"
        elif "Costa Rica" in title or "COSTA RICA" in title:
            # Verde reciclaje de Costa Rica
            background_gradient = "linear-gradient(135deg, #16a34a 0%, #22c55e 100%)"
            box_shadow = "0 10px 30px rgba(22, 163, 74, 0.3)"
        elif "Guatemala" in title or "GUATEMALA" in title:
            # Celeste (anteriormente de Honduras)
            background_gradient = "linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%)"
            box_shadow = "0 10px 30px rgba(14, 165, 233, 0.3)"
        else:
            # Azul medio por defecto
            background_gradient = "linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)"
            box_shadow = "0 10px 30px rgba(30, 64, 175, 0.3)"
        
        st.markdown(f"""
        <div style="
            background: {background_gradient};
            padding: 2rem 3rem;
            border-radius: 15px;
            margin: 2rem 0;
            box-shadow: {box_shadow};
            animation: slideInFromLeft 0.8s ease-out;
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
            <div style="display: flex; align-items: center;">
                <div>
                    <h2 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 700;">
                        {title}
                    </h2>
                    {subtitle_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Instancia del diseño profesional
professional_design = ProfessionalDesign()

@dataclass
class ProductClassification:
    """Clasificación de productos por silueta"""
    siluetas_planas: List[str]
    siluetas_curvas: List[str]
    
    def __post_init__(self):
        self.siluetas_planas = [
            "950", "5950", "5950 AF", "5950 DOGEAR", "5950 SPLIT PANEL",
            "950 AF", "950 AF TRUCKER", "950 SS", "950 TRUCKER",
            "LP 5950", "LP 950", "RC 5950", "RC 950"
        ]
        self.siluetas_curvas = [
            "920", "940", "970", "1920", "3930",
            "920 TRUCKER", "940 AF", "940 AF TRUCKER",
            "940 EF", "940 SS", "940 TRUCKER", "970 SS"
        ]
    
    def clasificar_silueta(self, silueta) -> Optional[str]:
        """Clasifica una silueta como plana o curva"""
        if pd.isna(silueta) or not isinstance(silueta, str):
            return None
        
        silueta_upper = str(silueta).strip().upper()
        if silueta_upper in self.siluetas_planas:
            return 'Planas'
        elif silueta_upper in self.siluetas_curvas:
            return 'Curvas'
        return None

# Instancia de clasificación
product_classifier = ProductClassification(siluetas_planas=[], siluetas_curvas=[])

@dataclass
class CountryData:
    """Datos específicos de un país"""
    name: str
    bodegas: List[str]
    capacidades: Dict[str, int]
    
    def get_total_capacity(self) -> int:
        """Obtiene la capacidad total del país"""
        return sum(self.capacidades.values())

class CountryManager:
    """Gestor de datos de países"""
    
    def __init__(self):
        self.countries = {
            "Guatemala": CountryData(
                name="Guatemala",
                bodegas=[
                    "NE Cayala", "NE Chimaltenango", "NE Concepcion", "NE Interplaza Escuintla",
                    "NE InterXela", "NE Metrocentro Outlet", "NE Metronorte", "NE Metroplaza Jutiapa",
                    "NE Miraflores", "NE Naranjo", "NE Oakland", "NE Outlet Santa clara",
                    "NE Paseo Antigua", "NE Peri Roosvelt", "NE Plaza Magdalena", "NE Plaza Videre",
                    "NE Portales", "NE Pradera Chiquimula", "NE Pradera Escuintla", "NE Pradera Huehuetenango",
                    "NE Pradera Xela", "NE Puerto Barrios", "NE Vistares", "CENTRAL NEW ERA"
                ],
                capacidades={
                    "NE Miraflores": 6989, "NE Oakland": 5276, "NE Cayala": 5109,
                    "NE Plaza Videre": 2208, "NE Concepcion": 2754, "NE Portales": 6453,
                    "NE Naranjo": 2790, "NE Peri Roosvelt": 2476, "NE Vistares": 4890,
                    "NE Chimaltenango": 2357, "NE Pradera Escuintla": 4619, "NE Interplaza Escuintla": 6769,
                    "NE Pradera Xela": 3827, "NE InterXela": 3907, "NE Pradera Huehuetenango": 4835,
                    "NE Metroplaza Jutiapa": 2766, "NE Pradera Chiquimula": 4837, "NE Plaza Magdalena": 4710,
                    "NE Metronorte": 6735, "NE Metrocentro Outlet": 5184, "NE Outlet Santa clara": 4860,
                    "NE Paseo Antigua": 2952, "NE Puerto Barrios": 3024
                }
            ),
            "El Salvador": CountryData(
                name="El Salvador",
                bodegas=[
                    "NE METROCENTRO LOURDES", "NE METROCENTRO SAN MIGUEL", "NE PLAZA MUNDO SOYAPANGO",
                    "NE USULUTÁN", "New Era Central", "NEW ERA EL PASEO", "NEW ERA METROCENTRO",
                    "NEW ERA METROCENTRO SANTA ANA", "NEW ERA MULTIPLAZA"
                ],
                capacidades={
                    "NEW ERA METROCENTRO": 4355, "NEW ERA MULTIPLAZA": 5443, "NEW ERA EL PASEO": 4436,
                    "NEW ERA METROCENTRO SANTA ANA": 5771, "NE USULUTÁN": 5760, "NE METROCENTRO SAN MIGUEL": 3600,
                    "NE PLAZA MUNDO SOYAPANGO": 3120, "NE METROCENTRO LOURDES": 6912
                }
            ),
            "Honduras": CountryData(
                name="Honduras",
                bodegas=[
                    "NE – Cascadas Mall Tegucigalpa", "NE – City Mall Tegucigalpa", "NE – Mega Mall SPS",
                    "NE – Multiplaza Tegucigalpa", "NE –Multiplaza SPS"
                ],
                capacidades={
                    "NE – Mega Mall SPS": 2730, "NE –Multiplaza SPS": 6540, "NE – City Mall Tegucigalpa": 5190,
                    "NE – Cascadas Mall Tegucigalpa": 3816, "NE – Multiplaza Tegucigalpa": 0
                }
            ),
            "Costa Rica": CountryData(
                name="Costa Rica",
                bodegas=[
                    "Bodega Central NEW ERA", "NE City Mall"
                ],
                capacidades={
                    "NE City Mall": 4260, "Bodega Central NEW ERA": 0
                }
            ),
            "PANAMA": CountryData(
                name="PANAMA",
                bodegas=[
                    "Almacén general", "Bodega Central Albrook", "NE Albrookmall",
                    "NE Metromall", "NE Multiplaza Panamá", "NE Westland"
                ],
                capacidades={
                    "NE Multiplaza Panamá": 6318, "NE Westland": 2972, "NE Metromall": 4422,
                    "NE Albrookmall": 4224, "Almacén general": 0, "Bodega Central Albrook": 0
                }
            )
        }
    
    def get_country_data(self, country: str) -> Optional[CountryData]:
        """Obtiene los datos de un país"""
        return self.countries.get(country)
    
    def get_bodegas(self, country: str) -> List[str]:
        """Obtiene las bodegas de un país"""
        country_data = self.get_country_data(country)
        return country_data.bodegas if country_data else []
    
    def get_capacidades(self, country: str) -> Dict[str, int]:
        """Obtiene las capacidades de un país"""
        country_data = self.get_country_data(country)
        return country_data.capacidades if country_data else {}

# Instancia del gestor de países
country_manager = CountryManager()

@dataclass
class LeagueCategories:
    """Categorías de ligas deportivas"""
    categories: Dict[str, List[str]]
    
    def __post_init__(self):
        self.categories = {
            "MLB": ["MLB", "MLB properties"],
            "NBA": ["NBA", "NBA Properties"],
            "NFL": ["NFL", "NFL Properties"],
            "MOTORSPORT": ["MOTORSPORT"],
            "ENTERTAINMENT": [
                "NEW ERA BRANDED",
                "ENTERTAINMENT",
                "MARCA PAIS",
                "WARNER BROS",
                "NONE LICENSED",
                "MLS",
                "MILB",
                "GUATEMALA SOCCER LEAGUE",
                "WBC",
                "EUROPEAN SOCCER",
                "FEDERACION DE BASEBALL PUERTO RICO",
                "FEDERACION DOMINICANA DE BASEBALL",
                "BASEBALL FEDERATION"
            ]
        }
    
    def get_category_values(self, category: str) -> List[str]:
        """Obtiene los valores de una categoría"""
        return self.categories.get(category, [])
    
    def get_all_categories(self) -> Dict[str, List[str]]:
        """Obtiene todas las categorías"""
        return self.categories

# Instancia de categorías de liga
league_categories = LeagueCategories(categories={})

class StockAnalyzer:
    """Analizador de stock con métricas de cumplimiento"""
    
    def __init__(self, config: StockAnalysisConfig):
        self.config = config
    
    def obtener_color_semaforo(self, total_headwear: int, capacidad: int) -> str:
        """Determina el color del semáforo basado en el porcentaje de cumplimiento"""
        if capacidad == 0:
            return "rojo"
        
        # Aplicar nueva fórmula: (((TOTAL HEADWEAR/CAPACIDAD)*100%)-100%)
        porcentaje_cumplimiento = ((total_headwear / capacidad) * 100) - 100
        
        if porcentaje_cumplimiento < 0:  # Valores negativos
            return "rojo"
        elif 0 <= porcentaje_cumplimiento <= 15:  # 0% a 15%
            return "verde"
        else:  # Mayores al 15%
            return "amarillo"
    
    def calculate_performance_metrics(self, stock_data: List[Dict]) -> Dict[str, Any]:
        """Calcula métricas de rendimiento del stock"""
        if not stock_data:
            return {}
        
        total_stock = sum(item.get('stock', 0) for item in stock_data)
        total_capacity = sum(item.get('capacity', 0) for item in stock_data if item.get('capacity', 0) > 0)
        
        return {
            'total_stock': total_stock,
            'total_capacity': total_capacity,
            'capacity_utilization': total_stock / total_capacity if total_capacity > 0 else 0,
            'low_stock_stores': len([item for item in stock_data if self._is_low_stock(item)]),
            'overstock_stores': len([item for item in stock_data if self._is_overstock(item)])
        }
    
    def _is_low_stock(self, item: Dict) -> bool:
        """Verifica si una tienda tiene stock bajo"""
        capacity = item.get('capacity', 0)
        stock = item.get('stock', 0)
        if capacity == 0:
            return False
        return stock < (capacity * 0.95)
    
    def _is_overstock(self, item: Dict) -> bool:
        """Verifica si una tienda tiene sobrestock"""
        capacity = item.get('capacity', 0)
        stock = item.get('stock', 0)
        if capacity == 0:
            return False
        return stock > capacity

# Instancia del analizador
stock_analyzer = StockAnalyzer(config)

class DataLoader:
    """Cargador de datos con validación robusta"""
    
    def __init__(self, country_manager: CountryManager):
        self.country_manager = country_manager
        self.required_columns = ['U_Marca', 'U_Silueta', 'Stock_Actual', 'Bodega', 'U_Liga', 'U_Segmento']
    
    def cargar_archivo(self, label_texto: str, pais: str) -> Optional[pd.DataFrame]:
        """Carga y valida el archivo CSV con manejo robusto"""
        archivo = st.file_uploader(label_texto, type=["csv"], key=f"uploader_{pais}")
        
        if archivo is None:
            return None
        
        try:
            return self._process_file(archivo, pais)
        except Exception as e:
            logger.error(f"Error al cargar archivo {pais}: {str(e)}")
            st.error(f"Error al cargar archivo {pais}: {str(e)}")
            return None
    
    def _process_file(self, archivo, pais: str) -> pd.DataFrame:
        """Procesa el archivo CSV"""
        with st.spinner(f"Cargando archivo {pais}..."):
            start_time = time.time()
            logger.info(f"Iniciando carga de archivo para {pais}")
            
            df = self._read_csv(archivo)
            df = self._clean_data(df)
            df = self._filter_by_country(df, pais)
            self._validate_columns(df, pais)
            
            # Actualizar la fecha del último trabajo con stock
            current_date = datetime.now().strftime('%d/%m/%Y')
            st.session_state.last_stock_work_date = current_date
            
            elapsed_time = time.time() - start_time
            logger.info(f"Archivo {pais} cargado exitosamente en {elapsed_time:.2f}s - Registros: {len(df):,}")
            st.success(f"✅ Archivo {pais} cargado ({elapsed_time:.2f}s) | Registros: {len(df):,}")
            return df
    
    def _read_csv(self, archivo) -> pd.DataFrame:
        """Lee el archivo CSV con configuración optimizada"""
        return pd.read_csv(
            archivo,
            encoding='utf-8',
            delimiter=';',
            dtype={'U_Silueta': str, 'Stock_Actual': str, 'Bodega': str, 'U_Liga': str, 'U_Segmento': str},
            low_memory=False,
            on_bad_lines='skip'
        )
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia y normaliza los datos"""
        df.columns = df.columns.str.strip()
        df['Bodega'] = df['Bodega'].astype(str).str.strip()
        df['U_Liga'] = df['U_Liga'].astype(str).str.strip().str.upper()
        df['U_Segmento'] = df['U_Segmento'].astype(str).str.strip().str.upper()
        
        # Conversión segura de stock a numérico
        df['Stock_Actual'] = pd.to_numeric(
            df['Stock_Actual'].str.replace(',', ''),
            errors='coerce'
        ).fillna(0)
        
        return df
    
    def _filter_by_country(self, df: pd.DataFrame, pais: str) -> pd.DataFrame:
        """Filtra datos por país y marca NEW ERA"""
        # Primero filtrar por marca NEW ERA
        df_new_era = df[df['U_Marca'].str.upper() == 'NEW ERA']
        
        # Luego filtrar por bodegas del país
        bodegas = self.country_manager.get_bodegas(pais)
        return df_new_era[df_new_era['Bodega'].isin(bodegas)] if bodegas else df_new_era
    
    def _validate_columns(self, df: pd.DataFrame, pais: str) -> None:
        """Valida que existan las columnas requeridas"""
        if not all(col in df.columns for col in self.required_columns):
            logger.error(f"Faltan columnas requeridas en el archivo de {pais}")
            st.error(f"❌ Faltan columnas requeridas en el archivo de {pais}")
            raise ValueError(f"Faltan columnas requeridas: {self.required_columns}")

# Instancia del cargador de datos
data_loader = DataLoader(country_manager)

class DataProcessor:
    """Procesador de datos consolidados"""
    
    def __init__(self, country_manager: CountryManager, league_categories: LeagueCategories, 
                 product_classifier: ProductClassification):
        self.country_manager = country_manager
        self.league_categories = league_categories
        self.product_classifier = product_classifier
    
    @st.cache_data
    def procesar_datos_consolidados(_self, df_hash: List[Dict], pais: str, selected_league: str = None) -> Optional[pd.DataFrame]:
        """Procesa los datos para generar tabla con múltiples niveles de encabezados"""
        df = pd.DataFrame(df_hash)
        
        if df is None or df.empty:
            return None
        
        with st.spinner(f"Generando tabla consolidada {pais}..."):
            logger.info(f"Iniciando procesamiento de datos consolidados para {pais}")
            
            df = _self._prepare_data(df)
            tabla_final = _self._create_base_table(pais)
            tabla_final = _self._process_categories(df, tabla_final, pais, selected_league)
            tabla_final = _self._calculate_totals(tabla_final, pais, selected_league)
            tabla_final = _self._format_table(tabla_final)
            
            logger.info(f"Procesamiento completado para {pais}")
            return tabla_final
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepara los datos para el procesamiento"""
        # Asegurar que U_Silueta sea string y manejar valores NaN
        df['U_Silueta'] = df['U_Silueta'].astype(str).fillna('').str.strip().str.upper()
        df['Tipo'] = df['U_Silueta'].apply(self.product_classifier.clasificar_silueta)
        
        # Filtrar solo siluetas válidas, Apparel y Accessories
        return df[(df['Tipo'].notna()) | (df['U_Segmento'] == 'APPAREL') | (df['U_Segmento'] == 'ACCESSORIES')].copy()
    
    def _create_base_table(self, pais: str) -> pd.DataFrame:
        """Crea la tabla base con las bodegas del país"""
        bodegas = self.country_manager.get_bodegas(pais)
        return pd.DataFrame(index=bodegas)
    
    def _process_categories(self, df: pd.DataFrame, tabla_final: pd.DataFrame, pais: str, selected_league: str = None) -> pd.DataFrame:
        """Procesa cada categoría de liga"""
        # Usar el parámetro pasado en lugar de session_state para compatibilidad con cache
        
        if selected_league:
            # Filtrar solo por la liga seleccionada
            categorias_a_procesar = {selected_league: self.league_categories.get_category_values(selected_league)}
            logger.info(f"Filtrado por liga específica: {selected_league}")
            logger.info(f"Valores de la liga: {categorias_a_procesar[selected_league]}")
        else:
            # Procesar todas las categorías
            categorias_a_procesar = self.league_categories.get_all_categories()
            logger.info("Procesando todas las categorías")
        
        for categoria, valores in categorias_a_procesar.items():
            df_cat = df[df['U_Liga'].str.upper().isin([v.upper() for v in valores])]
            logger.info(f"Categoría: {categoria}, Registros filtrados: {len(df_cat)}")
            
            if len(df_cat) == 0:
                logger.warning(f"No se encontraron datos para la categoría {categoria}")
                continue
            
            # Procesar Planas y Curvas
            pivot = self._process_headwear_types(df_cat)
            
            # Procesar Apparel
            apparel = self._process_apparel(df_cat)
            
            # Combinar resultados
            pivot = pivot.join(apparel, how='left').fillna(0)
            
            if selected_league:
                # Para liga específica, usar nombres simplificados
                pivot.columns = [f"TOTAL {col.upper()}" if col in ['Planas', 'Curvas'] 
                               else f"TOTAL {col.upper()}" for col in pivot.columns]
                logger.info(f"Columnas generadas para liga específica: {list(pivot.columns)}")
            else:
                # Para todas las ligas, usar el formato original
                pivot.columns = [f"{categoria} - {col}" for col in pivot.columns]
                logger.info(f"Columnas generadas para todas las ligas: {list(pivot.columns)}")
            
            tabla_final = tabla_final.join(pivot, how='left')
        
        # Procesar Accessories solo si no hay liga específica o si la liga específica aplica
        if not selected_league:
            accessories = self._process_accessories(df)
            tabla_final = tabla_final.join(accessories, how='left').fillna(0)
        else:
            # Para liga específica, procesar accessories solo de esa liga
            df_league = df[df['U_Liga'].str.upper().isin([v.upper() for v in categorias_a_procesar[selected_league]])]
            accessories = self._process_accessories(df_league)
            accessories = accessories.rename('TOTAL ACCESSORIES')
            tabla_final = tabla_final.join(accessories, how='left').fillna(0)
        
        return tabla_final.fillna(0).astype(int)
    
    def _process_headwear_types(self, df_cat: pd.DataFrame) -> pd.DataFrame:
        """Procesa tipos de headwear (planas y curvas)"""
        return df_cat[df_cat['Tipo'].notna()].pivot_table(
            index='Bodega',
            columns='Tipo',
            values='Stock_Actual',
            aggfunc='sum',
            fill_value=0
        )
    
    def _process_apparel(self, df_cat: pd.DataFrame) -> pd.Series:
        """Procesa datos de apparel"""
        return df_cat[df_cat['U_Segmento'] == 'APPAREL'].groupby('Bodega')['Stock_Actual'].sum().rename('Apparel')
    
    def _process_accessories(self, df: pd.DataFrame) -> pd.Series:
        """Procesa datos de accessories"""
        return df[df['U_Segmento'] == 'ACCESSORIES'].groupby('Bodega')['Stock_Actual'].sum().rename('TOTAL ACCESSORIES')
    
    def _calculate_totals(self, tabla_final: pd.DataFrame, pais: str, selected_league: str = None) -> pd.DataFrame:
        """Calcula totales y métricas"""
        
        if selected_league:
            # Para liga específica, los totales ya están calculados con nombres TOTAL
            if 'TOTAL PLANAS' not in tabla_final.columns:
                tabla_final['TOTAL PLANAS'] = tabla_final[[col for col in tabla_final.columns if 'PLANAS' in col.upper()]].sum(axis=1)
            if 'TOTAL CURVAS' not in tabla_final.columns:
                tabla_final['TOTAL CURVAS'] = tabla_final[[col for col in tabla_final.columns if 'CURVAS' in col.upper()]].sum(axis=1)
            
            tabla_final['TOTAL HEADWEAR'] = tabla_final['TOTAL PLANAS'] + tabla_final['TOTAL CURVAS']
            
            if 'TOTAL APPAREL' not in tabla_final.columns:
                tabla_final['TOTAL APPAREL'] = tabla_final[[col for col in tabla_final.columns if 'APPAREL' in col.upper()]].sum(axis=1)
            
            # No calcular % DE CUMPLIMIENTO para liga específica
            tabla_final['TOTAL GENERAL'] = tabla_final[['TOTAL HEADWEAR', 'TOTAL APPAREL', 'TOTAL ACCESSORIES']].sum(axis=1)
        else:
            # Lógica original para todas las ligas
            tabla_final['TOTAL PLANAS'] = tabla_final[[col for col in tabla_final.columns if 'Planas' in col]].sum(axis=1)
            tabla_final['TOTAL CURVAS'] = tabla_final[[col for col in tabla_final.columns if 'Curvas' in col]].sum(axis=1)
            tabla_final['TOTAL HEADWEAR'] = tabla_final['TOTAL PLANAS'] + tabla_final['TOTAL CURVAS']
            
            # Agregar capacidad
            capacidades = self.country_manager.get_capacidades(pais)
            tabla_final['CAPACIDAD EN TIENDA'] = tabla_final.index.map(lambda x: capacidades.get(x, 0))
            
            # Calcular % DE CUMPLIMIENTO
            tabla_final['% DE CUMPLIMIENTO'] = (((tabla_final['TOTAL HEADWEAR'] / tabla_final['CAPACIDAD EN TIENDA']) * 100) - 100).replace([np.inf, -np.inf], 0).fillna(0)
            tabla_final['% DE CUMPLIMIENTO'] = tabla_final['% DE CUMPLIMIENTO'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) and x != 0 else "N/A")
            
            tabla_final['TOTAL APPAREL'] = tabla_final[[col for col in tabla_final.columns if 'Apparel' in col]].sum(axis=1)
            tabla_final['TOTAL GENERAL'] = tabla_final[['TOTAL HEADWEAR', 'TOTAL APPAREL', 'TOTAL ACCESSORIES']].sum(axis=1)
        
        # Ordenar por TOTAL GENERAL
        tabla_final = tabla_final.sort_values('TOTAL GENERAL', ascending=False)
        
        # Agregar fila de TOTALES
        return self._add_totals_row(tabla_final, pais)
    
    def _add_totals_row(self, tabla_final: pd.DataFrame, pais: str) -> pd.DataFrame:
        """Agrega fila de totales"""
        fila_totales = tabla_final.sum()
        
        capacidad_total = self.country_manager.get_country_data(pais).get_total_capacity()
        total_headwear_suma = fila_totales['TOTAL HEADWEAR']
        
        if capacidad_total > 0:
            porcentaje_total = ((total_headwear_suma / capacidad_total) * 100) - 100
            fila_totales['% DE CUMPLIMIENTO'] = f"{porcentaje_total:.2f}%"
        else:
            fila_totales['% DE CUMPLIMIENTO'] = "N/A"
        
        fila_totales['CAPACIDAD EN TIENDA'] = capacidad_total
        tabla_final.loc['TOTAL'] = fila_totales
        
        return tabla_final
    
    def _format_table(self, tabla_final: pd.DataFrame) -> pd.DataFrame:
        """Formatea la tabla final con MultiIndex"""
        tabla_final.reset_index(inplace=True)
        tabla_final.rename(columns={'index': 'Bodega'}, inplace=True)
        
        # Crear MultiIndex para columnas
        columnas_multi = [('', 'Bodega')]
        
        for categoria in self.league_categories.get_all_categories().keys():
            columnas_multi.extend([
                (categoria, 'Planas'),
                (categoria, 'Curvas'),
                (categoria, 'Apparel')
            ])
        
        columnas_multi.extend([
            ('', 'TOTAL PLANAS'),
            ('', 'TOTAL CURVAS'),
            ('', 'TOTAL HEADWEAR'),
            ('', 'CAPACIDAD EN TIENDA'),
            ('', '% DE CUMPLIMIENTO'),
            ('', 'TOTAL APPAREL'),
            ('', 'TOTAL ACCESSORIES'),
            ('', 'TOTAL GENERAL')
        ])
        
        # Verificar columnas existentes y reordenar
        columnas_existentes = []
        for col in columnas_multi:
            nombre_col = f"{col[0]} - {col[1]}" if col[0] else col[1]
            if nombre_col in tabla_final.columns:
                columnas_existentes.append(col)
        
        nombres_columnas = [f"{col[0]} - {col[1]}" if col[0] else col[1] for col in columnas_existentes]
        tabla_final = tabla_final[nombres_columnas]
        
        # Crear MultiIndex
        multi_index = pd.MultiIndex.from_tuples(columnas_existentes)
        tabla_final.columns = multi_index
        
        return tabla_final

# Instancia del procesador de datos
data_processor = DataProcessor(country_manager, league_categories, product_classifier)

class ChartVisualizer:
    """Visualizador de gráficas con Plotly"""
    
    def __init__(self, stock_analyzer: StockAnalyzer, country_manager: CountryManager):
        self.stock_analyzer = stock_analyzer
        self.country_manager = country_manager
    
    def mostrar_grafica_comparativa(self, tabla: pd.DataFrame, pais: str) -> None:
        """Muestra gráfica comparativa de Stock vs Capacidad por bodega"""
        if tabla is None:
            return
        
        logger.info(f"Generando gráfica comparativa para {pais}")
        
        selected_league = st.session_state.get('selected_league', None)
        
        if selected_league:
            st.markdown(f"#### 📊 Stock por Bodega - {selected_league} - {pais}")
        else:
            st.markdown(f"#### 📊 Comparativa Stock vs Capacidad - {pais}")
        
        df_grafica = self._prepare_chart_data(tabla, pais)
        fig = self._create_chart(df_grafica)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Solo mostrar alertas y análisis de performance si no hay liga específica
        if not selected_league:
            self._show_alerts(df_grafica, pais)
            self._show_performance_analysis(df_grafica, pais)
        else:
            self._show_performance_analysis(df_grafica, pais)
    
    def _prepare_chart_data(self, tabla: pd.DataFrame, pais: str) -> pd.DataFrame:
        """Prepara los datos para la gráfica"""
        datos_grafica = tabla[tabla[('', 'Bodega')] != 'TOTAL'].copy()
        
        # Excluir bodegas específicas de las gráficas por país
        if pais == "Guatemala":
            datos_grafica = datos_grafica[datos_grafica[('', 'Bodega')] != 'CENTRAL NEW ERA'].copy()
        elif pais == "El Salvador":
            datos_grafica = datos_grafica[datos_grafica[('', 'Bodega')] != 'New Era Central'].copy()
        elif pais == "PANAMA":
            datos_grafica = datos_grafica[datos_grafica[('', 'Bodega')] != 'Almacén general'].copy()
        elif pais == "Costa Rica":
            datos_grafica = datos_grafica[datos_grafica[('', 'Bodega')] != 'Bodega Central NEW ERA'].copy()
        
        # Verificar si existe la columna CAPACIDAD EN TIENDA
        if ('', 'CAPACIDAD EN TIENDA') in datos_grafica.columns:
            capacidad_data = datos_grafica[('', 'CAPACIDAD EN TIENDA')].tolist()
        else:
            # Para liga específica, no hay columna de capacidad
            capacidad_data = [0] * len(datos_grafica)
        
        df_grafica = pd.DataFrame({
            'Bodega': datos_grafica[('', 'Bodega')].tolist(),
            'Stock': datos_grafica[('', 'TOTAL HEADWEAR')].tolist(),
            'Capacidad': capacidad_data
        })
        
        return df_grafica.sort_values('Stock', ascending=True)
    
    def _create_chart(self, df_grafica: pd.DataFrame) -> go.Figure:
        """Crea una gráfica ultra minimalista y limpia"""
        fig = go.Figure()
        
        selected_league = st.session_state.get('selected_league', None)
        
        # Barras de Capacidad - diseño minimalista (solo si no hay liga específica)
        if not selected_league and any(cap > 0 for cap in df_grafica['Capacidad']):
            fig.add_trace(go.Bar(
                y=df_grafica['Bodega'],
                x=df_grafica['Capacidad'],
                name='Capacidad Máxima',
                orientation='h',
                marker=dict(
                    color='rgba(0, 0, 0, 0.8)',
                    line=dict(width=0)  # Sin bordes para look minimalista
                ),
                text=[f"{x:,}" if x > 0 else "N/A" for x in df_grafica['Capacidad']],
                textposition='outside',
                textfont=dict(size=12, color='rgba(0, 0, 0, 0.8)'),
                hovertemplate='<b>%{y}</b><br>Capacidad: %{x:,}<extra></extra>',
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="rgba(0, 0, 0, 0.1)",
                    font=dict(color="#000", size=12)
                )
            ))
        
        # Barras de Stock - diseño minimalista
        fig.add_trace(go.Bar(
            y=df_grafica['Bodega'],
            x=df_grafica['Stock'],
            name='Stock Actual',
            orientation='h',
            marker=dict(
                color='rgba(107, 114, 128, 0.8)',
                line=dict(width=0)  # Sin bordes
            ),
            text=[f"{x:,}" for x in df_grafica['Stock']],
            textposition='outside',
            textfont=dict(size=12, color='rgba(107, 114, 128, 0.8)'),
            hovertemplate='<b>%{y}</b><br>Stock: %{x:,}<extra></extra>',
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="rgba(107, 114, 128, 0.1)",
                font=dict(color="#6b7280", size=12)
            )
        ))
        
        # Anotaciones minimalistas
        self._add_overstock_annotations(fig, df_grafica)
        
        # Layout ultra minimalista
        fig.update_layout(
            # Sin títulos de ejes para máximo minimalismo
            xaxis_title="",
            yaxis_title="",
            barmode='group',
            height=max(600, len(df_grafica) * 45),
            margin=dict(l=20, r=20, t=20, b=20),
            
            # Leyenda minimalista
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color='#6b7280'),
                bgcolor='rgba(0,0,0,0)',  # Transparente
                borderwidth=0  # Sin borde
            ),
            
            # Ejes minimalistas
            xaxis=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(0, 0, 0, 0.05)',  # Grillas casi invisibles
                tickformat=',',
                tickfont=dict(size=11, color='#9ca3af'),
                showline=False,  # Sin líneas de ejes
                zeroline=False,  # Sin línea de cero
                ticks=""  # Sin marcas de tick
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=12, color='#374151'),
                showline=False,
                zeroline=False,
                ticks=""
            ),
            
            # Fondo completamente limpio
            plot_bgcolor='white',
            paper_bgcolor='white',
            
            # Sin marcos ni decoraciones
            showlegend=True,
            hovermode='closest'
        )
        
        return fig
    
    def _add_overstock_annotations(self, fig: go.Figure, df_grafica: pd.DataFrame) -> None:
        """Agrega anotaciones de sobrestock y faltante de stock"""
        if not any(cap > 0 for cap in df_grafica['Capacidad']):
            return
        
        # Calcular distancia de referencia
        distancia_referencia = self._calculate_reference_distance(df_grafica)
        
        for _, row in df_grafica.iterrows():
            if row['Capacidad'] > 0:
                max_value_bodega = max(row['Stock'], row['Capacidad'])
                annotation_position = max_value_bodega + (distancia_referencia * 0.3)
                
                # SOBRESTOCK (Stock > Capacidad) - Color amarillo dorado
                if row['Stock'] > row['Capacidad']:
                    fig.add_annotation(
                        x=annotation_position,
                        y=row['Bodega'],
                        text="SOBRESTOCK",
                        showarrow=False,
                        font=dict(size=9, color='#f59e0b', family='Arial Black'),  # Amarillo dorado
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor='#f59e0b',  # Amarillo dorado
                        borderwidth=1
                    )
                
                # FALTANTE DE STOCK (Stock < Capacidad) - Color rojo
                elif row['Stock'] < row['Capacidad']:
                    fig.add_annotation(
                        x=annotation_position,
                        y=row['Bodega'],
                        text="FALTANTE DE STOCK",
                        showarrow=False,
                        font=dict(size=9, color='#ef4444', family='Arial Black'),  # Rojo
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor='#ef4444',  # Rojo
                        borderwidth=1
                    )
    
    def _calculate_reference_distance(self, df_grafica: pd.DataFrame) -> float:
        """Calcula la distancia de referencia para anotaciones"""
        referencia_bodega = "NE Cayala"
        
        for _, row in df_grafica.iterrows():
            if row['Bodega'] == referencia_bodega and row['Capacidad'] > 0:
                max_value_cayala = max(row['Stock'], row['Capacidad'])
                return (max_value_cayala * 0.40) + (max_value_cayala * 0.10)
        
        return 1000  # Valor por defecto
    
    def _show_alerts(self, df_grafica: pd.DataFrame, pais: str) -> None:
        """Muestra alertas de stock con diseño compacto"""
        st.markdown("---")
        st.markdown("### 🚨 ALERTAS DE STOCK")
        
        alertas = []
        
        # Buscar todas las bodegas que tienen FALTANTE DE STOCK (Stock < Capacidad)
        for _, row in df_grafica.iterrows():
            bodega = row['Bodega']
            stock_actual = row['Stock']
            capacidad = row['Capacidad']
            
            # Condición para FALTANTE DE STOCK: Stock < Capacidad y Capacidad > 0
            if capacidad > 0 and stock_actual < capacidad:
                faltante = capacidad - stock_actual
                alertas.append({
                    'bodega': bodega,
                    'stock': stock_actual,
                    'capacidad': capacidad,
                    'faltante': faltante
                })
        
        if alertas:
            alertas.sort(key=lambda x: x['faltante'], reverse=True)
            
            # Crear recuadros compactos - hasta 3 por fila
            for i in range(0, len(alertas), 3):
                cols = st.columns(3)
                batch_alertas = alertas[i:i+3]
                
                for j, alerta in enumerate(batch_alertas):
                    with cols[j]:
                        self._create_compact_alert_card(alerta)
        else:
            # Mensaje moderno y amigable cuando no hay alertas usando componentes nativos
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                border: 2px solid #10b981;
                border-radius: 20px;
                padding: 30px;
                margin: 20px 0;
                text-align: center;
                box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
            ">
            """, unsafe_allow_html=True)
            
            # Icono grande centrado
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 4rem;">✅</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Mensaje principal
            st.markdown("""
            <h2 style="
                color: #065f46;
                text-align: center;
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 15px;
            ">
                ¡Excelente gestión de inventario!
            </h2>
            """, unsafe_allow_html=True)
            
            # Mensaje clave
            st.markdown("""
            <h3 style="
                color: #047857;
                text-align: center;
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 10px;
            ">
                Capacidades abastecidas con suficiente stock
            </h3>
            """, unsafe_allow_html=True)
            
            # Descripción
            st.markdown("""
            <p style="
                color: #059669;
                text-align: center;
                font-size: 1rem;
                margin-bottom: 20px;
            ">
                Todas las bodegas mantienen niveles óptimos de inventario
            </p>
            """, unsafe_allow_html=True)
            
            # Badges usando columnas
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                    <span style="
                        background: rgba(16, 185, 129, 0.2);
                        color: #065f46;
                        padding: 8px 16px;
                        border-radius: 20px;
                        font-size: 0.9rem;
                        font-weight: 600;
                        border: 1px solid rgba(16, 185, 129, 0.3);
                        display: inline-block;
                        margin: 5px;
                    ">
                        📊 Stock Óptimo
                    </span>
                    <span style="
                        background: rgba(16, 185, 129, 0.2);
                        color: #065f46;
                        padding: 8px 16px;
                        border-radius: 20px;
                        font-size: 0.9rem;
                        font-weight: 600;
                        border: 1px solid rgba(16, 185, 129, 0.3);
                        display: inline-block;
                        margin: 5px;
                    ">
                        🎯 Capacidades Completas
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            # Cerrar container
            st.markdown("</div>", unsafe_allow_html=True)
    
    def _create_compact_alert_card(self, alerta: dict) -> None:
        """Crea una card moderna usando componentes mixtos"""
        # Determinar severidad y colores
        porcentaje_faltante = (alerta['faltante'] / alerta['capacidad']) * 100
        
        if porcentaje_faltante >= 50:
            color_principal = "#dc2626"
            severidad = "CRÍTICO"
            icono = "🚨"
            bg_color = "#fee2e2"
        elif porcentaje_faltante >= 25:
            color_principal = "#ef4444"
            severidad = "MODERADO"
            icono = "⚠️"
            bg_color = "#fecaca"
        else:
            color_principal = "#f87171"
            severidad = "LEVE"
            icono = "📋"
            bg_color = "#fed7d7"
        
        # Container principal con fondo de color
        st.markdown(f"""
        <div style="
            background: {bg_color};
            border: 2px solid {color_principal};
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            position: relative;
        ">
        """, unsafe_allow_html=True)
        
        # Badge de severidad
        st.markdown(f"""
        <div style="
            position: absolute;
            top: -8px;
            right: 20px;
            background: {color_principal};
            color: white;
            padding: 6px 16px;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        ">
            {severidad}
        </div>
        """, unsafe_allow_html=True)
        
        # Header con nombre de bodega
        st.markdown(f"""
        <div style="text-align: center; padding: 15px 0;">
            <div style="
                background: white;
                border-radius: 15px;
                padding: 12px 24px;
                display: inline-block;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 1px solid rgba(0,0,0,0.1);
            ">
                <span style="font-size: 1.3rem; margin-right: 8px;">{icono}</span>
                <span style="
                    color: #000000; 
                    font-size: 1.2rem; 
                    font-weight: 700;
                ">{alerta['bodega']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas usando columnas de Streamlit
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 5px;
            ">
                <div style="color: {color_principal}; font-size: 2rem; font-weight: 800; margin-bottom: 8px;">
                    {alerta['faltante']:,}
                </div>
                <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">
                    Faltante
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 5px;
            ">
                <div style="color: #374151; font-size: 2rem; font-weight: 800; margin-bottom: 8px;">
                    {alerta['stock']:,}
                </div>
                <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">
                    Stock
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 5px;
            ">
                <div style="color: #374151; font-size: 2rem; font-weight: 800; margin-bottom: 8px;">
                    {alerta['capacidad']:,}
                </div>
                <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">
                    Capacidad
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Barra de progreso
        capacidad_utilizada = 100 - porcentaje_faltante
        st.markdown(f"""
        <div style="margin: 20px 10px 10px 10px;">
            <div style="
                background: rgba(255,255,255,0.8);
                border-radius: 10px;
                padding: 4px;
                overflow: hidden;
            ">
                <div style="
                    background: {color_principal};
                    height: 10px;
                    border-radius: 6px;
                    width: {capacidad_utilizada:.1f}%;
                    transition: width 0.8s ease;
                "></div>
            </div>
            <div style="
                text-align: center;
                margin-top: 8px;
                font-size: 0.85rem;
                color: #6b7280;
                font-weight: 600;
            ">
                {capacidad_utilizada:.1f}% de capacidad utilizada
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Cerrar container principal
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _show_performance_analysis(self, df_grafica: pd.DataFrame, pais: str) -> None:
        """Muestra análisis de performance con diseño profesional"""
        selected_league = st.session_state.get('selected_league', None)
        
        # Header profesional con colores según el país
        st.markdown("---")
        
        # Determinar colores según el país
        if pais == "PANAMA":
            # Rojo de la bandera de Panamá
            background_gradient = "linear-gradient(135deg, #dc2626 0%, #ef4444 100%)"
            box_shadow = "0 10px 30px rgba(220, 38, 38, 0.3)"
        elif pais == "Honduras":
            # Azul (anteriormente de Guatemala)
            background_gradient = "linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)"
            box_shadow = "0 10px 30px rgba(30, 64, 175, 0.3)"
        elif pais == "El Salvador":
            # Azul oscuro de la bandera de El Salvador
            background_gradient = "linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%)"
            box_shadow = "0 10px 30px rgba(30, 58, 138, 0.3)"
        elif pais == "Costa Rica":
            # Verde reciclaje de Costa Rica
            background_gradient = "linear-gradient(135deg, #16a34a 0%, #22c55e 100%)"
            box_shadow = "0 10px 30px rgba(22, 163, 74, 0.3)"
        elif pais == "Guatemala":
            # Celeste (anteriormente de Honduras)
            background_gradient = "linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%)"
            box_shadow = "0 10px 30px rgba(14, 165, 233, 0.3)"
        else:
            # Azul medio por defecto
            background_gradient = "linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)"
            box_shadow = "0 10px 30px rgba(30, 64, 175, 0.3)"
        
        st.markdown(f"""
        <div style="
            background: {background_gradient};
            padding: 2rem 3rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: {box_shadow};
            animation: slideInFromRight 0.8s ease-out;
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
            <div style="display: flex; align-items: center;">
                <div>
                    <h2 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 700;">
                        Análisis de Performance{f" - {selected_league}" if selected_league else ""}
                    </h2>
                    <p style="color: #d1d5db; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                        Indicadores clave de rendimiento por bodega{f" para {selected_league}" if selected_league else ""}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        selected_league = st.session_state.get('selected_league', None)
        
        if selected_league:
            # Para liga específica, usar todos los datos sin filtrar por capacidad
            df_analisis = df_grafica.copy()
            # No calcular porcentaje de cumplimiento para liga específica
        else:
            # Para vista completa, filtrar por capacidad como antes
            if not any(cap > 0 for cap in df_grafica['Capacidad']):
                return
            
            df_analisis = df_grafica[df_grafica['Capacidad'] > 0].copy()
            df_analisis['Porcentaje_Cumplimiento'] = (df_analisis['Stock'] / df_analisis['Capacidad']) * 100
        
        # Calcular métricas siempre que haya datos
        if len(df_analisis) > 0:
            max_stock = df_analisis.loc[df_analisis['Stock'].idxmax()]
            min_stock = df_analisis.loc[df_analisis['Stock'].idxmin()]
            promedio_stock = df_analisis['Stock'].mean()
        else:
            return
        
        # Métricas con diseño profesional igual que Métricas Generales
        cols = st.columns(3)
        
        if selected_league:
            metricas_performance = [
                (max_stock['Bodega'], f"{max_stock['Stock']:,}", f"Mayor Stock {selected_league}", "🏆", "#10b981"),
                (min_stock['Bodega'], f"{min_stock['Stock']:,}", f"Menor Stock {selected_league}", "📊", "#ef4444"),
                (f"{promedio_stock:,.0f}", "unidades", f"Promedio {selected_league}", "📈", "#6b7280")
            ]
        else:
            metricas_performance = [
                (max_stock['Bodega'], f"{max_stock['Stock']:,}", "Mayor Stock", "🏆", "#10b981"),
                (min_stock['Bodega'], f"{min_stock['Stock']:,}", "Menor Stock", "📊", "#ef4444"),
                (f"{promedio_stock:,.0f}", "unidades", "Promedio General", "📈", "#6b7280")
            ]
        
        for i, (valor_principal, valor_secundario, nombre, emoji, color) in enumerate(metricas_performance):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid {color};">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.5rem;">{emoji}</span>
                        <span style="color: {color}; font-weight: 600; font-size: 0.9rem;">{nombre.upper()}</span>
                    </div>
                    <div style="font-size: 1.4rem; font-weight: 700; color: #374151; margin-bottom: 0.25rem;">
                        {valor_principal}
                    </div>
                    <div style="color: #6b7280; font-size: 1.2rem; font-weight: 600;">
                        {valor_secundario}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Instancia del visualizador de gráficas
chart_visualizer = ChartVisualizer(stock_analyzer, country_manager)

def mostrar_grafica_comparativa(tabla, pais):
    """Wrapper para compatibilidad"""
    chart_visualizer.mostrar_grafica_comparativa(tabla, pais)

def mostrar_tabla_consolidada(tabla, pais):
    """Muestra la tabla con múltiples niveles de encabezados"""
    if tabla is None:
        return
    
    logger.info(f"Mostrando tabla consolidada para {pais}")
    
    professional_design.create_section_header(
        f"Tabla Consolidada - {pais}", 
        "Detalle completo de inventario por bodega y categoría",
        "📊"
    )
    
    # Generar estilos dinámicos para el semáforo
    estilos_semaforo = []
    capacidades = country_manager.get_capacidades(pais)
    
    # Encontrar la posición de la columna "% DE CUMPLIMIENTO"
    col_cumplimiento_index = None
    for idx, col in enumerate(tabla.columns):
        if col[1] == '% DE CUMPLIMIENTO':
            col_cumplimiento_index = idx + 1  # +1 porque CSS es 1-based
            break
    
    if col_cumplimiento_index is None:
        logger.warning("No se encontró la columna % DE CUMPLIMIENTO")
        col_cumplimiento_index = 17  # Fallback al valor original
    
    for i, fila in tabla.iterrows():
        bodega = fila[('', 'Bodega')]
        total_headwear = fila[('', 'TOTAL HEADWEAR')]
        
        if bodega == 'TOTAL':
            capacidad = country_manager.get_country_data(pais).get_total_capacity()
        else:
            capacidad = capacidades.get(bodega, 0)
        
        if capacidad > 0:
            color = stock_analyzer.obtener_color_semaforo(total_headwear, capacidad)
            
            if color == "verde":
                color_css = "#28a745"  # Verde
            elif color == "amarillo":
                color_css = "#ffc107"  # Amarillo
            else:
                color_css = "#dc3545"  # Rojo
        else:
            color_css = "#6c757d"  # Gris para N/A
        
        # Crear selector CSS para la celda específica
        estilos_semaforo.append(f"""
            .stDataFrame tbody tr:nth-child({i+1}) td:nth-child({col_cumplimiento_index}) {{
                background-color: {color_css} !important;
                color: white !important;
                font-weight: bold !important;
            }}
        """)
    
    # CSS mejorado con semáforo y encabezados centrados
    st.markdown(f"""
    <style>
        /* Encabezados principales (nivel 0) - centrados */
        .stMultiIndex th.level0:not(:first-child) {{
            font-size: 16px !important;
            font-weight: 900 !important;
            text-align: center !important;
            background-color: #4a7a8c !important;
            color: white !important;
            vertical-align: middle !important;
        }}
        
        /* Subencabezados (nivel 1) - centrados */
        .stMultiIndex th.level1 {{
            font-size: 13px !important;
            font-weight: 800 !important;
            background-color: #f0f0f0 !important;
            text-align: center !important;
            vertical-align: middle !important;
        }}
        
        /* Primera columna (Bodega) - centrada */
        .stMultiIndex th.level0:first-child {{
            background-color: #4a7a8c !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
            vertical-align: middle !important;
        }}
        
        /* Todos los encabezados th - forzar centrado con mayor especificidad */
        .stDataFrame thead th,
        .stDataFrame th,
        div[data-testid="stDataFrame"] table thead th,
        div[data-testid="stDataFrame"] th {{
            text-align: center !important;
            vertical-align: middle !important;
        }}
        
        /* Centrar contenido de encabezados con texto específico */
        .stDataFrame th:contains("MLB"),
        .stDataFrame th:contains("NBA"), 
        .stDataFrame th:contains("NFL"),
        .stDataFrame th:contains("MOTORSPORT"),
        .stDataFrame th:contains("NEW ERA"),
        .stDataFrame th:contains("Planas"),
        .stDataFrame th:contains("Curvas"),
        .stDataFrame th:contains("Apparel") {{
            text-align: center !important;
        }}
        
        /* Forzar centrado en todos los headers de tabla */
        table thead th,
        table th {{
            text-align: center !important;
            vertical-align: middle !important;
        }}
        
        /* Fila de totales */
        .stDataFrame tr:last-child td {{
            background-color: #d35400 !important;
            color: white !important;
            font-weight: bold !important;
        }}
        
        /* Celdas de datos */
        .stDataFrame td {{
            text-align: center !important;
            vertical-align: middle !important;
        }}
        
        /* Estilos del semáforo */
        {''.join(estilos_semaforo)}
    </style>
    """, unsafe_allow_html=True)

    # Formatear números con separadores de miles
    tabla_formateada = tabla.copy()
    for col in tabla_formateada.columns:
        if col[1] not in ['Bodega', '% DE CUMPLIMIENTO']:  # Excluir porcentaje
            tabla_formateada[col] = tabla_formateada[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "0")
        elif col[1] == '% DE CUMPLIMIENTO':
            tabla_formateada[col] = tabla_formateada[col].astype(str)  # Ya está formateado
    
    st.dataframe(
        tabla_formateada,
        height=min(800, 35 * (len(tabla) + 1)),
        use_container_width=True
    )
    
    # Mostrar métricas resumidas mejoradas
    selected_league = st.session_state.get('selected_league', None)
    
    if selected_league:
        professional_design.create_section_header(
            f"Métricas {selected_league} - {pais}", 
            f"Resumen ejecutivo de inventario específico para {selected_league}",
            "📈"
        )
    else:
        professional_design.create_section_header(
            f"Métricas Generales - {pais}", 
            "Resumen ejecutivo de inventario por categoría",
            "📈"
        )
    
    cols = st.columns(4)
    
    metricas = [
        ('TOTAL HEADWEAR', 'Headwear Total', "🧢", "#6b7280"),
        ('TOTAL APPAREL', 'Apparel Total', "👕", "#9ca3af"),
        ('TOTAL ACCESSORIES', 'Accessories Total', "🧦", "#374151"),
        ('TOTAL GENERAL', 'Inventario Total', "📦", "#4b5563")
    ]
    
    for i, (col, nombre, emoji, color) in enumerate(metricas):
        with cols[i]:
            valor = tabla[('', col)].iloc[-1]
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {color};">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.5rem;">{emoji}</span>
                    <span style="color: {color}; font-weight: 600; font-size: 0.9rem;">{nombre.upper()}</span>
                </div>
                <div style="font-size: 2rem; font-weight: 700; color: #374151; margin-bottom: 0.25rem;">
                    {valor:,}
                </div>
                <div style="color: #6b7280; font-size: 0.85rem;">
                    unidades en stock{f" - {selected_league}" if selected_league else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # AGREGAR GRÁFICA COMPARATIVA
    if selected_league:
        professional_design.create_section_header(
            f"Análisis Visual {selected_league} - {pais}", 
            f"Visualización interactiva de stock específico para {selected_league}",
            "📊"
        )
    else:
        professional_design.create_section_header(
            f"Análisis Visual - {pais}", 
            "Comparativa interactiva de stock vs capacidad por bodega",
            "📊"
        )
    mostrar_grafica_comparativa(tabla, pais)

def exportar_excel_consolidado(tabla, nombre_archivo, pais):
    """Exporta la tabla consolidada a Excel con formato profesional"""
    if tabla is None:
        st.warning(f"No hay datos para exportar de {pais}")
        return
    
    try:
        selected_league = st.session_state.get('selected_league', None)
        
        if selected_league:
            logger.info(f"Iniciando exportación a Excel para {selected_league} - {pais}")
        else:
            logger.info(f"Iniciando exportación a Excel para {pais}")
        
        # Crear copia del DataFrame para exportación
        df_export = tabla.copy()
        df_export.columns = [' - '.join(col).strip(' - ') for col in df_export.columns.values]
        
        # Crear archivo Excel
        if selected_league:
            nombre_excel = f"stock_{selected_league.lower()}_{pais.lower().replace(' ', '_')}.xlsx"
        else:
            nombre_excel = f"stock_consolidado_{pais.lower().replace(' ', '_')}.xlsx"
        output = pd.ExcelWriter(nombre_excel, engine='openpyxl')
        
        if selected_league:
            sheet_name = f"{selected_league} {pais}"
        else:
            sheet_name = f"Stock {pais}"
        
        df_export.to_excel(output, sheet_name=sheet_name, index=False)
        
        # Aplicar formato
        workbook = output.book
        worksheet = output.sheets[sheet_name]
        
        # Estilos
        header_fill = PatternFill(start_color='4a7a8c', end_color='4a7a8c', fill_type='solid')
        header_font = Font(color='FFFFFF', bold=True, size=14)
        
        total_fill = PatternFill(start_color='d35400', end_color='d35400', fill_type='solid')
        total_font = Font(color='FFFFFF', bold=True, size=14)
        
        normal_font = Font(color='000000', size=10)
        
        # Colores para el semáforo
        verde_fill = PatternFill(start_color='28a745', end_color='28a745', fill_type='solid')
        amarillo_fill = PatternFill(start_color='ffc107', end_color='ffc107', fill_type='solid')
        rojo_fill = PatternFill(start_color='dc3545', end_color='dc3545', fill_type='solid')
        gris_fill = PatternFill(start_color='6c757d', end_color='6c757d', fill_type='solid')
        semaforo_font = Font(color='FFFFFF', bold=True, size=10)
        
        border = Border(
            left=Side(style='thin'), 
            right=Side(style='thin'), 
            top=Side(style='thin'), 
            bottom=Side(style='thin')
        )
        center_alignment = Alignment(horizontal='center', vertical='center')
        
        # Aplicar formatos
        for row in worksheet.iter_rows():
            for cell in row:
                cell.border = border
                cell.alignment = center_alignment
                
                if cell.row == 1:
                    cell.fill = header_fill
                    cell.font = header_font
                elif cell.row == worksheet.max_row:
                    cell.fill = total_fill
                    cell.font = total_font
                else:
                    cell.font = normal_font
        
        # Aplicar semáforo a la columna "% DE CUMPLIMIENTO"
        col_cumplimiento = None
        for col in range(1, worksheet.max_column + 1):
            if worksheet.cell(row=1, column=col).value == "% DE CUMPLIMIENTO":
                col_cumplimiento = col
                break
        
        if col_cumplimiento:
            capacidades = country_manager.get_capacidades(pais)
            
            for row in range(2, worksheet.max_row + 1):
                bodega = worksheet.cell(row=row, column=1).value
                
                # Buscar total_headwear en la fila correspondiente
                total_headwear = 0
                for col in range(1, worksheet.max_column + 1):
                    if worksheet.cell(row=1, column=col).value == "TOTAL HEADWEAR":
                        total_headwear = worksheet.cell(row=row, column=col).value or 0
                        break
                
                if bodega == 'TOTAL':
                    capacidad = country_manager.get_country_data(pais).get_total_capacity()
                else:
                    capacidad = capacidades.get(bodega, 0)
                
                cell = worksheet.cell(row=row, column=col_cumplimiento)
                
                if capacidad > 0:
                    color = stock_analyzer.obtener_color_semaforo(total_headwear, capacidad)
                    if color == "verde":
                        cell.fill = verde_fill
                    elif color == "amarillo":
                        cell.fill = amarillo_fill
                    else:
                        cell.fill = rojo_fill
                else:
                    cell.fill = gris_fill
                
                if row == worksheet.max_row:
                    cell.font = Font(color='FFFFFF', bold=True, size=14)
                else:
                    cell.font = semaforo_font
        
        # Autoajustar columnas
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            adjusted_width = (max_length + 2) * 1.1
            worksheet.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width
        
        # Agregar información adicional
        info_row = worksheet.max_row + 2
        worksheet.cell(row=info_row, column=1, value="Fecha:").font = Font(bold=True)
        worksheet.cell(row=info_row, column=2, value=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        worksheet.cell(row=info_row+1, column=1, value="Archivo origen:").font = Font(bold=True)
        worksheet.cell(row=info_row+1, column=2, value=nombre_archivo)
        
        worksheet.cell(row=info_row+2, column=1, value="País:").font = Font(bold=True)
        worksheet.cell(row=info_row+2, column=2, value=pais)
        
        # Agregar leyenda del semáforo
        worksheet.cell(row=info_row+4, column=1, value="Leyenda Semáforo:").font = Font(bold=True)
        worksheet.cell(row=info_row+5, column=1, value="Verde: 100%-115%").fill = verde_fill
        worksheet.cell(row=info_row+5, column=1).font = semaforo_font
        worksheet.cell(row=info_row+6, column=1, value="Amarillo: >115%").fill = amarillo_fill
        worksheet.cell(row=info_row+6, column=1).font = semaforo_font
        worksheet.cell(row=info_row+7, column=1, value="Rojo: <100%").fill = rojo_fill
        worksheet.cell(row=info_row+7, column=1).font = semaforo_font
        worksheet.cell(row=info_row+8, column=1, value="Gris: Sin capacidad definida").fill = gris_fill
        worksheet.cell(row=info_row+8, column=1).font = semaforo_font
        
        output.close()
        
        # Descargar archivo
        with open(nombre_excel, "rb") as f:
            st.download_button(
                label=f"📤 Descargar Reporte {pais}",
                data=f,
                file_name=f"STOCK_CONSOLIDADO_{pais.upper().replace(' ', '_')}_{config.fecha_reporte}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"download_{pais}"
            )
        
        # Limpiar archivo temporal
        os.remove(nombre_excel)
        logger.info(f"Exportación a Excel completada para {pais}")
        
    except Exception as e:
        logger.error(f"Error al exportar {pais}: {str(e)}")
        st.error(f"Error al exportar {pais}: {str(e)}")

def main():
    """Función principal"""
    logger.info("Iniciando aplicación New Era Analytics Dashboard")
    
    # Inyectar CSS personalizado
    professional_design.inject_custom_css()
    
    # Crear header principal con hora en tiempo real
    professional_design.create_main_header()
    
    # Descripción con diseño mejorado
    professional_design.create_leagues_section()
    
    # Crear pestañas para cada país con iconos mejorados
    tab_guatemala, tab_el_salvador, tab_honduras, tab_costa_rica, tab_panama = st.tabs([
        "Guatemala", 
        "El Salvador", 
        "Honduras", 
        "Costa Rica",
        "Panamá"
    ])
    
    # PESTAÑA GUATEMALA
    with tab_guatemala:
        professional_design.create_section_header(
            "Análisis de Stock - Guatemala", 
            "Gestión de inventario para 24 tiendas en territorio guatemalteco",
            "GT"
        )
        
        archivo_guatemala = data_loader.cargar_archivo("📁 Subir archivo BASE_DE_DATOS.csv", "Guatemala")
        
        if archivo_guatemala is not None:
            # Crear hash del DataFrame para cache
            df_hash = archivo_guatemala.to_dict('records')
            
            # Procesar datos Guatemala (con cache)
            selected_league = st.session_state.get('selected_league', None)
            tabla_guatemala = data_processor.procesar_datos_consolidados(df_hash, "Guatemala", selected_league)
            
            # Mostrar resultados Guatemala
            mostrar_tabla_consolidada(tabla_guatemala, "Guatemala")
            
            # Sección de exportación dentro de la pestaña
            professional_design.create_section_header(
                "Exportar Reporte - Guatemala", 
                "Generar archivo Excel con formato profesional",
                "GT"
            )
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                nombre_original_gt = archivo_guatemala.name if hasattr(archivo_guatemala, 'name') else "BASE_DE_DATOS.csv"
                nombre_archivo_gt = st.text_input("📝 Nombre del archivo origen", nombre_original_gt, key="nombre_gt")
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
                if st.button("🚀 Generar Excel Guatemala", key="excel_gt", use_container_width=True):
                    exportar_excel_consolidado(tabla_guatemala, nombre_archivo_gt, "Guatemala")
        else:
            # Mensaje de bienvenida cuando no hay archivo
            st.markdown("""
            <div class="country-card country-card-gt">
                <div class="country-flag">🇬🇹</div>
                <h3 class="country-title" style="color: #0ea5e9; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem;">Guatemala - Sistema de Stock</h3>
                <p class="country-description" style="color: #64748b; font-size: 1rem; font-weight: 500; line-height: 1.6; margin-bottom: 0; background: rgba(186, 230, 253, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(186, 230, 253, 0.3);">
                    Selecciona tu archivo BASE_DE_DATOS.csv para comenzar el análisis completo del inventario<br>
                    <strong style="color: #0ea5e9;">24 tiendas</strong> en operación
                </p>
            </div>
            """, unsafe_allow_html=True)

    # PESTAÑA PANAMA
    with tab_panama:
        professional_design.create_section_header(
            "Análisis de Stock - Panamá", 
            "Gestión de inventario para 6 tiendas estratégicas en Panamá",
            "PA"
        )
        
        archivo_panama = data_loader.cargar_archivo("📁 Subir archivo PANAMA.csv", "PANAMA")
        
        if archivo_panama is not None:
            # Crear hash del DataFrame para cache
            df_hash = archivo_panama.to_dict('records')
            
            # Procesar datos Panamá (con cache)
            selected_league = st.session_state.get('selected_league', None)
            tabla_panama = data_processor.procesar_datos_consolidados(df_hash, "PANAMA", selected_league)
            
            # Mostrar resultados Panamá
            mostrar_tabla_consolidada(tabla_panama, "PANAMA")
            
            # Sección de exportación dentro de la pestaña
            professional_design.create_section_header(
                "Exportar Reporte - Panamá", 
                "Generar archivo Excel con formato profesional",
                "PA"
            )
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                nombre_original_pa = archivo_panama.name if hasattr(archivo_panama, 'name') else "PANAMA.csv"
                nombre_archivo_pa = st.text_input("📝 Nombre del archivo origen", nombre_original_pa, key="nombre_pa")
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
                if st.button("🚀 Generar Excel PANAMA", key="excel_pa", use_container_width=True):
                    exportar_excel_consolidado(tabla_panama, nombre_archivo_pa, "PANAMA")
        else:
            # Mensaje de bienvenida cuando no hay archivo
            st.markdown("""
            <div class="country-card country-card-pa">
                <div class="country-flag">🇵🇦</div>
                <h3 class="country-title" style="color: #dc2626; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem;">Panamá - Sistema de Stock</h3>
                <p class="country-description" style="color: #64748b; font-size: 1rem; font-weight: 500; line-height: 1.6; margin-bottom: 0; background: rgba(254, 202, 202, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(254, 202, 202, 0.3);">
                    Selecciona tu archivo PANAMA.csv para comenzar el análisis de las 6 bodegas de Panamá<br>
                    <strong style="color: #dc2626;">6 tiendas</strong> en operación
                </p>
            </div>
            """, unsafe_allow_html=True)

    # PESTAÑA HONDURAS
    with tab_honduras:
        professional_design.create_section_header(
            "Análisis de Stock - Honduras", 
            "Gestión de inventario para 5 tiendas en Honduras",
            "HN"
        )
        
        archivo_honduras = data_loader.cargar_archivo("📁 Subir archivo HONDURAS.csv", "Honduras")
        
        if archivo_honduras is not None:
            # Crear hash del DataFrame para cache
            df_hash = archivo_honduras.to_dict('records')
            
            # Procesar datos Honduras (con cache)
            selected_league = st.session_state.get('selected_league', None)
            tabla_honduras = data_processor.procesar_datos_consolidados(df_hash, "Honduras", selected_league)
            
            # Mostrar resultados Honduras
            mostrar_tabla_consolidada(tabla_honduras, "Honduras")
            
            # Sección de exportación dentro de la pestaña
            professional_design.create_section_header(
                "Exportar Reporte - Honduras", 
                "Generar archivo Excel con formato profesional",
                "HN"
            )
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                nombre_original_hn = archivo_honduras.name if hasattr(archivo_honduras, 'name') else "HONDURAS.csv"
                nombre_archivo_hn = st.text_input("📝 Nombre del archivo origen", nombre_original_hn, key="nombre_hn")
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
                if st.button("🚀 Generar Excel Honduras", key="excel_hn", use_container_width=True):
                    exportar_excel_consolidado(tabla_honduras, nombre_archivo_hn, "Honduras")
        else:
            # Mensaje de bienvenida cuando no hay archivo
            st.markdown("""
            <div class="country-card country-card-hn">
                <div class="country-flag">🇭🇳</div>
                <h3 class="country-title" style="color: #1e40af; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem;">Honduras - Sistema de Stock</h3>
                <p class="country-description" style="color: #64748b; font-size: 1rem; font-weight: 500; line-height: 1.6; margin-bottom: 0; background: rgba(191, 219, 254, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(191, 219, 254, 0.3);">
                    Selecciona tu archivo HONDURAS.csv para comenzar el análisis completo del inventario<br>
                    <strong style="color: #1e40af;">5 tiendas</strong> en operación
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # PESTAÑA EL SALVADOR
    with tab_el_salvador:
        professional_design.create_section_header(
            "Análisis de Stock - El Salvador", 
            "Gestión de inventario para 9 tiendas en El Salvador",
            "SV"
        )
        
        archivo_el_salvador = data_loader.cargar_archivo("📁 Subir archivo EL_SALVADOR.csv", "El Salvador")
        
        if archivo_el_salvador is not None:
            # Crear hash del DataFrame para cache
            df_hash = archivo_el_salvador.to_dict('records')
            
            # Procesar datos El Salvador (con cache)
            selected_league = st.session_state.get('selected_league', None)
            tabla_el_salvador = data_processor.procesar_datos_consolidados(df_hash, "El Salvador", selected_league)
            
            # Mostrar resultados El Salvador
            mostrar_tabla_consolidada(tabla_el_salvador, "El Salvador")
            
            # Sección de exportación dentro de la pestaña
            professional_design.create_section_header(
                "Exportar Reporte - El Salvador", 
                "Generar archivo Excel con formato profesional",
                "SV"
            )
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                nombre_original_sv = archivo_el_salvador.name if hasattr(archivo_el_salvador, 'name') else "EL_SALVADOR.csv"
                nombre_archivo_sv = st.text_input("📝 Nombre del archivo origen", nombre_original_sv, key="nombre_sv")
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
                if st.button("🚀 Generar Excel El Salvador", key="excel_sv", use_container_width=True):
                    exportar_excel_consolidado(tabla_el_salvador, nombre_archivo_sv, "El Salvador")
        else:
            # Mensaje de bienvenida cuando no hay archivo
            st.markdown("""
            <div class="country-card country-card-sv">
                <div class="country-flag">🇸🇻</div>
                <h3 class="country-title" style="color: #1e3a8a; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem;">El Salvador - Sistema de Stock</h3>
                <p class="country-description" style="color: #64748b; font-size: 1rem; font-weight: 500; line-height: 1.6; margin-bottom: 0; background: rgba(191, 219, 254, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(191, 219, 254, 0.3);">
                    Selecciona tu archivo EL_SALVADOR.csv para comenzar el análisis de las 9 bodegas de El Salvador<br>
                    <strong style="color: #1e3a8a;">9 tiendas</strong> en operación
                </p>
            </div>
            """, unsafe_allow_html=True)

    # PESTAÑA COSTA RICA
    with tab_costa_rica:
        professional_design.create_section_header(
            "Análisis de Stock - Costa Rica", 
            "Gestión de inventario para 2 tiendas en Costa Rica",
            "CR"
        )
        
        archivo_costa_rica = data_loader.cargar_archivo("📁 Subir archivo COSTA_RICA.csv", "Costa Rica")
        
        if archivo_costa_rica is not None:
            # Crear hash del DataFrame para cache
            df_hash = archivo_costa_rica.to_dict('records')
            
            # Procesar datos Costa Rica (con cache)
            selected_league = st.session_state.get('selected_league', None)
            tabla_costa_rica = data_processor.procesar_datos_consolidados(df_hash, "Costa Rica", selected_league)
            
            # Mostrar resultados Costa Rica
            mostrar_tabla_consolidada(tabla_costa_rica, "Costa Rica")
            
            # Sección de exportación dentro de la pestaña
            professional_design.create_section_header(
                "Exportar Reporte - Costa Rica", 
                "Generar archivo Excel con formato profesional",
                "CR"
            )
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                nombre_original_cr = archivo_costa_rica.name if hasattr(archivo_costa_rica, 'name') else "COSTA_RICA.csv"
                nombre_archivo_cr = st.text_input("📝 Nombre del archivo origen", nombre_original_cr, key="nombre_cr")
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
                if st.button("🚀 Generar Excel Costa Rica", key="excel_cr", use_container_width=True):
                    exportar_excel_consolidado(tabla_costa_rica, nombre_archivo_cr, "Costa Rica")
        else:
            # Mensaje de bienvenida cuando no hay archivo
            st.markdown("""
            <div class="country-card country-card-cr">
                <div class="country-flag">🇨🇷</div>
                <h3 class="country-title" style="color: #16a34a; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem;">Costa Rica - Sistema de Stock</h3>
                <p class="country-description" style="color: #64748b; font-size: 1rem; font-weight: 500; line-height: 1.6; margin-bottom: 0; background: rgba(187, 247, 208, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(187, 247, 208, 0.3);">
                    Selecciona tu archivo COSTA_RICA.csv para comenzar el análisis de las 2 bodegas de Costa Rica<br>
                    <strong style="color: #16a34a;">2 tiendas</strong> en operación
                </p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()