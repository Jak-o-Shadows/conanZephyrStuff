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
from pathlib import Path

class ZephyrApp(ConanFile):
    name = "zephyr-app"
    version = "0.1"
    package_type = "application"

    settings = "os", "arch"
    options = {
        "flash" : [True, False]
    }
    default_options = {
        "flash" : False
    }
    exports_sources = "*"

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.22]")
        self.tool_requires("ninja/[>=1.10]")

    def requirements(self):
        self.requires("zephyr-sources/4.2.10@ign/stable-4.2.1")
        self.requires("zephyr-sdk/0.17.4@ign/stable-0.17.4")

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

    def build(self):
        app_src = Path(self.source_folder)
        app_build = Path(self.build_folder) / "zephyr_build"
        board = "stm32_min_dev@blue/stm32f103xb"
        board_revision = ""
        zephyr_path = Path(self.dependencies["zephyr-sources"].package_folder).as_posix() + "/zephyr"
        zephyr_modules = zephyr_path.parents[0]
        zephyr_stm_modules = f"{zephyr_modules}/modules/hal/stm32;{zephyr_modules}/modules/hal/cmsis"
        print(zephyr_stm_modules)
        cmake_cmd = f'cmake -B {app_build} -S {app_src} -DBOARD={board} -DZEPHYR_MODULES={zephyr_stm_modules} -GNinja'

        self.run(
            cmake_cmd,
            env="conanbuild"
        )

        build_cmd = f'ninja -C {app_build}'
        self.run(
            build_cmd,
            env="conanbuild"
        )
