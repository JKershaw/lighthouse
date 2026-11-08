


<!DOCTYPE html>
<html class="gl-system ui-gray with-top-bar with-header page-with-panels with-gl-container-queries  user-logged-out" lang="en">
<head prefix="og: http://ogp.me/ns#">
<meta charset="utf-8">
<meta content="IE=edge" http-equiv="X-UA-Compatible">
<meta content="width=device-width, initial-scale=1" name="viewport">
<title>GNOME / gtk · GitLab</title>
<link as="font" crossorigin="" href="/assets/gitlab-sans/GitLabSans-9892dc17af892e03de41625c0ee325117a3b8ee4ba6005f3a3eac68510030aed.woff2" rel="preload">
<link as="font" crossorigin="" href="/assets/gitlab-sans/GitLabSans-Italic-f96f17332d67b21ada2dfba5f0c0e1d5801eab99330472057bf18edd93d4ccf7.woff2" rel="preload">
<link as="font" crossorigin="" href="/assets/gitlab-mono/GitLabMono-29c2152dac8739499dd0fe5cd37a486ebcc7d4798c9b6d3aeab65b3172375b05.woff2" rel="preload">
<link as="font" crossorigin="" href="/assets/gitlab-mono/GitLabMono-Italic-af36701a2188df32a9dcea12e0424c380019698d4f76da9ad8ea2fd59432cf83.woff2" rel="preload">

<script>
//<![CDATA[
window.gon={};gon.api_version="v4";gon.default_avatar_url="https://gitlab.gnome.org/assets/no_avatar-849f9c04a3a0d0cea2424ae97b27447dc64a7dbfae83c036c45b403392f0e8ba.png";gon.max_file_size=500;gon.asset_host=null;gon.webpack_public_path="/assets/webpack/";gon.relative_url_root="";gon.user_color_mode="gl-system";gon.user_color_scheme="white";gon.markdown_surround_selection=null;gon.markdown_automatic_lists=null;gon.markdown_maintain_indentation=null;gon.math_rendering_limits_enabled=true;gon.recaptcha_api_server_url="https://www.recaptcha.net/recaptcha/api.js";gon.recaptcha_sitekey="6Lfhei8UAAAAAKwEVuEwxJX09r0AGdMm-DUTWNAQ";gon.gitlab_url="https://gitlab.gnome.org";gon.promo_url="https://about.gitlab.com";gon.forum_url="https://forum.gitlab.com";gon.docs_url="https://docs.gitlab.com";gon.revision="0d4c9a9a2fa";gon.feature_category="groups_and_projects";gon.gitlab_logo="/assets/gitlab_logo-2957169c8ef64c58616a1ac3f4fc626e8a35ce4eb3ed31bb0d873712f2a041a0.png";gon.secure=true;gon.sprite_icons="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg";gon.sprite_file_icons="/assets/file_icons/file_icons-90de312d3dbe794a19dee8aee171f184ff69ca9c9cf9fe37e8b254e84c3a1543.svg";gon.illustrations_path="/assets/illustrations-04a01984e0e87c0ff5382b3165c0edde89b46604b3dd8f8528bfb111ab1a435d.svg";gon.emoji_sprites_css_path="/assets/emoji_sprites-9f4e433199c18178b03727c749cbd0c22e569f69ffb05ec235a49dc29b318bb3.css";gon.emoji_backend_version=4;gon.test_env=false;gon.disable_animations=null;gon.suggested_label_colors={"#cc338b":"Magenta-pink","#dc143c":"Crimson","#c21e56":"Rose red","#cd5b45":"Dark coral","#ed9121":"Carrot orange","#eee600":"Titanium yellow","#009966":"Green-cyan","#8fbc8f":"Dark sea green","#6699cc":"Blue-gray","#e6e6fa":"Lavender","#9400d3":"Dark violet","#330066":"Deep violet","#36454f":"Charcoal grey","#808080":"Gray"};gon.first_day_of_week=1;gon.time_display_relative=true;gon.time_display_format=0;gon.ee=false;gon.jh=false;gon.dot_com=false;gon.uf_error_prefix="UF";gon.pat_prefix="ggopat";gon.fluid_layout=false;gon.keyboard_shortcuts_enabled=true;gon.emoji_autocomplete_enabled=true;gon.broadcast_message_dismissal_path=null;gon.diagramsnet_url="https://embed.diagrams.net";gon.features={"uiForOrganizations":false,"pageBreadcrumbsInTopBar":false,"orgSwitcher":false,"findAndReplace":false,"removeMonitorMetrics":true,"workItemsClientSideBoards":false,"hideUnpinnedSidebarItems":false,"workItemFeaturesField":true,"etagCachingPostRequests":false,"allowIframesInMarkdown":false,"useMermaidV12":false,"pageSpecificStyles":false};
//]]>
</script>

<script>
//<![CDATA[
const root = document.documentElement;
if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
  root.classList.add('gl-dark');
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (e.matches) {
    root.classList.add('gl-dark');
  } else {
    root.classList.remove('gl-dark');
  }
});

//]]>
</script>
<script>
//<![CDATA[
var gl = window.gl || {};
gl.startup_calls = {"/GNOME/gtk/-/refs/main/logs_tree/?format=json\u0026offset=0\u0026ref_type=HEADS":{},"/GNOME/gtk/-/blob/main/README.md?format=json\u0026ref_type=heads\u0026viewer=rich":{}};
gl.startup_graphql_calls = [{"query":"# @feature_category: source_code_management\nquery pathLastCommit($projectPath: ID!, $path: String, $ref: String!, $refType: RefType) {\n  project(fullPath: $projectPath) {\n    __typename\n    id\n    repository {\n      __typename\n      lastCommit(path: $path, ref: $ref, refType: $refType) {\n        __typename\n        id\n        sha\n        title\n        titleHtml\n        descriptionHtml\n        message\n        webPath\n        committerName\n        committerEmail\n        committedDate\n        authoredDate\n        authorName\n        authorEmail\n        authorGravatar\n        author {\n          __typename\n          id\n          name\n          avatarUrl\n          webPath\n        }\n        signature {\n          __typename\n          ... on GpgSignature {\n            gpgKeyPrimaryKeyid\n            verificationStatus\n          }\n          ... on X509Signature {\n            verificationStatus\n            x509Certificate {\n              id\n              subject\n              subjectKeyIdentifier\n              x509Issuer {\n                id\n                subject\n                subjectKeyIdentifier\n              }\n            }\n          }\n          ... on SshSignature {\n            verificationStatus\n            keyFingerprintSha256\n          }\n        }\n        pipelines(ref: $ref, first: 1) {\n          __typename\n          edges {\n            __typename\n            node {\n              __typename\n              id\n              detailedStatus {\n                __typename\n                id\n                detailsPath\n                icon\n                text\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n","variables":{"projectPath":"GNOME/gtk","ref":"main","path":""}}];

