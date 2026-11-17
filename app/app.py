"""Dashboard de l'analyse de l'IPO d'Anthropic. Lancement : streamlit run app/app.py"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from donnees import charger_prospectus  # noqa: E402
from gouvernance import repartition, voix_des_cofondateurs  # noqa: E402
from valorisation import actions_diluees, actions_non_diluees, capitalisation  # noqa: E402

BLEU, ORANGE, GRIS = "#38BDF8", "#F59E0B", "#64748B"
TURQUOISE = "#2DD4BF"

st.set_page_config(page_title="IPO d'Anthropic", page_icon="📈", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, .stMetric { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2.2rem; max-width: 1250px; }
    h1 { font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.2rem; }
    .sous-titre { color: #94A3B8; font-size: 0.95rem; margin-bottom: 0.8rem; }
    .badge { display: inline-block; padding: 0.2rem 0.65rem; margin: 0 0.4rem 0.4rem 0;
             border: 1px solid #1E293B; border-radius: 999px; background: #111A2E;
             color: #CBD5E1; font-size: 0.78rem; font-weight: 500; }
    .badge b { color: #2DD4BF; font-weight: 600; }
    div[data-testid="stMetric"] { background: linear-gradient(180deg, #121B2E 0%, #0F172A 100%);
             border: 1px solid #1E293B; border-radius: 14px; padding: 1rem 1.1rem;
             transition: border-color .2s ease, transform .2s ease; }
    div[data-testid="stMetric"]:hover { border-color: #2DD4BF55; transform: translateY(-2px); }
    div[data-testid="stMetricLabel"] p { color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
    div[data-testid="stMetricValue"] { font-weight: 650; font-variant-numeric: tabular-nums; }
    button[data-baseweb="tab"] { font-weight: 500; padding: 0.6rem 1rem; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #2DD4BF; }
    div[data-testid="stAlert"] { border-radius: 12px; }
    hr { border-color: #1E293B; }
    .note { color: #94A3B8; font-size: 0.85rem; line-height: 1.55; }
    </style>
    """,
    unsafe_allow_html=True,
)


