

<!DOCTYPE html>
<html lang="en" data-layout="responsive" data-local="" data-version="prod-frontend-00278-trw">
  <head>
    
    <script>
      window.addEventListener('error', window.__err=function f(e){f.p=f.p||[];f.p.push(e)});
    </script>
    <script>
      (function() {
        const theme = document.cookie.match(/prefers-color-scheme=(light|dark|auto)/)?.[1]
        if (theme) {
          document.querySelector('html').setAttribute('data-theme', theme);
        }
      }())
    </script>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    
    <meta class="js-gtmID" data-gtmid="GTM-W8MVQXG">
    <link rel="shortcut icon" href="/static/shared/icon/favicon.ico">
    
  
    <link rel="canonical" href="https://pkg.go.dev/golang.org/x/net">
  

    <link href="/static/frontend/frontend.min.css?version=prod-frontend-00278-trw" rel="stylesheet">
    
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Go Packages">
    
    
  <title>net module - golang.org/x/net - Go Packages</title>

    
  <link href="/static/frontend/unit/unit.min.css?version=prod-frontend-00278-trw" rel="stylesheet">
  
  <link href="/static/frontend/unit/main/main.min.css?version=prod-frontend-00278-trw" rel="stylesheet">


  </head>
  <body>
    
    <script>
      function loadScript(src, mod = true) {
        let s = document.createElement('script');
        let v = document.documentElement.dataset.version;
        if (v && src.startsWith('/static/')) {
          src += '?version=' + encodeURIComponent(v);
        }
        s.src = src;
        if (mod) {
          s.type = 'module';
          s.async = true;
          s.defer = true
        }
        document.head.appendChild(s);
      }
      loadScript("/third_party/dialog-polyfill/dialog-polyfill.js", false)
      loadScript("/static/frontend/frontend.js");
    </script>
    
  

    
  <header class="go-Header go-Header--full js-siteHeader">
    <div class="go-Header-inner go-Header-inner--dark">
      <nav class="go-Header-nav">
        <a href="https://go.dev/" class="js-headerLogo" data-gtmc="nav link"
            data-test-id="go-header-logo-link" role="heading" aria-level="1">
          <img class="go-Header-logo" src="/static/shared/logo/go-white.svg" alt="Go">
        </a>
         <div class="skip-navigation-wrapper">
            <a class="skip-to-content-link" aria-label="Skip to main content" href="#main-content"> Skip to Main Content </a>
          </div>
        <div class="go-Header-rightContent">
          
<div class="go-SearchForm js-searchForm">
  <form
    class="go-InputGroup go-ShortcutKey go-SearchForm-form"
    action="/search"
    data-shortcut="/"
    data-shortcut-alt="search"
    data-gtmc="search form"
    aria-label="Search for a package"
    role="search"
  >
    <input name="q" class="go-Input js-searchFocus" aria-label="Search for a package" type="search"
        autocapitalize="off" autocomplete="off" autocorrect="off" spellcheck="false"
        placeholder="Search packages or symbols"
        value="" />
    <input name="m" value="" hidden>
    <button class="go-Button go-Button--inverted" aria-label="Submit search">
      <img
        class="go-Icon"
        height="24"
        width="24"
        src="/static/shared/icon/search_gm_grey_24dp.svg"
        alt=""
      />
    </button>
  </form>
  <button class="go-SearchForm-expandSearch js-expandSearch" data-gtmc="nav button"
      aria-label="Open search" data-test-id="expand-search">
    <img class="go-Icon go-Icon--inverted" height="24" width="24"
        src="/static/shared/icon/search_gm_grey_24dp.svg" alt="">

  </button>
