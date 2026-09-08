function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Hello World Test')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
