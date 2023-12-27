import re
import sys


SVG_TEMPLATE = """<svg width="50" height="50" xmlns="http://www.w3.org/2000/svg">
  <text
    x="50%"
    y="50%"
    text-anchor="middle"
    font-size="300%"
    textLength="150%"
    dominant-baseline="central"
  >
  {emoji}
  </text>
</svg>"""

CONTIGUOUS_EMOJI_PATTERN = re.compile(
    r"""
(?:                                     # unnamed outer group
    \\U[0-9a-f]+                        # we always start with an emoji as a unicode escape sequence
    (?:                                 # unammed inner group
        \\U0{,5}200d                    # search for a zero-width joiner
        \\U[0-9a-f]+                    # followed immediately by another unicode-escape sequence
    )*                                  # end inner group and match multiples (there can be many joined emojis with zwj in sequence)
)                                       # end outer group
""",
    re.X,
)


def get_first_emoji(input_str: str) -> str:
    first_emoji = CONTIGUOUS_EMOJI_PATTERN.match(
        "".join([f"\\U{ord(code_point):0>8x}" for code_point in input_str])
    ).group()
    return first_emoji.encode("utf-8").decode("unicode-escape")


def emoji_to_html_entity(emoji: str) -> str:
    return "".join(
        "&#{};".format(ord(char)) if ord(char) > 127 else char for char in emoji
    )


def render_svg(emoji: str) -> str:
    return SVG_TEMPLATE.format(emoji=emoji)


input_emoji: None | str = None

if len(sys.argv) < 2:
    print("Emoji? Only the first will be used")
    input_emoji = get_first_emoji(input("> ")[1])
else:
    input_emoji = get_first_emoji(sys.argv[1])

if input_emoji is None:
    print("No emoji was provided")
    sys.exit(1)
# This is a force of habit, there's no indication using the utf-8 version won't work
html_entity_form = emoji_to_html_entity(input_emoji)

print(render_svg(html_entity_form))
