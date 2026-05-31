const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  saveFile: (fileName: string, fileBuffer: ArrayBuffer) =>
    ipcRenderer.invoke('save-file', fileName, fileBuffer)
})