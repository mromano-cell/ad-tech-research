function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Yelp Audiences Explorer')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getOrCreateLogSheet_() {
  var props = PropertiesService.getScriptProperties();
  var sheetId = props.getProperty('LOG_SHEET_ID');
  if (sheetId) {
    try {
      return SpreadsheetApp.openById(sheetId);
    } catch (e) {
      // Sheet was deleted or inaccessible, create a new one
    }
  }
  var ss = SpreadsheetApp.create('YA Explorer - AI Builder Submissions');
  var sheet = ss.getActiveSheet();
  sheet.setName('Submissions');
  sheet.appendRow([
    'Timestamp', 'Advertiser', 'Categories', 'Ideal Customer',
    'Competitors', 'Business Challenge', 'What Makes Them Unique',
    'Website URL', '# Strategies Generated', 'Strategy Names'
  ]);
  sheet.getRange('1:1').setFontWeight('bold');
  sheet.setFrozenRows(1);
  sheet.setColumnWidth(1, 160);
  sheet.setColumnWidth(2, 180);
  sheet.setColumnWidth(3, 250);
  sheet.setColumnWidth(4, 250);
  sheet.setColumnWidth(5, 200);
  sheet.setColumnWidth(6, 250);
  sheet.setColumnWidth(7, 250);
  sheet.setColumnWidth(8, 200);
  sheet.setColumnWidth(9, 100);
  sheet.setColumnWidth(10, 350);
  props.setProperty('LOG_SHEET_ID', ss.getId());
  return ss;
}

function logBuilderSubmission(data) {
  try {
    var ss = getOrCreateLogSheet_();
    var sheet = ss.getSheetByName('Submissions') || ss.getActiveSheet();
    sheet.appendRow([
      new Date(),
      data.advertiserName || '',
      (data.categories || []).join(', '),
      data.idealCustomer || '',
      data.competitors || '',
      data.challenge || '',
      data.differentiator || '',
      data.website || '',
      data.numStrategies || 0,
      data.strategyNames || ''
    ]);
    return { success: true };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function getLogSheetUrl() {
  var props = PropertiesService.getScriptProperties();
  var sheetId = props.getProperty('LOG_SHEET_ID');
  if (sheetId) {
    return 'https://docs.google.com/spreadsheets/d/' + sheetId;
  }
  return null;
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
