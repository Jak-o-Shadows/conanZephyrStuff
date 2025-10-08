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
import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, chdir, download, unzip
from pathlib import Path
 
 
class LocalZephyrSdkConan(ConanFile):
    name = "zephyr-sdk"
    version = "0.17.4"
    package_type = "application"
    settings = "os", "arch"

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.tool_requires("7zip/[>=19.00]")
 
    def _sdk_info(self):
        """Return url for the given OS/arch combo."""
        base_url = f"https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v{self.version}"
        os = str(self.settings.os).lower()
        arch = str(self.settings.arch).lower()
 
        if os == "linux" and arch == "x86_64":
            return f"{base_url}/zephyr-sdk-{self.version}_linux-x86_64.tar.xz"
        elif os == "windows" and arch == "x86_64":
            return f"{base_url}/zephyr-sdk-{self.version}_windows-x86_64.7z"
        elif os in ("macos", "darwin") and arch == "x86_64":
            return f"{base_url}/zephyr-sdk-{self.version}_macos-x86_64.tar.xz"
        elif os in ("macos", "darwin") and arch in ("armv8", "aarch64"):
            return f"{base_url}/zephyr-sdk-{self.version}_macos-aarch64.tar.xz"
        else:
            raise ConanInvalidConfiguration(f"No Zephyr SDK binary for {os}-{arch}")
 
    def build(self):
        url = self._sdk_info()
        filename = url.split("/")[-1]
        dir_out = os.path.join(self.build_folder, "zephyr")
        os.makedirs(dir_out, exist_ok=True)

        download(self, url=url, filename=filename)

        if self.settings.os == "Windows":
            # Explicitly extract the .7z file using the 7zip tool_requires
            self.run(f'7z x "{filename}" -o"{dir_out}"')
        else:
            # For other OSes, use the robust unzip() which handles .tar.xz
            unzip(self, filename, self.build_folder, strip_root=True)
 
    def package(self):
        # If the source directory exists, copy its contents.
        src = os.path.join(self.build_folder, "zephyr")
        copy(self, pattern="*", src=src, dst=self.package_folder)
 
    def package_info(self):
        self.buildenv_info.define("ZEPHYR_SDK_INSTALL_DIR", self.package_folder)
