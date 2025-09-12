 /*
  * SPDX-License-Identifier: MIT-0 OR Apache-2.0
  *
  * Copyright (c) 2025 Ignitarium Technologies & Solutions, Ltd.
  *
  * https://ignitarium.com/
  *
  * This source code is licensed under the MIT No Attribution License (MIT-0)
  * or the Apache License, Version 2.0, at your option.
  * You may not use this file except in compliance with one of these licenses.
  *
  * MIT-0 License: https://spdx.org/licenses/MIT-0.html
  * Apache-2.0 License: https://www.apache.org/licenses/LICENSE-2.0
  *
  */


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

    def requirements(self):
        self.requires("zephyr-sources/4.1.10@ign/stable-4.1")
        self.requires("zephyr-sdk/0.17.0@ign/stable-0.17.0")

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

        self.run(
            f"west build -p always -b stm32f3_disco -s {app_src} -d {app_build}",
            env="conanbuild"
        )

        if self.options.flash:
            self.output.into("Flashing the board................")
            self.run(f"west flah -d {app_build}")
