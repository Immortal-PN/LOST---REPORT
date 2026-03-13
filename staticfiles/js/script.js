document.addEventListener("DOMContentLoaded", function(){

const imageInput = document.getElementById("imageInput");

if(imageInput){

imageInput.addEventListener("change", function(){

const file = this.files[0];

if(file && file.size > 2 * 1024 * 1024){

alert("Image must be under 2MB");

this.value="";

}

});

}

});