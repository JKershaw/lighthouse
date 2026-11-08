<!DOCTYPE html>
<html class="client-nojs vector-feature-language-in-header-disabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-1 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-day vector-sticky-header-enabled vector-toc-available skin-thumbsize-clientpref-standard skin-underline-clientpref-browser" lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<title>Wikimedia APIs/Rate limits - MediaWiki</title>
<script>(function(){var className="client-js vector-feature-language-in-header-disabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-1 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-day vector-sticky-header-enabled vector-toc-available skin-thumbsize-clientpref-standard skin-underline-clientpref-browser";var cookie=document.cookie.match(/(?:^|; )mediawikiwikimwclientpreferences=([^;]+)/);if(cookie){cookie[1].split('%2C').forEach(function(pref){className=className.replace(new RegExp('(^| )'+pref.replace(/-clientpref-\w+$|[^\w-]+/g,'')+'-clientpref-\\w+( |$)'),'$1'+pref+'$2');});}document.documentElement.className=className;}());RLCONF={"wgBreakFrames":false,"wgSeparatorTransformTable":["",""],"wgDigitTransformTable":["",""],"wgDefaultDateFormat":"dmy","wgMonthNames":["","January","February","March","April","May","June","July","August","September","October","November","December"],"wgRequestId":"60d52f15-6dca-44c7-8a8a-8d7bd99143fe","wgCanonicalNamespace":"","wgCanonicalSpecialPageName":false,"wgNamespaceNumber":0,"wgPageName":"Wikimedia_APIs/Rate_limits","wgTitle":"Wikimedia APIs/Rate limits","wgCurRevisionId":8654799,"wgRevisionId":8654799,"wgArticleId":2365815,"wgIsArticle":true,"wgIsRedirect":false,"wgAction":"view","wgUserName":null,"wgUserGroups":["*"],"wgCategories":[],"wgPageViewLanguage":"en","wgPageContentLanguage":"en","wgPageContentModel":"wikitext","wgRelevantPageName":"Wikimedia_APIs/Rate_limits","wgRelevantArticleId":2365815,"wgTempUserName":null,"wgIsProbablyEditable":false,"wgRelevantPageIsProbablyEditable":false,"wgRestrictionEdit":["autoconfirmed"],"wgRestrictionMove":["autoconfirmed"],"wgNoticeProject":"mediawiki","wgConfirmEditCaptchaNeededForGenericEdit":"hcaptcha","wgConfirmEditForceShowCaptcha":false,"wgConfirmEditHCaptchaSiteKey":"5d0c670e-a5f4-4258-ad16-1f42792c9c62","wgMediaViewerOnClick":true,"wgMediaViewerEnabledByDefault":true,"wgMediaViewerDesktopVue":false,"wgVisualEditor":{"pageLanguageCode":"en","pageLanguageDir":"ltr","pageVariantFallbacks":"en"},"wgWMESchemaEditAttemptStepOversample":false,"wgWMEPageLength":8000,"wgTestKitchenUserExperiments":{"overrides":[],"enrolled":[],"assigned":[],"subject_ids":[]},"wgEditSubmitButtonLabelPublish":true,"wgVisualEditorPageIsDisambiguation":false,"wgDiscussionToolsFeaturesEnabled":{"replytool":true,"newtopictool":true,"sourcemodetoolbar":true,"topicsubscription":false,"autotopicsub":false,"visualenhancements":false},"wgDiscussionToolsFallbackEditMode":"visual","wgULSPosition":"personal","wgULSisCompactLinksEnabled":true,"wgULSContentLanguageSelectorEnabled":true,"wgULSLanguageSelectorV2Enabled":true,"wgCheckUserClientHintsHeadersJsApi":["brands","architecture","bitness","fullVersionList","mobile","model","platform","platformVersion"],"wgCheckUserClientHintsInEditRequest":true,"wgSiteNoticeId":"2.16"};
RLSTATE={"ext.globalCssJs.user.styles":"ready","site.styles":"ready","user.styles":"ready","ext.globalCssJs.user":"ready","user":"ready","user.options":"loading","ext.cite.styles":"ready","ext.discussionTools.init.styles":"ready","ext.wikimediamessages.styles":"ready","oojs-ui-core.styles":"ready","oojs-ui.styles.indicators":"ready","mediawiki.widgets.styles":"ready","oojs-ui-core.icons":"ready","skins.vector.search.codex.styles":"ready","skins.vector.styles":"ready","skins.vector.icons":"ready","ext.visualEditor.desktopArticleTarget.noscript":"ready","ext.uls.pt":"ready","wikibase.client.init":"ready","ext.readingLists.bookmark.icons":"ready","ext.readingLists.bookmark.styles":"ready","ext.dismissableSiteNotice.styles":"ready"};RLPAGEMODULES=["ext.cite.ux-enhancements","site","mediawiki.page.ready","mediawiki.toc","skins.vector.js","ext.centralNotice.geoIP","ext.centralNotice.startUp","ext.urlShortener.toolbar","ext.centralauth.centralautologin","ext.testKitchen","ext.wikimediaCustomizations.donorAccountCreation","mmv.bootstrap","ext.visualEditor.desktopArticleTarget.init","ext.echo.centralauth","ext.discussionTools.init","ext.eventLogging","ext.wikimediaEvents","ext.navigationTiming","ext.uls.compactlinks","ext.uls.interface","wikibase.databox.fromWikidata","ext.checkUser.clientHints","ext.readingLists.bookmark.anonymous","ext.dismissableSiteNotice"];</script>
<script>(RLQ=window.RLQ||[]).push(function(){mw.loader.impl(function(){return["user.options@12s5i",function($,jQuery,require,module){mw.user.tokens.set({"patrolToken":"+\\","watchToken":"+\\","csrfToken":"+\\"});
}];});});</script>
<link rel="stylesheet" href="/w/load.php?lang=en&amp;modules=ext.cite.styles%7Cext.discussionTools.init.styles%7Cext.dismissableSiteNotice.styles%7Cext.readingLists.bookmark.icons%2Cstyles%7Cext.uls.pt%7Cext.visualEditor.desktopArticleTarget.noscript%7Cext.wikimediamessages.styles%7Cmediawiki.widgets.styles%7Coojs-ui-core.icons%2Cstyles%7Coojs-ui.styles.indicators%7Cskins.vector.icons%2Cstyles%7Cskins.vector.search.codex.styles%7Cwikibase.client.init&amp;only=styles&amp;skin=vector-2022">
<script async="" src="/w/load.php?lang=en&amp;modules=startup&amp;only=scripts&amp;raw=1&amp;skin=vector-2022"></script>
<meta name="ResourceLoaderDynamicStyles" content="">
<link rel="stylesheet" href="/w/load.php?lang=en&amp;modules=site.styles&amp;only=styles&amp;skin=vector-2022">
<meta name="generator" content="MediaWiki 1.48.0-wmf.3">
<meta name="referrer" content="origin">
<meta name="referrer" content="origin-when-cross-origin">
<meta name="robots" content="max-image-preview:standard">
<meta name="format-detection" content="telephone=no">
<meta name="viewport" content="width=1120">
<meta property="og:site_name" content="MediaWiki">
<meta property="og:title" content="Wikimedia APIs/Rate limits - MediaWiki">
<meta property="og:type" content="website">
<link rel="preconnect" href="//thumb.wikimedia.org">
<link rel="apple-touch-icon" href="/static/apple-touch/mediawiki.png">
<link rel="icon" href="/static/favicon/mediawiki.ico">
<link rel="search" type="application/opensearchdescription+xml" href="/w/rest.php/v1/search" title="MediaWiki (en)">
<link rel="EditURI" type="application/rsd+xml" href="//www.mediawiki.org/w/api.php?action=rsd">
<link rel="canonical" href="https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits">
<link rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
<link rel="alternate" type="application/atom+xml" title="MediaWiki Atom feed" href="/w/index.php?title=Special:RecentChanges&amp;feed=atom">
<link rel="dns-prefetch" href="//meta.wikimedia.org" />
<link rel="dns-prefetch" href="auth.wikimedia.org">
</head>
<body class="mediawiki ltr sitedir-ltr mw-hide-empty-elt action-view ext-discussiontools-replytool-enabled ext-discussiontools-newtopictool-enabled ext-discussiontools-sourcemodetoolbar-enabled skin-vector-2022 ns-0 ns-subject page-Wikimedia_APIs_Rate_limits rootpage-Wikimedia_APIs skin--responsive skin-vector skin-vector-search-vue">
<div id="mw-aria-live-region" class="mw-aria-live-region" aria-live="polite"></div><a class="mw-jump-link" href="#bodyContent">Jump to content</a>
<div class="vector-header-container">
	<header class="vector-header mw-header no-font-mode-scale">
		<div class="vector-header-start">
			<nav class="vector-main-menu-landmark" aria-label="Site">
				
