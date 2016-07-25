from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "GavinNL")

class GLFWTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "glfw/3.2@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "lib")

    def test(self):
        os.chdir("bin")
        if not os.path.exists("glfw_test%s" % (".exe" if self.settings.os=="Windows" else "")):
            raise Exception("Example glfw_test not found!")
        try:
            self.run(".%sglfw_test" % os.sep)
        except Exception as e:
            self.output.warn("Unable to run glfw test, normal if running in CI\n%s" % str(e))
