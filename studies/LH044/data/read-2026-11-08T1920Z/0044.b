<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />

        <title>laravel/framework - Packagist.org</title>
        <meta name="description" content="The Laravel Framework." />
        <meta name="author" content="Jordi Boggiano" />
            <link rel="canonical" href="https://packagist.org/packages/laravel/framework" />

        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <link rel="shortcut icon" href="/favicon.ico?v=1793979009" />

        <link rel="stylesheet" href="/build/app.css?v=1793979009" />
        
            <link rel="alternate" type="application/rss+xml" title="New Releases - laravel/framework" href="https://packagist.org/feeds/package.laravel/framework.rss" />
    <link rel="alternate" type="application/rss+xml" title="New Releases - laravel" href="https://packagist.org/feeds/vendor.laravel.rss" />
            <link rel="alternate" type="application/rss+xml" title="Newly Submitted Packages - Packagist.org" href="https://packagist.org/feeds/packages.rss" />
        <link rel="alternate" type="application/rss+xml" title="New Releases - Packagist.org" href="https://packagist.org/feeds/releases.rss" />
        

        <link rel="search" type="application/opensearchdescription+xml" href="/search.osd?v=1793979009" title="Packagist.org" />

        <script nonce="CChVXH0+2OFecaL8IvzCBQ==">
            var onloadRecaptchaCallback = function() {
                document.querySelectorAll('.recaptcha-protected').forEach((el) => {
                    el.closest('form').querySelectorAll('button, input[type="submit"]').forEach((submit) => {
                        grecaptcha.render(submit, {
                            'sitekey' : '6LfKiPoUAAAAAGlKWkhEEx7X8muIVYy6oA0GNdX0',
                            'callback' : function (token) {
                                submit.form.submit();
                            }
                        });
                    })
                });
            };
        </script>
        
            <link rel="stylesheet" href="/css/github/markdown.css?v=1793979009">
        </head>
    <body>
    <section class="wrap">
        <header class="navbar-wrapper fixed-top">
                        <nav class="container">
                <div class="navbar navbar-expand-md" role="navigation">                        <h1 class="navbar-brand"><a href="/">Packagist</a> <em class="d-none d-lg-inline">The PHP Package Repository</em></h1>                    <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#main-navigation" aria-controls="main-navigation" aria-expanded="false">
                        <span class="visually-hidden">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>

                    <div class="collapse navbar-collapse" id="main-navigation">
                        <ul class="nav navbar-nav">
                            <li>
                                <a href="/explore/">Browse</a>
                            </li>
                            <li>
                                <a href="/about">About Packagist.org</a>
                            </li>
                            <li>
                                <a href="/packages/submit">Submit</a>
                            </li>                            <li>
                                <a href="/register/">Create account</a>
                            </li>
                            <li class="nav-user">
                                <section class="nav-user-signin">
                                    <a href="/login/">Sign in</a>

                                    <section class="signin-box">
                                        <form action="/login/" method="POST" id="nav_login">
                                            <div class="input-group">
                                                <span class="input-group-text"><span class="icon-user"></span></span>
                                                <input class="form-control" type="text" id="_username" name="_username" placeholder="Username / Email">
                                            </div>
                                            <div class="input-group">
                                                <span class="input-group-text"><span class="icon-lock"></span></span>
                                                <input class="form-control" type="password" id="_password" name="_password" placeholder="Password">
                                            </div>

                                            <div class="form-check">
                                                <input class="form-check-input" type="checkbox" id="_remember_me" name="_remember_me" value="on" checked="checked" />
                                                <label class="form-check-label" for="_remember_me">Remember me</label>
                                            </div>
                                            <div class="signin-box-buttons">
                                                <a href="/login/github" class="float-end btn btn-primary btn-github"><span class="icon-github"></span>Use Github</a>
                                                <button type="submit" class="btn btn-success" id="_submit_mini" name="_submit">Log in</button>
                                            </div>
                                        </form>

                                        <div class="signin-box-register">
                                            <a href="/register/">No account yet? Create one now!</a>
                                        </div>
                                    </section>
                                </section>
                            </li>                        </ul>
                    </div>
                </div>
            </nav>
        </header>

        <section class="wrapper wrapper-search">
    <div class="container ">
        <form name="search_query" method="get" action="/search/" id="search-form" autocomplete="off">
            <div class="sortable row">
                <div class="col-12 js-search-field-wrapper col-lg-9">
                    <input type="search" id="search_query_query" name="query" required="required" autocomplete="off" placeholder="Search packages..." tabindex="1" class=" form-control" value="" />
                </div>
            </div>
        </form>    </div>