<div id="vector-main-menu-dropdown" class="vector-dropdown vector-main-menu-dropdown vector-button-flush-left vector-button-flush-right"  title="Main menu" >
	<input type="checkbox" id="vector-main-menu-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-main-menu-dropdown" class="vector-dropdown-checkbox "  aria-label="Main menu"   >
	<label id="vector-main-menu-dropdown-label" for="vector-main-menu-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-menu mw-ui-icon-wikimedia-menu cdx-button__icon"></span>

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
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-main-menu.pin" aria-label="Move Main menu to sidebar">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-main-menu.unpin" aria-label="Hide Main menu">hide</button>
</div>

	
<div id="p-navigation" class="vector-menu mw-portlet mw-portlet-navigation"  >
	<div class="vector-menu-heading">
		Navigation
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="n-mainpage-description" class="mw-list-item"><a href="/wiki/MediaWiki" title="Visit the main page [z]" accesskey="z"><span>Main page</span></a></li><li id="n-mw-download" class="mw-list-item"><a href="/wiki/Download"><span>Get MediaWiki</span></a></li><li id="n-mw-extensions" class="mw-list-item"><a href="/wiki/Special:MyLanguage/Category:Extensions"><span>Get extensions</span></a></li><li id="n-blog-text" class="mw-list-item"><a href="https://diff.wikimedia.org/tech-blog/"><span>Tech blog</span></a></li><li id="n-mw-contribute" class="mw-list-item"><a href="/wiki/Special:MyLanguage/How_to_contribute"><span>Contribute</span></a></li>
		</ul>
		
	</div>
</div>

	
<div id="p-support" class="vector-menu mw-portlet mw-portlet-support"  >
	<div class="vector-menu-heading">
		Support
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="n-help" class="mw-list-item"><a href="/wiki/Special:MyLanguage/Help:Contents" title="The place to find out"><span>User help</span></a></li><li id="n-mw-faq" class="mw-list-item"><a href="/wiki/Special:MyLanguage/Manual:FAQ"><span>FAQ</span></a></li><li id="n-mw-manual" class="mw-list-item"><a href="/wiki/Special:MyLanguage/Manual:Contents"><span>Technical manual</span></a></li><li id="n-mw-supportdesk" class="mw-list-item"><a href="/wiki/Project:Support_desk"><span>Support desk</span></a></li><li id="n-mw-communication" class="mw-list-item"><a href="/wiki/Special:MyLanguage/Communication"><span>Communication</span></a></li>
		</ul>
		
	</div>
</div>

<div id="p-development" class="vector-menu mw-portlet mw-portlet-development"  >
	<div class="vector-menu-heading">
		Development
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="n-mw-developerportal" class="mw-list-item"><a href="https://developer.wikimedia.org/"><span>Developer portal</span></a></li><li id="n-svn_statistics" class="mw-list-item"><a href="/wiki/Special:MyLanguage/Development_statistics"><span>Code statistics</span></a></li>
		</ul>
		
	</div>
</div>

<div id="p-mediawiki.org" class="vector-menu mw-portlet mw-portlet-mediawiki_org"  >
	<div class="vector-menu-heading">
		mediawiki.org
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="n-portal" class="mw-list-item"><a href="/wiki/Project:Help" title="About the project, what you can do, where to find things"><span>Community portal</span></a></li><li id="n-recentchanges" class="mw-list-item"><a href="/wiki/Special:RecentChanges" title="A list of recent changes in the wiki [r]" accesskey="r"><span>Recent changes</span></a></li><li id="n-mw-translate" class="mw-list-item"><a href="/wiki/Special:LanguageStats"><span>Translate content</span></a></li><li id="n-specialpages" class="mw-list-item"><a href="/wiki/Special:SpecialPages" title="A list of all special pages [q]" accesskey="q"><span>Special pages</span></a></li><li id="n-randompage" class="mw-list-item"><a href="/wiki/Special:Random" title="Load a random page [x]" accesskey="x"><span>Random page</span></a></li><li id="n-mw-discussion" class="mw-list-item"><a href="/wiki/Project:Village_Pump"><span>Village pump</span></a></li><li id="n-sandboxlink-portlet-label" class="mw-list-item"><a href="/wiki/Project:Sandbox"><span>Sandbox</span></a></li>
		</ul>
		
	</div>
</div>

	
<div id="p-lang" class="vector-menu mw-portlet mw-portlet-lang"  >
	<div class="vector-menu-heading">
		In other languages
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			
		</ul>
		<div class="after-portlet after-portlet-lang"><span class="wb-langlinks-add wb-langlinks-link"><a href="https://www.wikidata.org/wiki/Special:NewItem?site=mediawikiwiki&amp;page=Wikimedia+APIs%2FRate+limits" title="Add interlanguage links" class="wbc-editpage">Add links</a></span></div>
	</div>
</div>

</div>

				</div>

	</div>
</div>

		</nav>
			
<a href="/wiki/MediaWiki" class="mw-logo">
	<img class="mw-logo-icon" src="/static/images/icons/mediawikiwiki.svg" alt="" aria-hidden="true" height="50" width="50">
	<span class="mw-logo-container skin-invert">
		<img class="mw-logo-wordmark" alt="MediaWiki" src="/static/images/mobile/copyright/mediawikiwiki-wordmark.svg" style="width: 7.5em; height: 1.125em;">
	</span>
</a>

		</div>
		<div class="vector-header-end">
			
<div id="p-search" role="search" class="vector-search-box-vue  vector-search-box-collapses vector-search-box-show-thumbnail vector-search-box-auto-expand-width vector-search-box">
	<a href="/wiki/Special:Search" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only search-toggle" title="Search MediaWiki [f]" accesskey="f"><span class="vector-icon mw-ui-icon-search mw-ui-icon-wikimedia-search cdx-button__icon"></span>

<span>Search</span>
	</a>
	<div class="vector-typeahead-search-container">
		<div class="cdx-typeahead-search cdx-typeahead-search--show-thumbnail cdx-typeahead-search--auto-expand-width">
			<form action="/w/index.php" id="searchform" class="cdx-search-input cdx-search-input--has-end-button">
				<div id="simpleSearch" class="cdx-search-input__input-wrapper"  data-search-loc="header-moved">
					<div class="cdx-text-input cdx-text-input--has-start-icon">
						<input
							class="cdx-text-input__input mw-searchInput" autocomplete="off"
							 type="search" name="search" placeholder="Search mediawiki.org" aria-label="Search mediawiki.org" autocapitalize="none" spellcheck="false" title="Search MediaWiki [f]" accesskey="f" id="searchInput"
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
	
<div id="p-vector-user-menu-preferences" class="vector-menu mw-portlet"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			<li id="ca-uls" class="mw-list-item active vector-menu-item--collapsible"><a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet uls-trigger" id=""><span class="vector-icon mw-ui-icon-wikimedia-language mw-ui-icon-wikimedia-wikimedia-language cdx-button__icon"></span>

<span>English</span>
</a>
</li>

			
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
	<input type="checkbox" id="vector-appearance-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-appearance-dropdown" class="vector-dropdown-checkbox "  aria-label="Appearance"   >
	<label id="vector-appearance-dropdown-label" for="vector-appearance-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-appearance mw-ui-icon-wikimedia-appearance cdx-button__icon"></span>

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
			<li id="pt-sitesupport-2" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="https://donate.wikimedia.org/?wmf_source=donate&amp;wmf_medium=sidebar&amp;wmf_campaign=www.mediawiki.org&amp;uselang=en" data-mw-donate-attempt="top_link" class=""><span>Donate</span></a>
</li>
<li id="pt-createaccount-2" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="/w/index.php?title=Special:CreateAccount&amp;returnto=Wikimedia+APIs%2FRate+limits" title="You are encouraged to create an account and log in; however, it is not mandatory" class=""><span>Create account</span></a>
</li>
<li id="pt-login-2" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="/w/index.php?title=Special:UserLogin&amp;returnto=Wikimedia+APIs%2FRate+limits" title="You are encouraged to log in; however, it is not mandatory [o]" accesskey="o" class=""><span>Log in</span></a>
</li>

			
		</ul>
		
	</div>
</div>

	</div>
	
<div id="vector-user-links-dropdown" class="vector-dropdown vector-user-menu vector-button-flush-right vector-user-menu-logged-out vector-user-links-dropdown--collapsible"  title="More options" >
	<input type="checkbox" id="vector-user-links-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-user-links-dropdown" class="vector-dropdown-checkbox "  aria-label="Personal tools"   >
	<label id="vector-user-links-dropdown-label" for="vector-user-links-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-userAvatar mw-ui-icon-wikimedia-userAvatar cdx-button__icon"></span>

<span class="vector-dropdown-label-text">Personal tools</span>
	</label>
	<div class="vector-dropdown-content">


		
<div id="p-personal" class="vector-menu mw-portlet mw-portlet-personal"  title="User menu" >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			<li id="pt-sitesupport" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="https://donate.wikimedia.org/?wmf_source=donate&amp;wmf_medium=sidebar&amp;wmf_campaign=www.mediawiki.org&amp;uselang=en" data-mw-donate-attempt="top_link" class=""><span class="vector-icon mw-ui-icon-heart mw-ui-icon-wikimedia-heart cdx-button__icon"></span>

