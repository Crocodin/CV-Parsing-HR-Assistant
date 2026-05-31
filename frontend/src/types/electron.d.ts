export {}

declare global {
  interface Window {
    electronAPI?: {
      saveFile: (fileName: string, fileBuffer: ArrayBuffer) => Promise<string>
    }
  }
}