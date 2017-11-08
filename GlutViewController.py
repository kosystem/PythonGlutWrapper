from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.freeglut import *
import GlutWrapper
import math

ESCAPE = b'\033'


class GlutViewController(GlutWrapper.GlutWrapper):
    """docstring for GlutViewController"""
    def __init__(self):
        super(GlutViewController, self).__init__()
        self.count = 0.0

    def display(self, deltaTime):
        self.drawAxis(50)

        self.count += 1.0
        glRotate(self.count, 0, 1, 0)
        glutSolidTeapot(10)

        if deltaTime > 0.0:
            fpsString = "FPS: %.1f" % (1.0/deltaTime)
            self.overlayString(fpsString, 0.0, 0.0)
        self.overlayString("LB", 0.0, -1.0)
        self.overlayString("RT", -20.0, 0.0)
        self.overlayString("RB", -20.0, -1.0)


    # User interface -----------------------------------
    def mouse(self, button, state, x, y):
        # print("MousePress: button: %d, x: %d, y:%d" % (button, x, y))
        self.mouseState.button = button
        self.mouseState.pressed = ~state
        self.mouseState.x = x
        self.mouseState.y = y
        if button == 3:
            self.camera.distance *= 0.875
        elif button == 4:
            self.camera.distance *= 1.125

    def motion(self, x, y):
        # print("MouseMove: x: %d, y: %d" % (x, y))
        movedX = x - self.mouseState.x
        movedY = y - self.mouseState.y
        if self.mouseState.button == 0 & self.mouseState.pressed:
            self.camera.pan += float(-movedX)/100.0
            self.camera.tilt += float(movedY)/100.0
        if self.camera.tilt > math.pi/2.0:
            self.camera.tilt = math.pi/2.0-0.01
        if self.camera.tilt < -math.pi/2.0:
            self.camera.tilt = -(math.pi/2.0-0.01)
        self.mouseState.x = x
        self.mouseState.y = y

    def keyboard(self, key, x, y):
        print("KeyboardPress: %s" % key)
        if key == ESCAPE:
            sys.exit()
        elif key == b'p':
            self.camera.distance *= 0.875
        elif key == b'n':
            self.camera.distance *= 1.125

    def setColor(self, color):
        glColor(color[0], color[1], color[2])
        glMaterial(GL_FRONT, GL_AMBIENT, color)
        glMaterial(GL_FRONT, GL_DIFFUSE, color)


if __name__ == '__main__':
    print("Hit ESC key to quit.")
    view = GlutViewController()
    view.frameTime = 1.0/60.0
    view.startFramework()
