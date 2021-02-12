// const navbar = document.getElementById('navbar');


// // This function closes navbar if user clicks anywhere outside of navbar once it's opened
// // Does not leave unused event listeners on
// // It's messy, but it works
// function closeNavbar(e) {
//   if (
//     document.body.classList.contains('show-nav') &&
//     e.target !== toggle &&
//     !toggle.contains(e.target) &&
//     e.target !== navbar &&
//     !navbar.contains(e.target)
//   ) {
//     document.body.classList.toggle('show-nav');
//     document.body.removeEventListener('click', closeNavbar);
//   } else if (!document.body.classList.contains('show-nav')) {
//     document.body.removeEventListener('click', closeNavbar);
//   }
// }

// // Toggle nav
// toggle.addEventListener('click', () => {
//   document.body.classList.toggle('show-nav');
//   document.body.addEventListener('click', closeNavbar);
// });






async function getResult() {
    var locationName = document.getElementById('locname').value;
    localStorage.setItem("locationName", locationName);
    const res = await fetch(
        'http://localhost:4000/search/'+locationName
    );

    const data = await res.json();
    console.log(data);
    
    // data["locations"].forEach(element => {
    //     response += `<p>${element}</p>`
    // });
    //data["locations"]
    document.getElementById("result").innerHTML ="hongkong-Tokyo"
    return data;
}

function showMap() { 
    if (typeof(Storage) !== "undefined") {
        var location = localStorage.getItem("locationName");
        console.log(location);
        
        document.getElementById("result").innerHTML = location; //it works
        window.open( 
        "http://localhost:4000/map/"+location, "_blank");
    } else {
        document.getElementById("result").innerHTML = "Sorry, your browser does not support Web Storage...";
    }
}
// //Check input length
// function checkLength(input, min, max) {
//     let correct = false;
//     if (input.value.length < min) {
//       showError(
//         input,
//         `${getFieldName(input)} must be at least ${min} characters`
//       );
//     } else if (input.value.length > max) {
//       showError(
//         input,
//         `${getFieldName(input)} must be less than ${max} characters`
//       );
//     } else {
//       showSuccess(input);
//       correct = true;
//     }
//     return correct;
//   }


//=========================================================================

//const form = document.getElementById('form');
// const broadcastname = document.getElementById('broadcastname');
// const groupid = document.getElementById('groupid');
// const message = document.getElementById('message');

// // Show input error message
// function showError(input, message) {
//   const formControl = input.parentElement;
//   formControl.className = 'form-control error';
//   const small = formControl.querySelector('small');
//   small.innerText = message;
// }

// // Show success outline
// function showSuccess(input) {
//   const formControl = input.parentElement;
//   formControl.className = 'form-control success';
// }


// // Check required fields
// function checkRequired(inputArr) {
//   let isRequired = false;
//   inputArr.forEach(function(input) {
//     if (input.value.trim() === '') {
//       showError(input, `${getFieldName(input)} is required`);
//       isRequired = true;
//     } else {
//       showSuccess(input);
//     }
//   });

//   return isRequired;
// }

// // Get fieldname
// function getFieldName(input) {
//   return input.id.charAt(0).toUpperCase() + input.id.slice(1);
// }

// // Event listeners
// form.addEventListener('submit', function(e) {
//   e.preventDefault();

//   if(!checkRequired([broadcastname, groupid, message])){
    
//     //showPosts();
//     createBroadcast();
//     postsContainer.innerHTML = ''; //remove all child in this div
//     showPosts(); // to refresh the page
    
//   }

// });


//const postsContainer = document.getElementById('posts-container');


// let login = 'veserve'
// let password = 'veserve'

// // Fetch posts from API
// async function getPosts() {
//   const res = await fetch(
//     `http://178.128.107.65:4000/broadcast/get_broadcast_list`, {
//       headers: {
//         "Authorization": `Basic ${btoa(`${login}:${password}`)}`
//     },
//     }
//   );

//   const data = await res.json();
//   //console.log(data);
//   return data;
// }




// window.addEventListener('scroll', () => {
//   const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
// });



