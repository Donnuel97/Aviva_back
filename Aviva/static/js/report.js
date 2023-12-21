document.getElementById('downloadexcel').addEventListener('click', function () {
    var table2excel = new Table2Excel();
    table2excel.export(document.getElementById("table"));
});

window.onload = function () {
    document.getElementById("export-pdf").addEventListener("click", () => {
        const table = this.document.getElementById("table");

        var currentDate = new Date();
        var dateString =
            currentDate.getFullYear() +
            '-' +
            ('0' + (currentDate.getMonth() + 1)).slice(-2) +
            '-' +
            ('0' + currentDate.getDate()).slice(-2) +
            '_' +
            ('0' + currentDate.getHours()).slice(-2) +
            '-' +
            ('0' + currentDate.getMinutes()).slice(-2);

        var filename = 'Report_' + dateString + '.pdf';

        var opt = {
            margin: 1,
            filename: filename,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
            useCss: true, // Use existing CSS styles
        };

        html2pdf().from(table).set(opt).save();
    });
};

