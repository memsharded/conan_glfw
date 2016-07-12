# Conan file for the GLFW library.

Was only able to test this on linux: Linux Mint 18.

On linux, this will download the source and compile it

On Windows, it will *hopefully* download the binaries provided by the dev team.

No implementation for MacoOS. I do not have a Mac so I have no idea how to compile stuff on it.

# Please submit pull requests if you can improve this.



# Compiling/Testing instructions On Linux

cd to the directory that contains conanfile.py

conan export GavinNL/testing

conan install glfw/3.2@GavinNL/testing --build

cd test

mkdir build

cd build

conan install ..

cmake ..

make

cd bin

./glfw_test

