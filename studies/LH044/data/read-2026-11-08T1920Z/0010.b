<!DOCTYPE html>
<html lang="en-US" data-theme="codeberg-auto">
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	
	<title>forgejo/forgejo: Beyond coding. We forge. - Codeberg.org</title>
	<link rel="manifest" href="/manifest.json">
	<meta name="author" content="forgejo">
	<meta name="description" content="forgejo - Beyond coding. We forge.">
	<meta name="keywords" content="git,non-profit,foss,oss,free,software,open,source,code,hosting">
	<meta name="referrer" content="same-origin">


	<link rel="alternate" type="application/atom+xml" title="" href="/forgejo/forgejo.atom">
	<link rel="alternate" type="application/rss+xml" title="" href="/forgejo/forgejo.rss">

	<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
	<link rel="alternate icon" href="/assets/img/favicon.png" type="image/png">

	
<script>
	
	window.addEventListener('error', function(e) {window._globalHandlerErrors=window._globalHandlerErrors||[]; window._globalHandlerErrors.push(e);});
	window.addEventListener('unhandledrejection', function(e) {window._globalHandlerErrors=window._globalHandlerErrors||[]; window._globalHandlerErrors.push(e);});
	window.config = {
		appUrl: 'https:\/\/codeberg.org\/',
		appSubUrl: '',
		assetVersionEncoded: encodeURIComponent('17.0.0-99-322c239~gitea-1.22.0'), 
		assetUrlPrefix: '\/assets',
		runModeIsProd:  true ,
		customEmojis: new Set(["git","gitea","codeberg","gitlab","github","gogs","forgejo"]),
		pageData: {"DATETIMESTRINGS":{"FUTURE":"in future","NOW":"now","relativetime.1day":"yesterday","relativetime.1month":"last month","relativetime.1week":"last week","relativetime.1year":"last year"},"PLURALSTRINGS_FALLBACK":{},"PLURALSTRINGS_LANG":{"relativetime.days":["%d day ago","%d days ago"],"relativetime.duration.days":["%d day","%d days"],"relativetime.duration.hours":["%d hour","%d hours"],"relativetime.duration.mins":["%d minute","%d minutes"],"relativetime.duration.months":["%d month","%d months"],"relativetime.duration.secs":["%d second","%d seconds"],"relativetime.duration.weeks":["%d week","%d weeks"],"relativetime.duration.years":["%d year","%d years"],"relativetime.hours":["%d hour ago","%d hours ago"],"relativetime.mins":["%d minute ago","%d minutes ago"],"relativetime.months":["%d month ago","%d months ago"],"relativetime.weeks":["%d week ago","%d weeks ago"],"relativetime.years":["%d year ago","%d years ago"]},"PLURAL_RULE_FALLBACK":0,"PLURAL_RULE_LANG":0},
		notificationSettings: {"EventSourceUpdateTime":10000,"MaxTimeout":60000,"MinTimeout":10000,"TimeoutStep":10000}, 
		enableTimeTracking:  true ,
		
		mermaidMaxSourceCharacters:  50000 ,
		
		i18n: {
			copy_success: "Copied!",
			copy_error: "Copy failed",
			error_occurred: "An error occurred",
			network_error: "Network error",
			remove_label_str: "Remove item \"%s\"",
			modal_confirm: "Confirm",
			modal_cancel: "Cancel",
			more_items: "More items",
			incorrect_root_url: "This Forgejo instance is configured to be served on \"https://codeberg.org/\". You are currently viewing Forgejo through a different URL, which may cause parts of the application to break. The canonical URL is controlled by Forgejo admins via the ROOT_URL setting in the app.ini.",
		},
	};
	
	window.config.pageData = window.config.pageData || {};
</script>
<script src="/assets/js/webcomponents.js?v=17.0.0-99-322c239~gitea-1.22.0"></script>

	

	
	<meta property="og:title" content="forgejo">

	<meta property="og:description" content="Beyond coding. We forge.">


	<meta property="og:url" content="https://codeberg.org/forgejo/forgejo">


	<meta property="og:type" content="object">


	<meta property="og:image" content="https://codeberg.org/forgejo/forgejo/-/summary-card">
	
		<meta property="og:image:width" content="1200">
	
	
		<meta property="og:image:height" content="600">
	
	
		<meta property="og:image:alt" content="Summary card of repository forgejo/forgejo, described as: Beyond coding. We forge.">
	

<meta property="og:site_name" content="Codeberg.org">

	<link rel="stylesheet" href="/assets/css/index.css?v=17.0.0-99-322c239~gitea-1.22.0">
<link rel="stylesheet" href="/assets/css/theme-codeberg-auto.css?v=17.0.0-99-322c239~gitea-1.22.0">

	
</head>
<body class="no-js" hx-swap="outerHTML" hx-ext="morph" hx-push-url="false">
	
	<noscript>
		<style>
			#tou-announcement { display: flex !important; justify-content: center; }
			#tou-announcement > :first-child, #tou-announcement > :last-child { display: none; }
		</style>
	</noscript>
	<div id="tou-announcement" class="tw-hidden">
		<div style="width: 108.3px"></div>
		<div>
		<span>Codeberg has changed its Terms of Use. <a href="https://codeberg.org/Codeberg/org/compare/17bdb39b0c1ecd0e423f3ba592650ce57fcdfbf5..71149c7fc95ccfeae36109b5cddca339e4aa1473?files=TermsOfUse.md#diff-d760d688bb9b929b62db808bfc76abe4493d095a">View complete changes</a>.</span>
		<ol>
			<li>LLM-generated content is being restricted. <a href="https://codeberg.org/Codeberg/org/commit/71149c7fc95ccfeae36109b5cddca339e4aa1473">View change</a> or <a href="https://blog.codeberg.org/protecting-our-floss-commons-from-llms.html">read the blog post</a></li>
			<li>Cryptocurrency projects are no longer allowed. <a href="https://codeberg.org/Codeberg/org/commit/f383b648fd733ab88083dc390b91e77cd7589980">View change</a></li>
		</ol>
		</div>
		<button class="ui secondary button small"><svg viewBox="0 0 16 16" class="svg octicon-x" aria-hidden="true" width="16" height="16"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.75.75 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.75.75 0 0 1-.734-.215L8 9.06l-3.22 3.22a.75.75 0 0 1-1.042-.018.75.75 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06"/></svg> Dismiss</button>
	</div>
	<div class="full height">
		<noscript>
			<div class="tw-ml-2 tw-mr-2 tw-text-center tw-text-text-light-2">This website requires JavaScript.</div>
		</noscript>

		

		
			


