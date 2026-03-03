document.addEventListener("DOMContentLoaded", () => {

    const scanBtn = document.getElementById("scan-btn");
    const reader = document.getElementById("reader");
    const resultDiv = document.getElementById("result");

    let scanner = null;

    scanBtn.onclick = () => {
        scanBtn.style.display = "none";
        reader.style.display = "block";

        scanner = new Html5Qrcode("reader");

        scanner.start(
            { facingMode: "environment" },
            { fps: 20, qrbox: 250 },
            (decodedText) => {

                scanner.pause();

                fetch(`/Bus_App/scan_result/?student_id=${decodedText}`)
                    .then(res => res.json())
                    .then(data => {

                        console.log("Server Response:", data);

                        if (data.status === "error") {
                            Swal.fire("Denied", data.message, "error")
                                .then(() => scanner.resume());
                            return;
                        }

                        Swal.fire("Success", "Entry Allowed", "success");

                        resultDiv.innerHTML = `
                            <div class="alert alert-success mt-3">
                                <b>${data.student.name}</b><br>
                                ID: ${data.student.id}<br>
                                Bus: ${data.student.bus}<br>
                                Dept: ${data.student.department}
                            </div>
                        `;

                        setTimeout(() => scanner.resume(), 1500);

                    })
                    .catch(err => {
                        console.error(err);
                        Swal.fire("Server Error", "Try again", "error");
                        scanner.resume();
                    });
            }
        );

    };

});