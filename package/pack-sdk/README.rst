
Zephyr SDK Conan Package
========================

This provides a Conan package for the `Zephyr SDK` version 0.17.0. using the altconanfile.py
Replace the already avilable ``conanfile.py`` with ``altconanfile.py``. ie, you need to copy the code inside ``altconanfile.py`` to ``conanfile.py``

Steps to Package Zephyr SDK with Conan
--------------------------------------

1. Download Zephyr SDK
~~~~~~~~~~~~~~~~~~~~~~

Download the SDK for your OS from the official Zephyr GitHub releases page:

`Zephyr SDK Releases <https://github.com/zephyrproject-rtos/sdk-ng/releases/tag/v0.17.0>`_

- **Linux (x86_64):**

.. code-block:: bash

   wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.0/zephyr-sdk-0.17.0_linux-x86_64.tar.xz

- **Windows (x86_64):**

Download ``zephyr-sdk-0.17.0_windows-x86_64.zip``

- **macOS (x86_64 or arm64):**

Download the matching tarball.

2. Extract the SDK
~~~~~~~~~~~~~~~~~~

Example for Linux:

.. code-block:: bash

   tar -xf zephyr-sdk-0.17.0_linux-x86_64.tar.xz

This will create a folder named:

::

   zephyr-sdk-0.17.0/

3. Prepare Conan Package
~~~~~~~~~~~~~~~~~~~~~~~~

Make sure that you've ``conanfile.py`` in the same directory where the extracted SDK folder lives:

::

   pack-sdk/
    ├─ conanfile.py
    └─ zephyr-sdk-0.17.0/

4. Create Package with Conan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the Conan create command:

.. code-block:: bash

   conan create .

- This will package the local ``zephyr-sdk-0.17.0`` into Conan.
- The package will also define ``ZEPHYR_SDK_INSTALL_DIR`` as an environment variable when consumed.

5. Test the Package
~~~~~~~~~~~~~~~~~~~

After creating, you can check it with:

.. code-block:: bash

   conan list zephyr-sdk

To use in another project’s ``conanfile.py``:

.. code-block:: python

   requires = "zephyr-sdk/0.17.0"

When consuming, the environment variable will be available:

.. code-block:: bash

   echo $ZEPHYR_SDK_INSTALL_DIR

6. Cleanup (Optional)
~~~~~~~~~~~~~~~~~~~~~

You can safely remove the original extracted ``zephyr-sdk-0.17.0`` folder after packaging:

.. code-block:: bash

   rm -rf zephyr-sdk-0.17.0
