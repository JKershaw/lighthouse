<!DOCTYPE html>
<html lang="en-US">
    <head>
        <script src="/static/js/theme-init.js" blocking="render"></script>
        <title>Moose - A postmodern object system for Perl 5 - metacpan.org</title>
        <link rel="preload" as="fetch" href="/account/login_status" crossorigin="anonymous" />
        <link href="/assets/style-I4CHMMGG.css" rel="stylesheet" type="text/css">
        <script src="/assets/main-KQ2ZKTMJ.js" type="module"></script>
        <link rel="alternate" type="application/rss+xml" title="Recent CPAN Uploads of Moose - MetaCPAN" href="/dist/Moose/releases.rss" />
        <link rel="canonical" href="https://metacpan.org/pod/Moose" />
        <meta name="description" content="A postmodern object system for Perl 5" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
        <link rel="shortcut icon" href="/static/icons/favicon.ico">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/icons/apple-touch-icon.png">
        <link rel="search" href="/static/opensearch.xml" type="application/opensearchdescription+xml" title="MetaCPAN">
<meta property="og:site_name"   content="MetaCPAN" />
<meta name="twitter:site"       content="@metacpan" />
<meta property="og:type"        content="article" />
<meta name="twitter:card"       content="summary" />
<meta property="og:url"         content="https://metacpan.org/pod/Moose" />
<meta property="og:title"       content="Moose" />
<meta property="og:description" content="A postmodern object system for Perl 5" />
<meta property="og:image"       content="https://metacpan.org/static/images/og.png" />
    </head>
    <body>
        <nav class="navbar" aria-label="Main navigation">
            <div class="header-logo-large d-none d-sm-block">
              <a href="/" tabindex="0">
                <svg class="logo" role="img" aria-label="MetaCPAN">
                  <use class="logo" href="/static/images/metacpan-logo.svg#logo" />
                </svg>
              </a>
            </div>
            <div class="header-logo-icon d-block d-sm-none">
              <a href="/">
                <svg class="logo" role="img" aria-label="MetaCPAN">
                  <use class="logo" href="/static/images/metacpan-logo.svg#dots" />
                </svg>
              </a>
            </div>
            <ul class="nav navbar-nav menu-items d-none d-md-flex">
              <li><a href="/about">About</a></li>
              <li><a href="/about/sponsors">Sponsor</a></li>
              <li><a href="https://grep.metacpan.org/">grep::cpan</a></li>
              <li><a href="/recent">Recent</a></li>
              <li><a href="/about/faq">FAQ</a></li>
              <li><a href="/tools">Tools</a></li>
              <li><a href="https://api.metacpan.org/">API</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right ms-auto">
                <li>
                    <button type="button" class="theme-toggle" aria-label="Toggle dark mode">
                        <i class="fas fa-moon" aria-hidden="true"></i>
                    </button>
                </li>
                <li class="d-block d-md-none">
                    <button type="button" class="searchbar-btn" aria-label="Search">
                        <i class="fa fa-search button-fa-icon" aria-hidden="true"></i>
                    </button>
                </li>
                <li>
                <form action="/search" class="searchbar-form search-form">
                   <input type="hidden" name="size" id="metacpan_search-size" value="20">
                  <div>
                      <div class="search-group">
                        <i class="fa fa-search" aria-hidden="true"></i>
                        <input type="text" name="q" placeholder="Search the CPAN" size="41" autocorrect="off" autocapitalize="off" spellcheck="false" id="metacpan_search-input" class="form-control" value="">
                      </div>
                  </div>
                </form>
                </li>
                    <li class="icon-slidepanel d-block d-md-none">
                      <button data-bs-toggle="slidepanel" data-bs-target=".slidepanel" aria-label="Open navigation menu" aria-expanded="false">
                        <span class="button-fa-icon">
                          <i class="fa fa-bars slidepanel-open" aria-hidden="true"></i>
                          <i class="fa fa-times slidepanel-close" aria-hidden="true"></i>
                        </span>
                      </button>
                    </li>
                <li class="dropdown login-dropdown show-logged-in">
                    <button type="button" class="dropdown-toggle" data-bs-toggle="dropdown" aria-label="Account" aria-expanded="false">
                      <i class="fa fa-user button-fa-icon logged-in-icon" aria-hidden="true"></i>
                      <i class="fas fa-chevron-down" aria-hidden="true"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="/account/identities">Identities</a></li>
                        <li><a class="dropdown-item" href="/account/profile">Profile</a></li>
                        <li><a class="dropdown-item" href="/account/favorite/list">Favorites</a></li>
                        <li>
                            <button type="button" class="dropdown-item logout-button">
                              Logout
                            </button>
                        </li>
                    </ul>
                </li>
                <li class="dropdown login-dropdown show-logged-out">
                    <button type="button" class="dropdown-toggle" data-bs-toggle="dropdown" aria-label="Login" aria-expanded="false">
                      <i class="fa fa-user button-fa-icon avatar-placeholder" aria-hidden="true"></i>
                      <i class="fas fa-chevron-down" aria-hidden="true"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <a class="dropdown-item" href="/login/github">
                                <i class="fab fa-github fa-fw" aria-hidden="true"></i>
                                GitHub
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="/login/google">
                                <i class="fab fa-google fa-fw" aria-hidden="true"></i>
                                Google
                            </a>
                        </li>
                    </ul>
                </li>
                <li class="dropdown login-dropdown hide-logged-in hide-logged-out">
                    <button aria-label="Account">
                      <i class="fa fa-user button-fa-icon" aria-hidden="true"></i>
                    </button>
                </li>
            </ul>
        </nav>
        <div class="page-content ">
          <div id="perl-ad-target" class="top-notify-banner perl-ad-target">
          </div>
          <nav class="sidebar" aria-label="Section navigation">
            <div class="slidepanel">
              <ul class="nav-list">

    <li class="nav-header no-margin-top">Distribution</li>
  <li>
    <i class="fas fa-cube sidebar-icon" aria-hidden="true"></i><a href="/dist/Moose">Moose</a>
  </li>
  <li>
    <i class="fas fa-tag sidebar-icon" aria-hidden="true"></i>Module version: 2.4001
  </li>
    <li>
      <i class="far fa-calendar sidebar-icon" aria-hidden="true"></i><span class="ttip" data-bs-toggle="tooltip" data-bs-placement="bottom" title="The date that this version of Moose was released."><span class="relatize">01 Oct 2026 00:35:44 UTC</span></span>
    </li>
    <li>
      <i class="fas fa-scale-balanced sidebar-icon" aria-hidden="true"></i>License: perl_5
    </li>
    <li>
      <i class="fas fa-code sidebar-icon" aria-hidden="true"></i>Perl: v5.8.3
    </li>

    <li><hr></li>
    <li class="nav-header">Code</li>
    <li>
      <i class="fas fa-download sidebar-icon" aria-hidden="true"></i><a itemprop="downloadUrl" href="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.4001.tar.gz">Download (<span itemprop="fileSize">939.74KB</span>)</a>
    </li>
  <li>
    <i class="far fa-file-code sidebar-icon" aria-hidden="true"></i><a data-keyboard-shortcut="g s" href="/dist/Moose/source/lib/Moose.pm">Source</a>
    (<a href="/dist/Moose/source/lib/Moose.pm?raw=1">raw</a>)
  </li>
  <li>
    <i class="far fa-folder-open sidebar-icon" aria-hidden="true"></i><a data-keyboard-shortcut="g b" href="/dist/Moose/source/lib">Browse</a>
    (<a href="/dist/Moose/source/lib?raw=1">raw</a>)
  </li>
    <li>
      <i class="far fa-file-lines sidebar-icon" aria-hidden="true"></i><a data-keyboard-shortcut="g c" href="/dist/Moose/changes">Changes</a>
    </li>

    <li><hr></li>
    <li class="nav-header">Project</li>
    <li>
      <i class="fas fa-house sidebar-icon" aria-hidden="true"></i><a rel="noopener nofollow" class="nopopup" href="http://moose.perl.org/">Homepage</a>
    </li>
    <li>
        <i class="fas fa-code-branch sidebar-icon" aria-hidden="true"></i><a rel="noopener nofollow" data-keyboard-shortcut="g r" href="https://github.com/moose/Moose">Repository</a>
    </li>
    <li>
      <i class="fas fa-circle-exclamation sidebar-icon" aria-hidden="true"></i><a rel="noopener nofollow" data-keyboard-shortcut="g i" href="https://rt.cpan.org/Dist/Display.html?Name=Moose">Issues</a>
      (74)
    </li>
    <li>
      <i class="fas fa-handshake-angle sidebar-icon" aria-hidden="true"></i><a class="nopopup" href="/dist/Moose/contribute">How to Contribute</a>
    </li>
    <li>
      <i class="far fa-comments sidebar-icon" aria-hidden="true"></i><a rel="noopener nofollow" target="_blank" href="https://kiwiirc.com/nextclient/#irc://irc.perl.org/#moose?nick=mc-guest-?">Chat</a>
    </li>

    <li><hr></li>
    <li class="nav-header">Quality</li>
    <li>
      <i class="fas fa-vial sidebar-icon" aria-hidden="true"></i><a rel="noopener nofollow" href="https://fast2-matrix.cpantesters.org/?dist=Moose+2.4001" title="Matrix">Testers</a>
    </li>
    <li>
      <i class="fas fa-crow sidebar-icon" aria-hidden="true"></i><a rel="noopener nofollow" href="https://matrix.perl-magpie.org/dist/Moose/2.4001" title="Magpie">Testers (Magpie)</a>
    </li>
    <li>
      <i class="fas fa-award sidebar-icon" aria-hidden="true"></i><a rel="noopener nofollow" href="https://cpants.cpanauthors.org/release/ETHER/Moose-2.4001">Kwalitee</a>
      <img src="https://cpants.cpanauthors.org/release/ETHER/Moose-2.4001.svg" alt="Kwalitee Score">
    </li>
    <li>
      <span class="ttip" data-bs-toggle="tooltip" data-bs-placement="bottom" title="The # people with an indexing permission on Moose who have released something to CPAN in the last 2 years (i.e. the # people likely able to release critical fixes in a timely manner)">
      <i class="fas fa-users sidebar-icon" aria-hidden="true"></i>Bus factor: 3
      </span>
    </li>

    <li><hr></li>
    <li class="nav-header">Activity</li>
    <li>
