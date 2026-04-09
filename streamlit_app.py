import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="CRM Comercial", layout="wide")

# --- LOGIN REAL ---
def login():
    st.title("🔐 Acceso CRM")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == "equipolostmary" and password == "Elfamaster26":
            st.session_state["role"] = "manager"
            st.session_state["login"] = True
        else:
            st.error("Usuario o contraseña incorrectos")

# --- CARGA DE DATOS (TEMPORAL SIN API) ---
def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/1EkUx27lMVtO7S88uuyYtzmjxBBiKyVNc1dXY-nUwpVM/gviz/tq?tqx=out:csv&sheet=Ventas S&A"
    df = pd.read_csv(url)
    return df

# --- GENERADOR DE INFORMES ---
def informes(df):
    st.title("📊 Generador de Informes")

    if "Zona" in df.columns:
        zonas = df["Zona"].dropna().unique()
        zona = st.selectbox("Selecciona zona", zonas)

        df_zona = df[df["Zona"] == zona]

        if st.button("Generar informe"):
            st.subheader(f"Informe zona {zona}")

            st.metric("Total registros", len(df_zona))

            st.dataframe(df_zona)
    else:
        st.warning("No existe columna 'Zona' en los datos")

# --- PLATAFORMA MANAGER ---
def manager(df):
    st.title("🧠 Plataforma Manager")

    menu = st.selectbox("Selecciona sección", [
        "Dashboard",
        "Buscar Punto de Venta",
        "Planes de acción"
    ])

    if menu == "Dashboard":
        st.subheader("Resumen global")
        st.metric("Total registros", len(df))
        st.dataframe(df.head())

    elif menu == "Buscar Punto de Venta":
        busqueda = st.text_input("Buscar por número de estanco")

        if busqueda:
            resultado = df[df.astype(str).apply(lambda row: row.str.contains(busqueda).any(), axis=1)]
            st.dataframe(resultado)

    elif menu == "Planes de acción":
        st.subheader("Seguimiento PDV")
        st.write("Aquí añadiremos estados y acciones")

# --- PLATAFORMA PDV ---
def pdv(df):
    st.title("🏪 Área Punto de Venta")
    st.write("Vista individual próximamente")

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
