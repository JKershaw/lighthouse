<!DOCTYPE html>
<html class="client-nojs vector-feature-language-in-header-enabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-0 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-os vector-sticky-header-enabled vector-toc-available skin-theme-clientpref-thumb-standard" lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<title>pacman - ArchWiki</title>
<script>(function(){var className="client-js vector-feature-language-in-header-enabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-0 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-os vector-sticky-header-enabled vector-toc-available skin-theme-clientpref-thumb-standard";var cookie=document.cookie.match(/(?:^|; )archwikimwclientpreferences=([^;]+)/);if(cookie){cookie[1].split('%2C').forEach(function(pref){className=className.replace(new RegExp('(^| )'+pref.replace(/-clientpref-\w+$|[^\w-]+/g,'')+'-clientpref-\\w+( |$)'),'$1'+pref+'$2');});}document.documentElement.className=className;}());RLCONF={"wgBreakFrames":false,"wgSeparatorTransformTable":["",""],"wgDigitTransformTable":["",""],"wgDefaultDateFormat":"dmy","wgMonthNames":["","January","February","March","April","May","June","July","August","September","October","November","December"],"wgRequestId":"f152e3ecfb406b7e69bafd2b","wgCanonicalNamespace":"","wgCanonicalSpecialPageName":false,"wgNamespaceNumber":0,"wgPageName":"Pacman","wgTitle":"Pacman","wgCurRevisionId":888786,"wgRevisionId":888786,"wgArticleId":1577,"wgIsArticle":true,"wgIsRedirect":false,"wgAction":"view","wgUserName":null,"wgUserGroups":["*"],"wgCategories":["Pages or sections flagged with Template:Expansion","Pages or sections flagged with Template:Out of date","Arch projects","Package manager"],"wgPageViewLanguage":"en","wgPageContentLanguage":"en","wgPageContentModel":"wikitext","wgRelevantPageName":"Pacman","wgRelevantArticleId":1577,"wgIsProbablyEditable":false,"wgRelevantPageIsProbablyEditable":false,"wgRestrictionEdit":[],"wgRestrictionMove":[],"wgVisualEditor":{"pageLanguageCode":"en","pageLanguageDir":"ltr","pageVariantFallbacks":"en"},"wgCheckUserClientHintsHeadersJsApi":["brands","architecture","bitness","fullVersionList","mobile","model","platform","platformVersion"],"wgEditSubmitButtonLabelPublish":false,"wgVisualEditorPageIsDisambiguation":false};
RLSTATE={"site.styles":"ready","user.styles":"ready","user":"ready","user.options":"loading","skins.vector.search.codex.styles":"ready","skins.vector.styles":"ready","skins.vector.icons":"ready","zzz.ext.archLinux.styles":"ready","ext.visualEditor.desktopArticleTarget.noscript":"ready"};RLPAGEMODULES=["site","mediawiki.page.ready","mediawiki.toc","skins.vector.js","ext.checkUser.clientHints","ext.visualEditor.desktopArticleTarget.init"];</script>
<script>(RLQ=window.RLQ||[]).push(function(){mw.loader.impl(function(){return["user.options@12s5i",function($,jQuery,require,module){mw.user.tokens.set({"patrolToken":"+\\","watchToken":"+\\","csrfToken":"+\\"});
}];});});</script>
<link rel="stylesheet" href="/load.php?lang=en&amp;modules=ext.visualEditor.desktopArticleTarget.noscript%7Cskins.vector.icons%2Cstyles%7Cskins.vector.search.codex.styles%7Czzz.ext.archLinux.styles&amp;only=styles&amp;skin=vector-2022">
<script async="" src="/load.php?lang=en&amp;modules=startup&amp;only=scripts&amp;raw=1&amp;skin=vector-2022"></script>
<meta name="ResourceLoaderDynamicStyles" content="">
<link rel="stylesheet" href="/load.php?lang=en&amp;modules=site.styles&amp;only=styles&amp;skin=vector-2022">
<meta name="generator" content="MediaWiki 1.46.2">
<meta name="referrer" content="no-referrer-when-downgrade">
<meta name="robots" content="max-image-preview:standard">
<meta name="format-detection" content="telephone=no">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, minimum-scale=0.25, maximum-scale=5.0">
<link rel="search" type="application/opensearchdescription+xml" href="/rest.php/v1/search" title="ArchWiki (en)">
<link rel="EditURI" type="application/rsd+xml" href="https://wiki.archlinux.org/api.php?action=rsd">
<link rel="license" href="https://www.gnu.org/copyleft/fdl.html">
<link rel="alternate" type="application/atom+xml" title="ArchWiki Atom feed" href="/index.php?title=Special:RecentChanges&amp;feed=atom">
</head>
<body class="skin--responsive skin-vector skin-vector-search-vue mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject page-Pacman rootpage-Pacman skin-vector-2022 action-view"><div id="archnavbar" class="noprint mw-no-invert">
    <div id="archnavbarlogo">
        <p><a id="logo" href="https://archlinux.org/"></a></p>
    </div>
    <div id="archnavbarmenu">
        <ul id="archnavbarlist">
                        <li id="anb-home"><a href="https://archlinux.org/">Home</a></li>            <li id="anb-packages"><a href="https://archlinux.org/packages/">Packages</a></li>            <li id="anb-forums"><a href="https://bbs.archlinux.org/">Forums</a></li>            <li id="anb-wiki" class="anb-selected"><a href="https://wiki.archlinux.org/">Wiki</a></li>            <li id="anb-gitlab"><a href="https://gitlab.archlinux.org/archlinux">GitLab</a></li>            <li id="anb-security"><a href="https://security.archlinux.org/">Security</a></li>            <li id="anb-aur"><a href="https://aur.archlinux.org/">AUR</a></li>            <li id="anb-download"><a href="https://archlinux.org/download/">Download</a></li>        </ul>
    </div>
</div>

<div id="mw-aria-live-region" class="mw-aria-live-region" aria-live="polite"></div><a class="mw-jump-link" href="#bodyContent">Jump to content</a>
<div class="vector-header-container">
	<header class="vector-header mw-header no-font-mode-scale">
		<div class="vector-header-start">
			<nav class="vector-main-menu-landmark" aria-label="Site">
				
<div id="vector-main-menu-dropdown" class="vector-dropdown vector-main-menu-dropdown vector-button-flush-left vector-button-flush-right"  title="Main menu" >
	<input type="checkbox" id="vector-main-menu-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-main-menu-dropdown" class="vector-dropdown-checkbox "  aria-label="Main menu"  >
	<label id="vector-main-menu-dropdown-label" for="vector-main-menu-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-menu mw-ui-icon-wikimedia-menu"></span>

