function changeField(selectObject) {
/*
 Dynamically handles changing input field of search page

 Args:
    selectObject: select button attribute using `this`
                enables checking value of option
*/

    var selected_option = selectObject.value; 
    var url_div = document.getElementById("url-div")
    var upload_div = document.getElementById("upload-div")
    // console.log("Selected option ->" + selected_option)

    if (selected_option==="url") {
        url_div.style.display = `inline-block`;
        upload_div.style.display = `none`;
    }
    else if (selected_option==="upload") {
        url_div.style.display = `none`;
        upload_div.style.display = `inline-block`;
    }
    
}

