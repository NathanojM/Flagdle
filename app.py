import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from difflib import SequenceMatcher
from operator import itemgetter

# ----------------------------
# PAGE SETUP
# ----------------------------

st.set_page_config(
    page_title="Guess the Flag",
    page_icon="🏳️",
    layout="wide"
)

st.title("🏳️ Guess the Flag!")
st.write("Can you identify the country from its flag's RGB colour composition?")
st.write("You have six guesses. Good luck!")

# ----------------------------
# LOAD DATA
# ----------------------------

@st.cache_data
def load_data():
    table = pd.read_csv("flagtable.csv")

    table["r"] = pd.to_numeric(table["r"])
    table["g"] = pd.to_numeric(table["g"])
    table["b"] = pd.to_numeric(table["b"])

    # Make black visible

    # Convert RGB to hexadecimal
    table["rgb"] = table.apply(
        lambda row: "#{:02x}{:02x}{:02x}".format(
            int(row["r"]),
            int(row["g"]),
            int(row["b"])
        ),
        axis=1
    )

    return table


try:
    allcountries = load_data()
except Exception as e:
    st.error(f"Could not load flagtable.csv: {e}")
    st.stop()


# ----------------------------
# START / RESET GAME
# ----------------------------

def new_game():
    country = random.choice(allcountries["Country"].dropna().unique())

    st.session_state.country = country
    st.session_state.guesses = 0
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.message = ""


if "country" not in st.session_state:
    new_game()


# ----------------------------
# PREPARE SELECTED FLAG
# ----------------------------

table = allcountries[
    allcountries["Country"] == st.session_state.country
].copy()

table = table[table["%"] >= 0.1].copy()

table.loc[table["%"] <= 1, "%"] = 3

table = table.sort_values(by="%", ascending=False)


# ----------------------------
# CREATE RGB CHART
# ----------------------------

fig = go.Figure()

fig.add_trace(go.Scatterternary(
    a=table["r"],
    b=table["g"],
    c=table["b"],
    mode="markers+lines",

    marker=dict(
        color=table["rgb"],
        size=table["%"] / 100,
        opacity=1
    ),

    line=dict(color="lightgray"),
    text=""
))

fig.update_ternaries(
    aaxis_title="Red",
    baxis_title="Green",
    caxis_title="Blue"
)

fig.update_layout(
    height=650,
    margin=dict(l=40, r=40, t=30, b=30)
)


# ----------------------------
# DISPLAY GAME
# ----------------------------

left, right = st.columns([2, 1])

with left:
    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("Your guess")

    remaining = 6 - st.session_state.guesses

    st.metric("Guesses remaining", remaining)

    st.progress(remaining / 6)

    if not st.session_state.game_over:

        with st.form("guess_form"):

            guess = st.text_input(
                "Enter a country:",
                placeholder="e.g. France"
            )

            submitted = st.form_submit_button("Submit guess")

        if submitted and guess.strip():

            guess = guess.strip().upper()

            countries = (
                allcountries["Country"]
                .dropna()
                .str.upper()
                .unique()
                .tolist()
            )

            if guess not in countries:

                matches = []

                for country in countries:
                    similarity = SequenceMatcher(
                        None, guess, country
                    ).ratio()

                    matches.append({
                        "country": country,
                        "res": similarity
                    })

                matches = sorted(
                    matches,
                    key=itemgetter("res"),
                    reverse=True
                )

                st.warning("Not a valid country.")

                st.write("Did you mean?")

                for match in matches[:3]:
                    st.write("- " + match["country"].title())

            elif guess == st.session_state.country.upper():

                st.session_state.guesses += 1
                st.session_state.won = True
                st.session_state.game_over = True

                st.success(
                    f"Correct! You guessed it in "
                    f"{st.session_state.guesses} guesses!"
                )

            else:

                st.session_state.guesses += 1

                if st.session_state.guesses >= 6:
                    st.session_state.game_over = True

                    st.error("Game over! You've used all six guesses.")

                else:
                    st.error("Incorrect! Try again.")

            st.rerun()


# ----------------------------
# REVEAL ANSWER
# ----------------------------

if st.session_state.game_over:

    st.divider()

    if st.session_state.won:
        st.balloons()
        st.success("You got it!")
    else:
        st.error("Better luck next time!")

    st.subheader(
        f"The answer was {st.session_state.country}"
    )

    iso = str(table.iloc[0]["ISO"]).lower()

    flag_url = f"https://flagcdn.com/h240/{iso}.png"

    st.image(flag_url, width=250)

    if st.button("🔄 Play Again"):
        new_game()
        st.rerun()
