import turtle


# from time import sleep


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
    def __init__(self, y, speed, *args, **kargs):
        super(PointsView, self).__init__(*args, **kargs)
        self.__msg = "Player A: {} | Player B: {}\nSpeed: {}"
        self.info_to_show = [0, 0, speed]
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
        values = (self.info_to_show[0], self.info_to_show[1], str(self.info_to_show[2]*100)[:3] + "%")
        self.write(self.__msg.format(*values), align="Center")


class Ball(turtle.Turtle):
    def __init__(self, radius, speed, *args, **kargs):
        super(Ball, self).__init__(*args, **kargs)
        self.shape("circle")
        self.shapesize(radius, radius)
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.dx = speed
        self.dy = speed
        self.speed_limit = 2
        self.__speed_multiplier = 1.5
        self.currentspeed = 2

    def speed_up(self):
        if abs(self.dx) < self.speed_limit:
            self.dx *= self.__speed_multiplier
        if abs(self.dy) < self.speed_limit:
            self.dy *= self.__speed_multiplier


class Window(object):
    def __init__(self):
        self.__screen = turtle.Screen()
        self.__screen.setup(800, 600)
        self.__screen.bgcolor("black")
        self.__screen.tracer(0)

        self.__last_windowsize = (self.__screen.window_width(), self.__screen.window_height())
        self.speed = 0.2
        self.__objects = (Pad(-350), Pad(340), Ball(1, self.speed), PointsView(240, self.speed))

    # Function to update the points
    def __update_points(self, a, b):
        if a and not b:
            self.__objects[3].info_to_show[0] += 1
        elif b and not a:
            self.__objects[3].info_to_show[1] += 1

    # Setup he buttons for the pads
    def __setup_key(self, fun, key):
        self.__screen.onkey(fun, key)
        # self.__screen.onkeypress(fun, key)

    # Setup the pads
    def setup_pads(self):
        ref = (("w", "s"), ("Up", "Down"))
        for index, object_ in enumerate(self.__objects[:2]):
            self.__setup_key(object_.up, ref[index][0])
            self.__setup_key(object_.down, ref[index][1])
        self.__setup_key(self.__speed_up_ball, "space")
        self.__screen.listen()

    # When the user change the window size adapt everything to the new one
    def update_sizes(self):
        windowsize = self.__screen.window_width(), self.__screen.window_height()
        if self.__last_windowsize != windowsize:
            for object_ in self.__objects:
                heigth, width, unknow = object_.shapesize()

                new_width = width * windowsize[0] / self.__last_windowsize[0]
                new_heigth = heigth * windowsize[1] / self.__last_windowsize[1]

                new_x = object_.xcor() * windowsize[0] / self.__last_windowsize[0]
                new_y = object_.ycor() * windowsize[1] / self.__last_windowsize[1]

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

    def __speed_up_ball(self):
        # Speed up the ball everytime it collapse with a pad
        self.__objects[2].speed_up()
        self.__objects[3].info_to_show[2] = abs(self.__objects[2].dx)

    def update_ball(self):
        new_x = self.__objects[2].xcor() + self.__objects[2].dx
        new_y = self.__objects[2].ycor() + self.__objects[2].dy
        # The ball colapse with the pad
        if (new_x > self.__objects[1].xcor() - (self.__objects[1].shapesize()[1] * 30 / 2)
            and (self.__objects[1].ycor() - self.__objects[1].shapesize()[0] * 90 / 6 < new_y < self.__objects[
                    1].ycor() + self.__objects[1].shapesize()[0] * 90 / 6)) or (
                new_x < self.__objects[0].xcor() + (self.__objects[0].shapesize()[1] * 30 / 2)
                and (self.__objects[0].ycor() - self.__objects[0].shapesize()[0] * 90 / 6 < new_y <
                     self.__objects[0].ycor() + self.__objects[0].shapesize()[0] * 90 / 6)):
            # Change the direction
            self.__objects[2].dx *= -1
            # Update the speed
            self.__speed_up_ball()
        # The ball colapse with the left end of the window
        elif -self.__last_windowsize[0] / 2 > new_x:
            # Give the points to respective players
            self.__objects[3].info_to_show[1] += 1
            # Restore the speed of the ball
            self.__objects[2].dy = self.speed
            self.__objects[2].dx = self.speed
            self.__objects[3].info_to_show[2] = self.speed
            # Restore the position of the ball to the middle
            new_x = 0
            new_y = 0
        # The ball colapse with the rigth end of the window
        elif new_x > self.__last_windowsize[0] / 2:
            #  Give the points to th player
            self.__objects[3].info_to_show[0] += 1
            # Restore the speed of the ball
            self.__objects[2].dy = self.speed
            self.__objects[2].dx = self.speed * -1
            self.__objects[3].info_to_show[2] = self.speed
            # Restore the position of the ball to the middle
            new_x = 0
            new_y = 0
        # the ball colapse with the up and down borders
        elif -self.__last_windowsize[1] / 2 > new_y:
            self.__objects[2].dy *= -1
            new_y = -self.__last_windowsize[1] / 2
        elif new_y > self.__last_windowsize[1] / 2:
            self.__objects[2].dy *= -1
            new_y = self.__last_windowsize[1] / 2

        # Update the coordinates
        self.__objects[2].setx(new_x)
        self.__objects[2].sety(new_y)
        self.__objects[3].update()

    def __check_points(self):
        if 10 in self.__objects[3].info_to_show[:2]:
            print(f"Player {'AB'[self.__objects[3].info_to_show[:2].index(10)]} Wins!")
            self.__objects[3].info_to_show[0] = 0
            self.__objects[3].info_to_show[1] = 0
            return "y" not in input("Do you want to play again?[y/n]")

    def run(self):
        self.setup_pads()
        while True:
            if self.__check_points():
                self.__screen.bye()
                exit(-1)
            # sleep(0.01)
            self.update_sizes()
            self.__screen.update()
            self.update_ball()
