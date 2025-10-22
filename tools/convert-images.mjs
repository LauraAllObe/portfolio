import sharp from 'sharp';
import {globby} from 'globby';
import {dirname, join, parse} from 'node:path';
import {mkdir} from 'node:fs/promises';

const files = await globby(['static/**/*.{jpg,jpeg,png}']);
for (const file of files) {
  const {dir, name} = parse(file);
  const outDir = dir; // write next to originals
  await mkdir(outDir, {recursive: true});

  const img = sharp(file).rotate(); // auto-orient

  // AVIF
  await img.clone().avif({quality: 50, effort: 4}).toFile(join(outDir, `${name}.avif`));
}
console.log('Done.');
