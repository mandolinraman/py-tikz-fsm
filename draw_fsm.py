"Generate images for neural net implementation presentation."

from tikz_fsm import State, Edge, FiniteStateMachine, flipbend


def main(build=True):
    "Main function."
    serial = True
    num_inputs = 2
    num_hidden = 3
    num_output = 2

    num_neurons = num_hidden + num_output
    num_states = num_inputs + num_neurons

    state_names = ["I0", "I1", "H0", "H1", "H2", "G0", "G1"]
    state_colors = (
        ["LimeGreen"] * num_inputs
        + ["Periwinkle"] * num_hidden
        + ["BurntOrange"] * num_output
    )
    state_labels = [rf"\textsf{{{j}}}" for j in range(num_states)]
    state_draw_style = None
    state_text_style = None

    if serial:
        state_pos = [(0, 0), (2, 0), (4, 0), (6, 0), (8, 0), (10, 0), (12, 0)]
    else:
        state_pos = [(0, 1), (0, -1), (3, 2), (3, 0), (3, -2), (6, 1), (6, -1)]

    adj = [
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 6),
        (2, 5),
        (2, 6),
        (3, 5),
        (3, 6),
        (4, 5),
        (4, 6),
    ]

    edge_label = None
    edge_text_style = None
    edge_draw_style = None
    # edge_draw_style = [
    #     None,
    #     None,
    #     None,
    #     "Turquoise",
    #     None,
    #     None,
    #     None,
    #     "Turquoise",
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    # ]

    if serial:
        bend_angle = [
            "left",
            "left",
            "left",
            "left",
            None,
            "right",
            "right",
            "right",
            "left",
            "left",
            "right",
            "right",
            None,
            "left",
        ]
    else:
        bend_angle = [
            None,
            None,
            None,
            "left=60",
            None,
            None,
            None,
            "right=60",
            None,
            None,
            None,
            None,
            None,
            None,
        ]

    num_edges = len(adj)

    degree = [0] * num_states
    for orig, dest in adj:
        degree[orig] += 1

    fsm = FiniteStateMachine(
        fill_style=r"\lightgrey", draw_style="black", text_style="black"
    )

    states = []
    for i in range(num_states):
        state = State(
            state_names[i],
            state_pos[i],
            state_labels[i],
            state_colors[i],
            state_draw_style,
            state_text_style,
        )
        fsm.add_state(state)
        states.append(state)

    for i, pair in enumerate(adj):
        fsm.add_edge(
            Edge(
                states[pair[0]],
                states[pair[1]],
                label=edge_label,
                bend=bend_angle[i],
                draw_style=edge_draw_style,
                text_style=edge_text_style,
            )
        )

    fsm.generate_tex("prefix.txt", "preamble.txt", "NN-labeled", build)

    # forward propagation
    for index in range(num_neurons + 1):
        i = index + num_inputs - 1
        fsm = FiniteStateMachine(
            fill_style=r"\lightgrey", draw_style="black", text_style="black"
        )
        new_statecolors = []
        new_statedraw = ["none"] * num_states
        new_statelabels = [""] * num_states
        for j in range(num_inputs + num_neurons):
            if j <= i:
                new_statecolors.append(state_colors[j])
            else:
                new_statecolors.append(state_colors[j] + "!10")

        new_adj = []
        new_edgelabel = []
        new_bend = []
        new_edgecolors = []
        new_edgetext = []

        # inactive edges
        for j in range(num_edges):
            orig, dest = adj[j]
            if dest != i:
                new_adj.append(adj[j])
                new_edgelabel.append("")
                new_bend.append(bend_angle[j])
                new_edgecolors.append(r"\lightgrey")
                new_edgetext.append(None)

        # active edges
        for j in range(num_edges):
            orig, dest = adj[j]
            if dest == i:
                new_adj.append(adj[j])
                new_edgelabel.append("")  # '$w_{{{}{}}}$'.format(p,q)
                new_bend.append(bend_angle[j])
                new_edgecolors.append(None)
                new_edgetext.append(None)

                new_statelabels[orig] = state_labels[orig]
                new_statedraw[orig] = None
                new_statelabels[dest] = state_labels[dest]
                new_statedraw[dest] = None

        if index == 0:
            for k in range(num_inputs):
                new_statelabels[k] = state_labels[k]
                new_statedraw[k] = None

        states = []
        for i in range(num_states):
            state = State(
                state_names[i],
                state_pos[i],
                new_statelabels[i],
                new_statecolors[i],
                new_statedraw[i],
                state_text_style,
            )
            fsm.add_state(state)
            states.append(state)

        for i, pair in enumerate(new_adj):
            fsm.add_edge(
                Edge(
                    states[pair[0]],
                    states[pair[1]],
                    label=new_edgelabel[i],
                    bend=new_bend[i],
                    draw_style=new_edgecolors[i],
                    text_style=new_edgetext[i],
                )
            )

        fsm.generate_tex("prefix.txt", "preamble.txt", f"NN-fp{index}", build)

    # backward propagation option 1
    for index in range(num_inputs + num_hidden + 1):
        i = num_inputs + num_hidden - index
        fsm = FiniteStateMachine(r"\lightgrey", "black", "black")
        new_statecolors = []
        new_statedraw = ["none"] * num_states
        new_statelabels = [""] * num_states
        for j in range(num_inputs + num_neurons):
            if j >= i:
                new_statecolors.append(state_colors[j])
            else:
                new_statecolors.append(state_colors[j] + "!10")

        new_adj = []
        new_edgelabel = []
        new_bend = []
        new_edgecolors = []
        new_edgetext = []

        # inactive edges
        for j in range(num_edges):
            dest, orig = adj[j]
            if dest != i:
                new_adj.append((orig, dest))
                new_edgelabel.append("")
                new_bend.append(flipbend(bend_angle[j]))
                new_edgecolors.append(r"\lightgrey")
                new_edgetext.append(None)

        # active edges
        for j in range(num_edges):
            dest, orig = adj[j]
            if dest == i:
                new_adj.append((orig, dest))
                new_edgelabel.append("")  # '$w_{{{}{}}}$'.format(p,q)
                new_bend.append(flipbend(bend_angle[j]))
                new_edgecolors.append(None)
                new_edgetext.append(None)

                new_statelabels[orig] = state_labels[orig]
                new_statedraw[orig] = None
                new_statelabels[dest] = state_labels[dest]
                new_statedraw[dest] = None

        if index == 0:
            for k in range(num_output):
                new_statelabels[-1 - k] = state_labels[-1 - k]
                new_statedraw[-1 - k] = None

        states = []
        for i in range(num_states):
            state = State(
                state_names[i],
                state_pos[i],
                new_statelabels[i],
                new_statecolors[i],
                new_statedraw[i],
                state_text_style,
            )
            fsm.add_state(state)
            states.append(state)

        for i, pair in enumerate(new_adj):
            fsm.add_edge(
                Edge(
                    states[pair[0]],
                    states[pair[1]],
                    label=new_edgelabel[i],
                    bend=new_bend[i],
                    draw_style=new_edgecolors[i],
                    text_style=new_edgetext[i],
                )
            )

        fsm.generate_tex("prefix.txt", "preamble.txt", f"NN-bp{index}", build)

    # backward propagation option 2
    count = [0] * num_states

    for index in range(num_neurons + 1):
        i = num_inputs + num_neurons - index
        fsm = FiniteStateMachine(r"\lightgrey", "black", "black")
        new_statecolors = []
        new_statedraw = ["none"] * num_states
        new_statelabels = [""] * num_states
        for j in range(num_inputs + num_neurons):
            if j >= i:
                new_statecolors.append(state_colors[j])
            else:
                new_statecolors.append(state_colors[j] + "!10")

        new_adj = []
        new_edgelabel = []
        new_bend = []
        new_edgecolors = []
        new_edgetext = []

        # inactive edges
        for j in range(num_edges):
            orig, dest = adj[j]
            if dest != i:
                new_adj.append((dest, orig))
                new_edgelabel.append("")
                new_bend.append(flipbend(bend_angle[j]))
                new_edgecolors.append(r"\lightgrey")
                new_edgetext.append(None)

        # active edges
        for j in range(num_edges):
            orig, dest = adj[j]
            if dest == i:
                count[orig] += 1
                new_adj.append((dest, orig))
                new_edgelabel.append("")  # '$w_{{{}{}}}$'.format(p,q)
                new_bend.append(flipbend(bend_angle[j]))
                new_edgecolors.append(None)
                new_edgetext.append(None)

                new_statelabels[orig] = state_labels[orig]
                new_statedraw[orig] = None
                new_statelabels[dest] = state_labels[dest]
                new_statedraw[dest] = None

            opacity = round(10 + 90 * count[orig] / degree[orig])
            if opacity < 100:
                new_statecolors[orig] = state_colors[orig] + f"!{opacity}"
            else:
                new_statecolors[orig] = state_colors[orig]

        if index == 0:
            for k in range(num_output):
                new_statelabels[-1 - k] = state_labels[-1 - k]
                new_statedraw[-1 - k] = None

            # new_statedraw[p] = None if count[p] > 0 else 'none'

        states = []
        for i in range(num_states):
            state = State(
                state_names[i],
                state_pos[i],
                new_statelabels[i],
                new_statecolors[i],
                new_statedraw[i],
                state_text_style,
            )
            fsm.add_state(state)
            states.append(state)

        for i, pair in enumerate(new_adj):
            fsm.add_edge(
                Edge(
                    states[pair[0]],
                    states[pair[1]],
                    label=new_edgelabel[i],
                    bend=new_bend[i],
                    draw_style=new_edgecolors[i],
                    text_style=new_edgetext[i],
                )
            )

        fsm.generate_tex(
            "prefix.txt", "preamble.txt", f"NN-varbp{index}", build
        )


# call main
main(True)