<nav id="navbar" aria-label="Navigation bar">
	<div class="navbar-left ui secondary menu">
		
		<a class="item" id="navbar-logo" href="/" aria-label="Home">
			<div class="branding" aria-hidden="true">
				<img width="30" height="30" loading="lazy" class="light-logo" src="/assets/img/svg/cb-logo.svg" alt="Logo">
				<img width="30" height="30" loading="lazy" class="dark-logo" src="/assets/img/svg/cb-logo-mono.svg" alt="Logo">
			</div>
		</a>

		
		<div class="ui secondary menu item navbar-mobile-right only-mobile">
			
			<button class="item tw-w-auto ui icon mini button tw-p-2 tw-m-0" id="navbar-expand-toggle" aria-label="Toggle menu"><svg viewBox="0 0 16 16" class="svg octicon-three-bars" aria-hidden="true" width="16" height="16"><path d="M1 2.75A.75.75 0 0 1 1.75 2h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 2.75m0 5A.75.75 0 0 1 1.75 7h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 7.75M1.75 12h12.5a.75.75 0 0 1 0 1.5H1.75a.75.75 0 0 1 0-1.5"/></svg></button>
		</div>

		
		
			<a class="item" href="/explore/repos">Explore</a>
		

		
			<a class="item" target="_blank" href="https://docs.codeberg.org/getting-started/what-is-codeberg/#what-is-codeberg-e.v.%3F">About</a>
			<a class="item" target="_blank" href="https://docs.codeberg.org/getting-started/faq/">FAQ</a>
			<a class="item" target="_blank" rel="noopener noreferrer" href="https://docs.codeberg.org">Help</a>
		

		<a class="item donation-pretty" href="https://donate.codeberg.org">Donate</a>
	</div>

	
	<div class="navbar-right ui secondary menu">
		
		
			
				<a class="item" href="/user/sign_up">
					<svg viewBox="0 0 16 16" class="tw-mr-1 svg octicon-person" aria-hidden="true" width="16" height="16"><path d="M10.561 8.073a6 6 0 0 1 3.432 5.142.75.75 0 1 1-1.498.07 4.5 4.5 0 0 0-8.99 0 .75.75 0 0 1-1.498-.07 6 6 0 0 1 3.431-5.142 3.999 3.999 0 1 1 5.123 0M10.5 5a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0"/></svg>
					<span>Register</span>
				</a>
			
			<a class="item" rel="nofollow" href="/user/login?redirect_to=%2fforgejo%2fforgejo">
				<svg viewBox="0 0 16 16" class="tw-mr-1 svg octicon-sign-in" aria-hidden="true" width="16" height="16"><path d="M2 2.75C2 1.784 2.784 1 3.75 1h2.5a.75.75 0 0 1 0 1.5h-2.5a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h2.5a.75.75 0 0 1 0 1.5h-2.5A1.75 1.75 0 0 1 2 13.25Zm6.56 4.5h5.69a.75.75 0 0 1 0 1.5H8.56l1.97 1.97a.749.749 0 0 1-.326 1.275.75.75 0 0 1-.734-.215L6.22 8.53a.75.75 0 0 1 0-1.06l3.25-3.25a.749.749 0 0 1 1.275.326.75.75 0 0 1-.215.734Z"/></svg>
				<span>Sign in</span>
			</a>
		
	</div>
</nav>

		



<div role="main" aria-label="forgejo/forgejo: Beyond coding. We forge." class="page-content repository file list ">
	<div class="secondary-nav">

	<div class="ui container">
		<div class="repo-header">
			<div class="flex-item tw-items-center">
				<div class="flex-item-leading">
					

	<img class="ui avatar tw-align-middle" src="/repo-avatars/73144-c883a242dec5299fbc06bbe3ee71d8c6" width="24" height="24" alt="forgejo/forgejo">


				</div>
				<div class="flex-item-main">
					<div class="flex-item-title tw-font-normal">
						<a class="muted" href="/forgejo">forgejo</a>/<a class="muted tw-font-semibold" href="/forgejo/forgejo">forgejo</a>
					</div>
				</div>
				<div class="flex-item-trailing">
					
					
						
					
					
					
				</div>
			</div>
			
				<div class="repo-buttons button-row">
					
					
					
					
					<a class="ui compact small basic button" href="/forgejo/forgejo.rss" data-tooltip-content="RSS feed">
						<svg viewBox="0 0 16 16" class="svg octicon-rss" aria-hidden="true" width="16" height="16"><path d="M2.002 2.725a.75.75 0 0 1 .797-.699C8.79 2.42 13.58 7.21 13.974 13.201a.75.75 0 0 1-1.497.098 10.5 10.5 0 0 0-9.776-9.776.747.747 0 0 1-.7-.798ZM2.84 7.05h-.002a7 7 0 0 1 6.113 6.111.75.75 0 0 1-1.49.178 5.5 5.5 0 0 0-4.8-4.8.75.75 0 0 1 .179-1.489M2 13a1 1 0 1 1 2 0 1 1 0 0 1-2 0"/></svg>
					</a>
					
					
					
	
	<div class="ui disabled labeled button" data-tooltip-content="Sign in to watch this repository.">
		<div class="ui compact small basic button">
			<svg viewBox="0 0 16 16" class="svg octicon-eye" aria-hidden="true" width="16" height="16"><path d="M8 2c1.981 0 3.671.992 4.933 2.078 1.27 1.091 2.187 2.345 2.637 3.023a1.62 1.62 0 0 1 0 1.798c-.45.678-1.367 1.932-2.637 3.023C11.67 13.008 9.981 14 8 14s-3.671-.992-4.933-2.078C1.797 10.83.88 9.576.43 8.898a1.62 1.62 0 0 1 0-1.798c.45-.677 1.367-1.931 2.637-3.022C4.33 2.992 6.019 2 8 2M1.679 7.932a.12.12 0 0 0 0 .136c.411.622 1.241 1.75 2.366 2.717C5.176 11.758 6.527 12.5 8 12.5s2.825-.742 3.955-1.715c1.124-.967 1.954-2.096 2.366-2.717a.12.12 0 0 0 0-.136c-.412-.621-1.242-1.75-2.366-2.717C10.824 4.242 9.473 3.5 8 3.5s-2.825.742-3.955 1.715c-1.124.967-1.954 2.096-2.366 2.717M8 10a2 2 0 1 1-.001-3.999A2 2 0 0 1 8 10"/></svg><span class="text not-mobile">Watch</span>
		</div>
		<a class="ui basic label" href="/forgejo/forgejo/watchers"
			aria-label="381 watchers"
			>
			381
		</a>
	</div>


					
					<form hx-target="this" hx-post="/forgejo/forgejo/action/star" hx-on::after-settle="this.querySelector('button').focus()" method="post" action="/forgejo/forgejo/action/star">
	<div class="ui labeled button" data-tooltip-content="Sign in to star this repository.">
		<button type="submit" class="ui compact small basic button" disabled aria-label="Star">
			
				<svg viewBox="0 0 16 16" class="svg octicon-star" aria-hidden="true" width="16" height="16"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25m0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41z"/></svg><span class="text not-mobile">Star</span>
			
		</button>
		<a hx-boost="false" class="ui basic label" href="/forgejo/forgejo/stars"
			aria-label="5798 stars"
			>
			5.8k
		</a>
	</div>