if (gl.startup_calls && window.fetch) {
  Object.keys(gl.startup_calls).forEach(apiCall => {
   gl.startup_calls[apiCall] = {
      fetchCall: fetch(apiCall, {
        // Emulate XHR for Rails AJAX request checks
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        // fetch won’t send cookies in older browsers, unless you set the credentials init option.
        // We set to `same-origin` which is default value in modern browsers.
        // See https://github.com/whatwg/fetch/pull/585 for more information.
        credentials: 'same-origin'
      })
    };
  });
}
if (gl.startup_graphql_calls && window.fetch) {
  const headers = {"X-CSRF-Token":"sNayAV3nXTipU1cer6oz0t1RljAunbJlZFRYuX_KvCgxyD_oiIapr09_vQBvK44gRzVENqi84ZGmmTw2VF12Fg","x-gitlab-feature-category":"groups_and_projects"};
  const url = `https://gitlab.gnome.org/api/graphql`

  const opts = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...headers,
    }
  };

  gl.startup_graphql_calls = gl.startup_graphql_calls.map(call => ({
    ...call,
    fetchCall: fetch(url, {
      ...opts,
      credentials: 'same-origin',
      body: JSON.stringify(call)
    })
  }))
}


//]]>
</script>



<meta content="light dark" name="color-scheme">
<link rel="stylesheet" href="/assets/application-79f356d98146549c21e5657de00ff91a957f995329d1725db0bb2a7251d2b59a.css" media="(prefers-color-scheme: light)" />
<link rel="stylesheet" href="/assets/application_dark-a3de088d254f447173abe48a05ec6b7ac075668b58b5be1aa26c5012bb0f8395.css" media="(prefers-color-scheme: dark)" />
<link rel="stylesheet" href="/assets/page_bundles/project-d8ddfdcca11af4ede140816f3befd2a538014d7403c28e0f3c62a50b61f93805.css" /><link rel="stylesheet" href="/assets/page_bundles/tree-c7ee4210fee3e1004d99dd5eb2483d2711447051180f46718d8cd1bc741b455a.css" /><link rel="stylesheet" href="/assets/page_bundles/commit_description-9e7efe20f0cef17d0606edabfad0418e9eb224aaeaa2dae32c817060fa60abcc.css" /><link rel="stylesheet" href="/assets/page_bundles/projects-f19dc1a1db773c979f17ccab5d349c8a65f20196156c47d16494b0f692e8f347.css" /><link rel="stylesheet" href="/assets/page_bundles/design_management-4765252040ab8edacfb27d7015bf41527629b0dc4fdacd1f1bc9d3f65cecae1b.css" /><link rel="stylesheet" href="/assets/page_bundles/issuable_list-7a33f8b5a79c609e4bac7e1fa1c5553962adf726cd700fbead1f9e974c41e7c9.css" /><link rel="stylesheet" href="/assets/page_bundles/issues_list-1d9cdbbaf9469f9073c410dc7a7f2543b02071773aa332daf63803eaaec87e62.css" /><link rel="stylesheet" href="/assets/page_bundles/issues_show-ec954ae4932e0bfe7383adee3c75f53c5985c6edea62c7ae4370cb1f6e85a91a.css" /><link rel="stylesheet" href="/assets/page_bundles/notes_shared-bd75305a90734f71761e8d13c4286994caf487acb52219ee52dcc65c0c3f6a05.css" /><link rel="stylesheet" href="/assets/page_bundles/work_items-b2f575a41145c7ff2490084c75138aab201b2593b93846f5812aec8cfb2a6ca2.css" />
<link rel="stylesheet" href="/assets/tailwind-1643fe418f6d3ad9eacf47d603d9c8150de2e6a435bbd333f32fd5f776cd7c7c.css" />


<link rel="stylesheet" href="/assets/fonts-deb7ad1d55ca77c0172d8538d53442af63604ff490c74acc2859db295c125bdb.css" />
<link rel="stylesheet" href="/assets/highlight/themes/white-2a02e7cdb193dcec5b8068ad0a57aee70b1cd0888c8d1dbe8ab5996651334922.css" media="(prefers-color-scheme: light)" />
<link rel="stylesheet" href="/assets/highlight/themes/dark-7fbedc840cde3d684b77966ee3740cd6cf4ba7c26a807b7c8701223af70f772f.css" media="(prefers-color-scheme: dark)" />

<script src="/assets/webpack/runtime.ea79027a.bundle.js" defer="defer"></script>
<script src="/assets/webpack/main.02b8bf31.chunk.js" defer="defer"></script>
<script src="/assets/webpack/tracker.1eb446cb.chunk.js" defer="defer"></script>
<script>
//<![CDATA[
window.snowplowOptions = {"namespace":"gl","hostname":"gitlab.gnome.org:443","postPath":"/-/collect_events","forceSecureTracker":true,"appId":"gitlab_sm"};
gl = window.gl || {};
gl.snowplowStandardContext = {"schema":"iglu:com.gitlab/gitlab_standard/jsonschema/1-1-8","data":{"environment":"self-managed","source":"gitlab-rails","client_type":"browser","correlation_id":"01M6Y9KRH9SVR5717WGYA3K2QJ","extra":{},"user_id":null,"global_user_id":null,"user_type":null,"is_gitlab_team_member":null,"namespace_id":8,"ultimate_parent_namespace_id":8,"project_id":665,"feature_enabled_by_namespace_ids":null,"realm":"self-managed","deployment_type":"self-managed","context_generated_at":"2026-11-08T19:19:24.025Z","organization_id":1}};
gl.snowplowPseudonymizedPageUrl = "https://gitlab.gnome.org/namespace8/project665";
gl.maskedDefaultReferrerUrl = null;
gl.ga4MeasurementId = 'G-ENFH3X7M5Y';
gl.duoEvents = [];
gl.onlySendDuoEvents = false;


