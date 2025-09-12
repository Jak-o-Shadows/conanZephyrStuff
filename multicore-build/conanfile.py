 # SPDX-License-Identifier: MIT-0 OR Apache-2.0
 #
 # Copyright (c) 2025 Ignitarium Technology Solutions Pvt Ltd
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
from conan.tools.env import VirtualBuildEnv, Environment
from pathlib import Path
 
class MultiCoreZephyrApp(ConanFile):
    name = "multi-core-zephyr"
    version = "0.1"
    package_type = "application"
 
    settings = "os", "arch"
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
 
        # Setup virtual build environment
        env = Environment()
        env.define("ZEPHYR_SDK_INSTALL_DIR", sdk_path)
        env.define("ZEPHYR_BASE", zephyr_path)
        envvars = env.vars(self)
        envvars.save_script("zephyr_env")
 
    def build(self):
        # --------- Core 0 Build ----------
        core0_src = Path(self.source_folder) / "core0/blinky"
        core0_build = Path(self.build_folder) / "core0_build"
        
        self.run(
                    f"west build -p always -b stm32f3_disco -s {core0_src} -d {core0_build}",
                    env="conanbuild"
                )
        
        # --------- Core 1 Build ----------
        core1_src = Path(self.source_folder) / "core1/blinky"
        core1_build = Path(self.build_folder) / "core1_build"
                
        self.run(
                    f"west build -p always -b stm32f3_disco -s {core1_src} -d {core1_build}",
                    env="conanbuild"
                )
        
        # Copy both built zephyr.elf files into the final package
        copy(
            self,
            "zephyr.elf",
            src=str(Path(self.build_folder) / "core0_build" / "zephyr"),
            dst=str(Path(self.source_folder) / "out" / "core0"),
            keep_path=False
        )

        copy(
            self,
            "zephyr.elf",
            src=str(Path(self.build_folder) / "core1_build" / "zephyr"),
            dst=str(Path(self.source_folder) / "out" / "core1"),
            keep_path=False
        )
