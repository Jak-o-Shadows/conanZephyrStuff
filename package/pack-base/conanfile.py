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
from conan.tools.files import copy, chdir, rmdir
from pathlib import Path
 
 
class ZephyrSourcesConan(ConanFile):
    name = "zephyr-sources"
    version = "4.1.10"
    package_type = "application"
    settings = "os", "arch"
 
    def layout(self):
        self.folders.source = "."
        self.folders.build = "build"
        self.folders.generators = "build/generators"
 
    def source(self):
        data = self.conan_data["sources"][self.version]
        url = data["url"]
        branch = data["branch"]
 
        repo_path = Path(self.source_folder) / "zephyr"
 
        # progress-enabled git clone
        self.run(f"git clone --progress --branch {branch} {url} {repo_path}")
 
    def build(self):
        zephyr_path = Path(self.source_folder) / "zephyr"
        self.run(f"west init -l {zephyr_path}", cwd=self.source_folder)
        self.run("west update", cwd=self.source_folder)
 
    def package(self):
        copy(self, pattern="*", src=self.source_folder, dst=self.package_folder)
        rmdir(self, Path(self.package_folder) / ".git")   # optional cleanup
 
    def package_info(self):
        self.buildenv_info.define(
            "ZEPHYR_BASE", str(Path(self.package_folder) / "zephyr")
        )
