$('#LipsColor').change(function () {
    UpdateData();
});

function show_red_value(x) {
    document.getElementById("red_value").innerHTML = x;
    UpdateData();
}

function show_blue_value(x) {
    document.getElementById("blue_value").innerHTML = x;
    UpdateData();
}

function show_green_value(x) {
    document.getElementById("green_value").innerHTML = x;
    UpdateData();
}

function UpdateData() {
    let red = $("#Red").val();
    let blue = $("#Blue").val();
    let green = $("#Green").val();
    let Img = $("#Img").is(":checked");
    let Lips = $("#LipsColor").is(":checked");
    $.ajax({
        type: "POST",
        url: "",
        data: {
            Img: Img,
            Lips : Lips,
            Red:red, Blue: blue, Green: green
        },
        success: function (result) {
            // alert("Success");
        }
    });
}