import math
from tkinter import TclError
from turtle import Screen, Terminator, Turtle

# Looping stops: first and last match so the mandala closes cleanly.
PALETTE = (
    (0.98, 0.82, 0.42),  # amber
    (0.96, 0.45, 0.32),  # coral
    (0.78, 0.25, 0.42),  # crimson
    (0.45, 0.22, 0.62),  # violet
    (0.20, 0.42, 0.78),  # cobalt
    (0.12, 0.62, 0.66),  # teal
    (0.55, 0.86, 0.62),  # celadon
    (0.98, 0.82, 0.42),  # amber
)

def _mix(c0, c1, t):
    return tuple(a + (b - a) * t for a, b in zip(c0, c1))


def palette_at(stops, t):
    t %= 1.0
    scaled = t * (len(stops) - 1)
    i = int(scaled)
    if i >= len(stops) - 1:
        return stops[-1]
    return _mix(stops[i], stops[i + 1], scaled - i)


def _hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        *(max(0, min(255, round(c * 255))) for c in rgb)
    )


def _bezier_point(p0, p1, p2, p3, t):
    u = 1.0 - t
    uu, tt = u * u, t * t
    return (
        uu * u * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + tt * t * p3[0],
        uu * u * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + tt * t * p3[1],
    )


def circle_bezier(t, radius, extent=None, max_chord_error=0.25):
    """Circular arc as cubic Bézier segments. Same convention as Turtle.circle."""
    if extent is None:
        extent = 360.0
    if radius == 0 or extent == 0:
        return

    heading = math.radians(t.heading())
    x, y = t.position()
    # Signed radius: positive is left of the heading (CCW), negative is right (CW).
    cx = x - radius * math.sin(heading)
    cy = y + radius * math.cos(heading)
    r = abs(radius)
    start = math.atan2(y - cy, x - cx)
    sweep = math.radians(extent if radius > 0 else -extent)

    max_seg = math.pi / 2  # one cubic is only accurate up to 90 degrees
    remaining = sweep
    angle = start
    direction = 1.0 if sweep >= 0 else -1.0

    while abs(remaining) > 1e-12:
        seg = direction * min(abs(remaining), max_seg)
        # Control-point offset that pulls the cubic onto the circle.
        kappa = (4.0 / 3.0) * math.tan(seg / 4.0)

        a0, a1 = angle, angle + seg
        p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
        p3 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        tx0, ty0 = -math.sin(a0), math.cos(a0)
        tx1, ty1 = -math.sin(a1), math.cos(a1)
        p1 = (p0[0] + r * kappa * tx0, p0[1] + r * kappa * ty0)
        p2 = (p3[0] - r * kappa * tx1, p3[1] - r * kappa * ty1)

        # Chord error of a step dθ is r * (1 - cos(dθ / 2)).
        if r > max_chord_error:
            dθ = 2.0 * math.acos(1.0 - max_chord_error / r)
            n = max(2, math.ceil(abs(seg) / dθ))
        else:
            n = 2
        for i in range(1, n + 1):
            t.goto(_bezier_point(p0, p1, p2, p3, i / n))

        angle = a1
        remaining -= seg

    t.setheading(t.heading() + (extent if radius > 0 else -extent))


def gen_mandala(size_of_gap=0.82, start_i=180, end_i=290+1):
    screen = Screen()
    screen.bgcolor("#04090a")
    screen.title("Mandagen 2")
    screen.tracer(5)

    t = Turtle()
    t.speed(0)
    t.goto(140, -90)

    span = max(1, end_i - start_i - 1)
    try:
        for i in range(start_i, end_i):
            progress = (i - start_i) / span
            t.hideturtle()
            t.right(120)
            t.pensize(3)
            # Neighboring stops, so the three arcs read as one wash, not one flat ink.
            t.color(_hex(palette_at(PALETTE, progress)))
            circle_bezier(t, -i / 3, 270)
            t.color(_hex(palette_at(PALETTE, progress + 0.045)))
            circle_bezier(t, i / 2, 270)
            t.color(_hex(palette_at(PALETTE, progress + 0.09)))
            circle_bezier(t, i / 5, 180)
    except (Terminator, TclError):
        return

    t.color(_hex(palette_at(PALETTE, 1.0)))
    t.right(120)
    circle_bezier(t, (1 - i) / 3, 120)
    screen.exitonclick()


if __name__ == "__main__":
    gen_mandala()
