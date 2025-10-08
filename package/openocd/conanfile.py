# Licensed under the LGPL-2.1-or-later license.


from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get
from pathlib import Path
import os

class OpenOCDConan(ConanFile):
    name = "openocd"
    version = "0.12.0"
    package_type = "application"
    settings = "os", "arch"
    exports_sources = "conandata.yml"

    def build(self):
        source_info = self.conan_data["sources"][self.version][0]  # TODO: Support other OS/arch
        get(self, **source_info)

    def package(self):
        copy(self, pattern="*", src=os.path.join(self.build_folder), dst=self.package_folder)

    def package_info(self):
        # Add the 'bin' directory of the package to the PATH
        bin_folder = str(Path(self.package_folder) / "bin")
        self.buildenv_info.append_path("PATH", bin_folder)

        # For consumers that need the path to the openocd executable
        openocd_exe = "openocd.exe" if self.settings.os == "Windows" else "openocd"
        self.runenv_info.define("OPENOCD_PATH", str(Path(bin_folder) / openocd_exe))