<span>Donate</span></a>
</li>
<li id="pt-createaccount" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="/w/index.php?title=Special:CreateAccount&amp;returnto=Wikimedia+APIs%2FRate+limits" title="You are encouraged to create an account and log in; however, it is not mandatory" class=""><span class="vector-icon mw-ui-icon-userAvatar mw-ui-icon-wikimedia-userAvatar cdx-button__icon"></span>

<span>Create account</span></a>
</li>
<li id="pt-login" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="/w/index.php?title=Special:UserLogin&amp;returnto=Wikimedia+APIs%2FRate+limits" title="You are encouraged to log in; however, it is not mandatory [o]" accesskey="o" class=""><span class="vector-icon mw-ui-icon-logIn mw-ui-icon-wikimedia-logIn cdx-button__icon"></span>

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
			<div id="siteNotice"><div id="mw-dismissablenotice-anonplace"></div><script>(function(){var node=document.getElementById("mw-dismissablenotice-anonplace");if(node){node.outerHTML="\u003Cdiv class=\"mw-dismissable-notice\"\u003E\u003Cdiv class=\"mw-dismissable-notice-close\"\u003E[\u003Ca tabindex=\"0\" role=\"button\"\u003Edismiss\u003C/a\u003E]\u003C/div\u003E\u003Cdiv class=\"mw-dismissable-notice-body\"\u003E\u003C!-- CentralNotice --\u003E\u003Cdiv id=\"localNotice\" data-nosnippet=\"\"\u003E\u003Cdiv class=\"sitenotice\" lang=\"en\" dir=\"ltr\"\u003E\u003Cdiv style=\"margin: 0.5em 0; padding: 15px; border: 2px solid var(--color-placeholder, black); display: flex; align-items: center; justify-content: space-between; gap: 15px;\" class=\"plainlinks\"\u003E\n\u003Cdiv style=\"flex-shrink: 0;\"\u003E\n\u003Cfigure class=\"mw-halign-none skin-invert\" typeof=\"mw:File\"\u003E\u003Ca href=\"/wiki/MediaWiki_Users_and_Developers_Conference_Fall_2026\" title=\"MediaWiki Users and Developers Conference Fall 2026\"\u003E\u003Cimg src=\"//thumb.wikimedia.org/wikipedia/commons/thumb/7/71/MediaWikiUsersDevelopersConferenceWordmark.png/120px-MediaWikiUsersDevelopersConferenceWordmark.png?utm_source=www.mediawiki.org\u0026amp;utm_campaign=parser\u0026amp;utm_content=thumbnail\" decoding=\"async\" loading=\"lazy\" width=\"120\" height=\"53\" class=\"mw-file-element\" srcset=\"//thumb.wikimedia.org/wikipedia/commons/thumb/7/71/MediaWikiUsersDevelopersConferenceWordmark.png/250px-MediaWikiUsersDevelopersConferenceWordmark.png?utm_source=www.mediawiki.org\u0026amp;utm_campaign=parser\u0026amp;utm_content=thumbnail 2x\" data-file-width=\"1080\" data-file-height=\"480\"/\u003E\u003C/a\u003E\u003Cfigcaption\u003E\u003C/figcaption\u003E\u003C/figure\u003E\n\u003C/div\u003E\n\u003Cdiv style=\"flex-grow: 1; text-align: center;\"\u003E\n\u003Cp\u003EThe \u003Ca href=\"/wiki/MediaWiki_Users_and_Developers_Conference_Fall_2026\" title=\"MediaWiki Users and Developers Conference Fall 2026\"\u003EMediaWiki Users and Developers Conference Fall 2026\u003C/a\u003E will take place November 11-13 in \u003Ca href=\"https://en.wikipedia.org/wiki/Ljubljana\" class=\"extiw\" title=\"w:Ljubljana\"\u003ELjubljana\u003C/a\u003E, \u003Ca href=\"https://en.wikipedia.org/wiki/Slovenia\" class=\"extiw\" title=\"w:Slovenia\"\u003ESlovenia\u003C/a\u003E. \u003Ca rel=\"nofollow\" class=\"external text\" href=\"https://luma.com/0ifiue5f\"\u003E\u003Cb\u003ERegister for the conference\u003C/b\u003E\u003C/a\u003E today!\n\u003C/p\u003E\n\u003C/div\u003E\n\u003Cdiv style=\"clear: both;\"\u003E\u003C/div\u003E\n\u003C/div\u003E\u003C/div\u003E\u003C/div\u003E\u003C/div\u003E\u003C/div\u003E";}}());</script></div>
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
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-toc.pin" aria-label="Move Contents to sidebar">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-toc.unpin" aria-label="Hide Contents">hide</button>
</div>


	<ul class="vector-toc-contents" id="mw-panel-toc-list">
		<li id="toc-mw-content-text"
			class="vector-toc-list-item vector-toc-level-1">
			<a href="#" class="vector-toc-link">
				<div class="vector-toc-text">Beginning</div>
			</a>
		</li>
		<li id="toc-Rationale"
		class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-expanded">
		<a class="vector-toc-link" href="#Rationale">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">1</span>
				<span>Rationale</span>
			</div>
		</a>
		
		<ul id="toc-Rationale-sublist" class="vector-toc-list">
		</ul>
	</li>
	<li id="toc-Best_practices"
		class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-expanded">
		<a class="vector-toc-link" href="#Best_practices">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">2</span>
				<span>Best practices</span>
			</div>
		</a>
		
		<ul id="toc-Best_practices-sublist" class="vector-toc-list">
		</ul>
	</li>
	<li id="toc-Limits"
		class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-expanded">
		<a class="vector-toc-link" href="#Limits">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">3</span>
				<span>Limits</span>
			</div>
		</a>
		
			<button aria-controls="toc-Limits-sublist" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only vector-toc-toggle">
				<span class="vector-icon mw-ui-icon-wikimedia-expand"></span>
				<span>Toggle Limits subsection</span>
			</button>
		
		<ul id="toc-Limits-sublist" class="vector-toc-list">
			<li id="toc-Action-based_rate_limits"
			class="vector-toc-list-item vector-toc-level-2">
			<a class="vector-toc-link" href="#Action-based_rate_limits">
				<div class="vector-toc-text">
					<span class="vector-toc-numb">3.1</span>
					<span>Action-based rate limits</span>
				</div>
			</a>
			
			<ul id="toc-Action-based_rate_limits-sublist" class="vector-toc-list">
			</ul>
		</li>
	</ul>
	</li>
	<li id="toc-Errors"
		class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-expanded">
		<a class="vector-toc-link" href="#Errors">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">4</span>
				<span>Errors</span>
			</div>
		</a>
		
		<ul id="toc-Errors-sublist" class="vector-toc-list">
		</ul>
	</li>
	<li id="toc-Caveats"
		class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-expanded">
		<a class="vector-toc-link" href="#Caveats">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">5</span>
				<span>Caveats</span>
			</div>
		</a>
		
		<ul id="toc-Caveats-sublist" class="vector-toc-list">
		</ul>
	</li>
	<li id="toc-Get_help"
		class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-expanded">
		<a class="vector-toc-link" href="#Get_help">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">6</span>
				<span>Get help</span>
			</div>
		</a>
		
		<ul id="toc-Get_help-sublist" class="vector-toc-list">
		</ul>
	</li>
	<li id="toc-See_also"
		class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-expanded">
		<a class="vector-toc-link" href="#See_also">
			<div class="vector-toc-text">
				<span class="vector-toc-numb">7</span>
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
	<input type="checkbox" id="vector-page-titlebar-toc-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-page-titlebar-toc" class="vector-dropdown-checkbox "  aria-label="Toggle the table of contents"   >
	<label id="vector-page-titlebar-toc-label" for="vector-page-titlebar-toc-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-listBullet mw-ui-icon-wikimedia-listBullet cdx-button__icon"></span>

<span class="vector-dropdown-label-text">Toggle the table of contents</span>
	</label>
	<div class="vector-dropdown-content">


							<div id="vector-page-titlebar-toc-unpinned-container" class="vector-unpinned-container">
			</div>
		
	</div>
</div>

					</nav>
					<h1 id="firstHeading" class="firstHeading mw-first-heading"><span lang="en" dir="ltr"><span class="mw-page-title-main">Wikimedia APIs/Rate limits</span></span></h1>
		<div class="mw-indicators">
	</div>
</header>
				<div class="vector-page-toolbar">
					<div class="vector-page-toolbar-container">
						<div id="left-navigation">
							<nav aria-label="Namespaces">
								
<div id="p-associated-pages" class="vector-menu vector-menu-tabs mw-portlet mw-portlet-associated-pages"  >
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			<li id="ca-nstab-main" class="selected mw-list-item vector-tab-noicon"><a data-mw-interface  href="/wiki/Wikimedia_APIs/Rate_limits" title="View the content page [c]" accesskey="c" class=""><span>Page</span></a>
</li>
<li id="ca-talk" class="mw-list-item vector-tab-noicon"><a data-mw-interface  href="/wiki/Talk:Wikimedia_APIs/Rate_limits" rel="discussion" title="Discussion about the content page [t]" accesskey="t" class=""><span>Discussion</span></a>
</li>

			
		</ul>
		
	</div>
