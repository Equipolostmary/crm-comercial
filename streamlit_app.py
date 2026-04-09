import streamlit as st

# Configuración inicial
st.set_page_config(page_title="CRM Comercial", layout="wide")

# --- LOGIN SIMPLE (placeholder) ---
def login():
    st.title("🔐 Acceso CRM")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        # Aquí luego conectaremos con Google Sheets
        if user == "admin":
            st.session_state["role"] = "manager"
            st.session_state["login"] = True
        else:
            st.session_state["role"] = "pdv"
            st.session_state["login"] = True

# --- GENERADOR DE INFORMES ---
def informes():
    st.title("📊 Generador de Informes")
    zona = st.selectbox("Selecciona zona", ["Este", "Murcia", "Valencia", "Alicante", "Albacete"])

    if st.button("Generar informe"):
        st.subheader(f"Informe zona {zona}")

        # Placeholder datos
        st.metric("Ventas totales", "--")
        st.metric("Crecimiento", "--")

        st.write("Gráficos próximamente...")

# --- PLATAFORMA MANAGER ---
def manager():
    st.title("🧠 Plataforma Manager")

    menu = st.selectbox("Selecciona sección", [
        "Dashboard",
        "Buscar Punto de Venta",
        "Planes de acción"
    ])

    if menu == "Dashboard":
        st.subheader("Resumen global")
        st.write("KPIs y gráficos aquí")

    elif menu == "Buscar Punto de Venta":
        busqueda = st.text_input("Buscar por número de estanco")
        st.write("Resultados aquí")

    elif menu == "Planes de acción":
        st.subheader("Seguimiento PDV")
        st.write("Estados, visitas, acciones...")

# --- PLATAFORMA PDV ---
def pdv():
    st.title("🏪 Área Punto de Venta")

    st.subheader("Mi rendimiento")
    st.metric("Ventas", "--")
    st.metric("Objetivo", "--")
    st.metric("Incentivo", "--")

    st.write("Gráfico de evolución próximamente...")

# --- APP PRINCIPAL ---
def main():
    if "login" not in st.session_state:
        st.session_state["login"] = False

    if not st.session_state["login"]:
        login()
    else:
        st.sidebar.title("Menú")

        seccion = st.sidebar.selectbox("Ir a", [
            "Informes",
            "Manager",
            "Punto de Venta"
        ])

        if seccion == "Informes":
            informes()
        elif seccion == "Manager":
            manager()
        elif seccion == "Punto de Venta":
            pdv()

        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()


if __name__ == "__main__":
    main()