//]]>
</script>



<script src="/assets/webpack/commons-graphql_explorer-pages.admin.application_settings.service_accounts-pages.admin.applications--b635524d.b3338b4b.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.abuse_reports.show-pages.dashboard.issues-pages.dashboard.issues.vue3-pages.dash-5ffc317d.0bcd8c23.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.abuse_reports.show-pages.dashboard.issues-pages.dashboard.issues.vue3-pages.dash-f8003152.f196957a.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.application_settings.service_accounts-pages.explore.analytics_dashboards-pages.e-306889d5.8b0f4475.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.abuse_reports.show-pages.dashboard.issues-pages.dashboard.work_items-pages.group-b344e337.050faeee.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.deploy_keys.index-pages.admin.deploy_keys.index.vue3-pages.admin.groups.index-pa-95f4ca76.204c76b4.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.dashboard.home-pages.registrations.new-pages.root-pages.root.vue3-pages.sessions.new-p-a41aff06.d68c093a.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.dashboard.home-pages.projects.snippets.show-pages.projects.snippets.show.vue3-pages.ro-3e3d840b.db458a62.chunk.js" defer="defer"></script>
<script src="/assets/webpack/0dcf7166.fee24f6c.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.search.show-pages.search.show.vue3-super_sidebar-super_sidebar.vue3.e1ab1d65.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-super_sidebar-super_sidebar.vue3.e38d27a4.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.search.show-super_sidebar.e41625fd.chunk.js" defer="defer"></script>
<script src="/assets/webpack/super_sidebar.ff1bc863.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects-pages.projects.activity-pages.projects.activity.vue3-pages.projects.alert_man-376eb50e.11611bcc.chunk.js" defer="defer"></script>
<script src="/assets/webpack/8632254b.bbb48efe.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-jira_connect_app-pages.admin.application_settings.service_accounts-pages.admin.impersonation-294ff6b2.052e3850.chunk.js" defer="defer"></script>
<script src="/assets/webpack/32327915.808412d1.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups.saved_views.show-pages.groups.work_items-pages.groups.work_items.show-pages.pro-164ac21d.01932e06.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.groups.index-pages.admin.groups.index.vue3-pages.admin.projects.index-pages.admi-81046c2c.cbf32916.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.blob.show.vue3-pages.projects.show-pages.projects.sh-7aa92eaa.aa63f32c.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.blob.show.vue3-pages.projects.show-pages.projects.sh-d934921b.1c5a3a9c.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.edit-pages.projects.blob.edit.vue3-pages.projects.blob.new-pages.project-d16b70ea.8fc1dfdd.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.blob.show.vue3-pages.projects.show-pages.projects.sh-4ce70f9d.15dca315.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.groups.index-pages.admin.projects.index-pages.dashboard.projects-pages.explore.p-25876521.02273cb0.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.admin.projects.index-pages.dashboard.projects-pages.explore.projects-pages.groups.show-c0a4d52d.b0c77b3a.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.blob.show.vue3-pages.projects.show-pages.projects.tr-c392bf45.8f6f5c63.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.snippets.show-pages.projects.tre-c684fcf6.703bdea7.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.commits.show-pages.projects.show-pages.projects.tree.show.1535a3b3.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.efbba67d.chunk.js" defer="defer"></script>
<script src="/assets/webpack/pages.projects.show.ef206841.chunk.js" defer="defer"></script>

<meta content="object" property="og:type">
<meta content="GitLab" property="og:site_name">
<meta content="GNOME / gtk · GitLab" property="og:title">
<meta content="GTK is a multi-platform toolkit for creating graphical user interfaces." property="og:description">
<meta content="https://gitlab.gnome.org/uploads/-/system/project/avatar/665/gtk-logo.png?v=1794163805" property="og:image">
<meta content="64" property="og:image:width">
<meta content="64" property="og:image:height">
<meta content="https://gitlab.gnome.org/GNOME/gtk" property="og:url">
<meta content="summary" property="twitter:card">
<meta content="GNOME / gtk · GitLab" property="twitter:title">
<meta content="GTK is a multi-platform toolkit for creating graphical user interfaces." property="twitter:description">
<meta content="https://gitlab.gnome.org/uploads/-/system/project/avatar/665/gtk-logo.png?v=1794163805" property="twitter:image">

<meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="03om89RcLhTOOnobBhNl3g04QHpP6yrTC2GQdTYYt5BSZKsaAT3agygWkAXGktgsl1ySfMnKeSfJrPT6HY99rg" />
<meta name="csp-nonce" />
<meta name="action-cable-url" content="/-/cable" />
<link crossorigin="use-credentials" href="/-/manifest.json" rel="manifest">
<link rel="icon" type="image/png" href="/uploads/-/system/appearance/favicon/1/GnomeLogoVertical.svg.png" id="favicon" data-original-href="/uploads/-/system/appearance/favicon/1/GnomeLogoVertical.svg.png" />
<link rel="apple-touch-icon" type="image/x-icon" href="/assets/apple-touch-icon-b049d4bc0dd9626f31db825d61880737befc7835982586d015bded10b4435460.png" />
<link crossorigin="use-credentials" href="/search/opensearch.xml" rel="search" title="Search GitLab" type="application/opensearchdescription+xml">
<link rel="alternate" type="application/atom+xml" title="gtk activity" href="/GNOME/gtk.atom" />




