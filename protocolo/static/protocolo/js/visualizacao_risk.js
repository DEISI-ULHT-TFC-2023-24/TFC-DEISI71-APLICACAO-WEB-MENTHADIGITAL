var button = document.getElementById("pdfButton");
button.addEventListener("click", function () {
    var doc = new jsPDF("p", "mm", [300, 300]);
    var makePDF = document.querySelector("#generatePdf");
    // fromHTML Method
    doc.fromHTML(makePDF);
    doc.save("Risco.pdf");
});