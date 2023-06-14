import xml.etree.ElementTree as ET
import itertools
import re


def parse_length(length):
    match = re.match(r"^([\d.]+)(px)?$", length)
    if match:
        return float(match.group(1))
    return 0.0


def calculate_mse(element1, element2):
    mse = 0.0
    if element1 is None or element2 is None:
        return 0.0

    if element1.tag != element2.tag:
        mse += 1.0

    for attr in element1.attrib.keys():
        if attr != "id":
            value1 = element1.attrib.get(attr, "0")
            value2 = element2.attrib.get(attr, "0")
            mse += (parse_length(value1) - parse_length(value2)) ** 2

    children1 = list(element1)
    children2 = list(element2)
    min_length = min(len(children1), len(children2))

    for child1, child2 in itertools.zip_longest(children1, children2):
        mse += calculate_mse(child1, child2)

    if len(children1) != len(children2):
        extra_children = (
            children1[min_length:]
            if len(children1) > len(children2)
            else children2[min_length:]
        )
        mse += sum(len(list(child.iter())) for child in extra_children)

    return mse


def calculate_svg_mse(svg_data1, svg_data2):
    element1 = ET.fromstring(svg_data1)
    element2 = ET.fromstring(svg_data2)
    mse = calculate_mse(element1, element2)
    return mse


if __name__ == "__main__":
    svg1 = open("../svg/emoji_u00a9.svg", "r").read()
    svg2 = open("../svg/emoji_u1f0cf.svg", "r").read()
    mse = calculate_svg_mse(svg1, svg2)
    print("MSE:", mse)

    svg2 = open("../svg/emoji_u00a9.svg", "r").read()
    print("MSE:", calculate_svg_mse(svg1, svg2))

    svg1 = open("result.svg", "r").read()
    svg2 = open("../svg/emoji_u1f1e6.svg", "r").read()
    print("Our 'A' and official 'A' MSE:", calculate_svg_mse(svg1, svg2))
