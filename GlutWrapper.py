from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from math import *
import time

ESCAPE = '\033'


class Camera(object):
    """docstring for Camera"""
    def __init__(self):
        self.lock_x = 0
        self.lock_y = 0
        self.lock_z = 0
        self.distance = 300
        self.pan = 0.0
        self.tilt = 0.0


class MouseState(object):
    """docstring for MouseState"""
    def __init__(self):
        self.button = 0
        self.pressed = 0
        self.x = 0
        self.y = 0


class GlutWrapper(object):
    """docstring for GlutWrapper"""
    def __init__(self):
        self.windowWidth = 640
        self.windowHeight = 480
        self.windowPositionX = 100
        self.windowPositionY = 100
        self.title = b"Glut Wrapper"
        self.camera = Camera()
        self.mouseState = MouseState()
        self.frameElapsed = 0.0
        self.displayElapsed = 0.0
        self.elapsedTime = 0.0
        self.frameTime = 1.0/20.0

    def startFramework(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
        glutInitWindowPosition(self.windowPositionX, self.windowPositionY)
        glutInitWindowSize(self.windowWidth, self.windowHeight)
        glutCreateWindow(self.title)

        glutDisplayFunc(self.displayFramework)
        glutReshapeFunc(self.reshape)
        glutIdleFunc(self.idle)

        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutPassiveMotionFunc(self.passiveMotion)
        # glutMouseWheelFunc(self.mouseWheel)

        glutKeyboardFunc(self.keyboard)
        glutKeyboardUpFunc(self.keyboardUp)
        glutSpecialFunc(self.special)
        glutSpecialUpFunc(self.specialUp)

        self.initialize()
        self.load()

        glutMainLoop()

    def displayFramework(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setLights()
        self.setCamera()
        self.display(self.getDisplayElapsed())

        glutSwapBuffers()

    def setCamera(self):
        width = glutGet(GLUT_WINDOW_WIDTH)
        height = glutGet(GLUT_WINDOW_HEIGHT)
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30.0, float(width) / height, 0.5, 10000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        distance = self.camera.distance
        tilt = self.camera.tilt
        pan = self.camera.pan
        lock_x = self.camera.lock_x
        lock_y = self.camera.lock_y
        lock_z = self.camera.lock_z
        gluLookAt(
            distance*sin(pan)*cos(tilt) + lock_x,
            distance*sin(tilt) + lock_y,
            distance*cos(pan)*cos(tilt) + lock_z,
            lock_x, lock_y, lock_z,
            0.0,
            1.0,
            0.0)

    def setLights(self):
        light1_position = (0.0, 1.0, 1.0, 0.0)
        light2_position = (0.0, -1.0, -1.0, 0.0)
        white_light = (1.0, 1.0, 1.0, 1.0)
        lmodel_ambient = (0.2, 0.2, 0.2, 1.0)
        ambient_light = (0.4, 0.4, 0.4, 1.0)

        glLight(GL_LIGHT0, GL_POSITION, light1_position)
        glLight(GL_LIGHT0, GL_AMBIENT, ambient_light)
        glLight(GL_LIGHT0, GL_DIFFUSE, white_light)
        glLight(GL_LIGHT0, GL_SPECULAR, white_light)

        glLight(GL_LIGHT1, GL_POSITION, light2_position)
        glLight(GL_LIGHT1, GL_AMBIENT, lmodel_ambient)
        glLight(GL_LIGHT1, GL_DIFFUSE, ambient_light)
        glLight(GL_LIGHT1, GL_SPECULAR, lmodel_ambient)

        # glLightModel(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)

    def getFrameElapsed(self):
        now = time.time()
        if self.frameElapsed == 0.0:
            self.frameElapsed = now
        elapsed = now - self.frameElapsed
        self.frameElapsed = now
        return elapsed

    def getDisplayElapsed(self):
        now = time.time()
        if self.displayElapsed == 0.0:
            self.displayElapsed = now
        elapsed = now - self.displayElapsed
        self.displayElapsed = now
        return elapsed

    # User overwite ---------------------------------------
    def display(self, deltaTime):
        glMaterial(GL_FRONT, GL_AMBIENT, (0.8, 0.6, 0.5, 1.0))
        glMaterial(GL_FRONT, GL_DIFFUSE, (0.8, 0.6, 0.5, 1.0))
        glutSolidTeapot(50)

    def idle(self):
        self.elapsedTime += self.getFrameElapsed()
        if self.elapsedTime >= self.frameTime:
            glutPostRedisplay()
            self.elapsedTime -= self.frameTime

    def reshape(self, w, h):
        glViewport(0, 0, w, h)

    def initialize(self):
        glClearColor(0.4, 0.5, 0.5, 1.0)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)

    def load(self):
        # NOTE: model data load
        pass

    # User interface -----------------------------------
    def mouse(self, button, state, x, y):
        #print "MousePress: button: %d, x: %d, y:%d" % (button, x, y)
        pass

    def motion(self, x, y):
        #print "MouseMove: x: %d, y: %d" % (x, y)
        pass

    def passiveMotion(self, x, y):
        self.mouseState.x = x
        self.mouseState.y = y

    def keyboard(self, key, x, y):
        #print "KeyboardPress: %c" % key
        if key == ESCAPE:
            sys.exit()

    def keyboardUp(self, key, x, y):
        #print "KeyboardUp: %c" % key
        pass

    def special(self, key, x, y):
        #print "SpecialKeyPress: %c" % key
        pass

    def specialUp(self, key, x, y):
        #print "SpecialKeyUp: %c" % key
        pass

    # Basic Draw ----------------------------------------------
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

    def drawHorizon(self, x, y, xTick, yTick):
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
        glColor(0.7, 0.7, 0.7, 1.0)
        for xi in range(-x, x+xTick, xTick):
            glVertex(xi, 0.0, -y)
            glVertex(xi, 0.0, y)
        for yi in range(-y, y+yTick, yTick):
            glVertex(-x, 0.0, yi)
            glVertex(x, 0.0, yi)
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
        lighting = glGetBoolean(GL_LIGHTING)
        light0 = glGetBoolean(GL_LIGHT0)
        light1 = glGetBoolean(GL_LIGHT1)

        currentcolor = glGetFloatv(GL_CURRENT_COLOR)
        depth = glGetBoolean(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glLineWidth(1.0)

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

        width = glutGet(GLUT_WINDOW_WIDTH)
        height = glutGet(GLUT_WINDOW_HEIGHT)/2

        glColor(color)
        if x >= 0:
            positionX = x/width*2.0
        else:
            positionX = (width + x)/width*2.0

        if y >= 0:
            positionY = (y + 10.0)/height*2.0
        else:
            positionY = (height + y)/height*2.0

        glRasterPos3f(positionX, positionY, 0.0)
        for x in string:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(x))

        # glPopAttrib()
        # glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        # glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        if lighting:
            glEnable(GL_LIGHTING)
        if light0:
            glEnable(GL_LIGHT0)
        if light1:
            glEnable(GL_LIGHT1)
        if depth:
            glEnable(GL_DEPTH_TEST)
        glColor(currentcolor)

    def drawBlock(self, w, h, d):
        glPushMatrix()
        glScale(w/100, h/100, d/100 )
        glutSolidCube(100)
        glPopMatrix()

    def drawSquer(self, w, h):
        glPushMatrix()
        glBegin(GL_QUADS)
        glVertex(w, h, 0)
        glVertex(-w, h, 0)
        glVertex(-w, -h, 0)
        glVertex(w, -h, 0)
        glEnd()
        glPopMatrix()

    def setColor(self, color):
        glColor(color[0], color[1], color[2])
        glMaterial(GL_FRONT, GL_AMBIENT, color)
        glMaterial(GL_FRONT, GL_DIFFUSE, color)


if __name__ == '__main__':
    #print "Hit ESC key to quit."
    gl = GlutWrapper()
    gl.title = b"Tracer"
    gl.startFramework()
