$(document).ready(function () {
    // Function to enable/disable filter button
    function toggleFilterButton() {
        var stateSelected = $('.select-btn.state select').val() !== 'All States';
        var facilitySelected = $('.select-btn.facilities select').val() !== 'All Facilities';
        var pdfButton = $('#export-pdf');
        var excelButton = $('#downloadexcel');

        // Enable or disable export buttons based on the filter button's status
        pdfButton.prop('disabled', !(stateSelected || facilitySelected));
        excelButton.prop('disabled', !(stateSelected || facilitySelected));
    }

    // Update facility choices based on the selected state
    $('.select-btn.state select').change(function () {
        var stateId = $(this).val();
        $.ajax({
            url: '/get_facilities/',
            data: {
                'state_id': stateId
            },
            dataType: 'json',
            success: function (data) {
                var facilitySelect = $('.select-btn.facilities select');
                facilitySelect.empty();
                facilitySelect.append('<option value="All Facilities">All Facilities</option>');
                $.each(data.facilities, function (key, value) {
                    facilitySelect.append('<option value="' + key + '">' + value + '</option>');
                });

                // Check and toggle the filter button when the state changes
                toggleFilterButton();
            }
        });
    });

    // Check and toggle the filter button when the facility changes
    $('.select-btn.facilities select').change(function () {
        toggleFilterButton();
    });

    // Toggle the filter button when it's clicked
    $('.sbt-button').click(function () {
        toggleFilterButton();

        // Check if the filter button is now enabled (indicating the filter is applied)
        if (!$('.sbt-button').prop('disabled')) {
            $('.age-count-headers').show();
        } else {
            $('.age-count-headers').hide();
        }
    });

    // Initial check and toggle when the page loads
    toggleFilterButton();
});
