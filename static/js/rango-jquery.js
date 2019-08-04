$(document).ready(function() {
    $("#about-btn").click(function() {
        alert("You clicked the button using jQuery!");
    });

    $("p:last").hover(
        function() {
            $(this).css('color', 'red');
        },
        function() {
            $(this).css('color', 'blue');
        }
    );
});