</div>

          <ul class="go-Header-menu">
            <li class="go-Header-menuItem">
              <a class="js-desktop-menu-hover" href="#" data-gtmc="nav link">
                Why Go
                <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_drop_down_gm_grey_24dp.svg" alt="submenu dropdown icon">
              </a>
              <ul class="go-Header-submenu go-Header-submenu--why js-desktop-submenu-hover" aria-label="submenu">
                  <li class="go-Header-submenuItem">
                    <div>
                      <a href="https://go.dev/solutions/case-studies">
                        <span>Case Studies</span>
                      </a>
                    </div>
                    <p>Common problems companies solve with Go</p>
                  </li>
                  <li class="go-Header-submenuItem">
                    <div>
                      <a href="https://go.dev/solutions/use-cases">
                        <span>Use Cases</span>
                      </a>
                    </div>
                    <p>Stories about how and why companies use Go</p>
                  </li>
                  <li class="go-Header-submenuItem">
                    <div>
                      <a href="https://go.dev/security/">
                        <span>Security</span>
                      </a>
                    </div>
                    <p>How Go can help keep you secure by default</p>
                  </li>
              </ul>
            </li>
            <li class="go-Header-menuItem">
              <a href="https://go.dev/learn/" data-gtmc="nav link">Learn</a>
            </li>
            <li class="go-Header-menuItem">
              <a class="js-desktop-menu-hover" href="#" data-gtmc="nav link">
                Docs
                <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_drop_down_gm_grey_24dp.svg" alt="submenu dropdown icon">
              </a>
              <ul class="go-Header-submenu go-Header-submenu--docs js-desktop-submenu-hover" aria-label="submenu">
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://go.dev/doc/effective_go">
                      <span>Effective Go</span>
                    </a>
                  </div>
                  <p>Tips for writing clear, performant, and idiomatic Go code</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://go.dev/doc/">
                      <span>Go User Manual</span>
                    </a>
                  </div>
                  <p>A complete introduction to building software with Go</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://pkg.go.dev/std">
                      <span>Standard library</span>
                    </a>
                  </div>
                  <p>Reference documentation for Go's standard library</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://go.dev/doc/devel/release">
                      <span>Release Notes</span>
                    </a>
                  </div>
                  <p>Learn what's new in each Go release</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="/api">
                      <span>API</span>
                    </a>
                  </div>
                  <p>Reference documentation for the pkg.go.dev API</p>
                </li>
              </ul>
            </li>
            <li class="go-Header-menuItem go-Header-menuItem--active">
              <a href="/" data-gtmc="nav link">Packages</a>
            </li>
            <li class="go-Header-menuItem">
              <a class="js-desktop-menu-hover" href="#" data-gtmc="nav link">
                Community
                <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_drop_down_gm_grey_24dp.svg" alt="submenu dropdown icon">
              </a>
              <ul class="go-Header-submenu go-Header-submenu--community js-desktop-submenu-hover" aria-label="submenu">
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://go.dev/talks/">
                      <span>Recorded Talks</span>
                    </a>
                  </div>
                  <p>Videos from prior events</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://www.meetup.com/pro/go">
                      <span>Meetups</span>
                      <i class="material-icons">
                        <img class="go-Icon" height="24" width="24"
                            src="/static/shared/icon/launch_gm_grey_24dp.svg" alt="">
                      </i>
                    </a>
                  </div>
                  <p>Meet other local Go developers</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://github.com/golang/go/wiki/Conferences">
                      <span>Conferences</span>
                      <i class="material-icons">
                        <img class="go-Icon" height="24" width="24"
                            src="/static/shared/icon/launch_gm_grey_24dp.svg" alt="">
                      </i>
                    </a>
                  </div>
                  <p>Learn and network with Go developers from around the world</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://go.dev/blog">
                      <span>Go blog</span>
                    </a>
                  </div>
                  <p>The Go project's official blog.</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    <a href="https://go.dev/help">
                      <span>Go project</span>
                    </a>
                  </div>
                  <p>Get help and stay informed from Go</p>
                </li>
                <li class="go-Header-submenuItem">
                  <div>
                    Get connected
                  </div>
                  <p></p>
                  <div class="go-Header-socialIcons">
                      <a
                        class="go-Header-socialIcon"
                        aria-label="Get connected with google-groups (Opens in new window)"
                        title="Get connected with google-groups (Opens in new window)"
                        href="https://groups.google.com/g/golang-nuts">
                        <img src="/static/shared/logo/social/google-groups.svg" />
                      </a>
                      <a
                        class="go-Header-socialIcon"
                        aria-label="Get connected with github (Opens in new window)"
                        title="Get connected with github (Opens in new window)"
                        href="https://github.com/golang">
                        <img src="/static/shared/logo/social/github.svg" />
                      </a>
                      <a
                        class="go-Header-socialIcon"
                        aria-label="Get connected with twitter (Opens in new window)"
                        title="Get connected with twitter (Opens in new window)"
                        href="https://twitter.com/golang">
                        <img src="/static/shared/logo/social/twitter.svg" />
                      </a>
                      <a
                        class="go-Header-socialIcon"
                        aria-label="Get connected with reddit (Opens in new window)"
                        title="Get connected with reddit (Opens in new window)"
                        href="https://www.reddit.com/r/golang/">
                        <img src="/static/shared/logo/social/reddit.svg" />
                      </a>
                      <a
                        class="go-Header-socialIcon"
                        aria-label="Get connected with slack (Opens in new window)"
                        title="Get connected with slack (Opens in new window)"
                        href="https://invite.slack.golangbridge.org/">
                        <img src="/static/shared/logo/social/slack.svg" />
                      </a>
                      <a
                        class="go-Header-socialIcon"
                        aria-label="Get connected with stack-overflow (Opens in new window)"
                        title=""
                        href="https://stackoverflow.com/collectives/go">
                        <img src="/static/shared/logo/social/stack-overflow.svg" />
                      </a>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
          <button class="go-Header-navOpen js-headerMenuButton go-Header-navOpen--white" data-gtmc="nav button" aria-label="Open navigation">
          </button>
        </div>
      </nav>
    </div>
  </header>
  <aside class="go-NavigationDrawer js-header">
    <nav class="go-NavigationDrawer-nav">
      <div class="go-NavigationDrawer-header">
        <a href="https://go.dev/">
          <img class="go-NavigationDrawer-logo" src="/static/shared/logo/go-blue.svg" alt="Go.">
        </a>
      </div>
      <ul class="go-NavigationDrawer-list">
          <li class="go-NavigationDrawer-listItem js-mobile-subnav-trigger go-NavigationDrawer-hasSubnav">
            <a href="#">
              <span>Why Go</span>
              <i class="material-icons">
                <img class="go-Icon" height="24" width="24"
                  src="/static/shared/icon/navigate_next_gm_grey_24dp.svg" alt="">
              </i>
            </a>

            <div class="go-NavigationDrawer go-NavigationDrawer-submenuItem">
              <div class="go-NavigationDrawer-nav">
                <div class="go-NavigationDrawer-header">
                  <a href="#">
                    <i class="material-icons">
                      <img class="go-Icon" height="24" width="24"
                        src="/static/shared/icon/navigate_before_gm_grey_24dp.svg" alt="">
                      </i>
                      Why Go
                  </a>
                </div>
                <ul class="go-NavigationDrawer-list">
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/solutions/case-studies">
                      Case Studies
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/solutions/use-cases">
                      Use Cases
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/security/">
                      Security
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </li>
          <li class="go-NavigationDrawer-listItem">
            <a href="https://go.dev/learn/">Learn</a>
          </li>
          <li class="go-NavigationDrawer-listItem js-mobile-subnav-trigger go-NavigationDrawer-hasSubnav">
            <a href="#">
              <span>Docs</span>
              <i class="material-icons">
                <img class="go-Icon" height="24" width="24"
                  src="/static/shared/icon/navigate_next_gm_grey_24dp.svg" alt="">
              </i>
            </a>

            <div class="go-NavigationDrawer go-NavigationDrawer-submenuItem">
              <div class="go-NavigationDrawer-nav">
                <div class="go-NavigationDrawer-header">
                  <a href="#"><i class="material-icons">
                    <img class="go-Icon" height="24" width="24"
                      src="/static/shared/icon/navigate_before_gm_grey_24dp.svg" alt="">
                    </i>
                    Docs
                  </a>
                </div>
                <ul class="go-NavigationDrawer-list">
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/doc/effective_go">
                      Effective Go
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/doc/">
                      Go User Manual
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://pkg.go.dev/std">
                      Standard library
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/doc/devel/release">
                      Release Notes
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="/api">
                      API
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </li>
          <li class="go-NavigationDrawer-listItem go-NavigationDrawer-listItem--active">
            <a href="/">Packages</a>
          </li>
          <li class="go-NavigationDrawer-listItem js-mobile-subnav-trigger go-NavigationDrawer-hasSubnav">
            <a href="#">
              <span>Community</span>
              <i class="material-icons">
                <img class="go-Icon" height="24" width="24"
                  src="/static/shared/icon/navigate_next_gm_grey_24dp.svg" alt="">
              </i>
            </a>
            <div class="go-NavigationDrawer go-NavigationDrawer-submenuItem">
              <div class="go-NavigationDrawer-nav">
                <div class="go-NavigationDrawer-header">
                  <a href="#">
                    <i class="material-icons">
                      <img class="go-Icon" height="24" width="24"
                        src="/static/shared/icon/navigate_before_gm_grey_24dp.svg" alt="">
                    </i>
                    Community
                  </a>
                </div>
                <ul class="go-NavigationDrawer-list">
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/talks/">
                      Recorded Talks
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://www.meetup.com/pro/go">
                      Meetups
                      <i class="material-icons">
                      <img class="go-Icon" height="24" width="24"
                          src="/static/shared/icon/launch_gm_grey_24dp.svg" alt="">
                      </i>
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://github.com/golang/go/wiki/Conferences">
                      Conferences
                      <i class="material-icons">
                        <img class="go-Icon" height="24" width="24" src="/static/shared/icon/launch_gm_grey_24dp.svg" alt="">
                      </i>
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/blog">
                      Go blog
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <a href="https://go.dev/help">
                      Go project
                    </a>
                  </li>
                  <li class="go-NavigationDrawer-listItem">
                    <div>Get connected</div>
                    <div class="go-Header-socialIcons">
                        <a class="go-Header-socialIcon" href="https://groups.google.com/g/golang-nuts"><img src="/static/shared/logo/social/google-groups.svg" /></a>
                        <a class="go-Header-socialIcon" href="https://github.com/golang"><img src="/static/shared/logo/social/github.svg" /></a>
                        <a class="go-Header-socialIcon" href="https://twitter.com/golang"><img src="/static/shared/logo/social/twitter.svg" /></a>
                        <a class="go-Header-socialIcon" href="https://www.reddit.com/r/golang/"><img src="/static/shared/logo/social/reddit.svg" /></a>
                        <a class="go-Header-socialIcon" href="https://invite.slack.golangbridge.org/"><img src="/static/shared/logo/social/slack.svg" /></a>
                        <a class="go-Header-socialIcon" href="https://stackoverflow.com/collectives/go"><img src="/static/shared/logo/social/stack-overflow.svg" /></a>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </li>
      </ul>
    </nav>
  </aside>
  <div class="go-NavigationDrawer-scrim js-scrim" role="presentation"></div>

    
  <main class="go-Main" id="main-content">
    <div class="go-Main-banner" role="alert"></div>
    <header class="go-Main-header js-mainHeader">
  
  
  <nav class="go-Main-headerBreadcrumb go-Breadcrumb" aria-label="Breadcrumb" data-test-id="UnitHeader-breadcrumb">
    <ol>
      
        
          <li data-test-id="UnitHeader-breadcrumbItem">
            <a href="/" data-gtmc="breadcrumb link">Discover Packages</a>
          </li>
        
        <li>
          <a href="/golang.org/x/net@v0.62.0" data-gtmc="breadcrumb link" aria-current="location"
              data-test-id="UnitHeader-breadcrumbCurrent">
            golang.org/x/net
          </a>
          
            <button
              class="go-Button go-Button--inline go-Clipboard js-clipboard"
              title="Copy path to clipboard.&#10;&#10;golang.org/x/net"
              aria-label="Copy Path to Clipboard"
              data-to-copy="golang.org/x/net"
              data-gtmc="breadcrumbs button"
            >
              <img
                class="go-Icon go-Icon--accented"
                height="24"
                width="24"
                src="/static/shared/icon/content_copy_gm_grey_24dp.svg"
                alt=""
              >
            </button>
          
        
      </li>
    </ol>
  </nav>

  <div class="go-Main-headerContent">
    
  <div class="go-Main-headerTitle js-stickyHeader">
    <a class="go-Main-headerLogo" href="https://go.dev/" aria-hidden="true" tabindex="-1" data-gtmc="header link" aria-label="Link to Go Homepage">
      <img height="78" width="207" src="/static/shared/logo/go-blue.svg" alt="Go">
    </a>
    <h1 class="UnitHeader-titleHeading" data-test-id="UnitHeader-title">net</h1>
    
      <span class="go-Chip go-Chip--inverted">module</span>
    
    
      
        <button
          class="go-Button go-Button--inline go-Clipboard js-clipboard"
          title="Copy path to clipboard.&#10;&#10;golang.org/x/net"
          aria-label="Copy Path to Clipboard"
          data-to-copy="golang.org/x/net"
          data-gtmc="title button"
          tabindex="-1"
        >
          <img
            class="go-Icon go-Icon--accented"
            height="24"
            width="24"
            src="/static/shared/icon/content_copy_gm_grey_24dp.svg"
            alt=""
          />
        </button>
      
    
  </div>

    
      
  <div class="go-Main-headerDetails">
    
      
  <span class="go-Main-headerDetailItem" data-test-id="UnitHeader-version">
    <a href="?tab=versions" aria-label="Version: v0.62.0" 
    data-gtmc="header link" aria-describedby="version-description">
      <span class="go-textSubtle" aria-hidden="true">Version: </span>
        v0.62.0
    </a>
    <div class="screen-reader-only" id="version-description" hidden>
      Opens a new window with list of versions in this module.
    </div>
    
    <span class="DetailsHeader-badge--latest" data-test-id="UnitHeader-minorVersionBanner">
      <span class="go-Chip DetailsHeader-span--latest">Latest</span>
      <span class="go-Chip DetailsHeader-span--notAtLatest">
        Latest
        
  <details class="go-Tooltip js-tooltip" data-gtmc="tooltip">
    <summary>
      <img class="go-Icon go-Icon--inverted" height="24" width="24" src="/static/shared/icon/alert_gm_grey_24dp.svg" alt="Warning">
    </summary>
    <p>This package is not in the latest version of its module.</p>
  </details>

      </span>
      <a href="/golang.org/x/net" aria-label="Go to Latest Version" data-gtmc="header link">
        <span class="go-Chip go-Chip--alert DetailsHeader-span--goToLatest">Go to latest</span>
      </a>
    </span>
  </span>

      
  <span class="go-Main-headerDetailItem" data-test-id="UnitHeader-commitTime">
    Published: Oct 27, 2026
  </span>

      
  <span class="go-Main-headerDetailItem" data-test-id="UnitHeader-licenses">
    License: <a href="/golang.org/x/net?tab=licenses" data-test-id="UnitHeader-license" 
        data-gtmc="header link" aria-describedby="license-description">BSD-3-Clause</a>
      
    
  </span>
  <div class="screen-reader-only" id="license-description" hidden>
    Opens a new window with license information.
  </div>

      
    
  </div>
  
  <div class="UnitHeader-overflowContainer">
    <svg class="UnitHeader-overflowImage" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
      <path d="M0 0h24v24H0z" fill="none"/>
      <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
    </svg>
    <select class="UnitHeader-overflowSelect js-selectNav" tabindex="-1">
      <option value="/">Main</option>
      <option value="/golang.org/x/net?tab=versions">
        Versions
      </option>
      <option value="/golang.org/x/net?tab=licenses">
        Licenses
      </option>
      
    </select>
  </div>


    
  </div>

