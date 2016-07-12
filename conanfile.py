from conans import ConanFile, CMake, tools
import sys
import os


class glfw3Conan(ConanFile):
	name    = "glfw"
	version = "3.2"
	license = "zlib/libpng License"

	url = "https://github.com/GavinNL/conan_glfw"

	options = { "shared"            : [True, False] 
		      }

	default_options = "shared=False"

	settings = "os", "compiler", "build_type", "arch"


	def source(self):

		if self.settings.os == "Windows":

			if self.settings.arch == "x86":
				zip_name = "glfw-3.2.bin.WIN32.zip" 
				tools.download("https://github.com/glfw/glfw/releases/download/3.2/glfw-3.2.bin.WIN32.zip", zip_name)
			else:
				zip_name = "glfw-3.2.bin.WIN64.zip"
				tools.download("https://github.com/glfw/glfw/releases/download/3.2/glfw-3.2.bin.WIN64.zip", zip_name)

		else:

			zip_name = "glfw-3.2.zip"
			tools.download("https://github.com/glfw/glfw/releases/download/3.2/glfw-3.2.zip", zip_name)

		tools.unzip(zip_name)
		os.unlink(zip_name)
          

	def system_requirements(self):

		if self.settings.os == "Linux":

			self.run('sudo apt-get install xorg-dev')        
			self.run('sudo apt-get install libgl1-mesa-dev')
			self.run('sudo apt-get install libglew-dev')

		elif self.settings.os == "Macos":
			print("  ***************** Need Help here **************** ")
			print("  Mac OS not implemented yet. Please help out! **** ")
			print("  ***************** Need Help here **************** ")
			sys.exit(1)

		# No requirements for windows since we are using the prepackaged binaries provided by the developers


	def build(self):

		if self.settings.os == "Linux":

			cmake = CMake(self.settings)

			args  = ["-DBUILD_SHARED_LIBS=ON"    if self.options.shared           else "-DBUILD_SHARED_LIBS=OFF"]
			args += ["-DGLFW_BUILD_DOCS=OFF" ]
			args += ["-DGLFW_BUILD_EXAMPLES=OFF" ]
			args += ["-DGLFW_BUILD_TESTS=OFF" ]
			args += ['-DCMAKE_INSTALL_PREFIX=install']

			self.run('cd %s' % self.conanfile_directory )
			self.run('cmake %s/glfw-3.2 %s %s' % ( self.conanfile_directory, cmake.command_line, ' '.join(args) ) )
			self.run("cmake --build . --target install %s" % cmake.build_config )
			self.run("echo cmake --build . --target install %s" % cmake.build_config )


			if self.settings.arch == "x86":
				folder = "glfw-3.2.bin.WIN32"
			else:
				folder = "glfw-3.2.bin.WIN64"


	def package(self):

		# If we are on windows, just download the binary provided by the dev team
		# rather than compiling it ourself, they provide binaries for mingw, VC11, VC12 and VC14
		if self.settings.os == "Windows":

			if self.settings.arch == "x86":
				folder = "glfw-3.2.bin.WIN32"
			else:
				folder = "glfw-3.2.bin.WIN64"

			self.copy("*",     dst="include", src="%s/include"%folder)

			if self.settings.compiler == "gcc" : 

				if self.settings.arch == "x86":
					LibDir = "%s/lib-mingw"%folder
				else:
					LibDir = "%s/lib-mingw-w64"%folder

				if self.options.shared:
					self.copy("libglfw3dll.a",     dst="lib",     src=LibDir )
					self.copy("glfw3.dll",         dst="lib",     src=LibDir )				           
				else:
					self.copy("libglfw3.a",           dst="lib",     src=LibDir )


			elif self.settings.compiler == "Visual Studio":

				v = self.settings.compiler.version

				if v == "14":				
					LibDir = "%s/lib-vc2015" % folder
				elif v == "12":
					LibDir = "%s/lib-vc2013" % folder
				elif v == "11":
					LibDir = "%s/lib-vc2012" % folder

				if self.options.shared:
					self.copy("glfw3dll.lib",     dst="lib",     src=LibDir)
					self.copy("glfw3.dll",        dst="lib",     src=LibDir)
				else:
					self.copy("glfw3.lib",        dst="lib",     src=LibDir)

		else:
			self.copy("*",     dst="include", src="install/include")
			self.copy("*",     dst="lib",     src="install/lib")
			self.copy("*",     dst="bin",     src="install/bin")

	def package_info(self):
		if self.settings.os == "Linux":
			self.cpp_info.libs = [ "glfw3", "rt", "m" ,"dl" ,"Xrandr" ,"Xinerama", "Xxf86vm" ,"Xext" ,"Xcursor", "Xrender" ,"Xfixes", "X11", "pthread", "xcb" ,"Xau", "Xdmcp", "GL", "GLEW" ]
		elif self.settings.os == "Windows":
			self.cpp_info.libs = [ "glfw3", "GL", "GLEW" ]

		elif self.settings.os == "Macos":
			self.cpp_info.libs = [ "glfw3", "GL", "GLEW" ]


