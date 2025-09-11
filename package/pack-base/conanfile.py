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