</header>
    
      <aside class="go-Main-aside  js-mainAside">
  
  <div class="UnitMeta">
    <h2 class="go-textLabel">Details</h2>
    
  <ul class="UnitMeta-details">
    <li>
      <details class="go-Tooltip js-tooltip" data-gtmc="tooltip">
        <summary class="go-textSubtle">
          
  <img class="go-Icon go-Icon--accented"
    tabindex="0"
    role="button"src="/static/shared/icon/check_circle_gm_grey_24dp.svg" alt="checked" aria-label="Valid file, toggle tooltip"height="24" width="24">

          Valid <a href="https://cs.opensource.google/go/x/net/+/v0.62.0:/go.mod" target="_blank" rel="noopener">go.mod</a> file
          <img class="go-Icon" role="button" tabindex="0" src="/static/shared/icon/help_gm_grey_24dp.svg" alt="" aria-label="Toggle go.mod validity tooltip" height="24" width="24">
        </summary>
        <p aria-live="polite" role="tooltip">
          The Go module system was introduced in Go 1.11 and is the official dependency management
          solution for Go.
        </p>
      </details>
    </li>
    <li>
      <details class="go-Tooltip js-tooltip" data-gtmc="tooltip">
        <summary class="go-textSubtle">
          
  <img class="go-Icon go-Icon--accented"
    tabindex="0"
    role="button"src="/static/shared/icon/check_circle_gm_grey_24dp.svg" alt="checked" aria-label="Valid file, toggle tooltip"height="24" width="24">

          Redistributable license
          <img class="go-Icon" role="button" tabindex="0" src="/static/shared/icon/help_gm_grey_24dp.svg" alt="" aria-label="Toggle redistributable help tooltip" height="24" width="24">
        </summary>
        <p aria-live="polite" role="tooltip">
          Redistributable licenses place minimal restrictions on how software can be used,
          modified, and redistributed.
        </p>
      </details>
    </li>
    <li>
      <details class="go-Tooltip js-tooltip" data-gtmc="tooltip">
        <summary class="go-textSubtle">
          
  <img class="go-Icon go-Icon--accented"
    tabindex="0"
    role="button"src="/static/shared/icon/check_circle_gm_grey_24dp.svg" alt="checked" aria-label="Valid file, toggle tooltip"height="24" width="24">

          Tagged version
          <img class="go-Icon" role="button" tabindex="0" src="/static/shared/icon/help_gm_grey_24dp.svg" alt="" aria-label="Toggle tagged version tooltip" height="24" width="24">
        </summary>
        <p aria-live="polite" role="tooltip">Modules with tagged versions give importers more predictable builds.</p>
      </details>
    </li>
    <li>
      <details class="go-Tooltip js-tooltip" data-gtmc="tooltip">
        <summary class="go-textSubtle">
          
  <img class="go-Icon"
    tabindex="0"
    role="button"src="/static/shared/icon/cancel_gm_grey_24dp.svg" alt="unchecked" aria-label="Missing or invalid file, toggle tooltip"height="24" width="24">

          Stable version
          <img class="go-Icon" role="button" tabindex="0" aria-label="Toggle stable version tooltip" src="/static/shared/icon/help_gm_grey_24dp.svg" alt="" height="24" width="24">
        </summary>
        <p aria-live="polite" role="tooltip">When a project reaches major version v1 it is considered stable.</p>
      </details>
    </li>
    <li class="UnitMeta-detailsLearn">
      <a href="/about#best-practices" data-gtmc="meta link">Learn more about best practices</a>
    </li>
  </ul>

    <h2 class="go-textLabel">Repository</h2>
    <div class="UnitMeta-repo">
      
        <a href="https://cs.opensource.google/go/x/net" title="https://cs.opensource.google/go/x/net" target="_blank" rel="noopener">
          cs.opensource.google/go/x/net
        </a>
      
    </div>
    
      <h2 class="go-textLabel" data-test-id="links-heading">Links</h2>
      <ul class="UnitMeta-links">
        
          <li>
            <a href="https://go.dev/security/policy"
                title="Report security issues in the Go standard library and sub-repositories">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/security_grey_24dp.svg" alt="">
              Report a Vulnerability
            </a>
          </li>
        
        
          <li>
            <a href="https://deps.dev/go/golang.org%2Fx%2Fnet/v0.62.0" title="View this module on Open Source Insights"
              target="_blank" rel="noopener" data-test-id="meta-link-depsdev">
              <img class="link-Icon" src="/static/shared/icon/depsdev-logo.svg"
                alt="Open Source Insights Logo" />
              Open Source Insights
            </a>
          </li>
        
        
  

        
  

        
  

      </ul>
    
  </div>

