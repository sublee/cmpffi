# -*- coding: utf-8 -*-
"""
    cmpffi
    ~~~~~~

    `cmp <https://github.com/camgunz/cmp>`_ for Python.

"""
import os
import re

from cffi import FFI


__version__ = '0.0.0-dev'
__all__ = ['MsgPack', 'init_context', 'libcmp', 'ffi']


CMP_DIR = os.path.join(os.path.dirname(__file__), 'cmp')


ffi = FFI()
with open(os.path.join(CMP_DIR, 'cmp.h')) as f:
    ffi.cdef(re.sub('(^#.*|.*extern.*)', '', f.read(), flags=re.MULTILINE))
libcmp = ffi.verify(r'''
#include <stdbool.h>
#include <cmp.h>
''', sources=[os.path.join(CMP_DIR, 'cmp.c')], include_dirs=[CMP_DIR])


@ffi.callback('bool(cmp_ctx_t *, void *, size_t)')
def read(ctx, data, limit):
    buf = ffi.from_handle(ctx.buf)
    ffi.buffer(data, limit)[:] = buf.read(limit)
    return True


@ffi.callback('size_t(cmp_ctx_t *, void *, size_t)')
def write(ctx, data, count):
    buf = ffi.from_handle(ctx.buf)
    data_to_write = ffi.buffer(ffi.cast('char *', data), count)
    return buf.write(data_to_write)


def make_writer(c_func):
    def func(self, data):
        return c_func(self.ctx, data)
    return func


def make_str_writer(c_func, is_str=True):
    def func(self, data):
        if is_str:
            data = data.encode('utf-8')
        size = len(data)
        return c_func(self.ctx, data, size)
    return func


def make_reader(c_func, c_type):
    def func(self):
        data_ptr = ffi.new(c_type + '*')
        c_func(self.ctx, data_ptr)
        return data_ptr[0]
    return func


def make_str_reader(c_func, is_str=True):
    def func(self):
        raise NotImplementedError
    return func


def init_context(buf):
    """Creates a new CMP context."""
    ctx = ffi.new('cmp_ctx_t *')
    libcmp.cmp_init(ctx, ffi.new_handle(buf), read, write)
    return ctx


class MsgPack(object):

    def __init__(self, buf):
        self.buf = buf
        self.ctx = init_context(buf)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.buf)

    # writers

    write_int = make_writer(libcmp.cmp_write_sint)
    write_uint = make_writer(libcmp.cmp_write_uint)
    write_float = make_writer(libcmp.cmp_write_float)
    write_double = make_writer(libcmp.cmp_write_double)
    write_bool = make_writer(libcmp.cmp_write_bool)
    write_nil = make_writer(libcmp.cmp_write_nil)
    write_array_size = make_writer(libcmp.cmp_write_array)
    write_map_size = make_writer(libcmp.cmp_write_map)
    write_str = make_str_writer(libcmp.cmp_write_str, is_str=True)
    write_bin = make_str_writer(libcmp.cmp_write_bin, is_str=False)
    def write_ext(self, type, data):
        size = len(data)
        return libcmp.cmp_write_ext(self.ctx, type, size, data)

    # readers

    read_int = make_reader(libcmp.cmp_read_sinteger, 'int64_t')
    read_uint = make_reader(libcmp.cmp_read_sinteger, 'uint64_t')
    read_float = make_reader(libcmp.cmp_read_float, 'float')
    read_double = make_reader(libcmp.cmp_read_float, 'double')
    read_bool = make_reader(libcmp.cmp_read_bool, 'bool')
    def read_nil(self):
        libcmp.cmp_read_nil(self.ctx)
    read_array_size = make_reader(libcmp.cmp_read_array, 'uint32_t')
    read_map_size = make_reader(libcmp.cmp_read_map, 'uint32_t')
    read_str = make_str_reader(libcmp.cmp_read_str, is_str=True)
    read_bin = make_str_reader(libcmp.cmp_read_bin, is_str=False)
    def read_ext(self, type, data):
        raise NotImplementedError