</form>

					
					
					


	<div class="ui labeled button
		
			disabled
		"
		
			data-tooltip-content="Sign in to fork this repository."
		
	>
		<a class="ui compact small basic button"
			
				
			
		>
			<svg viewBox="0 0 16 16" class="svg octicon-repo-forked" aria-hidden="true" width="16" height="16"><path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0M5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0m6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5m-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0"/></svg><span class="text not-mobile">Fork</span>
		</a>
		<dialog id="fork-repo-modal">
			<article>
				<header>You've already forked forgejo</header>
				<div class="content tw-text-left">
					<div class="ui list">
						
					</div>
					
				</div>
			</article>
		</dialog>
		<a class="ui basic label" href="/forgejo/forgejo/forks"
			aria-label="1026 forks"
			>
			1.0k
		</a>
	</div>




					
					
				</div>
			
		</div>
		
		
		
	</div>

	<overflow-menu class="ui container secondary pointing tabular top attached borderless menu tw-pt-0 tw-my-0">
		
			<div class="overflow-menu-items">
				
					<a class="active item" href="/forgejo/forgejo">
						<svg viewBox="0 0 16 16" class="svg octicon-code" aria-hidden="true" width="16" height="16"><path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.75.75 0 0 1 .734.215m-6.56 0a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.75.75 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"/></svg> Code
					</a>
				

				
					<a class="item" href="/forgejo/forgejo/issues">
						<svg viewBox="0 0 16 16" class="svg octicon-issue-opened" aria-hidden="true" width="16" height="16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0"/></svg> Issues
						
							<span class="ui small label">1.6k</span>
						
					</a>
				

				

				
					<a class="item" href="/forgejo/forgejo/pulls">
						<svg viewBox="0 0 16 16" class="svg octicon-git-pull-request" aria-hidden="true" width="16" height="16"><path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25m5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354M3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5m0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5m8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0"/></svg> Pull requests
						
							<span class="ui small label">177</span>
						
					</a>
				

				
					<a href="/forgejo/forgejo/projects" class="item">
						<svg viewBox="0 0 16 16" class="svg octicon-project" aria-hidden="true" width="16" height="16"><path d="M1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0M1.5 1.75v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25M11.75 3a.75.75 0 0 1 .75.75v7.5a.75.75 0 0 1-1.5 0v-7.5a.75.75 0 0 1 .75-.75m-8.25.75a.75.75 0 0 1 1.5 0v5.5a.75.75 0 0 1-1.5 0ZM8 3a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 3"/></svg> Projects
						
					</a>
				

				
					<a class="item" href="/forgejo/forgejo/releases">
						<svg viewBox="0 0 16 16" class="svg octicon-tag" aria-hidden="true" width="16" height="16"><path d="M1 7.775V2.75C1 1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 0 1 0 2.474l-5.026 5.026a1.75 1.75 0 0 1-2.474 0l-6.25-6.25A1.75 1.75 0 0 1 1 7.775m1.5 0c0 .066.026.13.073.177l6.25 6.25a.25.25 0 0 0 .354 0l5.025-5.025a.25.25 0 0 0 0-.354l-6.25-6.25a.25.25 0 0 0-.177-.073H2.75a.25.25 0 0 0-.25.25ZM6 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/></svg> Releases
						
							<span class="ui small label">125</span>
						
					</a>
				

				
					<a href="/forgejo/forgejo/packages" class="item">
						<svg viewBox="0 0 16 16" class="svg octicon-package" aria-hidden="true" width="16" height="16"><path d="m8.878.392 5.25 3.045c.54.314.872.89.872 1.514v6.098a1.75 1.75 0 0 1-.872 1.514l-5.25 3.045a1.75 1.75 0 0 1-1.756 0l-5.25-3.045A1.75 1.75 0 0 1 1 11.049V4.951c0-.624.332-1.201.872-1.514L7.122.392a1.75 1.75 0 0 1 1.756 0M7.875 1.69l-4.63 2.685L8 7.133l4.755-2.758-4.63-2.685a.25.25 0 0 0-.25 0M2.5 5.677v5.372c0 .09.047.171.125.216l4.625 2.683V8.432Zm6.25 8.271 4.625-2.683a.25.25 0 0 0 .125-.216V5.677L8.75 8.432Z"/></svg> Packages
						
							<span class="ui small label">1</span>
						
					</a>
				

				

				

				
					<a class="item" href="/forgejo/forgejo/activity">
						<svg viewBox="0 0 16 16" class="svg octicon-pulse" aria-hidden="true" width="16" height="16"><path d="M6 2c.306 0 .582.187.696.471L10 10.731l1.304-3.26A.75.75 0 0 1 12 7h3.25a.75.75 0 0 1 0 1.5h-2.742l-1.812 4.528a.751.751 0 0 1-1.392 0L6 4.77 4.696 8.03A.75.75 0 0 1 4 8.5H.75a.75.75 0 0 1 0-1.5h2.742l1.812-4.529A.75.75 0 0 1 6 2"/></svg> Activity
					</a>
				

				
					<a class="item" href="/forgejo/forgejo/actions">
						<svg viewBox="0 0 16 16" class="svg octicon-play" aria-hidden="true" width="16" height="16"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215"/></svg> Actions
						
							<span class="ui small label">15</span>
						
					</a>
				

				

				

				
			</div>
		
	</overflow-menu>
	<div class="ui tabs divider"></div>
</div>



	<div class="ui container ">
		




	<div id="flash-message" hx-swap-oob="true"></div>


		
		<div class="repo-description">
			<div id="repo-desc" class="tw-break-anywhere tw-text-16">
				
				<span class="description">Beyond coding. We forge.</span>
				<a class="link" href="https://forgejo.org">https://forgejo.org</a>
			</div>
		</div>
		<div class="repo-topics tw-my-2" id="repo-topics">
			
			
				
				<a class="repo-topic ui large label" href="/explore/repos?q=forge&topic=1">forge</a>
				
			
				
				<a class="repo-topic ui large label" href="/explore/repos?q=forgejo&topic=1">forgejo</a>
				
			
				
				<a class="repo-topic ui large label" href="/explore/repos?q=git&topic=1">git</a>
				
			
				
				<a class="repo-topic ui large label" href="/explore/repos?q=self-hosted&topic=1">self-hosted</a>
				
			
			
		</div>
		
		

		
			
			
		
		








	
	



	
	



	
	



	
	





		
		
