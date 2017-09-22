import cv2
from OpenGL.GL import *
from OpenGL.GLU import *

class OculusDrawerCompatibility(object):

    def __init__(self, cap):
        self.cap = cap
    
    def init_gl(self):
        self.tex = glGenTextures(1)

        _, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, TEX_WIDTH, 0, TEX_HEIGHT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
       
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, TEX_WIDTH, TEX_HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
 
    def idle_gl(self):
        _, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def display_gl(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, TEX_WIDTH, 0, TEX_HEIGHT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def resize_gl(self, w, h):
        pass
    
    def dispose_gl(self):
        pass



class EyeLeft(OculusDrawerCompatibility):

    def __init__(self, cap):
        super(EyeLeft, self).__init__(cap)

    def init_gl(self):
        super(EyeLeft, self).init_gl()

    def idle_gl(self):
        image = super(EyeLeft, self).idle_gl()

        # LEFT texture
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, TEX_WIDTH, TEX_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, image)

    def display_gl(self):
        super(EyeLeft, self).display_gl()
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glEnable(GL_TEXTURE_2D)

        glPushMatrix()
        glBegin(GL_QUADS)
        glColor3f(1, 0, 0)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, TEX_HEIGHT)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(TEX_WIDTH, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(TEX_WIDTH, TEX_HEIGHT)
        glEnd()
        glPopMatrix()
        
        glFlush()
        glutSwapBuffers()


class EyeRight(OculusDrawerCompatibility):
    
    def __init__(self, cap):
        super(EyeRight, self).__init__(cap)

    def init_gl(self):
        super(EyeRight, self).init_gl()

    def idle_gl(self):
        image = super(EyeRight, self).idle_gl()

        # RIGHT texture
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, TEX_WIDTH, TEX_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, image)

    def display_gl(self):
        super(EyeRight, self).display_gl()
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glEnable(GL_TEXTURE_2D)

        glPushMatrix()
        glBegin(GL_QUADS)
        glColor3f(0, 1, 0)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, TEX_HEIGHT)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(TEX_WIDTH, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(TEX_WIDTH, TEX_HEIGHT)
        glEnd()
        glPopMatrix()

        glFlush()
 
class OculusRenderer():
    def __init__(self, caps):
        self.caps = caps
        self.tex = -1

    def _concat_image(self):
        _, left = self.caps[LEFT].read()
        _, right = self.caps[RIGHT].read()
        
        image = cv2.hconcat(left, right)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
    
    def init_gl(self):
        self.tex = glGenTextures(1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, TEX_WIDTH, 0, TEX_HEIGHT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        image = self._concat_image()
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, TEX_WIDTH, TEX_HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    
    def idle_gl(self):
        image = self._concat_image() 
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, TEX_WIDTH, TEX_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, image)

    def display_gl(self):
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        """

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, TEX_WIDTH, 0, TEX_HEIGHT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glEnable(GL_TEXTURE_2D)
        
        glBegin(GL_QUADS)
        #glColor3f(1, 0, 0)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, TEX_HEIGHT)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(TEX_WIDTH, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(TEX_WIDTH, TEX_HEIGHT)
        glEnd()

        glFlush()
        glutSwapBuffers()

    def dispose_gl(self):
        pass