</section>


                
        
        <section class="wrapper">
            <section class="container content" role="main">
                                    <div id="search-container" class="d-none">
                        <div class="row">
                            <div class="search-list col-lg-9"></div>

                            <div class="search-facets col-lg-3">
                                <div class="search-facets-active-filters-wrapper" style="display:none">
                                    <div class="search-facets-active-filters-header">
                                        <span>Active filters</span>
                                        <div class="search-facets-clear-all"></div>
                                    </div>
                                    <div class="search-facets-active-filters"></div>
                                </div>
                                <div class="search-facets-type"></div>
                                <div class="search-facets-tags"></div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-lg-9">
                                <div id="powered-by">
                                    Search by <a href="https://www.algolia.com/"><img src="/img/sponsors/algolia-logo-light.svg?v=1793979009"></a>
                                </div>
                                <div id="pagination-container">
                                    <div class="pagination-mount"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                
                    <div class="row" id="view-package-page">
        <div class="col-12 package">
            <div class="package-header">
                <div class="row align-items-end g-2">
                    <div class="col-12 col-md">
                        <h2 class="title">
                                                        <a href="/packages/laravel/">laravel<span class="d-none"> </span>/</a><span class="d-none"> </span>framework
                        </h2>
                    </div>
                                            <div class="col-12 col-md-auto package-maintainers">
                            <p class="maintainers"><a href="/users/taylorotwell/" title="taylorotwell"><img width="40" height="40" alt="taylorotwell" src="https://www.gravatar.com/avatar/3074e5279656dc3b82e00ea7ba28e24824b7b5e1a3390927d45291a7c6c1faab?s=40&amp;d=identicon" srcset="https://www.gravatar.com/avatar/3074e5279656dc3b82e00ea7ba28e24824b7b5e1a3390927d45291a7c6c1faab?s=80&amp;d=identicon 2x"></a></p>
                        </div>
                                    </div>
            </div>

            <div class="row">
                <div class="col-lg-9">
                    <p class="requireme"><i class="bi bi-terminal"></i> <input type="text" readonly="readonly" value="composer require laravel/framework" /></p>

                    
                    
                                        
                    
                    <p class="description">The Laravel Framework.</p>

                                    </div>

                <div class="col-lg-3">
                    
                                            <div class="package-aside facts">
                            <div class="package-downloads-chart js-downloads-chart"></div>
                        </div>
                                    </div>
            </div>

            <div class="row package-facts">
                <div class="col-12 col-md-6 col-lg">
                    <div class="package-aside details">
                        <h5>Package info</h5>
                        <p class="canonical">
                            <a href="https://github.com/laravel/framework" title="Canonical Repository URL">github.com/laravel/framework</a>
                        </p>

                                                    <p><a rel="nofollow noopener external noindex ugc" href="https://laravel.com">Homepage</a></p>
                                                                                                                                                                                                                                                                        <p class="purl"><span title="PURL / Package-URL">pkg:composer/laravel/framework</span></p>
                    </div>
                </div>

                <div class="col-12 col-md-6 col-lg">
                    <div class="package-aside facts">
                        <h5>Security</h5>
                                                    <p>
                                <span>
                                    <a href="/packages/laravel/framework/advisories" rel="nofollow">Advisories</a>:
                                </span>
                                30
                            </p>
                                                                        <p>
                            <a rel="nofollow noopener external noindex ugc" href="https://intel.aikido.dev/packages/packagist/laravel/framework">
                                Aikido package health analysis
                            </a>
                        </p>
                        <p><a rel="nofollow noindex" href="/transparency-log?package=laravel/framework">Transparency log</a></p>
                    </div>
                </div>

                
                <div class="col-12 col-md-6 col-lg">
                    <div class="package-aside facts">
                        <h5>Statistics</h5>
                        <p>
                            <span>
                                <a href="/packages/laravel/framework/stats" rel="nofollow">Installs</a>:
                            </span>
                            615&#8201;441&#8201;477                        </p>
                                                    <p>
                                <span>
                                    <a href="/packages/laravel/framework/dependents?order_by=downloads" rel="nofollow">Dependents</a>:
                                </span>
                                21&#8201;436
                            </p>
                                                                            <p>
                                <span>
                                    <a href="/packages/laravel/framework/suggesters" rel="nofollow">Suggesters</a>:
                                </span>
                                364
                            </p>
                                                                            <p>
                                <span>
                                    <a href="https://github.com/laravel/framework/stargazers">Stars</a>:
                                </span>
                                34&#8201;997
                            </p>
                                                                            <p>
                                <span>
                                    <a rel="nofollow noopener external noindex ugc" href="https://github.com/laravel/framework/issues">Open Issues</a>:
                                </span>
                                84
                            </p>
                                            </div>
                </div>
            </div>

                            <div class="row versions-section">
                    <div class="version-details col-lg-9">
                                                    

