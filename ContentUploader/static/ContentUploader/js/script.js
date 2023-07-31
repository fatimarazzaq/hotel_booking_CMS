var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 500);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("main-page").style.display = "block";
}


const lines = document.querySelector('.lines');
const nav = document.querySelector('.mynav');
lines.addEventListener('click', function () {
  if (nav.classList.contains('display_block')) {
    nav.classList.remove('display_block');
  }
  else {
    nav.classList.add('display_block');
  }
})





var near_me = document.querySelector("#near_me");

near_me.addEventListener("click",function(){
  if(navigator.geolocation){
      navigator.geolocation.getCurrentPosition(getlocation,geterror);
  }else{
      console.log("Allow Location to view the content");
  }
})


function getlocation(location){
  console.log('finding');
  var lat = location.coords.latitude;
  var lon = location.coords.longitude;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
      if(this.readyState == 4 && this.status==200){
          var json_parsed = JSON.parse(this.responseText)
          console.log(json_parsed.results[1].address_components[1].long_name);
          var current_loc=json_parsed.results[1].address_components[1].long_name;
          window.location.href = `${window.location.protocol}//${window.location.host}/?location=${current_loc}`
          
      }
      // else{

      //     console.log('done');
      // }
  }
  xhr.open("GET","https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lon+"&sensor=true&key=AIzaSyD1Bftli2cVrxx0EjvqHzj_Z6LgVKM50oY");
  xhr.send();
}
function geterror(error){
  alert("Allow location to view the content")
}