<meta content="GTK is a multi-platform toolkit for creating graphical user interfaces." name="description">
<meta content="#ECECEF" media="(prefers-color-scheme: light)" name="theme-color">
<meta content="#232227" media="(prefers-color-scheme: dark)" name="theme-color">
</head>

<body class="tab-width-8 gl-browser-generic gl-platform-other" data-group="GNOME" data-group-full-path="GNOME" data-namespace-id="8" data-page="projects:show" data-page-type-id="gtk" data-project="gtk" data-project-full-path="GNOME/gtk" data-project-id="665">
<div id="js-tooltips-container"></div>

<script>
//<![CDATA[
gl = window.gl || {};
gl.client = {"isGeneric":true,"isOther":true};


//]]>
</script>


<header class="super-topbar js-super-topbar"></header>
<div class="layout-page js-page-layout page-with-super-sidebar">
<script>
//<![CDATA[
const outer = document.createElement('div');
outer.style.visibility = 'hidden';
outer.style.overflow = 'scroll';
document.body.appendChild(outer);
const inner = document.createElement('div');
outer.appendChild(inner);
const scrollbarWidth = outer.offsetWidth - inner.offsetWidth;
outer.parentNode.removeChild(outer);
document.documentElement.style.setProperty('--scrollbar-width', `${scrollbarWidth}px`);