def mise_en_forme(fig, hauteur=440):
    """Style commun des graphiques : fond transparent, grille discrète, police Inter."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#CBD5E1", size=13),
        height=hauteur,
        margin=dict(t=30, r=20, b=40, l=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#0F172A", bordercolor="#334155", font_family="Inter"),
        transition=dict(duration=300, easing="cubic-in-out"),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.08)", zeroline=False, linecolor="#1E293B")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.08)", zeroline=False, linecolor="#1E293B")
    return fig


st.title("Analyse de l'IPO d'Anthropic")
st.markdown(
    '<div class="sous-titre">Combien vaut Anthropic, qui décide, et quelles actions pourront arriver sur le marché.</div>'
    '<span class="badge">Nasdaq <b>ANT</b></span>'
    '<span class="badge">Fourchette <b>70 à 78 $</b></span>'
    '<span class="badge">825 M d\'actions offertes</span>'
    '<span class="badge">Source <b>S-1/A n°2</b> du 10/11/2026</span>',
    unsafe_allow_html=True,
)
st.caption("Projet pédagogique, pas un conseil en investissement.")

donnees = charger_prospectus(RACINE / "data" / "prospectus.csv")
onglet_valo, onglet_pouvoir, onglet_ventes = st.tabs(
    ["Valorisation selon le prix", "Qui décide ?", "Ventes futures"]
)

# ---------------------------------------------------------------- Valorisation
with onglet_valo:
    prix = st.slider("Prix de l'IPO (dollars par action)", 60.0, 100.0, 74.0, 0.5)
    nb_nd, nb_d = actions_non_diluees(prix, donnees), actions_diluees(prix, donnees)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Capitalisation, base non diluée", f"{capitalisation(prix, nb_nd) / 1e9:,.0f} Md$")
    c2.metric("Capitalisation, base diluée", f"{capitalisation(prix, nb_d) / 1e9:,.0f} Md$")
    c3.metric("Actions, base non diluée", f"{nb_nd / 1e9:.2f} Md")
    c4.metric("Actions, base diluée", f"{nb_d / 1e9:.2f} Md")

    grille = np.arange(60, 100.5, 0.5)
    courbe = pd.DataFrame(
        {
            "prix": grille,
            "non_diluee": [capitalisation(p, actions_non_diluees(p, donnees)) / 1e9 for p in grille],
            "diluee": [capitalisation(p, actions_diluees(p, donnees)) / 1e9 for p in grille],
        }
    )
    fig = go.Figure()
    fig.add_vrect(x0=70, x1=78, fillcolor=TURQUOISE, opacity=0.06, line_width=0,
                  annotation_text="fourchette du prospectus", annotation_position="top left")
    fig.add_trace(go.Scatter(x=courbe["prix"], y=courbe["non_diluee"], name="Base non diluée",
                             line=dict(color=BLEU, width=2.5, shape="spline"),
                             hovertemplate="%{y:,.0f} Md$<extra>non diluée</extra>"))
    fig.add_trace(go.Scatter(x=courbe["prix"], y=courbe["diluee"], name="Base diluée",
                             line=dict(color=ORANGE, width=2.5, shape="spline"),
                             fill="tonexty", fillcolor="rgba(245,158,11,0.08)",
                             hovertemplate="%{y:,.0f} Md$<extra>diluée</extra>"))
    fig.add_vline(x=prix, line_dash="dot", line_color=TURQUOISE, line_width=1.5)
    fig.update_layout(xaxis_title="Prix de l'IPO ($)", yaxis_title="Capitalisation (milliards de $)", hovermode="x unified")
    mise_en_forme(fig, 450)
    st.plotly_chart(fig, width="stretch")
    st.markdown(
        "<p class='note'>La base diluée ajoute environ 4,9 milliards d'actions (stock-options après méthode du rachat d'actions, "
        "RSU, dette convertible, plans liés aux dons des salariés). Chaque dollar de prix ajoute environ "
        "18 milliards de dollars de capitalisation diluée.</p>", unsafe_allow_html=True
    )

# ---------------------------------------------------------------- Qui décide ?
with onglet_pouvoir:
    tableau = repartition()
    v_cofond = voix_des_cofondateurs(tableau)
    k1, k2, k3 = st.columns(3)
    k1.metric("Droits de vote des 7 cofondateurs", f"{v_cofond:.0%}", "action F + leurs actions A", delta_color="off")
    capital_cofond = tableau.loc[tableau["groupe"] == "7 cofondateurs", "part_capital"].sum()
    k2.metric("Capital détenu par les 7 cofondateurs", f"{capital_cofond:.0%}")
    part_public = tableau.loc[tableau["groupe"] == "Public (actions de l'IPO)"].iloc[0]
    k3.metric("Le public (actions de l'IPO)", f"{part_public['part_capital']:.1%} du capital",
              f"{part_public['part_voix']:.1%} des voix", delta_color="off")

    ordre = tableau.sort_values("part_capital")
    fig2 = go.Figure()
    for colonne, nom, couleur in [("part_capital", "Part du capital", BLEU), ("part_voix", "Part des droits de vote", ORANGE)]:
        fig2.add_trace(go.Bar(y=ordre["groupe"], x=ordre[colonne] * 100, name=nom, orientation="h",
                              marker=dict(color=couleur, line=dict(width=0)),
                              text=[f"{v:.1f} %" if v > 0.001 else "" for v in ordre[colonne]],
                              textposition="outside", cliponaxis=False,
                              hovertemplate="%{y}<br>" + nom + " : %{x:.1f} %<extra></extra>"))
    fig2.update_layout(barmode="group", bargap=0.35, bargroupgap=0.08, xaxis_title="%")
    mise_en_forme(fig2, 540)
    st.plotly_chart(fig2, width="stretch")

    st.subheader("Les trois leviers du pouvoir")
    l1, l2, l3 = st.columns(3)
    l1.info("**Action T (1 action)**\n\nDétenue par le Long-Term Benefit Trust (5 trustees). "
            "Élit la **majorité du conseil d'administration**. Aucun droit économique.")
    l2.warning("**Action F (1 action)**\n\nDétenue par la Founder LLC (7 cofondateurs). "
               "**50,1 % des droits de vote**, sans baisse en cas d'émission d'actions. Aucun droit économique.")
    l3.success("**Actions A**\n\n1 voix par action, se partagent 49,9 % des voix. "
               "Le public n'en détient qu'environ 11 %, soit environ 5,5 % des voix.")
    st.markdown(
        "<p class='note'>Les actions N (Amazon, Google, partenaires du placement privé, fonds d'intérêt général) "
        "représentent environ 43 % du capital **sans aucun droit de vote**. "
        "Le pouvoir est attaché à deux actions sans valeur économique.</p>", unsafe_allow_html=True
    )
    with st.expander("Voir le tableau détaillé"):
        affichage = tableau[["groupe", "part_capital", "part_voix"]].copy()
        affichage["part_capital"] = (affichage["part_capital"] * 100).round(1)
        affichage["part_voix"] = (affichage["part_voix"] * 100).round(1)
        st.dataframe(affichage.rename(columns={"groupe": "Groupe", "part_capital": "Capital (%)", "part_voix": "Voix (%)"}),
                     hide_index=True, width="stretch")

# ---------------------------------------------------------------- Ventes futures
with onglet_ventes:
    calendrier = pd.read_csv(RACINE / "data" / "calendrier_deblocage.csv", parse_dates=["date_estimee"])
    lockup = calendrier[~calendrier["evenement"].str.startswith("Placement privé")].sort_values("date_estimee")
    lockup["cumul_milliards"] = lockup["actions_millions"].cumsum() / 1000
    m1, m2, m3 = st.columns(3)
    m1.metric("Actions mises en vente lors de l'IPO", "0,83 Md")
    m2.metric("Actions débloquées progressivement", f"{lockup['actions_millions'].sum() / 1000:.1f} Md")
    m3.metric("Débloquées dès le premier jour", "0,32 Md", "38 % des actions de l'IPO", delta_color="off")

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=lockup["date_estimee"], y=lockup["cumul_milliards"], line_shape="hv",
                              name="Actions A débloquées (cumul)", line=dict(color=ORANGE, width=2.5),
                              fill="tozeroy", fillcolor="rgba(245,158,11,0.10)",
                              customdata=lockup[["evenement", "actions_millions"]],
                              hovertemplate="%{customdata[0]}<br>+%{customdata[1]} millions<br>cumul %{y:.1f} Md<extra></extra>"))
    fig3.add_hline(y=0.825, line_dash="dot", line_color=BLEU, annotation_text="actions vendues lors de l'IPO",
                   annotation_font_color=BLEU)
    fig3.add_vrect(x0="2027-05-01", x1="2027-05-20", fillcolor=TURQUOISE, opacity=0.12, line_width=0,
                   annotation_text="mai 2027 : fin du lock-up de 180 jours et ventes possibles pour Google",
                   annotation_position="top left")
    fig3.update_layout(yaxis_title="Milliards d'actions")
    mise_en_forme(fig3, 480)
    st.plotly_chart(fig3, width="stretch")
    st.caption("Dates estimées à partir des règles du prospectus (certaines dépendent des dates de publication des résultats).")
    st.info("La simulation de l'impact d'une vente sur le cours sera ajoutée après la cotation, "
            "à partir du volume et de la volatilité réels de l'action ANT.")
