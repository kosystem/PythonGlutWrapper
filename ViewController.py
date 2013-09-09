from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.freeglut import *
import GlutWrapper
import math

ESCAPE = '\033'


class GlutViewController(GlutWrapper.GlutWrapper):
    """docstring for GlutViewController"""
    def __init__(self):
        super(GlutViewController, self).__init__()

    def display(self, deltaTime):
        self.drawAxis(10)
        # self.overlayString("test", 1, 1)

    # User interface -----------------------------------
    def mouse(self, button, state, x, y):
        print "MousePress: button: %d, x: %d, y:%d" % (button, x, y)
        self.mouseState.button = button
        self.mouseState.pressed = ~state
        self.mouseState.x = x
        self.mouseState.y = y
        if button == 3:
            self.camera.distance *= 0.875
        elif button == 4:
            sel.camera.distance *= 1.125

    def motion(self, x, y):
        # print "MouseMove: x: %d, y: %d" % (x, y)
        movedX = x - self.mouseState.x
        movedY = y - self.mouseState.y
        if self.mouseState.button == 0 & self.mouseState.pressed:
            self.camera.pan += float(-movedX)/100.0
            self.camera.tilt += float(movedY)/100.0
        if self.camera.tilt >= math.pi/2.0:
            self.camera.tilt = math.pi/2.0-0.01
        if self.camera.tilt <= -math.pi/2.0:
            self.camera.tilt = -(math.pi/2.0-0.01)
        self.mouseState.x = x
        self.mouseState.y = y

    def keyboard(self, key, x, y):
        print "KeyboardPress: %c" % key
        if key == ESCAPE:
            sys.exit()

    # Draw ----------------------------------------------
    def drawAxis(self, length):
        lighting = glGetBoolean(GL_LIGHTING)
        light0 = glGetBoolean(GL_LIGHT0)
        light1 = glGetBoolean(GL_LIGHT1)

        color = glGetFloatv(GL_CURRENT_COLOR)
        depth = glGetBoolean(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glLineWidth(1.0)

        glBegin(GL_LINES)
        glColor(1.0, 0.0, 0.0, 1.0)
        glVertex(0.0, 0.0, 0.0)
        glVertex(length, 0.0, 0.0)

        glColor(0.0, 1.0, 0.0, 1.0)
        glVertex(0.0,    0.0, 0.0)
        glVertex(0.0, length, 0.0)

        glColor(0.0, 0.0, 1.0, 1.0)
        glVertex(0.0, 0.0,    0.0)
        glVertex(0.0, 0.0, length)
        glEnd()
        if lighting:
            glEnable(GL_LIGHTING)
        if light0:
            glEnable(GL_LIGHT0)
        if light1:
            glEnable(GL_LIGHT1)
        if not depth:
            glDisable(GL_DEPTH_TEST)
        glColor(color)

    def overlayString(self, string, x, y, color=(1, 1, 1)):
        glMatrixMode(GL_PROJECTION)
        # glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, 2.0, 2.0, 0.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        # glPushMatrix()
        glLoadIdentity()
        # glPushAttrib(GL_ENABLE_BIT)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        glRasterPos3f(x, y, 0.0)
        glutBitmapString(GLUT_BITMAP_HELVETICA_12, string)

        # glPopAttrib()
        # glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        # glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


if __name__ == '__main__':
    view = GlutViewController()
    view.startFramework()