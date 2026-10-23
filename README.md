# conan-with-zephyr-RTOS



## Build System

Due to the large file size of the Zephyr sources, the GitHub Actions CI has been split into each Conan package. These are stored in Github releases, enabling a consumer to just grab them and use them locally.

As such, they are staged, with the Zephyr Sources being required for the Zephyr Base.