//]]>
</script><aside class="js-super-sidebar super-sidebar super-sidebar-loading" data-command-palette="{&quot;project_files_url&quot;:&quot;/GNOME/gtk/-/files/main?format=json&quot;,&quot;project_blob_url&quot;:&quot;/GNOME/gtk/-/blob/main&quot;}" data-is-saas="false" data-sidebar="{&quot;is_logged_in&quot;:false,&quot;compare_plans_url&quot;:&quot;https://about.gitlab.com/pricing&quot;,&quot;current_menu_items&quot;:[{&quot;id&quot;:&quot;project_overview&quot;,&quot;title&quot;:&quot;gtk&quot;,&quot;avatar&quot;:&quot;/uploads/-/system/project/avatar/665/gtk-logo.png?v=1794163805&quot;,&quot;entity_id&quot;:665,&quot;link&quot;:&quot;/GNOME/gtk&quot;,&quot;link_classes&quot;:&quot;shortcuts-project&quot;,&quot;is_active&quot;:true},{&quot;id&quot;:&quot;manage_menu&quot;,&quot;title&quot;:&quot;Manage&quot;,&quot;icon&quot;:&quot;users&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/activity&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;activity&quot;,&quot;title&quot;:&quot;Activity&quot;,&quot;link&quot;:&quot;/GNOME/gtk/activity&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-activity&quot;,&quot;description&quot;:&quot;Track what your team is working on and stay informed of changes&quot;,&quot;library_icon&quot;:&quot;history&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;members&quot;,&quot;title&quot;:&quot;Members&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/project_members&quot;,&quot;description&quot;:&quot;Control who has access to your project and what they can do&quot;,&quot;library_icon&quot;:&quot;users&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;labels&quot;,&quot;title&quot;:&quot;Labels&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/labels&quot;,&quot;description&quot;:&quot;Organize and categorize work across your project with consistent labels&quot;,&quot;library_icon&quot;:&quot;labels&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;plan_menu&quot;,&quot;title&quot;:&quot;Plan&quot;,&quot;icon&quot;:&quot;planning&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/work_items&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;project_issue_list&quot;,&quot;title&quot;:&quot;Work items&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/work_items&quot;,&quot;link_classes&quot;:&quot;shortcuts-issues has-sub-items&quot;,&quot;pill_count_field&quot;:&quot;openWorkItemsCount&quot;,&quot;pill_count_dynamic&quot;:false,&quot;description&quot;:&quot;Plan, track, and manage work in one place&quot;,&quot;library_icon&quot;:&quot;work-items&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;boards&quot;,&quot;title&quot;:&quot;Issue boards&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/boards&quot;,&quot;link_classes&quot;:&quot;shortcuts-issue-boards&quot;,&quot;description&quot;:&quot;Visualize and manage work with kanban-style boards&quot;,&quot;library_icon&quot;:&quot;work-item-issue-board&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;milestones&quot;,&quot;title&quot;:&quot;Milestones&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/milestones&quot;,&quot;description&quot;:&quot;Plan releases and group work into time-based phases&quot;,&quot;library_icon&quot;:&quot;milestone&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;project_wiki&quot;,&quot;title&quot;:&quot;Wiki&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/wikis&quot;,&quot;link_classes&quot;:&quot;shortcuts-wiki&quot;,&quot;description&quot;:&quot;Create and manage documentation&quot;,&quot;library_icon&quot;:&quot;book&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;code_menu&quot;,&quot;title&quot;:&quot;Code&quot;,&quot;icon&quot;:&quot;code&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/merge_requests&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;project_merge_request_list&quot;,&quot;title&quot;:&quot;Merge requests&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/merge_requests&quot;,&quot;link_classes&quot;:&quot;shortcuts-merge_requests&quot;,&quot;pill_count_field&quot;:&quot;openMergeRequestsCount&quot;,&quot;pill_count_dynamic&quot;:false,&quot;description&quot;:&quot;Collaborate on code changes with built-in review tools&quot;,&quot;library_icon&quot;:&quot;merge-request&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;files&quot;,&quot;title&quot;:&quot;Repository&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/tree/main&quot;,&quot;link_classes&quot;:&quot;shortcuts-tree&quot;,&quot;description&quot;:&quot;Browse and manage repository files and code&quot;,&quot;library_icon&quot;:&quot;repository&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;branches&quot;,&quot;title&quot;:&quot;Branches&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/branches&quot;,&quot;description&quot;:&quot;Manage project branches and branch protection&quot;,&quot;library_icon&quot;:&quot;branch&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;commits&quot;,&quot;title&quot;:&quot;Commits&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/commits/main?ref_type=heads&quot;,&quot;link_classes&quot;:&quot;shortcuts-commits&quot;,&quot;description&quot;:&quot;View commit history and changes&quot;,&quot;library_icon&quot;:&quot;commit&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;tags&quot;,&quot;title&quot;:&quot;Tags&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/tags&quot;,&quot;description&quot;:&quot;Create and manage release tags&quot;,&quot;library_icon&quot;:&quot;tag&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;graphs&quot;,&quot;title&quot;:&quot;Repository graph&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/network/main?ref_type=heads&quot;,&quot;link_classes&quot;:&quot;shortcuts-network&quot;,&quot;description&quot;:&quot;Visualize repository commit history and branches&quot;,&quot;library_icon&quot;:&quot;repository-graph&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;compare&quot;,&quot;title&quot;:&quot;Compare revisions&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/compare?from=main\u0026to=main&quot;,&quot;description&quot;:&quot;Compare changes between revisions&quot;,&quot;library_icon&quot;:&quot;comparison&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;project_snippets&quot;,&quot;title&quot;:&quot;Snippets&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/snippets&quot;,&quot;link_classes&quot;:&quot;shortcuts-snippets&quot;,&quot;description&quot;:&quot;Store and share code snippets&quot;,&quot;library_icon&quot;:&quot;snippet&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;build_menu&quot;,&quot;title&quot;:&quot;Build&quot;,&quot;icon&quot;:&quot;rocket&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/pipelines&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;pipelines&quot;,&quot;title&quot;:&quot;Pipelines&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/pipelines&quot;,&quot;link_classes&quot;:&quot;shortcuts-pipelines&quot;,&quot;description&quot;:&quot;Automate your build and deployment process&quot;,&quot;library_icon&quot;:&quot;pipeline&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;jobs&quot;,&quot;title&quot;:&quot;Jobs&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/jobs&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;description&quot;:&quot;Monitor individual build tasks and their results&quot;,&quot;library_icon&quot;:&quot;job&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;pipeline_schedules&quot;,&quot;title&quot;:&quot;Pipeline schedules&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/pipeline_schedules&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;description&quot;:&quot;Run your automation on a recurring schedule&quot;,&quot;library_icon&quot;:&quot;pipeline-schedule&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;artifacts&quot;,&quot;title&quot;:&quot;Artifacts&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/artifacts&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;description&quot;:&quot;Access build outputs and compiled binaries&quot;,&quot;library_icon&quot;:&quot;doc-compressed&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;deploy_menu&quot;,&quot;title&quot;:&quot;Deploy&quot;,&quot;icon&quot;:&quot;deployments&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/releases&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;releases&quot;,&quot;title&quot;:&quot;Releases&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/releases&quot;,&quot;link_classes&quot;:&quot;shortcuts-deployments-releases&quot;,&quot;description&quot;:&quot;Create and manage project releases&quot;,&quot;library_icon&quot;:&quot;release&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;container_registry&quot;,&quot;title&quot;:&quot;Container registry&quot;,&quot;link&quot;:&quot;/GNOME/gtk/container_registry&quot;,&quot;description&quot;:&quot;Store and deploy container images&quot;,&quot;library_icon&quot;:&quot;container-image&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_registry&quot;,&quot;title&quot;:&quot;Model registry&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/ml/models&quot;,&quot;description&quot;:&quot;Store and manage machine learning models&quot;,&quot;library_icon&quot;:&quot;model-registry&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;operations_menu&quot;,&quot;title&quot;:&quot;Operate&quot;,&quot;icon&quot;:&quot;cloud-pod&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/environments&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;environments&quot;,&quot;title&quot;:&quot;Environments&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/environments&quot;,&quot;link_classes&quot;:&quot;shortcuts-environments&quot;,&quot;description&quot;:&quot;Manage your staging and production deployments&quot;,&quot;library_icon&quot;:&quot;environment&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;monitor_menu&quot;,&quot;title&quot;:&quot;Monitor&quot;,&quot;icon&quot;:&quot;monitor&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/incidents&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;incidents&quot;,&quot;title&quot;:&quot;Incidents&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/incidents&quot;,&quot;description&quot;:&quot;Manage incident response and resolution&quot;,&quot;library_icon&quot;:&quot;work-item-incident&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;service_desk&quot;,&quot;title&quot;:&quot;Service Desk&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/issues/service_desk&quot;,&quot;description&quot;:&quot;Collect customer feedback and support requests via email&quot;,&quot;library_icon&quot;:&quot;service-desk&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;analyze_menu&quot;,&quot;title&quot;:&quot;Analyze&quot;,&quot;icon&quot;:&quot;chart&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/value_stream_analytics&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;cycle_analytics&quot;,&quot;title&quot;:&quot;Value stream analytics&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/value_stream_analytics&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-cycle-analytics&quot;,&quot;description&quot;:&quot;Analyze value stream and cycle time&quot;,&quot;library_icon&quot;:&quot;value-stream-analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;contributors&quot;,&quot;title&quot;:&quot;Contributor analytics&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/graphs/main?ref_type=heads&quot;,&quot;description&quot;:&quot;Track and view member contributions and activity&quot;,&quot;library_icon&quot;:&quot;contributor-analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;ci_cd_analytics&quot;,&quot;title&quot;:&quot;CI/CD analytics&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/pipelines/charts&quot;,&quot;description&quot;:&quot;Analyze CI/CD pipeline metrics and performance&quot;,&quot;library_icon&quot;:&quot;cicd-analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;repository_analytics&quot;,&quot;title&quot;:&quot;Repository analytics&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/graphs/main/charts&quot;,&quot;link_classes&quot;:&quot;shortcuts-repository-charts&quot;,&quot;description&quot;:&quot;Analyze repository coverage, statistics, and metrics&quot;,&quot;library_icon&quot;:&quot;repository-analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_experiments&quot;,&quot;title&quot;:&quot;Model experiments&quot;,&quot;link&quot;:&quot;/GNOME/gtk/-/ml/experiments&quot;,&quot;description&quot;:&quot;Track and manage machine learning experiments&quot;,&quot;library_icon&quot;:&quot;machine-learning&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false}],&quot;current_context_header&quot;:&quot;Project&quot;,&quot;support_path&quot;:&quot;https://support.gitlab.com&quot;,&quot;display_whats_new&quot;:false,&quot;show_version_check&quot;:null,&quot;search&quot;:{&quot;search_context&quot;:{&quot;group&quot;:{&quot;id&quot;:8,&quot;name&quot;:&quot;GNOME&quot;,&quot;full_name&quot;:&quot;GNOME&quot;},&quot;group_metadata&quot;:{&quot;issues_path&quot;:&quot;/groups/GNOME/-/issues&quot;,&quot;mr_path&quot;:&quot;/groups/GNOME/-/merge_requests&quot;},&quot;project&quot;:{&quot;id&quot;:665,&quot;name&quot;:&quot;gtk&quot;},&quot;project_metadata&quot;:{&quot;mr_path&quot;:&quot;/GNOME/gtk/-/merge_requests&quot;,&quot;issues_path&quot;:&quot;/GNOME/gtk/-/issues&quot;},&quot;code_search&quot;:true,&quot;ref&quot;:&quot;main&quot;,&quot;scope&quot;:null,&quot;for_snippets&quot;:null}},&quot;panel_type&quot;:&quot;project&quot;,&quot;shortcut_links&quot;:[{&quot;title&quot;:&quot;Snippets&quot;,&quot;href&quot;:&quot;/explore/snippets&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-snippets&quot;},{&quot;title&quot;:&quot;Groups&quot;,&quot;href&quot;:&quot;/explore/groups&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-groups&quot;},{&quot;title&quot;:&quot;Projects&quot;,&quot;href&quot;:&quot;/explore/projects&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-projects&quot;}],&quot;has_terms&quot;:true,&quot;allow_signup&quot;:&quot;false&quot;,&quot;pinned_items&quot;:[&quot;project_overview&quot;,&quot;members&quot;,&quot;project_issue_list&quot;,&quot;branches&quot;,&quot;project_merge_request_list&quot;,&quot;pipelines&quot;]}"></aside>