<span class="vector-dropdown-label-text">Main menu</span>
	</label>
	<div class="vector-dropdown-content">


				<div id="vector-main-menu-unpinned-container" class="vector-unpinned-container">
		
<div id="vector-main-menu" class="vector-main-menu vector-pinnable-element">
	<div
	class="vector-pinnable-header vector-main-menu-pinnable-header vector-pinnable-header-unpinned"
	data-feature-name="main-menu-pinned"
	data-pinnable-element-id="vector-main-menu"
	data-pinned-container-id="vector-main-menu-pinned-container"
	data-unpinned-container-id="vector-main-menu-unpinned-container"
>
	<div class="vector-pinnable-header-label">Main menu</div>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-main-menu.pin">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-main-menu.unpin">hide</button>
</div>

	
<div id="p-navigation" class="vector-menu mw-portlet mw-portlet-navigation"  >
	<div class="vector-menu-heading">
		Navigation
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="n-mainpage-description" class="mw-list-item"><a href="/title/Main_page" title="Visit the main page [z]" accesskey="z"><span>Main page</span></a></li><li id="n-Table-of-contents" class="mw-list-item"><a href="/title/Table_of_contents"><span>Table of contents</span></a></li><li id="n-portal" class="mw-list-item"><a href="/title/Getting_involved" title="Various ways Archers can contribute to the community"><span>Getting involved</span></a></li><li id="n-currentevents" class="mw-list-item"><a href="/title/ArchWiki:News" title="The latest lowdown on the wiki"><span>Wiki news</span></a></li><li id="n-randompage" class="mw-list-item"><a href="/title/Special:Random" title="Load a random page [x]" accesskey="x"><span>Random page</span></a></li>
		</ul>
		
	</div>
</div>

	
<div id="p-Interaction" class="vector-menu mw-portlet mw-portlet-Interaction"  >
	<div class="vector-menu-heading">
		Interaction
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="n-help" class="mw-list-item"><a href="/title/Category:Help" title="Wiki navigation, reading, and editing help"><span>Help</span></a></li><li id="n-Contributing" class="mw-list-item"><a href="/title/ArchWiki:Contributing"><span>Contributing</span></a></li><li id="n-recentchanges" class="mw-list-item"><a href="/title/Special:RecentChanges" title="A list of recent changes in the wiki [r]" accesskey="r"><span>Recent changes</span></a></li><li id="n-Recent-talks" class="mw-list-item"><a rel="nofollow" href="https://wiki.archlinux.org/index.php?title=Special:RecentChanges&amp;namespace=all-discussions"><span>Recent talks</span></a></li><li id="n-newpages" class="mw-list-item"><a href="/title/Special:NewPages"><span>New pages</span></a></li><li id="n-Statistics" class="mw-list-item"><a href="/title/ArchWiki:Statistics"><span>Statistics</span></a></li><li id="n-Requests" class="mw-list-item"><a href="/title/ArchWiki_talk:Requests"><span>Requests</span></a></li>
		</ul>
		
	</div>
</div>

</div>

				</div>

	</div>
</div>

		</nav>
			
<a href="/title/Main_page" class="mw-logo">
	<span class="mw-logo-container skin-invert">
		<strong class="mw-logo-wordmark">ArchWiki</strong>
	</span>
</a>

		</div>
		<div class="vector-header-end">
			
<div id="p-search" role="search" class="vector-search-box-vue  vector-search-box-collapses vector-search-box-show-thumbnail vector-search-box-auto-expand-width vector-search-box">
	<a href="/title/Special:Search" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only search-toggle" title="Search ArchWiki [f]" accesskey="f"><span class="vector-icon mw-ui-icon-search mw-ui-icon-wikimedia-search"></span>

<span>Search</span>
	</a>
	<div class="vector-typeahead-search-container">
		<div class="cdx-typeahead-search cdx-typeahead-search--show-thumbnail cdx-typeahead-search--auto-expand-width">
			<form action="/index.php" id="searchform" class="cdx-search-input cdx-search-input--has-end-button">
				<div id="simpleSearch" class="cdx-search-input__input-wrapper"  data-search-loc="header-moved">
					<div class="cdx-text-input cdx-text-input--has-start-icon">
						<input
							class="cdx-text-input__input mw-searchInput" autocomplete="off"
							 type="search" name="search" placeholder="Search ArchWiki" aria-label="Search ArchWiki" autocapitalize="none" spellcheck="false" title="Search ArchWiki [f]" accesskey="f" id="searchInput"
							>
						<span class="cdx-text-input__icon cdx-text-input__start-icon"></span>
					</div>
					<input type="hidden" name="title" value="Special:Search">
				</div>
				<button class="cdx-button cdx-search-input__end-button">Search</button>
			</form>
		</div>
	</div>
</div>

			<nav class="vector-user-links vector-user-links-wide" aria-label="Personal tools">
	<div class="vector-user-links-main">
	
<div id="p-vector-user-menu-preferences" class="vector-menu mw-portlet emptyPortlet"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			
		</ul>
		
	</div>
</div>

	
<div id="p-vector-user-menu-userpage" class="vector-menu mw-portlet emptyPortlet"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			
		</ul>
		
	</div>
</div>

	<nav class="vector-appearance-landmark" aria-label="Appearance">
		
<div id="vector-appearance-dropdown" class="vector-dropdown "  title="Change the appearance of the page&#039;s font size, width, and color" >
	<input type="checkbox" id="vector-appearance-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-appearance-dropdown" class="vector-dropdown-checkbox "  aria-label="Appearance"  >
	<label id="vector-appearance-dropdown-label" for="vector-appearance-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-appearance mw-ui-icon-wikimedia-appearance"></span>

<span class="vector-dropdown-label-text">Appearance</span>
	</label>
	<div class="vector-dropdown-content">


			<div id="vector-appearance-unpinned-container" class="vector-unpinned-container">
				
			</div>
		
	</div>
</div>

	</nav>
	
<div id="p-vector-user-menu-notifications" class="vector-menu mw-portlet emptyPortlet"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			
		</ul>
		
	</div>
</div>

	
<div id="p-vector-user-menu-overflow" class="vector-menu mw-portlet"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			<li id="pt-createaccount-2" class="mw-list-item user-links-collapsible-item"><a data-mw-interface  href="/index.php?title=Special:CreateAccount&amp;returnto=Pacman" title="You are encouraged to create an account and log in; however, it is not mandatory" class=""><span>Create account</span></a>
</li>
<li id="pt-login-2" class="mw-list-item user-links-collapsible-item"><a data-mw-interface  href="/index.php?title=Special:UserLogin&amp;returnto=Pacman" title="You are encouraged to log in; however, it is not mandatory [o]" accesskey="o" class=""><span>Log in</span></a>
</li>

			
		</ul>
		
	</div>
