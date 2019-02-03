function changeField(selectObject) {
/*
 Dynamically handles changing input field of search page

 Args:
    selectObject: select button attribute using `this`
                enables checking value of option
*/
    var selected_option = selectObject.value; 
    console.log("Selected option ->" + selected_option)

    var url_div = document.getElementById("url-div")
    var upload_div = document.getElementById("upload-div")
    var camera_div = document.getElementById("camera-div")


    if (selected_option==="url") {
        url_div.style.display = `inline-block`;
        upload_div.style.display = `none`;
        camera_div.style.display = `none`;

    }
    else if (selected_option==="upload") {
        upload_div.style.display = `inline-block`;
        url_div.style.display = `none`;
        camera_div.style.display = `none`;

    }
    else if (selected_option==="camera") {
        camera_div.style.display = `inline-block`;
        upload_div.style.display = `none`;
        url_div.style.display = `none`;

    }
    
}