<div class="activity-graph">
    <img src="/dist/Moose/activity.svg?res=month" alt="Activity Graph"/>
    <div class="comment">24 month</div>
</div>
    </li>

    <li class="dependencies-wrapper">
<div class="dependencies-card">
<ul class="dependencies">
  <li><button type="button" class="sidebar-toggle-header nav-header" aria-expanded="false" aria-controls="metacpan_dependencies"><i class="fas fa-chevron-right sidebar-toggle-chevron" aria-hidden="true"></i> 24 Dependencies</button></li>
  <li><a href="/pod/Carp" title="Carp" class="dep-name">Carp</a></li>
  <li><a href="/pod/Class::Load" title="Class::Load" class="dep-name">Class::Load</a></li>
  <li><a href="/pod/Class::Load::XS" title="Class::Load::XS" class="dep-name">Class::Load::XS</a></li>
  <li><a href="/pod/Data::OptList" title="Data::OptList" class="dep-name">Data::OptList</a></li>
  <li><a href="/pod/Devel::GlobalDestruction" title="Devel::GlobalDestruction" class="dep-name">Devel::GlobalDestruction</a></li>
  <li class="dep-more-indicator" id="metacpan_dependencies_more"><button type="button" class="btn-link dep-more-btn">and 19 more</button></li>
  <li class="slide-out slide-out-hidden" id="metacpan_dependencies">
    <div>
      <ul>
        <li><a href="/pod/Devel::OverloadInfo" title="Devel::OverloadInfo" class="dep-name">Devel::OverloadInfo</a></li>
        <li><a href="/pod/Devel::StackTrace" title="Devel::StackTrace" class="dep-name">Devel::StackTrace</a></li>
        <li><a href="/pod/Dist::CheckConflicts" title="Dist::CheckConflicts" class="dep-name">Dist::CheckConflicts</a></li>
        <li><a href="/pod/Eval::Closure" title="Eval::Closure" class="dep-name">Eval::Closure</a></li>
        <li><a href="/pod/List::Util" title="List::Util" class="dep-name">List::Util</a></li>
        <li><a href="/pod/MRO::Compat" title="MRO::Compat" class="dep-name">MRO::Compat</a></li>
        <li><a href="/pod/Module::Runtime" title="Module::Runtime" class="dep-name">Module::Runtime</a></li>
        <li><a href="/pod/Module::Runtime::Conflicts" title="Module::Runtime::Conflicts" class="dep-name">Module::Runtime::Conflicts</a></li>
        <li><a href="/pod/Package::DeprecationManager" title="Package::DeprecationManager" class="dep-name">Package::DeprecationManager</a></li>
        <li><a href="/pod/Package::Stash" title="Package::Stash" class="dep-name">Package::Stash</a></li>
        <li><a href="/pod/Package::Stash::XS" title="Package::Stash::XS" class="dep-name">Package::Stash::XS</a></li>
        <li><a href="/pod/Params::Util" title="Params::Util" class="dep-name">Params::Util</a></li>
        <li><a href="/pod/Scalar::Util" title="Scalar::Util" class="dep-name">Scalar::Util</a></li>
        <li><a href="/pod/Sub::Exporter" title="Sub::Exporter" class="dep-name">Sub::Exporter</a></li>
        <li><a href="/pod/Sub::Util" title="Sub::Util" class="dep-name">Sub::Util</a></li>
        <li><a href="/pod/Try::Tiny" title="Try::Tiny" class="dep-name">Try::Tiny</a></li>
        <li><a href="/pod/parent" title="parent" class="dep-name">parent</a></li>
        <li><a href="/pod/strict" title="strict" class="dep-name">strict</a></li>
        <li><a href="/pod/warnings" title="warnings" class="dep-name">warnings</a></li>
      </ul>
    </div>
  </li>
  <li>
    <hr>
  </li>
  <li>
    <a href="/module/Moose/requires">Reverse dependencies</a>
  </li>
  <li>
    <a href="http://deps.cpantesters.org/?module=Moose">CPAN Testers List</a>
  </li>
  <li>
    <a href="https://cpandeps.grinnz.com/?dist=Moose">Dependency graph</a>
  </li>
</ul>
</div>
    </li>

    <li><hr></li>
    <li class="nav-header">Tools</li>
    <li>
      <i class="far fa-compass sidebar-icon" aria-hidden="true"></i><a href="https://explorer.metacpan.org/?url=%2Fmodule%2FETHER%2FMoose-2.4001%2Flib%2FMoose.pm">MetaCPAN Explorer</a>
    </li>
    <li>
      <i class="fas fa-lock sidebar-icon" aria-hidden="true"></i><a href="/dist/Moose/permissions">Permissions</a>
    </li>
    <li>
      <i class="fas fa-rss sidebar-icon" aria-hidden="true"></i><a href="/dist/Moose/releases.rss">Subscribe to distribution</a>
    </li>
    <li>
      <i class="fas fa-terminal sidebar-icon" aria-hidden="true"></i><button class="btn btn-link" data-bs-toggle="modal" data-bs-target="#metacpan_install-instructions-dialog">
        Install Instructions
      </button>
    </li>

    <li><hr></li>
    <li class="nav-header">Find in Distribution</li>
    <li>
      <form action="/search">
        <label for="sidebar-search-dist"><i class="fas fa-magnifying-glass sidebar-icon" aria-hidden="true"></i>search</label>
        <input type="hidden" name="q" value="dist:Moose">
        <input id="sidebar-search-dist" type="search" name="q" placeholder="e.g. method name" class="form-control tool-bar-form">
        <input type="submit" style="display: none">
      </form>
    </li>
    <li>
      <form action="https://grep.metacpan.org/search">
        <label for="sidebar-grep-dist"><i class="fas fa-code sidebar-icon" aria-hidden="true"></i>grep</label>
        <input type="hidden" name="qd" value="Moose">
        <input type="hidden" name="source" value="metacpan">
        <input id="sidebar-grep-dist" type="search" name="q" placeholder="e.g. regex pattern" class="form-control tool-bar-form">
        <input type="submit" style="display: none">
     </form>
    </li>
    <li><hr></li>
    <li class="nav-header">Versions</li>
    <li class="version-jump">
<select class="select-navigator form-control tool-bar-form">
  <option disabled selected>Jump to version</option>
<option
  disabled
  value="/release/ETHER/Moose-2.4001/view/lib/Moose.pm"
>2.4001
  (ETHER on 2026-10-01)</option>
<option
  
  value="/release/ETHER/Moose-2.4000/view/lib/Moose.pm"
>2.4000
  (ETHER on 2025-07-04)</option>
<option
  
  value="/release/ETHER/Moose-2.2207/view/lib/Moose.pm"
>2.2207
  (ETHER on 2024-01-21)</option>
<option
  
  value="/release/DOY/Moose-2.0604/view/lib/Moose.pm"
>2.0604
  (DOY on 2012-09-19) UNAUTHORIZED</option>
<option
  
  value="/release/DOY/Moose-2.0603/view/lib/Moose.pm"
>2.0603
  (DOY on 2012-06-28) UNAUTHORIZED</option>
<option
  
  value="/release/DOY/Moose-2.0602/view/lib/Moose.pm"
>2.0602
  (DOY on 2012-05-07) UNAUTHORIZED</option>
<option
  
  value="/release/FLORA/Moose-2.0204/view/lib/Moose.pm"
>2.0204
  (FLORA on 2011-08-25) UNAUTHORIZED</option>
<option
  
  value="/release/FLORA/Moose-2.0007/view/lib/Moose.pm"
>2.0007
  (FLORA on 2011-05-15) UNAUTHORIZED</option>
<option
  
  value="/release/FLORA/Moose-1.07/view/lib/Moose.pm"
>1.07
  (FLORA on 2010-06-05)</option>
<option
  
  value="/release/FLORA/Moose-1.06/view/lib/Moose.pm"
>1.06
  (FLORA on 2010-06-01)</option>
<option
  
  value="/release/FLORA/Moose-1.05/view/lib/Moose.pm"
>1.05
  (FLORA on 2010-05-20)</option>
<option
  
  value="/release/FLORA/Moose-1.03/view/lib/Moose.pm"
>1.03
  (FLORA on 2010-05-06)</option>
<option
  
  value="/release/FLORA/Moose-1.02/view/lib/Moose.pm"
>1.02
  (FLORA on 2010-05-01)</option>
<option
  
  value="/release/FLORA/Moose-1.01/view/lib/Moose.pm"
>1.01
  (FLORA on 2010-03-26)</option>
<option
  
  value="/release/STEVAN/Moose-1.00/view/lib/Moose.pm"
>1.00
  (STEVAN on 2010-03-25)</option>
<option
  
  value="/release/FLORA/Moose-0.99/view/lib/Moose.pm"
