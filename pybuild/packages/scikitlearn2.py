from ..source import GitSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch

import os

class Scikitlearn2(Package):
    source = GitSource('https://github.com/AIPYX/scikit-learn.git', alias='scikit-learn2', branch='qpyc-0.20.0')
    patches = [
        #LocalPatch('0001-cross-compile'),
    ]

    def prepare(self):
        pass

    def build(self):
        PY_BRANCH = os.getenv('PY_BRANCH')
        PY_M_BRANCH = os.getenv('PY_M_BRANCH')
        BLD = os.path.join(os.getcwd(),'build/target')
        ANDROID_NDK = os.getenv("ANDROID_NDK")

        self.run([
            'python2',
            'setup.py',
            'build_ext',
            f'-I{BLD}/python{PY_BRANCH}/usr/include/python{PY_BRANCH}.{PY_M_BRANCH}'\
            f':{ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include'\
            f':{ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a/include'\
            f':{BLD}/openblas/usr/include',
            f'-L{BLD}/python{PY_BRANCH}/usr/lib'\
            f':{BLD}/openblas/usr/lib'\
            f':{ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a '\
            f':{ANDROID_NDK}/toolchains/renderscript/prebuilt/linux-x86_64/platform/arm'\
            f':{ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/lib/gcc/arm-linux-androideabi/4.9.x/armv7-a',
            f'-lpython{PY_BRANCH}.{PY_M_BRANCH},m',
        ])
        self.run([
            'python2',
            'setup.py',
            'build_py',
        ])
        self.run([
            'python2',
            'setup.py',
            'install',
            '--root',
            f'{BLD}/python{PY_BRANCH}',
        ])
