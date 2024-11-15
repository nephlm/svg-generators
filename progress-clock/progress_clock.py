#!/usr/bin/env python3

import argparse
import math
import sys


def eprint(s):
    print(s, file=sys.stderr)


def get_args():
    parser = argparse.ArgumentParser(
        description=(
            "Create a SVG progress clock, used in TTRPGs, such as Blades in the Dark. "
            + "The output is printed to stdout, redirect to a file to save."
        )
    )
    parser.add_argument(
        "sections",
        type=int,
        help="Number of sections in the progress clock.",
        metavar="SECTIONS",
    )
    parser.add_argument(
        "filled",
        type=int,
        help="Number of filled sections in the progress clock.",
        metavar="FILLED",
    )
    parser.add_argument(
        "--color",
        type=str,
        default="#47a",
        help='Color of the segments in the SVG circle. Default is "#47a".',
    )
    parser.add_argument(
        "--size", type=int, default=200, help="Size of the SVG canvas. Default is 200."
    )
    parser.add_argument(
        "--ring",
        action="store_true",
        help="Flag to indicate if the progress clock should be a ring. Default is False.",
    )

    args = parser.parse_args()
    if args.sections < args.filled:
        eprint(f"Can't fill more sections than exist ({args.filled}/{args.sections})")
        sys.exit(2)
    if args.color[0] != "#":
        args.color = "#" + args.color
    if len(args.color) not in (4, 7):
        eprint("--color must a standard RGB format such as #4aa or #4071af")
    return args


def header(image_size=200):
    size = image_size
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">'


def mask(args):
    center = args.size / 2
    radius = center * 0.55

    mask = f"""
    <mask id="transparent-circle">
        <rect width="{args.size}" height="{args.size}" fill="white" />
        <circle cx="{center}" cy="{center}" r="{radius}" fill="black" />
    </mask>
    """
    return mask


def main():
    args = get_args()
    center = args.size / 2
    radius = center * 0.9

    print(header(image_size=args.size))

    hole_radius = center * 0.55
    if args.ring:
        print(mask(args))

    sections = args.sections
    section_angle = 360 / sections
    section_radians = math.radians(section_angle)

    # start_point = None
    for i in range(sections):
        angle_radians = i * section_radians - math.radians(90)

        start_x = math.cos(angle_radians) * radius + center
        start_y = math.sin(angle_radians) * radius + center
        end_x = math.cos(angle_radians + section_radians) * radius + center
        end_y = math.sin(angle_radians + section_radians) * radius + center

        color = args.color if i < args.filled else "None"

        print(
            f'<path d="M{center},{center} L{start_x},{start_y} A{center*.9},{center*.9} 0 0,1 {end_x},{end_y} z" '
            + f' fill="{color}" stroke="black" stroke-width="2"'
            + (' mask="url(#transparent-circle)"' if args.ring else "")
            + "/>"
        )

    if args.ring:
        print(
            f'<circle cx="{center}" cy="{center}" r="{hole_radius}" fill="None" stroke="black" stroke-width="2" />'
        )

    print("</svg>")


if __name__ == "__main__":
    main()