</div>

	</div>
	
<div id="vector-user-links-dropdown" class="vector-dropdown vector-user-menu vector-button-flush-right vector-user-menu-logged-out user-links-collapsible-item"  title="More options" >
	<input type="checkbox" id="vector-user-links-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-user-links-dropdown" class="vector-dropdown-checkbox "  aria-label="Personal tools"  >
	<label id="vector-user-links-dropdown-label" for="vector-user-links-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-ellipsis mw-ui-icon-wikimedia-ellipsis"></span>

<span class="vector-dropdown-label-text">Personal tools</span>
	</label>
	<div class="vector-dropdown-content">


		
<div id="p-personal" class="vector-menu mw-portlet mw-portlet-personal user-links-collapsible-item"  title="User menu" >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			<li id="pt-createaccount" class="mw-list-item user-links-collapsible-item"><a data-mw-interface  href="/index.php?title=Special:CreateAccount&amp;returnto=Pacman" title="You are encouraged to create an account and log in; however, it is not mandatory" class=""><span class="vector-icon mw-ui-icon-userAdd mw-ui-icon-wikimedia-userAdd"></span>

<span>Create account</span></a>
</li>
<li id="pt-login" class="mw-list-item user-links-collapsible-item"><a data-mw-interface  href="/index.php?title=Special:UserLogin&amp;returnto=Pacman" title="You are encouraged to log in; however, it is not mandatory [o]" accesskey="o" class=""><span class="vector-icon mw-ui-icon-logIn mw-ui-icon-wikimedia-logIn"></span>

<span>Log in</span></a>
</li>

			
		</ul>
		
	</div>
</div>

	
	</div>
</div>

</nav>

		</div>
	</header>
</div>
<div class="mw-page-container">
	<div class="mw-page-container-inner">
		<div class="vector-sitenotice-container">
			<div id="siteNotice"></div>
		</div>
		<div class="vector-column-start">
			<div class="vector-main-menu-container">
		<div id="mw-navigation">
			<nav id="mw-panel" class="vector-main-menu-landmark" aria-label="Site">
				<div id="vector-main-menu-pinned-container" class="vector-pinned-container">
				
				</div>
		</nav>
		</div>
	</div>
	<div class="vector-sticky-pinned-container">
				<nav id="mw-panel-toc" aria-label="Contents" data-event-name="ui.sidebar-toc" class="mw-table-of-contents-container vector-toc-landmark">
					<div id="vector-toc-pinned-container" class="vector-pinned-container">
					<div id="vector-toc" class="vector-toc vector-pinnable-element">
	<div
	class="vector-pinnable-header vector-toc-pinnable-header vector-pinnable-header-pinned"
	data-feature-name="toc-pinned"
	data-pinnable-element-id="vector-toc"
	data-pinned-container-id="vector-toc-pinned-container"
	data-unpinned-container-id="vector-toc-unpinned-container"
>
	<h2 class="vector-pinnable-header-label">Contents</h2>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-toc.pin">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-toc.unpin">hide</button>
