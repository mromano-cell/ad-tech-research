function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Yelp Audiences Explorer')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function fetchWebsiteContent(url) {
  try {
    if (!url || (!url.startsWith('http://') && !url.startsWith('https://'))) {
      url = 'https://' + url;
    }
    var response = UrlFetchApp.fetch(url, {
      muteHttpExceptions: true,
      followRedirects: true,
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; YelpAudienceBuilder/1.0)' }
    });
    var code = response.getResponseCode();
    if (code !== 200) {
      return { success: false, error: 'Site returned HTTP ' + code };
    }
    var html = response.getContentText();
    // Strip scripts, styles, and HTML tags to get text content
    html = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
    html = html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
    html = html.replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, '');
    html = html.replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, '');
    html = html.replace(/<[^>]+>/g, ' ');
    html = html.replace(/&nbsp;/g, ' ');
    html = html.replace(/&amp;/g, '&');
    html = html.replace(/&lt;/g, '<');
    html = html.replace(/&gt;/g, '>');
    html = html.replace(/\s+/g, ' ').trim();
    // Truncate to ~3000 chars to keep prompt size reasonable
    if (html.length > 3000) {
      html = html.substring(0, 3000) + '...';
    }
    return { success: true, content: html };
  } catch (e) {
    return { success: false, error: e.message || 'Could not fetch website' };
  }
}
