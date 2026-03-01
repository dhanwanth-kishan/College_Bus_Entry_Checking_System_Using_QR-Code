const scanBtn = document.getElementById("scan-btn");
const reader = document.getElementById("reader");
const resultDiv = document.getElementById("result");

let scanner = null;
let isProcessing = false;

function startScanner() {
  if (!scanner) {
    scanner = new Html5Qrcode("reader");
  }

  scanner.start(
    { facingMode: "environment" },
    {
      fps: 25,
      qrbox: { width: 280, height: 280 }
    },
    onScanSuccess,
    () => {}
  ).catch(err => {
    console.log("Camera start error:", err);
  });
}

function onScanSuccess(decodedText) {
  if (isProcessing) return;
  isProcessing = true;

  console.log("Decoded:", decodedText);

  scanner.pause(true);

  fetch(`/Bus_App/scan-result/?student_id=${decodedText}`)
    .then(res => res.text())
    .then(html => {
      resultDiv.innerHTML = html;
      resultDiv.className = "success";

      setTimeout(() => {
        resultDiv.innerHTML = "";
        resultDiv.className = "";
        isProcessing = false;
        scanner.resume();
      }, 6000);
    })
    .catch(() => {
      resultDiv.innerHTML = "<p style='color:red;'>Server error</p>";
      resultDiv.className = "error";

      setTimeout(() => {
        resultDiv.innerHTML = "";
        resultDiv.className = "";
        isProcessing = false;
        scanner.resume();
      }, 4000);
    });
}

scanBtn.onclick = function () {
  reader.style.display = "block";
  scanBtn.style.display = "none";
  startScanner();
};