</div>


	<ul class="vector-toc-contents" id="mw-panel-toc-list">
		<li id="toc-mw-content-text"
			class="vector-toc-list-item vector-toc-level-1">
			<a href="#" class="vector-toc-link">
				<div class="vector-toc-text">Beginning</div>
			</a>
		</li>
		<li id="toc-Usage"
		class="vector-toc-list-item vector-toc-level-1">
		<a class="vector-toc-link" href="#Usage">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">1</span>
				<span>Usage</span>
			</div>
		</a>
		
			<button aria-controls="toc-Usage-sublist" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only vector-toc-toggle">
				<span class="vector-icon mw-ui-icon-wikimedia-expand"></span>
				<span>Toggle Usage subsection</span>
			</button>
		
		<ul id="toc-Usage-sublist" class="vector-toc-list">
			<li id="toc-Installing_packages"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Installing_packages">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.1</span>
					<span>Installing packages</span>
				</div>
			</a>
			
			<ul id="toc-Installing_packages-sublist" class="vector-toc-list">
				<li id="toc-Installing_specific_packages"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Installing_specific_packages">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.1.1</span>
					<span>Installing specific packages</span>
				</div>
			</a>
			
			<ul id="toc-Installing_specific_packages-sublist" class="vector-toc-list">
				<li id="toc-Virtual_packages"
			class="vector-toc-list-item vector-toc-level-4">
			<a class="vector-toc-link" href="#Virtual_packages">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.1.1.1</span>
					<span>Virtual packages</span>
				</div>
			</a>
			
			<ul id="toc-Virtual_packages-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-Installing_package_groups"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Installing_package_groups">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.1.2</span>
					<span>Installing package groups</span>
				</div>
			</a>
			
			<ul id="toc-Installing_package_groups-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-Removing_packages"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Removing_packages">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.2</span>
					<span>Removing packages</span>
				</div>
			</a>
			
			<ul id="toc-Removing_packages-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Upgrading_packages"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Upgrading_packages">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.3</span>
					<span>Upgrading packages</span>
				</div>
			</a>
			
			<ul id="toc-Upgrading_packages-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Querying_package_databases"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Querying_package_databases">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.4</span>
					<span>Querying package databases</span>
				</div>
			</a>
			
			<ul id="toc-Querying_package_databases-sublist" class="vector-toc-list">
				<li id="toc-Pactree"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Pactree">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.4.1</span>
					<span>Pactree</span>
				</div>
			</a>
			
			<ul id="toc-Pactree-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Database_structure"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Database_structure">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.4.2</span>
					<span>Database structure</span>
				</div>
			</a>
			
			<ul id="toc-Database_structure-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-Cleaning_the_package_cache"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Cleaning_the_package_cache">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.5</span>
					<span>Cleaning the package cache</span>
				</div>
			</a>
			
			<ul id="toc-Cleaning_the_package_cache-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Additional_commands"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Additional_commands">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.6</span>
					<span>Additional commands</span>
				</div>
			</a>
			
			<ul id="toc-Additional_commands-sublist" class="vector-toc-list">
				<li id="toc-Dry_run"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Dry_run">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.6.1</span>
					<span>Dry run</span>
				</div>
			</a>
			
			<ul id="toc-Dry_run-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-Installation_reason"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Installation_reason">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.7</span>
					<span>Installation reason</span>
				</div>
			</a>
			
			<ul id="toc-Installation_reason-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-What_happens_during_package_install/upgrade/removal"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#What_happens_during_package_install/upgrade/removal">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">1.8</span>
					<span>What happens during package install/upgrade/removal</span>
				</div>
			</a>
			
			<ul id="toc-What_happens_during_package_install/upgrade/removal-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
	</li>
	<li id="toc-Configuration"
		class="vector-toc-list-item vector-toc-level-1">
		<a class="vector-toc-link" href="#Configuration">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">2</span>
				<span>Configuration</span>
			</div>
		</a>
		
			<button aria-controls="toc-Configuration-sublist" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only vector-toc-toggle">
				<span class="vector-icon mw-ui-icon-wikimedia-expand"></span>
				<span>Toggle Configuration subsection</span>
			</button>
		
		<ul id="toc-Configuration-sublist" class="vector-toc-list">
			<li id="toc-General_options"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#General_options">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1</span>
					<span>General options</span>
				</div>
			</a>
			
			<ul id="toc-General_options-sublist" class="vector-toc-list">
				<li id="toc-Comparing_versions_before_updating"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Comparing_versions_before_updating">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.1</span>
					<span>Comparing versions before updating</span>
				</div>
			</a>
			
			<ul id="toc-Comparing_versions_before_updating-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Parallel_downloads"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Parallel_downloads">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.2</span>
					<span>Parallel downloads</span>
				</div>
			</a>
			
			<ul id="toc-Parallel_downloads-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Skip_package_from_being_upgraded"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Skip_package_from_being_upgraded">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.3</span>
					<span>Skip package from being upgraded</span>
				</div>
			</a>
			
			<ul id="toc-Skip_package_from_being_upgraded-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Skip_package_group_from_being_upgraded"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Skip_package_group_from_being_upgraded">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.4</span>
					<span>Skip package group from being upgraded</span>
				</div>
			</a>
			
			<ul id="toc-Skip_package_group_from_being_upgraded-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Skip_file_from_being_upgraded"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Skip_file_from_being_upgraded">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.5</span>
					<span>Skip file from being upgraded</span>
				</div>
			</a>
			
			<ul id="toc-Skip_file_from_being_upgraded-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Skip_files_from_being_installed_to_system"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Skip_files_from_being_installed_to_system">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.6</span>
					<span>Skip files from being installed to system</span>
				</div>
			</a>
			
			<ul id="toc-Skip_files_from_being_installed_to_system-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Maintain_several_configuration_files"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Maintain_several_configuration_files">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.7</span>
					<span>Maintain several configuration files</span>
				</div>
			</a>
			
			<ul id="toc-Maintain_several_configuration_files-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Hooks"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Hooks">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.1.8</span>
					<span>Hooks</span>
				</div>
			</a>
			
			<ul id="toc-Hooks-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-Repositories_and_mirrors"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Repositories_and_mirrors">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.2</span>
					<span>Repositories and mirrors</span>
				</div>
			</a>
			
			<ul id="toc-Repositories_and_mirrors-sublist" class="vector-toc-list">
				<li id="toc-Package_cache_directory"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Package_cache_directory">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.2.1</span>
					<span>Package cache directory</span>
				</div>
			</a>
			
			<ul id="toc-Package_cache_directory-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Package_security"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Package_security">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">2.2.2</span>
					<span>Package security</span>
				</div>
			</a>
			
			<ul id="toc-Package_security-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
	</ul>
	</li>
	<li id="toc-Troubleshooting"
		class="vector-toc-list-item vector-toc-level-1">
		<a class="vector-toc-link" href="#Troubleshooting">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">3</span>
				<span>Troubleshooting</span>
			</div>
		</a>
		
			<button aria-controls="toc-Troubleshooting-sublist" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only vector-toc-toggle">
				<span class="vector-icon mw-ui-icon-wikimedia-expand"></span>
				<span>Toggle Troubleshooting subsection</span>
			</button>
		
		<ul id="toc-Troubleshooting-sublist" class="vector-toc-list">
			<li id="toc-&quot;Failed_to_commit_transaction_(conflicting_files)&quot;_error"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#&quot;Failed_to_commit_transaction_(conflicting_files)&quot;_error">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.1</span>
					<span>"Failed to commit transaction (conflicting files)" error</span>
				</div>
			</a>
			
			<ul id="toc-&quot;Failed_to_commit_transaction_(conflicting_files)&quot;_error-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-&quot;Failed_to_commit_transaction_(invalid_or_corrupted_package)&quot;_error"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#&quot;Failed_to_commit_transaction_(invalid_or_corrupted_package)&quot;_error">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.2</span>
					<span>"Failed to commit transaction (invalid or corrupted package)" error</span>
				</div>
			</a>
			
			<ul id="toc-&quot;Failed_to_commit_transaction_(invalid_or_corrupted_package)&quot;_error-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-&quot;Failed_to_init_transaction_(unable_to_lock_database)&quot;_error"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#&quot;Failed_to_init_transaction_(unable_to_lock_database)&quot;_error">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.3</span>
					<span>"Failed to init transaction (unable to lock database)" error</span>
				</div>
			</a>
			
			<ul id="toc-&quot;Failed_to_init_transaction_(unable_to_lock_database)&quot;_error-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Packages_cannot_be_retrieved_on_installation"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Packages_cannot_be_retrieved_on_installation">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.4</span>
					<span>Packages cannot be retrieved on installation</span>
				</div>
			</a>
			
			<ul id="toc-Packages_cannot_be_retrieved_on_installation-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Fixing_an_unbootable_system_caused_by_an_interrupted_upgrade"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Fixing_an_unbootable_system_caused_by_an_interrupted_upgrade">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.5</span>
					<span>Fixing an unbootable system caused by an interrupted upgrade</span>
				</div>
			</a>
			
			<ul id="toc-Fixing_an_unbootable_system_caused_by_an_interrupted_upgrade-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-pacman_crashes_during_an_upgrade"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#pacman_crashes_during_an_upgrade">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.6</span>
					<span>pacman crashes during an upgrade</span>
				</div>
			</a>
			
			<ul id="toc-pacman_crashes_during_an_upgrade-sublist" class="vector-toc-list">
				<li id="toc-pacman:_command_not_found"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#pacman:_command_not_found">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.6.1</span>
					<span>pacman: command not found</span>
				</div>
			</a>
			
			<ul id="toc-pacman:_command_not_found-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-Manually_reinstalling_pacman"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Manually_reinstalling_pacman">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.7</span>
					<span>Manually reinstalling pacman</span>
				</div>
			</a>
			
			<ul id="toc-Manually_reinstalling_pacman-sublist" class="vector-toc-list">
				<li id="toc-Using_pacman-static"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Using_pacman-static">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.7.1</span>
					<span>Using pacman-static</span>
				</div>
			</a>
			
			<ul id="toc-Using_pacman-static-sublist" class="vector-toc-list">
				<li id="toc-Using_a_precompiled_pacman-static_binary_when_PKGBUILD_build_fails"
			class="vector-toc-list-item vector-toc-level-4">
			<a class="vector-toc-link" href="#Using_a_precompiled_pacman-static_binary_when_PKGBUILD_build_fails">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.7.1.1</span>
					<span>Using a precompiled pacman-static binary when PKGBUILD build fails</span>
				</div>
			</a>
			
			<ul id="toc-Using_a_precompiled_pacman-static_binary_when_PKGBUILD_build_fails-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-Using_an_external_pacman"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#Using_an_external_pacman">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.7.2</span>
					<span>Using an external pacman</span>
				</div>
			</a>
			
			<ul id="toc-Using_an_external_pacman-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-By_manually_extracting"
			class="vector-toc-list-item vector-toc-level-3">
			<a class="vector-toc-link" href="#By_manually_extracting">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.7.3</span>
					<span>By manually extracting</span>
				</div>
			</a>
			
			<ul id="toc-By_manually_extracting-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
		</li>
		<li id="toc-&quot;Unable_to_find_root_device&quot;_error_after_rebooting"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#&quot;Unable_to_find_root_device&quot;_error_after_rebooting">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.8</span>
					<span>"Unable to find root device" error after rebooting</span>
				</div>
			</a>
			
			<ul id="toc-&quot;Unable_to_find_root_device&quot;_error_after_rebooting-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-&quot;Warning:_current_locale_is_invalid;_using_default_&quot;C&quot;_locale&quot;_error"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#&quot;Warning:_current_locale_is_invalid;_using_default_&quot;C&quot;_locale&quot;_error">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.9</span>
					<span>"Warning: current locale is invalid; using default "C" locale" error</span>
				</div>
			</a>
			
			<ul id="toc-&quot;Warning:_current_locale_is_invalid;_using_default_&quot;C&quot;_locale&quot;_error-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Missing_locales_warning_messages"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Missing_locales_warning_messages">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.10</span>
					<span>Missing locales warning messages</span>
				</div>
			</a>
			
			<ul id="toc-Missing_locales_warning_messages-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-pacman_does_not_honor_proxy_settings"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#pacman_does_not_honor_proxy_settings">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.11</span>
					<span>pacman does not honor proxy settings</span>
				</div>
			</a>
			
			<ul id="toc-pacman_does_not_honor_proxy_settings-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-How_do_I_reinstall_all_packages,_retaining_information_on_whether_something_was_explicitly_installed_or_as_a_dependency?"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#How_do_I_reinstall_all_packages,_retaining_information_on_whether_something_was_explicitly_installed_or_as_a_dependency?">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.12</span>
					<span>How do I reinstall all packages, retaining information on whether something was explicitly installed or as a dependency?</span>
				</div>
			</a>
			
			<ul id="toc-How_do_I_reinstall_all_packages,_retaining_information_on_whether_something_was_explicitly_installed_or_as_a_dependency?-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-&quot;Cannot_open_shared_object_file&quot;_error"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#&quot;Cannot_open_shared_object_file&quot;_error">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.13</span>
					<span>"Cannot open shared object file" error</span>
				</div>
			</a>
			
			<ul id="toc-&quot;Cannot_open_shared_object_file&quot;_error-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Freeze_of_package_downloads"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Freeze_of_package_downloads">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.14</span>
					<span>Freeze of package downloads</span>
				</div>
			</a>
			
			<ul id="toc-Freeze_of_package_downloads-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Failed_retrieving_file_&#039;core.db&#039;_from_mirror"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Failed_retrieving_file_&#039;core.db&#039;_from_mirror">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.15</span>
					<span>Failed retrieving file 'core.db' from mirror</span>
				</div>
			</a>
			
			<ul id="toc-Failed_retrieving_file_&#039;core.db&#039;_from_mirror-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-error:_&#039;local-package.pkg.tar&#039;:_permission_denied"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#error:_&#039;local-package.pkg.tar&#039;:_permission_denied">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.16</span>
					<span>error: 'local-package.pkg.tar': permission denied</span>
				</div>
			</a>
			
			<ul id="toc-error:_&#039;local-package.pkg.tar&#039;:_permission_denied-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-error:_could_not_determine_cachedir_mount_point_/var/cache/pacman/pkg"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#error:_could_not_determine_cachedir_mount_point_/var/cache/pacman/pkg">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.17</span>
					<span>error: could not determine cachedir mount point /var/cache/pacman/pkg</span>
				</div>
			</a>
			
			<ul id="toc-error:_could_not_determine_cachedir_mount_point_/var/cache/pacman/pkg-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-error:_GPGME_error:_No_data"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#error:_GPGME_error:_No_data">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.18</span>
					<span>error: GPGME error: No data</span>
				</div>
			</a>
			
			<ul id="toc-error:_GPGME_error:_No_data-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-error:_GPGME_error:_General_error_and_&quot;::_File_/var/cache/pacman/pkg/&lt;package&gt;.pkg.tar.zst_is_corrupted_(invalid_or_corrupted_package_(PGP_signature))."
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#error:_GPGME_error:_General_error_and_&quot;::_File_/var/cache/pacman/pkg/&lt;package&gt;.pkg.tar.zst_is_corrupted_(invalid_or_corrupted_package_(PGP_signature)).">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.19</span>
					<span>error: GPGME error: General error and ":: File /var/cache/pacman/pkg/&lt;package>.pkg.tar.zst is corrupted (invalid or corrupted package (PGP signature)).</span>
				</div>
			</a>
			
			<ul id="toc-error:_GPGME_error:_General_error_and_&quot;::_File_/var/cache/pacman/pkg/&lt;package&gt;.pkg.tar.zst_is_corrupted_(invalid_or_corrupted_package_(PGP_signature)).-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Reinstall_broken_or_out-of-sync_packages"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Reinstall_broken_or_out-of-sync_packages">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.20</span>
					<span>Reinstall broken or out-of-sync packages</span>
				</div>
			</a>
			
			<ul id="toc-Reinstall_broken_or_out-of-sync_packages-sublist" class="vector-toc-list">
			</ul>
		</li>
		<li id="toc-Check_for_missing/corrupted_files"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Check_for_missing/corrupted_files">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.21</span>
					<span>Check for missing/corrupted files</span>
				</div>
			</a>
			
			<ul id="toc-Check_for_missing/corrupted_files-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
	</li>
	<li id="toc-See_also"
		class="vector-toc-list-item vector-toc-level-1">
		<a class="vector-toc-link" href="#See_also">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">4</span>
				<span>See also</span>
			</div>
		</a>
		
		<ul id="toc-See_also-sublist" class="vector-toc-list">
		</ul>
	</li>
