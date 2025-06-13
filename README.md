# GLLV Staffing Quote 💰

## Descripción
GLLV Staffing Quote es una aplicación web desarrollada con Streamlit que permite calcular y generar cotizaciones detalladas para servicios de staffing, incluyendo todos los costos asociados y la conversión a USD utilizando la TRM (Tasa Representativa del Mercado) actual.

## Características Principales
- 🎯 Cálculo automático de costos de nómina
- 💱 Conversión automática a USD usando la TRM actual
- 📊 Desglose detallado de todos los costos
- 💾 Exportación de resultados a Excel
- 🔄 Valores personalizables para coworking, medicina prepagada y póliza de vida
- 📱 Interfaz intuitiva y responsive

## Requisitos del Sistema
- Python 3.8 o superior
- Conexión a internet (para obtener la TRM actual)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Iniciar la aplicación:
```bash
streamlit run calculadora_tmr.py
```

2. La aplicación se abrirá en tu navegador predeterminado.

3. Para generar una cotización:
   - Ingresa el salario en pesos colombianos
   - Ajusta los valores adicionales si es necesario (coworking, medicina prepagada, póliza de vida)
   - Revisa el desglose detallado
   - Exporta los resultados a Excel si lo deseas

## Componentes de la Cotización

### Costos Fijos
- Coworking
- Medicina Prepagada
- Póliza de Vida

### Costos de Nómina
- Salud (12%)
- Pensión (12%)
- ARL (0.522%)
- SENA (2%)
- ICBF (3%)
- Caja de Compensación (4%)
- Prima de Servicios
- Cesantías
- Intereses de Cesantías
- Vacaciones

### Comisiones
- Comisión GLLV (configurable)

## Exportación de Datos
- Los archivos Excel se guardan automáticamente en la carpeta de descargas
- El nombre del archivo incluye timestamp para evitar sobrescrituras
- Incluye desglose completo de todos los costos

## Personalización
Los siguientes valores pueden ser personalizados:
- Porcentaje de comisión GLLV
- Costo de coworking
- Costo de medicina prepagada
- Costo de póliza de vida

## Soporte
Para reportar problemas o sugerir mejoras, por favor crear un issue en el repositorio.

## Licencia
[Especificar tipo de licencia]

## Desarrollado por
GLLV 