<div class="title">
    <span class="version-number">v13.40.0</span>

    <span class="release-date" title="Release Date (can be forged)">
        2026-11-03 15:07 UTC
    </span>
    </div>

<div class="clearfix package-links">
            <div class="row">
                            <div class="clearfix d-none d-md-block d-lg-none"></div>                <div class="clearfix d-none d-lg-block"></div>                <div class="requires col-md-6 col-lg-4 ">
                    <p class="link-type">Requires</p>
                                            <ul><li>php: ^8.3</li><li>composer-runtime-api: ^2.2</li><li><a href="/providers/ext-ctype">ext-ctype</a>: *</li><li>ext-filter: *</li><li>ext-hash: *</li><li><a href="/providers/ext-mbstring">ext-mbstring</a>: *</li><li><a href="/providers/ext-openssl">ext-openssl</a>: *</li><li>ext-session: *</li><li>ext-tokenizer: *</li><li><a href="/packages/brick/math">brick/math</a>: ^0.14.2 || ^0.15 || ^0.16 || ^0.17 || ^0.18 || ^0.19 || ^0.20 || ^1.0</li><li><a href="/packages/doctrine/inflector">doctrine/inflector</a>: ^2.0.5</li><li><a href="/packages/dragonmantank/cron-expression">dragonmantank/cron-expression</a>: ^3.4</li><li><a href="/packages/egulias/email-validator">egulias/email-validator</a>: ^4.0</li><li><a href="/packages/fruitcake/php-cors">fruitcake/php-cors</a>: ^1.3</li><li><a href="/packages/guzzlehttp/guzzle">guzzlehttp/guzzle</a>: ^7.8.2 || ^8.0</li><li><a href="/packages/guzzlehttp/promises">guzzlehttp/promises</a>: ^2.0.3 || ^3.0</li><li><a href="/packages/guzzlehttp/psr7">guzzlehttp/psr7</a>: ^2.9 || ^3.0</li><li><a href="/packages/guzzlehttp/uri-template">guzzlehttp/uri-template</a>: ^1.0 || ^2.0</li><li><a href="/packages/laravel/prompts">laravel/prompts</a>: ^0.3.25</li><li><a href="/packages/laravel/serializable-closure">laravel/serializable-closure</a>: ^2.0.10</li><li><a href="/packages/league/commonmark">league/commonmark</a>: ^2.8.1</li><li><a href="/packages/league/flysystem">league/flysystem</a>: ^3.25.1</li><li><a href="/packages/league/flysystem-local">league/flysystem-local</a>: ^3.25.1</li><li><a href="/packages/league/uri">league/uri</a>: ^7.5.1</li><li><a href="/packages/monolog/monolog">monolog/monolog</a>: ^3.10</li><li><a href="/packages/nesbot/carbon">nesbot/carbon</a>: ^3.8.4</li><li><a href="/packages/nunomaduro/termwind">nunomaduro/termwind</a>: ^2.0</li><li><a href="/packages/psr/container">psr/container</a>: ^1.1.1 || ^2.0.1</li><li><a href="/packages/psr/http-message">psr/http-message</a>: ^1.0 || ^2.0</li><li><a href="/packages/psr/log">psr/log</a>: ^1.0 || ^2.0 || ^3.0</li><li><a href="/packages/psr/simple-cache">psr/simple-cache</a>: ^1.0 || ^2.0 || ^3.0</li><li><a href="/packages/ramsey/uuid">ramsey/uuid</a>: ^4.7</li><li><a href="/packages/symfony/console">symfony/console</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/error-handler">symfony/error-handler</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/finder">symfony/finder</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/http-foundation">symfony/http-foundation</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/http-kernel">symfony/http-kernel</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/mailer">symfony/mailer</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/mime">symfony/mime</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/polyfill-php84">symfony/polyfill-php84</a>: ^1.36</li><li><a href="/packages/symfony/polyfill-php85">symfony/polyfill-php85</a>: ^1.36</li><li><a href="/packages/symfony/polyfill-php86">symfony/polyfill-php86</a>: ^1.36</li><li><a href="/packages/symfony/process">symfony/process</a>: ^7.4.5 || ^8.0.5</li><li><a href="/packages/symfony/routing">symfony/routing</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/uid">symfony/uid</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/var-dumper">symfony/var-dumper</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/tijsverkoyen/css-to-inline-styles">tijsverkoyen/css-to-inline-styles</a>: ^2.2.5</li><li><a href="/packages/vlucas/phpdotenv">vlucas/phpdotenv</a>: ^5.6.1</li><li><a href="/packages/voku/portable-ascii">voku/portable-ascii</a>: ^2.0.2</li></ul>
                                    </div>
                                                            <div class="devRequires col-md-6 col-lg-4 ">
                    <p class="link-type">Requires (Dev)</p>
                                            <ul><li>ext-gmp: *</li><li><a href="/packages/ably/ably-php">ably/ably-php</a>: ^1.0</li><li><a href="/packages/aws/aws-sdk-php">aws/aws-sdk-php</a>: ^3.322.9</li><li><a href="/packages/fakerphp/faker">fakerphp/faker</a>: ^1.24</li><li><a href="/packages/intervention/image">intervention/image</a>: ^4.2</li><li><a href="/packages/laravel/pint">laravel/pint</a>: ^1.18</li><li><a href="/packages/league/flysystem-aws-s3-v3">league/flysystem-aws-s3-v3</a>: ^3.25.1</li><li><a href="/packages/league/flysystem-ftp">league/flysystem-ftp</a>: ^3.25.1</li><li><a href="/packages/league/flysystem-path-prefixing">league/flysystem-path-prefixing</a>: ^3.25.1</li><li><a href="/packages/league/flysystem-read-only">league/flysystem-read-only</a>: ^3.25.1</li><li><a href="/packages/league/flysystem-sftp-v3">league/flysystem-sftp-v3</a>: ^3.25.1</li><li><a href="/packages/mockery/mockery">mockery/mockery</a>: ^1.6.10</li><li><a href="/packages/opis/json-schema">opis/json-schema</a>: ^2.4.1</li><li><a href="/packages/orchestra/testbench-core">orchestra/testbench-core</a>: ^11.6.0</li><li><a href="/packages/pda/pheanstalk">pda/pheanstalk</a>: ^7.0.0 || ^8.0.0</li><li><a href="/packages/php-http/discovery">php-http/discovery</a>: ^1.15</li><li><a href="/packages/phpstan/phpstan">phpstan/phpstan</a>: 2.3.1</li><li><a href="/packages/phpunit/phpunit">phpunit/phpunit</a>: ^11.5.50 || ^12.5.8 || ^13.0.3</li><li><a href="/packages/predis/predis">predis/predis</a>: ^2.3 || ^3.0</li><li><a href="/packages/rector/rector">rector/rector</a>: 2.6.3</li><li><a href="/packages/resend/resend-php">resend/resend-php</a>: ^1.0</li><li><a href="/packages/symfony/cache">symfony/cache</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/http-client">symfony/http-client</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/mercure">symfony/mercure</a>: ^0.8.0</li><li><a href="/packages/symfony/psr-http-message-bridge">symfony/psr-http-message-bridge</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/symfony/translation">symfony/translation</a>: ^7.4.0 || ^8.0.0</li><li><a href="/packages/web-token/jwt-library">web-token/jwt-library</a>: ^4.1</li></ul>
                                    </div>
                            <div class="clearfix d-none d-md-block d-lg-none"></div>                                <div class="suggests col-md-6 col-lg-4 ">
                    <p class="link-type">Suggests</p>
                                            <ul><li><a href="/providers/ext-apcu">ext-apcu</a>: Required to use the APC cache driver.</li><li>ext-fileinfo: Required to use the Filesystem class.</li><li><a href="/providers/ext-ftp">ext-ftp</a>: Required to use the Flysystem FTP driver.</li><li>ext-gd: Required to use Illuminate\Http\Testing\FileFactory::image().</li><li><a href="/providers/ext-memcached">ext-memcached</a>: Required to use the memcache cache driver.</li><li>ext-pcntl: Required to use all features of the queue worker and console signal trapping.</li><li><a href="/providers/ext-pdo">ext-pdo</a>: Required to use all database features.</li><li>ext-posix: Required to use all features of the queue worker.</li><li><a href="/providers/ext-redis">ext-redis</a>: Required to use the Redis cache and queue drivers (^4.0 || ^5.0 || ^6.0).</li><li><a href="/packages/ably/ably-php">ably/ably-php</a>: Required to use the Ably broadcast driver (^1.0).</li><li><a href="/packages/aws/aws-sdk-php">aws/aws-sdk-php</a>: Required to use the SQS queue driver, DynamoDb failed job storage, and SES mail driver (^3.322.9).</li><li><a href="/packages/brianium/paratest">brianium/paratest</a>: Required to run tests in parallel (^7.0 || ^8.0).</li><li><a href="/packages/fakerphp/faker">fakerphp/faker</a>: Required to generate fake data using the fake() helper (^1.23).</li><li><a href="/packages/filp/whoops">filp/whoops</a>: Required for friendly error pages in development (^2.14.3).</li><li><a href="/packages/intervention/image">intervention/image</a>: Required to use the image processing features (^4.2).</li><li><a href="/packages/laravel/tinker">laravel/tinker</a>: Required to use the tinker console command (^2.0).</li><li><a href="/packages/league/flysystem-aws-s3-v3">league/flysystem-aws-s3-v3</a>: Required to use the Flysystem S3 driver (^3.25.1).</li><li><a href="/packages/league/flysystem-ftp">league/flysystem-ftp</a>: Required to use the Flysystem FTP driver (^3.25.1).</li><li><a href="/packages/league/flysystem-path-prefixing">league/flysystem-path-prefixing</a>: Required to use the scoped driver (^3.25.1).</li><li><a href="/packages/league/flysystem-read-only">league/flysystem-read-only</a>: Required to use read-only disks (^3.25.1)</li><li><a href="/packages/league/flysystem-sftp-v3">league/flysystem-sftp-v3</a>: Required to use the Flysystem SFTP driver (^3.25.1).</li><li><a href="/packages/mockery/mockery">mockery/mockery</a>: Required to use mocking (^1.6).</li><li><a href="/packages/pda/pheanstalk">pda/pheanstalk</a>: Required to use the beanstalk queue driver (^7.0 || ^8.0).</li><li><a href="/packages/php-http/discovery">php-http/discovery</a>: Required to use PSR-7 bridging features (^1.15).</li><li><a href="/packages/phpunit/phpunit">phpunit/phpunit</a>: Required to use assertions and run tests (^11.5.50 || ^12.5.8 || ^13.0.3).</li><li><a href="/packages/predis/predis">predis/predis</a>: Required to use the predis connector (^2.3 || ^3.0).</li><li><a href="/packages/pusher/pusher-php-server">pusher/pusher-php-server</a>: Required to use the Pusher broadcast driver (^6.0 || ^7.0).</li><li><a href="/packages/resend/resend-php">resend/resend-php</a>: Required to enable support for the Resend mail transport (^0.10.0 || ^1.0).</li><li><a href="/packages/spatie/fork">spatie/fork</a>: Required to use the &#039;fork&#039; concurrency driver (^1.2).</li><li><a href="/packages/symfony/cache">symfony/cache</a>: Required to PSR-6 cache bridge (^7.4 || ^8.0).</li><li><a href="/packages/symfony/filesystem">symfony/filesystem</a>: Required to enable support for relative symbolic links (^7.4 || ^8.0).</li><li><a href="/packages/symfony/http-client">symfony/http-client</a>: Required to enable support for the Symfony API mail transports (^7.4 || ^8.0).</li><li><a href="/packages/symfony/mailgun-mailer">symfony/mailgun-mailer</a>: Required to enable support for the Mailgun mail transport (^7.4 || ^8.0).</li><li><a href="/packages/symfony/mercure">symfony/mercure</a>: Required to use the Mercure broadcast driver (^0.8).</li><li><a href="/packages/symfony/postmark-mailer">symfony/postmark-mailer</a>: Required to enable support for the Postmark mail transport (^7.4 || ^8.0).</li><li><a href="/packages/symfony/psr-http-message-bridge">symfony/psr-http-message-bridge</a>: Required to use PSR-7 bridging features (^7.4 || ^8.0).</li><li><a href="/packages/web-token/jwt-library">web-token/jwt-library</a>: Required to sign Mercure JWTs and use end-to-end encrypted channels (^4.1).</li></ul>
                                    </div>
                                            <div class="clearfix d-none d-lg-block"></div>                <div class="provides col-md-6 col-lg-4 ">
                    <p class="link-type">Provides</p>
                                            <ul><li><a href="/providers/psr/container-implementation">psr/container-implementation</a>: 1.1 || 2.0</li><li><a href="/providers/psr/log-implementation">psr/log-implementation</a>: 1.0 || 2.0 || 3.0</li><li><a href="/providers/psr/simple-cache-implementation">psr/simple-cache-implementation</a>: 1.0 || 2.0 || 3.0</li></ul>
                                    </div>
                            <div class="clearfix d-none d-md-block d-lg-none"></div>                                <div class="conflicts col-md-6 col-lg-4 ">
                    <p class="link-type">Conflicts</p>
                                            <ul><li><a href="/packages/tightenco/collect">tightenco/collect</a>: &lt;5.5.33</li></ul>
                                    </div>
                                                            <div class="replaces col-md-6 col-lg-4 ">
                    <p class="link-type">Replaces</p>
                                            <ul><li><a href="/packages/illuminate/auth">illuminate/auth</a>: v13.40.0</li><li><a href="/packages/illuminate/broadcasting">illuminate/broadcasting</a>: v13.40.0</li><li><a href="/packages/illuminate/bus">illuminate/bus</a>: v13.40.0</li><li><a href="/packages/illuminate/cache">illuminate/cache</a>: v13.40.0</li><li><a href="/packages/illuminate/collections">illuminate/collections</a>: v13.40.0</li><li>illuminate/concurrency: v13.40.0</li><li><a href="/packages/illuminate/conditionable">illuminate/conditionable</a>: v13.40.0</li><li><a href="/packages/illuminate/config">illuminate/config</a>: v13.40.0</li><li><a href="/packages/illuminate/console">illuminate/console</a>: v13.40.0</li><li><a href="/packages/illuminate/container">illuminate/container</a>: v13.40.0</li><li><a href="/packages/illuminate/contracts">illuminate/contracts</a>: v13.40.0</li><li><a href="/packages/illuminate/cookie">illuminate/cookie</a>: v13.40.0</li><li><a href="/packages/illuminate/database">illuminate/database</a>: v13.40.0</li><li><a href="/packages/illuminate/encryption">illuminate/encryption</a>: v13.40.0</li><li><a href="/packages/illuminate/events">illuminate/events</a>: v13.40.0</li><li><a href="/packages/illuminate/filesystem">illuminate/filesystem</a>: v13.40.0</li><li><a href="/packages/illuminate/hashing">illuminate/hashing</a>: v13.40.0</li><li><a href="/packages/illuminate/http">illuminate/http</a>: v13.40.0</li><li><a href="/packages/illuminate/image">illuminate/image</a>: v13.40.0</li><li><a href="/packages/illuminate/json-schema">illuminate/json-schema</a>: v13.40.0</li><li><a href="/packages/illuminate/log">illuminate/log</a>: v13.40.0</li><li><a href="/packages/illuminate/macroable">illuminate/macroable</a>: v13.40.0</li><li><a href="/packages/illuminate/mail">illuminate/mail</a>: v13.40.0</li><li><a href="/packages/illuminate/notifications">illuminate/notifications</a>: v13.40.0</li><li><a href="/packages/illuminate/pagination">illuminate/pagination</a>: v13.40.0</li><li><a href="/packages/illuminate/pipeline">illuminate/pipeline</a>: v13.40.0</li><li><a href="/packages/illuminate/process">illuminate/process</a>: v13.40.0</li><li><a href="/packages/illuminate/queue">illuminate/queue</a>: v13.40.0</li><li><a href="/packages/illuminate/redis">illuminate/redis</a>: v13.40.0</li><li><a href="/packages/illuminate/reflection">illuminate/reflection</a>: v13.40.0</li><li><a href="/packages/illuminate/routing">illuminate/routing</a>: v13.40.0</li><li><a href="/packages/illuminate/session">illuminate/session</a>: v13.40.0</li><li><a href="/packages/illuminate/support">illuminate/support</a>: v13.40.0</li><li><a href="/packages/illuminate/testing">illuminate/testing</a>: v13.40.0</li><li><a href="/packages/illuminate/translation">illuminate/translation</a>: v13.40.0</li><li><a href="/packages/illuminate/validation">illuminate/validation</a>: v13.40.0</li><li><a href="/packages/illuminate/view">illuminate/view</a>: v13.40.0</li><li><a href="/packages/spatie/once">spatie/once</a>: *</li></ul>
                                    </div>
                    </div>
    </div>