</ul>
</div>

					</div>
		</nav>
			</div>
		</div>
		<div class="mw-content-container">
			<main id="content" class="mw-body">
				<header class="mw-body-header vector-page-titlebar no-font-mode-scale">
					<nav aria-label="Contents" class="vector-toc-landmark">
						
<div id="vector-page-titlebar-toc" class="vector-dropdown vector-page-titlebar-toc vector-button-flush-left"  title="Table of Contents" >
	<input type="checkbox" id="vector-page-titlebar-toc-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-page-titlebar-toc" class="vector-dropdown-checkbox "  aria-label="Toggle the table of contents"  >
	<label id="vector-page-titlebar-toc-label" for="vector-page-titlebar-toc-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-listBullet mw-ui-icon-wikimedia-listBullet"></span>

<span class="vector-dropdown-label-text">Toggle the table of contents</span>
	</label>
	<div class="vector-dropdown-content">


							<div id="vector-page-titlebar-toc-unpinned-container" class="vector-unpinned-container">
			</div>
		
	</div>
</div>

					</nav>
					<h1 id="firstHeading" class="firstHeading mw-first-heading">pacman</h1>
							
<div id="p-lang-btn" class="vector-dropdown mw-portlet mw-portlet-lang"  >
	<input type="checkbox" id="p-lang-btn-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-p-lang-btn" class="vector-dropdown-checkbox mw-interlanguage-selector" aria-label="Go to an article in another language. Available in 13 languages"   >
	<label id="p-lang-btn-label" for="p-lang-btn-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--action-progressive mw-portlet-lang-heading-13" aria-hidden="true"  ><span class="vector-icon mw-ui-icon-language-progressive mw-ui-icon-wikimedia-language-progressive"></span>

