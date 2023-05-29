from tikz_fsm import State, Edge, FiniteStateMachine


def main(build=True):
    "Main function."

    fsm = FiniteStateMachine(
        fill_style=r"\lightgrey", draw_style="black", text_style="black"
    )

    num = 5  # number of time steps
    mem = 0  # output memory

    states = []
    outputs = [None]  # no output from q_0
    emission_color = "ForestGreen"
    trans_color = "NavyBlue"
    for i in range(num):
        state = State(f"q{i}", (2 * i, 0), f"$q_{i}$")
        fsm.add_state(state)
        states.append(state)

        if i > 0:
            output = State(f"o{i}", (2 * i, 2), f"$o_{i}$")
            fsm.add_state(output)
            outputs.append(output)

            # transition edge:
            trans = Edge(states[i - 1], states[i], draw_style=trans_color)
            fsm.add_edge(trans)

            # emission edge:
            emission = Edge(states[i], outputs[i],draw_style=emission_color)
            fsm.add_edge(emission)

            for j in range(1, mem + 1):
                angle = 0 if j == 1 else 30
                if i - j > 0:
                    ddnp = Edge(
                        outputs[i - j],
                        outputs[i],
                        bend=f"left={angle}",
                        draw_style=emission_color,
                    )
                    fsm.add_edge(ddnp)

    fsm.generate_tex("prefix.txt", "preamble.txt", "markov_model", build)


# call main
main(True)
