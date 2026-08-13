import streamlit as st

st.title("Mi primera app de Streamlit")

st.write("¡Hola! 👋")
st.write("Esta es mi primera aplicación creada con Streamlit.")

st.header("Mis primeros datos")

datos = {
    "Nombre": ["Ana", "Carlos", "Laura"],
    "Edad": [22, 25, 21],
    "Ciudad": ["Medellín", "Bogotá", "Cali"]
}

st.table(datos)

st.success("¡Gracias por visitar mi primera app! 🚀")
