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
from finances import (bfr_exploitation, charger_bilan, charger_etats, charger_trimestres,  # noqa: E402
                      chiffre_affaires_annuel, diagnostic)
from comparaison import parcours_depuis_ipo, tableau_comparatif  # noqa: E402

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
    '<span class="badge">Prix final <b>83 $</b> (fourchette 70 à 78 $)</span>'
    '<span class="badge">980 M d\'actions offertes</span>'
    '<span class="badge">1er jour <b>+17,1 %</b></span>'
    '<span class="badge">Sources <b>S-1/A n°2</b> et <b>424B4</b></span>',
    unsafe_allow_html=True,
)
st.caption("Projet pédagogique, pas un conseil en investissement.")

donnees = charger_prospectus(RACINE / "data" / "prospectus.csv")
definitif = charger_prospectus(RACINE / "data" / "ipo_definitive.csv")
comparatif = tableau_comparatif()
onglet_valo, onglet_jour, onglet_fi, onglet_pouvoir, onglet_ventes, onglet_spcx = st.tabs(
    ["Valorisation selon le prix", "Prix final et premier jour", "Diagnostic financier",
     "Qui décide ?", "Ventes futures", "Comparaison avec SpaceX"]
)

# ---------------------------------------------------------------- Valorisation
with onglet_valo:
    prix = st.slider("Prix de l'IPO (dollars par action)", 60.0, 100.0, 83.0, 0.5)
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
    fig.add_trace(go.Scatter(
        x=[83, 83], y=[comparatif.loc["capitalisation_base_ipo", "ANT"] / 1e9, comparatif.loc["capitalisation_diluee_ipo", "ANT"] / 1e9],
        mode="markers", name="Réel (424B4, 83 $)", marker=dict(color="#F8FAFC", size=10, symbol="diamond"),
        hovertemplate="%{y:,.0f} Md$<extra>424B4</extra>"))
    fig.update_layout(xaxis_title="Prix de l'IPO ($)", yaxis_title="Capitalisation (milliards de $)", hovermode="x unified")
    mise_en_forme(fig, 450)
    st.plotly_chart(fig, width="stretch")
    st.markdown(
        "<p class='note'>La base diluée ajoute environ 4,9 milliards d'actions (stock-options après méthode du rachat d'actions, "
        "RSU, dette convertible, plans liés aux dons des salariés). Chaque dollar de prix ajoute environ "
        "18 milliards de dollars de capitalisation diluée. Les courbes viennent du modèle construit sur le S-1/A ; "
        "les losanges blancs sont les chiffres réels du prospectus définitif, un peu au-dessus car l'offre a été augmentée de 155 millions d'actions.</p>", unsafe_allow_html=True
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
    m1.metric("Actions mises en vente lors de l'IPO", "0,98 Md", "424B4", delta_color="off")
    m2.metric("Actions débloquées progressivement", f"{lockup['actions_millions'].sum() / 1000:.1f} Md")
    m3.metric("Débloquées dès le premier jour", "0,32 Md", "environ 33 % des actions de l'IPO", delta_color="off")

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=lockup["date_estimee"], y=lockup["cumul_milliards"], line_shape="hv",
                              name="Actions A débloquées (cumul)", line=dict(color=ORANGE, width=2.5),
                              fill="tozeroy", fillcolor="rgba(245,158,11,0.10)",
                              customdata=lockup[["evenement", "actions_millions"]],
                              hovertemplate="%{customdata[0]}<br>+%{customdata[1]} millions<br>cumul %{y:.1f} Md<extra></extra>"))
    fig3.add_hline(y=0.98, line_dash="dot", line_color=BLEU, annotation_text="actions vendues lors de l'IPO",
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

# ---------------------------------------------------------------- Prix final et premier jour
with onglet_jour:
    a = comparatif["ANT"]
    j1, j2, j3, j4 = st.columns(4)
    j1.metric("Prix d'IPO", "83 $", "+5 $ au-dessus de la fourchette", delta_color="off")
    j2.metric("Clôture du 1er jour", "97,17 $", f"{a['rendement_cloture_j1']:+.1%}")
    j3.metric("Argent laissé sur la table", f"{a['argent_laisse_sur_la_table'] / 1e9:.1f} Md$")
    j4.metric("Capitalisation diluée à la clôture", f"{a['capitalisation_diluee_cloture_j1'] / 1e12:.2f} T$")

    cours = pd.read_csv(RACINE / "data" / "cours_ANT.csv", index_col=0, parse_dates=True).iloc[0]
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=["Prix d'IPO", "Ouverture", "Plus haut", "Plus bas", "Clôture"],
                          y=[83, cours["Open"], cours["High"], cours["Low"], cours["Close"]],
                          marker_color=[GRIS, BLEU, TURQUOISE, ORANGE, BLEU],
                          text=[f"{v:.2f} $<br>{v / 83 - 1:+.1%}" for v in [83, cours["Open"], cours["High"], cours["Low"], cours["Close"]]],
                          textposition="outside", cliponaxis=False, hovertemplate="%{x} : %{y:.2f} $<extra></extra>"))
    fig4.add_hline(y=83, line_dash="dot", line_color=GRIS)
    fig4.update_layout(yaxis_title="$ par action", yaxis_range=[0, 130], showlegend=False)
    mise_en_forme(fig4, 420)
    st.plotly_chart(fig4, width="stretch")

    st.subheader("Du S-1/A n°2 au prospectus définitif")
    ecarts = pd.DataFrame({
        "Élément": ["Prix", "Actions A émises par la société", "Total offert", "Actions N du placement privé (26 Md$)",
                    "Base non diluée", "Base diluée"],
        "S-1/A n°2": ["70 à 78 $", "801 351 354", "825 000 000", "351 351 350 (à 74 $)", "13 086 672 593 (à 74 $)", "18 012 993 379 (à 74 $)"],
        "424B4": ["83 $", "956 351 354", "980 000 000", f"{definitif['placement_prive_N_actions']:,.0f}".replace(",", " "),
                  f"{definitif['actions_total_apres_ipo']:,.0f}".replace(",", " "), "18 137 587 875"],
    })
    st.dataframe(ecarts, hide_index=True, width="stretch")
    st.markdown(
        "<p class='note'>La demande a permis à la fois de relever le prix au-dessus de la fourchette et d'augmenter l'offre de 19 %. "
        "Le placement privé étant un montant fixe en dollars, un prix plus élevé réduit le nombre d'actions N émises. "
        "Détail dans docs/04_ipo_definitive_et_premier_jour.md.</p>", unsafe_allow_html=True)

