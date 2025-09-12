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
from pathlib import Path
 
 
class LocalZephyrSdkConan(ConanFile):
    name = "zephyr-sdk"
    version = "0.17.0"
    package_type = "application"
    settings = "os", "arch"
 
    exports_sources = "zephyr-sdk-0.17.0/*"
 
    def package(self):
        sdk_src = Path(self.source_folder) / "zephyr-sdk-0.17.0"
        copy(self, pattern="*", src=sdk_src, dst=self.package_folder)
 
    def package_info(self):
        self.buildenv_info.define(
            "ZEPHYR_SDK_INSTALL_DIR",
            str(Path(self.package_folder) / "zephyr-sdk-0.17.0")
        )