</aside>
    
    <nav class="go-Main-nav go-Main-nav--sticky js-mainNav" aria-label="Outline">
  <div class="go-Main-navDesktop">
    
  <div class="UnitOutline-jumpTo">
    <button class="UnitOutline-jumpToInput go-ShortcutKey js-jumpToInput"
        aria-controls="jump-to-modal"
        aria-label="Open Jump to Identifier"
        data-shortcut="f"
        data-shortcut-alt="find"
        data-test-id="jump-to-button" data-gtmc="outline button">
      Jump to ...
    </button>
  </div>
  <ul class="go-Tree js-tree" role="tree" aria-label="Outline">
    
      <li class="js-readmeOutline">
        <a href="#section-readme" data-gtmc="outline link">
          README
        </a>
        
  <ul id="readme-outline">
    
      <li>
        <a href="#readme-report-issues-send-patches" data-gtmc="readme outline link">
          Report Issues / Send Patches
        </a>
         
      </li>
     
  </ul>

      </li>
    
    
    
    
      <li>
        <a href="#section-directories" data-gtmc="outline link">
          Directories
        </a>
      </li>
    
  </ul>

  </div>
  <div class="go-Main-navMobile js-mainNavMobile">
    <label class="go-Label">
      <select class="go-Select">
        
          <option selected disabled>README</option>
        
      </select>
    </label>
  </div>