<div class="ui segments repository-summary tw-mt-1 tw-mb-0">
	<div class="ui segment repository-menu">
		
			<a class="item muted " href="/forgejo/forgejo/commits/branch/forgejo">
				<svg viewBox="0 0 16 16" class="svg octicon-history" aria-hidden="true" width="16" height="16"><path d="m.427 1.927 1.215 1.215a8.002 8.002 0 1 1-1.6 5.685.75.75 0 1 1 1.493-.154 6.5 6.5 0 1 0 1.18-4.458l1.358 1.358A.25.25 0 0 1 3.896 6H.25A.25.25 0 0 1 0 5.75V2.104a.25.25 0 0 1 .427-.177M7.75 4a.75.75 0 0 1 .75.75v2.992l2.028.812a.75.75 0 0 1-.557 1.392l-2.5-1A.75.75 0 0 1 7 8.25v-3.5A.75.75 0 0 1 7.75 4"/></svg> <b>26,112</b> commits
			</a>
			<a class="item muted " href="/forgejo/forgejo/branches">
				<svg viewBox="0 0 16 16" class="svg octicon-git-branch" aria-hidden="true" width="16" height="16"><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.5 2.5 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25m-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0m8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5M4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5"/></svg> <b>31</b> branches
			</a>
			
				<a class="item muted " href="/forgejo/forgejo/tags">
					<svg viewBox="0 0 16 16" class="svg octicon-tag" aria-hidden="true" width="16" height="16"><path d="M1 7.775V2.75C1 1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 0 1 0 2.474l-5.026 5.026a1.75 1.75 0 0 1-2.474 0l-6.25-6.25A1.75 1.75 0 0 1 1 7.775m1.5 0c0 .066.026.13.073.177l6.25 6.25a.25.25 0 0 0 .354 0l5.025-5.025a.25.25 0 0 0 0-.354l-6.25-6.25a.25.25 0 0 0-.177-.073H2.75a.25.25 0 0 0-.25.25ZM6 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/></svg> <b>309</b> tags
				</a>
			
			<span class="item" data-tooltip-content="git: 345 MiB, lfs: 0 B" data-test-name="repo-size">
				
				<svg viewBox="0 0 16 16" class="svg octicon-database" aria-hidden="true" width="16" height="16"><path d="M1 3.5c0-.626.292-1.165.7-1.59.406-.422.956-.767 1.579-1.041C4.525.32 6.195 0 8 0s3.475.32 4.722.869c.622.274 1.172.62 1.578 1.04.408.426.7.965.7 1.591v9c0 .626-.292 1.165-.7 1.59-.406.422-.956.767-1.579 1.041C11.476 15.68 9.806 16 8 16c-1.805 0-3.475-.32-4.721-.869-.623-.274-1.173-.62-1.579-1.04-.408-.426-.7-.965-.7-1.591Zm1.5 0c0 .133.058.318.282.551.227.237.591.483 1.101.707C4.898 5.205 6.353 5.5 8 5.5s3.101-.295 4.118-.742c.508-.224.873-.471 1.1-.708.224-.232.282-.417.282-.55s-.058-.318-.282-.551c-.227-.237-.591-.483-1.101-.707C11.102 1.795 9.647 1.5 8 1.5s-3.101.295-4.118.742c-.508.224-.873.471-1.1.708-.224.232-.282.417-.282.55m0 4.5c0 .133.058.318.282.551.227.237.591.483 1.101.707C4.898 9.705 6.353 10 8 10s3.101-.295 4.118-.742c.508-.224.873-.471 1.1-.708.224-.232.282-.417.282-.55V5.724c-.241.15-.503.286-.778.407C11.475 6.68 9.805 7 8 7s-3.475-.32-4.721-.869a6 6 0 0 1-.779-.407Zm0 2.225V12.5c0 .133.058.318.282.55.227.237.592.484 1.1.708 1.016.447 2.471.742 4.118.742s3.102-.295 4.117-.742c.51-.224.874-.47 1.101-.707.224-.233.282-.418.282-.551v-2.275c-.241.15-.503.285-.778.406-1.247.549-2.917.869-4.722.869s-3.475-.32-4.721-.869a6 6 0 0 1-.779-.406"/></svg> <b>345</b> MiB
			</span>
		
	</div>
	
		<details class="stats" id="language-stats">
			<summary>
				<stats-bar>
					
						<div class="slice" style="width: 81.6%; background-color: #00ADD8" data-tooltip-placement="top" data-tooltip-content=Go data-tooltip-follow-cursor="horizontal"></div>
					
						<div class="slice" style="width: 10.4%; background-color: #cccccc" data-tooltip-placement="top" data-tooltip-content=go-html-template data-tooltip-follow-cursor="horizontal"></div>
					
						<div class="slice" style="width: 2.8%; background-color: #3178c6" data-tooltip-placement="top" data-tooltip-content=TypeScript data-tooltip-follow-cursor="horizontal"></div>
					
						<div class="slice" style="width: 2%; background-color: #f1e05a" data-tooltip-placement="top" data-tooltip-content=JavaScript data-tooltip-follow-cursor="horizontal"></div>
					
						<div class="slice" style="width: 1.8%; background-color: #663399" data-tooltip-placement="top" data-tooltip-content=CSS data-tooltip-follow-cursor="horizontal"></div>
					
						<div class="slice" style="width: 1.3%; background-color: #cccccc" data-tooltip-placement="top" data-tooltip-content=other data-tooltip-follow-cursor="horizontal"></div>
					
				</stats-bar>
			</summary>
			<ul>
				
					<li>
						<i class="color-icon" style="background-color: #00ADD8"></i>
						<span>
							
								Go
							
						</span>
						81.6%
					</li>
				
					<li>
						<i class="color-icon" style="background-color: #cccccc"></i>
						<span>
							
								go-html-template
							
						</span>
						10.4%
					</li>
				
					<li>
						<i class="color-icon" style="background-color: #3178c6"></i>
						<span>
							
								TypeScript
							
						</span>
						2.8%
					</li>
				
					<li>
						<i class="color-icon" style="background-color: #f1e05a"></i>
						<span>
							
								JavaScript
							
						</span>
						2%
					</li>
				
					<li>
						<i class="color-icon" style="background-color: #663399"></i>
						<span>
							
								CSS
							
						</span>
						1.8%
					</li>
				
					<li>
						<i class="color-icon" style="background-color: #cccccc"></i>
						<span>
							
								Other
							
						</span>
						1.3%
					</li>
				
			</ul>
		</details>
	
</div>


		
		
		
		<div class="repo-button-row">
			<div class="button-sequence tw-gap-y-2">
				






	




<script type="module">
	const data = {
		'textReleaseCompare': "Compare",
		'textCreateTag': "Create tag %s",
		'textCreateBranch': "Create branch %s",
		'textCreateBranchFrom': "from \"%s\"",
		'textBranches': "Branches",
		'textTags': "Tags",
		'textDefaultBranchLabel': "default",

		'mode': 'branches',
		'showBranchesInDropdown':  true ,
		'searchFieldPlaceholder': 'Filter branch or tag...',
		'branchForm':  null ,
		'disableCreateBranch':  true ,
		'setAction':  null ,
		'submitForm':  null ,
		'viewType': "branch",
		'refName': "forgejo",
		'commitIdShort': "e2bd913f63",
		'tagName': "",
		'branchName': "forgejo",
		'noTag':  null ,
		'defaultSelectedRefName': "forgejo",
		'repoDefaultBranch': "forgejo",
		'enableFeed':  true ,
		'rssURLPrefix': '\/forgejo\/forgejo/rss/branch/',
		'branchURLPrefix': '\/forgejo\/forgejo/src/branch/',
		'branchURLSuffix': '',
		'tagURLPrefix': '\/forgejo\/forgejo/src/tag/',
		'tagURLSuffix': '',
		'repoLink': "/forgejo/forgejo",
		'treePath': "",
		'branchNameSubURL': "branch/forgejo",
		'noResults': "No results found.",
	};
	
	window.config.pageData.branchDropdownDataList = window.config.pageData.branchDropdownDataList || [];
	window.config.pageData.branchDropdownDataList.push(data);
</script>

