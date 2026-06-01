import { app } from "electron";
import fs from "fs";
import path from "path";

export async function saveCV(file: File) {
  const buffer = Buffer.from(await file.arrayBuffer());

  const dir = path.join(app.getPath("documents"), "cv-storage");
  await fs.promises.mkdir(dir, { recursive: true });

  const filePath = path.join(dir, file.name);

  await fs.promises.writeFile(filePath, buffer);

  return filePath;
}