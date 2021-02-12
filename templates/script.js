
const toggle = document.getElementById('toggle');
const close = document.getElementById('close');
const open = document.getElementById('open');
const modal = document.getElementById('modal');
const navbar = document.getElementById('navbar');


// This function closes navbar if user clicks anywhere outside of navbar once it's opened
// Does not leave unused event listeners on
// It's messy, but it works
function closeNavbar(e) {
  if (
    document.body.classList.contains('show-nav') &&
    e.target !== toggle &&
    !toggle.contains(e.target) &&
    e.target !== navbar &&
    !navbar.contains(e.target)
  ) {
    document.body.classList.toggle('show-nav');
    document.body.removeEventListener('click', closeNavbar);
  } else if (!document.body.classList.contains('show-nav')) {
    document.body.removeEventListener('click', closeNavbar);
  }
}

// Toggle nav
toggle.addEventListener('click', () => {
  document.body.classList.toggle('show-nav');
  document.body.addEventListener('click', closeNavbar);
});

// Show modal
open.addEventListener('click', () => modal.classList.add('show-modal'));

// Hide modal
close.addEventListener('click', () => modal.classList.remove('show-modal'));

// Hide modal on outside click
window.addEventListener('click', e =>
  e.target == modal ? modal.classList.remove('show-modal') : false
);



//Check input length
function checkLength(input, min, max) {
    let correct = false;
    if (input.value.length < min) {
      showError(
        input,
        `${getFieldName(input)} must be at least ${min} characters`
      );
    } else if (input.value.length > max) {
      showError(
        input,
        `${getFieldName(input)} must be less than ${max} characters`
      );
    } else {
      showSuccess(input);
      correct = true;
    }
    return correct;
  }


//=========================================================================

const form = document.getElementById('form');
const broadcastname = document.getElementById('broadcastname');
const groupid = document.getElementById('groupid');
const message = document.getElementById('message');

// Show input error message
function showError(input, message) {
  const formControl = input.parentElement;
  formControl.className = 'form-control error';
  const small = formControl.querySelector('small');
  small.innerText = message;
}

// Show success outline
function showSuccess(input) {
  const formControl = input.parentElement;
  formControl.className = 'form-control success';
}


// Check required fields
function checkRequired(inputArr) {
  let isRequired = false;
  inputArr.forEach(function(input) {
    if (input.value.trim() === '') {
      showError(input, `${getFieldName(input)} is required`);
      isRequired = true;
    } else {
      showSuccess(input);
    }
  });

  return isRequired;
}

// Get fieldname
function getFieldName(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}

// Event listeners
form.addEventListener('submit', function(e) {
  e.preventDefault();

  if(!checkRequired([broadcastname, groupid, message])){
    
    //showPosts();
    createBroadcast();
    postsContainer.innerHTML = ''; //remove all child in this div
    showPosts(); // to refresh the page
    
  }

});


const postsContainer = document.getElementById('posts-container');
const loading = document.querySelector('.loader');
const filter = document.getElementById('filter');

let login = 'veserve'
let password = 'veserve'

// Fetch posts from API
async function getPosts() {
  const res = await fetch(
    `http://178.128.107.65:4000/broadcast/get_broadcast_list`, {
      headers: {
        "Authorization": `Basic ${btoa(`${login}:${password}`)}`
    },
    }
  );

  const data = await res.json();
  //console.log(data);
  return data;
}

// Show posts in DOM
async function showPosts() {
  const posts = await getPosts();
  
  posts["data"]["broadcast_list"].forEach(post => {
    const postEl = document.createElement('div');
    postEl.classList.add('post');
    postEl.innerHTML = `
      <div class="number">${post.broadcast_id}</div>
      <div class="post-info">
        <h2 class="post-title">Broadcast name: ${post.broadcast_name}</h2>
        <p class="post-body">Message: ${post.content}</p>
        <p class="post-bodyii">Create at: ${post.start_time}</p>

        <table>
          <tr>
            <th>Total</th><th>Delivered</th><th>Received</th><th>Read</th>
          </tr>
          <tr>
            <th>${post.amount_audience}</th><th>${post.amount_deliver}</th><th>${post.amount_receive}</th><th>${post.amount_read}</th>
          </tr>
        </table>
      </div>
    `;
    //console.log(post.broadcast_name);
    postsContainer.appendChild(postEl);
  });
}

//Show loader & fetch more posts
function showLoading() {
  loading.classList.add('show');

//   setTimeout(() => {
//     loading.classList.remove('show');

//     setTimeout(() => {
//       page++;
//       showPosts();
//     }, 300);
//   }, 1000);
}

// Filter posts by input
function filterPosts(e) {
  const term = e.target.value.toUpperCase();
  const posts = document.querySelectorAll('.post');

  posts.forEach(post => {
    const title = post.querySelector('.post-title').innerText.toUpperCase();
    const body = post.querySelector('.post-body').innerText.toUpperCase();
    const bodyii = post.querySelector('.post-bodyii').innerText.toUpperCase();

    if (title.indexOf(term) > -1 || body.indexOf(term) > -1 || bodyii.indexOf(term) > -1) {
      post.style.display = 'flex';
    } else {
      post.style.display = 'none';
    }
  });
}

// Show initial posts
showPosts();

window.addEventListener('scroll', () => {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

  if (scrollTop + clientHeight >= scrollHeight - 5) {
    showLoading();
  }
});

filter.addEventListener('input', filterPosts);



// create broadcast
function createBroadcast(){
    // here it should be a form-data rather than json
    //const data_in = {"broadcast_name": broadcastname.value, "group_id":groupid.value, "status":"active", "text": message.value};
    
    let formData = new FormData();
    formData.append('broadcast_name', broadcastname.value);
    formData.append('group_id', groupid.value);
    formData.append('status', "active");
    formData.append('text', message.value);

    fetch('http://178.128.107.65:4000/broadcast/create_broadcast', {
    method: 'POST', // or 'PUT'
    headers: {
        //'Content-Type': 'multipart/form-data',  #do NOT set content-type for form-data
        "Authorization": `Basic ${btoa(`${login}:${password}`)}`
    },
    body: formData,
    })
    .then(response => response.json())
    .then(data => {
    console.log('Success:', data);
    outbound.innerHTML = JSON.stringify(data["status"]);
    if (data.status == 0){
        //alert(`[Failure]: Invalid group name: ${groupname.value}`);
        showError(
          broadcastname,
            "[Failure]"
        );
    }
    })
    .catch((error) => {
    console.error('Error:', error);
    });
}