</div>

								
<div id="vector-variants-dropdown" class="vector-dropdown emptyPortlet"  >
	<input type="checkbox" id="vector-variants-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-variants-dropdown" class="vector-dropdown-checkbox " aria-label="Change language variant"    >
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
			<li id="ca-view" class="selected mw-list-item vector-menu-item--collapsible vector-tab-noicon"><a data-mw-interface  href="/wiki/Wikimedia_APIs/Rate_limits" class=""><span>Read</span></a>
</li>
<li id="ca-viewsource" class="mw-list-item vector-menu-item--collapsible vector-tab-noicon"><a data-mw-interface  href="/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;action=edit" title="This page is protected.
You can view its source [e]" accesskey="e" class=""><span>View source</span></a>
</li>
<li id="ca-history" class="mw-list-item vector-menu-item--collapsible vector-tab-noicon"><a data-mw-interface  href="/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;action=history" title="Past revisions of this page [h]" accesskey="h" class=""><span>View history</span></a>
</li>
<li id="ca-bookmark" class="mw-list-item vector-menu-item--collapsible"><a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only reading-lists-bookmark" id="" title="Add this page to your saved items"><span class="vector-icon mw-ui-icon-bookmarkOutline mw-ui-icon-wikimedia-bookmarkOutline cdx-button__icon"></span>

<span>Save</span>
</a>
</li>

			
		</ul>
		
	</div>
</div>

			</nav>

							<nav class="vector-page-tools-landmark" aria-label="Page tools">
								
<div id="vector-page-tools-dropdown" class="vector-dropdown vector-page-tools-dropdown"  >
	<input type="checkbox" id="vector-page-tools-dropdown-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-page-tools-dropdown" class="vector-dropdown-checkbox "  aria-label="Tools"   >
	<label id="vector-page-tools-dropdown-label" for="vector-page-tools-dropdown-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-verticalEllipsis mw-ui-icon-wikimedia-verticalEllipsis cdx-button__icon"></span>

<span class="vector-dropdown-label-text">Tools</span>
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
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-page-tools.pin" aria-label="Move Tools to sidebar">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-page-tools.unpin" aria-label="Hide Tools">hide</button>
</div>

	
<div id="p-cactions" class="vector-menu mw-portlet mw-portlet-cactions emptyPortlet vector-has-collapsible-items"  >
	<div class="vector-menu-heading">
		Actions
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			<li id="ca-view-more" class="selected mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="/wiki/Wikimedia_APIs/Rate_limits" class=""><span class="vector-icon mw-ui-icon-eye mw-ui-icon-wikimedia-eye cdx-button__icon"></span>

<span>Read</span></a>
</li>
<li id="ca-viewsource-more" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;action=edit" title="This page is protected.
You can view its source [e]" accesskey="e" class=""><span class="vector-icon mw-ui-icon-editLock mw-ui-icon-wikimedia-editLock cdx-button__icon"></span>

<span>View source</span></a>
</li>
<li id="ca-history-more" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;action=history" title="Past revisions of this page [h]" accesskey="h" class=""><span class="vector-icon mw-ui-icon-history mw-ui-icon-wikimedia-history cdx-button__icon"></span>

<span>View history</span></a>
</li>
<li id="ca-bookmark-more" class="mw-list-item vector-menu-item--collapsible"><a data-mw-interface  href="#" class="reading-lists-bookmark" title="Add this page to your saved items"><span class="vector-icon mw-ui-icon-bookmarkOutline mw-ui-icon-wikimedia-bookmarkOutline cdx-button__icon"></span>

<span>Save</span></a>
</li>

			
		</ul>
		
	</div>
</div>

<div id="p-tb" class="vector-menu mw-portlet mw-portlet-tb"  >
	<div class="vector-menu-heading">
		General
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="t-whatlinkshere" class="mw-list-item"><a href="/wiki/Special:WhatLinksHere/Wikimedia_APIs/Rate_limits" title="A list of all wiki pages that link here [j]" accesskey="j"><span>What links here</span></a></li><li id="t-recentchangeslinked" class="mw-list-item"><a href="/wiki/Special:RecentChangesLinked/Wikimedia_APIs/Rate_limits" rel="nofollow" title="Recent changes in pages linked from this page [k]" accesskey="k"><span>Related changes</span></a></li><li id="t-upload" class="mw-list-item"><a href="//commons.wikimedia.org/wiki/Special:UploadWizard" title="Upload files [u]" accesskey="u"><span>Upload file</span></a></li><li id="t-permalink" class="mw-list-item"><a href="/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;oldid=8654799" title="Permanent link to this revision of this page"><span>Permanent link</span></a></li><li id="t-info" class="mw-list-item"><a href="/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;action=info" title="More information about this page"><span>Page information</span></a></li><li id="t-cite" class="mw-list-item"><a href="/w/index.php?title=Special:CiteThisPage&amp;page=Wikimedia_APIs%2FRate_limits&amp;id=8654799&amp;wpFormIdentifier=titleform" title="Information on how to cite this page"><span>Cite this page</span></a></li><li id="t-urlshortener" class="mw-list-item"><a href="/w/index.php?title=Special:UrlShortener&amp;url=https%3A%2F%2Fwww.mediawiki.org%2Fwiki%2FWikimedia_APIs%2FRate_limits"><span>Get shortened URL</span></a></li>
		</ul>
		
	</div>
</div>

<div id="p-coll-print_export" class="vector-menu mw-portlet mw-portlet-coll-print_export"  >
	<div class="vector-menu-heading">
		Print/export
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			<li id="coll-create_a_book" class="mw-list-item"><a href="/w/index.php?title=Special:Book&amp;bookcmd=book_creator&amp;referer=Wikimedia+APIs%2FRate+limits"><span>Create a book</span></a></li><li id="coll-download-as-rl" class="mw-list-item"><a href="/w/index.php?title=Special:DownloadAsPdf&amp;page=Wikimedia_APIs%2FRate_limits&amp;action=show-download-screen"><span>Download as PDF</span></a></li><li id="t-print" class="mw-list-item"><a href="javascript:print();" rel="alternate" title="Printable version of this page [p]" accesskey="p"><span>Printable version</span></a></li>
		</ul>
		
	</div>
</div>

<div id="p-wikibase-otherprojects" class="vector-menu mw-portlet mw-portlet-wikibase-otherprojects emptyPortlet"  >
	<div class="vector-menu-heading">
		In other projects
	</div>
	<div class="vector-menu-content">
		
		<ul class="vector-menu-content-list">
			
			
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
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" data-event-name="pinnable-header.vector-appearance.pin" aria-label="Move Appearance to sidebar">move to sidebar</button>
	<button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" data-event-name="pinnable-header.vector-appearance.unpin" aria-label="Hide Appearance">hide</button>
</div>


