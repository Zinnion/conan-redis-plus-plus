#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class RedisPlusPlusConan(ConanFile):
    name = "redis-plus-plus"
    version = "1.1.0"
    description = "Redis client written in C++"
    topics = ("conan", "redis")
    url = "https://github.com/zinnion/conan-redis-plus-plus"
    homepage = "https://github.com/sewenew/redis-plus-plus"
    author = "Zinnion <mauro@zinnion.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    short_paths = True
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    options = {
       "shared": [True, False]
    }

    default_options = (
        "shared=True"
    )

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        self.run("find . -name CMakeLists.txt | while read line;do sed -i '/add_subdirectory(test)/d' $line;done")

    def requirements(self):
        self.requires("hiredis/0.14.0@zinnion/stable")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_PREFIX_PATH'] = self.deps_cpp_info['hiredis'].rootpath
        cmake.definitions['HIREDIS_STATIC_LIB'] = self.deps_cpp_info['hiredis'].libs
        cmake.definitions['MAKE_BUILD_TYPE'] = 'Release'
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
