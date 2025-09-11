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
        board = "stm32f3_disco"
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