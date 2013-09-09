from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from math import *

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
        self.windowHeigth = 480
        self.windowPositionX = 100
        self.windowPositionY = 100
        self.title = "Glut Wrapper"
        self.camera = Camera()
        self.mouseState = MouseState()

    def startFramework(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
        glutInitWindowPosition(self.windowPositionX, self.windowPositionY)
        glutInitWindowSize(self.windowWidth, self.windowHeigth)
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
        deltaTime = 0.1
        self.display(deltaTime)

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

    # User overwite ---------------------------------------
    def display(self, deltaTime):
        glMaterial(GL_FRONT, GL_AMBIENT, (0.8, 0.6, 0.5, 1.0))
        glMaterial(GL_FRONT, GL_DIFFUSE, (0.8, 0.6, 0.5, 1.0))
        glutSolidTeapot(50)

    def idle(self):
        # TODO: FPS
        glutPostRedisplay()

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
        print "MousePress: button: %d, x: %d, y:%d" % (button, x, y)

    def motion(self, x, y):
        print "MouseMove: x: %d, y: %d" % (x, y)

    def passiveMotion(self, x, y):
        self.mouseState.x = x
        self.mouseState.y = y

    def keyboard(self, key, x, y):
        print "KeyboardPress: %c" % key
        if key == ESCAPE:
            sys.exit()

    def keyboardUp(self, key, x, y):
        print "KeyboardUp: %c" % key

    def special(self, key, x, y):
        print "SpecialKeyPress: %c" % key

    def specialUp(self, key, x, y):
        print "SpecialKeyUp: %c" % key


if __name__ == '__main__':
    print "Hit ESC key to quit."
    gl = GlutWrapper()
    gl.title = "Tracer"
    gl.startFramework()