>0.99
  (FLORA on 2010-03-08)</option>
<option
  
  value="/release/FLORA/Moose-0.96/view/lib/Moose.pm"
>0.96
  (FLORA on 2010-02-06)</option>
<option
  
  value="/release/FLORA/Moose-0.95/view/lib/Moose.pm"
>0.95
  (FLORA on 2010-02-04)</option>
<option
  
  value="/release/FLORA/Moose-0.93/view/lib/Moose.pm"
>0.93
  (FLORA on 2009-11-19)</option>
<option
  
  value="/release/STEVAN/Moose-0.01/view/lib/Moose.pm"
>0.01
  (STEVAN on 2006-03-15)</option>
<optgroup label="BackPAN">
<option
  
  value="/release/ETHER/Moose-2.2206/view/lib/Moose.pm"
>2.2206
  (ETHER on 2023-07-23)</option>
<option
  
  value="/release/ETHER/Moose-2.2205/view/lib/Moose.pm"
>2.2205
  (ETHER on 2023-07-23)</option>
<option
  
  value="/release/ETHER/Moose-2.2204/view/lib/Moose.pm"
>2.2204
  (ETHER on 2023-07-23)</option>
<option
  
  value="/release/ETHER/Moose-2.2203/view/lib/Moose.pm"
>2.2203
  (ETHER on 2023-01-22)</option>
<option
  
  value="/release/ETHER/Moose-2.2202/view/lib/Moose.pm"
>2.2202
  (ETHER on 2023-01-14)</option>
<option
  
  value="/release/ETHER/Moose-2.2201/view/lib/Moose.pm"
>2.2201
  (ETHER on 2021-11-07)</option>
<option
  
  value="/release/ETHER/Moose-2.2200/view/lib/Moose.pm"
>2.2200
  (ETHER on 2021-10-31)</option>
<option
  
  value="/release/ETHER/Moose-2.2100-TRIAL/view/lib/Moose.pm"
>2.2100-TRIAL DEV
  (ETHER on 2021-04-13)</option>
<option
  
  value="/release/ETHER/Moose-2.2015/view/lib/Moose.pm"
>2.2015
  (ETHER on 2021-03-31)</option>
<option
  
  value="/release/ETHER/Moose-2.2014/view/lib/Moose.pm"
>2.2014
  (ETHER on 2020-12-19)</option>
<option
  
  value="/release/ETHER/Moose-2.2013/view/lib/Moose.pm"
>2.2013
  (ETHER on 2020-07-21)</option>
<option
  
  value="/release/ETHER/Moose-2.2012/view/lib/Moose.pm"
>2.2012
  (ETHER on 2019-11-22)</option>
<option
  
  value="/release/ETHER/Moose-2.2011/view/lib/Moose.pm"
>2.2011
  (ETHER on 2018-05-16)</option>
<option
  
  value="/release/ETHER/Moose-2.2010/view/lib/Moose.pm"
>2.2010
  (ETHER on 2018-02-16)</option>
<option
  
  value="/release/ETHER/Moose-2.2009/view/lib/Moose.pm"
>2.2009
  (ETHER on 2017-11-29)</option>
<option
  
  value="/release/ETHER/Moose-2.2008/view/lib/Moose.pm"
>2.2008
  (ETHER on 2017-11-21)</option>
<option
  
  value="/release/ETHER/Moose-2.2007/view/lib/Moose.pm"
>2.2007
  (ETHER on 2017-11-12)</option>
<option
  
  value="/release/ETHER/Moose-2.2006/view/lib/Moose.pm"
>2.2006
  (ETHER on 2017-07-12)</option>
<option
  
  value="/release/ETHER/Moose-2.2005/view/lib/Moose.pm"
>2.2005
  (ETHER on 2017-05-03)</option>
<option
  
  value="/release/ETHER/Moose-2.2004/view/lib/Moose.pm"
>2.2004
  (ETHER on 2017-01-31)</option>
<option
  
  value="/release/ETHER/Moose-2.2003/view/lib/Moose.pm"
>2.2003
  (ETHER on 2017-01-30)</option>
<option
  
  value="/release/ETHER/Moose-2.2002/view/lib/Moose.pm"
>2.2002
  (ETHER on 2017-01-30)</option>
<option
  
  value="/release/ETHER/Moose-2.2001/view/lib/Moose.pm"
>2.2001
  (ETHER on 2017-01-29)</option>
<option
  
  value="/release/ETHER/Moose-2.2000/view/lib/Moose.pm"
>2.2000
  (ETHER on 2017-01-29)</option>
<option
  
  value="/release/ETHER/Moose-2.1905-TRIAL/view/lib/Moose.pm"