<div class="js-branch-tag-selector ">
	
	<div class="ui dropdown custom">
		<button class="branch-dropdown-button gt-ellipsis ui basic small compact button tw-flex tw-m-0">
			<span class="text tw-flex tw-items-center tw-mr-1 gt-ellipsis">
				
					
						<svg viewBox="0 0 16 16" class="svg octicon-git-branch" aria-hidden="true" width="16" height="16"><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.5 2.5 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25m-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0m8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5M4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5"/></svg>
					
					<strong ref="dropdownRefName" class="tw-ml-2 tw-inline-block gt-ellipsis">forgejo</strong>
				
			</span>
			<svg viewBox="0 0 16 16" class="dropdown icon svg octicon-triangle-down" aria-hidden="true" width="14" height="14"><path d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427"/></svg>
		</button>
	</div>
</div>

				
					
					
					
					
					<a id="new-pull-request" class="ui compact basic button" href="/forgejo/forgejo/compare/forgejo...forgejo"
						data-tooltip-content="Compare">
						<svg viewBox="0 0 16 16" class="svg octicon-git-pull-request" aria-hidden="true" width="16" height="16"><path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25m5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354M3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5m0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5m8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0"/></svg>
					</a>
				
				
				
					<a href="/forgejo/forgejo/find/branch/forgejo" class="ui compact basic button">Find a file</a>
				

				

				
				




			</div>
			<div class="tw-flex tw-items-center max-[390px]:tw-w-full">
				
				
					<div class="clone-panel ui action tiny input max-[390px]:tw-w-full">
						

	<button class="ui small button" id="repo-clone-https" data-link="https://codeberg.org/forgejo/forgejo.git">
		HTTPS
	</button>


<input id="repo-clone-url" size="20" class="js-clone-url" value="https://codeberg.org/forgejo/forgejo.git" readonly>
<button class="ui small icon button" id="clipboard-btn" data-tooltip-content="Copy URL" data-clipboard-target="#repo-clone-url" aria-label="Copy URL">
	<svg viewBox="0 0 16 16" class="svg octicon-copy" aria-hidden="true" width="14" height="14"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"/><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg>
