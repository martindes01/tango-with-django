$(document).ready(function() {
    $("#about-btn").click(function() {
        $("#msg").append("ooo");
    });

    $("p:nth-last-child(2):first").hover(
        function() {
            $(this).css('color', 'red');
        },
        function() {
            $(this).css('color', 'blue');
        }
    );
});