<span class="vector-dropdown-label-text">13 languages</span>
	</label>
	<div class="vector-dropdown-content">

		<div class="vector-menu-content">
			
			<ul class="vector-menu-content-list">
				
				<li class="interlanguage-link interwiki-de mw-list-item"><a href="https://wiki.archlinux.de/title/Pacman" title="Pacman – Deutsch" lang="de" hreflang="de" data-title="Pacman" data-language-autonym="Deutsch" data-language-local-name="Deutsch" class="interlanguage-link-target"><span>Deutsch</span></a></li><li class="interlanguage-link interwiki-es mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Español)" title="Pacman – español" lang="es" hreflang="es" data-title="Pacman" data-language-autonym="Español" data-language-local-name="español" class="interlanguage-link-target"><span>Español</span></a></li><li class="interlanguage-link interwiki-fa mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(فارسی)" title="Pacman – فارسی" lang="fa" hreflang="fa" data-title="Pacman" data-language-autonym="فارسی" data-language-local-name="فارسی" class="interlanguage-link-target"><span>فارسی</span></a></li><li class="interlanguage-link interwiki-fi mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Suomi)" title="Pacman – suomi" lang="fi" hreflang="fi" data-title="Pacman" data-language-autonym="Suomi" data-language-local-name="suomi" class="interlanguage-link-target"><span>Suomi</span></a></li><li class="interlanguage-link interwiki-fr mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Français)" title="Pacman – français" lang="fr" hreflang="fr" data-title="Pacman" data-language-autonym="Français" data-language-local-name="français" class="interlanguage-link-target"><span>Français</span></a></li><li class="interlanguage-link interwiki-hu mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Magyar)" title="Pacman – magyar" lang="hu" hreflang="hu" data-title="Pacman" data-language-autonym="Magyar" data-language-local-name="magyar" class="interlanguage-link-target"><span>Magyar</span></a></li><li class="interlanguage-link interwiki-id mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Bahasa Indonesia)" title="Pacman – Bahasa Indonesia" lang="id" hreflang="id" data-title="Pacman" data-language-autonym="Bahasa Indonesia" data-language-local-name="Bahasa Indonesia" class="interlanguage-link-target"><span>Bahasa Indonesia</span></a></li><li class="interlanguage-link interwiki-it mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Italiano)" title="Pacman – italiano" lang="it" hreflang="it" data-title="Pacman" data-language-autonym="Italiano" data-language-local-name="italiano" class="interlanguage-link-target"><span>Italiano</span></a></li><li class="interlanguage-link interwiki-ja mw-list-item"><a href="https://wiki.archlinux.jp/index.php/Pacman" title="Pacman – 日本語" lang="ja" hreflang="ja" data-title="Pacman" data-language-autonym="日本語" data-language-local-name="日本語" class="interlanguage-link-target"><span>日本語</span></a></li><li class="interlanguage-link interwiki-pt mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Português)" title="Pacman – português" lang="pt" hreflang="pt" data-title="Pacman" data-language-autonym="Português" data-language-local-name="português" class="interlanguage-link-target"><span>Português</span></a></li><li class="interlanguage-link interwiki-ru mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Русский)" title="Pacman – русский" lang="ru" hreflang="ru" data-title="Pacman" data-language-autonym="Русский" data-language-local-name="русский" class="interlanguage-link-target"><span>Русский</span></a></li><li class="interlanguage-link interwiki-sv mw-list-item"><a href="https://wiki.archlinux.org/title/Pacman_(Svenska)" title="Pacman – svenska" lang="sv" hreflang="sv" data-title="Pacman" data-language-autonym="Svenska" data-language-local-name="svenska" class="interlanguage-link-target"><span>Svenska</span></a></li><li class="interlanguage-link interwiki-zh-hans mw-list-item"><a href="https://wiki.archlinuxcn.org/wiki/Pacman" title="Pacman – 中文（简体）" lang="zh-Hans" hreflang="zh-Hans" data-title="Pacman" data-language-autonym="中文（简体）" data-language-local-name="中文（简体）" class="interlanguage-link-target"><span>中文（简体）</span></a></li>
			</ul>
			
		</div>

	</div>
</div>
</header>
				<div class="vector-page-toolbar vector-feature-custom-font-size-clientpref--excluded">
					<div class="vector-page-toolbar-container">
						<div id="left-navigation">
							<nav aria-label="Namespaces">
								
<div id="p-associated-pages" class="vector-menu vector-menu-tabs mw-portlet mw-portlet-associated-pages"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="ca-nstab-main" class="selected vector-tab-noicon mw-list-item"><a href="/title/Pacman" title="View the content page [c]" accesskey="c"><span>Page</span></a></li><li id="ca-talk" class="vector-tab-noicon mw-list-item"><a href="/title/Talk:Pacman" rel="discussion" title="Discussion about the content page [t]" accesskey="t"><span>Discussion</span></a></li>
		</ul>
		
	</div>
