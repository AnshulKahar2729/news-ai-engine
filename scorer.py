def final_score(ai):
    return round(
        ai["severity"] * 0.35 +
        ai["permanence"] * 0.25 +
        ai["continuation_probability"] * 0.25 +
        ai["narrative_strength"] * 0.15,
        2
    )
