const table = document.querySelector('table');

// Add click event listeners after the table variable is defined
document.getElementById('export-pdf').addEventListener('click', () => {
    // Create a new jsPDF instance
    const pdf = new jsPDF();

    // Add the table to the PDF with a specified margin and position
    pdf.autoTable({ html: table, margin: { top: 20 } });

    // Save the PDF as a file
    pdf.save('table.pdf');
});

document.getElementById('export-excel').addEventListener('click', () => {
    // Use the TableExport library to export the table as Excel
    const tableExport = TableExport(table, {
        formats: ['xlsx'],
        exportButtons: false,
        xlsx: {
            mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            fileExtension: '.xlsx'
        }
    });

    const exportData = tableExport.getExportData();
    const xlsxData = exportData[table.id].xlsx;
    const blob = new Blob([xlsxData], { type: xlsxData.mimeType });

    const fileName = 'table.xlsx';
    if (navigator.msSaveBlob) {
        // For IE 10 and above
        navigator.msSaveBlob(blob, fileName);
    } else {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
    }
});