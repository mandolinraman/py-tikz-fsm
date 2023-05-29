"Python wrapper for TikZ to generate state diagram plots."

import os
from dataclasses import dataclass

# from collections import namedtuple


def read_file(file_location):
    "Reads a file into a list of strings."
    with open(file_location, "r", encoding="UTF-8") as input_data_file:
        input_data = input_data_file.readlines()
    return [line.rstrip() for line in input_data]


def write_file(file_location, output_data):
    "Writes a list of strings to a file."
    with open(file_location, "w", encoding="UTF-8") as output_data_file:
        output_data_file.write("\n".join(output_data) + "\n")


def flipbend(string):
    "Swaps right <-> right in a string"
    if string is None:
        return None
    if string.find("right") >= 0:
        return string.replace("right", "left")
    elif string.find("left") >= 0:
        return string.replace("left", "right")


@dataclass
class State:
    "State class definition."
    name: str
    pos: tuple
    label: str = None
    fill_style: str = None
    draw_style: str = None
    text_style: str = None

    @property
    def style(self) -> str:
        "Return style string."
        temp = ["state"]
        if self.fill_style:
            temp.append(f"fill={self.fill_style}")
        if self.draw_style:
            temp.append(f"draw={self.draw_style}")
        if self.text_style:
            temp.append(f"text={self.text_style}")
        return ",".join(temp)


@dataclass
class Edge:
    "Edge class definition."
    orig: State
    dest: State
    label: str = None
    bend: str = None
    loop: str = None
    draw_style: str = None
    text_style: str = None

    @property
    def style(self) -> str:
        "Return style string."
        temp = []
        if self.bend:
            temp.append(f"bend {self.bend}")
        if self.loop:
            temp.append(f"loop {self.loop}")
        if self.draw_style:
            temp.append(f"draw={self.draw_style}")
        if self.text_style:
            temp.append(f"text={self.text_style}")
        return ",".join(temp)


class FiniteStateMachine:
    "Finite state machine"

    def __init__(self, fill_style=None, draw_style=None, text_style=None):
        self.states = []
        self.edges = []

        temp = []
        if fill_style is not None:
            temp.append(f"fill={fill_style}")
        if draw_style is not None:
            temp.append(f"draw={draw_style}")
        if text_style is not None:
            temp.append(f"text={text_style}")

        self.default_style = ",".join(temp)

    def add_state(self, state):
        "Add a new state to the graph."
        self.states.append(state)

    def add_edge(self, edge):
        "Add a new edge to the graph."
        self.edges.append(edge)

    @property
    def num_states(self):
        "Number of states."
        return len(self.states)

    @property
    def num_edges(self):
        "Number of edges."
        return len(self.edges)

    def generate_tex(
        self, prefix_file, preamble_file, output_file, build=False
    ):
        "Generates a tex file and optionally compiles it to produce a pdf."
        # read prefix, preamble
        lines = read_file(prefix_file)
        lines += read_file(preamble_file)

        # rest of tex document:
        lines += [r"\begin{document}", r"  \pagestyle{empty}"]
        lines += [
            r"  \begin{tikzpicture}[->,>=stealth',shorten >=1pt,auto,node distance=4cm,semithick]"
        ]
        lines.append(
            rf"    \tikzstyle{{every state}}=[{self.default_style}]"
        )
        lines.append(
            r"    \tikzset{every loop/.style={min distance=10mm,looseness=10}}"
        )

        # define all states:
        for state in self.states:
            label = state.label or ""
            lines.append(
                rf"    \node[{state.style}] ({state.name}) "
                + rf"at {state.pos} {{{label}}};"
            )

        # define all edges:
        for edge in self.edges:
            label = edge.label or ""
            lines.append(
                rf"    \path ({edge.orig.name}) edge [{edge.style}] "
                + rf"node {{{label}}} ({edge.dest.name});"
            )

        # add suffix
        lines += [r"  \end{tikzpicture}", r"\end{document}"]

        # save file
        write_file(output_file + ".tex", lines)

        if build:
            os.system(f"pdflatex {output_file}.tex")
            os.system(f"pdfcrop {output_file}.pdf {output_file}.pdf")
            os.system(f"rm {output_file}.log {output_file}.aux")
