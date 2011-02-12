import Options, glob
from os.path import join, dirname, abspath, exists
from shutil import copy, rmtree
from os import unlink
import sys, os

srcdir = "."
blddir = "build"
VERSION = "0.0.1"

def set_options(opt):
  opt.tool_options("compiler_cxx")
  opt.tool_options("compiler_cc")

def configure(conf):
  conf.check_tool("compiler_cxx")
  conf.check_tool("compiler_cc")
  conf.check_tool("node_addon")
  
  
  conf.check_tool("irrklang")


def clean(ctx): 
  if exists("lib/node-irrklang.node"): unlink("lib/node-irrklang.node")
  if exists("build"): rmtree("build")

  # TODO: add support for more platforms..
  buildpath = abspath("build/default")
  cmd = "cd \"deps/glfw\" && PREFIX=%s make cocoa-clean"
  if os.system(cmd % (buildpath)) != 0:
    conf.fatal("Building glfw failed.")
  

def build(bld):
  node_ogl = bld.new_task_gen("cxx", "shlib", "node_addon")
  node_ogl.source = bld.glob("src/*.cc")
  node_ogl.name = "node-irrklang"
  node_ogl.target = "node-irrklang"
  node_ogl.uselib = ["irrklang"]
  bld.add_post_fun(copynode)

def copynode(ctx):
  if exists('build/default/node-irrklang.node'):
    copy('build/default/node-irrklang.node','lib/node-irrklang.node')

def test(tst):
  os.system("node test/sanity.js")