>2.1905-TRIAL DEV
  (ETHER on 2017-01-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1904-TRIAL/view/lib/Moose.pm"
>2.1904-TRIAL DEV
  (ETHER on 2016-12-22)</option>
<option
  
  value="/release/ETHER/Moose-2.1807/view/lib/Moose.pm"
>2.1807
  (ETHER on 2016-12-22)</option>
<option
  
  value="/release/ETHER/Moose-2.1903-TRIAL/view/lib/Moose.pm"
>2.1903-TRIAL DEV
  (ETHER on 2016-11-22)</option>
<option
  
  value="/release/ETHER/Moose-2.1902-TRIAL/view/lib/Moose.pm"
>2.1902-TRIAL DEV
  (ETHER on 2016-10-23)</option>
<option
  
  value="/release/ETHER/Moose-2.1901-TRIAL/view/lib/Moose.pm"
>2.1901-TRIAL DEV
  (ETHER on 2016-10-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1900-TRIAL/view/lib/Moose.pm"
>2.1900-TRIAL DEV
  (ETHER on 2016-10-09)</option>
<option
  
  value="/release/ETHER/Moose-2.1806/view/lib/Moose.pm"
>2.1806
  (ETHER on 2016-09-25)</option>
<option
  
  value="/release/ETHER/Moose-2.1805/view/lib/Moose.pm"
>2.1805
  (ETHER on 2016-08-19)</option>
<option
  
  value="/release/ETHER/Moose-2.1804/view/lib/Moose.pm"
>2.1804
  (ETHER on 2016-06-02)</option>
<option
  
  value="/release/ETHER/Moose-2.1803/view/lib/Moose.pm"
>2.1803
  (ETHER on 2016-05-31)</option>
<option
  
  value="/release/ETHER/Moose-2.1802/view/lib/Moose.pm"
>2.1802
  (ETHER on 2016-05-25)</option>
<option
  
  value="/release/ETHER/Moose-2.1801/view/lib/Moose.pm"
>2.1801
  (ETHER on 2016-05-02)</option>
<option
  
  value="/release/ETHER/Moose-2.1800/view/lib/Moose.pm"
>2.1800
  (ETHER on 2016-04-30)</option>
<option
  
  value="/release/ETHER/Moose-2.1705-TRIAL/view/lib/Moose.pm"
>2.1705-TRIAL DEV
  (ETHER on 2016-04-21)</option>
<option
  
  value="/release/ETHER/Moose-2.1704-TRIAL/view/lib/Moose.pm"
>2.1704-TRIAL DEV
  (ETHER on 2016-04-13)</option>
<option
  
  value="/release/ETHER/Moose-2.1703-TRIAL/view/lib/Moose.pm"
>2.1703-TRIAL DEV
  (ETHER on 2016-04-13)</option>
<option
  
  value="/release/ETHER/Moose-2.1702-TRIAL/view/lib/Moose.pm"
>2.1702-TRIAL DEV
  (ETHER on 2016-04-08)</option>
<option
  
  value="/release/ETHER/Moose-2.1701-TRIAL/view/lib/Moose.pm"
>2.1701-TRIAL DEV
  (ETHER on 2016-04-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1700-TRIAL/view/lib/Moose.pm"
>2.1700-TRIAL DEV
  (ETHER on 2016-04-06)</option>
<option
  
  value="/release/ETHER/Moose-2.1605/view/lib/Moose.pm"
>2.1605
  (ETHER on 2016-02-16)</option>
<option
  
  value="/release/ETHER/Moose-2.1604/view/lib/Moose.pm"
>2.1604
  (ETHER on 2015-11-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1603/view/lib/Moose.pm"
>2.1603
  (ETHER on 2015-08-28)</option>
<option
  
  value="/release/ETHER/Moose-2.1602-TRIAL/view/lib/Moose.pm"
>2.1602-TRIAL DEV
  (ETHER on 2015-08-14)</option>
<option
  
  value="/release/ETHER/Moose-2.1601-TRIAL/view/lib/Moose.pm"
>2.1601-TRIAL DEV
  (ETHER on 2015-08-10)</option>
<option
  
  value="/release/ETHER/Moose-2.1600/view/lib/Moose.pm"
>2.1600
  (ETHER on 2015-07-31)</option>
<option
  
  value="/release/ETHER/Moose-2.1501-TRIAL/view/lib/Moose.pm"
>2.1501-TRIAL DEV
  (ETHER on 2015-07-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1500-TRIAL/view/lib/Moose.pm"
>2.1500-TRIAL DEV
  (ETHER on 2015-07-01)</option>
<option
  
  value="/release/ETHER/Moose-2.1405/view/lib/Moose.pm"
>2.1405
  (ETHER on 2015-06-06)</option>
<option
  
  value="/release/ETHER/Moose-2.1404/view/lib/Moose.pm"
>2.1404
  (ETHER on 2015-04-16)</option>
<option
  
  value="/release/ETHER/Moose-2.1403/view/lib/Moose.pm"
>2.1403
  (ETHER on 2014-12-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1402/view/lib/Moose.pm"
>2.1402
  (ETHER on 2014-11-05)</option>
<option
  
  value="/release/ETHER/Moose-2.1401/view/lib/Moose.pm"
>2.1401
  (ETHER on 2014-11-03)</option>
<option
  
  value="/release/ETHER/Moose-2.1400/view/lib/Moose.pm"
>2.1400
  (ETHER on 2014-11-01)</option>
<option
  
  value="/release/ETHER/Moose-2.1307-TRIAL/view/lib/Moose.pm"
>2.1307-TRIAL DEV
  (ETHER on 2014-10-26)</option>
<option
  
  value="/release/ETHER/Moose-2.1306-TRIAL/view/lib/Moose.pm"
>2.1306-TRIAL DEV
  (ETHER on 2014-10-25)</option>
<option
  
  value="/release/ETHER/Moose-2.1305-TRIAL/view/lib/Moose.pm"
>2.1305-TRIAL DEV
  (ETHER on 2014-10-23)</option>
<option
  
  value="/release/ETHER/Moose-2.1304-TRIAL/view/lib/Moose.pm"
>2.1304-TRIAL DEV
  (ETHER on 2014-09-25)</option>
<option
  
  value="/release/ETHER/Moose-2.1213/view/lib/Moose.pm"
>2.1213
  (ETHER on 2014-09-25)</option>
<option
  
  value="/release/ETHER/Moose-2.1303-TRIAL/view/lib/Moose.pm"
>2.1303-TRIAL DEV
  (ETHER on 2014-09-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1212/view/lib/Moose.pm"
>2.1212
  (ETHER on 2014-09-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1302-TRIAL/view/lib/Moose.pm"
>2.1302-TRIAL DEV
  (ETHER on 2014-08-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1301-TRIAL/view/lib/Moose.pm"
>2.1301-TRIAL DEV
  (ETHER on 2014-08-19)</option>
<option
  
  value="/release/ETHER/Moose-2.1300-TRIAL/view/lib/Moose.pm"
>2.1300-TRIAL DEV
  (ETHER on 2014-08-12)</option>
<option
  
  value="/release/ETHER/Moose-2.1211/view/lib/Moose.pm"
>2.1211
  (ETHER on 2014-08-11)</option>
<option
  
  value="/release/ETHER/Moose-2.1210/view/lib/Moose.pm"
>2.1210
  (ETHER on 2014-07-03)</option>
<option
  
  value="/release/ETHER/Moose-2.1209/view/lib/Moose.pm"
>2.1209
  (ETHER on 2014-06-05)</option>
<option
  
  value="/release/ETHER/Moose-2.1208/view/lib/Moose.pm"
>2.1208
  (ETHER on 2014-06-01)</option>
<option
  
  value="/release/ETHER/Moose-2.1207/view/lib/Moose.pm"
>2.1207
  (ETHER on 2014-05-26)</option>
<option
  
  value="/release/ETHER/Moose-2.1206/view/lib/Moose.pm"
>2.1206
  (ETHER on 2014-05-14)</option>
<option
  
  value="/release/ETHER/Moose-2.1205/view/lib/Moose.pm"
>2.1205
  (ETHER on 2014-04-16)</option>
<option
  
  value="/release/ETHER/Moose-2.1204/view/lib/Moose.pm"
>2.1204
  (ETHER on 2014-02-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1203/view/lib/Moose.pm"
>2.1203
  (ETHER on 2014-02-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1202/view/lib/Moose.pm"
>2.1202
  (ETHER on 2014-01-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1201/view/lib/Moose.pm"
>2.1201
  (ETHER on 2014-01-11)</option>
<option
  
  value="/release/ETHER/Moose-2.1200/view/lib/Moose.pm"
>2.1200
  (ETHER on 2014-01-06)</option>
<option
  
  value="/release/ETHER/Moose-2.1108-TRIAL/view/lib/Moose.pm"
>2.1108-TRIAL DEV
  (ETHER on 2014-01-05)</option>
<option
  
  value="/release/ETHER/Moose-2.1107-TRIAL/view/lib/Moose.pm"
>2.1107-TRIAL DEV
  (ETHER on 2013-11-29)</option>
<option
  
  value="/release/ETHER/Moose-2.1106-TRIAL/view/lib/Moose.pm"
>2.1106-TRIAL DEV
  (ETHER on 2013-11-05)</option>
<option
  
  value="/release/ETHER/Moose-2.1105-TRIAL/view/lib/Moose.pm"
>2.1105-TRIAL DEV
  (ETHER on 2013-10-31)</option>
<option
  
  value="/release/ETHER/Moose-2.1104-TRIAL/view/lib/Moose.pm"
>2.1104-TRIAL DEV
  (ETHER on 2013-10-30)</option>
<option
  
  value="/release/ETHER/Moose-2.1103-TRIAL/view/lib/Moose.pm"
>2.1103-TRIAL DEV
  (ETHER on 2013-10-26)</option>
<option
  
  value="/release/ETHER/Moose-2.1102-TRIAL/view/lib/Moose.pm"
>2.1102-TRIAL DEV
  (ETHER on 2013-10-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1101-TRIAL/view/lib/Moose.pm"
>2.1101-TRIAL DEV
  (ETHER on 2013-10-20)</option>
<option
  
  value="/release/ETHER/Moose-2.1100-TRIAL/view/lib/Moose.pm"
>2.1100-TRIAL DEV
  (ETHER on 2013-09-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1005/view/lib/Moose.pm"
>2.1005
  (ETHER on 2013-08-07)</option>
<option
  
  value="/release/ETHER/Moose-2.1004/view/lib/Moose.pm"
>2.1004
  (ETHER on 2013-07-26)</option>
<option
  
  value="/release/ETHER/Moose-2.1003/view/lib/Moose.pm"
>2.1003
  (ETHER on 2013-07-26)</option>
<option
  
  value="/release/ETHER/Moose-2.0901-TRIAL/view/lib/Moose.pm"
>2.0901-TRIAL DEV
  (ETHER on 2013-06-21)</option>
<option
  
  value="/release/ETHER/Moose-2.0900-TRIAL/view/lib/Moose.pm"
>2.0900-TRIAL DEV
  (ETHER on 2013-05-27)</option>
<option
  
  value="/release/ETHER/Moose-2.1002-TRIAL/view/lib/Moose.pm"
>2.1002-TRIAL DEV
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.1001/view/lib/Moose.pm"
>2.1001
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.1000/view/lib/Moose.pm"
>2.1000
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.0803/view/lib/Moose.pm"
>2.0803
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.0802/view/lib/Moose.pm"
>2.0802
  (ETHER on 2013-05-07)</option>
<option
  
  value="/release/ETHER/Moose-2.0801/view/lib/Moose.pm"
>2.0801
  (ETHER on 2013-03-28)</option>
<option
  
  value="/release/ETHER/Moose-2.0800/view/lib/Moose.pm"
>2.0800
  (ETHER on 2013-03-28)</option>
<option
  
  value="/release/DOY/Moose-2.0601/view/lib/Moose.pm"
>2.0601
  (DOY on 2012-05-01)</option>
<option
  
  value="/release/DOY/Moose-2.0600/view/lib/Moose.pm"
>2.0600
  (DOY on 2012-04-29)</option>
<option
  
  value="/release/DOY/Moose-2.0502-TRIAL/view/lib/Moose.pm"
>2.0502-TRIAL DEV
  (DOY on 2012-04-25)</option>
<option
  
  value="/release/DOY/Moose-2.0501-TRIAL/view/lib/Moose.pm"
>2.0501-TRIAL DEV
  (DOY on 2012-04-03)</option>
<option
  
  value="/release/DOY/Moose-2.0403/view/lib/Moose.pm"
>2.0403
  (DOY on 2012-04-03)</option>
<option
  
  value="/release/DOY/Moose-2.0500-TRIAL/view/lib/Moose.pm"
>2.0500-TRIAL DEV
  (DOY on 2012-04-03)</option>
<option
  
  value="/release/DOY/Moose-2.0402/view/lib/Moose.pm"
>2.0402
  (DOY on 2012-02-04)</option>
<option
  
  value="/release/DOY/Moose-2.0401/view/lib/Moose.pm"
>2.0401
  (DOY on 2011-11-17)</option>
<option
  
  value="/release/DOY/Moose-2.0400/view/lib/Moose.pm"
>2.0400
  (DOY on 2011-11-15)</option>
<option
  
  value="/release/DOY/Moose-2.0302-TRIAL/view/lib/Moose.pm"
>2.0302-TRIAL DEV
  (DOY on 2011-11-02)</option>
<option
  
  value="/release/DOY/Moose-2.0301-TRIAL/view/lib/Moose.pm"
>2.0301-TRIAL DEV
  (DOY on 2011-10-21)</option>
<option
  
  value="/release/DOY/Moose-2.0300-TRIAL/view/lib/Moose.pm"
>2.0300-TRIAL DEV
  (DOY on 2011-09-24)</option>
<option
  
  value="/release/DOY/Moose-2.0205/view/lib/Moose.pm"
>2.0205
  (DOY on 2011-09-06)</option>
<option
  
  value="/release/DOY/Moose-2.0203/view/lib/Moose.pm"
>2.0203
  (DOY on 2011-08-24)</option>
<option
  
  value="/release/DOY/Moose-2.0202/view/lib/Moose.pm"
>2.0202
  (DOY on 2011-07-26)</option>
<option
  
  value="/release/DOY/Moose-2.0201/view/lib/Moose.pm"
>2.0201
  (DOY on 2011-07-22)</option>
<option
  
  value="/release/DOY/Moose-2.0200/view/lib/Moose.pm"
>2.0200
  (DOY on 2011-07-18)</option>
<option
  
  value="/release/DOY/Moose-2.0105-TRIAL/view/lib/Moose.pm"
>2.0105-TRIAL DEV
  (DOY on 2011-06-27)</option>
<option
  
  value="/release/DOY/Moose-2.0104-TRIAL/view/lib/Moose.pm"
>2.0104-TRIAL DEV
  (DOY on 2011-06-20)</option>
<option
  
  value="/release/DOY/Moose-2.0010/view/lib/Moose.pm"
>2.0010
  (DOY on 2011-06-20)</option>
<option
  
  value="/release/DOY/Moose-2.0103-TRIAL/view/lib/Moose.pm"
>2.0103-TRIAL DEV
  (DOY on 2011-06-20)</option>
<option
  
  value="/release/DOY/Moose-2.0009/view/lib/Moose.pm"
>2.0009
  (DOY on 2011-06-19)</option>
<option
  
  value="/release/DOY/Moose-2.0102-TRIAL/view/lib/Moose.pm"
>2.0102-TRIAL DEV
  (DOY on 2011-06-18)</option>
<option
  
  value="/release/DOY/Moose-2.0008/view/lib/Moose.pm"
>2.0008
  (DOY on 2011-06-16)</option>
<option
  
  value="/release/DOY/Moose-2.0101-TRIAL/view/lib/Moose.pm"
>2.0101-TRIAL DEV
  (DOY on 2011-06-06)</option>
<option
  
  value="/release/DOY/Moose-2.0100-TRIAL/view/lib/Moose.pm"
>2.0100-TRIAL DEV
  (DOY on 2011-06-06)</option>
<option
  
  value="/release/DOY/Moose-2.0006/view/lib/Moose.pm"
>2.0006
  (DOY on 2011-05-10)</option>
<option
  
  value="/release/DOY/Moose-2.0005/view/lib/Moose.pm"
>2.0005
  (DOY on 2011-05-09)</option>
<option
  
  value="/release/DOY/Moose-2.0004/view/lib/Moose.pm"
>2.0004
  (DOY on 2011-05-09)</option>
<option
  
  value="/release/DOY/Moose-2.0003/view/lib/Moose.pm"
>2.0003
  (DOY on 2011-05-09)</option>
<option
  
  value="/release/DOY/Moose-2.0002/view/lib/Moose.pm"
>2.0002
  (DOY on 2011-04-29)</option>
<option
  
  value="/release/DOY/Moose-2.0001/view/lib/Moose.pm"
>2.0001
  (DOY on 2011-04-23)</option>
<option
  
  value="/release/DOY/Moose-2.0000/view/lib/Moose.pm"
>2.0000
  (DOY on 2011-04-12)</option>
<option
  
  value="/release/DOY/Moose-1.9906-TRIAL/view/lib/Moose.pm"
>1.9906-TRIAL DEV
  (DOY on 2011-04-05)</option>
<option
  
  value="/release/DROLSKY/Moose-1.25/view/lib/Moose.pm"
>1.25
  (DROLSKY on 2011-04-02)</option>
<option
  
  value="/release/DOY/Moose-1.9905-TRIAL/view/lib/Moose.pm"
>1.9905-TRIAL DEV
  (DOY on 2011-03-28)</option>
<option
  
  value="/release/DOY/Moose-1.9904-TRIAL/view/lib/Moose.pm"
>1.9904-TRIAL DEV
  (DOY on 2011-03-04)</option>
<option
  
  value="/release/DOY/Moose-1.9903-TRIAL/view/lib/Moose.pm"
>1.9903-TRIAL DEV
  (DOY on 2011-02-28)</option>
<option
  
  value="/release/DROLSKY/Moose-1.24/view/lib/Moose.pm"
>1.24
  (DROLSKY on 2011-02-23)</option>
<option
  
  value="/release/DROLSKY/Moose-1.23/view/lib/Moose.pm"
>1.23
  (DROLSKY on 2011-02-14)</option>
<option
  
  value="/release/DROLSKY/Moose-1.22/view/lib/Moose.pm"
>1.22
  (DROLSKY on 2011-02-13)</option>
<option
  
  value="/release/DOY/Moose-1.9902-TRIAL/view/lib/Moose.pm"
>1.9902-TRIAL DEV
  (DOY on 2011-01-03)</option>
<option
  
  value="/release/DOY/Moose-1.9901-TRIAL/view/lib/Moose.pm"
>1.9901-TRIAL DEV
  (DOY on 2011-01-03)</option>
<option
  
  value="/release/DOY/Moose-1.9900-TRIAL/view/lib/Moose.pm"
>1.9900-TRIAL DEV
  (DOY on 2011-01-01)</option>
<option
  
  value="/release/DROLSKY/Moose-1.21/view/lib/Moose.pm"
>1.21
  (DROLSKY on 2010-11-24)</option>
<option
  
  value="/release/DROLSKY/Moose-1.20/view/lib/Moose.pm"
>1.20
  (DROLSKY on 2010-11-19)</option>
<option
  
  value="/release/DROLSKY/Moose-1.19/view/lib/Moose.pm"
>1.19
  (DROLSKY on 2010-11-02)</option>
<option
  
  value="/release/DROLSKY/Moose-1.18/view/lib/Moose.pm"
>1.18
  (DROLSKY on 2010-10-31)</option>
<option
  
  value="/release/DROLSKY/Moose-1.17/view/lib/Moose.pm"
>1.17
  (DROLSKY on 2010-10-19)</option>
<option
  
  value="/release/DROLSKY/Moose-1.16/view/lib/Moose.pm"
>1.16
  (DROLSKY on 2010-10-18)</option>
<option
  
  value="/release/DROLSKY/Moose-1.15/view/lib/Moose.pm"
>1.15
  (DROLSKY on 2010-10-05)</option>
<option
  
  value="/release/DROLSKY/Moose-1.14/view/lib/Moose.pm"
>1.14
  (DROLSKY on 2010-09-21)</option>
<option
  
  value="/release/DROLSKY/Moose-1.13/view/lib/Moose.pm"
>1.13
  (DROLSKY on 2010-09-13)</option>
<option
  
  value="/release/DROLSKY/Moose-1.12/view/lib/Moose.pm"
>1.12
  (DROLSKY on 2010-08-28)</option>
<option
  
  value="/release/DROLSKY/Moose-1.11/view/lib/Moose.pm"
>1.11
  (DROLSKY on 2010-08-28)</option>
<option
  
  value="/release/DROLSKY/Moose-1.10/view/lib/Moose.pm"
>1.10
  (DROLSKY on 2010-08-22)</option>
<option
  
  value="/release/DROLSKY/Moose-1.09/view/lib/Moose.pm"
>1.09
  (DROLSKY on 2010-07-25)</option>
<option
  
  value="/release/DOY/Moose-1.08/view/lib/Moose.pm"
>1.08
  (DOY on 2010-06-15)</option>
<option
  
  value="/release/FLORA/Moose-1.04/view/lib/Moose.pm"
>1.04
  (FLORA on 2010-05-20)</option>
<option
  
  value="/release/DROLSKY/Moose-0.98/view/lib/Moose.pm"
>0.98
  (DROLSKY on 2010-02-10)</option>
<option
  
  value="/release/DROLSKY/Moose-0.97/view/lib/Moose.pm"
>0.97
  (DROLSKY on 2010-02-10)</option>
<option
  
  value="/release/DROLSKY/Moose-0.94/view/lib/Moose.pm"
>0.94
  (DROLSKY on 2010-01-18)</option>
<option
  
  value="/release/DROLSKY/Moose-0.93_03/view/lib/Moose.pm"
>0.93_03 DEV
  (DROLSKY on 2010-01-05)</option>
<option
  
  value="/release/DROLSKY/Moose-0.93_02/view/lib/Moose.pm"
>0.93_02 DEV
  (DROLSKY on 2010-01-05)</option>
<option
  
  value="/release/DROLSKY/Moose-0.93_01/view/lib/Moose.pm"
>0.93_01 DEV
  (DROLSKY on 2010-01-04)</option>
<option
  
  value="/release/DROLSKY/Moose-0.92/view/lib/Moose.pm"
>0.92
  (DROLSKY on 2009-09-22)</option>
<option
  
  value="/release/DROLSKY/Moose-0.91/view/lib/Moose.pm"
>0.91
  (DROLSKY on 2009-09-20)</option>
<option
  
  value="/release/DROLSKY/Moose-0.90/view/lib/Moose.pm"
>0.90
  (DROLSKY on 2009-09-15)</option>
<option
  
  value="/release/DROLSKY/Moose-0.89_02/view/lib/Moose.pm"
>0.89_02 DEV
  (DROLSKY on 2009-09-11)</option>
<option
  
  value="/release/DROLSKY/Moose-0.89_01/view/lib/Moose.pm"
>0.89_01 DEV
  (DROLSKY on 2009-09-02)</option>
<option
  
  value="/release/DROLSKY/Moose-0.89/view/lib/Moose.pm"
>0.89
  (DROLSKY on 2009-08-13)</option>
<option
  
  value="/release/DROLSKY/Moose-0.88/view/lib/Moose.pm"
>0.88
  (DROLSKY on 2009-07-24)</option>
<option
  
  value="/release/DROLSKY/Moose-0.87/view/lib/Moose.pm"
>0.87
  (DROLSKY on 2009-07-07)</option>
<option
  
  value="/release/DROLSKY/Moose-0.86/view/lib/Moose.pm"
>0.86
  (DROLSKY on 2009-07-03)</option>
<option
  
  value="/release/DROLSKY/Moose-0.85/view/lib/Moose.pm"
>0.85
  (DROLSKY on 2009-06-26)</option>
<option
  
  value="/release/DROLSKY/Moose-0.84/view/lib/Moose.pm"
>0.84
  (DROLSKY on 2009-06-26)</option>
<option
  
  value="/release/DROLSKY/Moose-0.83/view/lib/Moose.pm"
>0.83
  (DROLSKY on 2009-06-23)</option>
<option
  
  value="/release/DROLSKY/Moose-0.82/view/lib/Moose.pm"
>0.82
  (DROLSKY on 2009-06-21)</option>
<option
  
  value="/release/DROLSKY/Moose-0.81/view/lib/Moose.pm"
>0.81
  (DROLSKY on 2009-06-07)</option>
<option
  
  value="/release/DROLSKY/Moose-0.80/view/lib/Moose.pm"
>0.80
  (DROLSKY on 2009-06-06)</option>
<option
  
  value="/release/DROLSKY/Moose-0.79/view/lib/Moose.pm"
>0.79
  (DROLSKY on 2009-05-13)</option>
<option
  
  value="/release/DROLSKY/Moose-0.78/view/lib/Moose.pm"
>0.78
  (DROLSKY on 2009-05-12)</option>
<option
  
  value="/release/DROLSKY/Moose-0.77/view/lib/Moose.pm"
>0.77
  (DROLSKY on 2009-05-02)</option>
<option
  
  value="/release/DROLSKY/Moose-0.76/view/lib/Moose.pm"
>0.76
  (DROLSKY on 2009-04-27)</option>
<option
  
  value="/release/DROLSKY/Moose-0.75_01/view/lib/Moose.pm"
>0.75_01 DEV
  (DROLSKY on 2009-04-23)</option>
<option
  
  value="/release/DROLSKY/Moose-0.75/view/lib/Moose.pm"
>0.75
  (DROLSKY on 2009-04-20)</option>
<option
  
  value="/release/DROLSKY/Moose-0.74/view/lib/Moose.pm"
>0.74
  (DROLSKY on 2009-04-07)</option>
<option
  
  value="/release/DROLSKY/Moose-0.73_02/view/lib/Moose.pm"
>0.73_02 DEV
  (DROLSKY on 2009-04-06)</option>
<option
  
  value="/release/DROLSKY/Moose-0.73_01/view/lib/Moose.pm"
>0.73_01 DEV
  (DROLSKY on 2009-04-05)</option>
<option
  
  value="/release/DROLSKY/Moose-0.73/view/lib/Moose.pm"
>0.73
  (DROLSKY on 2009-03-27)</option>
<option
  
  value="/release/DROLSKY/Moose-0.72_01/view/lib/Moose.pm"
>0.72_01 DEV
  (DROLSKY on 2009-03-26)</option>
<option
  
  value="/release/DROLSKY/Moose-0.72/view/lib/Moose.pm"
>0.72
  (DROLSKY on 2009-02-24)</option>
<option
  
  value="/release/DROLSKY/Moose-0.71_01/view/lib/Moose.pm"
>0.71_01 DEV
  (DROLSKY on 2009-02-22)</option>
<option
  
  value="/release/DROLSKY/Moose-0.71/view/lib/Moose.pm"
>0.71
  (DROLSKY on 2009-02-19)</option>
<option
  
  value="/release/DROLSKY/Moose-0.70/view/lib/Moose.pm"
>0.70
  (DROLSKY on 2009-02-14)</option>
<option
  
  value="/release/DROLSKY/Moose-0.69/view/lib/Moose.pm"
>0.69
  (DROLSKY on 2009-02-12)</option>
<option
  
  value="/release/DROLSKY/Moose-0.68/view/lib/Moose.pm"
>0.68
  (DROLSKY on 2009-02-04)</option>
<option
  
  value="/release/DROLSKY/Moose-0.67/view/lib/Moose.pm"
>0.67
  (DROLSKY on 2009-02-04)</option>
<option
  
  value="/release/DROLSKY/Moose-0.66/view/lib/Moose.pm"
>0.66
  (DROLSKY on 2009-02-03)</option>
<option
  
  value="/release/DROLSKY/Moose-0.65/view/lib/Moose.pm"
>0.65
  (DROLSKY on 2009-01-22)</option>
<option
  
  value="/release/DROLSKY/Moose-0.64/view/lib/Moose.pm"
>0.64
  (DROLSKY on 2008-12-31)</option>
<option
  
  value="/release/DROLSKY/Moose-0.63/view/lib/Moose.pm"
>0.63
  (DROLSKY on 2008-12-08)</option>
<option
  
  value="/release/DROLSKY/Moose-0.62_02/view/lib/Moose.pm"
>0.62_02 DEV
  (DROLSKY on 2008-12-05)</option>
<option
  
  value="/release/DROLSKY/Moose-0.62_01/view/lib/Moose.pm"
>0.62_01 DEV
  (DROLSKY on 2008-12-04)</option>
<option
  
  value="/release/DROLSKY/Moose-0.62/view/lib/Moose.pm"
>0.62
  (DROLSKY on 2008-11-26)</option>
<option
  
  value="/release/DROLSKY/Moose-0.61/view/lib/Moose.pm"
>0.61
  (DROLSKY on 2008-11-07)</option>
<option
  
  value="/release/DROLSKY/Moose-0.60/view/lib/Moose.pm"
>0.60
  (DROLSKY on 2008-10-24)</option>
<option
  
  value="/release/DROLSKY/Moose-0.59/view/lib/Moose.pm"
>0.59
  (DROLSKY on 2008-10-14)</option>
<option
  
  value="/release/DROLSKY/Moose-0.58/view/lib/Moose.pm"
>0.58
  (DROLSKY on 2008-09-20)</option>
<option
  
  value="/release/DROLSKY/Moose-0.57/view/lib/Moose.pm"
>0.57
  (DROLSKY on 2008-09-03)</option>
<option
  
  value="/release/DROLSKY/Moose-0.56/view/lib/Moose.pm"
>0.56
  (DROLSKY on 2008-09-01)</option>
<option
  
  value="/release/DROLSKY/Moose-0.55_04/view/lib/Moose.pm"
>0.55_04 DEV
  (DROLSKY on 2008-08-31)</option>
<option
  
  value="/release/DROLSKY/Moose-0.55_03/view/lib/Moose.pm"
>0.55_03 DEV
  (DROLSKY on 2008-08-30)</option>
<option
  
  value="/release/DROLSKY/Moose-0.55_02/view/lib/Moose.pm"
>0.55_02 DEV
  (DROLSKY on 2008-08-29)</option>
<option
  
  value="/release/DROLSKY/Moose-0.55_01/view/lib/Moose.pm"
>0.55_01 DEV
  (DROLSKY on 2008-08-20)</option>
<option
  
  value="/release/SARTAK/Moose-0.55/view/lib/Moose.pm"
>0.55
  (SARTAK on 2008-08-04)</option>
<option
  
  value="/release/STEVAN/Moose-0.54/view/lib/Moose.pm"
>0.54
  (STEVAN on 2008-07-04)</option>
<option
  
  value="/release/STEVAN/Moose-0.53/view/lib/Moose.pm"
>0.53
  (STEVAN on 2008-07-03)</option>
<option
  
  value="/release/STEVAN/Moose-0.52/view/lib/Moose.pm"
>0.52
  (STEVAN on 2008-07-03)</option>
<option
  
  value="/release/SARTAK/Moose-0.51/view/lib/Moose.pm"
>0.51
  (SARTAK on 2008-06-27)</option>
<option
  
  value="/release/SARTAK/Moose-0.50/view/lib/Moose.pm"
>0.50
  (SARTAK on 2008-06-13)</option>
<option
  
  value="/release/SARTAK/Moose-0.49/view/lib/Moose.pm"
>0.49
  (SARTAK on 2008-06-13)</option>
<option
  
  value="/release/STEVAN/Moose-0.48/view/lib/Moose.pm"
>0.48
  (STEVAN on 2008-05-29)</option>
<option
  
  value="/release/STEVAN/Moose-0.47/view/lib/Moose.pm"
>0.47
  (STEVAN on 2008-05-29)</option>
<option
  
  value="/release/STEVAN/Moose-0.46/view/lib/Moose.pm"
>0.46
  (STEVAN on 2008-05-28)</option>
<option
  
  value="/release/STEVAN/Moose-0.45/view/lib/Moose.pm"
>0.45
  (STEVAN on 2008-05-25)</option>
<option
  
  value="/release/STEVAN/Moose-0.44/view/lib/Moose.pm"
>0.44
  (STEVAN on 2008-05-11)</option>
<option
  
  value="/release/STEVAN/Moose-0.43/view/lib/Moose.pm"
>0.43
  (STEVAN on 2008-04-30)</option>
<option
  
  value="/release/STEVAN/Moose-0.42/view/lib/Moose.pm"
>0.42
  (STEVAN on 2008-04-29)</option>
<option
  
  value="/release/STEVAN/Moose-0.41/view/lib/Moose.pm"
>0.41
  (STEVAN on 2008-04-28)</option>
<option
  
  value="/release/STEVAN/Moose-0.40/view/lib/Moose.pm"
>0.40
  (STEVAN on 2008-03-15)</option>
<option
  
  value="/release/STEVAN/Moose-0.39/view/lib/Moose.pm"
>0.39
  (STEVAN on 2008-03-14)</option>
<option
  
  value="/release/STEVAN/Moose-0.38/view/lib/Moose.pm"
>0.38
  (STEVAN on 2008-02-15)</option>
<option
  
  value="/release/STEVAN/Moose-0.37/view/lib/Moose.pm"
>0.37
  (STEVAN on 2008-02-14)</option>
<option
  
  value="/release/STEVAN/Moose-0.36/view/lib/Moose.pm"
>0.36
  (STEVAN on 2008-01-26)</option>
<option
  
  value="/release/STEVAN/Moose-0.35/view/lib/Moose.pm"
>0.35
  (STEVAN on 2008-01-23)</option>
<option
  
  value="/release/STEVAN/Moose-0.34/view/lib/Moose.pm"
>0.34
  (STEVAN on 2008-01-21)</option>
<option
  
  value="/release/STEVAN/Moose-0.33/view/lib/Moose.pm"
>0.33
  (STEVAN on 2007-12-14)</option>
<option
  
  value="/release/STEVAN/Moose-0.32/view/lib/Moose.pm"
>0.32
  (STEVAN on 2007-12-04)</option>
<option
  
  value="/release/STEVAN/Moose-0.31/view/lib/Moose.pm"
>0.31
  (STEVAN on 2007-11-26)</option>
<option
  
  value="/release/STEVAN/Moose-0.30/view/lib/Moose.pm"
>0.30
  (STEVAN on 2007-11-23)</option>
<option
  
  value="/release/GRODITI/Moose-0.29/view/lib/Moose.pm"
>0.29
  (GRODITI on 2007-11-13)</option>
<option
  
  value="/release/GRODITI/Moose-0.28/view/lib/Moose.pm"
>0.28
  (GRODITI on 2007-11-13)</option>
<option
  
  value="/release/GRODITI/Moose-0.27/view/lib/Moose.pm"
>0.27
  (GRODITI on 2007-11-13)</option>
<option
  
  value="/release/STEVAN/Moose-0.26/view/lib/Moose.pm"
>0.26
  (STEVAN on 2007-09-27)</option>
<option
  
  value="/release/STEVAN/Moose-0.25/view/lib/Moose.pm"
>0.25
  (STEVAN on 2007-08-13)</option>
<option
  
  value="/release/STEVAN/Moose-0.24/view/lib/Moose.pm"
>0.24
  (STEVAN on 2007-07-03)</option>
<option
  
  value="/release/GRODITI/Moose-0.23/view/lib/Moose.pm"
>0.23
  (GRODITI on 2007-06-18)</option>
<option
  
  value="/release/STEVAN/Moose-0.22/view/lib/Moose.pm"
>0.22
  (STEVAN on 2007-05-31)</option>
<option
  
  value="/release/STEVAN/Moose-0.21/view/lib/Moose.pm"
>0.21
  (STEVAN on 2007-05-03)</option>
<option
  
  value="/release/STEVAN/Moose-0.20/view/lib/Moose.pm"
>0.20
  (STEVAN on 2007-04-06)</option>
<option
  
  value="/release/STEVAN/Moose-0.19/view/lib/Moose.pm"
>0.19
  (STEVAN on 2007-04-05)</option>
<option
  
  value="/release/STEVAN/Moose-0.18/view/lib/Moose.pm"
>0.18
  (STEVAN on 2007-03-11)</option>
<option
  
  value="/release/STEVAN/Moose-0.18_002/view/lib/Moose.pm"
>0.18_002 DEV
  (STEVAN on 2006-11-27)</option>
<option
  
  value="/release/STEVAN/Moose-0.18_001/view/lib/Moose.pm"
>0.18_001 DEV
  (STEVAN on 2006-11-27)</option>
<option
  
  value="/release/STEVAN/Moose-0.17/view/lib/Moose.pm"
>0.17
  (STEVAN on 2006-11-14)</option>
<option
  
  value="/release/STEVAN/Moose-0.16/view/lib/Moose.pm"
>0.16
  (STEVAN on 2006-11-14)</option>
<option
  
  value="/release/STEVAN/Moose-0.15/view/lib/Moose.pm"
>0.15
  (STEVAN on 2006-11-05)</option>
<option
  
  value="/release/STEVAN/Moose-0.14/view/lib/Moose.pm"
>0.14
  (STEVAN on 2006-10-10)</option>
<option
  
  value="/release/STEVAN/Moose-0.13/view/lib/Moose.pm"
>0.13
  (STEVAN on 2006-09-30)</option>
<option
  
  value="/release/STEVAN/Moose-0.12/view/lib/Moose.pm"
>0.12
  (STEVAN on 2006-09-01)</option>
<option
  
  value="/release/STEVAN/Moose-0.11/view/lib/Moose.pm"
>0.11
  (STEVAN on 2006-07-12)</option>
<option
  
  value="/release/STEVAN/Moose-0.10/view/lib/Moose.pm"
>0.10
  (STEVAN on 2006-07-06)</option>
<option
  
  value="/release/STEVAN/Moose-0.09_03/view/lib/Moose.pm"
>0.09_03 DEV
  (STEVAN on 2006-06-23)</option>
<option
  
  value="/release/STEVAN/Moose-0.09_02/view/lib/Moose.pm"
>0.09_02 DEV
  (STEVAN on 2006-05-16)</option>
<option
  
  value="/release/STEVAN/Moose-0.09_01/view/lib/Moose.pm"
>0.09_01 DEV
  (STEVAN on 2006-05-13)</option>
<option
  
  value="/release/STEVAN/Moose-0.05/view/lib/Moose.pm"
>0.05
  (STEVAN on 2006-04-27)</option>
<option
  
  value="/release/STEVAN/Moose-0.04/view/lib/Moose.pm"
>0.04
  (STEVAN on 2006-04-17)</option>
<option
  
  value="/release/STEVAN/Moose-0.03_02/view/lib/Moose.pm"
>0.03_02 DEV
  (STEVAN on 2006-04-13)</option>
<option
  
  value="/release/STEVAN/Moose-0.03_01/view/lib/Moose.pm"
>0.03_01 DEV
  (STEVAN on 2006-04-10)</option>
<option
  
  value="/release/STEVAN/Moose-0.03/view/lib/Moose.pm"
>0.03
  (STEVAN on 2006-03-30)</option>
<option
  
  value="/release/STEVAN/Moose-0.02/view/lib/Moose.pm"
>0.02
  (STEVAN on 2006-03-21)</option>
</optgroup>
</select>
    </li>
    <li class="version-diff">
<select class="select-navigator form-control tool-bar-form">
  <option disabled selected>Diff with version</option>
<option
  disabled
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.4001/lib/Moose.pm"
>2.4001
  (ETHER on 2026-10-01)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.4000/lib/Moose.pm"
>2.4000
  (ETHER on 2025-07-04)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2207/lib/Moose.pm"
>2.2207
  (ETHER on 2024-01-21)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/DOY/Moose-2.0604/lib/Moose.pm"
>2.0604
  (DOY on 2012-09-19) UNAUTHORIZED</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/DOY/Moose-2.0603/lib/Moose.pm"
>2.0603
  (DOY on 2012-06-28) UNAUTHORIZED</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/DOY/Moose-2.0602/lib/Moose.pm"
>2.0602
  (DOY on 2012-05-07) UNAUTHORIZED</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-2.0204/lib/Moose.pm"
>2.0204
  (FLORA on 2011-08-25) UNAUTHORIZED</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-2.0007/lib/Moose.pm"
>2.0007
  (FLORA on 2011-05-15) UNAUTHORIZED</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-1.07/lib/Moose.pm"
>1.07
  (FLORA on 2010-06-05)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-1.06/lib/Moose.pm"
>1.06
  (FLORA on 2010-06-01)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-1.05/lib/Moose.pm"
>1.05
  (FLORA on 2010-05-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-1.03/lib/Moose.pm"
>1.03
  (FLORA on 2010-05-06)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-1.02/lib/Moose.pm"
>1.02
  (FLORA on 2010-05-01)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-1.01/lib/Moose.pm"
>1.01
  (FLORA on 2010-03-26)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/STEVAN/Moose-1.00/lib/Moose.pm"
>1.00
  (STEVAN on 2010-03-25)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-0.99/lib/Moose.pm"
>0.99
  (FLORA on 2010-03-08)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-0.96/lib/Moose.pm"
>0.96
  (FLORA on 2010-02-06)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-0.95/lib/Moose.pm"
>0.95
  (FLORA on 2010-02-04)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/FLORA/Moose-0.93/lib/Moose.pm"
>0.93
  (FLORA on 2009-11-19)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/STEVAN/Moose-0.01/lib/Moose.pm"
>0.01
  (STEVAN on 2006-03-15)</option>
<optgroup label="BackPAN">
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2206/lib/Moose.pm"
>2.2206
  (ETHER on 2023-07-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2205/lib/Moose.pm"
>2.2205
  (ETHER on 2023-07-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2204/lib/Moose.pm"
>2.2204
  (ETHER on 2023-07-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2203/lib/Moose.pm"
>2.2203
  (ETHER on 2023-01-22)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2202/lib/Moose.pm"
>2.2202
  (ETHER on 2023-01-14)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2201/lib/Moose.pm"
>2.2201
  (ETHER on 2021-11-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2200/lib/Moose.pm"
>2.2200
  (ETHER on 2021-10-31)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2100-TRIAL/lib/Moose.pm"
>2.2100-TRIAL DEV
  (ETHER on 2021-04-13)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2015/lib/Moose.pm"
>2.2015
  (ETHER on 2021-03-31)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2014/lib/Moose.pm"
>2.2014
  (ETHER on 2020-12-19)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2013/lib/Moose.pm"
>2.2013
  (ETHER on 2020-07-21)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2012/lib/Moose.pm"
>2.2012
  (ETHER on 2019-11-22)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2011/lib/Moose.pm"
>2.2011
  (ETHER on 2018-05-16)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2010/lib/Moose.pm"
>2.2010
  (ETHER on 2018-02-16)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2009/lib/Moose.pm"
>2.2009
  (ETHER on 2017-11-29)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2008/lib/Moose.pm"
>2.2008
  (ETHER on 2017-11-21)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2007/lib/Moose.pm"
>2.2007
  (ETHER on 2017-11-12)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2006/lib/Moose.pm"
>2.2006
  (ETHER on 2017-07-12)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2005/lib/Moose.pm"
>2.2005
  (ETHER on 2017-05-03)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2004/lib/Moose.pm"
>2.2004
  (ETHER on 2017-01-31)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2003/lib/Moose.pm"
>2.2003
  (ETHER on 2017-01-30)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2002/lib/Moose.pm"
>2.2002
  (ETHER on 2017-01-30)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2001/lib/Moose.pm"
>2.2001
  (ETHER on 2017-01-29)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.2000/lib/Moose.pm"
>2.2000
  (ETHER on 2017-01-29)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1905-TRIAL/lib/Moose.pm"
>2.1905-TRIAL DEV
  (ETHER on 2017-01-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1904-TRIAL/lib/Moose.pm"
>2.1904-TRIAL DEV
  (ETHER on 2016-12-22)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1807/lib/Moose.pm"
>2.1807
  (ETHER on 2016-12-22)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1903-TRIAL/lib/Moose.pm"
>2.1903-TRIAL DEV
  (ETHER on 2016-11-22)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1902-TRIAL/lib/Moose.pm"
>2.1902-TRIAL DEV
  (ETHER on 2016-10-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1901-TRIAL/lib/Moose.pm"
>2.1901-TRIAL DEV
  (ETHER on 2016-10-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1900-TRIAL/lib/Moose.pm"
>2.1900-TRIAL DEV
  (ETHER on 2016-10-09)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1806/lib/Moose.pm"
>2.1806
  (ETHER on 2016-09-25)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1805/lib/Moose.pm"
>2.1805
  (ETHER on 2016-08-19)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1804/lib/Moose.pm"
>2.1804
  (ETHER on 2016-06-02)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1803/lib/Moose.pm"
>2.1803
  (ETHER on 2016-05-31)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1802/lib/Moose.pm"
>2.1802
  (ETHER on 2016-05-25)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1801/lib/Moose.pm"
>2.1801
  (ETHER on 2016-05-02)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1800/lib/Moose.pm"
>2.1800
  (ETHER on 2016-04-30)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1705-TRIAL/lib/Moose.pm"
>2.1705-TRIAL DEV
  (ETHER on 2016-04-21)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1704-TRIAL/lib/Moose.pm"
>2.1704-TRIAL DEV
  (ETHER on 2016-04-13)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1703-TRIAL/lib/Moose.pm"
>2.1703-TRIAL DEV
  (ETHER on 2016-04-13)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1702-TRIAL/lib/Moose.pm"
>2.1702-TRIAL DEV
  (ETHER on 2016-04-08)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1701-TRIAL/lib/Moose.pm"
>2.1701-TRIAL DEV
  (ETHER on 2016-04-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1700-TRIAL/lib/Moose.pm"
>2.1700-TRIAL DEV
  (ETHER on 2016-04-06)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1605/lib/Moose.pm"
>2.1605
  (ETHER on 2016-02-16)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1604/lib/Moose.pm"
>2.1604
  (ETHER on 2015-11-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1603/lib/Moose.pm"
>2.1603
  (ETHER on 2015-08-28)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1602-TRIAL/lib/Moose.pm"
>2.1602-TRIAL DEV
  (ETHER on 2015-08-14)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1601-TRIAL/lib/Moose.pm"
>2.1601-TRIAL DEV
  (ETHER on 2015-08-10)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1600/lib/Moose.pm"
>2.1600
  (ETHER on 2015-07-31)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1501-TRIAL/lib/Moose.pm"
>2.1501-TRIAL DEV
  (ETHER on 2015-07-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1500-TRIAL/lib/Moose.pm"
>2.1500-TRIAL DEV
  (ETHER on 2015-07-01)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1405/lib/Moose.pm"
>2.1405
  (ETHER on 2015-06-06)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1404/lib/Moose.pm"
>2.1404
  (ETHER on 2015-04-16)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1403/lib/Moose.pm"
>2.1403
  (ETHER on 2014-12-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1402/lib/Moose.pm"
>2.1402
  (ETHER on 2014-11-05)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1401/lib/Moose.pm"
>2.1401
  (ETHER on 2014-11-03)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1400/lib/Moose.pm"
>2.1400
  (ETHER on 2014-11-01)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1307-TRIAL/lib/Moose.pm"
>2.1307-TRIAL DEV
  (ETHER on 2014-10-26)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1306-TRIAL/lib/Moose.pm"
>2.1306-TRIAL DEV
  (ETHER on 2014-10-25)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1305-TRIAL/lib/Moose.pm"
>2.1305-TRIAL DEV
  (ETHER on 2014-10-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1304-TRIAL/lib/Moose.pm"
>2.1304-TRIAL DEV
  (ETHER on 2014-09-25)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1213/lib/Moose.pm"
>2.1213
  (ETHER on 2014-09-25)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1303-TRIAL/lib/Moose.pm"
>2.1303-TRIAL DEV
  (ETHER on 2014-09-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1212/lib/Moose.pm"
>2.1212
  (ETHER on 2014-09-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1302-TRIAL/lib/Moose.pm"
>2.1302-TRIAL DEV
  (ETHER on 2014-08-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1301-TRIAL/lib/Moose.pm"
>2.1301-TRIAL DEV
  (ETHER on 2014-08-19)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1300-TRIAL/lib/Moose.pm"
>2.1300-TRIAL DEV
  (ETHER on 2014-08-12)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1211/lib/Moose.pm"
>2.1211
  (ETHER on 2014-08-11)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1210/lib/Moose.pm"
>2.1210
  (ETHER on 2014-07-03)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1209/lib/Moose.pm"
>2.1209
  (ETHER on 2014-06-05)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1208/lib/Moose.pm"
>2.1208
  (ETHER on 2014-06-01)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1207/lib/Moose.pm"
>2.1207
  (ETHER on 2014-05-26)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1206/lib/Moose.pm"
>2.1206
  (ETHER on 2014-05-14)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1205/lib/Moose.pm"
>2.1205
  (ETHER on 2014-04-16)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1204/lib/Moose.pm"
>2.1204
  (ETHER on 2014-02-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1203/lib/Moose.pm"
>2.1203
  (ETHER on 2014-02-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1202/lib/Moose.pm"
>2.1202
  (ETHER on 2014-01-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1201/lib/Moose.pm"
>2.1201
  (ETHER on 2014-01-11)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1200/lib/Moose.pm"
>2.1200
  (ETHER on 2014-01-06)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1108-TRIAL/lib/Moose.pm"
>2.1108-TRIAL DEV
  (ETHER on 2014-01-05)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1107-TRIAL/lib/Moose.pm"
>2.1107-TRIAL DEV
  (ETHER on 2013-11-29)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1106-TRIAL/lib/Moose.pm"
>2.1106-TRIAL DEV
  (ETHER on 2013-11-05)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1105-TRIAL/lib/Moose.pm"
>2.1105-TRIAL DEV
  (ETHER on 2013-10-31)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1104-TRIAL/lib/Moose.pm"
>2.1104-TRIAL DEV
  (ETHER on 2013-10-30)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1103-TRIAL/lib/Moose.pm"
>2.1103-TRIAL DEV
  (ETHER on 2013-10-26)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1102-TRIAL/lib/Moose.pm"
>2.1102-TRIAL DEV
  (ETHER on 2013-10-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1101-TRIAL/lib/Moose.pm"
>2.1101-TRIAL DEV
  (ETHER on 2013-10-20)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1100-TRIAL/lib/Moose.pm"
>2.1100-TRIAL DEV
  (ETHER on 2013-09-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1005/lib/Moose.pm"
>2.1005
  (ETHER on 2013-08-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1004/lib/Moose.pm"
>2.1004
  (ETHER on 2013-07-26)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1003/lib/Moose.pm"
>2.1003
  (ETHER on 2013-07-26)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.0901-TRIAL/lib/Moose.pm"
>2.0901-TRIAL DEV
  (ETHER on 2013-06-21)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.0900-TRIAL/lib/Moose.pm"
>2.0900-TRIAL DEV
  (ETHER on 2013-05-27)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1002-TRIAL/lib/Moose.pm"
>2.1002-TRIAL DEV
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1001/lib/Moose.pm"
>2.1001
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.1000/lib/Moose.pm"
>2.1000
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.0803/lib/Moose.pm"
>2.0803
  (ETHER on 2013-05-23)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.0802/lib/Moose.pm"
>2.0802
  (ETHER on 2013-05-07)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.0801/lib/Moose.pm"
>2.0801
  (ETHER on 2013-03-28)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/ETHER/Moose-2.0800/lib/Moose.pm"
>2.0800
  (ETHER on 2013-03-28)</option>
<option
  
  value="/release/ETHER/Moose-2.4001/diff/DOY/Moos