# ---------------------------------------------------------------- Diagnostic financier
with onglet_fi:
    diag = diagnostic(charger_etats())
    tri = charger_trimestres()
    annuel = chiffre_affaires_annuel(tri)
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("CA des 12 derniers mois", f"{annuel['quatre_derniers_trimestres'] / 1000:.1f} Md$")
    f2.metric("Croissance du T3 2026 sur un an", f"x {1 + annuel['croissance_sur_un_an_dernier_trimestre']:.1f}")
    f3.metric("Marge après calcul (9M2026)", f"{diag.loc['9M2026', 'marge_apres_calcul']:.0%}")
    f4.metric("Flux disponible (9M2026)", f"{diag.loc['9M2026', 'flux_disponible'] / 1000:+.1f} Md$")

    trimestres = tri.columns
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=list(trimestres), y=tri.loc["chiffre_affaires", trimestres] / 1000, name="Chiffre d'affaires",
                          marker_color=BLEU, hovertemplate="%{y:.1f} Md$<extra>CA</extra>"))
    fig5.add_trace(go.Bar(x=list(trimestres), y=tri.loc["calcul_et_infrastructure", trimestres] / 1000, name="Coût du calcul",
                          marker_color=ORANGE, hovertemplate="%{y:.1f} Md$<extra>calcul</extra>"))
    fig5.update_layout(barmode="group", yaxis_title="Milliards de $", bargap=0.3)
    mise_en_forme(fig5, 400)
    st.plotly_chart(fig5, width="stretch")

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**Du résultat net au flux de trésorerie (9M2026, Md$)**")
        e = charger_etats()["9M2026"]
        fig6 = go.Figure(go.Waterfall(
            x=["Résultat net", "Juste valeur et autres", "Rémunération en actions", "Dotations", "CAF",
               "Variation de BFR", "Flux d'exploitation", "Investissements", "Flux disponible"],
            measure=["absolute", "relative", "relative", "relative", "total", "relative", "total", "relative", "total"],
            y=[e["resultat_net"] / 1000, e["elements_non_monetaires_hors_dotations_et_actions"] / 1000,
               e["remuneration_en_actions"] / 1000, e["dotations_amortissements"] / 1000, 0,
               e["variation_bfr"] / 1000, 0, -diag.loc["9M2026", "investissements"] / 1000, 0],
            increasing=dict(marker_color=TURQUOISE), decreasing=dict(marker_color=ORANGE),
            totals=dict(marker_color=BLEU), connector=dict(line=dict(color="#334155")),
            hovertemplate="%{x} : %{y:.1f} Md$<extra></extra>"))
        mise_en_forme(fig6, 420)
        fig6.update_layout(showlegend=False)
        st.plotly_chart(fig6, width="stretch")
    with g2:
        st.markdown("**Indicateurs du cours d'analyse financière**")
        table = pd.DataFrame({
            "Indicateur": ["Marge d'exploitation", "Marge d'exploitation ajustée", "Calcul / CA", "CAF (M$)",
                           "Investissements / dotations", "BFR d'exploitation au 30/09 (M$)", "Engagements de calcul (Md$)"],
            "2025": [f"{diag.loc['2025', 'marge_exploitation']:.0%}", f"{diag.loc['2025', 'marge_exploitation_ajustee']:.0%}",
                     f"{diag.loc['2025', 'poids_calcul_dans_ca']:.0%}", f"{diag.loc['2025', 'caf']:,.0f}",
                     f"{diag.loc['2025', 'investissements_sur_dotations']:.1f}", "", ""],
            "9M2026": [f"{diag.loc['9M2026', 'marge_exploitation']:.1%}", f"{diag.loc['9M2026', 'marge_exploitation_ajustee']:.1%}",
                       f"{diag.loc['9M2026', 'poids_calcul_dans_ca']:.0%}", f"{diag.loc['9M2026', 'caf']:,.0f}",
                       f"{diag.loc['9M2026', 'investissements_sur_dotations']:.1f}",
                       f"{bfr_exploitation(charger_bilan()):,.0f}", "900,9"],
        })
        st.dataframe(table, hide_index=True, width="stretch")
        st.markdown(
            "<p class='note'>La perte nette de 104 Md$ vient à 91 % de la variation de juste valeur de la dette convertible : "
            "plus Anthropic vaut cher, plus la valeur des actions promises aux prêteurs monte, et cette hausse est une charge comptable "
            "sans sortie d'argent. L'activité, elle, dégage une CAF positive.</p>", unsafe_allow_html=True)