</nav>
    <article class="go-Main-article js-mainContent">
  <div class="UnitDetails" data-test-id="UnitDetails" style="display: block;">
    <div class="UnitDetails-content js-unitDetailsContent" data-test-id="UnitDetails-content">
      
        
  <div class="UnitReadme UnitReadme--expanded js-readme">
    <h2 class="UnitReadme-title" id="section-readme">
      <img class="go-Icon" height="24" width="24" src="/static/shared/icon/chrome_reader_mode_gm_grey_24dp.svg" alt="">
      README
      <a class="UnitReadme-idLink" href="#section-readme" title="Go to Readme" aria-label="Go to Readme">¶</a>
    </h2>
    
      <div class="UnitReadme-content" data-test-id="Unit-readmeContent">
        <div class="Overview-readmeContent js-readmeContent"><h3 class="h1" id="readme-go-networking">Go Networking</h3>
<p><a href="https://pkg.go.dev/golang.org/x/net" rel="nofollow"><img src="https://pkg.go.dev/badge/golang.org/x/net.svg" alt="Go Reference"/></a></p>
<p>This repository holds supplementary Go networking packages.</p>
<h4 class="h2" id="readme-report-issues-send-patches">Report Issues / Send Patches</h4>
<p>This repository uses Gerrit for code changes. To learn how to submit changes to
this repository, see <a href="https://go.dev/doc/contribute" rel="nofollow">https://go.dev/doc/contribute</a>.</p>
<p>The git repository is <a href="https://go.googlesource.com/net" rel="nofollow">https://go.googlesource.com/net</a>.</p>
<p>The main issue tracker for the net repository is located at
<a href="https://go.dev/issues" rel="nofollow">https://go.dev/issues</a>. Prefix your issue with &#34;x/net:&#34; in the
subject line, so it is easy to find.</p>
</div>
      </div>
      <button class="UnitReadme-expandLink js-readmeExpand"
          data-test-id="readme-expand" data-gtmc="readme button"
          aria-label="Expand Readme">Expand ▾</button>
      <button class="UnitReadme-collapseLink js-readmeCollapse"
          data-test-id="readme-collapse" data-gtmc="readme button"
          aria-label="Expand Readme">Collapse ▴</button>
    
  </div>

      
      
      
      
        
  <div class="UnitDirectories js-unitDirectories">
    <h2 class="UnitDirectories-title" id="section-directories">
      <img class="go-Icon" height="24" width="24" src="/static/shared/icon/folder_gm_grey_24dp.svg" alt="">
      Directories
      <a class="UnitDirectories-idLink" href="#section-directories" title="Go to Directories" aria-label="Go to Directories">¶</a>
    </h2>
    <div class="UnitDirectories-toggles">
      <div class="UnitDirectories-toggleButtons">
        <button class="js-showInternalDirectories" data-test-id="internal-directories-toggle"
            data-gtmc="directories button" aria-label="Show Internal Directories">
          Show internal
        </button>
        <button class="js-expandAllDirectories" data-test-id="directories-toggle"
            data-gtmc="directories button" aria-label="Expand All Directories">
          Expand all
        </button>
      </div>
    </div>
    <table class="UnitDirectories-table UnitDirectories-table--tree js-expandableTable"
          data-test-id="UnitDirectories-table">
      <tr class="UnitDirectories-tableHeader UnitDirectories-tableHeader--tree">
        <th>Path</th>
        <th class="UnitDirectories-desktopSynopsis">Synopsis</th>
      </tr>
      
          
  
  <tr
      class="">
    <td data-id="bpf" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/bpf">bpf</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package bpf implements marshaling and unmarshaling of programs for the Berkeley Packet Filter virtual machine, and provides a Go implementation of the virtual machine.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package bpf implements marshaling and unmarshaling of programs for the Berkeley Packet Filter virtual machine, and provides a Go implementation of the virtual machine.</td></tr></tr>

      
          
  
  <tr data-aria-controls="context-ctxhttp "
      class="">
    <td data-id="context" data-aria-owns="context-ctxhttp ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton"
                aria-expanded="false"
                aria-label="1 more from"
                data-aria-controls="context-ctxhttp "
                data-aria-labelledby="context-button context"
                data-id="context-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><a href="/golang.org/x/net@v0.62.0/context">context</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package context has been superseded by the standard library context package.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package context has been superseded by the standard library context package.</td></tr><tr data-id="context-ctxhttp" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/context/ctxhttp">ctxhttp</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package ctxhttp provides helper functions for performing context-aware HTTP requests.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package ctxhttp provides helper functions for performing context-aware HTTP requests.</td></tr>

      
          
  
  <tr
      class="">
    <td data-id="dict" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/dict">dict</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package dict implements the Dictionary Server Protocol as defined in RFC 2229.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package dict implements the Dictionary Server Protocol as defined in RFC 2229.</td></tr></tr>

      
          
  
  <tr data-aria-controls="dns-dnsmessage "
      class="">
    <td data-id="dns" data-aria-owns="dns-dnsmessage ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton"
                aria-expanded="false"
                aria-label="1 more from"
                data-aria-controls="dns-dnsmessage "
                data-aria-labelledby="dns-button dns"
                data-id="dns-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><span>dns</span>
      </td>
      <td class="UnitDirectories-desktopSynopsis"></td></tr><tr data-id="dns-dnsmessage" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/dns/dnsmessage">dnsmessage</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package dnsmessage provides a mostly RFC 1035 compliant implementation of DNS message packing and unpacking.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package dnsmessage provides a mostly RFC 1035 compliant implementation of DNS message packing and unpacking.</td></tr>

      
          
  
  <tr data-aria-controls="html-atom html-charset "
      class="">
    <td data-id="html" data-aria-owns="html-atom html-charset ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton"
                aria-expanded="false"
                aria-label="2 more from"
                data-aria-controls="html-atom html-charset "
                data-aria-labelledby="html-button html"
                data-id="html-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><a href="/golang.org/x/net@v0.62.0/html">html</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package html implements an HTML5-compliant tokenizer and parser.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package html implements an HTML5-compliant tokenizer and parser.</td></tr><tr data-id="html-atom" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/html/atom">atom</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package atom provides integer codes (also known as atoms) for a fixed set of frequently occurring HTML strings: tag names and attribute keys such as &#34;p&#34; and &#34;id&#34;.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package atom provides integer codes (also known as atoms) for a fixed set of frequently occurring HTML strings: tag names and attribute keys such as &#34;p&#34; and &#34;id&#34;.</td><tr data-id="html-charset" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/html/charset">charset</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package charset provides common text encodings for HTML documents.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package charset provides common text encodings for HTML documents.</td></tr>

      
          
  
  <tr data-aria-controls="http-httpguts http-httpproxy "
      class="">
    <td data-id="http" data-aria-owns="http-httpguts http-httpproxy ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton"
                aria-expanded="false"
                aria-label="2 more from"
                data-aria-controls="http-httpguts http-httpproxy "
                data-aria-labelledby="http-button http"
                data-id="http-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><span>http</span>
      </td>
      <td class="UnitDirectories-desktopSynopsis"></td></tr><tr data-id="http-httpguts" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/http/httpguts">httpguts</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package httpguts provides functions implementing various details of the HTTP specification.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package httpguts provides functions implementing various details of the HTTP specification.</td><tr data-id="http-httpproxy" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/http/httpproxy">httpproxy</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package httpproxy provides support for HTTP proxy determination based on environment variables, as provided by net/http.ProxyFromEnvironment function.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package httpproxy provides support for HTTP proxy determination based on environment variables, as provided by net/http.ProxyFromEnvironment function.</td></tr>

      
          
  
  <tr data-aria-controls="http2-h2c http2-h2i http2-hpack http2-h2demo "
      class="">
    <td data-id="http2" data-aria-owns="http2-h2c http2-h2i http2-hpack http2-h2demo ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton"
                aria-expanded="false"
                aria-label="4 more from"
                data-aria-controls="http2-h2c http2-h2i http2-hpack http2-h2demo "
                data-aria-labelledby="http2-button http2"
                data-id="http2-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><a href="/golang.org/x/net@v0.62.0/http2">http2</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package http2 implements the HTTP/2 protocol.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package http2 implements the HTTP/2 protocol.</td></tr><tr data-id="http2-h2c" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/http2/h2c">h2c</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package h2c is deprecated.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package h2c is deprecated.</td><tr data-id="http2-h2i" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/http2/h2i">h2i</a>
            
            <span class="go-Chip go-Chip--inverted">command</span>
          </span>
          <div class="UnitDirectories-mobileSynopsis">The h2i command is an interactive HTTP/2 console.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">The h2i command is an interactive HTTP/2 console.</td><tr data-id="http2-hpack" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/http2/hpack">hpack</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package hpack implements HPACK, a compression format for efficiently representing HTTP header fields in the context of HTTP/2.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package hpack implements HPACK, a compression format for efficiently representing HTTP header fields in the context of HTTP/2.</td><tr data-id="http2-h2demo" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net/http2/h2demo">h2demo</a>
            <span class="go-Chip go-Chip--inverted">module</span>
            
          </span>
          <div class="UnitDirectories-mobileSynopsis"></div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis"></td></tr>

      
          
  
  <tr
      class="">
    <td data-id="icmp" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/icmp">icmp</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package icmp provides basic functions for the manipulation of messages used in the Internet Control Message Protocols, ICMPv4 and ICMPv6.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package icmp provides basic functions for the manipulation of messages used in the Internet Control Message Protocols, ICMPv4 and ICMPv6.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="idna" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/idna">idna</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package idna implements IDNA2008 using the compatibility processing defined by UTS (Unicode Technical Standard) #46, which defines a standard to deal with the transition from IDNA2003.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package idna implements IDNA2008 using the compatibility processing defined by UTS (Unicode Technical Standard) #46, which defines a standard to deal with the transition from IDNA2003.</td></tr></tr>

      
          
  
  <tr data-aria-controls="internal-gate internal-httpcommon internal-httpsfv internal-iana internal-quic/cmd/interop internal-quic/quicwire internal-socket internal-socks internal-sockstest internal-testcert internal-timeseries "
      class="UnitDirectories-internal">
    <td data-id="internal" data-aria-owns="internal-gate internal-httpcommon internal-httpsfv internal-iana internal-quic/cmd/interop internal-quic/quicwire internal-socket internal-socks internal-sockstest internal-testcert internal-timeseries ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton UnitDirectories-internal"
                aria-expanded="false"
                aria-label="11 more from"
                data-aria-controls="internal-gate internal-httpcommon internal-httpsfv internal-iana internal-quic/cmd/interop internal-quic/quicwire internal-socket internal-socks internal-sockstest internal-testcert internal-timeseries "
                data-aria-labelledby="internal-button internal"
                data-id="internal-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><span>internal</span>
      </td>
      <td class="UnitDirectories-desktopSynopsis"></td></tr><tr data-id="internal-gate" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/gate">gate</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package gate contains an alternative condition variable.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package gate contains an alternative condition variable.</td><tr data-id="internal-httpcommon" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/httpcommon">httpcommon</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis"></div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis"></td><tr data-id="internal-httpsfv" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/httpsfv">httpsfv</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package httpsfv provides functionality for dealing with HTTP Structured Field Values.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package httpsfv provides functionality for dealing with HTTP Structured Field Values.</td><tr data-id="internal-iana" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/iana">iana</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package iana provides protocol number resources managed by the Internet Assigned Numbers Authority (IANA).</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package iana provides protocol number resources managed by the Internet Assigned Numbers Authority (IANA).</td><tr data-id="internal-quic/cmd/interop" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/quic/cmd/interop">quic/cmd/interop</a>
            
            <span class="go-Chip go-Chip--inverted">command</span>
          </span>
          <div class="UnitDirectories-mobileSynopsis">The interop command is the client and server used by QUIC interoperability tests.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">The interop command is the client and server used by QUIC interoperability tests.</td><tr data-id="internal-quic/quicwire" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/quic/quicwire">quic/quicwire</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package quicwire encodes and decode QUIC/HTTP3 wire encoding types, particularly variable-length integers.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package quicwire encodes and decode QUIC/HTTP3 wire encoding types, particularly variable-length integers.</td><tr data-id="internal-socket" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/socket">socket</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package socket provides a portable interface for socket system calls.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package socket provides a portable interface for socket system calls.</td><tr data-id="internal-socks" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/socks">socks</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package socks provides a SOCKS version 5 client implementation.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package socks provides a SOCKS version 5 client implementation.</td><tr data-id="internal-sockstest" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/sockstest">sockstest</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package sockstest provides utilities for SOCKS testing.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package sockstest provides utilities for SOCKS testing.</td><tr data-id="internal-testcert" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/testcert">testcert</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package testcert contains a test-only localhost certificate.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package testcert contains a test-only localhost certificate.</td><tr data-id="internal-timeseries" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/internal/timeseries">timeseries</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package timeseries implements a time series structure for stats collection.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package timeseries implements a time series structure for stats collection.</td></tr>

      
          
  
  <tr
      class="">
    <td data-id="ipv4" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/ipv4">ipv4</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package ipv4 implements IP-level socket options for the Internet Protocol version 4.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package ipv4 implements IP-level socket options for the Internet Protocol version 4.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="ipv6" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/ipv6">ipv6</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package ipv6 implements IP-level socket options for the Internet Protocol version 6.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package ipv6 implements IP-level socket options for the Internet Protocol version 6.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="nettest" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/nettest">nettest</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package nettest provides utilities for network testing.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package nettest provides utilities for network testing.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="netutil" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/netutil">netutil</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package netutil provides network utility functions, complementing the more common ones in the net package.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package netutil provides network utility functions, complementing the more common ones in the net package.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="proxy" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/proxy">proxy</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package proxy provides support for a variety of protocols to proxy network data.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package proxy provides support for a variety of protocols to proxy network data.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="publicsuffix" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/publicsuffix">publicsuffix</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package publicsuffix provides a public suffix list based on data from https://publicsuffix.org/</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package publicsuffix provides a public suffix list based on data from https://publicsuffix.org/</td></tr></tr>

      
          
  
  <tr data-aria-controls="quic-qlog "
      class="">
    <td data-id="quic" data-aria-owns="quic-qlog ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton"
                aria-expanded="false"
                aria-label="1 more from"
                data-aria-controls="quic-qlog "
                data-aria-labelledby="quic-button quic"
                data-id="quic-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><a href="/golang.org/x/net@v0.62.0/quic">quic</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package quic implements the QUIC protocol.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package quic implements the QUIC protocol.</td></tr><tr data-id="quic-qlog" class="">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/quic/qlog">qlog</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package qlog serializes qlog events.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package qlog serializes qlog events.</td></tr>

      
          
  
  <tr
      class="">
    <td data-id="route" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/route">route</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package route provides basic functions for the manipulation of packet routing facilities on BSD variants.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package route provides basic functions for the manipulation of packet routing facilities on BSD variants.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="trace" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/trace">trace</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package trace implements tracing of requests and long-lived objects.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package trace implements tracing of requests and long-lived objects.</td></tr></tr>

      
          
  
  <tr data-aria-controls="webdav-internal/xml "
      class="">
    <td data-id="webdav" data-aria-owns="webdav-internal/xml ">
      <div class="UnitDirectories-pathCell">
        <div><button type="button" class="go-Button go-Button--inline UnitDirectories-toggleButton UnitDirectories-internal"
                aria-expanded="false"
                aria-label="1 more from"
                data-aria-controls="webdav-internal/xml "
                data-aria-labelledby="webdav-button webdav"
                data-id="webdav-button">
              <img class="go-Icon" height="24" width="24" src="/static/shared/icon/arrow_right_gm_grey_24dp.svg"
                  alt="">
            </button><a href="/golang.org/x/net@v0.62.0/webdav">webdav</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package webdav provides a WebDAV server implementation.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package webdav provides a WebDAV server implementation.</td></tr><tr data-id="webdav-internal/xml" class="UnitDirectories-internal">
      <td>
        <div class="UnitDirectories-subdirectory">
          <span>
            <a href="/golang.org/x/net@v0.62.0/webdav/internal/xml">internal/xml</a>
            
            
          </span>
          <div class="UnitDirectories-mobileSynopsis">Package xml implements a simple XML 1.0 parser that understands XML name spaces.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package xml implements a simple XML 1.0 parser that understands XML name spaces.</td></tr>

      
          
  
  <tr
      class="">
    <td data-id="websocket" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/websocket">websocket</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package websocket implements a client and server for the WebSocket protocol as specified in RFC 6455.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package websocket implements a client and server for the WebSocket protocol as specified in RFC 6455.</td></tr></tr>

      
          
  
  <tr
      class="">
    <td data-id="xsrftoken" data-aria-owns="">
      <div class="UnitDirectories-pathCell">
        <div><a href="/golang.org/x/net@v0.62.0/xsrftoken">xsrftoken</a>
            
          </div>
          <div class="UnitDirectories-mobileSynopsis">Package xsrftoken provides methods for generating and validating secure XSRF tokens.</div>
        </div>
      </td>
      <td class="UnitDirectories-desktopSynopsis">Package xsrftoken provides methods for generating and validating secure XSRF tokens.</td></tr></tr>

      
    </table>
  </div>

      
    </div>
  </div>
  <div id="showInternal-description" hidden> Click to show internal directories. </div>
  <div id="hideInternal-description" hidden> Click to hide internal directories. </div>
</article>
    <footer class="go-Main-footer"></footer>
  </main>

    
  <footer class="go-Footer">
    
    <div class="go-Footer-links">
      <div class="go-Footer-linkColumn">
        <a href="https://go.dev/solutions" class="go-Footer-link go-Footer-link--primary"
            data-gtmc="footer link">
          Why Go
        </a>
        <a href="https://go.dev/solutions/use-cases" class="go-Footer-link"
            data-gtmc="footer link">
          Use Cases
        </a>
        <a href="https://go.dev/solutions/case-studies" class="go-Footer-link"
            data-gtmc="footer link">
          Case Studies
        </a>
      </div>
      <div class="go-Footer-linkColumn">
        <a href="https://learn.go.dev/" class="go-Footer-link go-Footer-link--pr