</button>

						<button class="ui small jump dropdown icon button" data-tooltip-content="More operations">
							<svg viewBox="0 0 16 16" class="svg octicon-kebab-horizontal" aria-hidden="true" width="16" height="16"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3M1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3m13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/></svg>
							<div class="menu">
								
									<a class="item archive-link" href="/forgejo/forgejo/archive/forgejo.zip" rel="nofollow"><svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-zip" aria-hidden="true" width="16" height="16"><path d="M3.5 1.75v11.5c0 .09.048.173.126.217a.75.75 0 0 1-.752 1.298A1.75 1.75 0 0 1 2 13.25V1.75C2 .784 2.784 0 3.75 0h5.586c.464 0 .909.185 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v8.586A1.75 1.75 0 0 1 12.25 15h-.5a.75.75 0 0 1 0-1.5h.5a.25.25 0 0 0 .25-.25V4.664a.25.25 0 0 0-.073-.177L9.513 1.573a.25.25 0 0 0-.177-.073H7.25a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5h-3a.25.25 0 0 0-.25.25m3.75 8.75h.5c.966 0 1.75.784 1.75 1.75v3a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1-.75-.75v-3c0-.966.784-1.75 1.75-1.75M6 5.25a.75.75 0 0 1 .75-.75h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 6 5.25m.75 2.25h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5M8 6.75A.75.75 0 0 1 8.75 6h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 8 6.75M8.75 3h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5M8 9.75A.75.75 0 0 1 8.75 9h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 8 9.75m-1 2.5v2.25h1v-2.25a.25.25 0 0 0-.25-.25h-.5a.25.25 0 0 0-.25.25"/></svg>Download ZIP</a>
									<a class="item archive-link" href="/forgejo/forgejo/archive/forgejo.tar.gz" rel="nofollow"><svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-zip" aria-hidden="true" width="16" height="16"><path d="M3.5 1.75v11.5c0 .09.048.173.126.217a.75.75 0 0 1-.752 1.298A1.75 1.75 0 0 1 2 13.25V1.75C2 .784 2.784 0 3.75 0h5.586c.464 0 .909.185 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v8.586A1.75 1.75 0 0 1 12.25 15h-.5a.75.75 0 0 1 0-1.5h.5a.25.25 0 0 0 .25-.25V4.664a.25.25 0 0 0-.073-.177L9.513 1.573a.25.25 0 0 0-.177-.073H7.25a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5h-3a.25.25 0 0 0-.25.25m3.75 8.75h.5c.966 0 1.75.784 1.75 1.75v3a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1-.75-.75v-3c0-.966.784-1.75 1.75-1.75M6 5.25a.75.75 0 0 1 .75-.75h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 6 5.25m.75 2.25h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5M8 6.75A.75.75 0 0 1 8.75 6h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 8 6.75M8.75 3h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5M8 9.75A.75.75 0 0 1 8.75 9h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 8 9.75m-1 2.5v2.25h1v-2.25a.25.25 0 0 0-.25-.25h-.5a.25.25 0 0 0-.25.25"/></svg>Download TAR.GZ</a>
									<a class="item archive-link" href="/forgejo/forgejo/archive/forgejo.bundle" rel="nofollow"><svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-package" aria-hidden="true" width="16" height="16"><path d="m8.878.392 5.25 3.045c.54.314.872.89.872 1.514v6.098a1.75 1.75 0 0 1-.872 1.514l-5.25 3.045a1.75 1.75 0 0 1-1.756 0l-5.25-3.045A1.75 1.75 0 0 1 1 11.049V4.951c0-.624.332-1.201.872-1.514L7.122.392a1.75 1.75 0 0 1 1.756 0M7.875 1.69l-4.63 2.685L8 7.133l4.755-2.758-4.63-2.685a.25.25 0 0 0-.25 0M2.5 5.677v5.372c0 .09.047.171.125.216l4.625 2.683V8.432Zm6.25 8.271 4.625-2.683a.25.25 0 0 0 .125-.216V5.677L8.75 8.432Z"/></svg>Download BUNDLE</a>
								
								
								
									<a class="item js-clone-url-editor" data-href-template="vscode://vscode.git/clone?url={url}"><svg viewBox="-1 -1 34 34" class="tw-mr-2 svg gitea-open-with-vscode" aria-hidden="true" width="16" height="16"><path d="M30.9 3.4 24.3.3a2 2 0 0 0-2.3.4L9.4 12.2 3.9 8c-.5-.4-1.2-.4-1.7 0L.4 9.8c-.5.5-.5 1.4 0 2L5.2 16 .4 20.3c-.5.6-.5 1.5 0 2L2.2 24c.5.5 1.2.5 1.7 0l5.5-4L22 31.2a2 2 0 0 0 2.3.4l6.6-3.2a2 2 0 0 0 1.1-1.8V5.2a2 2 0 0 0-1.1-1.8M24 23.3 14.4 16 24 8.7z"/></svg>Open with VS Code</a>
								
									<a class="item js-clone-url-editor" data-href-template="vscodium://vscode.git/clone?url={url}"><svg xml:space="preserve" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" clip-rule="evenodd" viewBox="0 0 16 16" class="tw-mr-2 svg gitea-open-with-vscodium" aria-hidden="true" width="16" height="16"><path fill-rule="nonzero" d="m10.2.2.5-.3c.3 0 .5.2.7.4l.2.8-.2 1-.8 2.4c-.3 1-.4 2 0 2.9l.8-2c.2 0 .4.1.4.3l-.3 1L9.2 13l3.1-2.9c.3-.2.7-.5.8-1a2 2 0 0 0-.3-1c-.2-.5-.5-.9-.6-1.4l.1-.7c.1-.1.3-.2.5-.1.2 0 .3.2.4.4.3.5.4 1.2.5 1.8l.6-1.2c0-.2.2-.4.4-.6l.4-.2c.2 0 .4.3.4.4v.6l-.8 1.6-1.4 1.8 1-.4c.2 0 .6.2.7.5 0 .2 0 .4-.2.5-.3.2-.6.2-1 .2-1 0-2.2.6-2.9 1.4L9.6 15c-.4.4-.9 1-1.4.8-.8-.1-.8-1.3-1-1.8 0-.3-.2-.6-.4-.7-.3-.2-.5-.3-.8-.3-.6-.1-1.2 0-1.8-.2l-.8-.4-.4-.7c-.3-.6-.3-1.2-.5-1.8A4 4 0 0 0 1 8l-.4-.4v-.4c.2-.2.5-.2.7 0 .5.2.5.8 1 1.1V6.2s.3-.1.4 0l.2.5L3 9c.4-.4.6-1 .5-1.5L3.4 7l.3-.2c.2 0 .3.2.4.3v.7c0 .6-.3 1.1-.4 1.7-.2.4-.3 1-.1 1.4.1.5.5.9.9 1 .5.3 1.1.4 1.7.4-.4-.6-.7-1.2-.7-2 0-.7.4-1.3.6-2C6.3 7 5.7 5.8 4.8 5l-1.5-.7c-.4-.2-.7-.7-.7-1.2.3-.1.7 0 1 .1L5 4.5l.6.1c.2-.3 0-.6-.2-.8-.3-.5-1-.6-1.3-1a.9.9 0 0 1-.2-.8c0-.2.3-.4.5-.4.4 0 .7.3.9.5.8.8 1.2 1.8 1.4 3s0 2.5-.2 3.7c0 .3-.2.5-.1.8l.2.2c.2 0 .4 0 .5-.2.4-.3.8-.8.9-1.3l.1-1.2.1-.6.4-.2.3.3v.6c-.1.5-.2 1-.5 1.6a2 2 0 0 1-.6 1l-1 1c-.1.2-.2.6-.1.9 0 .2.2.4.4.5.4.2.8.2 1 0 .3-.1.5-.4.7-.6l.5-1.4.4-2.5C9.7 7 9.6 6 9 5.2c-.2-.4-.5-.7-1-1l-1-.8c-.2-.3-.4-.7-.3-1.2h.6c.4.1.7.4.9.8s.4.8.9 1l-1-2c-.1-.3-.3-.5-.2-.8 0-.2.2-.4.4-.4s.4.1.5.3l.2.5 1 3.1a4 4 0 0 0 .4-2.3L10 1V.2Z"/></svg>Open with VSCodium</a>
								
									<a class="item js-clone-url-editor" data-href-template="jetbrains://idea/checkout/git?idea.required.plugins.id=Git4Idea&amp;checkout.repo={url}"><svg xml:space="preserve" viewBox="0 0 70 70" class="tw-mr-2 svg gitea-open-with-jetbrains" aria-hidden="true" width="16" height="16"><linearGradient id="gitea-open-with-jetbrains__a" x1=".79" x2="33.317" y1="40.089" y2="40.089" gradientUnits="userSpaceOnUse"><stop offset=".258" style="stop-color:#f97a12"/><stop offset=".459" style="stop-color:#b07b58"/><stop offset=".724" style="stop-color:#577bae"/><stop offset=".91" style="stop-color:#1e7ce5"/><stop offset="1" style="stop-color:#087cfa"/></linearGradient><path d="M17.7 54.6.8 41.2l8.4-15.6L33.3 35z" style="fill:url(#gitea-open-with-jetbrains__a)"/><linearGradient id="gitea-open-with-jetbrains__b" x1="25.767" x2="79.424" y1="24.88" y2="54.57" gradientUnits="userSpaceOnUse"><stop offset="0" style="stop-color:#f97a12"/><stop offset=".072" style="stop-color:#cb7a3e"/><stop offset=".154" style="stop-color:#9e7b6a"/><stop offset=".242" style="stop-color:#757b91"/><stop offset=".334" style="stop-color:#537bb1"/><stop offset=".432" style="stop-color:#387ccc"/><stop offset=".538" style="stop-color:#237ce0"/><stop offset=".655" style="stop-color:#147cef"/><stop offset=".792" style="stop-color:#0b7cf7"/><stop offset="1" style="stop-color:#087cfa"/></linearGradient><path d="m70 18.7-1.3 40.5L41.8 70 25.6 59.6 49.3 35 38.9 12.3l9.3-11.2z" style="fill:url(#gitea-open-with-jetbrains__b)"/><linearGradient id="gitea-open-with-jetbrains__c" x1="63.228" x2="48.29" y1="42.915" y2="-1.719" gradientUnits="userSpaceOnUse"><stop offset="0" style="stop-color:#fe315d"/><stop offset=".078" style="stop-color:#cb417e"/><stop offset=".16" style="stop-color:#9e4e9b"/><stop offset=".247" style="stop-color:#755bb4"/><stop offset=".339" style="stop-color:#5365ca"/><stop offset=".436" style="stop-color:#386ddb"/><stop offset=".541" style="stop-color:#2374e9"/><stop offset=".658" style="stop-color:#1478f3"/><stop offset=".794" style="stop-color:#0b7bf8"/><stop offset="1" style="stop-color:#087cfa"/></linearGradient><path d="M70 18.7 48.7 43.9l-9.8-31.6 9.3-11.2z" style="fill:url(#gitea-open-with-jetbrains__c)"/><linearGradient id="gitea-open-with-jetbrains__d" x1="10.72" x2="55.524" y1="16.473" y2="90.58" gradientUnits="userSpaceOnUse"><stop offset="0" style="stop-color:#fe315d"/><stop offset=".04" style="stop-color:#f63462"/><stop offset=".104" style="stop-color:#df3a71"/><stop offset=".167" style="stop-color:#c24383"/><stop offset=".291" style="stop-color:#ad4a91"/><stop offset=".55" style="stop-color:#755bb4"/><stop offset=".917" style="stop-color:#1d76ed"/><stop offset="1" style="stop-color:#087cfa"/></linearGradient><path d="M33.7 58.1 5.6 68.3l4.5-15.8L16 33.1 0 27.7 10.1 0l22 2.7 21.6 24.7z" style="fill:url(#gitea-open-with-jetbrains__d)"/><path d="M13.7 13.5h43.2v43.2H13.7z" style="fill:#000"/><path d="M17.7 48.6h16.2v2.7H17.7zM29.4 22.4v-3.3h-9v3.3H23v11.3h-2.6V37h9v-3.3h-2.5V22.4zM38 37.3c-1.4 0-2.6-.3-3.5-.8s-1.7-1.2-2.3-1.9l2.5-2.8c.5.6 1 1 1.5 1.3s1.1.5 1.7.5c.7 0 1.3-.2 1.8-.7.4-.5.6-1.2.6-2.3V19.1h4v11.7c0 1.1-.1 2-.4 2.8s-.7 1.4-1.3 2c-.5.5-1.2 1-2 1.2-.8.3-1.6.5-2.6.5" style="fill:#fff"/></svg>Open with Intellij IDEA</a>
								
							</div>
						</button>
						<script>
	
	
	
	
	
	
	(window.updateCloneStates = function() {
		const httpsBtn = document.getElementById('repo-clone-https');
		const sshBtn = document.getElementById('repo-clone-ssh');
		const value = localStorage.getItem('repo-clone-protocol') || 'https';
		const isSSH = value === 'ssh' && sshBtn || value !== 'ssh' && !httpsBtn;

		if (httpsBtn) {
			httpsBtn.textContent = window.origin.split(':')[0].toUpperCase();
			httpsBtn.classList.toggle('primary', !isSSH);
			httpsBtn.classList.toggle('basic', isSSH);
		}
		if (sshBtn) {
			sshBtn.classList.toggle('primary', isSSH);
			sshBtn.classList.toggle('basic', !isSSH);
		}

		const btn = isSSH ? sshBtn : httpsBtn;
		if (!btn) return;

		
		function toOriginUrl(urlStr) {
			try {
				if (urlStr.startsWith('http://') || urlStr.startsWith('https://') || urlStr.startsWith('/')) {
					const {origin, protocol, hostname, port} = window.location;
					const url = new URL(urlStr, origin);
					url.protocol = protocol;
					url.hostname = hostname;
					url.port = port || (protocol === 'https:' ? '443' : '80');
					return url.toString();
				}
			} catch {}
			return urlStr;
		}
		const link = toOriginUrl(btn.getAttribute('data-link'));

		for (const el of document.getElementsByClassName('js-clone-url')) {
			el[el.nodeName === 'INPUT' ? 'value' : 'textContent'] = link;
		}
		for (const el of document.getElementsByClassName('js-clone-url-editor')) {
			el.href = el.getAttribute('data-href-template').replace('{url}', encodeURIComponent(link));
		}
	})();