<div class="broadcast-wrapper gl-rounded-lg gl-overflow-hidden">



</div>
<div class="panels-container gl-flex gl-gap-3">
<div class="content-panels gl-flex-1 gl-w-full gl-flex gl-gap-0 gl-relative js-content-panels gl-@container/content-panels">
<div class="paneled-view static-panel js-static-panel js-paneled-view content-wrapper">
<div class="panel-header">
<div class="panel-header-inner js-panel-header-inner">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"GNOME","item":"https://gitlab.gnome.org/GNOME"},{"@type":"ListItem","position":2,"name":"gtk","item":"https://gitlab.gnome.org/GNOME/gtk"}]}


</script>
<div data-testid="breadcrumb-links" id="js-vue-page-breadcrumbs-wrapper">
<div data-breadcrumbs-json="[{&quot;text&quot;:&quot;GNOME&quot;,&quot;href&quot;:&quot;/GNOME&quot;,&quot;avatarPath&quot;:&quot;/uploads/-/system/group/avatar/8/gnomelogo.png?v=1777306328&quot;},{&quot;text&quot;:&quot;gtk&quot;,&quot;href&quot;:&quot;/GNOME/gtk&quot;,&quot;avatarPath&quot;:&quot;/uploads/-/system/project/avatar/665/gtk-logo.png?v=1794163805&quot;}]" id="js-vue-page-breadcrumbs"></div>
<div id="js-injected-page-breadcrumbs"></div>
</div>
<div id="js-page-breadcrumbs-extra"></div>



<div class="panel-header-inner-actions">


<div class="panel-header-inner-actions-portal-target js-panel-actions-portal-target"></div>
</div>
</div>
</div>
<div class="panel-content">
<div class="panel-content-inner js-static-panel-inner">
<div class="alert-wrapper alert-wrapper-top-space gl-flex gl-flex-col gl-gap-3 container-fluid container-limited">



























</div>


<div class="container-fluid container-limited project-highlight-puc">
<main class="content gl-@container/panel" id="content-body" itemscope itemtype="http://schema.org/SoftwareSourceCode">
<div id="js-drawer-container"></div>
<div class="flash-container flash-container-page sticky" data-testid="flash-container">
<div id="js-global-alerts"></div>
</div>










<header class="project-home-panel js-show-on-project-root gl-mt-2">
<div class="gl-flex gl-justify-between gl-flex-wrap gl-flex-col gl-gap-5 @sm/panel:gl-flex-row">
<div class="home-panel-title-row gl-flex gl-items-center">
<img srcset="/uploads/-/system/project/avatar/665/gtk-logo.png?v=1794163805&amp;width=48 1x, /uploads/-/system/project/avatar/665/gtk-logo.png?v=1794163805&amp;width=96 2x" class="gl-avatar gl-avatar-s48 gl-self-start gl-shrink-0 gl-mr-4" height="48" width="48" loading="lazy" itemprop="image" alt="gtk" src="/uploads/-/system/project/avatar/665/gtk-logo.png?v=1794163805&amp;width=48" />

<h1 class="home-panel-title gl-heading-1 gl-flex gl-items-center gl-flex-wrap gl-gap-3 gl-break-anywhere gl-mb-0" data-testid="project-name-content" itemprop="name">
gtk
<button class="has-tooltip gl-border-0 gl-bg-transparent gl-p-0 gl-leading-0 gl-text-inherit visibility-icon gl-inline-flex" data-container="body" data-placement="top" title="Public - The project can be accessed without any authentication." type="button" aria-label="Public - The project can be accessed without any authentication."><svg class="s16 gl-fill-icon-subtle" data-testid="earth-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#earth"></use></svg></button>