</div>

							</div>
		</nav>
					</div>
				</div>
				<div id="bodyContent" class="vector-body" aria-labelledby="firstHeading" data-mw-ve-target-container>
					<div class="vector-body-before-content">
					
						<div id="siteSub" class="noprint">From mediawiki.org</div>
						<div id="contentSub"><div id="mw-content-subtitle"><div class="subpages">&lt; <bdi dir="ltr"><a href="/wiki/Wikimedia_APIs" title="Wikimedia APIs">Wikimedia APIs</a></bdi></div></div></div>
						
					</div>
					
					<div id="mw-content-text" class="mw-body-content"><div class="mw-content-ltr mw-parser-output" lang="en" dir="ltr"><style data-mw-deduplicate="TemplateStyles:r7036105">.mw-parser-output .nmbox{background:#f8f9fa;border:1px solid var(--border-color-base,#a2a9b1);box-sizing:border-box;margin:2px 0;padding:0}.mw-parser-output .nmbox *{box-sizing:border-box}.mw-parser-output .nmbox-header{background:#eaecf0;padding:4px 0.5em;font-weight:bold;text-align:center;white-space:nowrap}.mw-parser-output .nmbox .mbox-image{display:inline-block;padding-right:1em}.mw-parser-output .nmbox-text{border-top:1px solid var(--border-color-base,#a2a9b1);width:100%;padding:4px 0.5em}@media screen and (min-width:768px){.mw-parser-output .nmbox-header{display:table-cell;border-right:1px solid var(--border-color-base,#a2a9b1);width:1%}.mw-parser-output .nmbox-text{border-top:none;display:table-cell}}@media screen{html.skin-theme-clientpref-night .mw-parser-output .nmbox-header,html.skin-theme-clientpref-night .mw-parser-output .nmbox{background:transparent;color:inherit}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .nmbox-header,html.skin-theme-clientpref-os .mw-parser-output .nmbox{background:transparent;color:inherit}}</style>
<div class="nmbox noprint mw-content-ltr"><div class="nmbox-header"><div class="nmbox-image mbox-image"><span class="skin-invert" typeof="mw:File"><a href="/wiki/Wikimedia_APIs" title="Wikimedia APIs"><img src="//thumb.wikimedia.org/wikipedia/commons/thumb/8/8b/Wikimedia-logo_black.svg/20px-Wikimedia-logo_black.svg.png?utm_source=www.mediawiki.org&amp;utm_campaign=parser&amp;utm_content=thumbnail" decoding="async" loading="lazy" width="20" height="20" class="mw-file-element" srcset="//thumb.wikimedia.org/wikipedia/commons/thumb/8/8b/Wikimedia-logo_black.svg/40px-Wikimedia-logo_black.svg.png?utm_source=www.mediawiki.org&amp;utm_campaign=parser&amp;utm_content=thumbnail 2x" data-file-width="512" data-file-height="512"></a></span></div><b><a href="/wiki/Special:MyLanguage/Wikimedia_APIs" title="Special:MyLanguage/Wikimedia APIs">Wikimedia APIs</a><span style="display:none"><a href="/wiki/Wikimedia_APIs" title="Wikimedia APIs"> </a></span></b>
</div>
<div class="nmbox-text mbox-text"><style data-mw-deduplicate="TemplateStyles:r6387430">.mw-parser-output .hlist dl,.mw-parser-output .hlist ol,.mw-parser-output .hlist ul{margin:0;padding:0}.mw-parser-output .hlist dd,.mw-parser-output .hlist dt,.mw-parser-output .hlist li{margin:0;display:inline}.mw-parser-output .hlist dl dl,.mw-parser-output .hlist dl ol,.mw-parser-output .hlist dl ul,.mw-parser-output .hlist ol dl,.mw-parser-output .hlist ol ol,.mw-parser-output .hlist ol ul,.mw-parser-output .hlist ul dl,.mw-parser-output .hlist ul ol,.mw-parser-output .hlist ul ul{display:inline}.mw-parser-output .hlist .mw-empty-li,.mw-parser-output .hlist .mw-empty-elt{display:none}.mw-parser-output .hlist dt:after{content:": "}.mw-parser-output .hlist dd:after,.mw-parser-output .hlist li:after{content:" · ";font-weight:bold}.mw-parser-output .hlist dd:last-child:after,.mw-parser-output .hlist dt:last-child:after,.mw-parser-output .hlist li:last-child:after{content:none}.mw-parser-output .hlist dd dd:first-child:before,.mw-parser-output .hlist dd dt:first-child:before,.mw-parser-output .hlist dd li:first-child:before,.mw-parser-output .hlist dt dd:first-child:before,.mw-parser-output .hlist dt dt:first-child:before,.mw-parser-output .hlist dt li:first-child:before,.mw-parser-output .hlist li dd:first-child:before,.mw-parser-output .hlist li dt:first-child:before,.mw-parser-output .hlist li li:first-child:before{content:" (";font-weight:normal}.mw-parser-output .hlist dd dd:last-child:after,.mw-parser-output .hlist dd dt:last-child:after,.mw-parser-output .hlist dd li:last-child:after,.mw-parser-output .hlist dt dd:last-child:after,.mw-parser-output .hlist dt dt:last-child:after,.mw-parser-output .hlist dt li:last-child:after,.mw-parser-output .hlist li dd:last-child:after,.mw-parser-output .hlist li dt:last-child:after,.mw-parser-output .hlist li li:last-child:after{content:")";font-weight:normal}.mw-parser-output .hlist ol{counter-reset:listitem}.mw-parser-output .hlist ol>li{counter-increment:listitem}.mw-parser-output .hlist ol>li:before{content:" "counter(listitem)"\a0 "}.mw-parser-output .hlist dd ol>li:first-child:before,.mw-parser-output .hlist dt ol>li:first-child:before,.mw-parser-output .hlist li ol>li:first-child:before{content:" ("counter(listitem)"\a0 "}</style><div class="hlist">
<ul><li><a href="/wiki/Special:RestSandbox" title="Special:RestSandbox">Sandbox</a></li>
<li><a href="/wiki/Special:MyLanguage/Wikimedia_APIs/Access_policy" title="Special:MyLanguage/Wikimedia APIs/Access policy">Access policy</a><span style="display:none"><a href="/wiki/Wikimedia_APIs/Access_policy" title="Wikimedia APIs/Access policy"> </a></span></li>
<li><a href="/wiki/Special:MyLanguage/Wikimedia_APIs/Content_reuse" title="Special:MyLanguage/Wikimedia APIs/Content reuse">Content reuse</a><span style="display:none"><a href="/wiki/Wikimedia_APIs/Content_reuse" title="Wikimedia APIs/Content reuse"> </a></span></li>
<li><a href="/wiki/Special:MyLanguage/Wikimedia_APIs/Tools_and_bots" title="Special:MyLanguage/Wikimedia APIs/Tools and bots">Tools and bots</a><span style="display:none"><a href="/wiki/Wikimedia_APIs/Tools_and_bots" title="Wikimedia APIs/Tools and bots"> </a></span></li>
<li><a href="/wiki/Special:MyLanguage/Wikimedia_APIs/Changelog" title="Special:MyLanguage/Wikimedia APIs/Changelog">Changelog</a><span style="display:none"><a href="/wiki/Wikimedia_APIs/Changelog" title="Wikimedia APIs/Changelog"> </a></span></li></ul>
</div></div>
</div>
<p>Requests to Wikimedia APIs are subject to <b>rate limiting</b> to protect Wikimedia infrastructure from overloading and to ensure fair access to resources for all clients. Rate limits apply across all sites and platforms, including requests to the <a href="/wiki/API:Action_API" title="API:Action API">Action API</a> and <a href="/wiki/Wikimedia_REST_API" title="Wikimedia REST API">REST APIs</a>, and are enforced per user.
</p>
<style data-mw-deduplicate="TemplateStyles:r6651107">.mw-parser-output .note{background-position:left 7px top 50%;padding:0.5em 0.5em 0.5em 40px;margin:0.5em 0;overflow:hidden;background-color:#f8f9fa;color:#333;background-repeat:no-repeat;border:1px solid #ddd}.mw-parser-output .note-inline{display:inline-block;vertical-align:middle}.mw-parser-output .note-info{background-color:#eaf3ff;color:#333;background-image:url("https://upload.wikimedia.org/wikipedia/commons/e/ec/OOjs_UI_icon_information-progressive.svg");background-size:25px;border-color:#a3caff;padding-left:40px;min-height:25px}.mw-parser-output .note-reminder{background-color:#fff9ea;color:#333;background-image:url("https://upload.wikimedia.org/wikipedia/commons/a/a8/OOjs_UI_icon_lightbulb-yellow.svg");background-size:25px;border-color:#fc3;min-height:25px}.mw-parser-output .note-warn{background-color:#fff9ea;color:#333;background-image:url("https://upload.wikimedia.org/wikipedia/commons/3/3b/OOjs_UI_icon_alert-warning.svg");background-size:25px;border-color:#fc3;min-height:25px}.mw-parser-output .note-error{background-color:#fee7e6;color:#333;background-image:url("https://upload.wikimedia.org/wikipedia/commons/b/bf/OOjs_UI_icon_notice-destructive.svg");background-size:25px;border-color:#c33;min-height:25px}@media screen{html.skin-theme-clientpref-night .mw-parser-output .note{background-color:transparent;color:inherit}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .note{background-color:transparent;color:inherit}}</style><div role="note" class="note note-info">The rate limits described on this page are new in 2026 and are subject to experimentation and change.</div>
<meta property="mw:PageProp/toc">
<div class="mw-heading mw-heading2 ext-discussiontools-init-section"><h2 id="Rationale" data-mw-thread-id="h-Rationale"><span data-mw-comment-start="" id="h-Rationale"></span>Rationale<span data-mw-comment-end="h-Rationale"></span></h2></div>
<p>API rate limits are being deployed in 2026 to ensure <a href="/wiki/MediaWiki_Product_Insights/Responsible_Reuse" title="MediaWiki Product Insights/Responsible Reuse">fair and sustainable access</a> to Wikimedia resources. The goal is to reduce the amount of unauthenticated, automated API requests (about 33% at the end of 2025) and to prevent high-volume commercial consumers from putting <a href="https://diff.wikimedia.org/2025/04/01/how-crawlers-impact-the-operations-of-the-wikimedia-projects/" class="extiw" title="diffblog:2025/04/01/how-crawlers-impact-the-operations-of-the-wikimedia-projects/">undue load</a> on our infrastructure. 
</p><p>Ideally, members of Wikimedia communities will not be affected by this change. They may even benefit from the fact that fewer resources are being used by commercial consumers. However, it is possible that a small number of bots and other tools which operate at a very high rate may get rate limited. To avoid being impacted by rate limits, follow the best practices below.
</p>
<div class="mw-heading mw-heading2 ext-discussiontools-init-section"><h2 id="Best_practices" data-mw-thread-id="h-Best_practices"><span data-mw-comment-start="" id="h-Best_practices"></span>Best practices<span data-mw-comment-end="h-Best_practices"></span></h2></div>
<p>To avoid being rate limited, clients should follow these best practices and the rules in the <a href="https://wikitech.wikimedia.org/wiki/Robot_policy" class="extiw" title="wikitech:Robot policy">robot policy</a>. In particular, clients should:
</p>
<ul><li>include a meaningful User-Agent header that includes contact information such as an email or full URL. For example: <code>CoolBot/0.0 (https://example.org/coolbot/; [email withheld by Lighthouse]) generic-library/0.0</code>. For more information, see the <a href="https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy" class="extiw" title="foundation:Policy:Wikimedia Foundation User-Agent Policy">User-Agent policy</a>.</li>
<li>implement cookie support when using <a href="/wiki/Manual:Bot_passwords" title="Manual:Bot passwords">bot passwords</a> or <a href="/wiki/OAuth/For_Developers" title="OAuth/For Developers">OAuth</a> to authenticate. However, <a href="/wiki/OAuth/For_Developers#Authorisation_2" title="OAuth/For Developers">multi-user OAuth 2 apps</a> should not send cookies.</li>
<li>limit the number of concurrent requests to 3 or fewer.</li>
<li>follow API-specific guidelines, such as <a href="/wiki/API:Etiquette" title="API:Etiquette">Action API etiquette</a>.</li>
<li>respect the Retry-After header provided with a 429 Too Many Requests status code.</li></ul>
<p>Community members that need a higher rate of access should:
</p>
<ul><li>request the <a href="/wiki/Manual:Bots" title="Manual:Bots">bot flag</a> from your local wiki community. Community-approved bots get higher rate limits.</li>
<li>where appropriate, consider running your bot in Toolforge or another <a href="https://wikitech.wikimedia.org/wiki/Help:Cloud_Services_introduction" class="extiw" title="wikitech:Help:Cloud Services introduction">Wikimedia Cloud Services</a> offering.</li></ul>
<p>If you require high-volume, commercial access:
</p>
<ul><li><a class="external text" href="https://enterprise.wikimedia.com/">Wikimedia Enterprise</a> APIs are available with free access for all users up to certain speed and volume limits.</li>
<li><a class="external text" href="https://enterprise.wikimedia.com/pricing/">commercial rates</a> are offered for those who require higher speed, volumes or SLA requirements.</li></ul>
<div class="mw-heading mw-heading2 ext-discussiontools-init-section"><h2 id="Limits" data-mw-thread-id="h-Limits"><span data-mw-comment-start="" id="h-Limits"></span>Limits<span data-mw-comment-end="h-Limits"></span></h2></div>
<p>Rate limits take into account the client's identity and level of access. Below is an overview of rate limits grouped by the type of client (<a class="mw-selflink-fragment" href="#Caveats">caveats</a> apply). They are enforced per-minute to help to smooth out API traffic and minimize the impact on any user that inadvertently hits a rate limit. Limits have been set at a level that is high enough to still allow for short bursts of requests.
</p>
<table class="wikitable">
<tbody><tr>
<th>Group
</th>
<th>Description
</th>
<th>Limit (req/min)
</th></tr>
<tr>
<td rowspan="2">Unidentified
</td>
<td>Requests with no identifying characteristics other than IP address
</td>
<td>10
</td></tr>
<tr>
<td>Requests made from a web browser by an unauthenticated user
</td>
<td>200
</td></tr>
<tr>
<td rowspan="2">User-Agent only
</td>
<td>Unauthenticated bot requests with a <a href="https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy" class="extiw" title="foundation:Policy:Wikimedia Foundation User-Agent Policy">compliant User-Agent</a> header
</td>
<td>200
</td></tr>
<tr>
<td>Requests from third-party MediaWiki wikis (for example via <a href="/wiki/InstantCommons" title="InstantCommons">InstantCommons</a>)
</td>
<td>200
</td></tr>
<tr>
<td rowspan="4">Authenticated
</td>
<td>Authenticated requests from users who are new or have few edits
</td>
<td>200
</td></tr>
<tr>
<td>Authenticated requests from users who are established editors
</td>
<td>2000
</td></tr>
<tr>
<td>Authenticated requests from users with extended global rights (e.g. stewards)
</td>
<td>Exempt <sup id="cite_ref-exempt_1-0" class="reference"><a href="#cite_note-exempt-1"><span class="cite-bracket">[</span>limits 1<span class="cite-bracket">]</span></a></sup>
</td></tr>
<tr>
<td>Authenticated requests from bots accounts with a <a href="/wiki/Manual:Bots" title="Manual:Bots">bot flag</a> on any wiki
</td>
<td>Exempt <sup id="cite_ref-exempt_1-1" class="reference"><a href="#cite_note-exempt-1"><span class="cite-bracket">[</span>limits 1<span class="cite-bracket">]</span></a></sup>
</td></tr>
<tr>
<td><a href="https://wikitech.wikimedia.org/wiki/Help:Cloud_Services_introduction" class="extiw" title="wikitech:Help:Cloud Services introduction">Wikimedia Cloud Services</a> (WMCS)
</td>
<td>Server-side requests from WMCS with a compliant User-Agent
</td>
<td>Exempt <sup id="cite_ref-exempt_1-2" class="reference"><a href="#cite_note-exempt-1"><span class="cite-bracket">[</span>limits 1<span class="cite-bracket">]</span></a></sup>
</td></tr>
<tr>
<td>Known client
</td>
<td>Requests from clients granted an exemption by the Wikimedia Foundation
</td>
<td>Exempt <sup id="cite_ref-exempt_1-3" class="reference"><a href="#cite_note-exempt-1"><span class="cite-bracket">[</span>limits 1<span class="cite-bracket">]</span></a></sup>
</td></tr></tbody></table>
<div class="mw-references-wrap"><ol class="references" data-mw-group="limits">
<li id="cite_note-exempt-1"><span class="mw-cite-backlink">↑ <sup><a href="#cite_ref-exempt_1-0">1.0</a></sup> <sup><a href="#cite_ref-exempt_1-1">1.1</a></sup> <sup><a href="#cite_ref-exempt_1-2">1.2</a></sup> <sup><a href="#cite_ref-exempt_1-3">1.3</a></sup></span> <span class="reference-text">Clients that are exempt from API rate limiting are still subject to <a href="https://wikitech.wikimedia.org/wiki/Requestctl" class="extiw" title="wikitech:Requestctl">operational rate limits</a> and the <a href="https://wikitech.wikimedia.org/wiki/Robot_policy" class="extiw" title="wikitech:Robot policy">Robot policy</a>.</span>
</li>
</ol></div>
<div class="mw-heading mw-heading3"><h3 id="Action-based_rate_limits" data-mw-thread-id="h-Action-based_rate_limits-Limits"><span data-mw-comment-start="" id="h-Action-based_rate_limits-Limits"></span>Action-based rate limits<span data-mw-comment-end="h-Action-based_rate_limits-Limits"></span></h3></div>
<p>In addition to limits based on client identity, actions (such as editing pages, moving pages, and uploading files) are rate limited to prevent vandalism and other harmful behaviors. Action-based limits depend on the status of the user account and on the policy of the individual wiki. For example, most Wikimedia projects limit logged-out users to eight edits per minute. To learn more about actions and specific limits, see <a href="/wiki/Manual:Rate_limits" title="Manual:Rate limits">Manual:Rate limits</a>.
</p>
<div class="mw-heading mw-heading2 ext-discussiontools-init-section"><h2 id="Errors" data-mw-thread-id="h-Errors"><span data-mw-comment-start="" id="h-Errors"></span>Errors<span data-mw-comment-end="h-Errors"></span></h2></div>
<p>When a client exceeds its rate limit, the gateway responds with HTTP status code <a href="https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#429" class="extiw" title="en:List of HTTP status codes">429 (Too Many Requests)</a>. Other components involved in handling the request may also respond with status 429 when per-client limits are exceeded, or with status <a href="https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#503" class="extiw" title="en:List of HTTP status codes">503 (Service Unavailable)</a> when a backend system such as a database server is overloaded.
</p><p>Responses with status code 429 or 503 typically also have the <a href="https://en.wikipedia.org/wiki/List_of_HTTP_header_fields#Response_fields" class="extiw" title="en:List of HTTP header fields">Retry-After header</a> set, indicating how long the client should wait until it retries the request. If no such header is present, clients should wait at least five seconds, or implement <a href="https://en.wikipedia.org/wiki/Exponential_backoff" class="extiw" title="en:Exponential backoff">exponential back-off</a>.
</p>
<div class="mw-heading mw-heading2 ext-discussiontools-init-section"><h2 id="Caveats" data-mw-thread-id="h-Caveats"><span data-mw-comment-start="" id="h-Caveats"></span>Caveats<span data-mw-comment-end="h-Caveats"></span></h2></div>
<p>Operators of API clients should be aware of the following edge cases and pitfalls:
</p>
<ul><li>The limits described above do not apply to the <a href="https://wikitech.wikimedia.org/wiki/Machine_Learning/LiftWing/API" class="extiw" title="wikitech:Machine Learning/LiftWing/API">Lift Wing API</a>. To learn about rate limits for the Lift Wing API, see the <a href="https://wikitech.wikimedia.org/wiki/Machine_Learning/LiftWing/API/External_usage#Rate_limits_for_external_usage" class="extiw" title="wikitech:Machine Learning/LiftWing/API/External usage">documentation on Wikitech</a>.</li>
<li><a href="/wiki/OAuth/For_Developers#OAuth_1.0a" title="OAuth/For Developers">OAuth 1</a> access tokens are not supported on their own by the rate limit infrastructure. Requests using OAuth 1 tokens will be treated as unauthenticated with respect to rate limiting, unless you also send cookies with the request.</li>
<li>Elevated rate limits embedded directly in some older <a href="/wiki/OAuth/Owner-only_consumers" title="OAuth/Owner-only consumers">owner-only</a> tokens are ignored by the new rate limiting infrastructure (but are still used for endpoints on api.wikimedia.org, see <a href="https://phabricator.wikimedia.org/T409305" class="extiw" title="phab:T409305">T409305</a>). Going forward, rate limits will be determined by a user's current privileges, not limits assigned at the time of token creation.</li>
<li>Generally, a <i>refresh-token flow</i> or <i>client-credentials flow</i> would be preferred over direct use of owner-only tokens for <a href="/wiki/OAuth/For_Developers#OAuth_2" title="OAuth/For Developers">OAuth 2.0</a>, but support for that is still limited (see <a href="https://phabricator.wikimedia.org/T407987" class="extiw" title="phab:T407987">T407987</a> and <a href="https://phabricator.wikimedia.org/T412214" class="extiw" title="phab:T412214">T412214</a> ). For now, clients should support session cookies to be used along with OAuth tokens. This allows the correct rate limit class to be applied.</li></ul>
<div class="mw-heading mw-heading2 ext-discussiontools-init-section"><h2 id="Get_help" data-mw-thread-id="h-Get_help"><span data-mw-comment-start="" id="h-Get_help"></span>Get help<span data-mw-comment-end="h-Get_help"></span></h2></div>
<p>Bot operators who are unsure how to get the access they need can contact the Wikimedia Foundation at <span class="nowrap">bot-traffic<span class="skin-invert-image noviewer" typeof="mw:File"><span><img alt="@" src="//thumb.wikimedia.org/wikipedia/commons/thumb/8/88/At_sign.svg/20px-At_sign.svg.png?utm_source=www.mediawiki.org&amp;utm_campaign=parser&amp;utm_content=thumbnail" decoding="async" loading="lazy" width="15" height="15" class="mw-file-element" srcset="//thumb.wikimedia.org/wikipedia/commons/thumb/8/88/At_sign.svg/40px-At_sign.svg.png?utm_source=www.mediawiki.org&amp;utm_campaign=parser&amp;utm_content=thumbnail 2x" data-file-width="145" data-file-height="145"></span></span>wikimedia.org</span>.
</p>
<div class="mw-heading mw-heading2 ext-discussiontools-init-section"><h2 id="See_also" data-mw-thread-id="h-See_also"><span data-mw-comment-start="" id="h-See_also"></span>See also<span data-mw-comment-end="h-See_also"></span></h2></div>
<ul><li><a href="/wiki/Wikimedia_APIs/Rate_limits/FAQ" title="Wikimedia APIs/Rate limits/FAQ">Frequently asked questions about Wikimedia API rate limits</a></li>
<li><a href="/wiki/API:Etiquette" title="API:Etiquette">Best practices for using the Action API on Wikimedia wikis</a></li>
<li><a href="https://wikitech.wikimedia.org/wiki/External_request_limits" class="extiw" title="wikitech:External request limits">Technical overview of rate limiting in Wikimedia infrastructure</a></li></ul>
<!-- 
NewPP limit report
Parsed by mw‐web.codfw.main‐546d494d89‐qndss
Cached time: 20261015224134
Cache expiry: 2592000
Reduced expiry: false
Complications: [prevent‐selective‐update, show‐toc]
CPU time usage: 0.066 seconds
Real time usage: 0.094 seconds
Preprocessor visited node count: 411/1000000
Revision size: 7975/2097152 bytes
Post‐expand include size: 6905/2097152 bytes
Template argument size: 4018/2097152 bytes
Highest expansion depth: 18/100
Expensive parser function count: 1/500
Unstrip recursion depth: 0/20
Unstrip post‐expand size: 6439/5000000 bytes
Lua time usage: 0.004/10.000 seconds
Lua memory usage: 1042311/52428800 bytes
Number of Wikibase entities loaded: 0/500
-->
<!--
Transclusion expansion time report (%,ms,calls,template)
100.00%   74.088      1 -total
 85.04%   63.001      1 Template:Wikimedia_APIs
 81.13%   60.108      1 Template:Nmbox
 36.75%   27.224      5 Template:Ll
 33.85%   25.078      1 Template:Flatlist
 26.05%   19.303     10 Template:Translatable
 18.13%   13.434      5 Template:Pagelang
 10.00%    7.409      1 Template:Note
  3.14%    2.329      1 Template:Dir
  1.95%    1.444      1 Template:@
-->

<!-- Render ID 92bd320d-c8e9-11f1-9ba4-c315aa74bd1e -->

<!-- Saved in parser cache with key mediawikiwiki:pcache:2365815:|#|:idhash:canonical and timestamp 20261015224134 and revision id 8654799. Rendering was triggered because: diff-page
 -->
</div><!--
Post‐processing cache key mediawikiwiki:postproc‐pcache:2365815:|#|:idhash:enableSectionEditLinks=0!injectTOC=0!postproc=1!skin=vector‐2022!visibleLinks=single, generated at 20261015225445
--><noscript><img src="https://www.mediawiki.org/wiki/Special:CentralAutoLogin/start?useformat=desktop&amp;type=1x1&amp;usesul3=1" alt="" width="1" height="1" style="border: none; position: absolute;"></noscript>
<div class="printfooter" data-nosnippet="">Retrieved from "<a dir="ltr" href="https://www.mediawiki.org/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;oldid=8654799">https://www.mediawiki.org/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;oldid=8654799</a>"</div></div>
					<div id="catlinks" class="catlinks catlinks-allhidden" data-mw-interface=""></div>
				</div>
			</main>
			
		</div>
		<div class="mw-footer-container">
			<footer id="footer" class="mw-footer" >
				<ul id="footer-info" class="mw-portlet mw-portlet-footer-info">
	<li id="footer-info-lastmod"> This page was last edited on 15 October 2026, at 22:40.</li>
	<li id="footer-info-copyright">Text is available under the <a rel="nofollow" class="external text" href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike License</a>; additional terms may apply. Text in <a class="external text" href="https://www.mediawiki.org/wiki/Special:MyLanguage/Help:Contents">the Help: namespace</a> is available under the <a rel="nofollow" class="external text" href="https://creativecommons.org/publicdomain/zero/1.0/">Creative Commons CC0 License</a>.
By using this site, you agree to the <a class="external text" data-mw-original-href="//foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Terms_of_Use" href="https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Terms_of_Use">Terms of Use</a> and <a class="external text" data-mw-original-href="//foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Privacy_policy" href="https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Privacy_policy">Privacy Policy</a>.</li>
</ul>

				<ul id="footer-places" class="mw-portlet mw-portlet-footer-places">
	<li id="footer-places-privacy"><a href="https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Privacy_policy">Privacy policy</a></li>
	<li id="footer-places-about"><a href="/wiki/Project:About">About mediawiki.org</a></li>
	<li id="footer-places-disclaimers"><a href="/wiki/Project:General_disclaimer">Disclaimers</a></li>
	<li id="footer-places-legal-safety-contacts"><a href="https://foundation.wikimedia.org/wiki/Special:MyLanguage/Legal:Wikimedia_Foundation_Legal_and_Safety_Contact_Information">Legal &amp; safety contacts</a></li>
	<li id="footer-places-wm-codeofconduct"><a href="https://www.mediawiki.org/wiki/Special:MyLanguage/Code_of_Conduct">Code of Conduct</a></li>
	<li id="footer-places-developers"><a href="https://developer.wikimedia.org">Developers</a></li>
	<li id="footer-places-statslink"><a href="https://stats.wikimedia.org/#/www.mediawiki.org">Statistics</a></li>
	<li id="footer-places-cookiestatement"><a href="https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Cookie_statement">Cookie statement</a></li>
	<li id="footer-places-mobileview"><a href="//www.mediawiki.org/w/index.php?title=Wikimedia_APIs/Rate_limits&amp;mobileaction=toggle_view_mobile" class="noprint stopMobileRedirectToggle">Mobile view</a></li>
</ul>

				<ul id="footer-icons" class="mw-portlet mw-portlet-footer-icons noprint">
	<li id="footer-copyrightico"><a href="https://www.wikimedia.org/" class="cdx-button cdx-button--fake-button cdx-button--size-large cdx-button--fake-button--enabled"><picture><source media="(min-width: 500px)" srcset="/static/images/footer/wikimedia-button.svg" width="84" height="29"><img src="/static/images/footer/wikimedia.svg" width="25" height="25" alt="Wikimedia Foundation" lang="en" loading="lazy"></picture></a></li>
	<li id="footer-poweredbyico"><a href="https://www.mediawiki.org/" class="cdx-button cdx-button--fake-button cdx-button--size-large cdx-button--fake-button--enabled"><picture><source media="(min-width: 500px)" srcset="/w/resources/assets/poweredby_mediawiki.svg" width="88" height="31"><img src="/w/resources/assets/mediawiki_compact.svg" alt="Powered by MediaWiki" lang="en" width="25" height="25" loading="lazy"></picture></a></li>
</ul>

			</footer>
		</div>
	</div> 
</div> 
<div class="vector-header-container vector-sticky-header-container no-font-mode-scale">
	<div id="vector-sticky-header" class="vector-sticky-header">
		<div class="vector-sticky-header-start">
			<div class="vector-sticky-header-icon-start vector-button-flush-left" aria-hidden="true">
				<button class="cdx-button cdx-button--weight-quiet cdx-button--icon-only vector-sticky-header-search-toggle" tabindex="-1" data-event-name="ui.vector-sticky-search-form.icon"><span class="vector-icon mw-ui-icon-search mw-ui-icon-wikimedia-search cdx-button__icon"></span>

<span>Search</span>
			</button>
		</div>
			
		<div role="search" class="vector-search-box-vue  vector-search-box-show-thumbnail vector-search-box">
			<div class="vector-typeahead-search-container">
				<div class="cdx-typeahead-search cdx-typeahead-search--show-thumbnail">
					<form action="/w/index.php" id="vector-sticky-search-form" class="cdx-search-input cdx-search-input--has-end-button">
						<div  class="cdx-search-input__input-wrapper"  data-search-loc="header-moved">
							<div class="cdx-text-input cdx-text-input--has-start-icon">
								<input
									class="cdx-text-input__input mw-searchInput" autocomplete="off"
									
									type="search" name="search" placeholder="Search mediawiki.org">
								<span class="cdx-text-input__icon cdx-text-input__start-icon"></span>
							</div>
							<input type="hidden" name="title" value="Special:Search">
						</div>
						<button class="cdx-button cdx-search-input__end-button">Search</button>
					</form>
				</div>
			</div>
		</div>
		<div class="vector-sticky-header-context-bar">
				<nav aria-label="Contents" class="vector-toc-landmark">
						
					<div id="vector-sticky-header-toc" class="vector-dropdown mw-portlet mw-portlet-sticky-header-toc vector-sticky-header-toc vector-button-flush-left"  >
						<input type="checkbox" id="vector-sticky-header-toc-checkbox" role="button" aria-haspopup="true" data-event-name="ui.dropdown-vector-sticky-header-toc" class="vector-dropdown-checkbox "  aria-label="Toggle the table of contents"   >
						<label id="vector-sticky-header-toc-label" for="vector-sticky-header-toc-checkbox" class="vector-dropdown-label cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only " aria-hidden="true"  ><span class="vector-icon mw-ui-icon-listBullet mw-ui-icon-wikimedia-listBullet cdx-button__icon"></span>

<span class="vector-dropdown-label-text">Toggle the table of contents</span>
						</label>
						<div class="vector-dropdown-content">
					
						<div id="vector-sticky-header-toc-unpinned-container" class="vector-unpinned-container">
						</div>
					
						</div>
					</div>
			</nav>
				<div class="vector-sticky-header-context-bar-primary" aria-hidden="true" ><span lang="en" dir="ltr"><span class="mw-page-title-main">Wikimedia APIs/Rate limits</span></span></div>
			</div>
		</div>
		<div class="vector-sticky-header-end" aria-hidden="true">
			<div class="vector-sticky-header-icons">
				<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only" id="ca-talk-sticky-header" tabindex="-1" data-event-name="talk-sticky-header"><span class="vector-icon mw-ui-icon-speechBubbles mw-ui-icon-wikimedia-speechBubbles cdx-button__icon"></span>

<span></span>
			</a>
			<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only" id="ca-subject-sticky-header" tabindex="-1" data-event-name="subject-sticky-header"><span class="vector-icon mw-ui-icon-article mw-ui-icon-wikimedia-article cdx-button__icon"></span>

<span></span>
			</a>
			<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only" id="ca-history-sticky-header" tabindex="-1" data-event-name="history-sticky-header"><span class="vector-icon mw-ui-icon-wikimedia-history mw-ui-icon-wikimedia-wikimedia-history cdx-button__icon"></span>

<span></span>
			</a>
			<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only mw-watchlink" id="ca-watchstar-sticky-header" tabindex="-1" data-event-name="watch-sticky-header"><span class="vector-icon mw-ui-icon-wikimedia-star mw-ui-icon-wikimedia-wikimedia-star cdx-button__icon"></span>

<span></span>
			</a>
			<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only" id="ca-edit-sticky-header" tabindex="-1" data-event-name="wikitext-edit-sticky-header"><span class="vector-icon mw-ui-icon-wikimedia-wikiText mw-ui-icon-wikimedia-wikimedia-wikiText cdx-button__icon"></span>

<span></span>
			</a>
			<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only" id="ca-ve-edit-sticky-header" tabindex="-1" data-event-name="ve-edit-sticky-header"><span class="vector-icon mw-ui-icon-wikimedia-edit mw-ui-icon-wikimedia-wikimedia-edit cdx-button__icon"></span>

<span></span>
			</a>
			<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--icon-only" id="ca-viewsource-sticky-header" tabindex="-1" data-event-name="ve-edit-protected-sticky-header"><span class="vector-icon mw-ui-icon-wikimedia-editLock mw-ui-icon-wikimedia-wikimedia-editLock cdx-button__icon"></span>

<span></span>
			</a>
		</div>
			<div class="vector-sticky-header-buttons">
				<a href="#" class="cdx-button cdx-button--fake-button cdx-button--fake-button--enabled cdx-button--weight-quiet cdx-button--action-progressive" id="ca-addsection-sticky-header" tabindex="-1" data-event-name="addsection-sticky-header"><span class="vector-icon mw-ui-icon-speechBubbleAdd-progressive mw-ui-icon-wikimedia-speechBubbleAdd-progressive cdx-button__icon"></span>

<span>Add topic</span>
			</a>
		</div>
			<div class="vector-sticky-header-icon-end">
				<div class="vector-user-links">
				</div>
			</div>
		</div>
	</div>
</div>
<div class="mw-portlet mw-portlet-dock-bottom emptyPortlet" id="p-dock-bottom">
	<ul>
		
	</ul>
</div>
<script>(RLQ=window.RLQ||[]).push(function(){mw.config.set({"wgHostname":"mw-web.eqiad.main-58cf6dbc6c-8b8gg","wgBackendResponseTime":115,"wgDiscussionToolsPageThreads":[{"headingLevel":2,"name":"h-","type":"heading","level":0,"id":"h-Rationale","replies":[]},{"headingLevel":2,"name":"h-","type":"heading","level":0,"id":"h-Best_practices","replies":[]},{"headingLevel":2,"name":"h-","type":"heading","level":0,"id":"h-Limits","replies":[{"headingLevel":3,"name":"h-","type":"heading","level":0,"id":"h-Action-based_rate_limits-Limits","replies":[]}]},{"headingLevel":2,"name":"h-","type":"heading","level":0,"id":"h-Errors","replies":[]},{"headingLevel":2,"name":"h-","type":"heading","level":0,"id":"h-Caveats","replies":[]},{"headingLevel":2,"name":"h-","type":"heading","level":0,"id":"h-Get_help","replies":[]},{"headingLevel":2,"name":"h-","type":"heading","level":0,"id":"h-See_also","replies":[]}],"wgPageParseReport":{"limitreport":{"cputime":"0.066","walltime":"0.094","ppvisitednodes":{"value":411,"limit":1000000},"revisionsize":{"value":7975,"limit":2097152},"postexpandincludesize":{"value":6905,"limit":2097152},"templateargumentsize":{"value":4018,"limit":2097152},"expansiondepth":{"value":18,"limit":100},"expensivefunctioncount":{"value":1,"limit":500},"unstrip-depth":{"value":0,"limit":20},"unstrip-size":{"value":6439,"limit":5000000},"entityaccesscount":{"value":0,"limit":500},"timingprofile":["100.00%   74.088      1 -total"," 85.04%   63.001      1 Template:Wikimedia_APIs"," 81.13%   60.108      1 Template:Nmbox"," 36.75%   27.224      5 Template:Ll"," 33.85%   25.078      1 Template:Flatlist"," 26.05%   19.303     10 Template:Translatable"," 18.13%   13.434      5 Template:Pagelang"," 10.00%    7.409      1 Template:Note","  3.14%    2.329      1 Template:Dir","  1.95%    1.444      1 Template:@"]},"scribunto":{"limitreport-timeusage":{"value":"0.004","limit":"10.000"},"limitreport-memusage":{"value":1042311,"limit":52428800}},"cachereport":{"origin":"mw-web.codfw.main-546d494d89-qndss","timestamp":"20261015224134","ttl":2592000,"transientcontent":false},"discussiontools":{"limitreport-timeusage":"0.011"}}});});</script>
</body>
</html>