</script>

					</div>
				
				
			</div>
		</div>

		
			

			

		

		
			
			
			
			
			
			<table id="repo-files-table" class="ui single line table tw-mt-0" >
	<caption class="tw-sr-only">
		Repository files (latest commit first)
	</caption>
	<thead class="tw-sr-only">
		<th>Filename</th>
		<th>Latest commit message</th>
		<th>Latest commit date</th>
	</thead>
	<tbody>
		<tr class="commit-list">
			<td class="tw-overflow-hidden repo-files-table-latest-commit-cell repo-files-table-latest-commit-left" colspan="2">
				<div class="tw-flex">
					<div class="latest-commit">
						
	
		<img loading="lazy" alt="" class="ui avatar tw-align-middle tw-mr-2" src="/avatars/561ee781e72bbbfd2865db7b4ba4fbf50f64da3d3cb0f4e1897b6da25224a2a7?size=64" title="Mathieu Fenniak" width="24" height="24"/>
		
			<a class="muted author-wrapper" title="Mathieu Fenniak" href="/mfenniak"><strong>Mathieu Fenniak</strong></a>
		
	
	

<a href="/forgejo/forgejo/commit/e2bd913f63a93ce0b20bfd311908219cc91c2654" rel="nofollow" class="sha label">
	<span class="shortsha">e2bd913f63</span></a>

	
	
		<span class="tw-align-middle " data-tippy="commit-statuses" tabindex="0">
			





	<svg viewBox="0 0 16 16" class="commit-status icon text red svg octicon-x" aria-hidden="true" width="18" height="18"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.75.75 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.75.75 0 0 1-.734-.215L8 9.06l-3.22 3.22a.75.75 0 0 1-1.042-.018.75.75 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06"/></svg>



		</span>
	
	<div class="tippy-target">
		


<div class="commit-status-panel">
	<div class="ui top attached header commit-status-header">
		
			Some checks failed
		

		
	</div>

	<div class="commit-status-list">
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">/ build (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214818/jobs/0">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">/ e2e (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214818/jobs/1">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">/ release (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214818/jobs/2">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">testing-integration / test-unit (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214819/jobs/0">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">testing-integration / test-sqlite (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214819/jobs/1">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">testing-integration / test-mariadb (v10.6) (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214819/jobs/2">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">testing-integration / test-mariadb (v11.8) (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214819/jobs/3">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / semgrep/ci (push) <span class="text light-2">Successful in 27s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/12">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / frontend-checks (push) <span class="text light-2">Successful in 1m6s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/1">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / backend-checks (push) <span class="text light-2">Successful in 3m11s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/0">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / test-unit (push) <span class="text light-2">Successful in 5m20s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/2">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / test-remote-cacher (garnet) (push) <span class="text light-2">Successful in 2m3s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/6">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / test-remote-cacher (valkey) (push) <span class="text light-2">Successful in 2m4s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/5">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / test-remote-cacher (redis) (push) <span class="text light-2">Successful in 2m6s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/4">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / test-e2e (push) <span class="text light-2">Successful in 35m8s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/3">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / test-sqlite (push) <span class="text light-2">Successful in 46m57s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/9">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / test-mysql (push) <span class="text light-2">Successful in 50m17s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/7">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				


	<svg viewBox="0 0 16 16" class="commit-status icon text green svg octicon-check" aria-hidden="true" width="18" height="18"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 .018-1.042.75.75 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0"/></svg>






				<div class="status-context gt-ellipsis">testing / coverage (push) <span class="text light-2">Successful in 1m47s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/10">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				





	<svg viewBox="0 0 16 16" class="commit-status icon text red svg octicon-x" aria-hidden="true" width="18" height="18"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.75.75 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.75.75 0 0 1-.734-.215L8 9.06l-3.22 3.22a.75.75 0 0 1-1.042-.018.75.75 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06"/></svg>



				<div class="status-context gt-ellipsis">testing / test-pgsql (push) <span class="text light-2">Failing after 1h22m7s</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/8">Details</a></span>
				</div>
			</div>
		
			<div class="commit-status-item">
				



	<svg viewBox="0 0 16 16" class="commit-status icon text grey svg octicon-skip" aria-hidden="true" width="18" height="18"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0m9.78-2.22-5.5 5.5a.749.749 0 0 1-1.275-.326.75.75 0 0 1 .215-.734l5.5-5.5a.75.75 0 0 1 1.042.018.75.75 0 0 1 .018 1.042"/></svg>





				<div class="status-context gt-ellipsis">testing / security-check (push) <span class="text light-2">Has been skipped</span></div>
				<div class="ui status-details">
					
					<span><a href="/forgejo/forgejo/actions/runs/214821/jobs/11">Details</a></span>
				</div>
			</div>
		
		
	</div>
