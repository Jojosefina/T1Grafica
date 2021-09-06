import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4

def crear_dama(x,y,r,g,b,radius):
    
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+np.cos(np.radians(angle))*radius, 
                       y+np.sin(np.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+np.cos(np.radians(angle+10))*radius, 
                       y+np.sin(np.radians(angle+10))*radius, 
                       0.0, r, g, b])
    
    return np.array(circle, dtype = np.float32)

def crear_tablero():

    #Fondo blanco del tablero
    Fondo = np.array([
    #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 1.0, 1.0,
         0.5, -0.5, 0.0,  1.0, 1.0, 1.0,
         0.5,  0.5, 0.0,  1.0, 1.0, 1.0,
        -0.5,  0.5, 0.0,  1.0, 1.0, 1.0
    # It is important to use 32 bits data
        ], dtype = np.float32)
    
    #Cuadraditos negros

    CuadNeg = np.array([
    #   positions        colors
        -0.125, 0.375, 0.0,  0.0, 0.0, 0.0,
         0.0, 0.375, 0.0,  0.0, 0.0, 0.0,
         0.0,  0.5, 0.0,  0.0, 0.0, 0.0,
        -0.125,  0.5, 0.0,  0.0, 0.0, 0.0
    # It is important to use 32 bits data
        ], dtype = np.float32)

   # contador = 0 # Debe llegar a 32 (cuadrados negros)
    #while contador != 32:
         
    return np.array()


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea 1", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    #########################################################
    dama = crear_dama(0.5,0.0, 0.0, 1.0, 0.0, 0.2)
    tablero = crear_tablero()

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # Each shape must be attached to a Vertex Buffer Object (VBO)
    vboDama = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    glBufferData(GL_ARRAY_BUFFER, len(dama) * SIZE_IN_BYTES, dama, GL_STATIC_DRAW)


    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.5,0.5, 0.5, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)

    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    
    
    # It renders a scene using the active shader program (pipeline) and the active VAO (shapes)
    glDrawArrays(GL_TRIANGLES, 0, int(len(dama)/6))


    # Moving our draw to the active color buffer
    glfw.swap_buffers(window)

    # Waiting to close the window
    while not glfw.window_should_close(window):

        # Getting events from GLFW
        glfw.poll_events()
        
    glfw.terminate()