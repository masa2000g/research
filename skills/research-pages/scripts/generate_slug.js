#!/usr/bin/env node

const fs = require('fs');

function slugify(str) {
  return str
    .toString()
    .trim()
    .toLowerCase()
    // 日本語などは一旦削除して、スペースをハイフンに
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    || 'page';
}

if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: generate_slug.js <title>');
    process.exit(1);
  }
  process.stdout.write(slugify(input));
}

module.exports = { slugify };