</div>


	</div>


	
	<span class="grey commit-summary" title="perf: do not terminate CatFileBatch[Check] subprocess on git.ErrNotExist errors (#15167)"><span class="message-wrapper"><a href="/forgejo/forgejo/commit/e2bd913f63a93ce0b20bfd311908219cc91c2654" class="default-link muted">perf: do not terminate CatFileBatch[Check] subprocess on git.ErrNotExist errors (</a><a href="/forgejo/forgejo/issues/15167" class="ref-issue">#15167</a><a href="/forgejo/forgejo/commit/e2bd913f63a93ce0b20bfd311908219cc91c2654" class="default-link muted">)</a></span>
		
			<button class="ui button js-toggle-commit-body ellipsis-button" aria-expanded="false">...</button>
			<pre class="commit-body tw-hidden">Omits `git.ErrNotExist` from the errors that close the subprocesses, allowing them to be reused after checking that a commit doesn&#39;t exist.

Reviewed-on: <a href="https://codeberg.org/forgejo/forgejo/pulls/15167" class="ref-issue">#15167</a>
Reviewed-by: Andreas Ahlenstorf &lt;[email withheld by Lighthouse]&gt;</pre>
		
	</span>


					</div>
				</div>
			</td>
			<td class="text grey right age repo-files-table-latest-commit-cell tw-py-0"><relative-time prefix="" tense="past" datetime="2026-11-08T14:12:02+01:00" data-tooltip-content data-tooltip-interactive="true">2026-11-08 14:12:02 +01:00</relative-time></td>
		</tr>
		
		
			
			
			<tr data-entryname=".devcontainer" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/.devcontainer" title=".devcontainer">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg>.devcontainer
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/cb7b3bacd473302856f44db440f334e5bc4ff3c2" class="default-link muted">Update golang packages to v1.27 (forgejo) (</a><a href="/forgejo/forgejo/issues/14457" class="ref-issue">#14457</a><a href="/forgejo/forgejo/commit/cb7b3bacd473302856f44db440f334e5bc4ff3c2" class="default-link muted">)</a>
						
					</span>
				</td>
				<td class="text right age three wide"><relative-time prefix="" tense="past" datetime="2026-09-27T19:10:21+02:00" data-tooltip-content data-tooltip-interactive="true">2026-09-27 19:10:21 +02:00</relative-time></td>
			</tr>
		
			
			
			<tr data-entryname=".forgejo" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/.forgejo" title=".forgejo">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg>.forgejo
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/32a1363f7989799b412636297a89f843c08c6c6c" class="default-link muted">ci: change auto-labeling for run-end-to-end-tests into a warning comment (</a><a href="/forgejo/forgejo/issues/15139" class="ref-issue">#15139</a><a href="/forgejo/forgejo/commit/32a1363f7989799b412636297a89f843c08c6c6c" class="default-link muted">)</a>
						
					</span>
				</td>
				<td class="text right age three wide"><relative-time prefix="" tense="past" datetime="2026-11-05T19:52:15+01:00" data-tooltip-content data-tooltip-interactive="true">2026-11-05 19:52:15 +01:00</relative-time></td>
			</tr>
		
			
			
			<tr data-entryname=".semgrep" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/.semgrep" title=".semgrep">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg>.semgrep
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/10132ea16bb846dd71d703655cb67b318680ea0a" class="default-link muted">fix(ci): semgrep duplicate id (</a><a href="/forgejo/forgejo/issues/14085" class="ref-issue">#14085</a><a href="/forgejo/forgejo/commit/10132ea16bb846dd71d703655cb67b318680ea0a" class="default-link muted">)</a>
						
					</span>
				</td>
				<td class="text right age three wide"><relative-time prefix="" tense="past" datetime="2026-08-26T02:20:15+02:00" data-tooltip-content data-tooltip-interactive="true">2026-08-26 02:20:15 +02:00</relative-time></td>
			</tr>
		
			
			
			<tr data-entryname="assets" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/assets" title="assets">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg>assets
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/4d27873247907dcb5eb95f25dc4718a03ff2dad2" class="default-link muted">Update github.com/sourcegraph/zoekt digest to c4d8f35 (forgejo) (</a><a href="/forgejo/forgejo/issues/13831" class="ref-issue">#13831</a><a href="/forgejo/forgejo/commit/4d27873247907dcb5eb95f25dc4718a03ff2dad2" class="default-link muted">)</a>
						
					</span>
				</td>
				<td class="text right age three wide"><relative-time prefix="" tense="past" datetime="2026-11-06T18:17:15+01:00" data-tooltip-content data-tooltip-interactive="true">2026-11-06 18:17:15 +01:00</relative-time></td>
			</tr>
		
			
			
			<tr data-entryname="build" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/build" title="build">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg>build
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/8a8215bcea089f8bab81c817706159a19914073b" class="default-link muted">feat: improve space-efficiency of emoji data (</a><a href="/forgejo/forgejo/issues/14413" class="ref-issue">#14413</a><a href="/forgejo/forgejo/commit/8a8215bcea089f8bab81c817706159a19914073b" class="default-link muted">)</a>
						
					</span>
				</td>
				<td class="text right age three wide"><relative-time prefix="" tense="past" datetime="2026-09-19T09:54:48+02:00" data-tooltip-content data-tooltip-interactive="true">2026-09-19 09:54:48 +02:00</relative-time></td>
			</tr>
		
			
			
			<tr data-entryname="cmd" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/cmd" title="cmd">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg>cmd
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/d191d25cb3b5082607780bdff89fc2353a92161b" class="default-link muted">feat: show git config after AGit pull request creation (</a><a href="/forgejo/forgejo/issues/14497" class="ref-issue">#14497</a><a href="/forgejo/forgejo/commit/d191d25cb3b5082607780bdff89fc2353a92161b" class="default-link muted">)</a>
						
					</span>
				</td>
				<td class="text right age three wide"><relative-time prefix="" tense="past" datetime="2026-11-07T16:55:41+01:00" data-tooltip-content data-tooltip-interactive="true">2026-11-07 16:55:41 +01:00</relative-time></td>
			</tr>
		
			
			
			<tr data-entryname="contrib" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/contrib" title="contrib">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg>contrib
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/cda3aca4c92e775ccfeec66648a061e05f823b54" class="default-link muted">feat: always use UNIX sockets for internal communication (</a><a href="/forgejo/forgejo/issues/14148" class="ref-issue">#14148</a><a href="/forgejo/forgejo/commit/cda3aca4c92e775ccfeec66648a061e05f823b54" class="default-link muted">)</a>
						
					</span>
				</td>
				<td class="text right age three wide"><relative-time prefix="" tense="past" datetime="2026-10-02T22:42:18+02:00" data-tooltip-content data-tooltip-interactive="true">2026-10-02 22:42:18 +02:00</relative-time></td>
			</tr>
		
			
			
			<tr data-entryname="custom" data-ready="true" class="ready entry">
				<td class="name four wide">
					<span class="truncate">
						
							
								
								<a class="muted" href="/forgejo/forgejo/src/branch/forgejo/custom/conf" title="custom/conf">
									
									
									<svg viewBox="0 0 16 16" class="tw-mr-2 svg octicon-file-directory-fill" aria-hidden="true" width="16" height="16"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1z"/></svg><span class="text light-2">custom</span>/conf
									
								</a>
							
						
					</span>
				</td>
				<td class="message nine wide">
					<span class="truncate">
						
							
							<a href="/forgejo/forgejo/commit/e71c83d74dda1668e0aebad48fc442c2691dd53f" class="default-link muted">Add special webhook type for integration with git-pages (</a><a href="/forgejo/forgejo/issues/14966" class="ref-issue">#14966</a><a href="/forgej