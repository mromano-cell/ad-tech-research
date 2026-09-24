function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Yelp Audiences Explorer')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function logBuilderSubmission(data) {
  try {
    var props = PropertiesService.getScriptProperties();
    var key = 'sub_' + new Date().getTime() + '_' + Math.random().toString(36).substr(2, 5);
    var record = {
      timestamp: new Date().toISOString(),
      advertiserName: data.advertiserName || '',
      categories: Array.isArray(data.categories) ? data.categories.join(', ') : (data.categories || ''),
      idealCustomer: data.idealCustomer || '',
      competitors: data.competitors || '',
      challenge: data.challenge || '',
      differentiator: data.differentiator || '',
      website: data.website || '',
      numStrategies: data.numStrategies || 0,
      strategyNames: data.strategyNames || ''
    };
    props.setProperty(key, JSON.stringify(record));
    return { success: true };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

// Run this from the Apps Script editor to export all submissions to a Google Sheet
function exportSubmissionsToSheet() {
  var props = PropertiesService.getScriptProperties();
  var all = props.getProperties();
  var rows = [];
  for (var key in all) {
    if (key.indexOf('sub_') === 0) {
      try {
        var r = JSON.parse(all[key]);
        rows.push([r.timestamp, r.advertiserName, r.categories, r.idealCustomer, r.competitors, r.challenge, r.differentiator, r.website, r.numStrategies, r.strategyNames]);
      } catch (e) {}
    }
  }
  rows.sort(function(a, b) { return a[0] < b[0] ? -1 : 1; });
  var ss = SpreadsheetApp.create('YA Builder Submissions Export - ' + new Date().toLocaleDateString());
  var sheet = ss.getActiveSheet();
  sheet.appendRow(['Timestamp', 'Advertiser', 'Categories', 'Ideal Customer', 'Competitors', 'Challenge', 'Differentiator', 'Website', '# Strategies', 'Strategy Names']);
  for (var i = 0; i < rows.length; i++) {
    sheet.appendRow(rows[i]);
  }
  sheet.getRange(1, 1, 1, 10).setFontWeight('bold');
  sheet.autoResizeColumns(1, 10);
  Logger.log('Exported ' + rows.length + ' submissions to: ' + ss.getUrl());
  return { count: rows.length, url: ss.getUrl() };
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
