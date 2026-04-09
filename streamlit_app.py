import streamlit as st
import pandas as pd

st.set_page_config(page_title="CRM Comercial", layout="wide")

# LOGIN
def login():
    st.title("🔐 Acceso CRM")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == "equipolostmary" and password == "Elfamaster26":
            st.session_state["login"] = True
        else:
            st.error("Usuario o contraseña incorrectos")

# CARGA DATOS
def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/1EkUx27lMVtO7S88uuyYtzmjxBBiKyVNc1dXY-nUwpVM/gviz/tq?tqx=out:csv&sheet=Ventas%20S%26A"
    df = pd.read_csv(url)

    # 🔥 LIMPIEZA TOTAL
    df.columns = df.columns.astype(str).str.strip().str.upper()

    return df

# INFORMES
def informes(df):
    st.title("📊 Generador de Informes")

    if "REGION" not in df.columns:
        st.error("❌ No se encuentra la columna REGION")
        st.write("Columnas detectadas:", df.columns)
        return

    zonas = df["REGION"].dropna().unique()
    zona = st.selectbox("Selecciona zona", zonas)

    df_zona = df[df["REGION"] == zona]

    if st.button("Generar informe"):
        st.metric("Total PDV", len(df_zona))
        st.bar_chart(df_zona["REGION"].value_counts())

# MANAGER
def manager(df):
    st.title("🧠 Plataforma Manager")

    if "REGION" not in df.columns:
        st.error("❌ No se encuentra la columna REGION")
        st.write("Columnas detectadas:", df.columns)
        return

    menu = st.selectbox("Sección", ["Dashboard", "Buscar PDV"])

    # DASHBOARD
    if menu == "Dashboard":
        st.subheader("Resumen global")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total PDV", len(df))

        with col2:
            st.metric("Zonas", df["REGION"].nunique())

        st.subheader("Distribución por zonas")
        st.bar_chart(df["REGION"].value_counts())

    # BUSCADOR
    elif menu == "Buscar PDV":
        st.subheader("🔎 Buscar estanco")

        busqueda = st.text_input("Introduce VGIFTS")

        if busqueda:
            resultado = df[df.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)]

            if not resultado.empty:
                fila = resultado.iloc[0]

                st.success("Estanco encontrado")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Región", fila["REGION"])

                # PLAN
                plan_cols = [col for col in df.columns if "PLAN" in col]
                if plan_cols:
                    with col2:
                        st.metric("Plan", fila[plan_cols[0]])

                # VENTAS
                ventas_cols = [col for col in df.columns if "TOTAL" in col]

                if ventas_cols:
                    ventas = fila[ventas_cols].dropna()

                    st.subheader("📈 Evolución ventas")
                    st.line_chart(ventas)

                    if len(ventas) >= 2:
                        crecimiento = ((ventas.iloc[-1] - ventas.iloc[-2]) / ventas.iloc[-2]) * 100

                        st.subheader("🧠 Informe automático")

                        if crecimiento > 0:
                            st.success(f"📈 Crecimiento {crecimiento:.2f}%")
                        else:
                            st.error(f"📉 Caída {crecimiento:.2f}%")

                else:
                    st.warning("No se detectaron columnas de ventas (deben contener 'TOTAL')")

            else:
                st.error("No se encontró el estanco")

# PDV
def pdv(df):
    st.title("🏪 Área Punto de Venta")
    st.write("Próximamente")

# MAIN
def main():
    if "login" not in st.session_state:
        st.session_state["login"] = False

    if not st.session_state["login"]:
        login()
    else:
        df = cargar_datos()

        st.sidebar.title("Menú")
        seccion = st.sidebar.selectbox("Ir a", ["Informes", "Manager", "PDV"])

        if seccion == "Informes":
            informes(df)
        elif seccion == "Manager":
            manager(df)
        elif seccion == "PDV":
            pdv(df)

        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()

if __name__ == "__main__":
    main()
