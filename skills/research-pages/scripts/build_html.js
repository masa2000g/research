#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function buildHtml(title, htmlContent, templatePath) {
  const template = fs.readFileSync(templatePath, 'utf8');
  return template
    .replace(/{{TITLE}}/g, title)
    .replace('{{CONTENT}}', htmlContent);
}

if (require.main === module) {
  const [title, inputPath, outputPath] = process.argv.slice(2);
  if (!title || !inputPath || !outputPath) {
    console.error('Usage: build_html.js <title> <input-html-path> <output-html-path>');
    process.exit(1);
  }

  const templatePath = path.join(__dirname, '..', 'assets', 'base-template.html');
  const content = fs.readFileSync(inputPath, 'utf8');
  const html = buildHtml(title, content, templatePath);
  fs.writeFileSync(outputPath, html, 'utf8');
}

module.exports = { buildHtml };