<div class="metadata">
    <p class="license"><i class="bi bi-c-circle" title="License"></i> MIT <span class="source-reference"><i class="bi bi-bookmark-fill" title="Source Reference"></i> 1449bf241017087fbd38c118ecaabef3f6797fdc</span></p>

            <i class="bi bi-person-fill" title="Authors"></i>
        <ul class="authors">
                            <li>Taylor Otwell                        <span class="d-none d-md-inline">&lt;taylor<span style="display:none">.woop</span>@laravel.com&gt;</span></li>
                    </ul>
    
            <p class="tags">
            <i class="bi bi-tag-fill" title="Tags"></i>
            <a rel="nofollow noindex" href="https://packagist.org/search/?tags=framework">framework</a><a rel="nofollow noindex" href="https://packagist.org/search/?tags=laravel">laravel</a></p>
    
    <p class="publish-time"><i class="bi bi-clock-fill"></i> Published on Packagist.org on 2026-11-03 15:08 UTC</p>
</div>

                                            </div>
                    <div class="col-lg-3">
                        <div class="package-aside versions-wrapper">
    <ul class="versions">
                                                        
            <li class="details-toggler version" data-version-id="13.x-dev" data-load-more="/versions/9771905.json">
                <a class="version-number" rel="nofollow noindex" href="#13.x-dev" >13.x-dev</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version open" data-version-id="v13.40.0" data-load-more="/versions/10985168.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.40.0" >v13.40.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.39.0" data-load-more="/versions/10931412.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.39.0" >v13.39.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.38.0" data-load-more="/versions/10875814.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.38.0" >v13.38.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.37.0" data-load-more="/versions/10850320.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.37.0" >v13.37.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.36.0" data-load-more="/versions/10829922.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.36.0" >v13.36.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.35.0" data-load-more="/versions/10783818.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.35.0" >v13.35.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.34.0" data-load-more="/versions/10740647.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.34.0" >v13.34.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.33.0" data-load-more="/versions/10700483.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.33.0" >v13.33.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.32.0" data-load-more="/versions/10664697.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.32.0" >v13.32.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.31.0" data-load-more="/versions/10630204.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.31.0" >v13.31.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.30.1" data-load-more="/versions/10598364.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.30.1" >v13.30.1</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.30.0" data-load-more="/versions/10596140.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.30.0" >v13.30.0</a>

                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.29.0" data-load-more="/versions/10569032.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.29.0" >v13.29.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10569032">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.28.0" data-load-more="/versions/10568991.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.28.0" >v13.28.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10568991">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.27.0" data-load-more="/versions/10566962.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.27.0" >v13.27.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10566962">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.26.1" data-load-more="/versions/10537700.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.26.1" >v13.26.1</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10537700">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.26.0" data-load-more="/versions/10535668.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.26.0" >v13.26.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10535668">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.25.0" data-load-more="/versions/10506104.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.25.0" >v13.25.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10506104">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.24.0" data-load-more="/versions/10474314.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.24.0" >v13.24.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10474314">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.23.0" data-load-more="/versions/10438104.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.23.0" >v13.23.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10438104">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.22.0" data-load-more="/versions/10428723.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.22.0" >v13.22.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10428723">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.21.1" data-load-more="/versions/10414316.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.21.1" >v13.21.1</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10414316">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.21.0" data-load-more="/versions/10413621.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.21.0" >v13.21.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10413621">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.20.0" data-load-more="/versions/10381266.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.20.0" >v13.20.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10381266">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.19.0" data-load-more="/versions/10354173.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.19.0" >v13.19.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10354173">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.18.1" data-load-more="/versions/10336216.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.18.1" >v13.18.1</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10336216">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.18.0" data-load-more="/versions/10324021.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.18.0" >v13.18.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10324021">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.17.0" data-load-more="/versions/10298679.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.17.0" >v13.17.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10298679">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.16.1" data-load-more="/versions/10262877.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.16.1" >v13.16.1</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10262877">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.16.0" data-load-more="/versions/10262682.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.16.0" >v13.16.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10262682">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.15.0" data-load-more="/versions/10232999.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.15.0" >v13.15.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10232999">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.14.0" data-load-more="/versions/10214920.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.14.0" >v13.14.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10214920">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.13.0" data-load-more="/versions/10203586.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.13.0" >v13.13.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10203586">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.12.0" data-load-more="/versions/10176456.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.12.0" >v13.12.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10176456">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.11.2" data-load-more="/versions/10149404.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.11.2" >v13.11.2</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10149404">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.11.1" data-load-more="/versions/10145936.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.11.1" >v13.11.1</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10145936">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.11.0" data-load-more="/versions/10145332.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.11.0" >v13.11.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10145332">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.10.0" data-load-more="/versions/10145286.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.10.0" >v13.10.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10145286">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.9.0" data-load-more="/versions/10121952.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.9.0" >v13.9.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10121952">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.8.0" data-load-more="/versions/10085328.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.8.0" >v13.8.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10085328">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.7.0" data-load-more="/versions/10061106.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.7.0" >v13.7.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10061106">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.6.0" data-load-more="/versions/10034480.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.6.0" >v13.6.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10034480">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.5.0" data-load-more="/versions/10005020.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.5.0" >v13.5.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=10005020">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.4.0" data-load-more="/versions/9974550.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.4.0" >v13.4.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=9974550">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.3.0" data-load-more="/versions/9956155.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.3.0" >v13.3.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=9956155">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.2.0" data-load-more="/versions/9918055.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.2.0" >v13.2.0</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=9918055">
                        <i class="bi bi-shield-exclamation" data-bs-toggle="tooltip" data-bs-placement="top" title="Version has security advisories" data-bs-container="body"></i>
                    </a>
                
                
                
                
                                
                
                                                            </li>
                                                        
            <li class="details-toggler version" data-version-id="v13.1.1" data-load-more="/versions/9890513.json">
                <a class="version-number" rel="nofollow noindex" href="#v13.1.1" >v13.1.1</a>

                                    <a rel="nofollow noindex" class="action-alert advisory-alert" href="/packages/laravel/framework/advisories?version=9890513">
                        <i class="bi bi-shield-