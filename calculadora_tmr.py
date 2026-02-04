import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import os
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="GLLV Staffing Quote",
    page_icon="💰",
    layout="centered"
)

# Inicialización del session state
if 'editable' not in st.session_state:
    st.session_state.editable = False
if 'coworking' not in st.session_state:
    st.session_state.coworking = 550000
if 'med_prepagada' not in st.session_state:
    st.session_state.med_prepagada = 187300
if 'poliza_vida' not in st.session_state:
    st.session_state.poliza_vida = 18250
if 'porcentaje_comision' not in st.session_state:
    st.session_state.porcentaje_comision = 15.0
if 'aux_transporte' not in st.session_state:
    st.session_state.aux_transporte = 249095

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stMetric:hover {
        background-color: #e6e9ef;
    }
    .highlight {
        background-color: #ffd700;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

logoGllv = "./assets/GLLV Logo.png"

# Función para obtener el TMR del día
def obtener_tmr():
    #try:
        # URL de la API del Banco de la República (Colombia)
     #   url = "https://www.datos.gov.co/resource/32sa-8pi3.json"
     #  response = requests.get(url)
     #   data = response.json()
        
     #   # Obtener el último registro (TMR más reciente)
     #   ultimo_registro = data[0]
     #   fecha = ultimo_registro['vigenciadesde']
     #   valor = float(ultimo_registro['valor'])
        fecha = datetime.now().strftime("%Y-%m-%d")
        valor = 3500.0
        return fecha, valor

   # except Exception as e:
   #     st.error(f"Error al obtener el TRM: {str(e)}")
   #     return None, None

def toggle_editable():
    st.session_state.editable = not st.session_state.editable

def guardar_valores():
    st.session_state.editable = False
    st.success("Valores guardados exitosamente!")

# Título de la aplicación con logo
st.title("GLLV - Staffing Quote 💰")

# Obtener TMR actual
fecha_tmr, valor_tmr = obtener_tmr()

if fecha_tmr and valor_tmr:
    st.info(f"TRM actual ({fecha_tmr}): ${valor_tmr:,.2f} COP/USD")
else:
    st.warning("No se pudo obtener el TRM actual. Por favor, intente más tarde.")

# Sección de Datos de Entrada
st.subheader("Datos de Entrada")
monto_cop = st.number_input("Salario", min_value=0.0, step=100000.0, help="Ingrese el salario en pesos colombianos")

# Expander para valores adicionales
with st.expander("Valores Adicionales", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.coworking = st.number_input(
            "Coworking",
            value=st.session_state.coworking,
            disabled=not st.session_state.editable
        )
        st.session_state.med_prepagada = st.number_input(
            "Med Prepagada",
            value=st.session_state.med_prepagada,
            disabled=not st.session_state.editable
        )
    with col2:
        st.session_state.aux_transporte = st.number_input(
            "Auxilio de transporte",

            value=st.session_state.aux_transporte,
            
            disabled=not st.session_state.editable
        )
        st.session_state.poliza_vida = st.number_input(
            "Poliza de vida",
            value=st.session_state.poliza_vida,
            disabled=not st.session_state.editable
        )
        st.session_state.porcentaje_comision = st.number_input(
            "Porcentaje de Comisión GLLV (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.porcentaje_comision,
            step=0.1,
            disabled=not st.session_state.editable
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Editar valores" if not st.session_state.editable else "Cancelar edición", on_click=toggle_editable):
            pass
    with col2:
        if st.session_state.editable:
            if st.button("Guardar valores", on_click=guardar_valores):
                pass

# Sección de Resultados
st.subheader("Resultados")
if monto_cop > 0 and valor_tmr:
    # Cálculos
    aux_transporte = st.session_state.aux_transporte
    salud = monto_cop * 0.12
    pension = monto_cop * 0.12
    arl = monto_cop * 0.00522
    sena = monto_cop * 0.02
    icbf = monto_cop * 0.03
    caja_compensación = monto_cop * 0.04

    primas = round(monto_cop * 30/360)
    cesantias = round(monto_cop * 30/360)
    int_cesantias = round(monto_cop * 30 * 0.12/360)
    vacaciones = round(monto_cop * 30/720)
    
    # Cálculo del costo total
    costo_total = (
        aux_transporte +
        salud +
        pension +
        arl +
        sena +
        icbf +
        caja_compensación +
        primas +
        cesantias +
        int_cesantias +
        vacaciones
    ) + monto_cop

    costo = (st.session_state.coworking + st.session_state.med_prepagada + st.session_state.poliza_vida + st.session_state.aux_transporte) + costo_total
    gllv_fee = round(costo * (st.session_state.porcentaje_comision/100))
    costo_total_mensual = round(gllv_fee + costo)
    costo_total_mensual_USD = round(costo_total_mensual/valor_tmr)

    # Mostrar resultados principales en un contenedor destacado
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.metric("Costo Total Mensual COP", f"${costo_total_mensual:,.2f}")
    st.metric("Costo Total Mensual USD", f"${costo_total_mensual_USD:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Mostrar desglose detallado
    with st.expander("Ver desglose detallado", expanded=False):
        #mostrar_metricas = st.checkbox("Mostrar todas las métricas", value=False)
        #if mostrar_metricas:
        #    col1, col2 = st.columns(2)
        #    with col1:
        #        st.metric("Auxilio de transporte", f"${aux_transporte:,.2f}")
        #        st.metric("Salud", f"${salud:,.2f}")
        #        st.metric("Pensión", f"${pension:,.2f}")
        #        st.metric("ARL", f"${arl:,.2f}")
        #        st.metric("Sena", f"${sena:,.2f}")
        #        st.metric("ICBF", f"${icbf:,.2f}")
        #    with col2:
        #        st.metric("Caja de Compensación", f"${caja_compensación:,.2f}")
        #        st.metric("Primas", f"${primas:,.2f}")
        #        st.metric("Cesantías", f"${cesantias:,.2f}")
        #        st.metric("Int. Cesantías", f"${int_cesantias:,.2f}")
        #        st.metric("Vacaciones", f"${vacaciones:,.2f}")
        #        st.metric("Costo Total", f"${costo_total:,.2f}")

        # Tabla de desglose con formato mejorado
        st.subheader("Desglose")
        desglose = pd.DataFrame({
            'Concepto': [
                'Salario', 'TRM',
                'Salud', 'Pensión', 'ARL', 'Sena', 'ICBF', 
                'Caja de Compensación', 'Primas', 'Cesantías', 'Int. Cesantías', 
                'Vacaciones', 'Coworking', 'Medicina prepagada', 'Poliza de vida',
                'Gllv Fee', 'Costo Total Mensual', 'Costo Total Mensual USD'
            ],
            'Valor': [
                f"${monto_cop:,.2f}",
                f"${valor_tmr:,.2f}",
                f"${salud:,.2f}",
                f"${pension:,.2f}",
                f"${arl:,.2f}",
                f"${sena:,.2f}",
                f"${icbf:,.2f}",
                f"${caja_compensación:,.2f}",
                f"${primas:,.2f}",
                f"${cesantias:,.2f}",
                f"${int_cesantias:,.2f}",
                f"${vacaciones:,.2f}",
                f"${st.session_state.coworking:,.2f}",
                f"${st.session_state.med_prepagada:,.2f}",
                f"${st.session_state.poliza_vida:,.2f}",
                f"${gllv_fee:,.2f}",
                f"${costo_total_mensual:,.2f}",
                f"${costo_total_mensual_USD:,.2f}"
            ]
        })
        
        # Aplicar estilos a la tabla
        st.dataframe(
            desglose,
            hide_index=True,
            use_container_width=True
        )

        # Botón para exportar a Excel
       # if st.button("Exportar a Excel"):
            # Obtener la ruta de la carpeta de descargas
        #    downloads_path = str(Path.home() / "Downloads")
            # Crear el nombre del archivo con timestamp
        #    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        #    filename = f"desglose_{timestamp}.xlsx"
            # Ruta completa del archivo
        #    file_path = os.path.join(downloads_path, filename)
            
            # Exportar el archivo usando pandas
        #   desglose.to_excel(file_path, index=False, engine='xlsxwriter')
        #    st.success(f"Archivo exportado exitosamente a: {file_path}")

# Pie de página con información adicional
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Desarrollado usando Streamlit</p>
        <p style='font-size: 0.8em; color: #666;'>Última actualización: {}</p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True) 

