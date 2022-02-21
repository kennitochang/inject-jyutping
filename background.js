try{
  self.importScripts("lib/browser-polyfill.js", "lib/MessageManager.js", "lib/Trie.js", "background_scripts/main.js")
} catch (e) {
  console.log("Error: ", e);
}
