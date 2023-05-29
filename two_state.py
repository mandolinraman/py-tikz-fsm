from tikz_fsm import State, Edge, FiniteStateMachine


def main(build=True):
    "Main function."

    fsm = FiniteStateMachine(
        fill_style=r"\lightgrey", draw_style="black", text_style="black"
    )

    states = []
    for i in range(2):
        state = State(f"{i}", (2 * i, 0), f"${i}$")
        fsm.add_state(state)
        states.append(state)

    for i in range(2):
        for j in range(2):
            prob = 0.9 if i == j else 0.1
            if i != j:
                edge = Edge(states[i], states[j], label=f"${prob}$", bend="left=15")
            elif i == 0:
                edge = Edge(states[i], states[j], label=f"${prob}$", loop="left")
            else:
                edge = Edge(states[i], states[j], label=f"${prob}$", loop="right")

            fsm.add_edge(edge)

    fsm.generate_tex("prefix.txt", "preamble.txt", "two_state", build)


# call main
main(True)
