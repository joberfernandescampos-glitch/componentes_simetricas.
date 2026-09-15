import cmath
import math
import matplotlib.pyplot as plt
import streamlit as st

# Configuração da página Web
st.set_page_config(page_title="Componentes Simétricas", layout="centered")
st.title("⚡ JÓBER FERNANDES - COMPONENTES SIMÉTRICAS")

# --- ENTRADAS NA BARRA LATERAL ---
st.sidebar.header("📋 Parâmetros de Entrada")


def entrada_fasor(fase, def_mod, def_ang):
    st.sidebar.subheader(f"Corrente I{fase}")
    mod = st.sidebar.number_input(
        f"Módulo I{fase} (A):", min_value=0.0, value=float(def_mod), step=1.0
    )
    ang = st.sidebar.number_input(
        f"Ângulo I{fase} (°):",
        min_value=-360.0,
        max_value=360.0,
        value=float(def_ang),
        step=5.0,
    )
    return mod, ang


mod_a, ang_a = entrada_fasor("a", 210, 0)
mod_b, ang_b = entrada_fasor("b", 52, 240)
mod_c, ang_c = entrada_fasor("c", 65, 120)


def ajustar_angulo(ang):
    while ang > 180:
        ang -= 360
    while ang <= -180:
        ang += 360
    return ang


# --- PROCESSAMENTO MATEMÁTICO ---
Ia = cmath.rect(mod_a, math.radians(ang_a))
Ib = cmath.rect(mod_b, math.radians(ang_b))
Ic = cmath.rect(mod_c, math.radians(ang_c))

# 1. Corrente de Neutro
In = Ia + Ib + Ic
mod_In, ang_In = cmath.polar(In)

# Operadores de Deslocamento
a = cmath.rect(1, math.radians(120))
a2 = cmath.rect(1, math.radians(240))

# 2. Componentes de Sequência
I0 = In / 3
mod_I0, ang_I0 = cmath.polar(I0)

I1 = (Ia + (a * Ib) + (a2 * Ic)) / 3
mod_I1, ang_I1 = cmath.polar(I1)

I2 = (Ia + (a2 * Ib) + (a * Ic)) / 3
mod_I2, ang_I2 = cmath.polar(I2)

# --- EXIBIÇÃO DOS RESULTADOS ---
st.subheader("📊 Resultados Computados")

resultado_texto = (
    "--- Correntes de Fase (Entrada) ---\n"
    f"Ia = {mod_a:.4f} |_ {ajustar_angulo(ang_a):.2f}° A\n"
    f"Ib = {mod_b:.4f} |_ {ajustar_angulo(ang_b):.2f}° A\n"
    f"Ic = {mod_c:.4f} |_ {ajustar_angulo(ang_c):.2f}° A\n\n"
    "--- Componentes de Sequência ---\n"
    f"I0 = {mod_I0:.4f} |_ {ajustar_angulo(math.degrees(ang_I0)):.2f}° A\n"
    f"I1 = {mod_I1:.4f} |_ {ajustar_angulo(math.degrees(ang_I1)):.2f}° A\n"
    f"I2 = {mod_I2:.4f} |_ {ajustar_angulo(math.degrees(ang_I2)):.2f}° A\n\n"
    "--- Corrente de Neutro ---\n"
    f"In = {mod_In:.4f} |_ {ajustar_angulo(math.degrees(ang_In)):.2f}° A\n"
)

# Bloco estilo console negro original
st.text_area(
    label="Console de Saída:",
    value=resultado_texto,
    height=280,
    disabled=True,
)

# --- PLOTAGEM DOS DOIS GRÁFICOS FASORIAIS ---
st.subheader("📈 Diagramas Fasoriais")

# Criando duas colunas no Streamlit para os gráficos ficarem lado a lado na Web
col1, col2 = st.columns(2)


def plotar_fasor(ax, complexo, label, cor):
    ax.quiver(
        0,
        0,
        complexo.real,
        complexo.imag,
        angles="xy",
        scale_units="xy",
        scale=1,
        color=cor,
        label=label,
        width=0.015,
    )


# Encontrando um limite de escala comum para os dois gráficos ficarem proporcionais
maior_modulo = max(mod_a, mod_b, mod_c, mod_In, mod_I0, mod_I1, mod_I2, 1)
limite_grafico = maior_modulo * 1.2

# --- GRÁFICO 1: CORRENTES DE FASE (Coluna 1) ---
with col1:
    st.write("**Correntes de Fase e Neutro**")
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    plotar_fasor(ax1, Ia, "Ia", "blue")
    plotar_fasor(ax1, Ib, "Ib", "green")
    plotar_fasor(ax1, Ic, "Ic", "orange")
    plotar_fasor(ax1, In, "In", "red")

    ax1.set_xlim(-limite_grafico, limite_grafico)
    ax1.set_ylim(-limite_grafico, limite_grafico)
    ax1.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax1.axvline(0, color="black", linewidth=0.5, linestyle="--")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)
    ax1.set_aspect("equal")
    ax1.legend(loc="upper right")
    st.pyplot(fig1)

# --- GRÁFICO 2: COMPONENTES DE SEQUÊNCIA (Coluna 2) ---
with col2:
    st.write("**Componentes de Sequência**")
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    plotar_fasor(ax2, I0, "I0 (Zero)", "purple")
    plotar_fasor(ax2, I1, "I1 (Pos)", "brown")
    plotar_fasor(ax2, I2, "I2 (Neg)", "magenta")

    ax2.set_xlim(-limite_grafico, limite_grafico)
    ax2.set_ylim(-limite_grafico, limite_grafico)
    ax2.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax2.axvline(0, color="black", linewidth=0.5, linestyle="--")
    ax2.grid(True, which="both", linestyle=":", alpha=0.5)
    ax2.set_aspect("equal")
    ax2.legend(loc="upper right")
    st.pyplot(fig2)
