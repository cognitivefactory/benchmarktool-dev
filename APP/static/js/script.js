function getData() {
    alert("ok");
    var outputData = '/.bashrc';
    $.post("/postmethod", {
        data: JSON.stringify(outputData)
    }, function (err, req, resp) {
        window.location.href = "/resultats";
    });
}

$('#validation').click=function() { alert("ok")};

    