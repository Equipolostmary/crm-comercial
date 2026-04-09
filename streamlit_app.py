import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="CRM Comercial", layout="wide")

# --- LOGIN ---
def login():
    st.title("🔐 Acceso CRM")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == "equipolostmary" and password == "Elfamaster26":
            st.session_state["login"] = True
        else:
            st.error("Usuario o contraseña incorrectos")

# --- CARGA DE DATOS ---
def cargar_datos():
    try:
        url = "https://docs.google.com/spreadsheets/d/1EkUx27lMVtO7S88uuyYtzmjxBBiKyVNc1dXY-nUwpVM/gviz/tq?tqx=out:csv&sheet=Ventas%20S%26A"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error("Error cargando datos. Revisa permisos del Google Sheets.")
        st.exception(e)
        return pd.DataFrame()

# --- INFORMES POR ZONA ---
def informes(df):
    st.title("📊 Generador de Informes")

    if df.empty:
        st.warning("No hay datos")
        return

    col_zona = [col for col in df.columns if "zona" in col.lower()]

    if not col_zona:
        st.warning("No se encontró columna de zona")
        return

    col_zona = col_zona[0]
    zonas = df[col_zona].dropna().unique()

    zona = st.selectbox("Selecciona zona", zonas)

    df_zona = df[df[col_zona] == zona]

    if st.button("Generar informe"):
        st.subheader(f"📊 Zona {zona}")

        st.metric("Total puntos de venta", len(df_zona))

        st.bar_chart(df_zona[col_zona].value_counts())

# --- MANAGER ---
def manager(df):
    st.title("🧠 Plataforma Manager")

    if df.empty:
        st.warning("No hay datos")
        return

    menu = st.selectbox("Selecciona sección", [
        "Dashboard",
        "Buscar Punto de Venta"
    ])

    # DASHBOARD
    if menu == "Dashboard":
        st.subheader("📊 Resumen global")

        col_zona = [col for col in df.columns if "zona" in col.lower()][0]

        total_pdv = len(df)
        zonas = df[col_zona].nunique()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total PDV", total_pdv)

        with col2:
            st.metric("Zonas activas", zonas)

        st.subheader("Distribución por zonas")
        st.bar_chart(df[col_zona].value_counts())

    # BUSCADOR
    elif menu == "Buscar Punto de Venta":
        st.subheader("🔎 Buscar estanco")

        busqueda = st.text_input("Introduce número de estanco (VGIFTS)")

        if busqueda:
            resultado = df[df.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)]

            if not resultado.empty:
                fila = resultado.iloc[0]

                st.success(f"Estanco encontrado: {busqueda}")

                # Datos básicos
                col_zona = [c for c in df.columns if "zona" in c.lower()][0]
                col_plan = [c for c in df.columns if "plan" in c.lower()][0]

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Zona", fila[col_zona])

                with col2:
                    st.metric("Plan", fila[col_plan])

                # Ventas
                ventas_cols = [col for col in df.columns if "total" in col.lower()]

                if ventas_cols:
                    ventas = fila[ventas_cols].dropna()

                    st.subheader("📈 Evolución ventas")
                    st.line_chart(ventas)

                    if len(ventas) >= 2:
                        crecimiento = ((ventas.iloc[-1] - ventas.iloc[-2]) / ventas.iloc[-2]) * 100

                        st.subheader("🧠 Informe automático")

                        if crecimiento > 0:
                            st.success(f"Crecimiento del {crecimiento:.2f}% respecto al último mes")
                        else:
                            st.error(f"Caída del {crecimiento:.2f}% respecto al último mes")

                else:
                    st.warning("No se detectaron columnas de ventas")

            else:
                st.error("No se encontró el estanco")

# --- PDV (placeholder) ---
def pdv(df):
    st.title("🏪 Área Punto de Venta")
    st.write("Próximamente...")

# --- APP PRINCIPAL ---
def main():
    if "login" not in st.session_state:
        st.session_state["login"] = False

    if not st.session_state["login"]:
        login()
    else:
        df = cargar_datos()

        st.sidebar.title("Menú")

        seccion = st.sidebar.selectbox("Ir a", [
            "Informes",
            "Manager",
            "Punto de Venta"
        ])

        if seccion == "Informes":
            informes(df)
        elif seccion == "Manager":
            manager(df)
        elif seccion == "Punto de Venta":
            pdv(df)

        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()

if __name__ == "__main__":
    main()
