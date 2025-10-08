 # SPDX-License-Identifier: MIT-0 OR Apache-2.0
 #
 # Copyright (c) 2025 Ignitarium Technologies & Solutions, Ltd.
 #
 # https://ignitarium.com/
 #
 # This source code is licensed under the MIT No Attribution License (MIT-0)
 # or the Apache License, Version 2.0, at your option.
 # You may not use this file except in compliance with one of these licenses.
 #
 # MIT-0 License: https://spdx.org/licenses/MIT-0.html
 # Apache-2.0 License: https://www.apache.org/licenses/LICENSE-2.0


from conan import ConanFile
from conan.tools.files import copy
from conan.tools.env import Environment
from conan.tools.cmake import CMakeDeps, CMakeToolchain
from pathlib import Path

class ZephyrApp(ConanFile):
    name = "zephyr-app"
    version = "0.1"
    package_type = "application"

    settings = "os", "arch", "build_type"
    options = {
        "flash" : [True, False],
        "pristine" : [True, False]
    }
    default_options = {
        "flash" : False,
        "pristine" : False
    }
    exports_sources = "*"  # TODO: Be more explicit here

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.22]")
        self.tool_requires("ninja/[>=1.10]")
        self.build_requires("openocd/0.12.0")

    def requirements(self):
        self.requires("zephyr-sources/4.2.1")
        self.requires("zephyr-sdk/0.17.4")
        self.requires("hfsm2/2.5.2")

    def layout(self):
        self.folders.source = ""
        self.folders.build = "build"
        self.folders.generators = "build/generators"

    def generate(self):
        sdk_path = self.dependencies["zephyr-sdk"].package_folder.replace("\\", "/")
        zephyr_path = Path(self.dependencies["zephyr-sources"].package_folder).as_posix() + "/zephyr"

        env = Environment()
        env.define("ZEPHYR_SDK_INSTALL_DIR", sdk_path)
        env.define("ZEPHYR_BASE", zephyr_path)
        env.vars(self).save_script("zephyr_env")
        
        # Generate CMake integration files
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        app_src = Path(self.source_folder)
        app_build = Path(self.build_folder) / "zephyr_build"
        board = "stm32_min_dev@blue"
        filepath_toolchain_file = Path(self.generators_folder) / "conan_toolchain.cmake"

        # Allow west to do a pristine build
        if self.options.pristine:
            pristine = "-p always"
        else:
            pristine = ""

        self.run(
            # Use CMAKE_PROJECT_TOP_LEVEL_INCLUDES to inject Conan's configuration
            f"west build -b {board} -s {app_src} -d {app_build} {pristine} -- -DCMAKE_BUILD_TYPE={self.settings.build_type} -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES='{filepath_toolchain_file.as_posix()}'",
            env="conanbuild"
        )
        
        if self.options.flash:
            self.output.info("Flashing the board...")
            self.run(f"west flash -d {app_build}")
