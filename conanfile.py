from conans import ConanFile, CMake, tools
import sys
import os


class glfw3Conan( ConanFile ):
    name = "glfw"
    version = "3.2"
    license = "zlib/libpng License"

    url = "https://github.com/GavinNL/conan_glfw"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source( self ):
        zip_name = "glfw-3.2.zip"
        tools.download("https://github.com/glfw/glfw/releases/download/3.2/glfw-3.2.zip", zip_name)    
        tools.unzip(zip_name)
        os.unlink(zip_name)
        tools.replace_in_file("glfw-3.2/CMakeLists.txt", "project(GLFW C)", """project(GLFW C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
        """)

    def config(self):
        # It is a pure C project, the libcxx setting is not relevant at all
        del self.settings.compiler.libcxx

    def system_requirements( self ):
        if self.settings.os == "Linux":
            self.run( 'sudo apt-get install xorg-dev' )
            self.run( 'sudo apt-get install libgl1-mesa-dev' )
            self.run( 'sudo apt-get install libglew-dev' )
        elif self.settings.os == "Macos":
            print( "  ***************** Need Help here **************** " )
            print( "  Mac OS not implemented yet. Please help out! **** " )
            print( "  ***************** Need Help here **************** " )
            sys.exit( 1 )

    def build( self ):  
        cmake = CMake( self.settings )
        
        args = ["-DBUILD_SHARED_LIBS=ON"  if self.options.shared else "-DBUILD_SHARED_LIBS=OFF"]
        args += ["-DGLFW_BUILD_DOCS=OFF" ]
        args += ["-DGLFW_BUILD_EXAMPLES=OFF" ]
        args += ["-DGLFW_BUILD_TESTS=OFF" ]
        args += ['-DCMAKE_INSTALL_PREFIX="%s"' % self.package_folder]
        
        self.run('cmake %s/glfw-3.2 %s %s'
                  % (self.conanfile_directory, cmake.command_line, ' '.join( args ) ) )
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package( self ): 
        # almost everything already installed in build, but dll
        self.copy("*.dll", "bin", "bin")
    
    def package_info( self ):
        if self.settings.os == "Linux":
            self.cpp_info.libs = [ "glfw3", "rt", "m" , "dl" , "Xrandr" , "Xinerama", "Xxf86vm" , 
                                  "Xext" , "Xcursor", "Xrender" , "Xfixes", "X11", "pthread", 
                                  "xcb" , "Xau", "Xdmcp", "GL", "GLEW" ]
        elif self.settings.os == "Windows":
            if self.options.shared:
                self.cpp_info.libs = [ "glfw3dll", "opengl32" ]
            else:
                self.cpp_info.libs = [ "glfw3", "opengl32" ]
        elif self.settings.os == "Macos":
            self.cpp_info.libs = [ "glfw3", "GL", "GLEW" ]


