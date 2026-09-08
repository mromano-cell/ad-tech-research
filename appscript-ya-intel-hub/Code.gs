function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('YA Competitive Intel Hub')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