</div>

								
<div id="vector-variants-dropdown" class="vector-dropdown emptyPortlet"  >
	<input type="checkbox" id="vector-variants-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-variants-dropdown" class="vector-dropdown-checkbox " aria-label="Change language variant"   >
	<label id="vector-variants-dropdown-label" for="vector-variants-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet" aria-hidden="true"  ><span class="vector-dropdown-label-text">English</span>
	</label>
	<div class="vector-dropdown-content">


					
<div id="p-variants" class="vector-menu mw-portlet mw-portlet-variants emptyPortlet"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			
		</ul>
		
	</div>
</div>

				
	</div>
</div>

							</nav>
						</div>
						<div id="right-navigation" class="vector-collapsible">
							<nav aria-label="Views">
								
<div id="p-views" class="vector-menu vector-menu-tabs mw-portlet mw-portlet-views"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="ca-view" class="selected vector-tab-noicon mw-list-item"><a href="/title/Pacman"><span>Read</span></a></li><li id="ca-viewsource" class="vector-tab-noicon mw-list-item"><a href="/index.php?title=Pacman&amp;action=edit" title="This page is protected.&#10;You can view its source [e]" accesskey="e"><span>View source</span></a></li><li id="ca-history" class="vector-tab-noicon mw-list-item"><a href="/index.php?title=Pacman&amp;action=history" title="Past revisions of this page [h]" accesskey="h"><span>View history</span></a></li>
		</ul>
		
	</div>
</div>

							</nav>
				
							<nav class="vector-page-tools-landmark" aria-label="Page tools">
								
<div id="vector-page-tools-dropdown" class="vector-dropdown vector-page-tools-dropdown"  >
	<input type="checkbox" id="vector-page-tools-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-page-tools-dropdown" class="vector-dropdown-checkbox "  aria-label="Tools"  >
	<label id="vector-page-tools-dropdown-label" for="vector-page-tools-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet" aria-hidden="true"  ><span class="vector-dropdown-label-text">Tools</span>
	</label>
	<div class="vector-dropdown-content">


									<div id="vector-page-tools-unpinned-container" class="vector-unpinned-container">
						
<div id="vector-page-tools" class="vector-page-tools vector-pinnable-element">
	<div
	class="vector-pinnable-header vector-page-tools-pinnable-header vector-pinnable-header-unpinned"
	data-feature-name="page-tools-pinned"
	data-pinnable-element-id="vector-page-tools"
	data-pinned-container-id="vector-page-tools-pinned-container"
	data-unpinned-container-id="vector-page-tools-unpinned-container"
>
	<div class="vector-pinnable-header-label">Tools</div>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-page-tools.pin">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-page-tools.unpin">hide</button>
</div>

	
<div id="p-cactions" class="vector-menu mw-portlet mw-portlet-cactions emptyPortlet vector-has-collapsible-items"  title="More options" >
	<div class="vector-menu-heading">
		Actions
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="ca-more-view" class="selected vector-more-collapsible-item mw-list-item"><a href="/title/Pacman"><span>Read</span></a></li><li id="ca-more-viewsource" class="vector-more-collapsible-item mw-list-item"><a href="/index.php?title=Pacman&amp;action=edit"><span>View source</span></a></li><li id="ca-more-history" class="vector-more-collapsible-item mw-list-item"><a href="/index.php?title=Pacman&amp;action=history"><span>View history</span></a></li>
		</ul>
		
	</div>
</div>

<div id="p-tb" class="vector-menu mw-portlet mw-portlet-tb"  >
	<div class="vector-menu-heading">
		General
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="t-whatlinkshere" class="mw-list-item"><a href="/title/Special:WhatLinksHere/Pacman" title="A list of all wiki pages that link here [j]" accesskey="j"><span>What links here</span></a></li><li id="t-recentchangeslinked" class="mw-list-item"><a href="/title/Special:RecentChangesLinked/Pacman" rel="nofollow" title="Recent changes in pages linked from this page [k]" accesskey="k"><span>Related changes</span></a></li><li id="t-print" class="mw-list-item"><a href="javascript:print();" rel="alternate" title="Printable version of this page [p]" accesskey="p"><span>Printable version</span></a></li><li id="t-permalink" class="mw-list-item"><a href="/index.php?title=Pacman&amp;oldid=888786" title="Permanent link to this revision of this page"><span>Permanent link</span></a></li><li id="t-info" class="mw-list-item"><a href="/index.php?title=Pacman&amp;action=info" title="More information about this page"><span>Page information</span></a></li>
		</ul>
		
	</div>
</div>

</div>

									</div>
				
	</div>
</div>

							</nav>
						</div>
					</div>
				</div>
				<div class="vector-column-end no-font-mode-scale">
					<div class="vector-sticky-pinned-container">
						<div class="wp25eastereggs-vector-sitenotice-landmark"></div>
						<nav class="vector-page-tools-landmark" aria-label="Page tools">
							<div id="vector-page-tools-pinned-container" class="vector-pinned-container">
				
							</div>
		</nav>
						<nav class="vector-appearance-landmark" aria-label="Appearance">
							<div id="vector-appearance-pinned-container" class="vector-pinned-container">
				<div id="vector-appearance" class="vector-appearance vector-pinnable-element">
	<div
	class="vector-pinnable-header vector-appearance-pinnable-header vector-pinnable-header-pinned"
	data-feature-name="appearance-pinned"
	data-pinnable-element-id="vector-appearance"
	data-pinned-container-id="vector-appearance-pinned-container"
	data-unpinned-container-id="vector-appearance-unpinned-container"
>
	<div class="vector-pinnable-header-label">Appearance</div>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-appearance.pin">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-appearance.unpin">hide</button>
</div>


</div>

							</div>
		</nav>
					</div>
				</div>
				<div id="bodyContent" class="vector-body" aria-labelledby="firstHeading" data-mw-ve-target-container>
					<div class="vector-body-before-content">
							<div class="mw-indicators">
		</div>

						<div id="siteSub" class="noprint">From ArchWiki</div>
					</div>
					<div id="contentSub"><div id="mw-content-subtitle"></div></div>
					
					
					<div id="mw-content-text" class="mw-body-content"><div class="mw-content-ltr mw-parser-output" lang="en" dir="ltr"><p><span>
