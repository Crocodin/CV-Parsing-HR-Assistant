import { app, BrowserWindow } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url'
import fs from 'fs'
import { ipcMain } from 'electron'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Handle file saving from the renderer process
ipcMain.handle('save-file', async (event, fileName: string, fileBuffer: ArrayBuffer) => {
  const savePath = path.join(app.getPath('userData'), 'cvs', fileName)
  await fs.promises.mkdir(path.dirname(savePath), { recursive: true })
  fs.writeFileSync(savePath, Buffer.from(fileBuffer))
  return savePath
})

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    }
  })
  console.log('NODE_ENV:', process.env.NODE_ENV)

  // in dev load Vite dev server
  if (process.env.NODE_ENV === 'development') {
    win.loadURL('http://localhost:5173')
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})