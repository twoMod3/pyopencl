from __future__ import division, print_function, absolute_import

__copyright__ = "Copyright (C) 2018 Matt Wala"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np
import pytest

import pyopencl as cl
import pyopencl.cltypes as cltypes
import pyopencl.clrandom as clrandom
from pyopencl.tools import (  # noqa
        pytest_generate_tests_for_pyopencl
        as pytest_generate_tests)

try:
    import faulthandler
except ImportError:
    pass
else:
    faulthandler.enable()


class RanluxGeneratorShim(object):

    def __init__(self, cl_ctx):
        self.queue = cl.CommandQueue(cl_ctx)
        self.gen = clrandom.RanluxGenerator(self.queue)

    def uniform(self, *args, **kwargs):
        return self.gen.uniform(*args, **kwargs)

    def normal(self, *args, **kwargs):
        return self.gen.normal(*args, **kwargs)


@pytest.mark.parametrize("rng_class", [
    RanluxGeneratorShim,
    clrandom.PhiloxGenerator,
    clrandom.ThreefryGenerator])
@pytest.mark.parametrize("dtype", [
    np.int32,
    np.int64,
    np.float32,
    np.float64,
    cltypes.float2,
    cltypes.float3,
    cltypes.float4])
def test_clrandom_dtypes(ctx_factory, rng_class, dtype):
    cl_ctx = ctx_factory()
    rng = rng_class(cl_ctx)

    size = 10

    with cl.CommandQueue(cl_ctx) as queue:
        rng.uniform(queue, size, dtype)
        
        if dtype not in (np.int32, np.int64):
            rng.normal(queue, size, dtype)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        import py.test
        py.test.cmdline.main([__file__])
