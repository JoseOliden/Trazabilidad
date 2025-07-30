import streamlit as st
import json
from fpdf import FPDF
import tempfile
import os

# Clase PDF personalizada
class PDFReporteKayZero(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "INSTITUTO PERUANO DE ENERGÍA NUCLEAR - LABORATORIO AAN", ln=True, align="C")
        self.set_font("Arial", "", 10)
        #self.cell(0, 10, "Reporte de Resultados - Activación Neutrónica (Método k₀)", ln=True, align="C")
        self.cell(0, 10, "Reporte de Resultados - Activacion Neutronica (Metodo k0)", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        #self.cell(0, 10, f'Página {self.page_no()}', align="C")
        self.cell(0, 10, f'Pagina {self.page_no()}', align="C")


    def info_general(self, datos):
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Cliente: {datos['cliente']}", ln=True)
        self.cell(0, 10, f"Lote ID: {datos['lote_id']}", ln=True)
        #self.cell(0, 10, f"Fecha de Recepción: {datos['fecha_recepcion']}", ln=True)
        self.cell(0, 10, f"Fecha de Recepcion: {datos['fecha_recepcion']}", ln=True)
        self.cell(0, 10, f"Analista: {datos['analista']}", ln=True)
        #self.cell(0, 10, f"Método: {datos['metodo']}", ln=True)
        self.cell(0, 10, f"Metodo: {datos['metodo']}", ln=True)
        self.ln(5)

    def datos_muestra(self, muestra):
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, "Datos de la muestra", ln=True)
        self.set_font("Arial", "", 10)
        #self.cell(0, 10, f"Código de Muestra: {muestra['codigo']}", ln=True)
        self.cell(0, 10, f"Codigo de Muestra: {muestra['codigo']}", ln=True)
        self.cell(0, 10, f"Fecha de Irradiación: {muestra['fecha_irradiacion']}", ln=True)
        self.cell(0, 10, f"Fecha de Conteo: {muestra['fecha_conteo']}", ln=True)
        self.cell(0, 10, f"Tiempo de Conteo: {muestra['tiempo_conteo_s']} s", ln=True)
        self.cell(0, 10, f"Detector: {muestra['detector']}", ln=True)
        self.ln(5)

    def tabla_resultados(self, resultados):
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, "Resultados de concentración (ppm)", ln=True)
        self.set_font("Arial", "B", 9)
        self.cell(40, 8, "Elemento", border=1)
        self.cell(40, 8, "Nuclido", border=1)
        self.cell(50, 8, "Concentración (ppm)", border=1)
        self.cell(50, 8, "Incertidumbre (%)", border=1)
        self.ln()

        self.set_font("Arial", "", 9)
        for r in resultados:
            self.cell(40, 8, r["elemento"], border=1)
            self.cell(40, 8, r["nuclido"], border=1)
            self.cell(50, 8, f"{r['concentracion_ppm']:.2f}", border=1)
            self.cell(50, 8, f"{r['incertidumbre_relativa_%']:.2f}", border=1)
            self.ln()

# Interfaz Streamlit
st.set_page_config(page_title="Reporte KayZero AAN", layout="centered")
st.title("☢️ Generador de Reportes AAN - KayZero")

st.markdown("Sube un archivo `.json` generado con resultados de análisis por activación neutrónica.")

uploaded_file = st.file_uploader("Selecciona el archivo JSON", type="json")

if uploaded_file:
    datos = json.load(uploaded_file)

    st.success("✅ Archivo cargado correctamente.")
    st.subheader("Resumen de Datos")
    st.write(f"**Cliente:** {datos['cliente']}")
    st.write(f"**Lote ID:** {datos['lote_id']}")
    st.write(f"**Muestra:** {datos['muestra']['codigo']}")
    st.write(f"**Método:** {datos['metodo']}")

    st.subheader("Resultados")
    st.table(datos["muestra"]["resultados"])

    if st.button("📄 Generar Reporte PDF"):
        pdf = PDFReporteKayZero()
        pdf.add_page()
        pdf.info_general(datos)
        pdf.datos_muestra(datos["muestra"])
        pdf.tabla_resultados(datos["muestra"]["resultados"])

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            st.success("📄 Reporte generado exitosamente.")
            with open(tmp.name, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar Reporte PDF",
                    data=f,
                    file_name="Reporte_KayZero_AAN.pdf",
                    mime="application/pdf"
                )
