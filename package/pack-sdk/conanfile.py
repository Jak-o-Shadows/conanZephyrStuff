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
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get
from pathlib import Path
 
 
class LocalZephyrSdkConan(ConanFile):
    name = "zephyr-sdk"
    version = "0.17.0"
    package_type = "application"
    settings = "os", "arch"
 
    def _sdk_info(self):
        """Return url for the given OS/arch combo."""
        base_url = f"https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v{self.version}"
        os = str(self.settings.os).lower()
        arch = str(self.settings.arch).lower()
 
        if os == "linux" and arch == "x86_64":
            return f"{base_url}/zephyr-sdk-{self.version}_linux-x86_64.tar.xz"
        elif os == "windows" and arch == "x86_64":
            return f"{base_url}/zephyr-sdk-{self.version}_windows-x86_64.zip"
        elif os in ("macos", "darwin") and arch == "x86_64":
            return f"{base_url}/zephyr-sdk-{self.version}_macos-x86_64.tar.xz"
        elif os in ("macos", "darwin") and arch in ("armv8", "aarch64"):
            return f"{base_url}/zephyr-sdk-{self.version}_macos-aarch64.tar.xz"
        else:
            raise ConanInvalidConfiguration(f"No Zephyr SDK binary for {os}-{arch}")
 
    def build(self):
        url = self._sdk_info()
        # strip_root=True removes the top-level zephyr-sdk-* folder
        get(self, url=url, strip_root=True)
 
    def package(self):
        sdk_src = Path(self.build_folder) / f"zephyr-sdk-{self.version}"
        copy(self, pattern="*", src=sdk_src, dst=self.package_folder)
 
    def package_info(self):
        self.buildenv_info.define(
            "ZEPHYR_SDK_INSTALL_DIR",
            str(Path(self.package_folder) / f"zephyr-sdk-{self.version}")
        )