</h1>
</div>
<div data-can-read-project="true" data-can-request-access="false" data-can-withdraw-access-request="false" data-dashboard-path="/dashboard/projects" data-is-project-empty="false" data-project-full-path="GNOME/gtk" data-project-id="665" data-request-access-path="/GNOME/gtk/-/project_members/request_access" data-sign-in-path="/users/sign_in?redirect_to_referer=yes" data-star-count="298" data-starred="false" data-starrers-path="/GNOME/gtk/-/starrers" data-withdraw-access-request-path="/GNOME/gtk/-/project_members/leave" id="js-home-panel"></div>
</div>

</header>

<div class="project-page-indicator js-show-on-project-root"></div>
<div class="project-page-layout">
<div class="project-page-layout-sidebar js-show-on-project-root gl-mt-5">
<aside class="project-page-sidebar" data-testid="project-page-sidebar">
<div class="project-page-sidebar-block home-panel-home-desc gl-py-4 gl-border-b gl-border-b-subtle !gl-pt-2">
<h2 class="gl-text-base gl-font-bold gl-leading-reset gl-text-heading gl-m-0 gl-mb-1">Project information</h2>
<div class="home-panel-description gl-break-words">
<div class="home-panel-description-markdown read-more-container" data-read-more-height="320" itemprop="description">
<div class="read-more-content read-more-content--has-scrim">
<p data-sourcepos="1:1-1:71" dir="auto">GTK is a multi-platform toolkit for creating graphical user interfaces.</p>
</div>
<div class="js-read-more-trigger gl-hidden gl-w-full gl-h-8 gl-absolute gl-bottom-0 gl-z-2 gl-bg-default">
<button aria-label="Expand project information" type="button" class="gl-button btn btn-md btn-link "><span class="gl-button-text">
<svg class="s14" data-testid="chevron-down-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#chevron-down"></use></svg>
Read more

</span>

</button></div>
</div>
</div>
<div class="gl-mb-2">
<div class="progress repository-languages-bar js-show-on-project-root"><div class="progress-bar has-tooltip" style="width: 91.27%; background-color:#555555" data-html="true" title="&lt;span class=&quot;repository-language-bar-tooltip-language&quot;&gt;C&lt;/span&gt;&amp;nbsp;&lt;span class=&quot;repository-language-bar-tooltip-share&quot;&gt;91.3%&lt;/span&gt;"></div><div class="progress-bar has-tooltip" style="width: 6.58%; background-color:#663399" data-html="true" title="&lt;span class=&quot;repository-language-bar-tooltip-language&quot;&gt;CSS&lt;/span&gt;&amp;nbsp;&lt;span class=&quot;repository-language-bar-tooltip-share&quot;&gt;6.6%&lt;/span&gt;"></div><div class="progress-bar has-tooltip" style="width: 0.57%; background-color:#007800" data-html="true" title="&lt;span class=&quot;repository-language-bar-tooltip-language&quot;&gt;Meson&lt;/span&gt;&amp;nbsp;&lt;span class=&quot;repository-language-bar-tooltip-share&quot;&gt;0.6%&lt;/span&gt;"></div><div class="progress-bar has-tooltip" style="width: 0.32%; background-color:#c6538c" data-html="true" title="&lt;span class=&quot;repository-language-bar-tooltip-language&quot;&gt;SCSS&lt;/span&gt;&amp;nbsp;&lt;span class=&quot;repository-language-bar-tooltip-share&quot;&gt;0.3%&lt;/span&gt;"></div><div class="progress-bar has-tooltip" style="width: 0.28%; background-color:#f34b7d" data-html="true" title="&lt;span class=&quot;repository-language-bar-tooltip-language&quot;&gt;C++&lt;/span&gt;&amp;nbsp;&lt;span class=&quot;repository-language-bar-tooltip-share&quot;&gt;0.3%&lt;/span&gt;"></div></div>
</div>
</div>
<div class="project-page-sidebar-block gl-py-4 gl-border-b gl-border-b-subtle">
<nav class="project-stats">
<ul class="nav gl-gap-y-2 gl-gap-x-5">
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2" href="/GNOME/gtk/-/commits/main"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="commit-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#commit"></use></svg><strong class="project-stat-value">91,058</strong> Commits</a>
</li>
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2" href="/GNOME/gtk/-/branches"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="branch-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#branch"></use></svg><strong class="project-stat-value">1,463</strong> Branches</a>
</li>
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2" href="/GNOME/gtk/-/tags"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="label-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#label"></use></svg><strong class="project-stat-value">867</strong> Tags</a>
</li>
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2" href="/GNOME/gtk/-/releases"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="rocket-launch-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#rocket-launch"></use></svg><strong class="project-stat-value">51</strong> Releases</a>
</li>
</ul>

</nav>
</div>
<div class="project-page-sidebar-block gl-py-4 gl-border-b gl-border-b-subtle">
<div class="project-buttons gl-mb-2 js-show-on-project-root" data-testid="project-buttons">
<ul class="nav gl-gap-y-2 gl-gap-x-5">
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2 btn-default" data-event-tracking="click_readme_on_project_overview" data-event-label="view" href="/GNOME/gtk/-/blob/main/README.md"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="doc-text-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#doc-text"></use></svg>README</a>
</li>
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2 btn-default" itemprop="license" data-event-tracking="click_license_on_project_overview" data-event-label="view" href="/GNOME/gtk/-/blob/main/COPYING"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="scale-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#scale"></use></svg><span class="project-stat-value">GNU Library General Public License v2 only</span></a>
</li>
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2 btn-default" data-event-tracking="click_changelog_on_project_overview" data-event-label="view" href="/GNOME/gtk/-/blob/main/NEWS"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="doc-text-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#doc-text"></use></svg>CHANGELOG</a>
</li>
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2 btn-default" data-event-tracking="click_contributing_on_project_overview" data-event-label="view" href="/GNOME/gtk/-/blob/main/CONTRIBUTING.md"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="doc-text-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#doc-text"></use></svg>CONTRIBUTING</a>
</li>
<li class="nav-item gl-leading-1">
<a class="nav-link stat-link !gl-px-0 !gl-pb-2 btn-default" data-event-tracking="click_pages_on_project_overview" href="https://gnome.pages.gitlab.gnome.org/gtk"><svg class="s16 gl-fill-icon-subtle gl-mr-3" data-testid="external-link-icon"><use href="/assets/icons-557611e974a59dbbc29ee0980dc4bc97610b136af3a30b5c715d47d566317bc5.svg#external-link"></use></svg>GitLab Pages</a>
</li>
</ul>

