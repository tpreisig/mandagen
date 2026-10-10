import colorsys
from tkinter import TclError
from turtle import Screen, Terminator, Turtle


def gen_mandala(size_of_gap=0.82, start_i=180, end_i=290):
    screen = Screen()
    screen.bgcolor("#04090a")
    screen.title("Mandagen 1")
    screen.tracer(200)

    t = Turtle()
    t.speed(10)
    h=120
    t.goto(140, -90)

    try:
        for i in range(start_i, end_i):
            rgb = colorsys.hsv_to_rgb(h, 1,1)
            t.color(rgb)
            h += 0.82
            t.hideturtle()
            t.right(120)
            t.pensize(3)
            t.circle(-i/3, 270, steps=120)
            t.circle(i/2, 270, steps=120)
            t.circle(i/5, 180, steps=120)
    except (Terminator, TclError):
        return

    color = colorsys.hsv_to_rgb(h,1,1)
    t.color(color)
    t.right(120)
    t.circle((1-i)/3, 120)
    screen.exitonclick()

if __name__ == "__main__":
    gen_mandala()
