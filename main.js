let pyodide = null;
let fileText = '';

async function initPyodideApp() {
  pyodide = await loadPyodide();
  const pyCode = await fetch("py/search.py").then(res => res.text());
  await pyodide.runPythonAsync(pyCode);
}

document.getElementById('fileInput').addEventListener('change', async function () {
  const file = this.files[0];
  const encoding = document.getElementById("encoding").value;
  if (file) {
    try {
      const buffer = await file.arrayBuffer();
      const decoder = new TextDecoder(encoding);
      fileText = decoder.decode(buffer);
      alert('File loaded successfully!');
    } catch (err) {
      alert('Error reading file with encoding ' + encoding);
    }
  }
});

async function runSearch() {
  const query = document.getElementById("searchInput").value.trim();
  const useBinary = document.getElementById("binaryToggle").checked;
  
  if (!fileText || !query) {
    alert("Please upload a file and enter a search query.");
    return;
  }

  pyodide.globals.set("text_data", fileText);
  pyodide.globals.set("query", query);
  pyodide.globals.set("use_binary", useBinary);

  const result = pyodide.runPython(`
from search import search_text, binary_search_text

if use_binary:
    binary_search_text(text_data, query)
else:
    search_text(text_data, query)
  `);

  document.getElementById("output").innerText = result;
}

initPyodideApp();