</div>
</div>


<div class="project-page-sidebar-block gl-py-4">
<p class="gl-font-bold gl-text-strong gl-m-0 gl-mb-1">Created on</p>
<span>February 08, 2018</span>
</div>
</aside>

</div>
<div class="project-page-layout-content">
<div class="project-show-files">
<div class="gl-flex navigation-root">
<div id="js-file-browser" style="width:320px"></div>
<div class="gl-w-full gl-min-w-0">
<div class="tree-holder gl-clearfix gl-mt-4" id="tree-holder">
<div data-breadcrumbs-can-collaborate="false" data-breadcrumbs-can-edit-tree="false" data-breadcrumbs-can-push-code="false" data-breadcrumbs-can-push-to-branch="false" data-breadcrumbs-new-blob-path="/GNOME/gtk/-/new/main" data-breadcrumbs-new-branch-path="/GNOME/gtk/-/branches/new" data-breadcrumbs-new-dir-path="/GNOME/gtk/-/create_dir/main" data-breadcrumbs-new-tag-path="/GNOME/gtk/-/tags/new" data-breadcrumbs-upload-path="/GNOME/gtk/-/create/main" data-custom-code-dropdown-clients="[]" data-download-links="[{&quot;text&quot;:&quot;zip&quot;,&quot;path&quot;:&quot;/GNOME/gtk/-/archive/main/gtk-main.zip?ref_type=heads&quot;},{&quot;text&quot;:&quot;tar.gz&quot;,&quot;path&quot;:&quot;/GNOME/gtk/-/archive/main/gtk-main.tar.gz?ref_type=heads&quot;},{&quot;text&quot;:&quot;tar.bz2&quot;,&quot;path&quot;:&quot;/GNOME/gtk/-/archive/main/gtk-main.tar.bz2?ref_type=heads&quot;},{&quot;text&quot;:&quot;tar&quot;,&quot;path&quot;:&quot;/GNOME/gtk/-/archive/main/gtk-main.tar?ref_type=heads&quot;}]" data-escaped-ref="main" data-http-url="https://gitlab.gnome.org/GNOME/gtk.git" data-project-id="665" data-project-path="GNOME/gtk" data-project-root-path="/GNOME/gtk" data-ref="main" data-ref-type="heads" data-root-ref="main" data-show-no-ssh-key-message="" data-ssh-url="[email withheld by Lighthouse]:GNOME/gtk.git" data-user-settings-ssh-keys-path="/-/user_settings/ssh_keys" data-web-ide-button-options="{&quot;is_fork&quot;:false,&quot;needs_to_fork&quot;:true,&quot;gitpod_enabled&quot;:false,&quot;is_blob&quot;:false,&quot;show_edit_button&quot;:false,&quot;show_web_ide_button&quot;:false,&quot;show_gitpod_button&quot;:false,&quot;show_pipeline_editor_button&quot;:false,&quot;web_ide_url&quot;:&quot;/-/ide/project/GNOME/gtk/edit/main&quot;,&quot;edit_url&quot;:&quot;&quot;,&quot;pipeline_editor_url&quot;:&quot;/GNOME/gtk/-/ci/editor?branch_name=main&quot;,&quot;gitpod_url&quot;:&quot;&quot;,&quot;user_preferences_gitpod_path&quot;:&quot;/-/profile/preferences#user_gitpod_enabled&quot;,&quot;user_profile_enable_gitpod_path&quot;:&quot;/-/user_settings/profile?user%5Bgitpod_enabled%5D=true&quot;}" data-xcode-url="" id="js-repository-blob-header-app"></div>
<div class="info-well project-last-commit gl-mt-5">
<div class="gl-flex gl-items-center gl-justify-center gl-m-auto gl-min-h-9 @lg/panel:gl-min-h-[4.5rem]" data-history-link="/GNOME/gtk/-/commits/main" data-ref-type="heads" id="js-last-commit">
<div class="gl-spinner-container" role="status"><span aria-hidden class="gl-spinner gl-spinner-md gl-spinner-dark !gl-align-text-bottom"></span><span class="gl-sr-only !gl-absolute">Loading</span>
</div>
</div>
</div>
<div data-escaped-ref="main" data-full-name="GNOME / gtk" data-has-revs-file="false" data-project-path="GNOME/gtk" data-project-short-path="gtk" data-ref="main" data-ref-type="heads" id="js-tree-list"></div>

</div>
</div>
</div>

</div>
</div>
</div>


</main>
</div>


</div>


</div>
</div>
<div class="paneled-view-portal" id="contextual-panel-portal"></div>
</div>
</div>

</div>


<script>
//<![CDATA[
if ('loading' in HTMLImageElement.prototype) {
  document.querySelectorAll('img.lazy').forEach(img => {
    img.loading = 'lazy';
    let imgUrl = img.dataset.src;
    // Only adding width + height for avatars for now
    // Keep this logic in sync with appendWidthToAvatarUrl in
    // app/assets/javascripts/vue_shared/components/user_avatar/utils.js
    if (imgUrl.indexOf('/avatar/') > -1 && !imgUrl.includes('width=')) {
      const targetWidth = img.getAttribute('width') || img.width;
      imgUrl += imgUrl.includes('?') ? `&width=${targetWidth}` : `?width=${targetWidth}`;
    }
    img.src = imgUrl;
    img.removeAttribute('data-src');
    img.classList.remove('lazy');
    img.classList.add('js-lazy-loaded');
    img.dataset.testid = 'js-lazy-loaded-content';
  });
}

//]]>
</script>
<script>
//<![CDATA[
gl = window.gl || {};
gl.experiments = {};


//]]>
</script>

</body>
</html>