# ---------------------------------------------------------------- Comparaison avec SpaceX
with onglet_spcx:
    s = comparatif["SPCX"]
    a = comparatif["ANT"]
    st.markdown("<p class='note'>SpaceX (SPCX) est entrée au Nasdaq le 12/06/2026 à 135 $. "
                "Chiffres du prospectus définitif de chaque société.</p>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Capitalisation diluée à l'IPO", f"{a['capitalisation_diluee_ipo'] / 1e9:,.0f} Md$",
              f"SpaceX : {s['capitalisation_diluee_ipo'] / 1e9:,.0f} Md$", delta_color="off")
    s2.metric("Capitalisation / CA 12 mois", f"{a['capitalisation_diluee_sur_ca']:.0f} x",
              f"SpaceX : {s['capitalisation_diluee_sur_ca']:.0f} x", delta_color="off")
    s3.metric("Rendement 1er jour (clôture)", f"{a['rendement_cloture_j1']:+.1%}",
              f"SpaceX : {s['rendement_cloture_j1']:+.1%}", delta_color="off")
    s4.metric("Flottant", f"{a['flottant']:.1%}", f"SpaceX : {s['flottant']:.1%}", delta_color="off")

    parcours = pd.concat([parcours_depuis_ipo("ANT", 83), parcours_depuis_ipo("SPCX", 135)], axis=1)
    fig7 = go.Figure()
    for ticker, couleur in [("SPCX", GRIS), ("ANT", TURQUOISE)]:
        serie = parcours[ticker].dropna()
        fig7.add_trace(go.Scatter(x=serie.index, y=(serie - 1) * 100, name=ticker, mode="lines+markers" if len(serie) < 3 else "lines",
                                  line=dict(color=couleur, width=2.5), marker=dict(size=9),
                                  hovertemplate="séance %{x} : %{y:+.1f} %<extra>" + ticker + "</extra>"))
    fig7.add_hline(y=0, line_dash="dot", line_color="#475569", annotation_text="prix d'IPO")
    fig7.update_layout(xaxis_title="Séances depuis la cotation", yaxis_title="Écart au prix d'IPO (%)", hovermode="x unified")
    mise_en_forme(fig7, 430)
    st.plotly_chart(fig7, width="stretch")

    lignes = {
        "Prix d'IPO": ("83 $", "135 $"),
        "Produit brut de l'offre": ("81,3 Md$", "75,0 Md$"),
        "Placement privé simultané": ("26 Md$ (fournisseurs de calcul)", "aucun"),
        "Écart base diluée / non diluée": (f"{a['actions_diluees'] / a['actions_base'] - 1:+.0%}", f"{s['actions_diluees'] / s['actions_base'] - 1:+.0%}"),
        "Qui contrôle": ("7 cofondateurs, environ 61 % des voix", "Elon Musk, 82,4 % des voix"),
        "Part du capital des contrôlants": ("environ 13 %", "environ 46 % (estimation)"),
        "Croissance du CA sur un an": ("x 12,3 (T3 2026)", "+15 % (T1 2026)"),
        "Marge d'exploitation": ("-3,8 % (9M2026)", "-13,9 % (2025)"),
        "Investissements / CA (2025)": ("4 % au bilan, calcul surtout loué", "111 %"),
        "Rendement à l'ouverture / clôture J1": (f"{a['rendement_ouverture_j1']:+.1%} / {a['rendement_cloture_j1']:+.1%}",
                                                f"{s['rendement_ouverture_j1']:+.1%} / {s['rendement_cloture_j1']:+.1%}"),
        "Argent laissé sur la table": (f"{a['argent_laisse_sur_la_table'] / 1e9:.1f} Md$", f"{s['argent_laisse_sur_la_table'] / 1e9:.1f} Md$"),
    }
    st.dataframe(pd.DataFrame([(k, v[0], v[1]) for k, v in lignes.items()], columns=["", "Anthropic", "SpaceX"]),
                 hide_index=True, width="stretch")
    st.markdown(
        "<p class='note'>SpaceX possède ses actifs (fusées, satellites) et investit plus que son chiffre d'affaires ; "
        "Anthropic loue sa capacité de calcul et porte 900,9 Md$ d'engagements hors bilan. "
        "Cinq mois après son IPO, SpaceX cote à peu près son prix d'introduction après être montée à +57 %. "
        "Détail dans docs/05_comparaison_spacex.md.</p>", unsafe_allow_html=True)
