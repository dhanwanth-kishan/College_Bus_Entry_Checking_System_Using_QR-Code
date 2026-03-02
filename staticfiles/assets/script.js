document.addEventListener("DOMContentLoaded", () => {
    const scanBtn = document.getElementById("scan-btn");
    const reader = document.getElementById("reader");
    const resultDiv = document.getElementById("result");

    let scanner = null;
    let isProcessing = false;

    if (scanBtn) {
        scanBtn.addEventListener("click", () => {
            scanBtn.style.display = "none";
            startScanner();
        });
    }

    function startScanner() {
        if (!scanner) {
            scanner = new Html5Qrcode("reader");
        }

        scanner.start(
            { facingMode: "environment" },
            {
                fps: 25,
                qrbox: { width: 250, height: 250 }
            },
            onScanSuccess,
            () => {} 
        ).catch(err => {
            console.error("Camera error:", err);
            alert("Camera access denied.");
            scanBtn.style.display = "block";
        });
    }

    function onScanSuccess(decodedText) {
        if (isProcessing) return;
        isProcessing = true;

        scanner.pause(true); 

        fetch(`/Bus_App/scan-result/?student_id=${encodeURIComponent(decodedText.trim())}`)
            .then(res => res.text())
            .then(html => {
                resultDiv.innerHTML = html;
                resultDiv.className = "success";
                setTimeout(() => {
                    resultDiv.innerHTML = "";
                    resultDiv.className = "";
                    isProcessing = false;
                    scanner.resume();
                }, 5000);
            })
            .catch(err => {
                resultDiv.innerHTML = "<p>Error connecting to server</p>";
                resultDiv.className = "error";
                setTimeout(() => {
                    resultDiv.innerHTML = "";
                    resultDiv.className = "";
                    isProcessing = false;
                    scanner.resume();
                }, 3000);
            });
    }
});
