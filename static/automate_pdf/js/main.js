let step = 1;
let pdfImg = $("#pdfImg");
let pdfInvite, namesInvite, height, width;
let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

function getSample(){

}

$(document).ready(
    function (e) {
        $('#nextButton').click(function () {
            if(step === 1){
                $('#step1').css("display", "none");
                $('#step2').css("display", "block");

                step += 1; // go to next step

            }
            else if (step === 2){
                $('#step2').css("display", "none");

                // get uploaded pdf file
                pdfInvite = $("#invite").prop('files')[0];
                namesInvite = $("#invitees").prop('files')[0];

                // Create a json form data to send data to server
                let formData = new FormData();
                formData.append('file', pdfInvite);
                formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

                // Make a Post request to get an image of the pdf
                $.ajax({
                    type: 'POST',
                    url: '/get_position/',
                    data: formData,
                    async: true,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        resp = JSON.parse(resp);
                        if (resp.status === 'OK'){
                            console.log(resp);
                            pdfImg.attr("src", resp.src);
                            pdfImg.attr("width", resp.width);
                            pdfImg.attr('height', resp.height);
                            width = parseFloat(resp.width);
                            height = parseFloat(resp.height);
                            $('#step3').css("display", "block");
                        }

                        else{
                            console.log("[Error]: " + resp);
                        }
                    }
                });

                step += 1; // We go to the next step
            }
            else{
                let formData = new FormData();
                formData.append('invite', pdfInvite);
                formData.append('invitees', namesInvite);
                formData.append('x-coords', x_coord.toString());
                formData.append('y-coords', (height-y_coord).toString());
                formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
                $.ajax({
                    type: 'POST',
                    url: '/automate/',
                    data: formData,
                    async: true,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        resp = JSON.parse(resp);
                        if (resp.status === 'OK'){
                            console.log(resp);
                        }

                        else{
                            console.log("[Error]: " + resp);
                        }
                    }
                });
            }
        })
    }
);