</span>
</p>
<div class="archwiki-template-meta-related-articles"><p>Related articles</p><ul>
<li><a href="/title/Pacman/Package_signing" title="Pacman/Package signing">/Package signing</a></li>
<li><a href="/title/Pacman/Pacnew_and_Pacsave" title="Pacman/Pacnew and Pacsave">/Pacnew and Pacsave</a></li>
<li><a href="/title/Pacman/Restore_local_database" title="Pacman/Restore local database">/Restore local database</a></li>
<li><a href="/title/Pacman/Rosetta" title="Pacman/Rosetta">/Rosetta</a></li>
<li><a href="/title/Pacman/Tips_and_tricks" title="Pacman/Tips and tricks">/Tips and tricks</a></li>
<li><a href="/title/Arch_User_Repository" title="Arch User Repository">Arch User Repository</a></li>
<li><a href="/title/Creating_packages" title="Creating packages">Creating packages</a></li>
<li><a href="/title/Downgrading_packages" title="Downgrading packages">Downgrading packages</a></li>
<li><a href="/title/FAQ#Package_management" class="mw-redirect" title="FAQ">FAQ#Package management</a></li>
<li><a href="/title/Namcap" title="Namcap">namcap</a></li>
<li><a href="/title/Package_proxy_cache" title="Package proxy cache">Package proxy cache</a></li>
<li><a href="/title/System_maintenance" title="System maintenance">System maintenance</a></li>
</ul></div>
<p>The <a rel="nofollow" class="external text" href="https://pacman.archlinux.page/">pacman</a> <a href="https://en.wikipedia.org/wiki/Package_manager" class="extiw" title="wikipedia:Package manager">package manager</a> is one of the major distinguishing features of <a href="/title/Arch_Linux" title="Arch Linux">Arch Linux</a>. It combines a simple binary package format with an easy-to-use <a href="/title/Arch_build_system" title="Arch build system">Arch build system</a>. The goal of <i>pacman</i> is to make it possible to easily manage packages, whether they are from the <a href="/title/Official_repositories" title="Official repositories">official repositories</a> or the user's own builds.
</p><p><i>pacman</i> keeps the system up-to-date by synchronizing package lists with the master server. This server/client model also allows the user to download/install packages with a simple command, complete with all required dependencies.
</p><p><i>pacman</i> is written in the <a href="/title/C" title="C">C</a> programming language and uses the <span class="plainlinks archwiki-template-man" title="$ man 1 bsdtar"><a rel="nofollow" class="external text" href="https://man.archlinux.org/man/bsdtar.1">bsdtar(1)</a></span> <a href="https://en.wikipedia.org/wiki/tar_(computing)" class="extiw" title="w:tar (computing)">tar</a> format for packaging.
</p>
<div class="archwiki-template-box archwiki-template-box-tip"><strong>Tip</strong> The <span class="plainlinks archwiki-template-pkg"><a rel="nofollow" class="external text" href="https://archlinux.org/packages/?name=pacman">pacman</a></span> package contains tools such as <a href="/title/Makepkg" title="Makepkg">makepkg</a> and <span class="plainlinks archwiki-template-man" title="$ man 8 vercmp"><a rel="nofollow" class="external text" href="https://man.archlinux.org/man/vercmp.8">vercmp(8)</a></span>. Other useful tools such as <a href="#Pactree">pactree</a> and <a href="/title/Checkupdates" class="mw-redirect" title="Checkupdates">checkupdates</a> are found in <span class="plainlinks archwiki-template-pkg"><a rel="nofollow" class="external text" href="https://archlinux.org/packages/?name=pacman-contrib">pacman-contrib</a></span>. Run <code>pacman -Ql pacman pacman-contrib | grep -E 'bin/.+'</code> to see the full list.</div>
<meta property="mw:PageProp/toc" />
<div class="mw-heading mw-heading2"><h2 id="Usage">Usage</h2></div>
<p>What follows is just a small sample of the operations that <i>pacman</i> can perform. To read more examples, refer to <span class="plainlinks archwiki-template-man" title="$ man 8 pacman"><a rel="nofollow" class="external text" href="https://man.archlinux.org/man/pacman.8">pacman(8)</a></span>.
</p>
<div class="archwiki-template-box archwiki-template-box-tip"><strong>Tip</strong> For those who have used other Linux distributions before, there is a helpful <a href="/title/Pacman/Rosetta" title="Pacman/Rosetta">Pacman/Rosetta</a> article.</div>
<div class="mw-heading mw-heading3"><h3 id="Installing_packages">Installing packages</h3></div>
<p>A package is an archive containing:
</p>
<ul><li>all of the (compiled) files of an application</li>
<li>metadata about the application, such as application name, version, dependencies, etc.</li>
<li>installation files and directives for <i>pacman</i></li></ul>
<p>Arch's package manager <i>pacman</i> can install, update, and remove those packages. Using packages instead of compiling and installing programs yourself has various benefits:
</p>
<ul><li>easily updatable: <i>pacman</i> will update existing packages as soon as updates are available</li>
<li>dependency checks: <i>pacman</i> handles dependencies for you, you only need to specify the program and <i>pacman</i> installs it together with every other program it needs</li>
<li>clean removal: <i>pacman</i> has a list of every file in a package; this way, no files are unintentionally left behind when you decide to remove a package.</li></ul>
<div class="archwiki-template-box archwiki-template-box-note"><strong>Note</strong> 
<ul><li>Packages often have <a href="/title/PKGBUILD#optdepends" title="PKGBUILD">optional dependencies</a> which are packages that provide additional functionality to the application but not strictly required for running it. When installing a package, <i>pacman</i> will list a package's optional dependencies, but they will not be found in <code>pacman.log</code>. Use the <a href="#Querying_package_databases">#Querying package databases</a> command to view the optional dependencies of a package.</li>
<li>When installing a package which you require only as a (optional) dependency of some other package (i.e. not required by you explicitly), it is recommended to use the <code>--asdeps</code> option. For details, see the <a href="#Installation_reason">#Installation reason</a> section.</li></ul></div>
<div class="archwiki-template-box archwiki-template-box-warning"><strong>Warning</strong> When installing packages in Arch, avoid refreshing the package list without <a href="#Upgrading_packages">upgrading the system</a> (for example, when a <a href="#Packages_cannot_be_retrieved_on_installation">package is no longer found</a> in the official repositories). In practice, do <b>not</b> run <code>pacman -Sy <i>package_name</i></code> instead of <code>pacman -Sy<b>u</b> <i>package_name</i></code>, as the former could lead to dependency issues. See <a href="/title/System_maintenance#Partial_upgrades_are_unsupported" title="System maintenance">System maintenance#Partial upgrades are unsupported</a> and <a rel="nofollow" class="external text" href="https://bbs.archlinux.org/viewtopic.php?id=89328">BBS#89328</a>.</div>
<div class="mw-heading mw-heading4"><h4 id="Installing_specific_packages">Installing specific packages</h4></div>
<p>To install a single package or list of packages, including dependencies, issue the following command:
</p>
<pre># pacman -S <i>package_name1</i> <i>package_name2</i> 