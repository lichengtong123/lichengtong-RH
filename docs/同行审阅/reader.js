"use strict";

const frame = document.getElementById("reader");
const manuscript = new URL("素数计数与黎曼猜想-预印版-同行审阅-加密.pdf", window.location.href);
const viewer = new URL("pdfjs/web/viewer.html", window.location.href);
viewer.searchParams.set("file", manuscript.href);
viewer.hash = "zoom=auto";

// Configure the same-origin viewer before it opens the encrypted manuscript.
document.addEventListener("webviewerloaded", (event) => {
  if (event.detail?.source !== frame.contentWindow) return;
  const options = event.detail.source.PDFViewerApplicationOptions;
  options.set("disablePreferences", true);
  options.set("enableScripting", false);
  options.set("enableAltTextModelDownload", false);
  options.set("sidebarViewOnLoad", 0);
  options.set("localeProperties", { lang: "zh-CN" });
});

frame.src = viewer.href;
