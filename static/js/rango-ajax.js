$(document).ready(function() {
    $("#likes").click(function() {
        // Retrieve category ID
        var catid = $(this).attr("data-catid");

        // Make AJAX GET request to /rango/like/ containing category ID
        $.get(
            "/rango/like/",
            {
                category_id: catid
            },
            function(data) {
                // Print number of likes
                $("#like_count").html(data);

                // Hide like button
                $("#likes").hide();
            }
        );
    });
});
