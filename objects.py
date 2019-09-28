import turtle
from time import sleep


class Pad(turtle.Turtle):
    def __init__(self, x, *args, **kargs):
        super(Pad, self).__init__(*args, **kargs)
        self.shape("square")
        self.shapesize(6, 2)
        self.color("blue")
        self.penup()
        self.goto(x, 0)
        self.dx = 0
        self.dy = 0
        self.currentspeed = 30

    def up(self):
        self.sety(self.ycor() + self.currentspeed)

    def down(self):
        self.sety(self.ycor() - self.currentspeed)


class PointsView(turtle.Turtle):
    def __init__(self, y, *args, **kargs):
        super(PointsView, self).__init__(*args, **kargs)
        self.__msg = "Player A: {} | Player B: {}\nSpeed: {}"
        self.points = [0, 0, 1.5]
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(0, y)
        self.write(self.__msg.format(0, 0, 1.5), align="center")
        self.dx = 0
        self.dy = 0
        self.currentspeed = 0

    def update(self):
        self.clear()
        self.write(self.__msg.format(*[str(point) for point in self.points]), align="center")


class Ball(turtle.Turtle):
    def __init__(self, radius, *args, **kargs):
        super(Ball, self).__init__(*args, **kargs)
        self.shape("circle")
        self.shapesize(radius, radius)
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.dx = 1.5
        self.dy = 1.5
        self.currentspeed = 2


class Window(object):
    def __init__(self):
        self.__screen = turtle.Screen()
        self.__screen.setup(800, 600)
        self.__screen.bgcolor("black")
        self.__screen.tracer(0)

        self.__last_windowsize = (self.__screen.window_width(), self.__screen.window_height())

        self.__objects = (Pad(-350), Pad(340), Ball(1), PointsView(240))

    def __setup_key(self, fun, key):
        self.__screen.onkey(fun, key)
        # self.__screen.onkeypress(fun, key)

    def __update_points(self):
        pass

    def setup(self):
        ref = (("w", "s"), ("Up", "Down"))
        for index, object_ in enumerate(self.__objects[:2]):
            self.__setup_key(object_.up, ref[index][0])
            self.__setup_key(object_.down, ref[index][1])
        self.__screen.listen()

    def update(self):
        windowsize = self.__screen.window_width(), self.__screen.window_height()
        if self.__last_windowsize != windowsize:
            for object_ in self.__objects:
                heigth, width, unknow = object_.shapesize()

                new_width = width * windowsize[0] / self.__last_windowsize[0]
                new_heigth = heigth * windowsize[1] / self.__last_windowsize[1]

                new_x = object_.xcor() * windowsize[0] / self.__last_windowsize[0]
                new_y = object_.ycor() * windowsize[1] / self.__last_windowsize[1]
                if object_ == self.__objects[-1]:
                    print(new_x, new_y)

                new_speed = (new_heigth * object_.currentspeed) / heigth

                ball_new_dx = object_.dx * new_width / width
                ball_new_dy = object_.dy * new_heigth / heigth

                object_.shapesize(new_heigth, new_width)

                object_.setx(new_x)
                object_.sety(new_y)

                object_.currentspeed = new_speed

                object_.dx = ball_new_dx
                object_.dy = ball_new_dy

            self.__last_windowsize = windowsize

    def update_ball(self):
        new_x = self.__objects[2].xcor() + self.__objects[2].dx
        new_y = self.__objects[2].ycor() + self.__objects[2].dy
        # The ball colapse with the pad
        if new_x > self.__objects[1].xcor() - (self.__objects[1].shapesize()[1] * 30 / 2) \
                and (self.__objects[1].ycor() - self.__objects[1].shapesize()[0] * 90 / 6 < new_y < self.__objects[
            1].ycor() + self.__objects[1].shapesize()[0] * 90 / 6):
            self.__objects[2].dx *= -1
            if abs(self.__objects[2].dx) < 5:
                self.__objects[2].dx *= 1.1
                self.__objects[3].points[2] *= 1.1
            if abs(self.__objects[2].dy) < 5:
                self.__objects[2].dy *= 1.1
                self.__objects[3].points[2] *= 1.1
        elif new_x < self.__objects[0].xcor() + (self.__objects[0].shapesize()[1] * 30 / 2) \
                and (self.__objects[0].ycor() - self.__objects[0].shapesize()[0] * 90 / 6 < new_y < self.__objects[
            0].ycor() + self.__objects[0].shapesize()[0] * 90 / 6):
            self.__objects[2].dx *= -1
            if abs(self.__objects[2].dx) < 5:
                self.__objects[2].dx *= 1.1
                self.__objects[3].points[2] *= 1.1
            if abs(self.__objects[2].dy) < 5:
                self.__objects[2].dy *= 1.1
                self.__objects[3].points[2] *= 1.1
        # The ball colapse with the end of the window
        elif -self.__last_windowsize[0] / 2 > new_x or new_x > self.__last_windowsize[0] / 2:
            self.__objects[2].dx *= -1
            if -self.__last_windowsize[0] / 2 > new_x:
                self.__objects[3].points[1] += 1
            else:
                self.__objects[3].points[0] += 1
            self.__objects[2].dy = 1.5
            self.__objects[2].dx = 1.5
            self.__objects[3].points[2] = 1.5
            new_x = 0
            new_y = 0
        # the ball colapse with the up and down borders
        elif -self.__last_windowsize[1] / 2 > new_y:
            self.__objects[2].dy *= -1
            new_y = -self.__last_windowsize[1] / 2
        elif new_y > self.__last_windowsize[1] / 2:
            self.__objects[2].dy *= -1
            new_y = self.__last_windowsize[1] / 2
        self.__objects[2].setx(new_x)
        self.__objects[2].sety(new_y)
        self.__objects[3].update()

    def run(self):
        self.setup()
        while True:
            sleep(0.01)
            self.update()
            self.__screen.update()
            self.update_ball()
