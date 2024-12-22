'''OpenGL extension IBM.texture_mirrored_repeat

This module customises the behaviour of the 
OpenGL.raw.GL.IBM.texture_mirrored_repeat to provide a more 
Python-friendly API

Overview (from the spec)
	
	IBM_texture_mirrored_repeat extends the set of texture wrap modes to
	include a mode (GL_MIRRORED_REPEAT_IBM) that effectively uses a texture
	map twice as large at the original image in which the additional half of
	the new image is a mirror image of the original image.
	
	This new mode relaxes the need to generate images whose opposite edges
	match by using the original image to generate a matching "mirror image".

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/IBM/texture_mirrored_repeat.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.IBM.texture_mirrored_repeat import *
from OpenGL.raw.GL.IBM.texture_mirrored_repeat import _EXTENSION_NAME

def glInitTextureMirroredRepeatIBM():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION