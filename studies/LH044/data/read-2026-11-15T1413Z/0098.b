<!DOCTYPE html>

<html lang="en" data-content_root="../">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta property="og:title" content="os — Miscellaneous operating system interfaces" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://docs.python.org/3/library/os.html" />
<meta property="og:site_name" content="Python documentation" />
<meta property="og:description" content="Source code: Lib/os.py This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, s..." />
<meta property="og:image:width" content="1146" />
<meta property="og:image:height" content="600" />
<meta property="og:image" content="https://docs.python.org/3.15/_images/social_previews/summary_library_os_900ce1c0.png" />
<meta property="og:image:alt" content="Source code: Lib/os.py This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, s..." />
<meta name="description" content="Source code: Lib/os.py This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, s..." />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#3776ab">

    <title>os — Miscellaneous operating system interfaces &#8212; Python 3.15.2 documentation</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link rel="stylesheet" type="text/css" href="../_static/pygments.css?v=b86133f3" />
    <link id="pygments_dark_css" media="(prefers-color-scheme: dark)" rel="stylesheet" type="text/css" href="../_static/pygments_dark.css?v=0fc419ee" />
    <link rel="stylesheet" type="text/css" href="../_static/classic.css?v=234b1a7c" />
    <link rel="stylesheet" type="text/css" href="../_static/pydoctheme.css?v=48df1187" />
    
    <script src="../_static/documentation_options.js?v=c6788839"></script>
    <script src="../_static/doctools.js?v=fd6eb6e6"></script>
    <script src="../_static/sphinx_highlight.js?v=6ffebe34"></script>
    
    <script src="../_static/sidebar.js"></script>
    
    <link rel="search" type="application/opensearchdescription+xml"
          title="Search within Python 3.15.2 documentation"
          href="../_static/opensearch.xml"/>
    <link rel="author" title="About these documents" href="../about.html" />
    <link rel="index" title="Index" href="../genindex.html" />
    <link rel="search" title="Search" href="../search.html" />
    <link rel="copyright" title="Copyright" href="../copyright.html" />
    <link rel="next" title="io — Core tools for working with streams" href="io.html" />
    <link rel="prev" title="Generic Operating System Services" href="allos.html" />
    
      
      <script defer file-types="bz2,epub,zip" data-domain="docs.python.org" src="https://analytics.python.org/js/script.file-downloads.outbound-links.js"></script>
      
      <link rel="canonical" href="https://docs.python.org/3/library/os.html">
      
    

    
    <style>
      @media only screen {
        table.full-width-table {
            width: 100%;
        }
      }
    </style>
<link rel="stylesheet" href="../_static/pydoctheme_dark.css" media="(prefers-color-scheme: dark)" id="pydoctheme_dark_css">
    <link rel="shortcut icon" type="image/png" href="../_static/py.svg">
            <script type="text/javascript" src="../_static/copybutton.js"></script>
            <script type="text/javascript" src="../_static/menu.js"></script>
            <script type="text/javascript" src="../_static/search-focus.js"></script>
            <script type="text/javascript" src="../_static/themetoggle.js"></script> 
            <script type="text/javascript" src="../_static/rtd_switcher.js"></script>
            <meta name="readthedocs-addons-api-version" content="1">

  </head>
<body>
<div class="mobile-nav">
    <input type="checkbox" id="menuToggler" class="toggler__input" aria-controls="navigation"
           aria-pressed="false" aria-expanded="false" role="button" aria-label="Menu">
    <nav class="nav-content" role="navigation">
        <label for="menuToggler" class="toggler__label">
            <span></span>
        </label>
        <span class="nav-items-wrapper">
            <a href="https://www.python.org/" class="nav-logo">
                <img src="../_static/py.svg" alt="Python logo">
            </a>
            <span class="version_switcher_placeholder"></span>
            <form role="search" class="search" action="../search.html" method="get">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" class="search-icon">
                    <path fill-rule="nonzero" fill="currentColor" d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 001.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 00-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 005.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                </svg>
                <input placeholder="Quick search" aria-label="Quick search" type="search" name="q">
                <input type="submit" value="Go">
            </form>
        </span>
    </nav>
    <div class="menu-wrapper">
        <nav class="menu" role="navigation" aria-label="main navigation">
            <div class="language_switcher_placeholder"></div>
            
<label class="theme-selector-label">
    Theme
    <select class="theme-selector" oninput="activateTheme(this.value)">
        <option value="auto" selected>Auto</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
    </select>
</label>
  <div>
    <h3><a href="../contents.html">Table of Contents</a></h3>
    <ul>
<li><a class="reference internal" href="#"><code class="xref py py-mod docutils literal notranslate"><span class="pre">os</span></code> — Miscellaneous operating system interfaces</a><ul>
<li><a class="reference internal" href="#file-names-command-line-arguments-and-environment-variables">File Names, Command Line Arguments, and Environment Variables</a></li>
<li><a class="reference internal" href="#python-utf-8-mode">Python UTF-8 Mode</a></li>
<li><a class="reference internal" href="#process-parameters">Process Parameters</a></li>
<li><a class="reference internal" href="#file-object-creation">File Object Creation</a></li>
<li><a class="reference internal" href="#file-descriptor-operations">File Descriptor Operations</a><ul>
<li><a class="reference internal" href="#querying-the-size-of-a-terminal">Querying the size of a terminal</a></li>
<li><a class="reference internal" href="#inheritance-of-file-descriptors">Inheritance of File Descriptors</a></li>
</ul>
</li>
<li><a class="reference internal" href="#files-and-directories">Files and Directories</a><ul>
<li><a class="reference internal" href="#timer-file-descriptors">Timer File Descriptors</a></li>
<li><a class="reference internal" href="#linux-extended-attributes">Linux extended attributes</a></li>
</ul>
</li>
<li><a class="reference internal" href="#process-management">Process Management</a></li>
<li><a class="reference internal" href="#interface-to-the-scheduler">Interface to the scheduler</a></li>
<li><a class="reference internal" href="#miscellaneous-system-information">Miscellaneous System Information</a></li>
<li><a class="reference internal" href="#random-numbers">Random numbers</a></li>
</ul>
</li>
</ul>

  </div>
  <div>
    <h4>Previous topic</h4>
    <p class="topless"><a href="allos.html"
                          title="previous chapter">Generic Operating System Services</a></p>
  </div>
  <div>
    <h4>Next topic</h4>
    <p class="topless"><a href="io.html"
                          title="next chapter"><code class="xref py py-mod docutils literal notranslate"><span class="pre">io</span></code> — Core tools for working with streams</a></p>
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', () => {
        const title = document.querySelector('meta[property="og:title"]').content;
        const elements = document.querySelectorAll('.improvepage');
        const pageurl = window.location.href.split('?')[0];
        elements.forEach(element => {
            const url = new URL(element.href.split('?')[0].replace("-nojs", ""));
            url.searchParams.set('pagetitle', title);
            url.searchParams.set('pageurl', pageurl);
            url.searchParams.set('pagesource', "library/os.rst");
            element.href = url.toString();
        });
    });
  </script>
  <div role="note" aria-label="source link">
    <h3>This page</h3>
    <ul class="this-page-menu">
      <li><a href="../bugs.html">Report a bug</a></li>
      <li><a class="improvepage" href="../improve-page-nojs.html">Improve this page</a></li>
      <li>
        <a href="https://github.com/python/cpython/blob/3.15/Doc/library/os.rst?plain=1"
            rel="nofollow">Show source
        </a>
      </li>
      
    </ul>
  </div>
        </nav>
    </div>
</div>

  
    <div class="related" role="navigation" aria-label="Related">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../genindex.html" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../py-modindex.html" title="Python Module Index"
             >modules</a> |</li>
        <li class="right" >
          <a href="io.html" title="io — Core tools for working with streams"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="allos.html" title="Generic Operating System Services"
             accesskey="P">previous</a> |</li>

          <li class="root-icon"><img src="../_static/py.svg" alt="Python logo" style="vertical-align: middle; margin-top: -1px"></li>
          <li><a href="https://www.python.org/">Python</a> &#187;</li>
          <li class="switchers">
            <div class="language_switcher_placeholder"></div>
            <div class="version_switcher_placeholder"></div>
          </li>
          <li>
              
          </li>
    <li id="cpython-language-and-version">
      <a href="../index.html">3.15.2 documentation</a> &#187;
    </li>

          <li class="nav-item nav-item-1"><a href="index.html" >The Python standard library</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="allos.html" accesskey="U">Generic Operating System Services</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href=""><code class="xref py py-mod docutils literal notranslate"><span class="pre">os</span></code> — Miscellaneous operating system interfaces</a></li>
                <li class="right">
                    

    <div class="inline-search" role="search">
        <form class="inline-search" action="../search.html" method="get">
          <input placeholder="Quick search" aria-label="Quick search" type="search" name="q" id="search-box">
          <input type="submit" value="Go">
        </form>
    </div>
                     |
                </li>
            <li class="right">
<label class="theme-selector-label">
    Theme
    <select class="theme-selector" oninput="activateTheme(this.value)">
        <option value="auto" selected>Auto</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
    </select>
</label> |</li>
            
      </ul>
    </div>    

    <div class="document">
      <div class="documentwrapper">
        <div class="bodywrapper">
          <div class="body" role="main">
            
  <section id="module-os">
<span id="os-miscellaneous-operating-system-interfaces"></span><h1><code class="xref py py-mod docutils literal notranslate"><span class="pre">os</span></code> — Miscellaneous operating system interfaces<a class="headerlink" href="#module-os" title="Link to this heading">¶</a></h1>
<p><strong>Source code:</strong> <a class="extlink-source reference external" href="https://github.com/python/cpython/tree/3.15/Lib/os.py">Lib/os.py</a></p>
<hr class="docutils" />
<p>This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see <a class="reference internal" href="../builtins/functions.html#open" title="open"><code class="xref py py-func docutils literal notranslate"><span class="pre">open()</span></code></a>, if
you want to manipulate paths, see the <a class="reference internal" href="os.path.html#module-os.path" title="os.path: Operations on pathnames."><code class="xref py py-mod docutils literal notranslate"><span class="pre">os.path</span></code></a> module, and if you want to
read all the lines in all the files on the command line see the <a class="reference internal" href="fileinput.html#module-fileinput" title="fileinput: Loop over standard input or a list of files."><code class="xref py py-mod docutils literal notranslate"><span class="pre">fileinput</span></code></a>
module.  For creating temporary files and directories see the <a class="reference internal" href="tempfile.html#module-tempfile" title="tempfile: Generate temporary files and directories."><code class="xref py py-mod docutils literal notranslate"><span class="pre">tempfile</span></code></a>
module, and for high-level file and directory handling see the <a class="reference internal" href="shutil.html#module-shutil" title="shutil: High-level file operations, including copying."><code class="xref py py-mod docutils literal notranslate"><span class="pre">shutil</span></code></a>
module.</p>
<p>Notes on the availability of these functions:</p>
<ul class="simple">
<li><p>The design of all built-in operating system dependent modules of Python is
such that as long as the same functionality is available, it uses the same
interface; for example, the function <code class="docutils literal notranslate"><span class="pre">os.stat(path)</span></code> returns stat
information about <em>path</em> in the same format (which happens to have originated
with the POSIX interface).</p></li>
<li><p>Extensions peculiar to a particular operating system are also available
through the <code class="xref py py-mod docutils literal notranslate"><span class="pre">os</span></code> module, but using them is of course a threat to
portability.</p></li>
<li><p>All functions accepting path or file names accept both bytes and string
objects, and result in an object of the same type, if a path or file name is
returned.</p></li>
<li><p>On VxWorks, os.popen, os.fork, os.execv and os.spawn*p* are not supported.</p></li>
<li><p>On WebAssembly platforms, Android and iOS, large parts of the <code class="xref py py-mod docutils literal notranslate"><span class="pre">os</span></code> module are
not available or behave differently. APIs related to processes (e.g.
<a class="reference internal" href="#os.fork" title="os.fork"><code class="xref py py-func docutils literal notranslate"><span class="pre">fork()</span></code></a>, <a class="reference internal" href="#os.execve" title="os.execve"><code class="xref py py-func docutils literal notranslate"><span class="pre">execve()</span></code></a>) and resources (e.g. <a class="reference internal" href="#os.nice" title="os.nice"><code class="xref py py-func docutils literal notranslate"><span class="pre">nice()</span></code></a>)
are not available. Others like <a class="reference internal" href="#os.getuid" title="os.getuid"><code class="xref py py-func docutils literal notranslate"><span class="pre">getuid()</span></code></a> and <a class="reference internal" href="#os.getpid" title="os.getpid"><code class="xref py py-func docutils literal notranslate"><span class="pre">getpid()</span></code></a> are
emulated or stubs. WebAssembly platforms also lack support for signals (e.g.
<a class="reference internal" href="#os.kill" title="os.kill"><code class="xref py py-func docutils literal notranslate"><span class="pre">kill()</span></code></a>, <a class="reference internal" href="#os.wait" title="os.wait"><code class="xref py py-func docutils literal notranslate"><span class="pre">wait()</span></code></a>).</p></li>
</ul>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>All functions in this module raise <a class="reference internal" href="../builtins/exceptions.html#OSError" title="OSError"><code class="xref py py-exc docutils literal notranslate"><span class="pre">OSError</span></code></a> (or subclasses thereof) in
the case of invalid or inaccessible file names and paths, or other arguments
that have the correct type, but are not accepted by the operating system.</p>
</div>
<dl class="py exception">
<dt class="sig sig-object py" id="os.error">
<span class="property"><span class="k"><span class="pre">exception</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">error</span></span><a class="headerlink" href="#os.error" title="Link to this definition">¶</a></dt>
<dd><p>An alias for the built-in <a class="reference internal" href="../builtins/exceptions.html#OSError" title="OSError"><code class="xref py py-exc docutils literal notranslate"><span class="pre">OSError</span></code></a> exception.</p>
</dd></dl>

<dl class="py data">
<dt class="sig sig-object py" id="os.name">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#os.name" title="Link to this definition">¶</a></dt>
<dd><p>The name of the operating system dependent module imported.  The following
names have currently been registered: <code class="docutils literal notranslate"><span class="pre">'posix'</span></code>, <code class="docutils literal notranslate"><span class="pre">'nt'</span></code>,
<code class="docutils literal notranslate"><span class="pre">'java'</span></code>.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="sys.html#sys.platform" title="sys.platform"><code class="xref py py-data docutils literal notranslate"><span class="pre">sys.platform</span></code></a> has a finer granularity.  <a class="reference internal" href="#os.uname" title="os.uname"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.uname()</span></code></a> gives
system-dependent version information.</p>
<p>The <a class="reference internal" href="platform.html#module-platform" title="platform: Retrieves as much platform identifying data as possible."><code class="xref py py-mod docutils literal notranslate"><span class="pre">platform</span></code></a> module provides detailed checks for the
system’s identity.</p>
</div>
</dd></dl>

<section id="file-names-command-line-arguments-and-environment-variables">
<span id="filesystem-encoding"></span><span id="os-filenames"></span><h2>File Names, Command Line Arguments, and Environment Variables<a class="headerlink" href="#file-names-command-line-arguments-and-environment-variables" title="Link to this heading">¶</a></h2>
<p>In Python, file names, command line arguments, and environment variables are
represented using the string type. On some systems, decoding these strings to
and from bytes is necessary before passing them to the operating system. Python
uses the <a class="reference internal" href="../glossary.html#term-filesystem-encoding-and-error-handler"><span class="xref std std-term">filesystem encoding and error handler</span></a> to perform this
conversion (see <a class="reference internal" href="sys.html#sys.getfilesystemencoding" title="sys.getfilesystemencoding"><code class="xref py py-func docutils literal notranslate"><span class="pre">sys.getfilesystemencoding()</span></code></a>).</p>
<p>The <a class="reference internal" href="../glossary.html#term-filesystem-encoding-and-error-handler"><span class="xref std std-term">filesystem encoding and error handler</span></a> are configured at Python
startup by the <a class="reference internal" href="../c-api/init_config.html#c.PyConfig_Read" title="PyConfig_Read"><code class="xref c c-func docutils literal notranslate"><span class="pre">PyConfig_Read()</span></code></a> function: see
<a class="reference internal" href="../c-api/init_config.html#c.PyConfig.filesystem_encoding" title="PyConfig.filesystem_encoding"><code class="xref c c-member docutils literal notranslate"><span class="pre">filesystem_encoding</span></code></a> and
<a class="reference internal" href="../c-api/init_config.html#c.PyConfig.filesystem_errors" title="PyConfig.filesystem_errors"><code class="xref c c-member docutils literal notranslate"><span class="pre">filesystem_errors</span></code></a> members of <a class="reference internal" href="../c-api/init_config.html#c.PyConfig" title="PyConfig"><code class="xref c c-type docutils literal notranslate"><span class="pre">PyConfig</span></code></a>.</p>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.1: </span>On some systems, conversion using the file system encoding may fail. In this
case, Python uses the <a class="reference internal" href="codecs.html#surrogateescape"><span class="std std-ref">surrogateescape encoding error handler</span></a>, which means that undecodable bytes are replaced by a
Unicode character U+DC<em>xx</em> on decoding, and these are again
translated to the original byte on encoding.</p>
</div>
<p>The <a class="reference internal" href="../glossary.html#term-filesystem-encoding-and-error-handler"><span class="xref std std-term">file system encoding</span></a> must
guarantee to successfully decode all bytes below 128. If the file system
encoding fails to provide this guarantee, API functions can raise
<a class="reference internal" href="../builtins/exceptions.html#UnicodeError" title="UnicodeError"><code class="xref py py-exc docutils literal notranslate"><span class="pre">UnicodeError</span></code></a>.</p>
<p>See also the <a class="reference internal" href="../glossary.html#term-locale-encoding"><span class="xref std std-term">locale encoding</span></a>.</p>
</section>
<section id="python-utf-8-mode">
<span id="utf8-mode"></span><h2>Python UTF-8 Mode<a class="headerlink" href="#python-utf-8-mode" title="Link to this heading">¶</a></h2>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.7: </span>See <span class="target" id="index-0"></span><a class="pep reference external" href="https://peps.python.org/pep-0540/"><strong>PEP 540</strong></a> for more details.</p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.15: </span>Python UTF-8 mode is now enabled by default (<span class="target" id="index-1"></span><a class="pep reference external" href="https://peps.python.org/pep-0686/"><strong>PEP 686</strong></a>).
It may be disabled by setting <span class="target" id="index-2"></span><a class="reference internal" href="../using/cmdline.html#envvar-PYTHONUTF8"><code class="xref std std-envvar docutils literal notranslate"><span class="pre">PYTHONUTF8=0</span></code></a> as
an environment variable or by using the <a class="reference internal" href="../using/cmdline.html#cmdoption-X"><code class="xref std std-option docutils literal notranslate"><span class="pre">-X</span> <span class="pre">utf8=0</span></code></a> command line option.</p>
</div>
<p>The Python UTF-8 Mode ignores the <a class="reference internal" href="../glossary.html#term-locale-encoding"><span class="xref std std-term">locale encoding</span></a> and forces the usage
of the UTF-8 encoding:</p>
<ul class="simple">
<li><p>Use UTF-8 as the <a class="reference internal" href="../glossary.html#term-filesystem-encoding-and-error-handler"><span class="xref std std-term">filesystem encoding</span></a>.</p></li>
<li><p><a class="reference internal" href="sys.html#sys.getfilesystemencoding" title="sys.getfilesystemencoding"><code class="xref py py-func docutils literal notranslate"><span class="pre">sys.getfilesystemencoding()</span></code></a> returns <code class="docutils literal notranslate"><span class="pre">'utf-8'</span></code>.</p></li>
<li><p><a class="reference internal" href="locale.html#locale.getpreferredencoding" title="locale.getpreferredencoding"><code class="xref py py-func docutils literal notranslate"><span class="pre">locale.getpreferredencoding()</span></code></a> returns <code class="docutils literal notranslate"><span class="pre">'utf-8'</span></code> (the <em>do_setlocale</em>
argument has no effect).</p></li>
<li><p><a class="reference internal" href="sys.html#sys.stdin" title="sys.stdin"><code class="xref py py-data docutils literal notranslate"><span class="pre">sys.stdin</span></code></a>, <a class="reference internal" href="sys.html#sys.stdout" title="sys.stdout"><code class="xref py py-data docutils literal notranslate"><span class="pre">sys.stdout</span></code></a>, and <a class="reference internal" href="sys.html#sys.stderr" title="sys.stderr"><code class="xref py py-data docutils literal notranslate"><span class="pre">sys.stderr</span></code></a> all use
UTF-8 as their text encoding, with the <code class="docutils literal notranslate"><span class="pre">surrogateescape</span></code>
<a class="reference internal" href="codecs.html#error-handlers"><span class="std std-ref">error handler</span></a> being enabled for <code class="xref py py-data docutils literal notranslate"><span class="pre">sys.stdin</span></code>
and <code class="xref py py-data docutils literal notranslate"><span class="pre">sys.stdout</span></code> (<code class="xref py py-data docutils literal notranslate"><span class="pre">sys.stderr</span></code> continues to use
<code class="docutils literal notranslate"><span class="pre">backslashreplace</span></code> as it does in the default locale-aware mode)</p></li>
<li><p>On Unix, <a class="reference internal" href="#os.device_encoding" title="os.device_encoding"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.device_encoding()</span></code></a> returns <code class="docutils literal notranslate"><span class="pre">'utf-8'</span></code> rather than the
device encoding.</p></li>
</ul>
<p>Note that the standard stream settings in UTF-8 mode can be overridden by
<span class="target" id="index-3"></span><a class="reference internal" href="../using/cmdline.html#envvar-PYTHONIOENCODING"><code class="xref std std-envvar docutils literal notranslate"><span class="pre">PYTHONIOENCODING</span></code></a> (just as they can be in the default locale-aware
mode).</p>
<p>As a consequence of the changes in those lower level APIs, other higher
level APIs also exhibit different default behaviours:</p>
<ul class="simple">
<li><p>Command line arguments, environment variables and filenames are decoded
to text using the UTF-8 encoding.</p></li>
<li><p><a class="reference internal" href="#os.fsdecode" title="os.fsdecode"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.fsdecode()</span></code></a> and <a class="reference internal" href="#os.fsencode" title="os.fsencode"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.fsencode()</span></code></a> use the UTF-8 encoding.</p></li>
<li><p><a class="reference internal" href="../builtins/functions.html#open" title="open"><code class="xref py py-func docutils literal notranslate"><span class="pre">open()</span></code></a>, <a class="reference internal" href="io.html#io.open" title="io.open"><code class="xref py py-func docutils literal notranslate"><span class="pre">io.open()</span></code></a>, and <a class="reference internal" href="codecs.html#codecs.open" title="codecs.open"><code class="xref py py-func docutils literal notranslate"><span class="pre">codecs.open()</span></code></a> use the UTF-8
encoding by default. However, they still use the strict error handler by
default so that attempting to open a binary file in text mode is likely
to raise an exception rather than producing nonsense data.</p></li>
</ul>
<p>The <a class="reference internal" href="#utf8-mode"><span class="std std-ref">Python UTF-8 Mode</span></a> is enabled by default.
It can be disabled using the <a class="reference internal" href="../using/cmdline.html#cmdoption-X"><code class="xref std std-option docutils literal notranslate"><span class="pre">-X</span> <span class="pre">utf8=0</span></code></a> command line
option or the <span class="target" id="index-4"></span><a class="reference internal" href="../using/cmdline.html#envvar-PYTHONUTF8"><code class="xref std std-envvar docutils literal notranslate"><span class="pre">PYTHONUTF8=0</span></code></a> environment variable.
The Python UTF-8 Mode can only be disabled at Python startup. Its value
can be read from <a class="reference internal" href="sys.html#sys.flags" title="sys.flags"><code class="xref py py-data docutils literal notranslate"><span class="pre">sys.flags.utf8_mode</span></code></a>.</p>
<p>If the UTF-8 mode is disabled, the interpreter defaults to using
the current locale settings, <em>unless</em> the current locale is identified
as a legacy ASCII-based locale (as described for <span class="target" id="index-5"></span><a class="reference internal" href="../using/cmdline.html#envvar-PYTHONCOERCECLOCALE"><code class="xref std std-envvar docutils literal notranslate"><span class="pre">PYTHONCOERCECLOCALE</span></code></a>),
and locale coercion is either disabled or fails.
In such legacy locales, the interpreter will default to enabling UTF-8 mode
unless explicitly instructed not to do so.</p>
<p>See also the <a class="reference internal" href="../using/windows.html#win-utf8-mode"><span class="std std-ref">UTF-8 mode on Windows</span></a>
and the <a class="reference internal" href="../glossary.html#term-filesystem-encoding-and-error-handler"><span class="xref std std-term">filesystem encoding and error handler</span></a>.</p>
</section>
<section id="process-parameters">
<span id="os-procinfo"></span><h2>Process Parameters<a class="headerlink" href="#process-parameters" title="Link to this heading">¶</a></h2>
<p>These functions and data items provide information and operate on the current
process and user.</p>
<dl class="py function">
<dt class="sig sig-object py" id="os.ctermid">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">ctermid</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.ctermid" title="Link to this definition">¶</a></dt>
<dd><p>Return the filename corresponding to the controlling terminal of the process.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, not WASI.</p>
</div>
</dd></dl>

<dl class="py data">
<dt class="sig sig-object py" id="os.environ">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">environ</span></span><a class="headerlink" href="#os.environ" title="Link to this definition">¶</a></dt>
<dd><p>A <a class="reference internal" href="../glossary.html#term-mapping"><span class="xref std std-term">mapping</span></a> object where keys and values are strings that represent
the process environment.  For example, <code class="docutils literal notranslate"><span class="pre">environ['HOME']</span></code> is the pathname
of your home directory (on some platforms), and is equivalent to
<code class="docutils literal notranslate"><span class="pre">getenv(&quot;HOME&quot;)</span></code> in C.</p>
<p>This mapping is captured the first time the <code class="xref py py-mod docutils literal notranslate"><span class="pre">os</span></code> module is imported,
typically during Python startup as part of processing <code class="file docutils literal notranslate"><span class="pre">site.py</span></code>.  Changes
to the environment made after this time are not reflected in <code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code>,
except for changes made by modifying <code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code> directly.</p>
<p>This mapping may be used to modify the environment as well as query the
environment.  <a class="reference internal" href="#os.putenv" title="os.putenv"><code class="xref py py-func docutils literal notranslate"><span class="pre">putenv()</span></code></a> will be called automatically when the mapping
is modified.</p>
<p>On Unix, keys and values use <a class="reference internal" href="sys.html#sys.getfilesystemencoding" title="sys.getfilesystemencoding"><code class="xref py py-func docutils literal notranslate"><span class="pre">sys.getfilesystemencoding()</span></code></a> and
<code class="docutils literal notranslate"><span class="pre">'surrogateescape'</span></code> error handler. Use <a class="reference internal" href="#os.environb" title="os.environb"><code class="xref py py-data docutils literal notranslate"><span class="pre">environb</span></code></a> if you would like
to use a different encoding.</p>
<p>On Windows, the keys are converted to uppercase. This also applies when
getting, setting, or deleting an item. For example,
<code class="docutils literal notranslate"><span class="pre">environ['monty']</span> <span class="pre">=</span> <span class="pre">'python'</span></code> maps the key <code class="docutils literal notranslate"><span class="pre">'MONTY'</span></code> to the value
<code class="docutils literal notranslate"><span class="pre">'python'</span></code>.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Calling <a class="reference internal" href="#os.putenv" title="os.putenv"><code class="xref py py-func docutils literal notranslate"><span class="pre">putenv()</span></code></a> directly does not change <code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code>, so it’s better
to modify <code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code>.</p>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>On some platforms, including FreeBSD and macOS, setting <code class="docutils literal notranslate"><span class="pre">environ</span></code> may
cause memory leaks.  Refer to the system documentation for
<code class="xref c c-func docutils literal notranslate"><span class="pre">putenv()</span></code>.</p>
</div>
<p>You can delete items in this mapping to unset environment variables.
<a class="reference internal" href="#os.unsetenv" title="os.unsetenv"><code class="xref py py-func docutils literal notranslate"><span class="pre">unsetenv()</span></code></a> will be called automatically when an item is deleted from
<code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code>, and when one of the <a class="reference internal" href="../builtins/stdtypes.html#dict.pop" title="dict.pop"><code class="xref py py-meth docutils literal notranslate"><span class="pre">pop()</span></code></a> or
<a class="reference internal" href="../builtins/stdtypes.html#dict.clear" title="dict.clear"><code class="xref py py-meth docutils literal notranslate"><span class="pre">clear()</span></code></a> methods is called.</p>
<p>If the <em class="manpage"><a class="manpage reference external" href="https://manpages.debian.org/clearenv(3)">clearenv(3)</a></em> function is available, the <a class="reference internal" href="../builtins/stdtypes.html#dict.clear" title="dict.clear"><code class="xref py py-meth docutils literal notranslate"><span class="pre">clear()</span></code></a> method
uses it and emits a single <code class="docutils literal notranslate"><span class="pre">os._clearenv</span></code> audit event. Otherwise, it emits
an <code class="docutils literal notranslate"><span class="pre">os.unsetenv</span></code> event on each deleted variable.</p>
<p class="audit-hook">Raises an <a class="reference internal" href="sys.html#auditing"><span class="std std-ref">auditing event</span></a> <code class="docutils literal notranslate"><span class="pre">os.unsetenv</span></code> with argument <code class="docutils literal notranslate"><span class="pre">key</span></code>.</p>
<p class="audit-hook">Raises an <a class="reference internal" href="sys.html#auditing"><span class="std std-ref">auditing event</span></a> <code class="docutils literal notranslate"><span class="pre">os._clearenv</span></code> with no arguments.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p>The <a class="reference internal" href="#os.reload_environ" title="os.reload_environ"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.reload_environ()</span></code></a> function.</p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.9: </span>Updated to support <span class="target" id="index-6"></span><a class="pep reference external" href="https://peps.python.org/pep-0584/"><strong>PEP 584</strong></a>’s merge (<code class="docutils literal notranslate"><span class="pre">|</span></code>) and update (<code class="docutils literal notranslate"><span class="pre">|=</span></code>) operators.</p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.15: </span>The <a class="reference internal" href="../builtins/stdtypes.html#dict.clear" title="dict.clear"><code class="xref py py-meth docutils literal notranslate"><span class="pre">clear()</span></code></a> method can now emit an <code class="docutils literal notranslate"><span class="pre">os._clearenv</span></code> audit
event.</p>
</div>
</dd></dl>

<dl class="py data">
<dt class="sig sig-object py" id="os.environb">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">environb</span></span><a class="headerlink" href="#os.environb" title="Link to this definition">¶</a></dt>
<dd><p>Bytes version of <a class="reference internal" href="#os.environ" title="os.environ"><code class="xref py py-data docutils literal notranslate"><span class="pre">environ</span></code></a>: a <a class="reference internal" href="../glossary.html#term-mapping"><span class="xref std std-term">mapping</span></a> object where both keys
and values are <a class="reference internal" href="../builtins/stdtypes.html#bytes" title="bytes"><code class="xref py py-class docutils literal notranslate"><span class="pre">bytes</span></code></a> objects representing the process environment.
<code class="xref py py-data docutils literal notranslate"><span class="pre">environ</span></code> and <code class="xref py py-data docutils literal notranslate"><span class="pre">environb</span></code> are synchronized (modifying
<code class="xref py py-data docutils literal notranslate"><span class="pre">environb</span></code> updates <code class="xref py py-data docutils literal notranslate"><span class="pre">environ</span></code>, and vice versa).</p>
<p><code class="xref py py-data docutils literal notranslate"><span class="pre">environb</span></code> is only available if <a class="reference internal" href="#os.supports_bytes_environ" title="os.supports_bytes_environ"><code class="xref py py-const docutils literal notranslate"><span class="pre">supports_bytes_environ</span></code></a> is
<code class="docutils literal notranslate"><span class="pre">True</span></code>.</p>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.2.</span></p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.9: </span>Updated to support <span class="target" id="index-7"></span><a class="pep reference external" href="https://peps.python.org/pep-0584/"><strong>PEP 584</strong></a>’s merge (<code class="docutils literal notranslate"><span class="pre">|</span></code>) and update (<code class="docutils literal notranslate"><span class="pre">|=</span></code>) operators.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.reload_environ">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">reload_environ</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.reload_environ" title="Link to this definition">¶</a></dt>
<dd><p>The <a class="reference internal" href="#os.environ" title="os.environ"><code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code></a> and <a class="reference internal" href="#os.environb" title="os.environb"><code class="xref py py-data docutils literal notranslate"><span class="pre">os.environb</span></code></a> mappings are a cache of
environment variables at the time that Python started.
As such, changes to the current process environment are not reflected
if made outside Python, or by <a class="reference internal" href="#os.putenv" title="os.putenv"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.putenv()</span></code></a> or <a class="reference internal" href="#os.unsetenv" title="os.unsetenv"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.unsetenv()</span></code></a>.
Use <code class="xref py py-func docutils literal notranslate"><span class="pre">os.reload_environ()</span></code> to update <code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code> and <code class="xref py py-data docutils literal notranslate"><span class="pre">os.environb</span></code>
with any such changes to the current process environment.</p>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>This function is not thread-safe. Calling it while the environment is
being modified in another thread is an undefined behavior. Reading from
<a class="reference internal" href="#os.environ" title="os.environ"><code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code></a> or <a class="reference internal" href="#os.environb" title="os.environb"><code class="xref py py-data docutils literal notranslate"><span class="pre">os.environb</span></code></a>, or calling <a class="reference internal" href="#os.getenv" title="os.getenv"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.getenv()</span></code></a>
while reloading, may return an empty result.</p>
</div>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.14.</span></p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">chdir</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span></em><span class="sig-paren">)</span></dt>
<dt class="sig sig-object py">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">fchdir</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fd</span></span></em><span class="sig-paren">)</span></dt>
<dt class="sig sig-object py">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getcwd</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>These functions are described in <a class="reference internal" href="#os-file-dir"><span class="std std-ref">Files and Directories</span></a>.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.fsencode">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">fsencode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">filename</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.fsencode" title="Link to this definition">¶</a></dt>
<dd><p>Encode <a class="reference internal" href="../glossary.html#term-path-like-object"><span class="xref std std-term">path-like</span></a> <em>filename</em> to the
<a class="reference internal" href="../glossary.html#term-filesystem-encoding-and-error-handler"><span class="xref std std-term">filesystem encoding and error handler</span></a>; return <a class="reference internal" href="../builtins/stdtypes.html#bytes" title="bytes"><code class="xref py py-class docutils literal notranslate"><span class="pre">bytes</span></code></a>
unchanged.</p>
<p><a class="reference internal" href="#os.fsdecode" title="os.fsdecode"><code class="xref py py-func docutils literal notranslate"><span class="pre">fsdecode()</span></code></a> is the reverse function.</p>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.2.</span></p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.6: </span>Support added to accept objects implementing the <a class="reference internal" href="#os.PathLike" title="os.PathLike"><code class="xref py py-class docutils literal notranslate"><span class="pre">os.PathLike</span></code></a>
interface.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.fsdecode">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">fsdecode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">filename</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.fsdecode" title="Link to this definition">¶</a></dt>
<dd><p>Decode the <a class="reference internal" href="../glossary.html#term-path-like-object"><span class="xref std std-term">path-like</span></a> <em>filename</em> from the
<a class="reference internal" href="../glossary.html#term-filesystem-encoding-and-error-handler"><span class="xref std std-term">filesystem encoding and error handler</span></a>; return <a class="reference internal" href="../builtins/stdtypes.html#str" title="str"><code class="xref py py-class docutils literal notranslate"><span class="pre">str</span></code></a>
unchanged.</p>
<p><a class="reference internal" href="#os.fsencode" title="os.fsencode"><code class="xref py py-func docutils literal notranslate"><span class="pre">fsencode()</span></code></a> is the reverse function.</p>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.2.</span></p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.6: </span>Support added to accept objects implementing the <a class="reference internal" href="#os.PathLike" title="os.PathLike"><code class="xref py py-class docutils literal notranslate"><span class="pre">os.PathLike</span></code></a>
interface.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.fspath">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">fspath</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.fspath" title="Link to this definition">¶</a></dt>
<dd><p>Return the file system representation of the path.</p>
<p>If <a class="reference internal" href="../builtins/stdtypes.html#str" title="str"><code class="xref py py-class docutils literal notranslate"><span class="pre">str</span></code></a> or <a class="reference internal" href="../builtins/stdtypes.html#bytes" title="bytes"><code class="xref py py-class docutils literal notranslate"><span class="pre">bytes</span></code></a> is passed in, it is returned unchanged.
Otherwise <a class="reference internal" href="#os.PathLike.__fspath__" title="os.PathLike.__fspath__"><code class="xref py py-meth docutils literal notranslate"><span class="pre">__fspath__()</span></code></a> is called and its value is
returned as long as it is a <code class="xref py py-class docutils literal notranslate"><span class="pre">str</span></code> or <code class="xref py py-class docutils literal notranslate"><span class="pre">bytes</span></code> object.
In all other cases, <a class="reference internal" href="../builtins/exceptions.html#TypeError" title="TypeError"><code class="xref py py-exc docutils literal notranslate"><span class="pre">TypeError</span></code></a> is raised.</p>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.6.</span></p>
</div>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="os.PathLike">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">PathLike</span></span><a class="headerlink" href="#os.PathLike" title="Link to this definition">¶</a></dt>
<dd><p>An <a class="reference internal" href="../glossary.html#term-abstract-base-class"><span class="xref std std-term">abstract base class</span></a> for objects representing a file system path,
e.g. <a class="reference internal" href="pathlib.html#pathlib.PurePath" title="pathlib.PurePath"><code class="xref py py-class docutils literal notranslate"><span class="pre">pathlib.PurePath</span></code></a>.</p>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.6.</span></p>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="os.PathLike.__fspath__">
<span class="property"><span class="k"><span class="pre">abstractmethod</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">__fspath__</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.PathLike.__fspath__" title="Link to this definition">¶</a></dt>
<dd><p>Return the file system path representation of the object.</p>
<p>The method should only return a <a class="reference internal" href="../builtins/stdtypes.html#str" title="str"><code class="xref py py-class docutils literal notranslate"><span class="pre">str</span></code></a> or <a class="reference internal" href="../builtins/stdtypes.html#bytes" title="bytes"><code class="xref py py-class docutils literal notranslate"><span class="pre">bytes</span></code></a> object,
with the preference being for <code class="xref py py-class docutils literal notranslate"><span class="pre">str</span></code>.</p>
</dd></dl>

</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getenv">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getenv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">key</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.getenv" title="Link to this definition">¶</a></dt>
<dd><p>Return the value of the environment variable <em>key</em> as a string if it exists, or
<em>default</em> if it doesn’t. <em>key</em> is a string. Note that
since <code class="xref py py-func docutils literal notranslate"><span class="pre">getenv()</span></code> uses <a class="reference internal" href="#os.environ" title="os.environ"><code class="xref py py-data docutils literal notranslate"><span class="pre">os.environ</span></code></a>, the mapping of <code class="xref py py-func docutils literal notranslate"><span class="pre">getenv()</span></code> is
similarly also captured on import, and the function may not reflect
future environment changes.</p>
<p>On Unix, keys and values are decoded with <a class="reference internal" href="sys.html#sys.getfilesystemencoding" title="sys.getfilesystemencoding"><code class="xref py py-func docutils literal notranslate"><span class="pre">sys.getfilesystemencoding()</span></code></a>
and <code class="docutils literal notranslate"><span class="pre">'surrogateescape'</span></code> error handler. Use <a class="reference internal" href="#os.getenvb" title="os.getenvb"><code class="xref py py-func docutils literal notranslate"><span class="pre">os.getenvb()</span></code></a> if you
would like to use a different encoding.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, Windows.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getenvb">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getenvb</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">key</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.getenvb" title="Link to this definition">¶</a></dt>
<dd><p>Return the value of the environment variable <em>key</em> as bytes if it exists, or
<em>default</em> if it doesn’t. <em>key</em> must be bytes. Note that
since <code class="xref py py-func docutils literal notranslate"><span class="pre">getenvb()</span></code> uses <a class="reference internal" href="#os.environb" title="os.environb"><code class="xref py py-data docutils literal notranslate"><span class="pre">os.environb</span></code></a>, the mapping of <code class="xref py py-func docutils literal notranslate"><span class="pre">getenvb()</span></code> is
similarly also captured on import, and the function may not reflect
future environment changes.</p>
<p><code class="xref py py-func docutils literal notranslate"><span class="pre">getenvb()</span></code> is only available if <a class="reference internal" href="#os.supports_bytes_environ" title="os.supports_bytes_environ"><code class="xref py py-const docutils literal notranslate"><span class="pre">supports_bytes_environ</span></code></a>
is <code class="docutils literal notranslate"><span class="pre">True</span></code>.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix.</p>
</div>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.2.</span></p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.get_exec_path">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">get_exec_path</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">env</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.get_exec_path" title="Link to this definition">¶</a></dt>
<dd><p>Returns the list of directories that will be searched for a named
executable, similar to a shell, when launching a process.
<em>env</em>, when specified, should be an environment variable dictionary
to lookup the PATH in.
By default, when <em>env</em> is <code class="docutils literal notranslate"><span class="pre">None</span></code>, <a class="reference internal" href="#os.environ" title="os.environ"><code class="xref py py-data docutils literal notranslate"><span class="pre">environ</span></code></a> is used.</p>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.2.</span></p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getegid">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getegid</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.getegid" title="Link to this definition">¶</a></dt>
<dd><p>Return the effective group id of the current process.  This corresponds to the
“set id” bit on the file being executed in the current process.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, not WASI.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.geteuid">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">geteuid</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.geteuid" title="Link to this definition">¶</a></dt>
<dd><p id="index-8">Return the current process’s effective user id.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, not WASI.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getgid">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getgid</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.getgid" title="Link to this definition">¶</a></dt>
<dd><p id="index-9">Return the real group id of the current process.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix.</p>
<p>The function is a stub on WASI, see <a class="reference internal" href="intro.html#wasm-availability"><span class="std std-ref">WebAssembly platforms</span></a> for more
information.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getgrouplist">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getgrouplist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">user</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group</span></span></em>, <em class="sig-param"><span class="positional-only-separator o"><abbr title="Positional-only parameter separator (PEP 570)"><span class="pre">/</span></abbr></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.getgrouplist" title="Link to this definition">¶</a></dt>
<dd><p>Return list of group ids that <em>user</em> belongs to. If <em>group</em> is not in the
list, it is included; typically, <em>group</em> is specified as the group ID
field from the password record for <em>user</em>, because that group ID will
otherwise be potentially omitted.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, not WASI.</p>
</div>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 3.3.</span></p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getgroups">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getgroups</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.getgroups" title="Link to this definition">¶</a></dt>
<dd><p>Return list of supplemental group ids associated with the current process.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, not WASI.</p>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>On macOS, <code class="xref py py-func docutils literal notranslate"><span class="pre">getgroups()</span></code> behavior differs somewhat from
other Unix platforms. If the Python interpreter was built with a
deployment target of <code class="docutils literal notranslate"><span class="pre">10.5</span></code> or earlier, <code class="xref py py-func docutils literal notranslate"><span class="pre">getgroups()</span></code> returns
the list of effective group ids associated with the current user process;
this list is limited to a system-defined number of entries, typically 16,
and may be modified by calls to <a class="reference internal" href="#os.setgroups" title="os.setgroups"><code class="xref py py-func docutils literal notranslate"><span class="pre">setgroups()</span></code></a> if suitably privileged.
If built with a deployment target greater than <code class="docutils literal notranslate"><span class="pre">10.5</span></code>,
<code class="xref py py-func docutils literal notranslate"><span class="pre">getgroups()</span></code> returns the current group access list for the user
associated with the effective user id of the process; the group access
list may change over the lifetime of the process, it is not affected by
calls to <code class="xref py py-func docutils literal notranslate"><span class="pre">setgroups()</span></code>, and its length is not limited to 16.  The
deployment target value can be obtained with
<a class="reference internal" href="sysconfig.html#sysconfig.get_config_var" title="sysconfig.get_config_var"><code class="xref py py-func docutils literal notranslate"><span class="pre">sysconfig.get_config_var('MACOSX_DEPLOYMENT_TARGET')</span></code></a>.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getlogin">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getlogin</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.getlogin" title="Link to this definition">¶</a></dt>
<dd><p>Return the name of the user logged in on the controlling terminal of the
process.  For most purposes, it is more useful to use
<a class="reference internal" href="getpass.html#getpass.getuser" title="getpass.getuser"><code class="xref py py-func docutils literal notranslate"><span class="pre">getpass.getuser()</span></code></a> since the latter checks the environment variables
<span class="target" id="index-10"></span><code class="xref std std-envvar docutils literal notranslate"><span class="pre">LOGNAME</span></code> or <span class="target" id="index-11"></span><code class="xref std std-envvar docutils literal notranslate"><span class="pre">USERNAME</span></code> to find out who the user is, and
falls back to <code class="docutils literal notranslate"><span class="pre">pwd.getpwuid(os.getuid())[0]</span></code> to get the login name of the
current real user id.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, Windows, not WASI.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getpgid">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getpgid</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#os.getpgid" title="Link to this definition">¶</a></dt>
<dd><p>Return the process group id of the process with process id <em>pid</em>. If <em>pid</em> is 0,
the process group id of the current process is returned.</p>
<div class="availability docutils container">
<p><a class="reference internal" href="intro.html#availability"><span class="std std-ref">Availability</span></a>: Unix, not WASI.</p>
</div>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="os.getpgrp">
<span class="sig-prename descclassname"><span class="pre">os.</span></span><span class="sig-name descname"><span class="pre">getpgrp</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#os.getpgrp" title="Link to this definition">¶</a></dt>
<dd><p id="index-12">Return the id of the current process group